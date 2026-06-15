from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from pydantic import BaseModel, Field
import asyncio
from adb import ensure_adb_server, adb_connect, projector_shutdown
from log import log
from version import VERSION

PROJECTOR_IP = "192.168.50.29"
PROJECTOR_PORT = 5555

@asynccontextmanager
async def lifespan(app: FastAPI):
    log(f"Starting Projector ADB Bridge - version {VERSION}")
    yield

app = FastAPI(lifespan=lifespan)

class ShutdownRequest(BaseModel):
    delay_seconds: int = Field(..., ge=0, le=86400)


async def shutdown_after_delay(delay_seconds: int):
    log(f"Zaplanowano wyłączenie za {delay_seconds}s")

    await asyncio.sleep(delay_seconds)

    ensure_adb_server()

    try:
        devices = adb_connect(PROJECTOR_IP, PROJECTOR_PORT)
        log(f"Connected to projector: {devices}")
    except Exception as e:
        log(f"Failed to connect to projector: {e}")
        return
    
    try:
        projector_shutdown(f"{PROJECTOR_IP}:{PROJECTOR_PORT}")
        log("Projector shutdown command sent successfully")
    except Exception as e:
        log(f"Failed to send projector shutdown command: {e}")
        return


@app.get("/")
def healthcheck():
    return {"status": "ok"}


@app.post("/shutdown")
async def shutdown(request: ShutdownRequest):
    asyncio.create_task(
        shutdown_after_delay(request.delay_seconds)
    )

    return {
        "status": "scheduled",
        "delay": request.delay_seconds
    }