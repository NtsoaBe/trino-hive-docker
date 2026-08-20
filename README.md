# trino-hive-docker
This project is a modern Data Lakehouse platform built around the Medallion Architecture, with Bronze, Silver, and Gold layers.
The platform progressively ingests, transforms, cleans, and enriches data as it moves through each layer, providing a structured foundation for analytics and downstream data consumption.

## Architechure Diagram

![Architecture Diagram](docs/Architecture_dataplatform.png)

## Architecture & Tech Stack
| Component | Technology | Description |
|---|---|---|
| Orchestrator | Pypyr | Executes YAML-based automation pipelines. |
| Compute Engine | Trino | Handles data transformation and querying. |
| Storage Layer | MinIO | Provides object storage for data. |
| Table Format | Apache Iceberg | Manages and organizes data tables. |



## How do we run the application
Step 0 - You need to install [here](https://docs.docker.com/get-started/get-docker/):
- Docker
- Docker compose 

Step 1 - Pull the project
```bash
git clone https://github.com/NtsoaBe/trino-hive-docker.git
```
Step 2 - Inside the project create a python venv, then install the requirements.txt
```bash
cd trino-hive-docker

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```


Step 3 -  Go to the docker_folder directory, run all the service with docker compose
```bash
cd docker_folder

docker compose up --build
```
## Service access
| Service | Port |
|---|---:|
| MinIO Web UI | 9003 |
| Trino Server | 8080 |

- You can use [Dbeaver] (https://dbeaver.io/), or [trino client] (https://trino.io/docs/current/client.html) if you want to connect to Trino server.
From trino client
```bash
trino --server http://localhost:8080
```

## Ressource creation
Run the workflow who automate the ressource creation
```bash
pypyr create_ressource_workflow
```
## Run the pipeline
You can run the entire pipeline using this command
```bash
pypyr pipeline
```
Then, heck the result
```sql
SELECT *
    FROM iceberg.project_weather.weather_hourly_silver;
```

## Future Work & Improvements
Upcoming planned improvements include:

- **Scalability:** Deploy the platform on a distributed Kubernetes cluster to support high availability and horizontal scalability.
- **Infrastructure as Code (IaC):** Introduce Terraform to automate infrastructure provisioning and ensure reproducible, version-controlled environments.
- **Semantic Layer Integration:** Integrate Cube Core as a centralized semantic layer and metric store, enabling BI developers and data analysts to securely and consistently query the platform's data.

