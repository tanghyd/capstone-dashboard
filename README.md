# capstone-dashboard

Dashboard application to be run via Docker on AWS

Build docker in directory using Dockerfile specification.

`docker build -t capstone-dashboard`

Run docker routing all port 80 (HTTP) requests to the dashboard hosted on port 8080.

`docker run -p 80:8080 -dit --name dashboard capstone-dashboard`
