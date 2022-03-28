import datetime
import simplejson as json
import jsonschema
import re
from jsonschema import validate

class Utilidades():

    @staticmethod
    def mayusculas(texto):
        try:
            return str(texto).upper()
        except Exception as e:
            return texto

    @staticmethod
    def formatoFecha(fecha):
    	dia = str(fecha.day)
    	dia = "0"+dia if len(dia) == 1 else dia
    	mes = str(fecha.month)
    	mes = "0"+mes if len(mes) == 1 else mes
    	anio = str(fecha.year)

    	fechaFormateada =  dia + "-" + mes + "-" + anio
    	return fechaFormateada

    @staticmethod
    def formatoFechaHora(fecha):
        return str(fecha.strftime("%d-%m-%Y %H:%M")) 

    """
        Valida fecha en formato dd-mm-YYYY
    """
    @staticmethod
    def validarDate(date_text, formato):
        try:
            if str(date_text) != datetime.datetime.strptime(str(date_text), formato).strftime(formato):
                raise ValueError
            return True
        except ValueError:
            return False

    @staticmethod
    def obtener_datos(query):
        jsonData = []
        if query:
            """
            Esta funcion sirve solo cuando la query es de tipo sql 1 model list  o sql model(first)
            """
            if isinstance(query, list):
                for datos in query:
                    d = {}
                    for column in datos.__table__.columns:
                        data = getattr(datos, column.name)
                        if isinstance(data, bytes):
                            Bi = binascii.hexlify(data)
                            Bi = str(Bi.decode('ascii'))
                            data = Bi
                        if isinstance(data, datetime.datetime):
                            data = Utilidades.formatoFechaHora(data)

                        if isinstance(data, datetime.date):
                            data = Utilidades.formatoFecha(data)

                        d[column.name] = data
                    jsonData.append(d)
            else:
                d = {}
                for column in query.__table__.columns:
                    data = getattr(query, column.name)
                    if isinstance(data, bytes):
                        Bi = binascii.hexlify(data)
                        Bi = str(Bi.decode('ascii'))
                        data = Bi
                    if isinstance(data, datetime.datetime):
                        data = Utilidades.formatoFechaHora(data)
                    if isinstance(data, datetime.date):
                            data = Utilidades.formatoFecha(data)
                    d[column.name] = data
                jsonData.append(d)
        return  json.loads(json.dumps(jsonData))

    @staticmethod
    def obtener_datos_collection(query):
        """
            Esta funcion sirve solo cuando la query es de tipo select all()
        """
        first = False
        name_first_table = ""
        json_primary = {}
        primary_key = None
        foreign_key = None
        if query:
            for tablas in query:
                for datos in tablas:
                    if datos:
                        tabla_actual = str(datos.__table__)
                        if not first:
                            name_first_table = tabla_actual
                            first = True

                        col = {}
                        for column in datos.__table__.columns:
                            data = getattr(datos, column.name)

                            if isinstance(data, bytes):
                                Bi = binascii.hexlify(data)
                                Bi = str(Bi.decode('ascii'))
                                data = Bi
                                #data = data.decode("ISO-8859-1")
                            if isinstance(data, datetime.datetime):
                                data = Utilidades.formatoFechaHora(data)
                                
                            if isinstance(data, datetime.date):
                                data = Utilidades.formatoFecha(data)
                            col[column.name] = data

                        if name_first_table == tabla_actual:
                            primary_key = int(getattr(datos, "id"))
                            if not primary_key in json_primary:
                                
                                json_primary[primary_key] = {}
                                json_primary[primary_key] = col
                        else:
                            foreign_key = int(getattr(datos, "id"))
                            if not tabla_actual in json_primary[primary_key]:
                                json_primary[primary_key][tabla_actual] = {}
                                if not foreign_key in json_primary[primary_key][tabla_actual]:
                                    json_primary[primary_key][tabla_actual][foreign_key] = {}
                                    json_primary[primary_key][tabla_actual][foreign_key] = col
                                else:
                                    json_primary[primary_key][tabla_actual][foreign_key] = col
                            else:
                                if not foreign_key in json_primary[primary_key][tabla_actual]:
                                    json_primary[primary_key][tabla_actual][foreign_key] = {}
                                    json_primary[primary_key][tabla_actual][foreign_key] = col
                                else:
                                    json_primary[primary_key][tabla_actual][foreign_key] = col
        return  json_primary
 
    @staticmethod
    #valida la data con un schema json
    def validateJson(jsonData, jsonSchema):
        try:
            validate(jsonData, jsonSchema)
        except jsonschema.exceptions.ValidationError as err:
            return {"path":(err.schema_path[1]), "message": err.message}
        return True

    
    @staticmethod
    def getRefSex(id_sexo):
        if id_sexo == "1" or id_sexo.upper() == 'M':
            return 1
        if id_sexo == "2" or id_sexo.upper() == 'F':
            return 2
        return 3

    @staticmethod
    def getCodEstructuraPais(id_pais):
        naciones = {1:'chile',2:'colombia',3:'peru',4:'mexico'}    
        file = open('snd_backend/aplicacion/schemas/estructura/'+naciones[id_pais]+'.json',)    
        estructura = json.loads(file.read())
        dicEstruct = {}
        for nivel in estructura:
            if int(nivel['NivelEstructura']) == 1:
                dicEstruct['tipo_ensenanza'] = int(nivel['RefOrganizationTypeId'])
            elif int(nivel['NivelEstructura']) == 2:
                dicEstruct['grado'] = int(nivel['RefOrganizationTypeId'])
            elif int(nivel['NivelEstructura']) == 3:
                dicEstruct['curso'] = int(nivel['RefOrganizationTypeId'])
            elif int(nivel['NivelEstructura']) == 4:    
                dicEstruct['material'] = int(nivel['RefOrganizationTypeId'])  
        
        return dicEstruct     

    @staticmethod
    def es_correo_valido(correo):
        """   
            Usar expresiones regulares para ver si es un correo electrónico válido en Python
            Recuerda importar el módulo re
            Por cierto, está probado con Python 3, si usas la versión 2 y no funciona, no trates
            de adaptarlo, mejor actualiza tu versión
            @author parzibyte
        """
        expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        return re.match(expresion_regular, correo) is not None