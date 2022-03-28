import os
import json
from flask import Flask
from flask_restful import Resource, Api

from app.modelos.User import User

class GetUser(Resource):
    def get(self):
        ret = []
        res = User.query.all()
        for user in res:
            ret.append(
                {
                    'username': user.username,
                    'email': user.email
                }
            )
        return ret, 200