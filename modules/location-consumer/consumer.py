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
SessionClass = sessionmaker(engine)
session = SessionClass()

for x in consumer:
    message = json.loads(x.value.decode('utf-8'))
    new_location = Location()
    new_location.person_id = message["person_id"]
    new_location.id = message["id"]
    new_location.creation_time = message["creation_time"]
    new_location.coordinate = ST_Point(
        message["latitude"], message["longitude"])
    print(new_location)
    validation_results: Dict = LocationSchema().validate(new_location)
    if validation_results:
        print(f"Unexpected data format in payload: {validation_results}")
        raise Exception(f"Invalid payload: {validation_results}")

    session.add(new_location)
    session.commit()
    print(new_location)
