import os
import logging
import time
import api
import csv

logger = logging.getLogger(__name__)


# [{x0: [y0, y1, ..., yn]}]
def write_to_csv(experiment, data_points):
    n = api.get_number_of_nodes()
    t = time.strftime("%y%m%d_%H%M")

    filename = f"{experiment}_{n}_{t}.csv"
    if not os.path.exists("results"):
        os.makedirs("results")
    with open(f"results/{filename}", "w") as f:
        w = csv.DictWriter(f, data_points[0].keys())
        w.writeheader()
        for p in data_points:
            w.writerow(p)


    logger.info(f"Writing data to {filename}")
    pass