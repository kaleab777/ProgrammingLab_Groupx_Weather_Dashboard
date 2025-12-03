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
        windspeed_ms REAL,
        humidity_percent REAL,
        cloudcover_percent REAL,
        weather_code INTEGER
    )
""")

    conn.commit()

    # Migration: ensure humidity_percent and cloudcover_percent exist for older DB files
    cursor.execute("PRAGMA table_info('weather')")
    existing_cols = [row[1] for row in cursor.fetchall()]
    if 'humidity_percent' not in existing_cols:
        cursor.execute("ALTER TABLE weather ADD COLUMN humidity_percent REAL")
    if 'cloudcover_percent' not in existing_cols:
        cursor.execute(
            "ALTER TABLE weather ADD COLUMN cloudcover_percent REAL")

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

    # Insert record including humidity and cloudcover so the DB stores those extra fields
    cursor.execute("""
        INSERT INTO weather (city, timestamp, temperature_c, windspeed_ms, humidity_percent, cloudcover_percent)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        record["city"],
        record["timestamp"],
        record.get("temperature_c"),
        record.get("windspeed_ms"),
        record.get("humidity_percent"),
        record.get("cloudcover_percent")
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


def get_city_rows(city: str, db_path="data/weather.db", limit: int = 20):
    """
    Read stored weather measurements for a given city.

    Pipeline role:
      - QUERY: get data from SQLite so the visualization can use it.

    Returns:
      list of (timestamp_str, temperature_float) tuples.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        SELECT timestamp, temperature_c
        FROM weather
        WHERE city = ?
        ORDER BY timestamp ASC
        LIMIT ?
    """, (city, limit))

    rows = cur.fetchall()

    conn.close()
    return rows
