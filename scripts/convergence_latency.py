# input: metric client_req_exec_time
# output: 1 series, x value: client request, y value: exec time

import logging
import api
import helpers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EXPERIMENT = "convergence_latency"
PROM_QUERY = (f"max(bottomk({4*api.get_number_of_byz()+1}, convergence_latency) by (view)) by (view)")

def transform(time_series):
    data_points = []
    print(time_series)
    # sort data points ASC wrt state length, gives us client_reqs in ASC order
    data_asc = sorted(time_series, key=lambda m: float(m["metric"]["view"]))

    for el in data_asc:
        x = int(el["metric"]["view"])
        y = str(float(el["value"][1])).replace(".", ",")
        data_points.append({ "old_view": x, "conv_lat": y })

    # build key:val pairs for data points and return
    return data_points

if __name__ == "__main__":
    logger.info("Starting data extraction for convergence latency experiment")
    results = api.get_time_series_for_q(PROM_QUERY)
    data_points = transform(results)
    helpers.write_to_csv(EXPERIMENT, data_points)