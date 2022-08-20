from typing import Dict
from concurrent import futures

from app.udaconnect.models import Location

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import json

from sqlalchemy.ext.declarative import declarative_base
from kafka import KafkaConsumer

from geoalchemy2.functions import ST_Point
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema

TOPIC_NAME = 'locations'
KAFKA_SERVER = 'kafka:9092'
consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER)

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

engine = create_engine(
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
conn = engine.connect()

for x in consumer:
    message = json.loads(x.value.decode('utf-8'))
    person_id = message["person_id"]
    latitude = message["latitude"]
    longitude = message["longitude "]
    insert = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))" \
        .format(person_id, latitude, longitude)

    print(insert)
    conn.execute(insert)
