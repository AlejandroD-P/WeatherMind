import os
import joblib
import pandas as pd
from models.recommendation import Recommendation

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "activity_classifier.joblib")

ACTIVITY_MAP = {
    "Senderismo": 0,
    "Ciclismo": 1,
    "Paseo": 2,
    "Campamento": 0,
    "Camping": 0,
    "Viaje por carretera": 1,
    "Carretera": 1,
    "Correr": 1,
    "Picnic": 2
}

_model = None
if os.path.exists(MODEL_PATH):
    try:
        _model = joblib.load(MODEL_PATH)
    except Exception:
        _model = None

def _extract_val(weather_data, attr_name, default=0.0):
    val = weather_data.get(attr_name, default) if isinstance(weather_data, dict) else getattr(weather_data, attr_name, default)
    try:
        return float(val) if val is not None else float(default)
    except (ValueError, TypeError):
        return float(default)

def generate_recommendation(activity_name: str, weather_data):
    t = _extract_val(weather_data, "temperature", 20.0)
    h = _extract_val(weather_data, "humidity", 50.0)
    w = _extract_val(weather_data, "wind_speed", 10.0)
    p = _extract_val(weather_data, "precipitation", 0.0)
    press = _extract_val(weather_data, "pressure", 1013.2)
    if press == 0.0:
        press = 1013.2

    act_idx = int(ACTIVITY_MAP.get(activity_name, 0))

    pred_class = 0
    confidence = 0.0

    if _model is not None:
        try:
            cols = ["temperature", "humidity", "wind_speed", "precipitation", "pressure", "activity"]
            df_row = pd.DataFrame([[t, h, w, p, press, act_idx]], columns=cols)
            
            # 1. Predicción de clase
            pred_class = int(_model.predict(df_row)[0])
            
            # 2. Extraer el porcentaje de confianza
            probabilidades = _model.predict_proba(df_row)[0]
            confidence = float(max(probabilidades))
        except Exception:
            pred_class = 2 if (press < 995.0 or w > 45.0 or p > 5.0) else (1 if w > 25.0 else 0)
            confidence = 0.2 if pred_class == 2 else (0.5 if pred_class == 1 else 0.9)
    else:
        pred_class = 2 if (press < 995.0 or w > 45.0 or p > 5.0) else (1 if w > 25.0 else 0)
        confidence = 0.2 if pred_class == 2 else (0.5 if pred_class == 1 else 0.9)
        
    # Definir umbrales de tolerancia dinámicos según la actividad (Alineado con el if/else de arriba)
    max_t, min_t = 32.0, 10.0
    max_w = 25.0
    max_p = 0.5
    max_h = 80.0

    if activity_name == "Viaje por carretera":
        max_t, min_t = 40.0, -5.0  # En auto el clima afecta poco
        max_w = 60.0               # Solo vientos muy fuertes desestabilizan
        max_p = 10.0               # Solo lluvia torrencial afecta la visibilidad
        max_h = 100.0              # La humedad no importa dentro del auto
    elif activity_name in ["Ciclismo", "Carrera al aire libre"]:
        max_w = 20.0               # El viento en contra es crítico
        max_p = 0.5                # Piso resbaladizo
    elif activity_name in ["Campamento", "Camping"]:
        min_t = 5.0                # Se puede acampar con frío con buen equipo
        max_p = 2.0                # Lluvia ligera es tolerable en tienda

    # Evaluar razones reales de peligro
    reasons = []
    if t > max_t: reasons.append(f"temperatura extrema ({t}°C)")
    elif t < min_t: reasons.append(f"temperatura muy baja ({t}°C)")
    if w > max_w: reasons.append(f"viento de precaución ({w} km/h)")
    if p > max_p: reasons.append(f"lluvia ({p} mm)")
    if h > max_h: reasons.append(f"humedad incómoda ({h}%)")

    # --- FILTRO CORRECTIVO (OVERRIDE) DE LA IA ---
    if not reasons and pred_class == 2:
        pred_class = 0
        confidence = 0.85
    elif len(reasons) >= 2 or (p > max_p * 1.5) or (w > max_w * 1.2):
        pred_class = 2
        confidence = 0.90
    elif len(reasons) == 1 and pred_class == 0:
        pred_class = 1

    justification = f"Factores observados: {', '.join(reasons)}." if reasons else "Condiciones ideales para esta actividad."

#  CÁLCULO DE HORARIO Y DÍA ÓPTIMO
    optimal_msg = ""
    if _model is not None:
        cols = ["temperature", "humidity", "wind_speed", "precipitation", "pressure", "activity"]
        
        # 1. Evaluar el mejor bloque de hora (Dinámico por actividad)
        best_hour, best_h_conf = None, -1.0
        
        # Definir qué actividades exigen estrictamente luz de día
        requiere_luz = activity_name in ["Senderismo", "Ciclismo", "Caminata", "Carrera al aire libre"]
        
        if hasattr(weather_data, "hourly_forecast") and weather_data.hourly_forecast:
            for f in weather_data.hourly_forecast:
                time_str = str(f.get("time"))
                
                try:
                    hour = int(time_str[11:13])
                except (ValueError, IndexError):
                    hour = 12
                
                # Si exige luz y es de noche, saltar esta hora
                if requiere_luz and not (7 <= hour <= 17):
                    continue
                    
                df_h = pd.DataFrame([[f.get("temperature", 20.0), f.get("humidity", 50.0), f.get("wind_speed", 10.0), f.get("precipitation", 0.0), f.get("pressure", 1013.2), act_idx]], columns=cols)
                prob_0 = _model.predict_proba(df_h)[0][0]
                
                # Penalizar ligeramente el viaje por carretera si es de noche (riesgo visual/accidentes)
                if activity_name == "Viaje por carretera" and not (6 <= hour <= 18):
                    prob_0 -= 0.15
                    
                if prob_0 > best_h_conf:
                    best_h_conf = prob_0
                    best_hour = time_str.replace("T", " a las ")
                    
        # 2. Evaluar el mejor día
        best_day, best_d_conf = None, -1.0
        if hasattr(weather_data, "daily_forecast") and weather_data.daily_forecast:
            for f in weather_data.daily_forecast:
                df_d = pd.DataFrame([[f.get("temperature", 20.0), f.get("humidity", 50.0), f.get("wind_speed", 10.0), f.get("precipitation", 0.0), f.get("pressure", 1013.2), act_idx]], columns=cols)
                prob_0 = _model.predict_proba(df_d)[0][0]
                if prob_0 > best_d_conf:
                    best_d_conf = prob_0
                    best_day = f.get("time")

        if best_hour and best_day:
            optimal_msg = f"\n\nHorario óptimo próximo: {best_hour} ({int(best_h_conf*100)}% viable).\nDía ideal de la semana: {best_day}."

    if pred_class == 0:
        level = "Bajo"
        status = "Recomendado"
        msg = f"Recomendado para {activity_name}. {justification}{optimal_msg}"
        color = "#27ae60"
    elif pred_class == 1:
        level = "Moderado"
        status = "Precaución"
        msg = f"Precaución al realizar {activity_name}. {justification} Tome previsiones antes de salir.{optimal_msg}"
        color = "#f39c12"
    else:
        level = "Alto"
        status = "No Recomendado"
        msg = f"No recomendado para {activity_name}. {justification} Condiciones climáticas desfavorables o de riesgo.{optimal_msg}"
        color = "#c0392b"

    rec_obj = Recommendation(risk_level=level, status=status, message=msg)
    rec_obj.color = color
    rec_obj.confidence = confidence
    rec_obj.best_day = best_day if best_day else "" # Nueva línea para enviar a la interfaz
    return rec_obj