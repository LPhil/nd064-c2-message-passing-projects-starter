from datetime import datetime
from flask import request
from flask_accepts import responds
from flask_restx import Namespace, Resource
from typing import Optional
from werkzeug.exceptions import abort, HTTPException

from udadb import Connection, ConnectionSchema, ConnectionService

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("Connections", description="Connections API Microservice.")  # noqa

@api.route("/connection/<person_id>")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema(many=True))
    def get(self, person_id) -> ConnectionSchema:
        try:
            start_date: datetime = datetime.strptime(
                request.args["start_date"], DATE_FORMAT
            )
            end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
            distance: Optional[int] = request.args.get("distance", 5)

            results = ConnectionService.find_contacts(
                person_id=person_id,
                start_date=start_date,
                end_date=end_date,
                meters=distance,
            )
            return results

        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(500)