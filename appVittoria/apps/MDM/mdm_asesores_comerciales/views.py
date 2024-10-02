from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import AsesoreSerializer, MovimientosAsesoresSerializer
from rest_framework.permissions import IsAuthenticated
from .utils import enviarCorreoUsuario
from ...ADM.vittoria_usuarios.serializers import UsuarioCrearSerializer
from django.utils import timezone
from .models import AsesoresComerciales
from ...ADM.vittoria_usuarios.models import Usuarios
from .models import MovimientosAsesores
from ...ADM.vittoria_roles.models import Roles
import random
import string
# logs
from ...ADM.vittoria_logs.methods import createLog, datosTipoLog, datosAsesores

# declaracion variables log
datosAux = datosAsesores()
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
def asesor_list(request):
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

            # paginacion
            page_size = int(request.data['page_size'])
            page = int(request.data['page'])
            offset = page_size * page
            limit = offset + page_size
            # Filtros
            filters = {}

            if 'estado' in request.data and request.data['estado'] != '':
                filters['estado__in'] = request.data['estado']

            if 'state' in request.data and request.data['state'] != '':
                filters['state'] = str(request.data['state'])

            print(filters)

            # toma de datos
            asesor = AsesoresComerciales.objects.filter(**filters).order_by('-created_at')
            serializerAllDta = AsesoreSerializer(asesor, many=True)
            serializer = AsesoreSerializer(asesor[offset:limit], many=True)
            new_serializer_data = {'cont': asesor.count(),
                                   'info': serializer.data,
                                   'asesores': serializerAllDta.data
                                   }
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)
    # USUARIO LISTAR EXPORTAR


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def asesor_findOne(request, pk):
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
            asesor = AsesoresComerciales.objects.get(pk=pk, state=1)
        except AsesoresComerciales.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            logModel['dataRecibida'] = str(errorNoExiste)
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(errorNoExiste, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = AsesoreSerializer(asesor)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def asesor_update_state(request, pk):
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
            asesor = AsesoresComerciales.objects.get(pk=pk, state=1)
        except AsesoresComerciales.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')

            serializer = AsesoreSerializer(asesor, data=request.data, partial=True)
            if serializer.is_valid():
                asesor = serializer.save()
                user = Usuarios.objects.filter(email=asesor.email, state=1).first()
                if user is not None:
                    data = {'error': 'Usuario ya existe.'}
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                password = generate_pass()
                rol = Roles.objects.filter(id=63, state=1).first()
                serializerUser = {
                        'username':format_username(asesor.nombres, asesor.apellidos),
                        'imagen':'',
                        'nombres': asesor.nombres,
                        'canal':'megabahia.megadescuento.com',
                        'apellidos': asesor.apellidos,
                        'email': asesor.email,
                        'estado': asesor.estado,
                        'idRol':rol,
                        'pais': asesor.pais,
                        'provincia': asesor.provincia,
                        'ciudad': asesor.ciudad,
                        'tipoEnvio':'',
                        'telefono':asesor.whatsapp,
                        'whatsapp':asesor.whatsapp,
                        'compania':'',
                        'twitter':'',
                        'facebook':'',
                        'instagram':'',
                        'state':1,
                    }

                newUser = Usuarios.objects.create(**serializerUser)
                newUser.set_password(password)
                newUser.save()

                asesor.usuario = newUser.id
                asesor.save()

                enviarCorreoUsuario(newUser, password)

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
def asesor_update(request, pk):
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
            logModel['dataEnviada'] = str(request.data)
            asesor = AsesoresComerciales.objects.get(pk=pk)
        except AsesoresComerciales.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')

            serializer = AsesoreSerializer(asesor, data=request.data, partial=True)
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
def activate_asesor(request, pk):
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
            asesor = AsesoresComerciales.objects.get(pk=pk)
        except AsesoresComerciales.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')

            serializer = AsesoreSerializer(asesor, data=request.data, partial=True)
            if serializer.is_valid():
                asesor = serializer.save()
                user = Usuarios.objects.filter(email=asesor.email).first()
                if user is None:
                    data = {'error': 'Usuario no existe.'}
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

                user.estado = asesor.estado
                user.state = asesor.state
                user.save()

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
def asesor_delete(request, pk):
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
            asesor = AsesoresComerciales.objects.get(pk=pk, state=1)
        except AsesoresComerciales.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            serializer = AsesoreSerializer(asesor, data={'estado': request.data['estado'], 'state': '0',
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
def asesor_create(request):
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
            asesor = AsesoresComerciales.objects.filter(email=request.data['email']).first()
            if asesor is not None:
                data = {'error': 'Email ya existe.'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            request.data['created_at'] = str(timezone_now)
            if 'updated_at' in request.data:
                request.data.pop('updated_at')
            logModel['dataEnviada'] = str(request.data)

            serializer = AsesoreSerializer(data=request.data)
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


#MOVIMIENTOS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movimiento_create(request):
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
            request.data['created_at'] = str(timezone_now)

            logModel['dataEnviada'] = str(request.data)

            asesor = AsesoresComerciales.objects.filter(id = request.data['asesor']).first()

            if asesor is None:
                errorNoExiste = {'error': 'No existe asesor'}
                createLog(logModel, errorNoExiste, logExcepcion)
                return Response(status=status.HTTP_404_NOT_FOUND)

            request.data['asesor'] = asesor.id
            request.data['saldo_ingreso'] = float(request.data['saldo_ingreso'])

            if 'Carga de saldo' in request.data['tipo_movimiento'] or 'Saldo incial' in request.data['tipo_movimiento']:
                movimientoAsesor = MovimientosAsesores.objects.filter(asesor=request.data['asesor']).order_by('-created_at').first()
                request.data['saldo_total'] = round(float(movimientoAsesor.saldo_total)+float(request.data['saldo_ingreso']),2)
                request.data['saldo_egreso'] = 0

            serializer = MovimientosAsesoresSerializer(data=request.data)

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movimiento_asesor_list(request):
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

            # paginacion
            page_size = int(request.data['page_size'])
            page = int(request.data['page'])
            offset = page_size * page
            limit = offset + page_size
            # Filtros
            filters = {"state": "1"}

            if 'asesor' in request.data and request.data['asesor'] != '':
                filters['asesor'] = request.data['asesor']

            # toma de datos
            movimientos_asesor = MovimientosAsesores.objects.filter(**filters).order_by('-created_at')
            serializer = MovimientosAsesoresSerializer(movimientos_asesor[offset:limit], many=True)
            allSerializer = MovimientosAsesoresSerializer(movimientos_asesor, many=True)

            new_serializer_data = {'cont': movimientos_asesor.count(),
                                   'allData': allSerializer.data,
                                   'info': serializer.data,
                                   }
            return Response(new_serializer_data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movimiento_asesor_update(request, pk):
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
            logModel['dataEnviada'] = str(request.data)
            movimiento_asesor = MovimientosAsesores.objects.get(pk=pk)
        except AsesoresComerciales.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            if 'created_at' in request.data:
                request.data.pop('created_at')

            serializer = MovimientosAsesoresSerializer(movimiento_asesor, data=request.data, partial=True)
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



def generate_pass():
    caracteres = string.ascii_letters + string.digits
    contraseña = ''.join(random.choice(caracteres) for i in range(8))

    return contraseña

def format_username(name, lastName):
    initial_name = name[0].upper()
    lastName_mayus = lastName.upper()

    return f"{initial_name}.{lastName_mayus}"