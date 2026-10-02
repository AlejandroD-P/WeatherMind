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
    if _model is not None:
        try:
            cols = ["temperature", "humidity", "wind_speed", "precipitation", "pressure", "activity"]
            df_row = pd.DataFrame([[t, h, w, p, press, act_idx]], columns=cols)
            pred_class = int(_model.predict(df_row)[0])
        except Exception:
            pred_class = 2 if (press < 995.0 or w > 45.0 or p > 5.0) else (1 if w > 25.0 else 0)
    else:
        pred_class = 2 if (press < 995.0 or w > 45.0 or p > 5.0) else (1 if w > 25.0 else 0)

    # Justificación detallada según las variables detectadas
    reasons = []
    if t > 30.0:
        reasons.append(f"temperatura elevada ({t}°C)")
    elif t < 10.0:
        reasons.append(f"temperatura baja ({t}°C)")
    if w > 25.0:
        reasons.append(f"ráfagas de viento considerables ({w} km/h)")
    if p > 0.5:
        reasons.append(f"presencia de lluvia ({p} mm)")
    if h > 80.0:
        reasons.append(f"humedad alta ({h}%)")

    justification = f"Factores observados: {', '.join(reasons)}." if reasons else "Condiciones estables dentro de los rangos óptimos."

    if pred_class == 0:
        level = "Bajo"
        status = "Recomendado"
        msg = f"Recomendado para {activity_name}. {justification}"
        color = "#27ae60"
    elif pred_class == 1:
        level = "Moderado"
        status = "Precaución"
        msg = f"Precaución al realizar {activity_name}. {justification} Tome previsiones antes de salir."
        color = "#f39c12"
    else:
        level = "Alto"
        status = "No Recomendado"
        msg = f"No recomendado para {activity_name}. {justification} Condiciones climáticas desfavorables o de riesgo."
        color = "#c0392b"

    rec_obj = Recommendation(risk_level=level, status=status, message=msg)
    rec_obj.color = color
    return rec_obj