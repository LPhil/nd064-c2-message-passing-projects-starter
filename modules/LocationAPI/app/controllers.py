from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from werkzeug.exceptions import abort, HTTPException

from udadb import LocationService, LocationSchema, Location


api = Namespace("Locations", description="Locations API Microservice.")  # noqa

@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        try:
            request.get_json()
            location: Location = LocationService.create(request.get_json())
            return location

        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(500)

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        try:
            location: Location = LocationService.retrieve(location_id)
            return location

        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(500)
