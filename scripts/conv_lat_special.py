# input: metric client_req_exec_time
# output: 1 series, x value: client request, y value: exec time

import logging
import api
import helpers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EXPERIMENT = "convergence_latency"
Q_CONV_LAT = (f"bottomk({4*api.get_number_of_byz()+1}, convergence_latency) by (view)")
Q_CONV_LAT_max = (f"max(bottomk({4*api.get_number_of_byz()+1}, convergence_latency) by (view)) by(view)")

def transform(conv_lat_time_series, conv_lat_max_time_series): #, msgs_sent_time_series, bts_sent_time_series):
    data_points = []
    # sort data points ASC wrt view
    conv_lat_asc = sorted(conv_lat_time_series, key=lambda m: float(m["metric"]["view"]))
    conv_lat_asc_max = sorted(conv_lat_max_time_series, key=lambda m: float(m["metric"]["view"]))

    for i in range(len(conv_lat_asc)):

        conv_lat = str(float(conv_lat_asc[i]["value"][1])).replace(".", ",")
        view = int(conv_lat_asc[i]["metric"]["view"])
        node = str(conv_lat_asc[i]["metric"]["node_id"])
        data_points.append({ "old_view": view, "conv_lat": conv_lat, "node": node}),
                            #"msgs_sent": msgs_sent, "bytes_sent": bts_sent})
    
    conv_lat = str(float(conv_lat_asc_max[0]["value"][1])).replace(".", ",")
    view = int(conv_lat_asc_max[0]["metric"]["view"])
    data_points.append({"old_view": view, "conv_lat": conv_lat, "node": "MAX"})

    # build key:val pairs for data points and return
    return data_points

if __name__ == "__main__":
    logger.info("Starting data extraction for convergence latency experiment")
    conv_lat_time_series = api.get_time_series_for_q(Q_CONV_LAT)
    conv_lat_max_time_series = api.get_time_series_for_q(Q_CONV_LAT_max)
    data_points = transform(conv_lat_time_series, conv_lat_max_time_series)
    csv_path = helpers.write_to_csv(EXPERIMENT, data_points)
    snapshot_path = helpers.get_snapshot()
    helpers.collect_to_res_folder(EXPERIMENT, [csv_path, snapshot_path])
    helpers.cleanup()