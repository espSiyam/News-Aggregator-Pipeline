# Apache-Airflow
Steps to run the project:
1. Run in cmd: docker compose up airflow-init
2. Run docker-compose up
3. Open this url to the browser: http://localhost:8080/login/?next=http%3A%2F%2Flocalhost%3A8080%2Fhome


After changing the requirement.txt:
1. build the composer: docker-compose build
2. docker-compose up


Note: can't upload data to gcp from airflow directly as it is running on a docker server, we need separate permission apart from the permission we have on our local machine. May be service account may help.