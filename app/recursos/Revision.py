import json, os
from flask import Flask, request, jsonify, Response
from flask_restful import Resource, reqparse

from app.modelos.Revision import Revision
from app.modelos.Persona import Persona
from app.modelos.Vehiculo import Vehiculo

from datetime import datetime

class Revisiones(Resource):
    def get(self):
        ret = []
        res = Revision.query.join(Vehiculo, Revision.vehiculo_id == Vehiculo.id).all()
        if res:
            for r in res:
                ret.append(
                    {
                        #'fecha_revision': r.fecha_revision,
                        'observaciones': r.observaciones,
                        'vehiculo_id': r.vehiculo_id,
                        'patente': r.patente
                    }
                )
        return ret, 200

class RevisionesPorPatente(Resource):
    def get(self, patente):
        #data = self.parser.parse_args()
        try:
            #patente = data["patente"]
            patente = patente
            revisiones = Revision.get_data_by_patente(patente)
            if revisiones:
                return {'success':True,'mensaje': "Acción realizada con éxito.", 'data': revisiones}, 200
            return {'success':False,'mensaje': 'No se encontró el recurso solicitado', 'data':[]}, 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # exc_type, fname, exc_tb.tb_lineno
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'success':False,'mensaje': str(msj) }, 500

class RevisionSave(Resource):
    def post(self):
        data = request.get_json()
        #return {"data": data}, 200
        if data is None:
            return {"success": False, "message": "Faltan datos del json"}, 401

        try:
            if 'revision' not in data:
                return {"success": False, "message": "Faltan datos de revision del json"}, 401
            else:
                dataRevision = data["revision"]
                if 'fecha_revision' not in dataRevision:
                    return {"success": False, "message": "Falta la fecha de revision"}, 401
                if 'observaciones' not in dataRevision:
                    return {"success": False, "message": "Falta la observaciones"}, 401
                if 'vehiculo_id' not in dataRevision:
                    if 'vehiculo' not in data:
                        return {"success": False, "message": "Falta datos de vehiculo a ingresar"}, 401
                    else:
                        #check si existe patente
                        dataVehiculo = data["vehiculo"]
                        patente = dataVehiculo['patente']
                        VehiculoByPantente = Vehiculo.get_data_by_patente(patente)
                        if VehiculoByPantente is not None:
                            vehiculo_id = VehiculoByPantente[0]['id']
                        else:
                            if 'persona_id' not in dataVehiculo:
                                if 'persona' not in dataVehiculo:
                                    return {"success": False, "message": "Falta datos del propietario del vehiculo a ingresar"}, 401
                                else:
                                    #check si existe persona propietaria del vehiculo
                                    dataPropietario = dataVehiculo['persona']
                                    PropietarioIdentificacion = dataPropietario['identificacion']
                                    Propietario =  Persona.get_data_by_identificacion(PropietarioIdentificacion)
                                    if Propietario is not None:
                                        propietario_id = Propietario[0]['id']
                                    else:
                                        dataJsonPropietario = {}
                                        dataJsonPropietario['identificacion'] = dataPropietario["identificacion"]
                                        dataJsonPropietario['nombre'] = dataPropietario["nombre"]
                                        dataJsonPropietario['apellido'] = dataPropietario["apellido"]
                                        PropietarioInsert = Persona.insert_data(dataJsonPropietario)
                                        if PropietarioInsert is not None:
                                            propietario_id = PropietarioInsert['response']['data']['last_id']
                                        else:
                                            return {"success": False, "message": "No se pudo ingresar el propietario"}, 401
                            else:
                                propietario_id = dataVehiculo['persona_id']
                            
                            if propietario_id is not None:
                                dataJsonVehiculo = {}
                                dataJsonVehiculo['marca'] = dataVehiculo['marca']
                                dataJsonVehiculo['modelo'] = dataVehiculo['modelo']
                                dataJsonVehiculo['patente'] = dataVehiculo['patente']
                                dataJsonVehiculo['anio'] = dataVehiculo['anio']
                                dataJsonVehiculo['persona_id'] = propietario_id
                                VehiculoInsert = Vehiculo.insert_data(dataJsonVehiculo)
                                if VehiculoInsert is not None:
                                    vehiculo_id = VehiculoInsert['response']['data']['last_id']
                                else:
                                    return {"success": False, "message": "No se pudo ingresar el vehiculo"}, 401

                else:
                    vehiculo_id = dataRevision['vehiculo_id']
                if vehiculo_id is not None:
                    if 'persona_id' not in dataRevision:
                        if 'persona' not in dataRevision:
                            return {"success": False, "message": "Falta datos del encargado del vehiculo a ingresar"}, 401
                        else:
                            #check si existe persona propietaria del vehiculo
                            dataEncargado = dataRevision['persona']
                            EncargadoIdentificacion = dataEncargado['identificacion']
                            Encargado =  Persona.get_data_by_identificacion(EncargadoIdentificacion)
                            if Encargado is not None:
                                encargado_id = Encargado[0]['id']
                            else:
                                dataJsonEncargado = {}
                                dataJsonEncargado['identificacion'] = dataEncargado["identificacion"]
                                dataJsonEncargado['nombre'] = dataEncargado["nombre"]
                                dataJsonEncargado['apellido'] = dataEncargado["apellido"]
                                EncargadoInsert = Persona.insert_data(dataJsonEncargado)
                                if EncargadoInsert is not None:
                                    encargado_id = EncargadoInsert['response']['data']['last_id']
                                else:
                                    return {"success": False, "message": "No se pudo ingresar el encargado"}, 401
                    else:
                        encargado_id = dataRevision['persona_id']
                    
                    if encargado_id is not None:
                        dataJsonRevision = {}
                        dataJsonRevision['vehiculo_id'] = vehiculo_id
                        dataJsonRevision['fecha_revision'] = datetime.now().strftime('%Y-%m-%d')
                        dataJsonRevision['observaciones'] = dataRevision['observaciones']
                        dataJsonRevision['persona_id'] = encargado_id
                        RevisionInsert = Revision.insert_data(dataJsonRevision)

                        if RevisionInsert is not None:
                            revision_id = RevisionInsert['response']['data']['last_id']
                            return {'success': True, 'mensaje': "Acción realizada con éxito.", 'data': revision_id}, 200
                        else:
                            return {"success": False, "message": "No se pudo ingresar el encargado"}, 401
                    else:
                        return {"success": False, "message": "Falta encargado_id"}, 401
                else:
                    return {"success": False, "message": "Falta vehiculo_id"}, 401
    
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # exc_type, fname, exc_tb.tb_lineno
            msj = 'Error: ' + str(exc_obj) + ' File: ' + \
                fname + ' linea: ' + str(exc_tb.tb_lineno)
            return {'success': False, 'mensaje': str(msj)}, 500