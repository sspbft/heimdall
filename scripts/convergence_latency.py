# input: metric client_req_exec_time
# output: 1 series, x value: client request, y value: exec time

import logging
import api
import helpers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EXPERIMENT = "convergence_latency"
#Q_CONV_LAT = (f"max(bottomk({4*api.get_number_of_byz()+1}, convergence_latency) by (view)) by (view)")
Q_CONV_LAT = (f"max(bottomk(5, convergence_latency) by (view)) by (view)")
Q_MSGS_SENT = f"sum(msgs_during_exp) by (exp_param)"
Q_BYTES_SENT = f"sum(bytes_during_exp) by (exp_param)"

def transform(conv_lat_time_series, msgs_sent_time_series, bts_sent_time_series):
    data_points = []
    # sort data points ASC wrt state length, gives us client_reqs in ASC order
    conv_lat_asc = sorted(conv_lat_time_series, key=lambda m: float(m["metric"]["view"]))
    msgs_sent_asc = sorted(msgs_sent_time_series, key=lambda m: float(m["metric"]["exp_param"]))
    bts_sent_asc = sorted(bts_sent_time_series, key=lambda m: float(m["metric"]["exp_param"]))

    for i in range(len(conv_lat_asc)):
        # if int(conv_lat_asc[i]["metric"]["view"]) != int(msgs_sent_asc[i]["metric"]["exp_param"]):
        #     raise ValueError("Results not matching")
        conv_lat = str(float(conv_lat_asc[i]["value"][1])).replace(".", ",")
        view = int(conv_lat_asc[i]["metric"]["view"])
        msgs_sent = int(msgs_sent_asc[i]["value"][1])
        bts_sent = int(bts_sent_asc[i]["value"][1])
        data_points.append({ "old_view": view, "conv_lat": conv_lat,
                            "msgs_sent": msgs_sent, "bytes_sent": bts_sent})

    # build key:val pairs for data points and return
    return data_points

if __name__ == "__main__":
    logger.info("Starting data extraction for convergence latency experiment")
    conv_lat_time_series = api.get_time_series_for_q(Q_CONV_LAT)
    msgs_sent_time_series = api.get_time_series_for_q(Q_MSGS_SENT)
    bytes_sent_time_series = api.get_time_series_for_q(Q_BYTES_SENT)
    data_points = transform(conv_lat_time_series, msgs_sent_time_series, bytes_sent_time_series)
    csv_path = helpers.write_to_csv(EXPERIMENT, data_points)
    snapshot_path = helpers.get_snapshot()
    helpers.collect_to_res_folder(EXPERIMENT, [csv_path, snapshot_path])
    helpers.cleanup()