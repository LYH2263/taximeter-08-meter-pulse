import pytest

from app.engines.night_compare import compare_day_night
from app.engines.tariff_breakdown import NegativeInput, calc_fare

T = {"start_price": 11, "start_include_km": 3, "per_km": 2.5, "per_slow_min": 0.8, "night_factor": 1.2}

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

def test_pulse_hops_drop_tail():
    # 含 3 公里，超 2.34 公里 → 4 个 0.5 公里跳（余 0.34 不计）；2.9 分钟 → 2 整分钟跳
    r = calc_fare(5.34, 2.9, False, T, pulse=True)
    assert r["pulse_enabled"] is True
    assert r["mileage_hops"] == 4
    assert r["slow_hops"] == 2
    assert r["per_mileage_hop"] == 1.25
    assert r["per_slow_hop"] == 0.8
    assert r["mileage"] == 5.0
    assert r["slow_fee"] == 1.6
    # 起步只收一次：11 + 5.0 + 1.6
    assert r["start"] == 11
    assert r["total"] == 17.6

def test_pulse_within_include_km():
    r = calc_fare(2, 0.4, False, T, pulse=True)
    assert r["mileage_hops"] == 0
    assert r["slow_hops"] == 0
    assert r["total"] == 11

def test_pulse_exact_hop_boundary():
    # 超含公里恰为 2.5 公里（5 个整跳），浮点误差不应吞掉最后一跳
    r = calc_fare(5.5, 3, False, T, pulse=True)
    assert r["mileage_hops"] == 5
    assert r["slow_hops"] == 3
    assert r["mileage"] == 6.25

def test_pulse_night_factor_after_hops():
    # 夜间布尔仍乘在跳后金额上：(11 + 4*1.25 + 2*0.8) * 1.2
    r = calc_fare(5.34, 2.9, True, T, pulse=True)
    assert r["mileage_hops"] == 4
    assert r["slow_hops"] == 2
    assert r["per_mileage_hop"] == 1.5
    assert r["per_slow_hop"] == 0.96
    assert r["total"] == round((11 + 5.0 + 1.6) * 1.2, 2)

def test_pulse_disabled_is_continuous_with_zero_hops():
    r = calc_fare(5.34, 2.9, False, T)
    assert r["pulse_enabled"] is False
    assert r["mileage_hops"] == 0
    assert r["slow_hops"] == 0
    # 现行连续计价：2.34*2.5 + 2.9*0.8 + 11
    assert r["total"] == round(11 + 2.34 * 2.5 + 2.9 * 0.8, 2)

def test_pulse_compare_uses_continuous():
    c = compare_day_night(5.34, 2.9, T)
    assert c["day"]["mileage_hops"] == 0
    assert c["night"]["mileage_hops"] == 0

def test_negative_rejected():
    with pytest.raises(NegativeInput):
        calc_fare(-1, 2, False, T, pulse=True)
    with pytest.raises(NegativeInput):
        calc_fare(5, -0.1, False, T)
