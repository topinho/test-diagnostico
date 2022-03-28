import json, os
from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api

from app.modelos.Persona import Persona

class Personas(Resource):
    def get(self):
        ret = []
        res = Persona.query.all()
        if res:
            for p in res:
                ret.append(
                    {
                        'identificacion': p.identificacion,
                        'nombre': p.nombre,
                        'apellido': p.apellido
                    }
                )
        return ret, 200

class PersonaSave(Resource):
    def post(self):
        data = request.get_json()
        #return {"data": data}, 200
        if data is None:
            return {"success": False, "message": "Faltan datos del json"}, 401
        
        try:
            dataJson = {}
            dataJson['identificacion'] = data["identificacion"]
            dataJson['nombre'] = data["nombre"]
            dataJson['apellido'] = data["apellido"]
            PersonaInsert = Persona.insert_data(dataJson)
            # return PersonatInsert
            PersonaId = PersonaInsert['response']['data']['last_id']
            return {'success': True, 'mensaje': "Acción realizada con éxito.", 'data': PersonaId}, 200
    
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # exc_type, fname, exc_tb.tb_lineno
            msj = 'Error: ' + str(exc_obj) + ' File: ' + \
                fname + ' linea: ' + str(exc_tb.tb_lineno)
            return {'success': False, 'mensaje': str(msj)}, 500