FROM prefecthq/prefect:2-latest-conda

COPY docker-requirement.txt .

RUN pip install -r docker-requirement.txt --trusted-host pypi.python.org --no-cache-dir

COPY flows /opt/prefect/flows

RUN mkdir -p /opt/prefect/new_data/yellow