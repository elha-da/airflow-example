# Debian GNU/Linux 10
ARG AIRFLOW_VERSION
FROM apache/airflow:$AIRFLOW_VERSION

USER root

COPY /requirements.txt /requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /requirements.txt

USER airflow
