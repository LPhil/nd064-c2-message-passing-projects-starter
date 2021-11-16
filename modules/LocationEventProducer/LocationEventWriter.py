import grpc
import locationevent_pb2
import locationevent_pb2_grpc

from datetime import datetime

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

channel = grpc.insecure_channel("localhost:30010")
#channel = grpc.insecure_channel("localhost:5005")
stub = locationevent_pb2_grpc.LocationServiceStub(channel)


print("Sending sample payload...")
response = stub.Get(locationevent_pb2.Empty())
print(response)

# Update this with desired payload
locaction = locationevent_pb2.LocationEvent(
    user_id = 25,
    latitude = 130,
    longitude = -240,
    creation_time = str(datetime.now())
)

print("Sending sample payload...")
response = stub.Create(locaction)
print(response)
