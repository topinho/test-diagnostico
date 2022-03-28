# Test Diagnostico.

German Torres.

1. Guardar Revision.

http://localhost:5050/revisiones/save

post 

body -> raw

{
    "vehiculo": {
        "marca": "Ford",
        "modelo": "Fiesta",
        "patente": "QWE-534",
        "anio": 2019,
        "persona": {
            "identificacion": "XXXXXXX",
            "nombre": "Dueño",
            "apellido": "Vehiculo"
        }
    },
    "revision": {
        "aprobado": false,
        "observaciones": "Ninguna",
        "fecha_revision": "2022-02-12",
        "persona": {
            "identificacion": "YYYYYYY",
            "nombre": "Encargado",
            "apellido": "Servicio"
        }
    }
}

2. http://localhost:5050/inspecciones/save

post 

body -> raw

{
    "revision_id": N,
    "tipo_inspeccion_id": 3, (1,2,3)
    "observaciones": "Ninguna",
    "estado": "Pendiente",
    "persona_id": 2
}

3. http://localhost:5050/inspecciones/delete/8

delete

Id de inspeccion a eliminar

4. http://localhost:5050/revisiones/por-patente/AAA-198

Patente a buscar.