from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials #----------
import uvicorn
import psutil
from .dash_app_mod import dash_app
from .monitor import CPU_COUNT, update_df

# Создание FastAPI приложения
app = FastAPI()
security = HTTPBasic()
# Монтирование WSGI приложения dash_app на маршрут "/dashboard"
app.mount("/dashboard/", WSGIMiddleware(dash_app.server))

# Обработчик корневого маршрута "/"
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Обработчик маршрута "/cpu/"
# @app.get("/cpu/")
# async def cpu(cpu_id: int | None = None):
#     if cpu_id is None:
#         return {"cpu_percent": psutil.cpu_percent(), "cpu_count": psutil.cpu_count()}
#     else:
#         if 0 <= cpu_id < CPU_COUNT:
#             return {f"cpu{cpu_id+1}_percent": psutil.cpu_percent(percpu=True)[cpu_id]}
#         raise HTTPException(status_code=404, detail=f"CPU not found. cpu_id must be between 0 and {CPU_COUNT-1}, but got {cpu_id}")
#-----
@app.get("/cpu/")
async def cpu(cpu_id: int | None = None, credentials: HTTPBasicCredentials = Depends(security)):
    if not check_credentials(credentials.username, credentials.password):
        raise HTTPException(status_code=401, detail="Unauthorized")
        
    if cpu_id is None:
        return {"cpu_percent": psutil.cpu_percent(), "cpu_count": psutil.cpu_count()}
    else:
        if 0 <= cpu_id < CPU_COUNT:
            return {f"cpu{cpu_id+1}_percent": psutil.cpu_percent(percpu=True)[cpu_id]}
        raise HTTPException(status_code=404, detail=f"CPU not found. cpu_id must be between 0 and {CPU_COUNT-1}, but got {cpu_id}")

#-----
# Обработчик маршрута "/ram/"
# @app.get("/ram/")
# async def ram():
#     # Получение информации о памяти с помощью модуля psutil
#     ram_info = psutil.virtual_memory()
    
#     # Возвращение информации о памяти в виде словаря
#     return {
#         "total": ram_info.total,
#         "available": ram_info.available,
#         "used": ram_info.used,
#         "free": ram_info.free,
#         "percent": ram_info.percent
#     }
#------
@app.get("/ram/")
async def ram(credentials: HTTPBasicCredentials = Depends(security)):
    if not check_credentials(credentials.username, credentials.password):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Получение информации о памяти с помощью модуля psutil
    ram_info = psutil.virtual_memory()
    
    # Возвращение информации о памяти в виде словаря
    return {
        "total": ram_info.total,
        "available": ram_info.available,
        "used": ram_info.used,
        "free": ram_info.free,
        "percent": ram_info.percent
    }
#-------
# Обработчик маршрута "/disk/"
@app.get("/disk/")
async def disk():
    # Получение информации о дисковом пространстве с помощью модуля psutil
    disk_info = psutil.disk_usage('/')
    
    # Возвращение информации о дисковом пространстве в виде словаря
    return {
        "total": disk_info.total,
        "used": disk_info.used,
        "free": disk_info.free,
        "percent": disk_info.percent
    }

# Обработчик маршрута "/network/"
@app.get("/network/")
async def network():
    # Получение информации о сетевом трафике с помощью модуля psutil
    network_info = psutil.net_io_counters()
    
    # Возвращение информации о сетевом трафике в виде словаря
    return {
        "bytes_sent": network_info.bytes_sent,
        "bytes_received": network_info.bytes_recv,
        "packets_sent": network_info.packets_sent,
        "packets_received": network_info.packets_recv
    }


#---- функция проверки учетных данных
def check_credentials(username: str, password: str):
    return username == "er" and password == "er"
#-------
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


    