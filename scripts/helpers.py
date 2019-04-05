import os
import logging
import time
import api
import csv
import requests
import shutil

logger = logging.getLogger(__name__)

def generate_res_name(experiment):
    n = api.get_number_of_nodes()
    t = time.strftime("%y%m%d_%H%M")
    return f"{experiment}_{n}_{t}"

def write_to_csv(experiment, data_points):
    filename = f"{generate_res_name(experiment)}.csv"
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    path = f"tmp/{filename}"
    with open(path, "w") as f:
        w = csv.DictWriter(f, data_points[0].keys())
        w.writeheader()
        for p in data_points:
            w.writerow(p)
    logger.info(f"Writing data to {path}")
    return os.path.abspath(path)


def get_snapshot():
    snapshot_name = api.create_snapshot()
    logger.info(f"Snapshot {snapshot_name} created")
    path = os.path.abspath(f"../prometheus/data/data/snapshots/{snapshot_name}")
    if not os.path.exists(path):
        raise ValueError(f"Snapshot path {path} does not exist, quitting")
    return path

def collect_to_res_folder(experiment, paths):
    folder_name = generate_res_name(experiment)
    folder_path = f"results/{folder_name}"
    os.makedirs(folder_path)
    for p in paths:
        os.rename(p, f"{os.path.abspath(folder_path)}/{p.split('/')[-1]}")

def cleanup():
    shutil.rmtree("tmp", ignore_errors=True)