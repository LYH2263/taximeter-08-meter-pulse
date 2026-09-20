import math
import sqlite3


def _hops(amount: float, step: float) -> int:
    if step <= 0:
        return 0
    return max(0, math.floor(amount / step + 1e-9))


def calc_fare(distance_km: float, slow_min: float, night: bool, tariff: dict, pulse: dict | None = None) -> dict:
    distance_km = float(distance_km)
    slow_min = float(slow_min)
    if distance_km < 0 or slow_min < 0:
        raise ValueError("distance_km 与 slow_min 不允许为负")
    base = float(tariff["start_price"])
    include = float(tariff["start_include_km"])
    per_km = float(tariff["per_km"])
    per_slow = float(tariff["per_slow_min"])
    night_f = float(tariff.get("night_factor", 1.0)) if night else 1.0
    pulse_on = bool(pulse and pulse.get("enabled"))
    dist = max(0.0, distance_km - include)
    if pulse_on:
        d_step = float(pulse.get("distance_step_km", 0.5) or 0.5)
        s_step = float(pulse.get("slow_step_min", 1.0) or 1.0)
        distance_hops = _hops(dist, d_step)
        slow_hops = _hops(slow_min, s_step)
        per_hop_mile = per_km * d_step
        per_hop_slow = per_slow * s_step
        mile = distance_hops * per_hop_mile
        slow = slow_hops * per_hop_slow
    else:
        d_step = s_step = 0.0
        distance_hops = slow_hops = 0
        per_hop_mile = per_hop_slow = 0.0
        mile = dist * per_km
        slow = slow_min * per_slow
    sub = base + mile + slow
    return {
        "distance_km": round(distance_km, 2),
        "slow_min": round(slow_min, 1),
        "night": night,
        "night_factor": night_f,
        "pulse_enabled": pulse_on,
        "distance_step_km": round(d_step, 2),
        "slow_step_min": round(s_step, 2),
        "distance_hops": distance_hops,
        "slow_hops": slow_hops,
        "per_hop_mileage": round(per_hop_mile, 2),
        "per_hop_slow": round(per_hop_slow, 2),
        "start": round(base * night_f, 2),
        "mileage": round(mile * night_f, 2),
        "slow_fee": round(slow * night_f, 2),
        "total": round(sub * night_f, 2),
    }
