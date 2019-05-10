# input: metric msgs_during_exp

import logging
import api
import helpers
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EXPERIMENT = "msg_distribution"
VE = "VIEW_ESTABLISHMENT"
REP = "REPLICATION"
PM = "PRIMARY_MONITORING"
FD = "FAILURE_DETECTOR"

def calculate_msg_distribution(req_count):
    logger.info("Starting data extraction for calculating message distribution from experiment with {req_count} requests")
    msg_count_time_series = api.get_time_series_for_q(f"msgs_during_exp{{exp_param='{req_count}'}}")
    counts = { VE: 0, REP: 0, PM: 0, FD: 0 }
    # sum all module message counts over nodes
    logger.info("Summing message count over all nodes")
    for node_count in msg_count_time_series:
        data = node_count["metric"]
        counts[VE] += int(data["view_est_msgs"])
        counts[REP] += int(data["rep_msgs"])
        counts[PM] += int(data["prim_mon_msgs"])
        counts[FD] += int(data["fd_msgs"])

    logger.info(f"Calculating message distribution from {counts}")
    # calculate total number of messages
    total = 0
    for cnt in counts.values():
        total += cnt
    # calculate distribution
    dist = {
        VE: (counts[VE] / total) * 100,
        REP: (counts[REP] / total) * 100,
        PM: (counts[PM] / total) * 100,
        FD: (counts[FD] / total) * 100
    }
    return dist

def calculate_bytes_distribution(req_count):
    logger.info("Starting data extraction for calculating bytes distribution from experiment with {req_count} requests")
    msg_count_time_series = api.get_time_series_for_q(f"bytes_during_exp{{exp_param='{req_count}'}}")
    bts = { VE: 0, REP: 0, PM: 0, FD: 0 }
    # sum all module message counts over nodes
    logger.info("Summing bytes count over all nodes")
    for node_count in msg_count_time_series:
        data = node_count["metric"]
        bts[VE] += int(data["view_est_bytes"])
        bts[REP] += int(data["rep_bytes"])
        bts[PM] += int(data["prim_mon_bytes"])
        bts[FD] += int(data["fd_bytes"])

    logger.info(f"Calculating bytes distribution from {bts}")
    # calculate total number of messages
    total = 0
    for cnt in bts.values():
        total += cnt
    # calculate distribution
    dist = {
        VE: (bts[VE] / total) * 100,
        REP: (bts[REP] / total) * 100,
        PM: (bts[PM] / total) * 100,
        FD: (bts[FD] / total) * 100
    }
    return dist

def main():
    if len(sys.argv) != 2:
        raise ValueError("Run as python msg_distribution.py REQ_COUNT")
    req_count = int(sys.argv[1]) - 1
    msg_dist = calculate_msg_distribution(req_count)
    logger.info(f"Calculation of message distribution finished, result {msg_dist}")
    bytes_dist = calculate_bytes_distribution(req_count)
    logger.info(f"Calculation of bytes distribution finished, result {bytes_dist}")

    logger.info(f"\n\n### Result ###\n" +
                f"### Message distribution ###\n" +
                f"{VE}: {round(msg_dist[VE])}%\n{REP}: {round(msg_dist[REP])}%\n" +
                f"{PM}: {round(msg_dist[PM])}%\n{FD}: {round(msg_dist[FD])}%" + 
                f"\n\n### Bytes distribution ###\n" +
                f"{VE}: {round(bytes_dist[VE])}%\n{REP}: {round(bytes_dist[REP])}%\n" +
                f"{PM}: {round(bytes_dist[PM])}%\n{FD}: {round(bytes_dist[FD])}%")

if __name__ == "__main__":
    main()