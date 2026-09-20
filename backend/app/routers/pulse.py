from fastapi import APIRouter, HTTPException
from app.schemas.fare import PulseEnabledRequest
from app.services.taxi_service import TaxiService
router = APIRouter()
@router.get("/pulse")
def list_pulse_rules():
    with TaxiService() as s:
        return {"items": s.pulse_rules()}
@router.post("/pulse/{rule_id}/enabled")
def set_pulse_enabled(rule_id: int, body: PulseEnabledRequest):
    with TaxiService() as s:
        row = s.set_pulse_enabled(rule_id, body.enabled)
        if row is None: raise HTTPException(404, "脉冲规则不存在")
        return row
