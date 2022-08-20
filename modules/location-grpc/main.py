import time
from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc

from app.udaconnect.models import Location

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from sqlalchemy.ext.declarative import declarative_base


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def __init__(self) -> None:
        DB_USERNAME = os.environ["DB_USERNAME"]
        DB_PASSWORD = os.environ["DB_PASSWORD"]
        DB_HOST = os.environ["DB_HOST"]
        DB_PORT = os.environ["DB_PORT"]
        DB_NAME = os.environ["DB_NAME"]

        engine = create_engine(
            f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        SessionClass = sessionmaker(engine)
        self.session = SessionClass()

    def Get(self, request, context):
        id = request.id
        location = self.session.query(
            Location).filter(Location.id == id).first()
        print("Location: {}".format(location))
        if location is None:
            return location_pb2.LocationMessage(
                id=id,
                person_id=None,
                longitude=None,
                latitude=None,
                creation_time=None
            )
        else:
            return location_pb2.LocationMessage(**{
                "id": location.id,
                "person_id": location.person_id,
                "longitude": location.longitude,
                "latitude": location.latitude,
                "creation_time": location.creation_time.isoformat(),
            })

    def Create(self, request, context):

        request_value = {
            "creation_time": request.creation_time,
            "longitude": request.longitude,
            "person_id": int(request.person_id),
            "id": int(request.id),
            "latitude": request.latitude,
        }
        print(request_value)

        return location_pb2.LocationMessage(**request_value)


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(
    LocationServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
