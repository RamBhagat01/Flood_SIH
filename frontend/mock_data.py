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

def get_historical_replay_data(hour: int):
    """Mock data simulating the 2015 Chennai flood progression (0 to 72 hours)."""
    rng = np.random.default_rng(2015)
    progress = min(hour / 48.0, 1.0)

    n_points = 35
    lats = CHENNAI_CENTER[0] + rng.normal(0, 0.06, n_points)
    lons = CHENNAI_CENTER[1] + rng.normal(0, 0.06, n_points)

    base_prob = rng.uniform(0.1, 0.3, n_points)
    flood_prob = np.clip(base_prob + progress * rng.uniform(0.2, 0.65, n_points), 0, 0.99)
    rainfall_mm = progress * rng.uniform(80, 420, n_points)

    points = []
    for i in range(n_points):
        points.append({
            "lat": round(float(lats[i]), 4),
            "lon": round(float(lons[i]), 4),
            "flood_probability": round(float(flood_prob[i]), 2),
            "rainfall_mm": round(float(rainfall_mm[i]), 1),
        })

    avg_rainfall = round(float(np.mean(rainfall_mm)), 1)
    affected_pct = round(float(np.mean(flood_prob > 0.5)) * 100, 1)
    water_level_cm = round(progress * 195 + rng.normal(0, 8), 1)

    if hour <= 6:
        narrative = "🌧 Hour 0-6: Continuous heavy rainfall starts across Chennai. Water logging reported in low-lying roads."
    elif hour <= 18:
        narrative = "🌊 Hour 6-18: Chembarambakkam reservoir release increases. Adyar & Cooum rivers swelling."
    elif hour <= 36:
        narrative = "🚨 Hour 18-36: Severe inundation in Velachery, Mudichur, Saidapet, and Tambaram."
    elif hour <= 54:
        narrative = "⚠️ Hour 36-54: Peak catastrophe. Airport runway flooded, power grid cut off in multiple zones."
    else:
        narrative = "📉 Hour 54-72: Rain subsides. NDMA and military rescue boats deployed in high-risk zones."

    return {
        "points": points,
        "avg_rainfall_mm": avg_rainfall,
        "affected_area_pct": affected_pct,
        "water_level_cm": max(water_level_cm, 0),
        "narrative": narrative,
    }

def get_pincode_data():
    """Mock database of Chennai locations and pincodes for risk prediction lookup."""
    return {
        "600042 - Velachery": {
            "pincode": "600042",
            "area": "Velachery",
            "risk_score": 0.88,
            "risk_level": "VERY HIGH",
            "elevation_m": 2.5,
            "predicted_rain_6h": "78.5 mm",
            "built_up_area": "84%",
            "top_risk_factors": [
                {"factor": "Elevation", "impact": "Critical (2.5m above sea level)", "weight": "+35%"},
                {"factor": "Proximity to Pallikaranai Marshland", "impact": "High water overflow risk", "weight": "+30%"},
                {"factor": "6-Hour Predicted Rainfall", "impact": "78.5 mm (Heavy)", "weight": "+20%"},
                {"factor": "Drainage Infrastructure", "impact": "High congestion index", "weight": "+15%"},
            ],
            "evacuation_status": "Immediate advisory — move to upper floors or nearest relief center.",
            "nearest_shelter": "Velachery Government Higher Sec School (1.2 km away)",
        },
        "600045 - Tambaram": {
            "pincode": "600045",
            "area": "Tambaram",
            "risk_score": 0.65,
            "risk_level": "HIGH",
            "elevation_m": 8.0,
            "predicted_rain_6h": "62.0 mm",
            "built_up_area": "71%",
            "top_risk_factors": [
                {"factor": "Adyar River Proximity", "impact": "River overflow warning level", "weight": "+40%"},
                {"factor": "6-Hour Predicted Rainfall", "impact": "62.0 mm (Moderate to Heavy)", "weight": "+25%"},
                {"factor": "Elevation", "impact": "Moderate (8.0m)", "weight": "+15%"},
                {"factor": "Drainage Capacity", "impact": "Partial obstruction reported", "weight": "+20%"},
            ],
            "evacuation_status": "Standby advisory — keep emergency kit ready.",
            "nearest_shelter": "Tambaram Community Hall (0.8 km away)",
        },
        "600096 - OMR Perungudi": {
            "pincode": "600096",
            "area": "OMR Perungudi",
            "risk_score": 0.79,
            "risk_level": "HIGH",
            "elevation_m": 3.8,
            "predicted_rain_6h": "71.2 mm",
            "built_up_area": "89%",
            "top_risk_factors": [
                {"factor": "Built-up Fraction", "impact": "89% non-permeable surface", "weight": "+35%"},
                {"factor": "Elevation", "impact": "Low-lying zone (3.8m)", "weight": "+30%"},
                {"factor": "6-Hour Predicted Rainfall", "impact": "71.2 mm", "weight": "+25%"},
                {"factor": "Road Inundation", "impact": "OMR main arterial road vulnerable", "weight": "+10%"},
            ],
            "evacuation_status": "Prepare for road blockages and urban water logging.",
            "nearest_shelter": "Perungudi Relief Shelter #2 (1.5 km away)",
        },
        "600017 - T. Nagar": {
            "pincode": "600017",
            "area": "T. Nagar",
            "risk_score": 0.52,
            "risk_level": "ELEVATED",
            "elevation_m": 6.2,
            "predicted_rain_6h": "45.0 mm",
            "built_up_area": "92%",
            "top_risk_factors": [
                {"factor": "Stormwater Drain Capacity", "impact": "Severe urban runoff", "weight": "+40%"},
                {"factor": "Built-up Fraction", "impact": "92% impervious ground", "weight": "+30%"},
                {"factor": "Elevation", "impact": "Moderate (6.2m)", "weight": "+15%"},
                {"factor": "Rainfall", "impact": "45.0 mm", "weight": "+15%"},
            ],
            "evacuation_status": "Water logging in low basement areas possible.",
            "nearest_shelter": "T. Nagar Govt Girls Higher Sec School (0.5 km away)",
        },
        "600040 - Anna Nagar": {
            "pincode": "600040",
            "area": "Anna Nagar",
            "risk_score": 0.18,
            "risk_level": "LOW",
            "elevation_m": 12.5,
            "predicted_rain_6h": "32.0 mm",
            "built_up_area": "65%",
            "top_risk_factors": [
                {"factor": "Elevation", "impact": "Safe height (12.5m above sea level)", "weight": "-45%"},
                {"factor": "Drainage Infrastructure", "impact": "Operational stormwater network", "weight": "-25%"},
                {"factor": "Rainfall Intensity", "impact": "32.0 mm (Light to Moderate)", "weight": "-20%"},
                {"factor": "River Distance", "impact": "Far from Adyar/Cooum banks", "weight": "-10%"},
            ],
            "evacuation_status": "Safe — No immediate evacuation required.",
            "nearest_shelter": "Anna Nagar Tower Park Community Center (0.3 km away)",
        },
    }

def get_active_alerts():
    """Mock database of active emergency broadcast alerts."""
    return pd.DataFrame([
        {
            "Alert ID": "ALT-9021",
            "Target Zone": "Velachery (600042)",
            "Risk Level": "VERY HIGH",
            "Channel": "SMS + WhatsApp + Siren",
            "Recipients": "45,200",
            "Sent Time": "10 mins ago",
            "Status": "DELIVERED",
        },
        {
            "Alert ID": "ALT-9022",
            "Target Zone": "OMR Perungudi (600096)",
            "Risk Level": "HIGH",
            "Channel": "SMS + WhatsApp",
            "Recipients": "32,800",
            "Sent Time": "25 mins ago",
            "Status": "DELIVERED",
        },
        {
            "Alert ID": "ALT-9023",
            "Target Zone": "Tambaram (600045)",
            "Risk Level": "HIGH",
            "Channel": "Cell Broadcast (CAP)",
            "Recipients": "61,000",
            "Sent Time": "40 mins ago",
            "Status": "DELIVERED",
        },
        {
            "Alert ID": "ALT-9024",
            "Target Zone": "T. Nagar (600017)",
            "Risk Level": "ELEVATED",
            "Channel": "SMS Advisory",
            "Recipients": "28,500",
            "Sent Time": "1 hour ago",
            "Status": "DELIVERED",
        },
    ])


def get_rescue_team_status():
    """Mock database of NDRF and Fire & Rescue team deployments."""
    return pd.DataFrame([
        {
            "Team ID": "NDRF-01",
            "Unit Name": "4th Battalion NDRF",
            "Assigned Zone": "Velachery",
            "Boats Deployed": 6,
            "Personnel": 24,
            "Status": "ACTIVE RESCUE",
        },
        {
            "Team ID": "NDRF-04",
            "Unit Name": "4th Battalion NDRF",
            "Assigned Zone": "Tambaram / Mudichur",
            "Boats Deployed": 8,
            "Personnel": 30,
            "Status": "ACTIVE RESCUE",
        },
        {
            "Team ID": "TNSFRS-02",
            "Unit Name": "TN Fire & Rescue Services",
            "Assigned Zone": "OMR Perungudi",
            "Boats Deployed": 3,
            "Personnel": 15,
            "Status": "EN ROUTE",
        },
        {
            "Team ID": "TNSFRS-05",
            "Unit Name": "TN Fire & Rescue Services",
            "Assigned Zone": "Anna Nagar",
            "Boats Deployed": 0,
            "Personnel": 12,
            "Status": "STANDBY",
        },
    ])


def get_evacuation_routes():
    """Mock data for safe evacuation routes vs closed roads."""
    return pd.DataFrame([
        {"Route Name": "Velachery Main Rd -> Guindy Flyover", "Status": "SUBMERGED (CLOSED)", "Risk": "CRITICAL"},
        {"Route Name": "OMR Tollgate -> Madhya Kailash", "Status": "PASSABLE (WATERLOGGED)", "Risk": "MODERATE"},
        {"Route Name": "GST Road -> Airport Flyover", "Status": "OPEN & SAFE", "Risk": "LOW"},
        {"Route Name": "Inner Ring Road -> Koyambedu", "Status": "OPEN & SAFE", "Risk": "LOW"},
        {"Route Name": "Mudichur Road -> Tambaram West", "Status": "SUBMERGED (CLOSED)", "Risk": "CRITICAL"},
    ])

def get_active_alerts():
    """Mock database of active emergency broadcast alerts."""
    return pd.DataFrame([
        {
            "Alert ID": "ALT-9021",
            "Target Zone": "Velachery (600042)",
            "Risk Level": "VERY HIGH",
            "Channel": "SMS + WhatsApp + Siren",
            "Recipients": "45,200",
            "Sent Time": "10 mins ago",
            "Status": "DELIVERED",
        },
        {
            "Alert ID": "ALT-9022",
            "Target Zone": "OMR Perungudi (600096)",
            "Risk Level": "HIGH",
            "Channel": "SMS + WhatsApp",
            "Recipients": "32,800",
            "Sent Time": "25 mins ago",
            "Status": "DELIVERED",
        },
        {
            "Alert ID": "ALT-9023",
            "Target Zone": "Tambaram (600045)",
            "Risk Level": "HIGH",
            "Channel": "Cell Broadcast (CAP)",
            "Recipients": "61,000",
            "Sent Time": "40 mins ago",
            "Status": "DELIVERED",
        },
        {
            "Alert ID": "ALT-9024",
            "Target Zone": "T. Nagar (600017)",
            "Risk Level": "ELEVATED",
            "Channel": "SMS Advisory",
            "Recipients": "28,500",
            "Sent Time": "1 hour ago",
            "Status": "DELIVERED",
        },
    ])


def get_rescue_team_status():
    """Mock database of NDRF and Fire & Rescue team deployments."""
    return pd.DataFrame([
        {
            "Team ID": "NDRF-01",
            "Unit Name": "4th Battalion NDRF",
            "Assigned Zone": "Velachery",
            "Boats Deployed": 6,
            "Personnel": 24,
            "Status": "ACTIVE RESCUE",
        },
        {
            "Team ID": "NDRF-04",
            "Unit Name": "4th Battalion NDRF",
            "Assigned Zone": "Tambaram / Mudichur",
            "Boats Deployed": 8,
            "Personnel": 30,
            "Status": "ACTIVE RESCUE",
        },
        {
            "Team ID": "TNSFRS-02",
            "Unit Name": "TN Fire & Rescue Services",
            "Assigned Zone": "OMR Perungudi",
            "Boats Deployed": 3,
            "Personnel": 15,
            "Status": "EN ROUTE",
        },
        {
            "Team ID": "TNSFRS-05",
            "Unit Name": "TN Fire & Rescue Services",
            "Assigned Zone": "Anna Nagar",
            "Boats Deployed": 0,
            "Personnel": 12,
            "Status": "STANDBY",
        },
    ])


def get_evacuation_routes():
    """Mock data for safe evacuation routes vs closed roads."""
    return pd.DataFrame([
        {"Route Name": "Velachery Main Rd -> Guindy Flyover", "Status": "SUBMERGED (CLOSED)", "Risk": "CRITICAL"},
        {"Route Name": "OMR Tollgate -> Madhya Kailash", "Status": "PASSABLE (WATERLOGGED)", "Risk": "MODERATE"},
        {"Route Name": "GST Road -> Airport Flyover", "Status": "OPEN & SAFE", "Risk": "LOW"},
        {"Route Name": "Inner Ring Road -> Koyambedu", "Status": "OPEN & SAFE", "Risk": "LOW"},
        {"Route Name": "Mudichur Road -> Tambaram West", "Status": "SUBMERGED (CLOSED)", "Risk": "CRITICAL"},
    ])