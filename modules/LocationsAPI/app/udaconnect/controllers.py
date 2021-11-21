from datetime import datetime

from app.udaconnect.models import Location, Person
from app.udaconnect.schemas import (
    ConnectionSchema,
    LocationSchema,
    PersonSchema
)
from app.udaconnect.services import LocationService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from werkzeug.exceptions import abort
from typing import Optional, List

#DATE_FORMAT = "%Y-%m-%d"

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
        except:
            abort(500)

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        try:
            location: Location = LocationService.retrieve(location_id)
            return location
        except:
            abort(500)


#@api.route("/persons/<person_id>/connection")
#@api.param("start_date", "Lower bound of date range", _in="query")
#@api.param("end_date", "Upper bound of date range", _in="query")
#@api.param("distance", "Proximity to a given user in meters", _in="query")
#class ConnectionDataResource(Resource):
#    @responds(schema=ConnectionSchema(many=True))
#    def get(self, person_id) -> ConnectionSchema:
#        try:
#            start_date: datetime = datetime.strptime(
#                request.args["start_date"], DATE_FORMAT
#            )
#            end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
#            distance: Optional[int] = request.args.get("distance", 5)
#
#            results = ConnectionService.find_contacts(
#                person_id=person_id,
#                start_date=start_date,
#                end_date=end_date,
#                meters=distance,
#            )
#            return results
#        except:
#            abort(500)