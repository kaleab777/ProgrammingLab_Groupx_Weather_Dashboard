from datetime import datetime
import matplotlib.pyplot as plt
import os


def plot_temperature_rows(rows, city="City", save_path=None):
    """
    rows: list of (timestamp_str, temperature_float) tuples
    city: city name used for titles/filename
    save_path: optional directory to save PNG (default "data")
    Returns the path to the saved image file.
    """
    if not rows:
        raise ValueError("No rows to plot")

    # Parse timestamps (ISO 8601 string) into datetime objects
    times = [datetime.fromisoformat(ts) for ts, _ in rows]
    temps = [t for _, t in rows]

    # Make sure save folder exists
    if save_path is None:
        save_path = "data"
    os.makedirs(save_path, exist_ok=True)

    # Plot
    plt.figure(figsize=(8, 4))
    plt.plot(times, temps, marker="o", linestyle="-")
    plt.title(f"Temperature over time — {city}")
    plt.xlabel("Time (UTC)")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)
    plt.tight_layout()
    plt.gcf().autofmt_xdate()  # rotate and format x labels

    # Save file
    filename = f"temperature_{city.replace(' ', '_')}.png"
    out_path = os.path.join(save_path, filename)
    plt.savefig(out_path)
    # If you want to show interactively during demo, uncomment next line:
    # plt.show()
    plt.close()
    return out_path
