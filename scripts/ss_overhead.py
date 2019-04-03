# input: metric client_req_exec_time
# output: 1 series, x value: client request, y value: exec time

import logging
import api
import helpers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EXPERIMENT = "ss_overhead"
PROM_QUERY = (f"max(bottomk({api.get_number_of_byz()+1}, client_req_exec_time) by (state_length)) by (state_length)")

def transform(time_series):
    data_points = []
    # sort data points ASC wrt state length, gives us client_reqs in ASC order
    data_asc = sorted(time_series, key=lambda m: float(m["metric"]["state_length"]))

    for el in data_asc:
        x = int(el["metric"]["state_length"])
        y = str(float(el["value"][1])).replace(".", ",")
        data_points.append({ "req": x, "exec_time": y })

    # build key:val pairs for data points and return
    return data_points

if __name__ == "__main__":
    logger.info("Starting data extraction for self-stabilization overhead experiment")
    results = api.get_time_series_for_q(PROM_QUERY)
    data_points = transform(results)
    helpers.write_to_csv(EXPERIMENT, data_points)