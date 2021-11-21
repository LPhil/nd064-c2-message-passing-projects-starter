import json, os, logging
from proto import locationevent_pb2, locationevent_pb2_grpc

from datetime import datetime
from flask import jsonify
from kafka import KafkaProducer

# Setup logging and misc
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup Kafka producer
KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
KAFKA_HOST = os.environ["KAFKA_HOST"]
producer = KafkaProducer(bootstrap_servers=KAFKA_HOST)

class LocationEventProducer(locationevent_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        logger.debug("Message received")

        creation_time = datetime.fromtimestamp(request.creation_time)
        kafka_request = {
            "user_id": request.user_id,
            "latitude": request.latitude,
            "longitude": request.longitude,
            "creation_time": creation_time.replace(microsecond=0).timestamp()
        }

        producer.send(KAFKA_TOPIC, json.dumps(kafka_request).encode())
        producer.flush()

        logger.info("Forward request for topic '{}' to kafka-broker: {} ".format(KAFKA_TOPIC, json.dumps(kafka_request)))
        return locationevent_pb2.LocationEvent(**kafka_request)

    def Get(self, request, context):
        return locationevent_pb2.LocationEvent(
            user_id = 42,
            latitude = -1237.923,
            longitude = 2850.2791,
            creation_time = datetime.now().timestamp()
        )


def create_app(flask, server):
    locationevent_pb2_grpc.add_LocationServiceServicer_to_server(LocationEventProducer(), server)

    @flask.route('/health')
    def health():
        return jsonify("I am healthy!")