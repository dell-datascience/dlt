FROM python:3.9

RUN pip install uuid

WORKDIR app/

COPY python.py python.py

ENTRYPOINT ["bash"]