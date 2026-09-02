"""
Placeholder/mock data so the frontend can be built and demoed before the
real rainfall (ConvLSTM) and flood (XGBoost) models are ready.
Replace these functions with real backend/model calls later —
the rest of the app doesn't need to change, since it just calls these functions.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

CHENNAI_CENTER = (13.0827, 80.2707)


def get_dashboard_kpis():
    """Top-level summary numbers shown in the KPI cards."""
    return {
        "rainfall_next_6h": 48.2,
        "max_rainfall": 82.7,
        "max_rainfall_time": "21:00",
        "flood_probability": 0.72,
        "risk_level": "HIGH",
        "population_exposed": 124320,
        "critical_facilities_at_risk": 37,
        "last_updated": datetime.now().strftime("%H:%M IST"),
    }


def get_rainfall_forecast(horizon_hours=6):
    """Hourly rainfall forecast for the next `horizon_hours` hours."""
    now = datetime.now()
    hours = [(now + timedelta(hours=i)).strftime("%H:%M") for i in range(1, horizon_hours + 1)]
    rng = np.random.default_rng(42)
    rainfall = np.clip(rng.normal(loc=15, scale=6, size=horizon_hours) + np.linspace(0, 10, horizon_hours), 0, None)
    return pd.DataFrame({"time": hours, "rainfall_mm": rainfall.round(1)})


def get_flood_risk_timeline(horizon_hours=6):
    """Flood risk probability over the same forecast window."""
    now = datetime.now()
    hours = [(now + timedelta(hours=i)).strftime("%H:%M") for i in range(1, horizon_hours + 1)]
    risk = np.clip(np.linspace(0.3, 0.82, horizon_hours) + np.random.default_rng(1).normal(0, 0.03, horizon_hours), 0, 1)
    return pd.DataFrame({"time": hours, "flood_probability": risk.round(2)})


def get_map_points(n_points=40):
    """Sample lat/lon grid points around Chennai with a mock flood probability each."""
    rng = np.random.default_rng(7)
    lats = CHENNAI_CENTER[0] + rng.normal(0, 0.05, n_points)
    lons = CHENNAI_CENTER[1] + rng.normal(0, 0.05, n_points)
    probs = np.clip(rng.beta(2, 3, n_points), 0, 1)
    return pd.DataFrame({"lat": lats, "lon": lons, "flood_probability": probs.round(2)})


def get_location_details(lat, lon):
    """What shows in the popup when a judge clicks a point on the map."""
    rng = np.random.default_rng(int(abs(lat * lon * 1000)) % 1000)
    return {
        "latitude": round(lat, 4),
        "longitude": round(lon, 4),
        "rainfall_6h": round(float(rng.uniform(10, 90)), 1),
        "flood_probability": round(float(rng.uniform(0.1, 0.9)), 2),
        "elevation_m": round(float(rng.uniform(2, 15)), 1),
        "built_up_fraction": round(float(rng.uniform(0.2, 0.9)), 2),
    }


def risk_level_from_probability(p):
    if p < 0.2:
        return "LOW"
    elif p < 0.4:
        return "MODERATE"
    elif p < 0.6:
        return "ELEVATED"
    elif p < 0.8:
        return "HIGH"
    else:
        return "VERY HIGH"

def get_population_points(n_points=40):
    """Mock population density points around Chennai."""
    rng = np.random.default_rng(11)
    lats = CHENNAI_CENTER[0] + rng.normal(0, 0.05, n_points)
    lons = CHENNAI_CENTER[1] + rng.normal(0, 0.05, n_points)
    population = rng.integers(500, 15000, n_points)
    return pd.DataFrame({"lat": lats, "lon": lons, "population": population})


def get_elevation_points(n_points=40):
    """Mock elevation points around Chennai (used for the Elevation layer)."""
    rng = np.random.default_rng(23)
    lats = CHENNAI_CENTER[0] + rng.normal(0, 0.05, n_points)
    lons = CHENNAI_CENTER[1] + rng.normal(0, 0.05, n_points)
    elevation = np.clip(rng.normal(8, 4, n_points), 1, None)
    return pd.DataFrame({"lat": lats, "lon": lons, "elevation_m": elevation.round(1)})


def get_high_risk_roads():
    """Mock list of roads overlapping high flood-risk zones."""
    return pd.DataFrame({
        "road": ["Anna Salai", "Velachery Main Road", "OMR (Old Mahabalipuram Road)",
                 "GST Road", "Mount Road"],
        "risk_percent": [84, 77, 73, 68, 55],
    })


def get_critical_facilities():
    """Mock list of critical facilities and their flood risk."""
    return pd.DataFrame({
        "facility": ["General Hospital A", "Community Hospital B", "Government School C",
                     "Fire Station D", "Government Hospital E"],
        "type": ["Hospital", "Hospital", "School", "Emergency", "Hospital"],
        "risk_level": ["HIGH", "MODERATE", "HIGH", "LOW", "HIGH"],
    })


def get_river_status():
    """Placeholder — real river/gauge data isn't wired up yet, so we say so
    rather than making up numbers."""
    return {
        "available": False,
        "message": "River-level integration — planned / data unavailable in prototype.",
    }