import os
from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.helpers.time_helper import dev_add_minutes
from app.core.config import settings


def dev_only():
    env_mode = settings.ENV
    if env_mode != "DEV":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not allowed. only dev"+" "+env_mode,
        )

router = APIRouter(
    prefix="/dev",
    tags=["dev"],
    dependencies=[Depends(dev_only)]
)
@router.post("/add-minutes")
async def add_minutes(request: Request):
    body = await request.json()
    minutes = body.get("minutes")

    if minutes is None:
        raise HTTPException(status_code=400, detail="minutes is required")

    dev_add_minutes(int(minutes))

    return {"ok": True, "added_minutes": int(minutes)}
    

