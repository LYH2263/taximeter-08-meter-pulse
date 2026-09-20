import math

MILEAGE_HOP_KM = 0.5
SLOW_HOP_MIN = 1
# 抵消二进制浮点误差，使 3.5 个 0.5 公里这样的整数边界稳定取整
_EPS = 1e-9


class NegativeInput(ValueError):
    """公里或低速为负，拒绝计价且不得写记录。"""


def calc_fare(distance_km: float, slow_min: float, night: bool, tariff: dict, pulse: bool = False) -> dict:
    distance_km = float(distance_km)
    slow_min = float(slow_min)
    if distance_km < 0 or slow_min < 0:
        raise NegativeInput("distance_km 与 slow_min 不得为负")

    base = float(tariff["start_price"])
    include = float(tariff["start_include_km"])
    per_km = float(tariff["per_km"])
    per_slow = float(tariff["per_slow_min"])
    night_f = float(tariff.get("night_factor", 1.0)) if night else 1.0
    per_mileage_hop = per_km * MILEAGE_HOP_KM
    per_slow_hop = per_slow * SLOW_HOP_MIN

    billable_km = max(0.0, distance_km - include)
    if pulse:
        # 超出含公里的部分按每 0.5 公里一跳，低速按每整分钟一跳，不足一跳的尾数不计
        mileage_hops = int(math.floor(billable_km / MILEAGE_HOP_KM + _EPS))
        slow_hops = int(math.floor(slow_min / SLOW_HOP_MIN + _EPS))
        mile = mileage_hops * per_mileage_hop
        slow = slow_hops * per_slow_hop
    else:
        mileage_hops = 0
        slow_hops = 0
        mile = billable_km * per_km
        slow = slow_min * per_slow

    # 夜间系数乘在跳后金额（及起步价）上
    return {
        "distance_km": round(distance_km, 2),
        "slow_min": round(slow_min, 1),
        "night": night,
        "night_factor": night_f,
        "pulse_enabled": bool(pulse),
        "mileage_hops": mileage_hops,
        "slow_hops": slow_hops,
        "hop_distance_km": MILEAGE_HOP_KM,
        "hop_slow_min": SLOW_HOP_MIN,
        "per_mileage_hop": round(per_mileage_hop * night_f, 2),
        "per_slow_hop": round(per_slow_hop * night_f, 2),
        "start": round(base * night_f, 2),
        "mileage": round(mile * night_f, 2),
        "slow_fee": round(slow * night_f, 2),
        "total": round((base + mile + slow) * night_f, 2),
    }
