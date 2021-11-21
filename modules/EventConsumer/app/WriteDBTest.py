import os, json, logging

from datetime import datetime
from sqlalchemy import create_engine, exc

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)
conn = engine.connect()

insert = "INSERT INTO location (person_id, coordinate, creation_time) VALUES ({}, ST_Point({}, {}), ('{}'))" \
    .format(8, 23424, 453234, datetime.fromtimestamp(1637172615.0))
print(insert)
conn.execute(insert)
