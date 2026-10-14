from types import SimpleNamespace
import pytest
from fastapi.testclient import TestClient
from .main_1 import app, check_credentials

client = TestClient(app)
AUTH = ("test-user", "test-only-password")

@pytest.fixture(autouse=True)
def configure_credentials(monkeypatch):
    monkeypatch.setenv("MONITOR_USERNAME", AUTH[0])
    monkeypatch.setenv("MONITOR_PASSWORD", AUTH[1])


def test_root():
    assert client.get("/").json() == {"message": "Hello World"}

@pytest.mark.parametrize("path", ["/cpu/", "/ram/"])
def test_missing_credentials(path):
    assert client.get(path).status_code == 401


def test_wrong_credentials():
    response = client.get("/cpu/", auth=("wrong", "wrong"))
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Basic"


def test_unconfigured_credentials_fail_closed(monkeypatch):
    monkeypatch.delenv("MONITOR_PASSWORD")
    assert not check_credentials(*AUTH)


def test_cpu(monkeypatch):
    monkeypatch.setattr("psutil.cpu_percent", lambda percpu=False: [8] * 8 if percpu else 100)
    monkeypatch.setattr("psutil.cpu_count", lambda: 8)
    assert client.get("/cpu/", auth=AUTH).json() == {"cpu_percent": 100, "cpu_count": 8}
    assert client.get("/cpu/?cpu_id=7", auth=AUTH).json() == {"cpu8_percent": 8}
    for index in (-1, 8):
        assert client.get(f"/cpu/?cpu_id={index}", auth=AUTH).status_code == 404
    assert client.get("/cpu/?cpu_id=invalid", auth=AUTH).status_code == 422


def test_ram(monkeypatch):
    expected = dict(total=100, available=50, used=50, free=50, percent=50)
    monkeypatch.setattr("psutil.virtual_memory", lambda: SimpleNamespace(**expected))
    assert client.get("/ram/", auth=AUTH).json() == expected


def test_disk(monkeypatch):
    expected = dict(total=1000, used=500, free=500, percent=50)
    monkeypatch.setattr("psutil.disk_usage", lambda _: SimpleNamespace(**expected))
    assert client.get("/disk/").json() == expected


def test_network(monkeypatch):
    monkeypatch.setattr("psutil.net_io_counters", lambda: SimpleNamespace(bytes_sent=1000, bytes_recv=2000, packets_sent=50, packets_recv=100))
    assert client.get("/network/").json() == dict(bytes_sent=1000, bytes_received=2000, packets_sent=50, packets_received=100)


def test_dashboard_mount():
    assert client.get("/dashboard/").status_code == 200


def test_interval_seconds():
    from .dash_app_mod import update_interval
    assert update_interval(2) == 2000
