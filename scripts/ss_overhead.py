# input: metric client_req_exec_time
# output: 1 series, x value: client request, y value: exec time

import logging
import api
import helpers
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EXPERIMENT = "ss_overhead"
PROM_QUERY = (f"bottomk({api.get_number_of_byz()+1}, client_req_exec_time) by (state_length)")

def transform(time_series):
    data_points = []
    # sort data points ASC wrt state length, gives us client_reqs in ASC order
    data_asc = sorted(time_series, key=lambda m: float(m["metric"]["state_length"]))
    data_dct = {}
    for el in data_asc:
        x = int(el["metric"]["state_length"])
        if x in data_dct:
            if float(el["value"][1]) > data_dct[x].get("exec_time"):
                y = float(el["value"][1])
                total_msgs = int(el["metric"]["total_msgs_sent"])
                total_bytes = int(el["metric"]["total_bytes_sent"])
                int_msgs = int(el["metric"]["msgs_sent"])
                int_bytes = int(el["metric"]["bytes_sent"])
                data_dct[x] = {"exec_time": y, "total_msgs": total_msgs,
                           "total_bytes": total_bytes, "msgs": int_msgs, "bytes": int_bytes}

        else:
            #y = str(float(el["value"][1])).replace(".", ",")
            y = float(el["value"][1])
            total_msgs = int(el["metric"]["total_msgs_sent"])
            total_bytes = int(el["metric"]["total_bytes_sent"])
            int_msgs = int(el["metric"]["msgs_sent"])
            int_bytes = int(el["metric"]["bytes_sent"])
            data_dct[x] = {"exec_time": y, "total_msgs": total_msgs,
                           "total_bytes": total_bytes, "msgs": int_msgs, "bytes": int_bytes}

        
    for res in data_dct:
        y = float(el["value"][1])
        y = str(data_dct[res]["exec_time"]).replace(".", ",")
        total_msgs = data_dct[res]["total_msg"]
        total_bytes = data_dct[res]["total_bytes"]
        int_msgs = data_dct[res]["msgs"]
        int_bytes = data_dct[res]["bytes"]
        data_points.append({ "req": res, "exec_time": y, "total_msgs": total_msgs,
                             "total_bytes": total_bytes, "msgs": int_msgs, "bytes": int_bytes})

    # build key:val pairs for data points and return
    return data_points

def main():
    logger.info("Starting data extraction for self-stabilization overhead experiment")
    results = api.get_time_series_for_q(PROM_QUERY)
    if len(results) == 0:
        logger.warning("No results found, quitting")
        return
    data_points = transform(results)
    csv_path = helpers.write_to_csv(EXPERIMENT, data_points)
    snapshot_path = helpers.get_snapshot()
    helpers.collect_to_res_folder(EXPERIMENT, [csv_path, snapshot_path])
    helpers.cleanup()

if __name__ == "__main__":
    main()