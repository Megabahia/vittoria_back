from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from urllib.parse import urlparse
from django.db.models import Sum
from .constantes import mapeoTodoMegaDescuento, mapeoMegaDescuento, mapeoMegaDescuentoSinEnvio, \
    mapeoTodoMegaDescuentoSinEnvio,mapeoTodoMayorista,mapeoTodoMayoristaSinEnvio,mapeoTodoContraEntrega,mapeoTodoTiendaMulticompras, mapeoTodoMaxiDescuento, mapeoTodoMegaBahia
from .serializers import (
    CreateOrderSerializer, PedidosSerializer, ProductosBodegaListSerializer
)
from django.db.models import Max

from .models import (
    Pedidos
)
from ...FACTURACION.facturacion.models import FacturasEncabezados, FacturasDetalles
from ...MDM.mdm_clientes.models import Clientes
from ...MDM.mdm_clientes.serializers import ClientesUpdateSerializer

from ...MDP.mdp_productos.models import Productos
from ...WOOCOMMERCE.woocommerce.models import Productos as ProductosBodega

from ...MDM.mdm_prospectosClientes.models import ProspectosClientes,ProspectosClientesDetalles

# Sumar Fechas
from datetime import datetime
from datetime import timedelta

from .utils import (
    enviarCorreoVendedor, enviarCorreoCliente, enviarCorreoClienteDespacho, enviarCorreoCourierDespacho,
    enviarCorreoVendedorDespacho, enviarCorreoClienteRechazado, enviarCorreoVendedorRechazado,
    enviarCorreoNotificacionProductos,enviarCorreoVendedorVentaConcreta,enviarCorreoVendedorDevolucion,enviarCorreoTodosClientes,enviarCorreoVendedorEmpacado,enviarCorreoAdminAutorizador
)
from ...ADM.vittoria_usuarios.models import Usuarios
from ...ADM.vittoria_catalogo.models import Catalogo

# logs
from ...ADM.vittoria_logs.methods import createLog, datosTipoLog, datosProductosMDP
import re

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
            #Utiliza urlparse para obtener la información de la URL
            parsed_url = urlparse(dominio_completo)
            #Combina el nombre de host (dominio) y el esquema (protocolo)
            domain = parsed_url.netloc
            dominio_permitidos = Catalogo.objects.filter(tipo='INTEGRACION_WOOCOMMERCE', valor=domain).first()
            if dominio_permitidos is None:
                error = f"Llego un dominio: {domain}"
                createLog(logModel, error, logTransaccion)
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            articulos = []

            for articulo in request.data['line_items']:
                caracteristicas = ""
                for meta in articulo['meta_data']:
                    if meta['display_key'] != '_reduced_stock':
                        caracteristicas = caracteristicas + f"<strong>{meta['display_key']}</strong>: {meta['display_value']}<br>"

                articulos.append({
                    "codigo": articulo['sku'],
                    "articulo": articulo['name'],
                    "valorUnitario": round(float(articulo['price']), 2),
                    "cantidad": articulo['quantity'],
                    "precio": round(float(articulo['total']), 2),
                    "caracteristicas": caracteristicas
                })

            canal = request.data['_links']['collection'][0]['href']
            codigoVendedor = next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm17'), None)
            nombreVendedor = next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm18'), None)

            print(canal)
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
            elif 'https://mayorista.megadescuento.com/' in canal:
                data = mapeoTodoMayorista(request, articulos)
            elif 'https://contraentrega.megadescuento.com/' in canal:
                data = mapeoTodoContraEntrega(request, articulos)
            elif 'https://maxidescuento.megadescuento.com/' in canal:
                data = mapeoTodoMaxiDescuento(request, articulos)
            elif 'https://megabahia.megadescuento.com/' in canal:
                data = mapeoTodoMegaBahia(request, articulos)
            elif 'https://tiendamulticompras.megadescuento.com' in canal:
                #validarDatosEnvio = next((objeto['value'] for objeto in request.data['meta_data'] if
                #                          objeto["key"] == '_shipping_wooccm13'), None)
                #if '@' in validarDatosEnvio:
                data = mapeoTodoTiendaMulticompras(request, articulos)
                #else:
                #    data = mapeoTodoTiendaMulticompras(request, articulos)

            serializer = CreateOrderSerializer(data=data)

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
                prospectoEncabezado = ProspectosClientes.objects.create(**serializerProspect)
                detalleProspecto = []

                for articuloP in serializer.data['articulos']:
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

                if data['facturacion']['codigoVendedor']:
                    enviarCorreoAdminAutorizador(data)
                #enviarCorreoTodosClientes(data)
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
def orders_create_contact(request):
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

            serializer = CreateOrderSerializer(data=request.data)

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
            if 'canal' in request.data and request.data['canal'] != '':
                filters['canal'] = request.data['canal'].upper()
            if 'rol' in request.data:
                if 'codigoVendedor' in request.data:
                    filters.pop('codigoVendedor')
                elif 'compania' in request.data:
                    filters.pop('codigoVendedor__in')


            # Serializar los datos
            query = Pedidos.objects.filter(**filters).order_by('-created_at')

            suma_total = Pedidos.objects.filter(**filters).aggregate(Sum('total'))
            serializer = PedidosSerializer(query[offset:limit], many=True)
            new_serializer_data = {'cont': query.count(), 'info': serializer.data,'suma_total':suma_total}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def orders_list_bodega(request):
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
            filters = {}

            #if 'inicio' in request.data and request.data['inicio'] != '':
            #    filters['created_at__gte'] = str(request.data['inicio'])
            #if 'fin' in request.data and request.data['fin'] != '':
            #    filters['created_at__lte'] = datetime.strptime(request.data['fin'], "%Y-%m-%d").date() + timedelta(
            #        days=1)

            if 'bodega' in request.data and request.data['bodega'] != '':
                filters['bodega'] = request.data['bodega'].upper()

            if 'estado' in request.data and request.data['estado'] != '':
                filters['estado'] = request.data['estado'].upper()

            unique_ids = ProductosBodega.objects.filter(**filters).values('bodega', 'pedido_id').annotate(
                max_id=Max('id')
            ).values_list('max_id', flat=True)

            # Consulta principal para obtener los registros completos basados en los ID obtenidos en la subconsulta
            query = ProductosBodega.objects.filter(id__in=unique_ids)
            serializer=ProductosBodegaListSerializer(query, many = True)

            # envio de datos
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def orders_listOne_bodega(request, pk):
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

        if request.method == 'POST':
            try:
                queryProducts = ProductosBodega.objects.filter(pedido_id=pk, bodega=request.data['bodega'])
                datosFiltrados = ProductosBodega.objects.filter(pedido_id=pk)

                if len(queryProducts) != len(datosFiltrados):
                    mostrar_datos = False
                else:
                    mostrar_datos = True

                # tomar el dato
                serializer = ProductosBodegaListSerializer(queryProducts, many=True)
                new_serializer_data = {'info': serializer.data, 'mostrar_datos': mostrar_datos}

                createLog(logModel, new_serializer_data, logTransaccion)
                return Response(new_serializer_data, status=status.HTTP_200_OK)
            except Pedidos.DoesNotExist:
                err = {"error": "No existe"}
                createLog(logModel, err, logExcepcion)
                return Response(err, status=status.HTTP_404_NOT_FOUND)

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
                if serializer.data['estado'] == 'Autorizado' and 'Previo-Pago' in serializer.data['metodoPago']:
                    enviarCorreoCliente(serializer.data)
                    enviarCorreoVendedor(serializer.data)
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
                if serializer.data['estado'] == 'Empacado':
                    enviarCorreoCliente(serializer.data)
                    enviarCorreoVendedorEmpacado(serializer.data)
                    for articulo in serializer.data['articulos']:
                        producto = Productos.objects.filter(codigoBarras=articulo['codigo'], state=1).first()
                        if producto:
                            producto.stock = producto.stock - int(articulo['cantidad'])
                            producto.save()
                            if producto.idPadre != '':
                                productoPadre = Productos.objects.filter(codigoBarras=producto.idPadre, state=1).first()
                                if productoPadre:
                                    productoPadre.stock = productoPadre.stock - int(articulo['cantidad'])
                                    productoPadre.save()
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
                if serializer.data['estado'] == 'Completado':
                    enviarCorreoVendedorVentaConcreta(serializer.data)
                if serializer.data['estado'] == 'Paquete Ingresado Stock':
                    enviarCorreoVendedorDevolucion(serializer.data)
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def orders_notificacion(request, pk):
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
            enviarCorreoNotificacionProductos(serializer.data)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)