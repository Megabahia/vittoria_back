
from rest_framework import status

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import Productos
from ...MDP.mdp_productos.models import Productos as ProductosPrincipales
from .serializers import ProductosSerializer
# logs
from ...ADM.vittoria_logs.methods import createLog, datosTipoLog, datosProductosMDP
from datetime import datetime
from datetime import timedelta
# declaracion variables log
datosAux = datosProductosMDP()
datosTipoLogAux = datosTipoLog()
# asignacion datos modulo
logModulo = datosAux['modulo']
logApi = datosAux['api']
# asignacion tipo de datos
logTransaccion = datosTipoLogAux['transaccion']
logExcepcion = datosTipoLogAux['excepcion']

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mdrp_productos_list(request):
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

            if 'codigoBarras' in request.data and request.data['codigoBarras'] != '':
                codigo_barras_sin_espacios = request.data['codigoBarras'].strip()
                filters['codigo_barras__icontains'] = codigo_barras_sin_espacios

            if 'inicio' in request.data and request.data['inicio'] != '':
                filters['created_at__gte'] = str(request.data['inicio'])
            if 'fin' in request.data and request.data['fin'] != '':
                filters['created_at__lte'] = datetime.strptime(request.data['fin'], "%Y-%m-%d").date() + timedelta(
                    days=1)

            query = Productos.objects.filter(**filters).order_by('-created_at')

            serializer = ProductosSerializer(query[offset:limit], many=True)
            new_serializer_data = {'cont': query.count(),
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mdrp_productos_create(request):
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

        logModel['dataEnviada'] = str(request.data)
        query = Productos.objects.filter(codigo_barras=request.data['codigo_barras'], state=1).first()
        if query is not None:
            errorNoExiste = {'error': 'Ya existe el producto'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(errorNoExiste, status=status.HTTP_404_NOT_FOUND)
        try:
            logModel['dataEnviada'] = str(request.data)
            request.data['created_at'] = str(timezone_now)
            if 'updated_at' in request.data:
                request.data.pop('updated_at')


            serializer = ProductosSerializer(data=request.data)

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
def mdrp_productos_update(request, pk):
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
        logModel['dataEnviada'] = str(request.data)
        try:
            logModel['dataEnviada'] = str(request.data)
            query = Productos.objects.get(pk=pk, state=1)
        except Productos.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            if 'created_at' in request.data:
                request.data.pop('created_at')

            serializer = ProductosSerializer(query, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()

                if serializer.data['estado'] == 'Enviado':
                    imagen_relativa = serializer.data['imagen'].split('https://appvittoria.s3.amazonaws.com/')[-1]

                    serializerProducto = {
                        "nombre": serializer.data['nombre'],
                        "descripcion": serializer.data['descripcion'],
                        "codigoBarras": serializer.data['codigo_barras'],
                        "stock": serializer.data['stock'],
                        "costoCompra": serializer.data['costoCompra'],
                        "precioVentaA": serializer.data['precioVentaA'],
                        "precioVentaB": serializer.data['precioVentaB'],
                        "precioVentaC": serializer.data['precioVentaC'],
                        "precioVentaD": serializer.data['precioVentaD'],
                        "precioVentaE": serializer.data['precioVentaE'],
                        "precioVentaF": serializer.data['precioVentaF'],
                        "porcentaje_comision": serializer.data['porcentaje_comision'],
                        "valor_comision": serializer.data['valor_comision'],
                        "estado": 'Inactivo',
                        "lote": serializer.data['lote'],
                        "proveedor": serializer.data['proveedor'],
                        "imagen_principal": imagen_relativa,
                        "canal": 'megabahia.megadescuento.com',
                        "prefijo":'MEGA',
                        "stockVirtual": [
                            {"canal": "vittoria-test.netlify.app", "estado": False},
                            {"canal": "maxidescuento.megadescuento.com", "estado": False},
                            {"canal": "megabahia.megadescuento.com", "estado": True},
                            {"canal": "tiendamulticompras.megadescuento.com", "estado": False},
                            {"canal": "contraentrega.megadescuento.com", "estado": False},
                            {"canal": "mayorista.megadescuento.com", "estado": False},
                            {"canal": "megadescuento.com", "estado": False},
                            {"canal": "todomegacentro.megadescuento.com", "estado": False},
                            {"canal": "superbarato.megadescuento.com", "estado": False}
                        ]
                    }
                    ProductosPrincipales.objects.create(**serializerProducto)

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
def mdrp_producto_listOne(request, pk):
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
            query = Productos.objects.get(pk=pk, state=1)
        except Productos.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = ProductosSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)
