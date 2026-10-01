# 🛒 AWS Retail Data Pipeline

An end-to-end **Retail Data Engineering Pipeline** built with **Python, Apache Airflow, Amazon S3, AWS Athena, and EC2** using a **Medallion Architecture**.

## 🏗️ Architecture

```text
Raw Data → Amazon S3 → 🥉 Bronze → 🥈 Silver → 🥇 Gold → AWS Athena → 📊 Reports
```

**Apache Airflow** orchestrates the complete pipeline on **AWS EC2**.

## 🛠️ Tech Stack

* **Language:** Python, Bash
* **Orchestration:** Apache Airflow
* **Storage:** Amazon S3
* **Analytics:** AWS Athena
* **Compute:** Amazon EC2
* **Libraries:** Pandas, Boto3
* **Version Control:** Git, GitHub

## 📁 Project Structure

```text
retail_mgmt_aws/
├── airflow/
│   └── dags/
│       └── retail_dag.py
├── python_scripts/
│   ├── bronze_load.py
│   ├── silver_load.py
│   ├── gold_load.py
│   ├── athena_setup.py
│   └── generate_reports.py
├── requirements.txt
└── README.md
```

## 🚀 Run

```bash
git clone https://github.com/amankumar-dev/retail_mgmt_aws.git
cd retail_mgmt_aws

python3 -m venv retail_mgmt_venv
source retail_mgmt_venv/bin/activate

pip install -r requirements.txt
airflow standalone
```

Open:

```text
http://<EC2-PUBLIC-IP>:8080
```

Trigger the `retail_pipeline` DAG and monitor:

```text
Bronze → Silver → Gold → Athena → Reports
```

## 🔐 AWS Setup

The pipeline uses an **EC2 IAM Role** for AWS authentication and **Amazon S3** as the central data storage layer.

```text
EC2 + Airflow → S3 → Bronze → Silver → Gold → Athena
```

## ✨ Key Features

* ☁️ Cloud-based data pipeline
* 🔄 Automated workflow orchestration
* 🏗️ Medallion Architecture
* 📦 S3-based data lake
* 🔍 Serverless analytics with Athena
* 📊 Automated report generation

## 👨‍💻 Author

**Aman Kumar**

*Data Engineering Enthusiast Building End-to-End Data Pipelines*
