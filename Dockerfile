FROM python:3.10-slim-buster 
USER root 
RUN mkdir /app
COPY . /app/ 
WORKDIR /app/ 
RUN pip3 install -r requirements.txt 
ENV AWS_DEFAULT_REGIION="us-east-2"
ENV BUCKET_NAME="mynetworksecurity33"
ENV PREDICTION_BUCKET_NAME="my-network-datasource"
ENV AIRFLOW_HOME="/app/airflow"
ENV AIRFLOW_CORE_DAGBAG_IMPORT_TIMEOUT=1000
ENV AIRFLOW_CORE_ENABLE_XCOM_PICKLING=True 
RUN airflow db init
RUN airflow users create \
    --username admin \
    --firstname sowmya \
    --lastname am \
    --role Admin \
    --email sowmya.anekonda@gmail.com \
    --password admin
# RUN airflow users create -e sowmya.anekonda@gmail.com -f sowmya -l am -p admin -r Admin -u admin 
RUN chmod 777 start.sh 
RUN apt update -y 
ENTRYPOINT [ "/bin/sh" ]
CMD ["start.sh"]