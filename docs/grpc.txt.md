# GRPC Client Test
With this sample implementation, you can send the following payload to the grpc server

```bash
python modules/EventProducerAPI/WritergRPCTest.py
```
Put in a non-valid 'user_id' and get a gRPC 'NOT_FOUND' error, is also tested.

## Payload
message LocationEvent {
  int32 user_id = 1;
  double latitude = 2;
  double longitude = 3;
  double creation_time = 4;
}

message Empty { }

service LocationService {
    rpc Create(LocationEvent) returns (LocationEvent);
    rpc Get(Empty) returns (LocationEvent);
}
