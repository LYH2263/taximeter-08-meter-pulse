from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.taxi_service import TaxiService

router = APIRouter()


class PulseSwitch(BaseModel):
    enabled: bool


@router.get("/pulse")
def get_pulse():
    with TaxiService() as s:
        active = s.pulse_rule()
        return {"enabled": active is not None, "active": active, "rules": s.pulse_rules()}


@router.post("/pulse")
def post_pulse(body: PulseSwitch):
    with TaxiService() as s:
        if body.enabled:
            active = s.set_pulse(True)
            if active is None:
                raise HTTPException(409, "没有可用的脉冲规则")
            return {"enabled": True, "active": active}
        s.set_pulse(False)
        return {"enabled": False, "active": None}
