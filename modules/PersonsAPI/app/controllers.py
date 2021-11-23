from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import List
from werkzeug.exceptions import abort

from udadb import Person, PersonSchema, PersonService


api = Namespace("Persons", description="Persons API Microservice.")  # noqa

@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        try:
            payload = request.get_json()
            new_person: Person = PersonService.create(payload)
            return new_person
        except:
            abort(500)

    @responds(schema=PersonSchema(many=True))
    def get(self) -> List[Person]:
        try:
            persons: List[Person] = PersonService.retrieve_all()
            return persons
        except:
            abort(500)

@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        try:
            person: Person = PersonService.retrieve(person_id)
            return person
        except:
            abort(500)