import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .serializers import (
    CreateContactSerializer, ContactosSerializer,
)
from ...MDP.mdp_productos.models import Productos
from ...WOOCOMMERCE.woocommerce.models import (
    Pedidos
)
from .models import (
    Contactos
)
from ..woocommerce.utils import (
    enviarCorreoAdministradorGDC
)
from ..woocommerce.serializers import (
    PedidosSerializer
)
from django.db.models import Sum
from django.db.models import Q

from datetime import datetime
from datetime import timedelta

from ...ADM.vittoria_usuarios.models import Usuarios
from ...ADM.vittoria_catalogo.models import Catalogo
# logs
from ...ADM.vittoria_logs.methods import createLog, datosTipoLog, datosProductosMDP
from ...MDM.mdm_prospectosClientes.models import ProspectosClientes,ProspectosClientesDetalles
from ...MDM.mdm_facturas.models import FacturasEncabezados, FacturasDetalles
from ...MDM.mdm_clientes.models import Clientes

# declaracion variables log
datosAux = datosProductosMDP()
datosTipoLogAux = datosTipoLog()
# asignacion datos modulo
logModulo = datosAux['modulo']
logApi = datosAux['api']
# asignacion tipo de datos
logTransaccion = datosTipoLogAux['transaccion']
logExcepcion = datosTipoLogAux['excepcion']

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gdc_create_contact(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/',
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

            if request.data['facturacion']['identificacion'] != '':
                queryProspectos = ProspectosClientes.objects.filter(
                    Q(identificacion=request.data['facturacion']['identificacion'])).first()
                queryClientes = Clientes.objects.filter(
                    Q(cedula=request.data['facturacion']['identificacion'])).first()
            elif request.data['facturacion']['correo'] !='':
                queryProspectos = ProspectosClientes.objects.filter(
                    Q(correo1=request.data['facturacion']['correo']) |
                    Q(correo2=request.data['facturacion']['correo'])).first()
                queryClientes = Clientes.objects.filter(
                    Q(correo=request.data['facturacion']['correo'])).first()
            else:
                queryProspectos = ProspectosClientes.objects.filter(Q(whatsapp=request.data['facturacion']['telefono'])).first()
                queryClientes = Clientes.objects.filter(Q(telefono=request.data['facturacion']['telefono'])).first()

            if queryProspectos is not None or queryClientes is not None:
                return Response('Contacto ya existe', status=status.HTTP_400_BAD_REQUEST)
            else:
                articulos = []

                for articulo in request.data['articulos']:
                    articulos.append({
                        "codigo": articulo['codigo'],
                        "articulo": articulo['articulo'],
                        "valorUnitario": articulo['valorUnitario'],
                        "cantidad": articulo['cantidad'],
                    })

                serializer = CreateContactSerializer(data=request.data)
                print(request)
                if serializer.is_valid():
                    serializer.save()

                    serializerProspect = {
                        "nombres": serializer.data['facturacion']['nombres'],
                        "apellidos": serializer.data['facturacion']['apellidos'],
                        "telefono": serializer.data['facturacion']['telefono'],
                        "tipoCliente": '',
                        "whatsapp": serializer.data['facturacion']['telefono'],
                        "facebook": '',
                        "twitter": '',
                        "instagram": '',
                        "correo1": serializer.data['facturacion']['correo'],
                        "correo2": '',
                        "pais": serializer.data['facturacion']['pais'],
                        "provincia": serializer.data['facturacion']['provincia'],
                        "ciudad": serializer.data['facturacion']['ciudad'],
                        "canal": serializer.data['canal'],
                        "canalOrigen": '',
                        "metodoPago": '',
                        "codigoProducto": '',
                        "nombreProducto": '',
                        "precio": 0,
                        "tipoPrecio": '',
                        "nombreVendedor": serializer.data['facturacion']['nombreVendedor'],
                        "confirmacionProspecto": '',
                        "imagen": '',
                        "tipoIdentificacion": "Cédula",
                        "identificacion": serializer.data['facturacion']['identificacion'],
                        "nombreCompleto": '',
                        "callePrincipal": '',
                        "numeroCasa": '',
                        "calleSecundaria": '',
                        "referencia": '',
                        "comentarios": '',
                        "comentariosVendedor": '',
                        "cantidad": 0,
                        "subTotal": 0,
                        "descuento": 0,
                        "iva": 0,
                        "total": 0,
                        "courier": "",
                        "articulos": '',
                        "facturacion": '',
                        "envio": '',
                        "state": 1
                    }
                    Pedidos.objects.create(**serializer.data)

                    prospectoEncabezado = ProspectosClientes.objects.create(**serializerProspect)
                    detalleProspecto = []

                    for articuloP in request.data['articulos']:
                        detalleProspecto.append({
                            'articulo': articuloP['articulo'],
                            'valorUnitario': articuloP['valorUnitario'],
                            'cantidad': articuloP['cantidad'],
                            'precio': articuloP['precio'],
                            'codigo': articuloP['codigo'],
                            'informacionAdicional': '',
                            'descuento': 0,
                            'impuesto': 0,
                            'valorDescuento': 0,
                            'total': 0,
                            'state': 1
                        })

                    for detalle in detalleProspecto:
                        ProspectosClientesDetalles.objects.create(
                            prospectoClienteEncabezado=prospectoEncabezado, **detalle)
                    enviarCorreoAdministradorGDC(request.data)

                    createLog(logModel, serializer.data, logTransaccion)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                createLog(logModel, serializer.errors, logExcepcion)
                return Response(status=status.HTTP_200_OK)

        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gdc_create_venta(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/',
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

            articulos = []

            for articulo in request.data['articulos']:
                articulos.append({
                    "codigo": articulo['codigo'],
                     "articulo": articulo['articulo'],
                     "valorUnitario": articulo['valorUnitario'],
                    "cantidad": articulo['cantidad'],
                })

            serializer = CreateContactSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                dataPedidos = {**serializer.data, "codigoVendedor": serializer.data['facturacion']['codigoVendedor']}
                Pedidos.objects.create(**dataPedidos)

                #for articulo in serializer.data['articulos']:
                #    producto = Productos.objects.filter(codigoBarras=articulo['codigo'], state=1).first()
                #    if producto:
                #        producto.stock = producto.stock - int(articulo['cantidad'])
                #        producto.save()
                #        if producto.idPadre != '':
                #            productoPadre = Productos.objects.filter(codigoBarras=producto.idPadre, state=1).first()
                #            if productoPadre:
                #                productoPadre.stock = productoPadre.stock - int(articulo['cantidad'])
                #                productoPadre.save()
                enviarCorreoAdministradorGDC(request.data)

                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(status=status.HTTP_200_OK)

        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def contacts_list(request):
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

            if 'telefono' in request.data:
                if request.data['telefono'] != '':
                    filters['facturacion__icontains'] = str(request.data['telefono'])

            if 'numeroPedido' in request.data and request.data['numeroPedido'] != '':
                filters['numeroPedido__icontains'] = str(request.data['numeroPedido'])

            if 'nombre' in request.data and request.data['nombre'] != '':
                filters['facturacion__nombres__icontains'] = str(request.data['nombre'])

            if 'apellido' in request.data and request.data['apellido'] != '':
                filters['facturacion__apellidos__icontains'] = str(request.data['apellido'])

            if 'canalEnvio' in request.data and request.data['canalEnvio'] != '':
                filters['canalEnvio'] = request.data['canalEnvio'].upper()
            if 'canal' in request.data and request.data['canal'] != '':
                filters['canal'] = request.data['canal'].upper()



            # Serializar los datos
            query = Contactos.objects.filter(**filters).order_by('-created_at')

            suma_total = Contactos.objects.filter(**filters).aggregate(Sum('total'))

            serializer = ContactosSerializer(query[offset:limit], many=True)
            new_serializer_data = {'cont': query.count(), 'info': serializer.data,'suma_total':suma_total}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def contact_listOne(request, pk):
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
            query = Contactos.objects.get(pk=pk, state=1)
        except Contactos.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = ContactosSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gdc_validate_contact(request):
        try:

            if request.data['facturacion']['identificacion'] != '':
                queryProspectos = ProspectosClientes.objects.filter(
                    Q(identificacion=request.data['facturacion']['identificacion'])).first()
                queryClientes = Clientes.objects.filter(
                    Q(cedula=request.data['facturacion']['identificacion'])).first()
            elif request.data['facturacion']['correo'] !='':
                queryProspectos = ProspectosClientes.objects.filter(
                    Q(correo1=request.data['facturacion']['correo']) |
                    Q(correo2=request.data['facturacion']['correo'])).first()
                queryClientes = Clientes.objects.filter(
                    Q(correo=request.data['facturacion']['correo'])).first()
            else:
                queryProspectos = ProspectosClientes.objects.filter(Q(whatsapp=request.data['facturacion']['telefono'])).first()
                queryClientes = Clientes.objects.filter(Q(telefono=request.data['facturacion']['telefono'])).first()

            if queryProspectos is not None or queryClientes is not None:
                return Response('Contacto ya existe', status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_200_OK)

        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def contacts_update(request, pk):
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
            query = Contactos.objects.get(pk=pk, state=1)

        except Contactos.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'POST':

            if 'numeroComprobante' in request.data and request.data['numeroComprobante'] is not None:
                if Contactos.objects.filter(numeroComprobante=request.data['numeroComprobante']).exclude(pk=pk).first():
                    return Response(data='Ya existe el número de comprobante', status=status.HTTP_404_NOT_FOUND)

            if 'numTransaccionTransferencia' in request.data and request.data['numTransaccionTransferencia'] is not None:
                if Contactos.objects.filter(numTransaccionTransferencia=request.data['numTransaccionTransferencia']).exclude(pk=pk).first():
                    return Response(data='Ya existe el número de transacción', status=status.HTTP_404_NOT_FOUND)

            queryClientes=None
            if 'facturacion' in request.data and request.data['facturacion']['identificacion'] != '':
                queryClientes = Clientes.objects.filter(
                    Q(cedula=request.data['facturacion']['identificacion'])).first()
            elif 'facturacion' in request.data and request.data['facturacion']['correo'] != '':
                queryClientes = Clientes.objects.filter(
                    Q(correo=request.data['facturacion']['correo'])).first()
            elif 'facturacion' in request.data and request.data['facturacion']['telefono'] != '':
                queryClientes = Clientes.objects.filter(Q(telefono=request.data['facturacion']['telefono'])).first()

            serializer = ContactosSerializer(query, data=request.data, partial=True)

            if serializer.is_valid():

                serializer.save()
                fotoCupon=serializer.data['fotoCupon'].split(".com/")[1] if serializer.data['fotoCupon'] is not None else None
                query2 = Pedidos.objects.filter(numeroPedido=serializer.data['numeroPedido']).first()
                dataPedidos = {**serializer.data, "codigoVendedor": serializer.data['facturacion']['codigoVendedor'], 'fotoCupon':None}
                serializerPedido = PedidosSerializer(query2, data=dataPedidos, partial=True)
                if serializerPedido.is_valid():
                    serializerPedido.save()
                    query2.fotoCupon=fotoCupon
                    query2.save()
                else:
                    print(serializerPedido.errors)

                if 'Entregado' in serializer.data['estado']:
                    Pedidos.objects.filter(numeroPedido=serializer.data['numeroPedido']).update(estado='Entregado')

                #Obtener id cliente
                datosCliente=Clientes.objects.filter(cedula=serializer.data['facturacion']['identificacion']).first()
                #CREAR FACTURACION ELECTRONICA
                if serializer.data['tipoPago'] is not None and 'facturaElectronica' in serializer.data['tipoPago']:
                    serializerFacturacionElectronica={
                        'cliente':datosCliente,
                        'fecha':serializer.data['created_at'][:10],
                        'tipoIdentificacion':'Cedula',
                        'identificacion':serializer.data['facturacion']['identificacion'],
                        'telefono':serializer.data['facturacion']['telefono'],
                        'correo':serializer.data['facturacion']['correo'],
                        'nombreVendedor':serializer.data['facturacion']['nombreVendedor'],
                        'total':serializer.data['total'],
                        'subTotal':serializer.data['subtotal'],
                        'canal':serializer.data['canal'],
                        'pais':serializer.data['facturacion']['pais'],
                        'provincia':serializer.data['facturacion']['provincia'],
                        'ciudad':serializer.data['facturacion']['ciudad'],
                        'numeroProductosComprados':len(serializer.data['articulos']),
                        'state':1,
                    }
                    facturaEncabezado = FacturasEncabezados.objects.create(**serializerFacturacionElectronica)

                    detalleFactura = []

                    for articuloFDetalle in serializer.data['articulos']:
                        detalleFactura.append({
                            'articulo':articuloFDetalle['articulo'],
                            'valorUnitario':articuloFDetalle['valorUnitario'],
                            'cantidad':articuloFDetalle['cantidad'],
                            'precio':articuloFDetalle['precio'],
                            'codigo':articuloFDetalle['codigo'],
                            'total':articuloFDetalle['precio'],
                            'state':1,
                        })

                    for detalle in detalleFactura:
                        FacturasDetalles.objects.create(
                            facturaEncabezado_id=facturaEncabezado.id, **detalle)

                #CLIENT
                serializerClient = {
                    "tipoCliente": "Consumidor final",
                    "tipoIdentificacion": "Cédula",
                    "cedula": serializer.data['facturacion']['identificacion'],
                    "nombreCompleto": serializer.data['facturacion']['nombres'] + ' ' +
                                      serializer.data['facturacion']['apellidos'],
                    "nombres": serializer.data['facturacion']['nombres'],
                    "apellidos": serializer.data['facturacion']['apellidos'],
                    "nacionalidad": "Ecuatoriana",
                    "paisNacimiento": serializer.data['facturacion']['pais'],
                    "provinciaNacimiento": serializer.data['facturacion']['provincia'],
                    "ciudadNacimiento": serializer.data['facturacion']['ciudad'],
                    "correo": serializer.data['facturacion']['correo'],
                    "telefono": serializer.data['facturacion']['telefono'],
                    "state": 1
                }
                if queryClientes is not None:
                    (Clientes.objects.filter(cedula=serializer.data['facturacion']['identificacion'])
                     .update(**serializerClient))
                else:
                    Clientes.objects.create(**serializerClient)

                if 'Entregado' in serializer.data['estado']:
                    for articulo in serializer.data['articulos']:
                        producto = Productos.objects.filter(codigoBarras=articulo['codigo'], canal=articulo['canal'], woocommerceId=articulo['woocommerceId'], state=1).first()
                        if producto:
                            producto.stock = producto.stock - int(articulo['cantidad'])
                            producto.save()
                            if producto.idPadre != '':
                                productoPadre = Productos.objects.filter(codigoBarras=producto.idPadre, state=1).first()
                                if productoPadre:
                                    productoPadre.stock = productoPadre.stock - int(articulo['cantidad'])
                                    productoPadre.save()

                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        print('error', err)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)