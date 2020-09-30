FROM continuumio/miniconda3

COPY requirements.txt /tmp/
COPY ./app /app
WORKDIR "/app"

RUN conda install --file /tmp/requirements.txt  --channel anaconda --channel conda-forge

ENTRYPOINT [ "python" ]
CMD [ "index.py" ]
