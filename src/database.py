import sqlite3


def init_db(db_path="data/weather.db"):
    """
    Creates the SQLite database file and weather table if they don't exist.
    Simple and clean.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            timestamp TEXT,
            temperature_c REAL,
            windspeed_ms REAL
        )
    """)

    conn.commit()
    conn.close()


def save_record_to_db(record, db_path="data/weather.db"):
    """
    Saves one weather record (a dict from fetch_weather()) into the weather table.
    Returns True if successful, False otherwise.
    """
    if not record:
        return False  # nothing to save

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO weather (city, timestamp, temperature_c, windspeed_ms)
        VALUES (?, ?, ?, ?)
    """, (
        record["city"],
        record["timestamp"],
        record["temperature_c"],
        record["windspeed_ms"]
    ))

    conn.commit()
    conn.close()
    return True


def query_weather_by_city(city: str):
    """
    Read stored weather measurements for a given city.

    Pipeline role:
      - QUERY: get data from SQLite so the visualization can use it.

    Returns:
      list of (timestamp_str, temperature_float) tuples.
    """
    conn = sqlite3.connect("data/weather.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT timestamp, temperature_c
        FROM weather
        WHERE city = ?
        ORDER BY timestamp ASC
    """, (city,))

    rows = cur.fetchall()

    conn.close()
    return rows
