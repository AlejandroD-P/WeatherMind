import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODELS_DIR, "activity_classifier.joblib")
DATASET_PATH = os.path.join(BASE_DIR, "dataset_entrenamiento.csv")

print("[*] Generando dataset meteorológico balanceado...")
np.random.seed(42)

N = 3000
temperatures = np.random.normal(loc=22.0, scale=8.0, size=N)
humidities = np.random.uniform(20, 85, N)
wind_speeds = np.random.gamma(shape=2.0, scale=10.0, size=N)
precipitations = np.random.exponential(scale=1.2, size=N)
pressures = np.random.normal(loc=1013.0, scale=8.0, size=N)
activities = np.random.choice([0, 1, 2], size=N)

labels = []
for t, h, w, p, press, act in zip(temperatures, humidities, wind_speeds, precipitations, pressures, activities):
    if press < 995.0 or w > 50.0 or p > 10.0:
        labels.append(2)
    elif act == 0:  # Senderismo
        if 12 <= t <= 27 and w <= 22 and p <= 0.8:
            labels.append(0)
        elif 6 <= t <= 33 and w <= 38 and p <= 3.5:
            labels.append(1)
        else:
            labels.append(2)
    elif act == 1:  # Ciclismo
        if 14 <= t <= 28 and w <= 18 and p <= 0.2:
            labels.append(0)
        elif 8 <= t <= 34 and w <= 32 and p <= 2.0:
            labels.append(1)
        else:
            labels.append(2)
    else:  # Paseo
        if 15 <= t <= 26 and w <= 28 and p <= 1.2:
            labels.append(0)
        elif 10 <= t <= 32 and w <= 42 and p <= 4.0:
            labels.append(1)
        else:
            labels.append(2)

df = pd.DataFrame({
    "temperature": np.round(temperatures, 1),
    "humidity": np.round(humidities, 1),
    "wind_speed": np.round(wind_speeds, 1),
    "precipitation": np.round(precipitations, 2),
    "pressure": np.round(pressures, 1),
    "activity": activities,
    "risk_level": labels
})

df.to_csv(DATASET_PATH, index=False)
print(f"[OK] Dataset guardado: {DATASET_PATH} ({len(df)} muestras)")

X = df[["temperature", "humidity", "wind_speed", "precipitation", "pressure", "activity"]]
y = df["risk_level"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

clf = RandomForestClassifier(n_estimators=70, max_depth=7, random_state=42, n_jobs=-1)
clf.fit(X_train, y_train)

cv_scores = cross_val_score(clf, X_train, y_train, cv=5)
print(f"[OK] Validación cruzada (5 folds) - Precisión media: {cv_scores.mean() * 100:.2f}%")

y_pred = clf.predict(X_test)
print("\n--- REPORTE DE CLASIFICACIÓN ---")
print(classification_report(y_test, y_pred, target_names=["Bajo (Recomendado)", "Moderado", "Alto (No Recomendado)"]))

print("--- MATRIZ DE CONFUSIÓN ---")
print(confusion_matrix(y_test, y_pred))

joblib.dump(clf, MODEL_PATH)
print(f"\n[OK] Modelo guardado con éxito en: {MODEL_PATH}")