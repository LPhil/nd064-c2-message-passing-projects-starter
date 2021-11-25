import json, os, logging
import grpc, requests

from datetime import datetime
from flask import jsonify
from kafka import KafkaProducer
from proto import locationevent_pb2, locationevent_pb2_grpc

# Setup logging and misc
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup Kafka producer
KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
KAFKA_HOST = os.environ["KAFKA_HOST"]
producer = KafkaProducer(bootstrap_servers=KAFKA_HOST)

# URI to check for existing persons
PERSONS_URI = os.environ["PERSONS_URI"]

class LocationEventProducer(locationevent_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        try:
            logger.debug("Message received")

            if PERSONS_URI:
                request_url = f'{PERSONS_URI}/{request.user_id}'
                logger.debug(f'Request URL {request_url}')
                r = requests.get(request_url)
                if not r:
                    logger.error("{} [{}]".format(request_url, r.status_code))
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(r.text)
                    return locationevent_pb2.LocationEvent()

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

        except Exception as e:
            logger.error(e)
            context.set_code(grpc.StatusCode.ABORTED)
            return locationevent_pb2.LocationEvent()


    def Get(self, request, context):
        return locationevent_pb2.LocationEvent(
            user_id = 42,
            latitude = -52.923,
            longitude = 27.2791,
            creation_time = datetime.now().timestamp()
        )


def create_app(flask, server):
    locationevent_pb2_grpc.add_LocationServiceServicer_to_server(LocationEventProducer(), server)

    @flask.route('/health')
    def health():
        return jsonify("I am healthy!")