# Heimdall
Metrics environment used for gathering and visualization.

First, make sure you have Docker and docker-compose installed and then simply run `docker-compose up` and the Grafana container can be accessed on [localhost:3000](http://localhost:3000). Log in with `admin:admin` and start creating dashboards! The Grafana container is bootstrapped with a data source connected to the Prometheus container which is bootstrapped with metrics for the Prometheus service itself, just to demonstrate functionality. Remember to add the `prometheus/sd.json` file if dynamic service discovery is needed - otherwise it is fine to just modify `prometheus/prometheus.yml`.

## Adding targets to Prometheus
The Prometheus container is setup to scan a file `prometheus/sd.json` to enable dynamic service discovery, which is utilized by us in our Thor + BFTList setup. We have setup Thor to automatically generate the `sd.json` file with the appropriate targets depending on how many instances are currently being run of BFTList. This makes it possible to run an arbitrary amount of nodes and automatically get metrics for all of these with zero configuration. 

There is a sample json file, `prometheus/sample_sd.json` which can be used for testing when running two BFTList instances locally on ports.