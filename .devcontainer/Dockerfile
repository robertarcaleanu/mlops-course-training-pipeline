FROM python:3.11-slim

WORKDIR /workspaces

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    libssl-dev \
    git \
 && rm -rf /var/lib/apt/lists/*

# Set Airflow home directory
ENV AIRFLOW_HOME=/workspaces/mlops-course-training-pipeline
ENV AIRFLOW__CORE__DAGS_FOLDER=${AIRFLOW_HOME}/dags
ENV AIRFLOW__CORE__PLUGINS_FOLDER=${AIRFLOW_HOME}/plugins

# Set load examples to False for cleaner setup
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

# Upgrade pip and install specific version of Apache Airflow
RUN pip install --upgrade pip && \
    pip install apache-airflow==2.10.0 

# Copy requirements.txt and install additional dependencies
COPY requirements.txt /root/requirements.txt
RUN pip install -r /root/requirements.txt

EXPOSE 8081

# Initialize Airflow DB and create the admin user
RUN airflow db init && \
    airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com \
    --password admin

CMD ["bash"]
