import json
import requests
import io
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from urllib.parse import urlparse
from django.db.models import Sum
from openpyxl import Workbook
from django.http import HttpResponse
from .constantes import mapeoTodoMegaDescuento, mapeoMegaDescuento, mapeoMegaDescuentoSinEnvio, \
    mapeoTodoMegaDescuentoSinEnvio, mapeoTodoMayoristaSinEnvio, mapeoTodoContraEntrega, mapeoTodoTiendaMulticompras, \
    mapeoTodoMaxiDescuento, mapeoTodoMegaBahia, mapeoCrearProductoWoocommerce, obtener_tipo_pedido
from .serializers import (
    CreateOrderSerializer, PedidosSerializer, ProductosBodegaListSerializer, CreateOrderSuperBaratoSerializer
)
from ..gdc_gestor_contactos.models import Contactos
from ...MDP.mdp_productos.serializers import ProductoCreateSerializer
from django.db.models import Max
from ..gdc_gestor_contactos.serializers import ContactosSerializer
from .models import (
    Pedidos, UniqueCode
)
from ...ADM.vittoria_integraciones.models import Integraciones
from ...FACTURACION.facturacion.models import FacturasEncabezados, FacturasDetalles
from ...MDM.mdm_clientes.models import Clientes
from ...MDM.mdm_clientes.serializers import ClientesUpdateSerializer, ClientesSerializer

from ...MDP.mdp_productos.models import Productos
from ...WOOCOMMERCE.woocommerce.models import Productos as ProductosBodega

from ...MDM.mdm_prospectosClientes.models import ProspectosClientes,ProspectosClientesDetalles

# Sumar Fechas
from datetime import datetime
from datetime import timedelta

from .utils import (
    enviarCorreoVendedor, enviarCorreoCliente, enviarCorreoClienteDespacho, enviarCorreoCourierDespacho,
    enviarCorreoVendedorDespacho, enviarCorreoClienteRechazado, enviarCorreoVendedorRechazado,
    enviarCorreoNotificacionProductos,enviarCorreoVendedorVentaConcreta,enviarCorreoVendedorDevolucion,enviarCorreoTodosClientes,enviarCorreoVendedorEmpacado,enviarCorreoAdminAutorizador, enviarCodigoCorreo
)
from ...ADM.vittoria_usuarios.models import Usuarios
from ...ADM.vittoria_catalogo.models import Catalogo

from django.core.mail import send_mail
from django.utils.crypto import get_random_string

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



            index = request.data['_links']['collection'][0]['href'].find('.com')
            if index != -1:
                canal_principal = request.data['_links']['collection'][0]['href'][:index + 4]
            else:
                canal_principal = request.data['_links']['collection'][0]['href']

            canal_corto = canal_principal.replace('https://', '')
            canal = request.data['_links']['collection'][0]['href']

            #INTEGRACIONES
            integraciones = Integraciones.objects.all()

            #ARITUCULOS
            articulos = []

            for articulo in request.data['line_items']:
                caracteristicas = ""
                for meta in articulo['meta_data']:
                    if meta['display_key'] != '_reduced_stock':
                        caracteristicas = caracteristicas + f"<strong>{meta['display_key']}</strong>: {meta['display_value']}<br>"

                product_ped=Productos.objects.filter(codigoBarras=articulo['sku'], canal = canal_corto).first()
                query_param = Catalogo.objects.filter(tipo='STOCK').first()
                if product_ped is None:
                    stock_nuevo = int(query_param.valor)
                    data_prod=mapeoCrearProductoWoocommerce(request.data['line_items'], stock_nuevo, canal, request.data['date_created'])
                    serializer_prod = ProductoCreateSerializer(data = data_prod)
                    if serializer_prod.is_valid():
                        serializer_prod.save()

                articulos.append({
                    "codigo": articulo['sku'],
                    "articulo": articulo['name'],
                    "valorUnitario": round(float(articulo['price']), 2),
                    "cantidad": articulo['quantity'],
                    "precio": round(float(articulo['total']), 2),
                    "caracteristicas": caracteristicas
                })

            codigoVendedor = next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm17'), None)
            nombreVendedor = next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm18'), None)

            if 'https://megadescuento.com' in canal:
                validarDatosEnvio = next((objeto['value'] for objeto in request.data['meta_data'] if
                                          objeto["key"] == '_shipping_wooccm13'), None)
                if validarDatosEnvio and '@' in validarDatosEnvio:
                    data = mapeoMegaDescuento(request, articulos)
                else:
                    data = mapeoMegaDescuentoSinEnvio(request, articulos)
            elif 'https://todomegacentro.megadescuento.com' in canal and codigoVendedor != '' and nombreVendedor != '':
                validarDatosEnvio = next((objeto['value'] for objeto in request.data['meta_data'] if
                                          objeto["key"] == '_shipping_wooccm13'), None)
                if validarDatosEnvio and '@' in validarDatosEnvio:
                    data = mapeoTodoMegaDescuento(request, articulos)
                else:
                    data = mapeoTodoMegaDescuentoSinEnvio(request, articulos)
            elif 'https://mayorista.megadescuento.com/' in canal:
                data = mapeoTodoMayoristaSinEnvio(request, articulos)
            elif 'https://contraentrega.megadescuento.com/' in canal:
                data = mapeoTodoContraEntrega(request, articulos)
            elif 'https://maxidescuento.megadescuento.com/' in canal:
                data = mapeoTodoMaxiDescuento(request, articulos)
            elif 'https://megabahia.megadescuento.com/' in canal:
                data = mapeoTodoMegaBahia(request, articulos)
            elif 'https://tiendamulticompras.megadescuento.com' in canal:
                data = mapeoTodoTiendaMulticompras(request, articulos)
            elif 'superbarato.megadescuento.com' in canal:
                data = mapeoTodoTiendaMulticompras(request, articulos)

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

                # if data['facturacion']['codigoVendedor']:
                enviarCorreoAdminAutorizador(data)
                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def orders_create_super_barato(request):
    timezone_now = timezone.localtime(timezone.now())
    request.POST._mutable = True
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

            if 'created_at' in request.data:
                request.data.pop('created_at')
            if 'facturacion' in request.data and isinstance(request.data['facturacion'], str):
                facturacionTemporal = request.data.pop('facturacion')[0]
                print('entro if', facturacionTemporal)
                request.data['facturacion'] = json.loads(facturacionTemporal)
            if 'articulos' in request.data and isinstance(request.data['articulos'], str):
                articulosTemporal = request.data.pop('articulos')[0]
                request.data['articulos'] = json.loads(articulosTemporal)

            logModel['dataEnviada'] = str(request.data)

            # dominio_completo = request.headers.get('X-Wc-Webhook-Source')
            # Utiliza urlparse para obtener la información de la URL
            # parsed_url = urlparse(dominio_completo)
            # Combina el nombre de host (dominio) y el esquema (protocolo)
            # domain = parsed_url.netloc
            # dominio_permitidos = Catalogo.objects.filter(tipo='INTEGRACION_WOOCOMMERCE', valor=domain).first()
            # if dominio_permitidos is None:
            #    error = f"Llego un dominio: {domain}"
            #    createLog(logModel, error, logTransaccion)
            #    return Response(error, status=status.HTTP_400_BAD_REQUEST)


            canal = request.data['canal']

            # ARITUCULOS
            articulos = []
            for articulo in request.data['articulos']:
                caracteristicas = ""

                articulos.append({
                    "codigo": articulo['codigo'],
                    "articulo": articulo['articulo'],
                    "valorUnitario": round(float(articulo['valorUnitario']), 2),
                    "cantidad": articulo['cantidad'],
                    "precio": round(float(articulo['precio']), 2),
                    "caracteristicas": caracteristicas
                })

            request.data['facturacion'] = json.dumps(request.data.pop('facturacion')[0])
            request.data['articulos'] = json.dumps(request.data.pop('articulos')[0])
            request.data['gestion_pedido'] = obtener_tipo_pedido(canal)
            serializer = CreateOrderSuperBaratoSerializer(data=request.data)

            if serializer.is_valid():
                print('entro al valid')
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

            if 'usuarioVendedor' in request.data and request.data['usuarioVendedor'] != '':
                filters['facturacion__contains'] = {"codigoVendedor": request.data['usuarioVendedor']}

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
                filters['canal__icontains'] = request.data['canal'].upper()

            if 'metodoPago' in request.data and request.data['metodoPago'] != '':
                filters['metodoPago__icontains'] = request.data['metodoPago'].upper()

            if 'rol' in request.data and 1 == request.data['rol']:
                if 'codigoVendedor' in request.data:
                    filters.pop('codigoVendedor')

            if 'gestion_pedido' in request.data and request.data['gestion_pedido'] != '':
                filters['gestion_pedido'] = request.data['gestion_pedido'].upper()

            companiaUsuario=Usuarios.objects.filter(email=request.user).values_list('compania', flat=True).first()
            usuarios=Usuarios.objects.filter(compania=companiaUsuario).values('username','email','nombres','apellidos')

            # Serializar los datos
            query = Pedidos.objects.filter(**filters).order_by('-created_at')
            estados = Pedidos.objects.values_list('estado', flat=True).distinct()
            metodoPago = Pedidos.objects.values_list('metodoPago', flat=True).distinct()
            if 'estado' in request.data and request.data['estado'] == 'Entregado':
                suma_total = Pedidos.objects.filter(**filters).aggregate(Sum('subtotal'))
                if suma_total['subtotal__sum'] is None:
                    suma_total['subtotal__sum']=0
            else:
                suma_total = Pedidos.objects.filter(estado='Entregado').aggregate(Sum('subtotal'))

            serializer = PedidosSerializer(query[offset:limit], many=True)
            new_serializer_data = {'cont': query.count(), 'info': serializer.data, 'suma_total': suma_total, 'estados': estados, 'usuarios': usuarios, 'metodosEnvios': metodoPago}
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
def orders_update_bodega(request, pk):
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
            query = ProductosBodega.objects.get(pk=pk)
        except ProductosBodega.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':

            serializer = ProductosBodegaListSerializer(query, data=request.data, partial=True)
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
def orders_update(request, pk):
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

            if query.numeroGuia is None and 'estado' in request.data and request.data['estado'] == 'Autorizado':
                numero_guia = generar_numero_guia()
                request.data['numeroGuia'] = numero_guia

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
                        ProductosBodega.objects.create(**{
                            "pedido": query,
                            "nombre": articulo['articulo'],
                            "codigoBarras": articulo['codigo'] if 'codigo' in articulo else None,
                            "caracteristicas": articulo['caracteristicas'] if 'caracteristicas' in articulo else None,
                            "cantidad": articulo['cantidad'] if 'cantidad' in articulo else None,
                            "precio": articulo['valorUnitario'] if 'valorUnitario' in articulo else None,
                            "total": articulo['precio'] if 'precio' in articulo else None,
                            "bodega": articulo['bodega'] if 'bodega' in articulo else None,
                            "imagen": articulo['imagen'] if 'imagen' in articulo else None,
                            "estado": 'Autorizado',
                        })


                if serializer.data['estado'] == 'Empacado':
                    enviarCorreoCliente(serializer.data)
                    enviarCorreoVendedorEmpacado(serializer.data)
                    for articulo in serializer.data['articulos']:
                        producto = Productos.objects.filter(codigoBarras=articulo['codigo'], stockVirtual__contains= {'canal': serializer.data['canal'], 'estado': True}, state=1).first()
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

                    queryProspectos = ProspectosClientes.objects.filter(identificacion=serializer.data['facturacion']['identificacion']).first()
                    if queryProspectos is not None:
                        queryProspectos.nombres = serializer.data['facturacion']['nombres']
                        queryProspectos.apellidos = serializer.data['facturacion']['apellidos']
                        queryProspectos.correo1 = serializer.data['facturacion']['correo']
                        queryProspectos.nombreCompleto = serializer.data['facturacion']['nombres'] + ' ' + serializer.data['facturacion']['apellidos']
                        queryProspectos.whatsapp = serializer.data['facturacion']['telefono']
                        queryProspectos.pais = serializer.data['facturacion']['pais']
                        queryProspectos.provincia = serializer.data['facturacion']['provincia']
                        queryProspectos.ciudad = serializer.data['facturacion']['ciudad']
                        queryProspectos.callePrincipal = serializer.data['facturacion']['callePrincipal']
                        queryProspectos.numeroCasa = serializer.data['facturacion']['numero']
                        queryProspectos.calleSecundaria = serializer.data['facturacion']['calleSecundaria']
                        queryProspectos.referencia = serializer.data['facturacion']['referencia']

                        queryProspectos.save()

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def orders_update_formaPago(request, pk):
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
            query = Pedidos.objects.get(pk=pk, state=1)
        except Pedidos.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':

            #Validaciones
            if 'numeroComprobante' in request.data and request.data['numeroComprobante'] is not None:
                if Pedidos.objects.filter(numeroComprobante=request.data['numeroComprobante']).exclude(pk=pk).first():
                    return Response(data='Ya existe el número de comprobante', status=status.HTTP_404_NOT_FOUND)

            if 'numTransaccionTransferencia' in request.data and request.data['numTransaccionTransferencia'] is not None:
                if Pedidos.objects.filter(numTransaccionTransferencia=request.data['numTransaccionTransferencia']).exclude(pk=pk).first():
                    return Response(data='Ya existe el número de transacción para transferencia', status=status.HTTP_404_NOT_FOUND)

            if 'numTransaccionCredito' in request.data and request.data['numTransaccionCredito'] is not None:
                if Pedidos.objects.filter(numTransaccionCredito=request.data['numTransaccionCredito']).exclude(pk=pk).first():
                    return Response(data='Ya existe el número de transacción para tarjeta de crédito', status=status.HTTP_404_NOT_FOUND)


            now = timezone.localtime(timezone.now())
            # request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')

            serializer = PedidosSerializer(query, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                dataPedidos = {**serializer.data}

                dataPedidos.pop('archivoFactura')
                #dataPedidos.pop('archivoFormaPagoCredito')
                dataPedidos.pop('fotoCupon')

                query2 = Contactos.objects.filter(numeroPedido=serializer.data['numeroPedido']).first()
                serializerContacto = ContactosSerializer(query2, data=dataPedidos, partial=True)

                if serializerContacto.is_valid():
                    contacto = serializerContacto.save()
                    if 'archivoFactura' in  serializer.data and serializer.data['archivoFactura'] is not None:
                        contacto.archivoFactura = obtener_parte_deseada_url(serializer.data['archivoFactura'])

                    '''
                    if 'archivoFormaPagoCredito' in  serializer.data and serializer.data['archivoFormaPagoCredito'] is not None:
                        contacto.archivoFormaPagoCredito = obtener_parte_deseada_url(serializer.data['archivoFormaPagoCredito'])
                    '''

                    contacto.estado = 'Por confirmar'
                    print('CONTACT', contacto)
                    contacto.save()

                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data,  status=status.HTTP_200_OK)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def orders_update_queja(request, pk):
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
            query = Pedidos.objects.get(pk=pk, state=1)
        except Pedidos.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':

            #Validaciones
            if 'numeroComprobanteQueja' in request.data and request.data['numeroComprobanteQueja'] is not None:
                if Pedidos.objects.filter(numeroComprobanteQueja=request.data['numeroComprobanteQueja']).exclude(pk=pk).first():
                    return Response(data='Ya existe el número de comprobante', status=status.HTTP_404_NOT_FOUND)

            now = timezone.localtime(timezone.now())
            # request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')

            serializer = PedidosSerializer(query, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                dataPedidos = {**serializer.data}

                dataPedidos.pop('archivoFactura')
                dataPedidos.pop('archivoFacturaQueja')

                #dataPedidos.pop('archivoFormaPagoCredito')
                dataPedidos.pop('fotoCupon')

                query2 = Contactos.objects.filter(numeroPedido=serializer.data['numeroPedido']).first()
                serializerContacto = ContactosSerializer(query2, data=dataPedidos, partial=True)
                if serializerContacto.is_valid():
                    contacto = serializerContacto.save()
                    if 'archivoFacturaQueja' in serializer.data and serializer.data['archivoFacturaQueja'] is not None:
                        contacto.archivoFacturaQueja = obtener_parte_deseada_url(serializer.data['archivoFacturaQueja'])

                    contacto.estado = 'Queja'

                    contacto.save()

                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data,  status=status.HTTP_200_OK)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


def generar_numero_guia():

    # Obtén el valor máximo de numeroGuia
    max_numero_guia = Pedidos.objects.aggregate(Max('numeroGuia'))['numeroGuia__max']
    print(max_numero_guia)

    # Encuentra el pedido que tiene ese numeroGuia
    pedido = Pedidos.objects.filter(numeroGuia=max_numero_guia).first()

    counter = 0

    today = datetime.now()
    year_two_digits = today.year % 100
    month = today.month
    formatted_month = f"{month:02}"

    if max_numero_guia is None:
        return f"{year_two_digits}{formatted_month}{1:04}"

    if pedido is not None:
        print('entro if')
        last_year = pedido.numeroGuia[:2]
        last_month = pedido.numeroGuia[2:4]

        if (last_month != formatted_month) or (last_year != str(today.year)[-2:]):
            counter = 1
        else:
            countNumGuia = pedido.numeroGuia[-4:]
            counter = int(countNumGuia) + 1

    # Verifica si es un nuevo mes o año para resetear el contador
    return f"{year_two_digits}{formatted_month}{counter:04}"

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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pedidos_exportar(request):
    """
    Este metodo realiza una exportacion de todos los productos en excel de la tabla productos, de la base de datos mdp
    @rtype: DEvuelve un archivo excel
    """
    # Obtener los datos que deseas incluir en el archivo Excel
    filters = {"state": "1"}

    estado = request.GET.get('estado', None)
    usuarioVendedor = request.GET.get('usuarioVendedor', None)
    inicio = request.GET.get('inicio', None)
    fin = request.GET.get('fin', None)
    codigoVendedor = request.GET.get('codigoVendedor', None)
    compania = request.GET.get('compania', None)
    canalEnvio = request.GET.get('canalEnvio', None)
    canal = request.GET.get('canal', None)
    rol = request.GET.get('rol', None)
    if estado is not None:
        filters['estado__in'] = [estado]

    if usuarioVendedor is not None:
        filters['facturacion__contains'] = {"codigoVendedor": usuarioVendedor}

    if inicio is not None:
        filters['created_at__gte'] = str(inicio)
    if fin is not None:
        filters['created_at__lte'] = datetime.strptime(fin, "%Y-%m-%d").date() + timedelta(
            days=1)

    if codigoVendedor is not None:
        filters['codigoVendedor'] = codigoVendedor.upper()

    if compania is not None:
        vendedores = list(
            Usuarios.objects.filter(compania=compania).values_list('username', flat=True))
        filters['codigoVendedor__in'] = vendedores

    if canalEnvio is not None:
        filters['canalEnvio'] = canalEnvio.upper()

    if canal is not None:
        filters['canal'] = canal.upper()

    if rol is not None:
        if 'codigoVendedor' in request.data:
            filters.pop('codigoVendedor')

    # Serializar los datos
    query = Pedidos.objects.filter(**filters).order_by('-created_at')

    # Crear un libro de trabajo de Excel
    wb = Workbook()
    ws = wb.active

    # Definir los encabezados
    ws.append(['FECHA PEDIDO', 'CANAL PEDIDO', 'NUMERO PEDIDO', 'NOMBRES FACTURACION', 'APELLIDOS FACTURACION', 'METODO', 'TELEFONO', 'ESTADO', 'COMISION', 'CODIGO VENDEDOR', 'NOMBRE VENDEDOR', 'CENTRO DE NEGOCIO'])

    # Agregar datos de productos a las filas siguientes
    for pedido in query:
        pedidoSerializer = PedidosSerializer(pedido).data
        facturacion = pedidoSerializer.get('facturacion', {})

        # Verificar si los campos están vacíos antes de acceder a ellos
        fecha_pedido = pedidoSerializer.get('created_at', '').split('T')[0]
        canal_pedido = pedidoSerializer.get('canal', '')
        numero_pedido = pedidoSerializer.get('numeroPedido', '')

        nombres = facturacion.get('nombres', '')
        apellidos = facturacion.get('apellidos', '')
        metodo_pago = pedidoSerializer.get('metodoPago', '')
        telefono = facturacion.get('telefono', '')

        estado = pedidoSerializer.get('estado', '')
        comision = pedidoSerializer.get('comision', '')
        codigo_vendedor = facturacion.get('codigoVendedor', '')
        nombre_vendedor = facturacion.get('nombreVendedor', '')
        centro_negocio = pedidoSerializer.get('companiaVendedor', '')

        # Agregar datos a la hoja de trabajo
        ws.append([fecha_pedido, canal_pedido, numero_pedido, nombres, apellidos, metodo_pago, telefono, estado, comision, codigo_vendedor, nombre_vendedor, centro_negocio])

    # Crear una respuesta HTTP con el contenido del libro de trabajo
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_productos.xlsx"'
    wb.save(response)
    return response


@api_view(['POST'])
def orders_send_code(request):
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
            email = request.data['email']
            if not email:
                return Response({'error': 'Email es requerido'}, status=status.HTTP_400_BAD_REQUEST)

            cliente = Clientes.objects.filter(correo=email).first()
            if cliente:
                serializer = ClientesSerializer(cliente)
                # Generar un código de 6 dígitos
                code = get_random_string(length=6, allowed_chars='0123456789')

                # Guardar el código en la base de datos
                UniqueCode.objects.create(email_cliente=email, code=code)

                # Enviar correo electrónico
                enviarCodigoCorreo(serializer.data, code)
                return Response({'message': 'Correo enviado correctamente'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def orders_verify_code(request):
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

            email_cliente = request.data['correo']
            code = request.data['codigo']

            if not email_cliente or not code:
                return Response('Email y código son requeridos', status=status.HTTP_400_BAD_REQUEST)

            # Verificar el código y el email
            unique_code = UniqueCode.objects.filter(email_cliente=email_cliente, code=code, state=1).first()
            if unique_code:
                # Cambiar el estado del código para indicar que ya ha sido usado o verificado
                unique_code.state = 0
                unique_code.save()

                # Recuperar y devolver los datos del cliente asociados al correo
                cliente = Clientes.objects.filter(correo=email_cliente).first()
                if cliente:
                    serializer = ClientesSerializer(cliente)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response('Cliente no encontrado', status=status.HTTP_404_NOT_FOUND)
            else:
                return Response('Código no válido', status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


def transformar_archivo(url):
    # Hacer la petición GET para descargar el archivo
    respuesta = requests.get(url)

    # Verificar que la petición fue exitosa
    if respuesta.status_code == 200:
        # Usar io.BytesIO para manejar el archivo en memoria
        archivo_en_memoria = io.BytesIO(respuesta.content)
        archivo_en_memoria.name = url.split('/')[-1]  # Opcional, asignar un nombre al archivo
        return archivo_en_memoria
    else:
        print("Error al descargar el archivo")
        return None


def obtener_parte_deseada_url(url):

    # Parsear la URL
    parsed_url = urlparse(url)

    # Obtener el path y limpiar la barra inicial si existe
    clean_path = parsed_url.path.lstrip('/')

    return clean_path