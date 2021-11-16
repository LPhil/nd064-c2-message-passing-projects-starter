import grpc

from flask import Flask
from gevent.pywsgi import WSGIServer

from concurrent import futures
from LocationEventProducer import create_app

# Setup flask
flask_app = Flask(__name__)
# Setup gRPC server
grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))

if __name__ == "__main__":
    create_app(flask_app, grpc_server)
    print("Starting gRPC server on port 5005...")
    grpc_server.add_insecure_port("[::]:5005")
    grpc_server.start()
    # Keep thread alive
    # grpc_server.wait_for_termination()
    http_server = WSGIServer(('', 5000), flask_app)
    http_server.serve_forever()
    #flask_server.run(debug=True, host="0.0.0.0")
