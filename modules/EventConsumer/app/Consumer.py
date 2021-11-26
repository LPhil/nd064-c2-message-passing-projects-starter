import os, json, logging

from datetime import datetime
from kafka import KafkaConsumer
from sqlalchemy import create_engine, exc

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup Kafka producer
KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
KAFKA_HOST = os.environ["KAFKA_HOST"]

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_HOST)

def dbsave(location):
    try:
        engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=False)
        conn = engine.connect()

        user_id = int(location["user_id"])
        latitude, longitude = float(location["latitude"]), float(location["longitude"])
        creation_time = float(location["creation_time"])

        insert = "INSERT INTO location (person_id, coordinate, creation_time) VALUES ({}, ST_Point({}, {}), ('{}'))" \
            .format(user_id, latitude, longitude, datetime.fromtimestamp(creation_time).isoformat())

        conn.execute(insert)
        logging.debug(insert)

    except exc.SQLAlchemyError as err:
        logger.error(err)


def start_consumer():
    try:
        logger.info("start_consumer called")
        for location in consumer:
            message = location.value.decode('utf-8')
            logger.debug('consuming {}'.format(message))

            location_message = json.loads(message)
            logger.info('message {}'.format(location_message))
            dbsave(location_message)

    except KeyboardInterrupt:
        logger.warning("Detected signal exit. Exiting application ...")

    consumer.close()