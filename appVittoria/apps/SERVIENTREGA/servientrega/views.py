from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime
import requests
from ...config.config import SERVIENTREGA_USER, SERVIENTREGA_PASSWORD, SERVIENTREGA_URL, SERVIENTREGA_URL_GENERACION
# logs
from ...ADM.vittoria_logs.methods import createLog, datosTipoLog, datosProductosMDP

# declaracion variables log
datosAux = datosProductosMDP()
datosTipoLogAux = datosTipoLog()
# asignacion datos modulo
logModulo = datosAux['modulo']
logApi = datosAux['api']
# asignacion tipo de datos
logTransaccion = datosTipoLogAux['transaccion']
logExcepcion = datosTipoLogAux['excepcion']


# CRUD PRODUCTOS
# LISTAR TODOS
@api_view(['GET'])
def productos_list_ciudades(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'LEER',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    if request.method == 'GET':
        try:
            logModel['dataEnviada'] = str(request.data)
            # Serializar los datos
            resp = requests.get(
                f"""{SERVIENTREGA_URL}/api/ciudades/['{SERVIENTREGA_USER}','{SERVIENTREGA_PASSWORD}']""", verify=False)
            # envio de datos
            return Response(resp.json(), status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def productos_list_guiawebs(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'LEER',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    if request.method == 'POST':
        try:
            logModel['dataEnviada'] = str(request.data)
            request.data['login_creacion'] = SERVIENTREGA_USER
            request.data['password'] = SERVIENTREGA_PASSWORD
            # Serializar los datos
            resp = requests.post(f"""{SERVIENTREGA_URL}/api/guiawebs/""", json=request.data, verify=False)
            # envio de datos
            return Response(resp.json(), status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def productos_list_GuiaRetornoNacional(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'LEER',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    if request.method == 'POST':
        try:
            logModel['dataEnviada'] = str(request.data)
            request.data['login_creacion'] = SERVIENTREGA_USER
            request.data['password'] = SERVIENTREGA_PASSWORD
            # Serializar los datos
            resp = requests.post(f"""{SERVIENTREGA_URL}/api/GuiaRetornoNacional/""", json=request.data, verify=False)
            # envio de datos
            return Response(resp.json(), status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def productos_list_GuiaRecaudo(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'LEER',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    if request.method == 'POST':
        try:
            logModel['dataEnviada'] = str(request.data)
            request.data['login_creacion'] = SERVIENTREGA_USER
            request.data['password'] = SERVIENTREGA_PASSWORD
            # Serializar los datos
            resp = requests.post(f"""{SERVIENTREGA_URL}/api/GuiaRecaudo""", json=request.data, verify=False)
            # envio de datos
            return Response(resp.json(), status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def productos_list_GuiasWeb(request, pk):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'LEER',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    if request.method == 'GET':
        try:
            logModel['dataEnviada'] = str(request.data)
            # Serializar los datos
            resp = requests.get(
                f"""{SERVIENTREGA_URL_GENERACION}/api/GuiasWeb/['{pk}','{SERVIENTREGA_USER}','{SERVIENTREGA_PASSWORD}','1']""",
                verify=False)
            # envio de datos
            return Response(resp.json(), status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def productos_list_GuiaDigital(request, pk):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'LEER',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    if request.method == 'GET':
        try:
            logModel['dataEnviada'] = str(request.data)
            # Serializar los datos
            resp = requests.get(
                f"""{SERVIENTREGA_URL_GENERACION}/api/GuiaDigital/['{pk}','{SERVIENTREGA_USER}','{SERVIENTREGA_PASSWORD}']""",
                verify=False)
            # envio de datos
            return Response(resp.json(), status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def productos_list_ImprimeSticker(request, pk):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'LEER',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    if request.method == 'GET':
        try:
            logModel['dataEnviada'] = str(request.data)
            # Serializar los datos
            resp = requests.get(
                f"""{SERVIENTREGA_URL_GENERACION}/api/ImprimeSticker/['{pk}','{SERVIENTREGA_USER}','{SERVIENTREGA_PASSWORD}']""",
                verify=False)
            # envio de datos
            return Response(resp.json(), status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def productos_list_Manifiestos(request, date):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'LEER',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    if request.method == 'GET':
        try:
            logModel['dataEnviada'] = str(request.data)
            # Serializar los datos
            resp = requests.get(
                f"""{SERVIENTREGA_URL_GENERACION}/api/Manifiestos/['{date}','{SERVIENTREGA_USER}','{SERVIENTREGA_PASSWORD}', 'T']""",
                verify=False)
            # envio de datos
            return Response(resp.json(), status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def productos_list_ImprimeRotulos(request, pk):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'LEER',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    if request.method == 'GET':
        try:
            logModel['dataEnviada'] = str(request.data)
            # Serializar los datos
            resp = requests.get(
                f"""{SERVIENTREGA_URL_GENERACION}/api/ImprimeRotulos/['{pk}','{SERVIENTREGA_USER}','{SERVIENTREGA_PASSWORD}']""",
                verify=False)
            # envio de datos
            return Response(resp.json(), status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
