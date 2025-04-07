# Robot monitoring application

***
## Reqs:
* Python (3.11=<)

## Setup
1. clone the repo
2. `cd monitoring-backend`
3. `pip3 install poetry`
4. `poetry install`
5. `python3 monitoring.py` or `docker build -t monitoring . && docker run -p 5487:5487 robots`


## CLI (`monitoring.py`)

* Application running host `--host <YOUR_HOST>` (default is `0.0.0.0`)

* Application running port `--port <YOUR_PORT>` (default is `5487`)

* Refresh frequency in HZ `--refresh-hz <REFRESH_FREQUENCY_IN_HZ>` (default is `10`)

* Application running host `--log-level <APPLICATION_LOG_LEVEL>` (default is `INFO`)

*if you have changed host or port, change them also in `monitoring-frontend/.env` for the frontend.

***