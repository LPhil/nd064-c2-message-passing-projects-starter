import grpc

from proto import locationevent_pb2, locationevent_pb2_grpc
from datetime import datetime

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

channel = grpc.insecure_channel("localhost:30005")
stub = locationevent_pb2_grpc.LocationServiceStub(channel)

# Fix sample payload
print("Receiving sample payload...")
response = stub.Get(locationevent_pb2.Empty())
print(response)


# Update this with desired payload
locaction = locationevent_pb2.LocationEvent(
    user_id = 1,
    latitude = 27.523434535432,
    longitude = -25.6344353453,
    creation_time = datetime.now().timestamp()
)

print("Sending sample payload...")
response = stub.Create(locaction)
print(response)


# payload with error respond
locaction = locationevent_pb2.LocationEvent(
    user_id = 25,
    latitude = 27.52342,
    longitude = -25.6343,
    creation_time = datetime.now().timestamp()
)

print("Sending sample payload, expect error...")
response = stub.Create(locaction)
print(response)
