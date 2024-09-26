# Create your views here.
from .models import GdParametrizaciones
from .serializers import (
    GdParametrizacionesSerializer,
    GdParametrizacionesHijoSerializer,
    GdParametrizacionesListaSerializer,
    GdParametrizacionesFiltroSerializer,
    GdParametrizacionesTipoSerializer,
    GdParametrizacionesResource,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.http import HttpResponse
# logs
from ...ADM.vittoria_logs.methods import createLog, datosParametrizacionesMDO, datosTipoLog

# declaracion variables log
datosAux = datosParametrizacionesMDO()
datosTipoLogAux = datosTipoLog()
# asignacion datos modulo
logModulo = datosAux['modulo']
logApi = datosAux['api']
# asignacion tipo de datos
logTransaccion = datosTipoLogAux['transaccion']
logExcepcion = datosTipoLogAux['excepcion']


# CRUD GdParametrizaciones
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gd_parametrizaciones_list(request):
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
            # paginacion
            page_size = int(request.data['page_size'])
            page = int(request.data['page'])
            offset = page_size * page
            limit = offset + page_size
            # Filtros
            filters = {"state": "1"}
            if 'nombre' in request.data:
                if request.data['nombre'] != '':
                    filters['nombre__startswith'] = str(request.data['nombre'])
            if 'tipo' in request.data:
                if request.data['tipo'] != '':
                    filters['tipo'] = str(request.data['tipo'])

            # Serializar los datos
            query = GdParametrizaciones.objects.filter(**filters).order_by('-created_at')
            serializer = GdParametrizacionesListaSerializer(query[offset:limit], many=True)
            serializerAllData = GdParametrizacionesListaSerializer(query, many=True)

            new_serializer_data = {'cont': query.count(),
                                   'data': serializerAllData.data,
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

        # CREAR


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gd_parametrizaciones_create(request):
    request.POST._mutable = True
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'create/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'CREAR',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    if request.method == 'POST':
        try:
            logModel['dataEnviada'] = str(request.data)
            request.data['created_at'] = str(timezone_now)
            if 'updated_at' in request.data:
                request.data.pop('updated_at')

            serializer = GdParametrizacionesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        # ENCONTRAR UNO


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gd_parametrizaciones_findOne(request, pk):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'listOne/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'LEER',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    try:
        try:
            query = GdParametrizaciones.objects.get(pk=pk, state=1)
        except GdParametrizaciones.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = GdParametrizacionesSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

    # ACTUALIZAR


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gd_parametrizaciones_update(request, pk):
    request.POST._mutable = True
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'update/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'ESCRIBIR',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    try:
        try:
            query = GdParametrizaciones.objects.get(pk=pk, state=1)
        except GdParametrizaciones.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'POST':
            logModel['dataEnviada'] = str(request.data)
            request.data['updated_at'] = str(timezone_now)
            if 'created_at' in request.data:
                request.data.pop('created_at')

            serializer = GdParametrizacionesSerializer(query, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

    # ELIMINAR


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def gd_parametrizaciones_delete(request, pk):
    nowDate = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'delete/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'BORRAR',
        'fechaInicio': str(nowDate),
        'dataEnviada': '{}',
        'fechaFin': str(nowDate),
        'dataRecibida': '{}'
    }
    try:
        try:
            query = GdParametrizaciones.objects.get(pk=pk, state=1)
        except GdParametrizaciones.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'DELETE':
            serializer = GdParametrizacionesSerializer(query, data={'state': '0', 'updated_at': str(nowDate)},
                                                     partial=True)
            if serializer.is_valid():
                serializer.save()
                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data, status=status.HTTP_200_OK)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)
    # GET ESTADOS

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gd_valor_list(request):
    if request.method == 'POST':
        try:
            print('REQUEST: ',request)
            query = GdParametrizaciones.objects.filter(state=1, valor=request.data['valor'])
            serializer = GdParametrizacionesFiltroSerializer(query, many=True)
            return Response(serializer.data)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gd_estado_list(request):
    if request.method == 'GET':
        try:
            query = GdParametrizaciones.objects.filter(state=1, tipo="ESTADO")
            serializer = GdParametrizacionesFiltroSerializer(query, many=True)
            return Response(serializer.data)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

        # GET TIPO DE PARAMETRIZACIONES/CATÁLOGO


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gd_tipo_list(request):
    if request.method == 'GET':
        try:
            query = GdParametrizaciones.objects.filter(state=1).values('tipo').distinct()
            serializer = GdParametrizacionesTipoSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

        # GET TIPO DE PARAMETRIZACIONES/CATÁLOGO


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gd_parametrizaciones_list_hijos(request):
    if request.method == 'POST':
        try:
            query = GdParametrizaciones.objects.filter(state=1, tipo=str(request.data['tipo']))
            serializer = GdParametrizacionesHijoSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

        # TODAS LAS PARAMETRIZACIONES DE ACUERDO AL TIPO


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gd_parametrosTipo_list(request):
    if request.method == 'POST':
        try:
            query = GdParametrizaciones.objects.filter(state=1, tipo=request.data['tipo'])
            serializer = GdParametrizacionesFiltroSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

        # POST FILTRO Y NOMBRE


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gd_parametrizaciones_filter_name(request):
    if request.method == 'POST':
        try:
            query = GdParametrizaciones.objects.filter(state=1, nombre=request.data['nombre'],
                                                     tipo=request.data['tipo'])
            serializer = GdParametrizacionesHijoSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


# POST FILTRO Y NOMBRE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gd_parametrizaciones_filter_listOne_name_tipo(request):
    if request.method == 'POST':
        try:
            query = GdParametrizaciones.objects.get(state=1, nombre=request.data['nombre'], tipo=request.data['tipo'])
            serializer = GdParametrizacionesSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gd_parametrizaciones_exportar(request):
    """
    Este metodo realiza una exportacion de todos los catalogos en excel de la tabla catalogo, de la base de datos central
    @rtype: DEvuelve un archivo excel
    """
    person_resource = GdParametrizacionesResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.xls, content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename="foo.xls"'
    return response
