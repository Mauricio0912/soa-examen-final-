from flask import Blueprint, request, Response

from src.services.alumno_service import AlumnoService
from src.services.soap_handler import (
    parse_soap_request,
    create_soap_response,
    create_soap_fault,
    alumno_to_xml,
    alumnos_to_xml,
    string_response_to_xml
)
from src.services.wsdl import get_wsdl

soap_bp = Blueprint('soap', __name__)

SOAP_CONTENT_TYPE = 'text/xml; charset=utf-8'


@soap_bp.route('/', methods=['GET'])
def wsdl():
    if 'wsdl' in request.args:
        service_url = request.url_root.rstrip('/') + '/soap'
        return Response(get_wsdl(service_url), content_type=SOAP_CONTENT_TYPE)
    return Response('AlumnoService SOAP - Usa ?wsdl para ver el WSDL', content_type='text/plain')


@soap_bp.route('/', methods=['POST'])
def soap_endpoint():
    try:
        operation, params = parse_soap_request(request.data)
        service = AlumnoService()
        response_xml = dispatch_operation(service, operation, params)
        return Response(response_xml, content_type=SOAP_CONTENT_TYPE)
    except ValueError as e:
        return Response(
            create_soap_fault('Client', str(e)),
            content_type=SOAP_CONTENT_TYPE,
            status=400
        )
    except Exception as e:
        return Response(
            create_soap_fault('Server', f'Error interno: {str(e)}'),
            content_type=SOAP_CONTENT_TYPE,
            status=500
        )


def dispatch_operation(service: AlumnoService, operation: str, params: dict) -> str:
    handlers = {
        'CrearAlumno': handle_crear_alumno,
        'ObtenerAlumno': handle_obtener_alumno,
        'ObtenerPorMatricula': handle_obtener_por_matricula,
        'ListarAlumnos': handle_listar_alumnos,
        'ActualizarAlumno': handle_actualizar_alumno,
        'EliminarAlumno': handle_eliminar_alumno,
        'EliminarAlumnos': handle_eliminar_alumnos,
    }

    handler = handlers.get(operation)
    if not handler:
        raise ValueError(f'Operación no soportada: {operation}')

    return handler(service, params)


def handle_crear_alumno(service: AlumnoService, params: dict) -> str:
    nombre = params['nombre']
    result = service.crear_alumno(nombre)
    return create_soap_response(alumno_to_xml(result, 'CrearAlumnoResponse'))


def handle_obtener_alumno(service: AlumnoService, params: dict) -> str:
    id = int(params['id'])
    result = service.obtener_alumno(id)

    if result:
        return create_soap_response(alumno_to_xml(result, 'ObtenerAlumnoResponse'))
    raise ValueError(f'Alumno {id} no encontrado')


def handle_obtener_por_matricula(service: AlumnoService, params: dict) -> str:
    matricula = params['matricula']
    result = service.obtener_por_matricula(matricula)

    if result:
        return create_soap_response(alumno_to_xml(result, 'ObtenerPorMatriculaResponse'))
    raise ValueError(f'Alumno con matrícula {matricula} no encontrado')


def handle_listar_alumnos(service: AlumnoService, params: dict) -> str:
    result = service.listar_alumnos()
    return create_soap_response(alumnos_to_xml(result, 'ListarAlumnosResponse'))


def handle_actualizar_alumno(service: AlumnoService, params: dict) -> str:
    id = int(params['id'])
    nombre = params['nombre']
    result = service.actualizar_alumno(id, nombre)

    if result:
        return create_soap_response(alumno_to_xml(result, 'ActualizarAlumnoResponse'))
    raise ValueError(f'Alumno {id} no encontrado')


def handle_eliminar_alumno(service: AlumnoService, params: dict) -> str:
    id = int(params['id'])
    success = service.eliminar_alumno(id)

    if success:
        return create_soap_response(string_response_to_xml(f'Alumno {id} eliminado exitosamente', 'EliminarAlumnoResponse'))
    raise ValueError(f'Alumno {id} no encontrado')


def handle_eliminar_alumnos(service: AlumnoService, params: dict) -> str:
    ids = [int(id) for id in params['ids']]
    if len(ids) < 2:
        raise ValueError('Se requieren al menos 2 IDs para eliminar')
    count = service.eliminar_alumnos(ids)
    return create_soap_response(string_response_to_xml(f'{count} alumnos eliminados exitosamente', 'EliminarAlumnosResponse'))
