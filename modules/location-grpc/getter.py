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

response = stub.Get(location_pb2.LocationID(id=29))
print(response)
