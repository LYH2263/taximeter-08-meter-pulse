import pytest
from app.engines.night_compare import compare_day_night
from app.engines.tariff_breakdown import calc_fare

T = {"start_price": 11, "start_include_km": 3, "per_km": 2.5, "per_slow_min": 0.8, "night_factor": 1.2}
P = {"enabled": True, "distance_step_km": 0.5, "slow_step_min": 1.0}

def test_day_short():
    r = calc_fare(5, 2, False, T)
    assert r["total"] == 17.6
    assert r["mileage"] == 5.0

def test_night_long():
    r = calc_fare(18, 12, True, T)
    assert r["total"] == 69.72

def test_compare_delta():
    c = compare_day_night(18, 12, T)
    assert c["night_total"] > c["day_total"]

def test_pulse_exact_steps():
    r = calc_fare(5, 2, False, T, P)
    # 超含公里 2km = 4 跳，每跳 1.25；低速 2 跳，每跳 0.8
    assert r["pulse_enabled"] is True
    assert r["distance_hops"] == 4
    assert r["slow_hops"] == 2
    assert r["per_hop_mileage"] == 1.25
    assert r["per_hop_slow"] == 0.8
    assert r["total"] == 17.6

def test_pulse_remainder_dropped():
    # 2.4 超公里只够 4 跳（0.4 公里尾数不计）；2.7 分钟只够 2 跳
    r = calc_fare(5.4, 2.7, False, T, P)
    assert r["distance_hops"] == 4
    assert r["slow_hops"] == 2
    assert r["mileage"] == 5.0
    assert r["slow_fee"] == 1.6
    assert r["total"] == 17.6
    # 落到 2.5 公里则多一跳
    r2 = calc_fare(5.5, 3, False, T, P)
    assert r2["distance_hops"] == 5
    assert r2["slow_hops"] == 3
    assert r2["total"] == 19.65

def test_pulse_night_multiplies_after_hops():
    r = calc_fare(18, 12, True, T, P)
    assert r["distance_hops"] == 30
    assert r["slow_hops"] == 12
    # 夜间布尔乘在跳后金额上
    assert r["mileage"] == 45.0
    assert r["slow_fee"] == 11.52
    assert r["start"] == 13.2
    assert r["total"] == 69.72

def test_pulse_start_once_within_include():
    r = calc_fare(3, 0, False, T, P)
    assert r["distance_hops"] == 0
    assert r["slow_hops"] == 0
    assert r["total"] == 11.0

def test_pulse_disabled_is_continuous_with_zero_hops():
    r = calc_fare(5.4, 2.7, False, T, None)
    assert r["pulse_enabled"] is False
    assert r["distance_hops"] == 0
    assert r["slow_hops"] == 0
    assert r["per_hop_mileage"] == 0.0
    assert r["per_hop_slow"] == 0.0
    assert r["mileage"] == 6.0
    assert r["slow_fee"] == 2.16
    assert r["total"] == 19.16

def test_negative_rejected():
    with pytest.raises(ValueError):
        calc_fare(-1, 0, False, T, P)
    with pytest.raises(ValueError):
        calc_fare(0, -0.5, False, T, P)
