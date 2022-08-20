import grpc
import location_pb2
import location_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel(
    "udaconnect-location.staging.udacity.impara8.com:5005")
# "localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

# Update this with desired payload
location = location_pb2.LocationMessage(
    creation_time="2020-08-18T10:37:06",
    longitude="37.553441",
    person_id=1,
    id=30,
    latitude="-122.290524",
)


response = stub.Create(location)
print(response)
