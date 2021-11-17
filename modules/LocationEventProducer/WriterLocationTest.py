import grpc
import locationevent_pb2, locationevent_pb2_grpc

from datetime import datetime

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

#channel = grpc.insecure_channel("localhost:30010")
channel = grpc.insecure_channel("localhost:5005")
stub = locationevent_pb2_grpc.LocationServiceStub(channel)

print("Receiving sample payload...")
response = stub.Get(locationevent_pb2.Empty())
print(response)

# Update this with desired payload
locaction = locationevent_pb2.LocationEvent(
    user_id = 6,
    latitude = 23424.52342,
    longitude = -453234.6343,
    creation_time = datetime.now().timestamp()
)

print("Sending sample payload...")
response = stub.Create(locaction)
print(response)