from setuptools import setup

setup(
  name='UdaDB',
  version='0.1.0',
  packages=['udadb'],
  install_requires=[
      "flask_sqlalchemy==2.5.1",
      "geoalchemy2==0.9.4",
      "marshmallow==3.14.1",
      "marshmallow_sqlalchemy==0.26.1",
      "Shapely==1.8.0",
      "SQLAlchemy==1.4.27",
  ],
)