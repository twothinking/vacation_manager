FROM python:3.6-slim

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && \
    apt-get install -y libssl-dev && \
    pip install --upgrade pip

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install -e .
EXPOSE 80
CMD ["python", "vacation_manager.py"]