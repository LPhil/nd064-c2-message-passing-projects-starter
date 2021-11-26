from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import List
from werkzeug.exceptions import abort, HTTPException

from udadb import Person, PersonSchema, PersonService

api = Namespace("Persons", description="Persons API Microservice.")  # noqa

@api.route("/persons")
@api.doc(responses={200: 'Success'})
@api.doc(responses={500: 'Internal Server Error'})
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        try:
            payload = request.get_json()
            new_person: Person = PersonService.create(payload)
            return new_person

        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(500)

    @responds(schema=PersonSchema(many=True))
    def get(self) -> List[Person]:
        try:
            persons: List[Person] = PersonService.retrieve_all()
            return persons

        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(500)

@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
@api.doc(responses={200: 'Success'})
@api.doc(responses={404: '<person_id> not found'})
@api.doc(responses={500: 'Internal Server Error'})
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        try:
            person: Person = PersonService.retrieve(person_id)
            if person is None:
                abort(404)
            return person

        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(500)