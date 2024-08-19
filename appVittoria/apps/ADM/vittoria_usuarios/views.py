from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from .models import Usuarios
from .serializers import UsuarioSerializer, UsuarioImagenSerializer, UsuarioRolSerializer, UsuarioCrearSerializer, \
    UsuarioFiltroSerializer, UsuarioResource
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import logout
from ..vittoria_autenticacion.models import Token
# contraeña
from django.utils.crypto import get_random_string
# logs
from ..vittoria_logs.methods import createLog, datosUsuarios, datosTipoLog
from django_rest_passwordreset.views import ResetPasswordRequestToken
# enviar email usuario creado
from ..vittoria_autenticacion.password_reset import resetPasswordNewUser

# declaracion variables log
datosAux = datosUsuarios()
datosTipoLogAux = datosTipoLog()
# asignacion datos modulo
logModulo = datosAux['modulo']
logApi = datosAux['api']
# asignacion tipo de datos
logTransaccion = datosTipoLogAux['transaccion']
logExcepcion = datosTipoLogAux['excepcion']


# USUARIO LISTAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def usuario_list(request):
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
    try:
        if request.method == 'POST':
            logModel['dataEnviada'] = str(request.data)
            if 'page_size' not in request.data or 'page' not in request.data:
                # error no existen los datos
                errorPaginacion = {'error': 'No existe el/los parámetros de páginacion'}
                createLog(logModel, errorPaginacion, logExcepcion)
                return Response(errorPaginacion, status=status.HTTP_400_BAD_REQUEST)
            # paginacion
            page_size = int(request.data['page_size'])
            page = int(request.data['page'])
            offset = page_size * page
            limit = offset + page_size
            # Filtros
            filters = {}
            if 'idRol' in request.data and request.data['idRol'] != 0:
                filters['idRol'] = request.data['idRol']
            if 'pais' in request.data and '' != request.data['pais']:
                filters['pais'] = request.data['pais']
            if 'provincia' in request.data and '' != request.data['provincia']:
                filters['provincia'] = request.data['provincia']
            if 'ciudad' in request.data and '' != request.data['ciudad']:
                filters['ciudad'] = request.data['ciudad']
            if 'estado' in request.data and request.data['estado'] != '':
                filters['estado'] = str(request.data['estado'])
            if 'state' in request.data and request.data['state'] != '':
                filters['state'] = str(request.data['state'])
            if 'email' in request.data and request.data['email'] != '':
                filters['email__icontains'] = str(request.data['email'])
            if 'compania' in request.data and request.data['compania'] != '':
                filters['compania'] = str(request.data['compania'])
            if 'tipoEnvio' in request.data and request.data['tipoEnvio'] != '':
                filters['tipoEnvio'] = str(request.data['tipoEnvio'])
            # toma de datos
            usuario = Usuarios.objects.filter(**filters).order_by('-created_at')
            serializerAllDta = UsuarioRolSerializer(usuario, many=True)
            serializer = UsuarioRolSerializer(usuario[offset:limit], many=True)
            new_serializer_data = {'cont': usuario.count(),
                                   'info': serializer.data,
                                   'usuarios': serializerAllDta.data
                                   }
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)
    # USUARIO LISTAR EXPORTAR


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def usuario_listExport(request):
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
    try:
        if request.method == 'POST':
            logModel['dataEnviada'] = str(request.data)
            # Filtros
            filters = {"state": "1"}
            if 'idRol' in request.data:
                if request.data['idRol'] != 0:
                    filters['idRol'] = int(request.data['idRol'])
            if 'estado' in request.data:
                if request.data['estado'] != '':
                    filters['estado'] = str(request.data['estado'])

            # toma de datos
            usuario = Usuarios.objects.filter(**filters).order_by('-created_at')
            serializer = UsuarioRolSerializer(usuario, many=True)
            new_serializer_data = {'cont': usuario.count(),
                                   'info': serializer.data}
            return Response(new_serializer_data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usuario_findOne(request, pk):
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
            logModel['dataEnviada'] = str(request.data)
            usuario = Usuarios.objects.get(pk=pk, state=1)
        except Usuarios.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            logModel['dataRecibida'] = str(errorNoExiste)
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(errorNoExiste, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = UsuarioSerializer(usuario)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def usuario_update(request, pk):
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
            logModel['dataEnviada'] = str(request.data)
            usuario = Usuarios.objects.get(pk=pk, state=1)
        except Usuarios.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')

            if 'username' in request.data and '' != request.data['username']:
                request.data['username'] = request.data['username'].upper()

            serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def usuario_delete(request, pk):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'delete/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'BORRAR',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    try:
        try:
            logModel['dataEnviada'] = str(request.data)
            usuario = Usuarios.objects.get(pk=pk, state=1)
        except Usuarios.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            serializer = UsuarioSerializer(usuario, data={'estado': request.data['estado'], 'state': '0',
                                                          'updated_at': str(now)}, partial=True)
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
    # CREAR USUARIO


@api_view(['POST'])
def usuario_create(request):
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

    try:
        if request.method == 'POST':
            user = Usuarios.objects.filter(email=request.data['email'], state=1,estado='Activo').first()
            if user is not None:
                data = {'error': 'Email ya existe.'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            request.data['created_at'] = str(timezone_now)
            if 'updated_at' in request.data:
                request.data.pop('updated_at')
            logModel['dataEnviada'] = str(request.data)
            # AGREGA CONTRASEÑA
            request.data['password'] = get_random_string(length=32)
            if 'username' in request.data and '' != request.data['username']:
                request.data['username'] = request.data['username'].upper()
            serializer = UsuarioCrearSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                account = serializer.save()
                data['response'] = 'Usuario creado correctamente'
                data['email'] = account.email
                data['username'] = account.username
                token = Token.objects.get(user=account).key
                data['token'] = token
                createLog(logModel, data, logTransaccion)
                data['tokenEmail'] = str(resetPasswordNewUser(data['email']))
            else:
                data = serializer.errors
                createLog(logModel, data, logExcepcion)
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            return Response(data)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def usuarioImagen_update(request, pk):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'update/imagen/',
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
            logModel['dataEnviada'] = str(request.data)
            usuario = Usuarios.objects.get(pk=pk, state=1)
        except Usuarios.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            serializer = UsuarioImagenSerializer(usuario, data=request.data, partial=True)
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

    # toma los vendedores


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendedor_list(request):
    if request.method == 'GET':
        try:
            query = Usuarios.objects.filter(state=1, idRol__nombre="Vendedor")
            serializer = UsuarioFiltroSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

        # toma los usuarios


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def usuarios_list_rol(request):
    if request.method == 'POST':
        try:
            query = Usuarios.objects.filter(state=1, idRol__nombre=request.data['rol'])
            serializer = UsuarioFiltroSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usuarios_exportar(request):
    """
    Este metodo realiza una exportacion de todos los catalogos en excel de la tabla catalogo, de la base de datos central
    @rtype: DEvuelve un archivo excel
    """
    person_resource = UsuarioResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.xls, content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename="foo.xls"'
    return response
