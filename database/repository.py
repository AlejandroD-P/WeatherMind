from database.db import get_connection


def save_history(
        date,
        city,
        activity,
        weather,
        recommendation
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO history(

        date,
        city,
        activity,
        temperature,
        humidity,
        wind,
        uv,
        precipitation,
        risk,
        recommendation

    )

    VALUES(?,?,?,?,?,?,?,?,?,?)

    """,

    (

        date,
        city,
        activity,

        weather.temperature,
        weather.humidity,
        weather.wind_speed,
        weather.uv_index,
        weather.precipitation_probability,

        recommendation.risk_level,

        recommendation.message

    )

    )

    conn.commit()

    conn.close()


def get_last_history(limit=10):

    conn=get_connection()

    cursor=conn.cursor()

    cursor.execute("""

    SELECT

    date,
    city,
    activity,
    temperature,
    risk

    FROM history

    ORDER BY id DESC

    LIMIT ?

    """,(limit,))

    rows=cursor.fetchall()

    conn.close()

    return rows

def clear_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()

def get_filtered_history(activity=None, risk=None, limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT date, city, activity, temperature, risk FROM history WHERE 1=1"
    params = []

    if activity and activity != "Todas":
        query += " AND activity = ?"
        params.append(activity)

    if risk and risk != "Todos":
        query += " AND risk = ?"
        params.append(risk)

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()
    return rows