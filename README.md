# WeatherMind 🌤️🤖

**WeatherMind** es una aplicación de escritorio desarrollada en Python que combina el consumo en tiempo real de APIs meteorológicas abiertas con un modelo predictivo de aprendizaje automático (*Machine Learning*) para evaluar condiciones climáticas y generar recomendaciones contextuales de riesgo según la actividad seleccionada.

---

## 🛠️ Arquitectura y Tecnologías

- **Interfaz de Usuario (UI)**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (diseño moderno con soporte de modo oscuro).
- **Servicios Externos**: 
  - *Open-Meteo Geocoding API* (geolocalización con resolución priorizada para México y Latinoamérica).
  - *Open-Meteo Forecast API* (temperatura, precipitación, viento, humedad, UV, presión atmosférica).
- **Motor Predictivo de IA**: 
  - `Scikit-Learn` (`RandomForestClassifier`) serializado con `joblib`.
  - Clasificación de nivel de riesgo (`Bajo`, `Moderado`, `Alto`) y generación de justificaciones explicativas contextuales.
- **Persistencia**: `SQLite3` (almacenamiento transaccional local del historial de consultas).
- **Pruebas Automatizadas**: `unittest`.

---

## 📁 Estructura del Proyecto

```text
WeatherMind/
├── app/                  # Configuración global, constantes y logger
├── assets/               # Recursos visuales e íconos
├── database/             # Conexión SQLite y capa de acceso a datos (repository)
├── logic/                # Motor de recomendación e inferencia de IA
├── models/               # Dataclasses (WeatherData, Recommendation, Activity)
├── services/             # Integración con APIs de geocodificación y pronóstico
├── ui/                   # Paneles y orquestador principal (main_window)
├── tests/                # Pruebas unitarias de integración
├── dataset_entrenamiento.csv
├── train_classifier.py   # Script de entrenamiento del modelo ML
├── main.py               # Punto de entrada de la aplicación
└── requirements.txt