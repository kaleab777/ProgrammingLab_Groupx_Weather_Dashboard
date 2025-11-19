from visual import plot_temperature_rows
from database import query_weather_by_city
from database import init_db, save_record_to_db
from fetcher import fetch_weather
import sqlite3

# 1. Ensure DB exists
init_db()

# 2. Fetch a record
rec = fetch_weather("Stuttgart", 48.78, 9.18)
print("Fetched:", rec)

# 3. Save it
ok = save_record_to_db(rec)
print("Save OK:", ok)

# '# 4. Check last row
# conn = sqlite3.connect("data/weather.db")
# cur = conn.cursor()
# for row in cur.execute("SELECT * FROM weather ORDER BY id DESC LIMIT 1"):
#     print("From DB:", row)
# conn.close()

# rows = query_weather_by_city("Berlin")
# print("Berlin rows:", rows)

# rows2 = query_weather_by_city("Stuttgart")
# print("Stuttgart rows:", rows2)'

# src/test_plot.py


city = "Stuttgart"
rows = query_weather_by_city(city)   # returns list of (timestamp, temp)

print("Rows to plot:", len(rows))
out = plot_temperature_rows(rows, city=city)
print("Saved chart to:", out)
