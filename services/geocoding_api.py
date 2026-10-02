import urllib.parse
import urllib.request
import json

def get_coordinates(city_name):
    # Si llega una tupla, desempaquetar o convertir a texto
    if isinstance(city_name, (tuple, list)):
        city_name = city_name[0] if city_name else ""
    city_name = str(city_name).strip()
    
    if not city_name:
        return None

    # Codificar la ciudad y pedir hasta 5 resultados en español
    encoded_city = urllib.parse.quote(city_name.strip())
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_city}&count=5&language=es&format=json"

    try:
        req = urllib.request.Request(
            url, 
            headers={"User-Agent": "WeatherMindApp/1.0 (Python)"}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status != 200:
                return None
            data = json.loads(response.read().decode("utf-8"))

        results = data.get("results")
        if not results:
            return None

        # Si el usuario es de México o busca ciudades latinas, priorizar match con país
        best_match = results[0]
        for res in results:
            country = res.get("country", "")
            if "Mexico" in country or "México" in country:
                best_match = res
                break

        lat = best_match.get("latitude")
        lon = best_match.get("longitude")
        name = best_match.get("name", city_name)
        country = best_match.get("country", "")
        admin1 = best_match.get("admin1", "")

        # Formato limpio: "Monterrey, Nuevo León, México"
        parts = [p for p in [name, admin1, country] if p]
        display_name = ", ".join(parts) if parts else name

        return (lat, lon, display_name, country)

    except Exception as e:
        print(f"Error en geocoding_api: {e}")
        return None