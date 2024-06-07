# from fastapi.testclient import TestClient
# from .main_1 import app


# client = TestClient(app)

# def test_root():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Hello World"}

# def test_cpu(monkeypatch):
#     monkeypatch.setattr("psutil.cpu_percent", lambda: 100)
#     monkeypatch.setattr("psutil.cpu_count", lambda: 8)
#     #monkeypatch.setattr("cpu1", lambda: 8)

#     response = client.get("/cpu/")
#     assert response.status_code == 401

#     response = client.get("/cpu/", auth=("admin", "admin"))
#     assert response.status_code == 200
#     assert response.json() == {"cpu_percent": 100, "cpu_count": 8}

#     #monkeypatch.setattr("psutil.cpu_percent", lambda percpu: 100)
#     monkeypatch.setattr("cpu1", lambda percpu: 8)
#     response = client.get("/cpu/?cpu_id=0", auth=("admin", "admin"))
#     assert response.status_code == 200
#     assert response.json() == {"cpu1": 8}

#     response = client.get("/cpu/?cpu_id=7")
#     assert response.status_code == 200
#     assert response.json() == {"cpu8": 100}

#     response = client.get("/cpu/?cpu_id=-1")
#     assert response.status_code == 404
#     assert response.json() == {"detail": "CPU not found. cpu_id must be between 0 and 7, but got -1"}

#     response = client.get("/cpu/?cpu_id=121")
#     assert response.status_code == 404
#     assert response.json() == {"detail": "CPU not found. cpu_id must be between 0 and 7, but got 121"}

# #----------
# def test_root():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Hello World"}

# def test_unauthorized_access():
#     response = client.get("/cpu/")
#     assert response.status_code == 401

# def test_authorized_access():
#     response = client.get("/cpu/", headers={"Authorization": "Basic YWRtaW46YWRtaW4="})  # base64("admin:admin")
#     assert response.status_code == 200

# def test_save_settings():
#     response = client.post("/settings/", json={"setting_name": "value"}, headers={"Authorization": "Basic YWRtaW46YWRtaW4="})
#     assert response.status_code == 200
#     assert response.json() == {"message": "Settings saved successfully"}

# def test_load_settings():
#     response = client.get("/settings/", headers={"Authorization": "Basic YWRtaW46YWRtaW4="})
#     assert response.status_code == 200
#     assert response.json() == {"setting_name": "value"}
# #-----------


from fastapi.testclient import TestClient
from .main_1 import app
import psutil

client = TestClient(app)

# Тест проверки корневого маршрута
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

# Тест проверки доступа без авторизации
def test_unauthorized_access():
    response = client.get("/cpu/")
    assert response.status_code == 401

# Тест проверки доступа с авторизацией
def test_authorized_access():
    response = client.get("/cpu/", headers={"Authorization": "Basic YWRtaW46YWRtaW4="})  # ("admin:admin")
    assert response.status_code == 200

# Тестирование функционала CPU
def test_cpu(monkeypatch):
    monkeypatch.setattr("psutil.cpu_percent", lambda: 100)
    monkeypatch.setattr("psutil.cpu_count", lambda: 8)

    response = client.get("/cpu/")#без регистрации 
    assert response.status_code == 401

    response = client.get("/cpu/", auth = ("admin" , "admin"))  # ("admin:admin")
    assert response.status_code == 200
    assert response.json() == {"cpu_percent": 100, "cpu_count": 8}

    monkeypatch.setattr("psutil.cpu_percent", lambda percpu: [8] * 8)
    response = client.get("/cpu/?cpu_id=0", headers={"Authorization": "Basic YWRtaW46YWRtaW4="})  # ("admin:admin")
    assert response.status_code == 200
    assert response.json() == {"cpu1_percent": 8}

    response = client.get("/cpu/?cpu_id=7", headers={"Authorization": "Basic YWRtaW46YWRtaW4="})  # ("admin:admin")
    assert response.status_code == 200
    assert response.json() == {"cpu8_percent": 8}

    response = client.get("/cpu/?cpu_id=-1", headers={"Authorization": "Basic YWRtaW46YWRtaW4="})  # ("admin:admin")
    assert response.status_code == 404
    assert response.json() == {"detail": "CPU not found. cpu_id must be between 0 and 7, but got -1"}

    response = client.get("/cpu/?cpu_id=121", headers={"Authorization": "Basic YWRtaW46YWRtaW4="})  # ("admin:admin")
    assert response.status_code == 404
    assert response.json() == {"detail": "CPU not found. cpu_id must be between 0 and 7, but got 121"}

# Тестирование функционала RAM
def test_ram(monkeypatch):
    monkeypatch.setattr("psutil.virtual_memory", lambda: psutil._psosx.svmem(total=100, available=50, percent=50, used=50, free=50, active = 50, inactive = 0 , wired = 0 ))

    response = client.get("/ram/", headers={"Authorization": "Basic YWRtaW46YWRtaW4="})
    assert response.status_code == 200
    assert response.json() == {"total": 100, "available": 50, "used": 50, "free": 50, "percent": 50}

# # Тестирование функционала SWAP
# def test_swap(monkeypatch):
#     monkeypatch.setattr("psutil.swap_memory", lambda: psutil._common.svmem(total=200, used=100, free=100, percent=50))

#     response = client.get("/swap/", headers={"Authorization": "Basic YWRtaW46YWRtaW4="})
#     assert response.status_code == 200
#     assert response.json() == {"total": 200, "used": 100, "free": 100, "percent": 50}

# Тестирование функционала ROM (дискового пространства)
def test_rom(monkeypatch):
    monkeypatch.setattr("psutil.disk_usage", lambda _: psutil._common.sdiskusage(total=1000, used=500, free=500, percent=50))

    response = client.get("/disk/", headers={"Authorization": "Basic YWRtaW46YWRtaW4="})
    assert response.status_code == 200
    assert response.json() == {"total": 1000, "used": 500, "free": 500, "percent": 50}

# Тестирование функционала Network
def test_network(monkeypatch):
    monkeypatch.setattr("psutil.net_io_counters", lambda: psutil._common.snetio(bytes_sent=1000, bytes_recv=2000, packets_sent=50, packets_recv=100, errin = 0, errout = 0 , dropin = 0 , dropout = 0))

    response = client.get("/network/", headers={"Authorization": "Basic YWRtaW46YWRtaW4="})
    assert response.status_code == 200
    assert response.json() == {"bytes_sent": 1000, "bytes_received": 2000, "packets_sent": 50, "packets_received": 100}