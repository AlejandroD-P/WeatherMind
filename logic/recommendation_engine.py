from models.weather_data import WeatherData
from models.recommendation import Recommendation
from logic.risk_calculator import calculate_risk


def generate_recommendation(weather: WeatherData, activity: str) -> Recommendation:
    risk = calculate_risk(weather)

    if risk == "Bajo":
        return Recommendation(
            risk_level="Bajo",
            status="Recomendado",
            message=f"Las condiciones son favorables para realizar {activity.lower()}."
        )

    if risk == "Moderado":
        return Recommendation(
            risk_level="Moderado",
            status="Precaución",
            message=f"Puedes realizar {activity.lower()}, pero considera protección solar, hidratación y revisar cambios del clima."
        )

    return Recommendation(
        risk_level="Alto",
        status="No recomendable",
        message=f"No se recomienda realizar {activity.lower()} debido a condiciones meteorológicas de riesgo."
    )