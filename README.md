# Heimdall
Metrics environment used for gathering and visualization.

First, make sure you have [Docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/) installed and then simply run `docker-compose up` and the Grafana container can be accessed on [localhost:6060](http://localhost:6060). Log in with `admin:admin` and start creating dashboards! The Grafana container is bootstrapped with a data source connected to the Prometheus container which is bootstrapped with metrics for the Prometheus service itself, just to demonstrate functionality. Remember to add the `prometheus/sd.json` file if dynamic service discovery is needed - otherwise it is fine to just modify `prometheus/prometheus.yml`.

## Ports used

| Port number   | Service                       | 
| ------------- |:-----------------------------:|
| 6060          | Grafana                       |
| 6061          | Prometheus                    |

## Adding targets to Prometheus
The Prometheus container is setup to scan a file `prometheus/sd.json` to enable dynamic service discovery, which is utilized by us in our Thor + BFTList setup. We have setup Thor to automatically generate the `sd.json` file with the appropriate targets depending on how many instances are currently being run of BFTList. This makes it possible to run an arbitrary amount of nodes and automatically get metrics for all of these with zero configuration. 

There is a sample json file, `prometheus/sample_sd.json` which can be used for testing when running two BFTList instances locally on ports.

## Extracting data for visualization
```
cd scripts
python3.7 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Extracting data for self-stabilization overhead experiment
Run the following
```
cd scripts && source env/bin/activate
python ss_overhead.py
```
CSV file with data points will then be available in `results/`.

### Importing a Prometheus snapshot
```
mkdir prometheus/snapshots
cp -R PATH_TO_SNAPSHOT prometheus/snapshots
```

Modify the last line in `docker-compose.yml` and enter the correct snapshot name and run `docker-compose -f docker-compose.with-snapshot.yml up --force-recreate`, and all data in Prometheus will be loaded from the snapshot.