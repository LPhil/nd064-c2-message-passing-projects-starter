import grpc, logging

from concurrent import futures
from flask import Flask
from gevent import pywsgi

from app.LocationProducer import create_app

# Setup flask
app = Flask(__name__)
# Setup gRPC server
grpc_server = grpc.server(futures.ThreadPoolExecutor()) # 3.8: Default value of max_workers is changed to min(32, os.cpu_count() + 4).

if __name__ == "__main__":
    create_app(app, grpc_server)
    print("Starting gRPC server on port 5005...")
    grpc_server.add_insecure_port("[::]:5005")
    grpc_server.start()
    # Keep thread alive
    # grpc_server.wait_for_termination()
    http_server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
