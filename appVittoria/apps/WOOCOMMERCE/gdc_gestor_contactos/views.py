from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .serializers import (
    CreateContactSerializer, ContactosSerializer,
)

from ...FACTURACION.facturacion.models import FacturasEncabezados, FacturasDetalles

from .models import (
    Contactos
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


            #queryProspectos = ProspectosClientes.objects.filter(Q(identificacion=request.data['facturacion']['identificacion']) |
            #                                          Q(correo1=request.data['facturacion']['correo']) |
            #                                          Q(correo2=request.data['facturacion']['correo']) |
            #                                          Q(whatsapp=request.data['facturacion']['telefono']))

            #queryClientes = Clientes.objects.filter(
            #    Q(cedula=request.data['facturacion']['identificacion']) |
            #    Q(correo=request.data['facturacion']['correo']) |
            #    Q(telefono=request.data['facturacion']['telefono']))


            #if queryProspectos or queryClientes:
            #    return Response('Contacto ya existe', status=status.HTTP_400_BAD_REQUEST)

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
                prospectoEncabezado=ProspectosClientes.objects.create(**serializerProspect)
                detalleProspecto = []

                for articuloP in request.data['articulos']:
                    detalleProspecto.append({
                        'articulo':articuloP['articulo'],
                        'valorUnitario':articuloP['valorUnitario'],
                        'cantidad':articuloP['cantidad'],
                        'precio' : articuloP['precio'],
                        'codigo':articuloP['codigo'],
                        'informacionAdicional':'',
                        'descuento':0,
                        'impuesto':0,
                        'valorDescuento':0,
                        'total':0,
                        'state':1
                    })

                for detalle in detalleProspecto:
                    ProspectosClientesDetalles.objects.create(
                        prospectoClienteEncabezado=prospectoEncabezado, **detalle)

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
            if 'canal' in request.data and request.data['canal'] != '':
                filters['canal'] = request.data['canal'].upper()
            if 'rol' in request.data:
                if 'codigoVendedor' in request.data:
                    filters.pop('codigoVendedor')
                elif 'compania' in request.data:
                    filters.pop('codigoVendedor__in')


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

            serializer = ContactosSerializer(query, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                if serializer.data['estado'] == 'Autorizado' and 'Previo-Pago' in serializer.data['metodoPago']:
                    facturaCreada = FacturasEncabezados.objects.create(**{
                        "numeroPedido": serializer.data['numeroPedido'],
                        "estadoPedido": "En espera",
                        "fechaPedido": serializer.data['created_at'][:10],
                        "notaCliente": "",
                        "nombresFacturacion": serializer.data['facturacion']['nombres'],
                        "apellidosFacturacion": serializer.data['facturacion']['apellidos'],
                        "empresaFacturacion": "",
                        "direccionFacturacion": serializer.data['facturacion']['callePrincipal'],
                        "ciudadFacturacion": serializer.data['facturacion']['ciudad'],
                        "provinciaFacturacion": serializer.data['facturacion']['provincia'],
                        "codigoPostalFacturacion": "",
                        "paisFacturacion": serializer.data['facturacion']['pais'],
                        "correoElectronicoFacturacion": serializer.data['facturacion']['correo'],
                        "telefonoFacturacion": serializer.data['facturacion']['telefono'],
                        "nombresEnvio": serializer.data['envio']['nombres'],
                        "apellidosEnvio": serializer.data['envio']['apellidos'],
                        "direccionEnvio": serializer.data['envio']['callePrincipal'],
                        "ciudadEnvio": serializer.data['envio']['ciudad'],
                        "provinciaEnvio": serializer.data['envio']['provincia'],
                        "codigoPostalEnvio": "",
                        "paisEnvio": serializer.data['envio']['pais'],
                        "metodoPago": serializer.data['metodoPago'],
                        "descuentoCarrito": "",
                        "subtotalPedido": serializer.data['subtotal'],
                        "metodoEnvio": "",
                        "importeEnvioPedido": "",
                        "importeReemsolsadoPedido": "",
                        "importeTotalPedido": serializer.data['total'],
                        "importeTotalImpuestoPedido": "",
                        "estadoSRI": "",
                    })
                    for articulo in serializer.data['articulos']:
                        FacturasDetalles.objects.create(**{
                            "numeroPedido": serializer.data['numeroPedido'],
                            "SKU": articulo['codigo'],
                            "articulo": articulo['articulo'],
                            "nombreArticulo": "",
                            "cantidad": articulo['cantidad'],
                            "precio": articulo['precio'],
                            "cupon": "",
                            "importeDescuento": "",
                            "importeImpuestoDescuento": "",
                            "facturaEncabezado": facturaCreada
                        })
                #if serializer.data['estado'] == 'Empacado':
                #    for articulo in serializer.data['articulos']:
                #        producto = Contactos.objects.filter(codigoBarras=articulo['codigo'], state=1).first()
                #        if producto:
                #            producto.stock = producto.stock - int(articulo['cantidad'])
                #            producto.save()
                #            if producto.idPadre != '':
                #                productoPadre = Contactos.objects.filter(codigoBarras=producto.idPadre, state=1).first()
                #                if productoPadre:
                #                    productoPadre.stock = productoPadre.stock - int(articulo['cantidad'])
                #                    productoPadre.save()
                #if serializer.data['estado'] == 'Despachado':
                #    enviarCorreoClienteDespacho(serializer.data)
                #    enviarCorreoCourierDespacho(serializer.data)
                #    enviarCorreoVendedorDespacho(serializer.data)
                    # Se crea el usuario cuando el pedido es despachado
                #    cliente = {
                #        'nombreCompleto': serializer.data['facturacion']['nombres'] + serializer.data['facturacion']['apellidos'],
                #        'nombres': serializer.data['facturacion']['nombres'],
                #        'apellidos': serializer.data['facturacion']['apellidos'],
                #        'cedula': serializer.data['facturacion']['identificacion'],
                #        'tipoIdentificacion': 'Cédula',
                #        'correo': serializer.data['facturacion']['correo'],
                #        'paisNacimiento': serializer.data['facturacion']['pais'],
                #        'provinciaNacimiento': serializer.data['facturacion']['provincia'],
                #        'ciudadNacimiento': serializer.data['facturacion']['ciudad'],
                #    }

                #    clienteExiste = Clientes.objects.filter(cedula=serializer.data['facturacion']['identificacion']).first()
                #    if clienteExiste is None:
                #        Clientes.objects.create(**cliente)
                #    else:
                #        clienteSerializer = ClientesUpdateSerializer(clienteExiste, data=cliente, partial=True)
                #        if clienteSerializer.is_valid():
                #            clienteSerializer.save()
                #if serializer.data['estado'] == 'Rechazado':
                #    enviarCorreoClienteRechazado(serializer.data)
                #    enviarCorreoVendedorRechazado(serializer.data)
                #if serializer.data['estado'] == 'Completado':
                #    enviarCorreoVendedorVentaConcreta(serializer.data)
                #if serializer.data['estado'] == 'Paquete Ingresado Stock':
                #    enviarCorreoVendedorDevolucion(serializer.data)
                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)