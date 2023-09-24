# Airflow DAG with SparkSubmitOperator Sample

This repository contains a sample Airflow DAG (Directed Acyclic Graph) that uses the SparkSubmitOperator to submit Spark jobs. This is a basic setup to demonstrate how to integrate Apache Airflow with Apache Spark using the SparkSubmitOperator.

## Project Structure

The project is organized as follows:

- **spark_dag_src/**: This directory contains Spark applications that serve as tasks for your DAG. You can place your Spark job scripts here.

- **spark_test/**: This directory contains unit tests for your Spark tasks. It's important to thoroughly test your Spark code to ensure it behaves as expected.

- **dag_spark_submit_operator.py**: This is the main Airflow DAG definition file. It orchestrates the execution of Spark jobs using the SparkSubmitOperator. You can customize this file to define your DAG structure.

## Getting Started

Follow these steps to get started with the project:

### Prerequisites

- Git (for cloning the repository)
- Python (for running Airflow and installing dependencies)
- Apache Airflow (if not already installed, you can follow the [official installation guide](https://airflow.apache.org/docs/apache-airflow/stable/start.html))
- Apache Spark (if not already installed, you can follow the [official installation guide](https://spark.apache.org/docs/latest/api/python/getting_started/index.html))
- install the libs with requirements.txt 
  ```bash
    pip install -r requirements.txt
  ```
- Change Gitlab-ci variables
  ```bash
  YOUR_REGISTERY_IMAGE, AIRFLOW_DEVELOPMENT_PATH, PRODUCTION_REPO_URL, YOUR_REGISTERY_PRODUCTION_IMAGE, YOUR_AIRFLOW_HOST_IP, PRODUCTION_REPO_URL
  ```
- Read the Dag Code and change the info with your custom Variables

### Clone the Repository

```bash
git clone https://github.com/mhzauser/airflow-dag-spark.git
```
### setup your environment
- clone the project and setup changes
- when set the tag and runners start your dag update automatically

enjoy :D

### TODO 
- [ ] description for dag
- [ ] description for cutoff and lineage concept

