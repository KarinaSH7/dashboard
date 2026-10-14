# System monitor

A university Python project with a FastAPI metrics API and a Dash interface. It reads CPU, memory, disk and network information from the computer running the server.

## Run locally

Use Python 3.12 and a virtual environment. From the repository root run the following commands.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main_1:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/dashboard/ for the interface and http://127.0.0.1:8000/docs for the API documentation.

CPU and memory endpoints use HTTP Basic authentication. Set MONITOR_USERNAME and MONITOR_PASSWORD in your local shell before starting the server. There are no built-in credentials. If either variable is missing, those requests are rejected.

The dashboard, disk and network endpoints remain unauthenticated in this coursework version. Do not expose this application to the internet or a shared network. Basic authentication alone does not encrypt traffic.

## API routes

- GET / returns a simple health message
- GET /cpu/ returns aggregate CPU usage
- GET /cpu/?cpu_id=0 returns one logical CPU sample
- GET /ram/ returns memory information
- GET /disk/ returns disk usage
- GET /network/ returns cumulative network counters

Memory and disk sizes and network byte counters are measured in bytes. CPU and memory percentages are point-in-time samples. Network counters are totals, not transfer rates.

## Tests

```sh
python -m pytest app/test_.py -q
```

The cleanup passed 11 automated checks on Python 3.12. Browser interaction has not been verified.

Tests replace system readings with predictable objects and use test-only credentials. They check responses, rejected credentials, missing configuration and CPU index boundaries. These checks do not establish production readiness.

## Maintenance work

The original university project is preserved in Git history. The portfolio cleanup moves credentials out of source code, makes memory tests platform-independent, fixes CPU index validation and converts the interface refresh setting from seconds to milliseconds. It also corrects where the average CPU sample is written.

## Known limitations

Several interface callbacks independently sample the same shared data frame. This is a single-user local exercise, not a reliable multi-user telemetry service. The connections graph is still a placeholder. Disk counters and some hardware metrics may be unavailable on particular machines. Browser rendering and hardware compatibility require additional manual checks.
