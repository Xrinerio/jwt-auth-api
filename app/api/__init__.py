from flask_restx import Api

from .auth.endpoints import api as ns1

api = Api(prefix="/api/", doc="/api/doc")

api.add_namespace(ns1)