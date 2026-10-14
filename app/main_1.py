"""Local system metrics API and Dash interface."""
import os
import secrets
import psutil
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from .dash_app_mod import dash_app

app = FastAPI(title="System monitor")
security = HTTPBasic()
app.mount("/dashboard/", WSGIMiddleware(dash_app.server))


def check_credentials(username, password):
    expected_user = os.environ.get("MONITOR_USERNAME", "")
    expected_password = os.environ.get("MONITOR_PASSWORD", "")
    return bool(expected_user and expected_password) and secrets.compare_digest(username.encode(), expected_user.encode()) and secrets.compare_digest(password.encode(), expected_password.encode())


def require_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    if not check_credentials(credentials.username, credentials.password):
        raise HTTPException(status_code=401, detail="Unauthorized", headers={"WWW-Authenticate": "Basic"})


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/cpu/", dependencies=[Depends(require_credentials)])
async def cpu(cpu_id: int | None = None):
    if cpu_id is None:
        return {"cpu_percent": psutil.cpu_percent(), "cpu_count": psutil.cpu_count()}
    values = psutil.cpu_percent(percpu=True)
    if not 0 <= cpu_id < len(values):
        raise HTTPException(status_code=404, detail=f"CPU not found. cpu_id must be between 0 and {len(values)-1}, but got {cpu_id}")
    return {f"cpu{cpu_id+1}_percent": values[cpu_id]}


@app.get("/ram/", dependencies=[Depends(require_credentials)])
async def ram():
    info = psutil.virtual_memory()
    return {key: getattr(info, key) for key in ("total", "available", "used", "free", "percent")}


@app.get("/disk/")
async def disk():
    info = psutil.disk_usage(os.path.abspath(os.sep))
    return {key: getattr(info, key) for key in ("total", "used", "free", "percent")}


@app.get("/network/")
async def network():
    info = psutil.net_io_counters()
    return {"bytes_sent": info.bytes_sent, "bytes_received": info.bytes_recv,
            "packets_sent": info.packets_sent, "packets_received": info.packets_recv}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main_1:app", host="127.0.0.1", port=8000)
