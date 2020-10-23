# capstone-dashboard

## Flask
Run with Flask on 0.0.0.0 port 8080:
`cd dashboard`
`python index.py`

This can be changed in `dashboard/index.py`

## Gunicorn
Run with Gunicorn on 0.0.0.0 port 8080:
`cd dashboard`
`gunicorn -b 0.0.0.0:8080 wsgh:server`

## Docker
Note: Had some issues with some ports on my local machine and couldn't test Docker with the new Gunicorn server.

Build docker in directory using Dockerfile specification.

`docker build -t capstone-dashboard .`

Run docker routing all port 80 (HTTP) requests to the dashboard hosted on port 8080.

`docker run -p 80:8080 -dit --name dashboard capstone-dashboard`
