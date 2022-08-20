import time
import json
from concurrent import futures

from app.udaconnect.models import Location

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from sqlalchemy.ext.declarative import declarative_base
from kafka import KafkaConsumer

TOPIC_NAME = 'locations'
KAFKA_SERVER = 'kafka:9092'
consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER)
for message in consumer:
    print(message)
