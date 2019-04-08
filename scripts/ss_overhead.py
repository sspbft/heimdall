# input: metric client_req_exec_time
# output: 1 series, x value: client request, y value: exec time

import logging
import api
import helpers
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EXPERIMENT = "ss_overhead"
Q_EXEC_TIME = f"max(bottomk({api.get_number_of_byz()+1}, client_req_exec_time) by (state_length)) by (state_length)"
Q_MSGS_SENT = f"sum(msgs_during_exp) by (exp_param)"
Q_BYTES_SENT = f"sum(bytes_during_exp) by (exp_param)"

def transform(exec_time_series, msgs_sent_time_series, bts_sent_time_series):
    data_points = []
    # sort data points ASC wrt state length, gives us client_reqs in ASC order
    exec_time_asc = sorted(exec_time_series, key=lambda m: float(m["metric"]["state_length"]))
    msgs_sent_asc = sorted(msgs_sent_time_series, key=lambda m: float(m["metric"]["exp_param"]))
    bts_sent_asc = sorted(bts_sent_time_series, key=lambda m: float(m["metric"]["exp_param"]))
    for i in range(len(exec_time_asc)):
        if int(exec_time_asc[i]["metric"]["state_length"]) != int(msgs_sent_asc[i]["metric"]["exp_param"]):
            raise ValueError("Results not matching")
        x = int(exec_time_asc[i]["metric"]["state_length"])
        exec_time = str(float(exec_time_asc[i]["value"][1])).replace(".", ",")
        msgs_sent = int(msgs_sent_asc[i]["value"][1])
        bts_sent = int(bts_sent_asc[i]["value"][1])
        data_points.append({"req": x, "exec_time": exec_time,
                            "msgs_sent": msgs_sent, "bytes_sent": bts_sent})

    # build key:val pairs for data points and return
    return data_points

def main():
    logger.info("Starting data extraction for self-stabilization overhead experiment")
    exec_time_series = api.get_time_series_for_q(Q_EXEC_TIME)
    msgs_sent_time_series = api.get_time_series_for_q(Q_MSGS_SENT)
    bytes_sent_time_series = api.get_time_series_for_q(Q_BYTES_SENT)

    if len(exec_time_series) == 0:
        logger.warning("No results found, quitting")
        return
    data_points = transform(exec_time_series, msgs_sent_time_series, bytes_sent_time_series)
    csv_path = helpers.write_to_csv(EXPERIMENT, data_points)
    snapshot_path = helpers.get_snapshot()
    helpers.collect_to_res_folder(EXPERIMENT, [csv_path, snapshot_path])
    helpers.cleanup()

if __name__ == "__main__":
    main()