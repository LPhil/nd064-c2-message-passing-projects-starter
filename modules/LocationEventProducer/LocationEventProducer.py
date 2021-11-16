import json, os, logging
import locationevent_pb2, locationevent_pb2_grpc

from flask import jsonify, request
from kafka import KafkaProducer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup Kafka producer
KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
KAFKA_HOST = os.environ["KAFKA_HOST"]
producer = KafkaProducer(bootstrap_servers=KAFKA_HOST)

class LocationEventProducer(locationevent_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        logger.info("Message received: " + request)

        kafka_request = {
            "UserID": request.UserID,
            "Latitude": request.Latitude,
            "Longitude": request.Longitude,
            "CreationDate": request.CreationDate
        }

        producer.send(KAFKA_TOPIC, json.dumps(kafka_request).encode())
        producer.flush()

        logger.info("Forward to Kafka Broker: " + kafka_request)
        return locationevent_pb2.LocationMessage(**kafka_request)


def create_app(flask, server):
    locationevent_pb2_grpc.add_LocationServiceServicer_to_server(LocationEventProducer, server)

    @flask.route('/health')
    def health():
        return jsonify("I am healthy!")