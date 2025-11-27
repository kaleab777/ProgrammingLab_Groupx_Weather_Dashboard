from database import init_db, save_record_to_db, get_city_rows
from fetcher import fetch_weather, get_coordinates_for_city
from visual import plot_temperature_rows


def main():
    # 1. Choose a database file
    db_path = "data/weather.db"

    # 2. Initialize the DB (creates file + table only if missing)
    init_db(db_path)

    # 3. Define the cities you want to fetch (list of names)
    cities = ["Nairobi", "Cairo", "Lagos", "Johannesburg", "Casablanca"]

    # 4. Fetch + save each city
    for city in cities:
        coords = get_coordinates_for_city(city)
        if not coords:
            print(f"Could not find coordinates for {city}, skipping.")
            continue
        lat, lon = coords["latitude"], coords["longitude"]
        print(f"Fetching {city} ({lat}, {lon})...")
        record = fetch_weather(city, lat, lon)
        print("Fetched:", record)

        if record:
            ok = save_record_to_db(record, db_path)
            print("Save OK:", ok)

    # 5. Query back and visualize each city
    for city in cities:
        rows = get_city_rows(city, db_path)
        print(f"{city} rows:", rows[:5])

        if rows:
            plot_path = plot_temperature_rows(rows, city)
            print(f"Plot saved → {plot_path}")

    print("Done.")


if __name__ == "__main__":
    main()
