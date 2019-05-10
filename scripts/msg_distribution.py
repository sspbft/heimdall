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

def main():
    if len(sys.argv) != 2:
        raise ValueError("Run as python msg_distribution.py REQ_COUNT")
    req_count = int(sys.argv[1]) - 1
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
    logger.info(f"Calculation finished, result: {dist}\n\n### Result ###\n" + 
                f"{VE}: {round(dist[VE])}%\n{REP}: {round(dist[REP])}%\n" +
                f"{PM}: {round(dist[PM])}%\n{FD}: {round(dist[FD])}%")

if __name__ == "__main__":
    main()