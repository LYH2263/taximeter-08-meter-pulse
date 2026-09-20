from app.db import connect
from app.engines.night_compare import compare_day_night
from app.engines.tariff_breakdown import calc_fare
from app.repositories import pulse, runs, settings, tariff, trips

class TaxiService:
    def __init__(self): self._c = connect()
    def close(self): self._c.close()
    def __enter__(self): return self
    def __exit__(self, *a): self.close()
    def list_trips(self): return trips.list_all(self._c)
    def trip(self, tid): return trips.get(self._c, tid)
    def tariff(self): return tariff.get_active(self._c)
    def settings(self): return settings.get_map(self._c)
    def history(self, limit=50): return runs.list_recent(self._c, limit)
    def pulse_rule(self): return pulse.get_active(self._c)
    def pulse_rules(self): return pulse.list_all(self._c)
    def set_pulse(self, enabled):
        if enabled:
            rules = pulse.list_all(self._c)
            if not rules:
                return None
            return pulse.enable(self._c, rules[0]["id"])
        pulse.disable_all(self._c)
        return None
    def fare(self, distance_km, slow_min, night, trip_id, persist):
        t = tariff.get_active(self._c)
        p = pulse.get_active(self._c)
        r = calc_fare(distance_km, slow_min, night, t, p)
        rid = runs.insert(self._c, "fare", {"distance_km": distance_km, "slow_min": slow_min, "night": night}, r, trip_id) if persist else None
        return {"run_id": rid, **r}
    def compare(self, distance_km, slow_min, persist):
        t = tariff.get_active(self._c)
        p = pulse.get_active(self._c)
        r = compare_day_night(distance_km, slow_min, t, p)
        rid = runs.insert(self._c, "compare", {"distance_km": distance_km, "slow_min": slow_min}, r, None) if persist else None
        return {"run_id": rid, **r}
    def dashboard(self):
        items = trips.list_all(self._c)
        clean = [x for x in items if "种子" not in x["label"]]
        dirty = [x for x in items if "种子" in x["label"]]
        return {"trip_count": len(items), "clean": len(clean), "dirty": len(dirty)}
