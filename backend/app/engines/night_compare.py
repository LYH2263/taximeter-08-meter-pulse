from app.engines.tariff_breakdown import calc_fare


def compare_day_night(distance_km: float, slow_min: float, tariff: dict, pulse: dict | None = None) -> dict:
    day = calc_fare(distance_km, slow_min, False, tariff, pulse)
    night = calc_fare(distance_km, slow_min, True, tariff, pulse)
    return {
        "distance_km": day["distance_km"],
        "slow_min": day["slow_min"],
        "pulse_enabled": day["pulse_enabled"],
        "day_total": day["total"],
        "night_total": night["total"],
        "delta": round(night["total"] - day["total"], 2),
        "day": day,
        "night": night,
    }
