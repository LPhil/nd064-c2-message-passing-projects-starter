import os, json, logging

from datetime import datetime
from kafka import KafkaConsumer
from sqlalchemy import create_engine, exc


engine = create_engine(f"postgresql://ct_admin:wowimsosecure@localhost:5432/geoconnections", echo=True)
conn = engine.connect()

insert = "INSERT INTO location (person_id, coordinate, creation_time) VALUES ({}, ST_Point({}, {}), ('{}'))" \
    .format(8, 23424, 453234, datetime.fromtimestamp(1637172615.0))
print(insert)
conn.execute(insert)
