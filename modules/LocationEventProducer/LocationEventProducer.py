import json, os, logging
import locationevent_pb2, locationevent_pb2_grpc

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

        kafka_request = {
            "user_id": request.user_id,
            "latitude": request.latitude,
            "longitude": request.longitude,
            "creation_time": request.creation_time
        }

        producer.send(KAFKA_TOPIC, json.dumps(kafka_request).encode())
        producer.flush()

        logger.info("Forward request Kafka Broker: " + json.dumps(kafka_request))
        return locationevent_pb2.LocationEvent(**kafka_request)

    def Get(self, request, context):
        return locationevent_pb2.LocationEvent(
            user_id = 42,
            latitude = -127,
            longitude = 250,
            creation_time = str(datetime.now())
        )


def create_app(flask, server):
    locationevent_pb2_grpc.add_LocationServiceServicer_to_server(LocationEventProducer(), server)

    @flask.route('/health')
    def health():
        return jsonify("I am healthy!")