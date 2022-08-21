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
    longitude="37.5534409999999994",  # "37.55363",
    person_id=6,
    latitude="-153.2905240000000049",  # "-122.290883",
)


response = stub.Create(location)
print(response)
