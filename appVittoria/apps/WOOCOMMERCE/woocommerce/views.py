from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from urllib.parse import urlparse

from .constantes import mapeoTodoMegaDescuento, mapeoMegaDescuento, mapeoMegaDescuentoSinEnvio, \
    mapeoTodoMegaDescuentoSinEnvio
from .serializers import (
    CreateOrderSerializer, PedidosSerializer,
)
from .models import (
    Pedidos
)
from ...MDM.mdm_clientes.models import Clientes
from ...MDM.mdm_clientes.serializers import ClientesUpdateSerializer

from ...MDP.mdp_productos.models import Productos

# Sumar Fechas
from datetime import datetime
from datetime import timedelta

from .utils import (
    enviarCorreoVendedor, enviarCorreoCliente, enviarCorreoClienteDespacho, enviarCorreoCourierDespacho,
    enviarCorreoVendedorDespacho, enviarCorreoClienteRechazado, enviarCorreoVendedorRechazado
)
from ...ADM.vittoria_usuarios.models import Usuarios
from ...ADM.vittoria_catalogo.models import Catalogo

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
@api_view(['POST'])
def orders_create(request):
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

            dominio_completo = request.headers.get('X-Wc-Webhook-Source')
            print('dominio_completo', dominio_completo)
            # Utiliza urlparse para obtener la información de la URL
            parsed_url = urlparse(dominio_completo)
            # Combina el nombre de host (dominio) y el esquema (protocolo)
            domain = parsed_url.netloc
            print('dominio del que llega', dominio_completo)
            dominio_permitidos = Catalogo.objects.filter(tipo='INTEGRACION_WOOCOMMERCE', valor=domain).first()
            if dominio_permitidos is None:
                error = f"Llego un dominio: {domain}"
                createLog(logModel, error, logTransaccion)
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            articulos = []

            for articulo in request.data['line_items']:
                articulos.append({
                    "codigo": articulo['sku'],
                    "articulo": articulo['name'],
                    "valorUnitario": articulo['price'],
                    "cantidad": articulo['quantity'],
                    "precio": articulo['total'],
                })

            canal = request.data['_links']['collection'][0]['href']
            codigoVendedor = next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm17'), None)
            nombreVendedor = next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm18'), None)

            if 'https://megadescuento.com' in canal:
                validarDatosEnvio = next((objeto['value'] for objeto in request.data['meta_data'] if
                                          objeto["key"] == '_shipping_wooccm13'), None)
                if '@' in validarDatosEnvio:
                    data = mapeoMegaDescuento(request, articulos)
                else:
                    data = mapeoMegaDescuentoSinEnvio(request, articulos)
            elif 'https://todomegacentro.megadescuento.com' in canal and codigoVendedor != '' and nombreVendedor != '':
                validarDatosEnvio = next((objeto['value'] for objeto in request.data['meta_data'] if
                                          objeto["key"] == '_shipping_wooccm13'), None)
                if '@' in validarDatosEnvio:
                    data = mapeoTodoMegaDescuento(request, articulos)
                else:
                    data = mapeoTodoMegaDescuentoSinEnvio(request, articulos)

            serializer = CreateOrderSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                enviarCorreoVendedor(data)
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
def orders_list(request):
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

            if 'estado' in request.data and request.data['estado'] != '':
                filters['estado__in'] = request.data['estado']

            if 'inicio' in request.data and request.data['inicio'] != '':
                filters['created_at__gte'] = str(request.data['inicio'])
            if 'fin' in request.data and request.data['fin'] != '':
                filters['created_at__lte'] = datetime.strptime(request.data['fin'], "%Y-%m-%d").date() + timedelta(
                    days=1)

            if 'codigoVendedor' in request.data and request.data['codigoVendedor'] != '':
                filters['codigoVendedor'] = request.data['codigoVendedor'].upper()

            if 'compania' in request.data and request.data['compania'] != '':
                vendedores = list(
                    Usuarios.objects.filter(compania=request.data['compania']).values_list('username', flat=True))
                filters['codigoVendedor__in'] = vendedores

            if 'canalEnvio' in request.data and request.data['canalEnvio'] != '':
                filters['canalEnvio'] = request.data['canalEnvio'].upper()

            # Serializar los datos
            query = Pedidos.objects.filter(**filters).order_by('-created_at')
            serializer = PedidosSerializer(query[offset:limit], many=True)
            new_serializer_data = {'cont': query.count(), 'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def orders_update(request, pk):
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
            query = Pedidos.objects.get(pk=pk, state=1)
        except Pedidos.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            if 'codigoConfirmacion' in request.data and '' != request.data['codigoConfirmacion']:
                if Pedidos.objects.filter(codigoConfirmacion=request.data['codigoConfirmacion']).exclude(pk=pk).first():
                    return Response(data='Ya existe el numero transacción', status=status.HTTP_404_NOT_FOUND)
            now = timezone.localtime(timezone.now())
            # request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            serializer = PedidosSerializer(query, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                if serializer.data['estado'] == 'Empacado':
                    enviarCorreoCliente(serializer.data)
                    for articulo in serializer.data['articulos']:
                        producto = Productos.objects.filter(codigoBarras=articulo['codigo'], state=1).first()
                        if producto:
                            producto.stock = producto.stock - int(articulo['cantidad'])
                            producto.save()
                if serializer.data['estado'] == 'Despachado':
                    enviarCorreoClienteDespacho(serializer.data)
                    enviarCorreoCourierDespacho(serializer.data)
                    enviarCorreoVendedorDespacho(serializer.data)
                    # Se crea el usuario cuando el pedido es despachado
                    cliente = {
                        'nombreCompleto': serializer.data['facturacion']['nombres'] + serializer.data['facturacion']['apellidos'],
                        'nombres': serializer.data['facturacion']['nombres'],
                        'apellidos': serializer.data['facturacion']['apellidos'],
                        'cedula': serializer.data['facturacion']['identificacion'],
                        'tipoIdentificacion': 'Cédula',
                        'correo': serializer.data['facturacion']['correo'],
                        'paisNacimiento': serializer.data['facturacion']['pais'],
                        'provinciaNacimiento': serializer.data['facturacion']['provincia'],
                        'ciudadNacimiento': serializer.data['facturacion']['ciudad'],
                    }

                    clienteExiste = Clientes.objects.filter(cedula=serializer.data['facturacion']['identificacion']).first()
                    if clienteExiste is None:
                        Clientes.objects.create(**cliente)
                    else:
                        clienteSerializer = ClientesUpdateSerializer(clienteExiste, data=cliente, partial=True)
                        if clienteSerializer.is_valid():
                            clienteSerializer.save()
                if serializer.data['estado'] == 'Rechazado':
                    enviarCorreoClienteRechazado(serializer.data)
                    enviarCorreoVendedorRechazado(serializer.data)
                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def orders_listOne(request, pk):
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
            query = Pedidos.objects.get(pk=pk, state=1)
        except Pedidos.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = PedidosSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def orders_devolucion(request, pk):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'devolucion/',
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
            query = Pedidos.objects.get(pk=pk, state=1)
        except Pedidos.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            if 'created_at' in request.data:
                request.data.pop('created_at')
            serializer = PedidosSerializer(query, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                for articulo in serializer.data['articulos']:
                    producto = Productos.objects.filter(codigoBarras=articulo['codigo'], state=1).first()
                    if producto:
                        producto.stock = producto.stock + int(articulo['cantidad'])
                        producto.save()
                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)