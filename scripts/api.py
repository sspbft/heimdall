import requests
import logging
import api

logger = logging.getLogger(__name__)

PROM_URL = "http://localhost:6061/api/v1"

def get_number_of_byz():
    n = get_number_of_nodes()
    if n == 6:
        return 1
    elif n > 6 and n <= 12:
        return 2
    else:
        return 3

def get_number_of_nodes():
    data = get_time_series_for_q("count(up)")
    return int(data[0]["value"][1])

def get_time_series_for_q(q):
    logger.info(f"Querying Prometheus for q={q}")
    url = f"{PROM_URL}/query?query={q}"
    r = requests.get(url)
    return r.json()["data"]["result"]