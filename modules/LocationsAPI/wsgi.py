import os

from gevent import pywsgi
from app import create_app

app = create_app(os.getenv("FLASK_ENV") or "test")
if __name__ == "__main__":
    http_server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()