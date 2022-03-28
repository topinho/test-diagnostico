import json, os
from flask import Flask, request, jsonify, Response
from flask_restful import Resource, reqparse

from app.modelos.Inspeccion import Inspeccion

class Inspecciones(Resource):
    def get(self):
        ret = []
        res = Inspeccion.query.all()
        if res:
            for p in res:
                ret.append(
                    {
                        'marca': p.marca,
                        'modelo': p.modelo,
                        'patente': p.patente
                    }
                )
        return ret, 200

class InspeccionSave(Resource):
    def post(self):
        data = request.get_json()
        #return {"data": data}, 200
        if data is None:
            return {"success": False, "message": "Faltan datos del json"}, 401
        
        try:
            dataJson = {}
            dataJson['revision_id'] = data["revision_id"]
            dataJson['tipo_inspeccion_id'] = data["tipo_inspeccion_id"]
            dataJson['observaciones'] = data["observaciones"]
            dataJson['estado'] = data["estado"]
            dataJson['persona_id'] = data["persona_id"]
            InspeccionInsert = Inspeccion.insert_data(dataJson)
            # return InspecciontInsert
            InspeccionId = InspeccionInsert['response']['data']['last_id']
            return {'success': True, 'mensaje': "Acción realizada con éxito.", 'data': InspeccionId}, 200
    
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # exc_type, fname, exc_tb.tb_lineno
            msj = 'Error: ' + str(exc_obj) + ' File: ' + \
                fname + ' linea: ' + str(exc_tb.tb_lineno)
            return {'success': False, 'mensaje': str(msj)}, 500

class InspeccionDelete(Resource):
    def delete(self, id):
        try:
            inspeccion_id = id
            if inspeccion_id is None:
                return {'success':False,'mensaje': 'Debe ingresar el inspeccion_id.', 'data':[]}, 404	
            InspeccionDelete = Inspeccion.delete_data(inspeccion_id)
            if InspeccionDelete:
                return {'success':True,'mensaje': "Acción realizada con éxito."}, 200
            else:
                return {'success':False,'mensaje': 'No se encontró el recurso solicitado', 'data':[]}, 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # exc_type, fname, exc_tb.tb_lineno
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'success':False,'mensaje': str(msj) }, 500