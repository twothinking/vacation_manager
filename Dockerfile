FROM python:3

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && \
    pip install --upgrade pip

COPY . /app
WORKDIR /app
RUN pip install -r web/requirements.txt
EXPOSE 80
ENTRYPOINT ["python"]
CMD ["web/VacationManager.py"]