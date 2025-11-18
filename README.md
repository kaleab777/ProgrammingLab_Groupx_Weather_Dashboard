# ProgrammingLab_GroupX_Weather_Dashboard

A lightweight interactive dashboard that fetches current weather and 7-day forecasts for multiple cities, displays comparative time-series charts (temperature, precipitation), and lets users add/remove cities. Optional map view to show city locations.

---

## 🧭 Project Overview
This project is developed for the **Programming Lab – Applied Python, Open Data & Interactive Visualization** course.  
It demonstrates data handling, REST API integration, and interactive visualization using open-source tools.

---

## 🌦️ Data Sources and APIs
- **Open-Meteo API** – provides free, real-time and forecast weather data  
  https://open-meteo.com/
- (Optional) **OpenWeatherMap API** – for extended weather metrics  
  https://openweathermap.org/api

---

## 🧰 Tools & Libraries
- Python 3  
- `requests` – API data fetching  
- `sqlite3` – lightweight local database  
- `pandas` – data processing  
- `plotly` / `matplotlib` or `D3.js` – visualization  
- GitHub – collaboration & version control

---

## 👥 Team Members
- **Cinar Acar** – Database — design schema, store and query data  
- **Kaleab Tesfaye** – API & Fetcher — connect to Open-Meteo, parse JSON  
- **Mohammed Elshamy** – Visualization — create charts and prepare slides
-  ## 👥 Branching & Work Distribution Plan
- **Kaleab** → Database setup (SQLite), data handling  
  - Branch: `feature-db`

- **Teammate 2** → API integration, fetching weather data  
  - Branch: `feature-api`

- **Teammate 3** → Visualizations (Plotly or D3.js)  
  - Branch: `feature-visuals`

All work will be developed on separate branches and merged to `main` using Pull Requests after review.


**Instructor:** Prof.Dr.-Ing Mohamed Eliemy

---

## 🗂️ Folder Structure
/src → Python scripts (API, database, visualization)
/data → Datasets or cached API responses
/docs → Documentation & presentation files
