
def mapeoCrearProducto(request):
    index = request.data['permalink'].find('.com')
    if index != -1:
        canal = request.data['permalink'][:index + 4]
    else:
        canal = request.data['permalink']

    canal = canal.replace('https://', '')

    # Lista de todos los canales disponibles en stockVirtual
    canales_stock_virtual = [
        "vittoria-test.netlify.app",
        "maxidescuento.megadescuento.com",
        "megabahia.megadescuento.com",
        "tiendamulticompras.megadescuento.com",
        "contraentrega.megadescuento.com",
        "mayorista.megadescuento.com",
        "megadescuento.com",
        "todomegacentro.megadescuento.com"
    ]

    # Generar la lista stockVirtual comparando el canal extraído con la lista de canales
    stock_virtual = [{"canal": sv_canal, "estado": sv_canal == canal} for sv_canal in canales_stock_virtual]

    return {
        "woocommerceId":request.data['id'],
        "nombre":request.data['name'],
        "descripcion":request.data['description'],
        "codigoBarras":request.data['sku'],
        "stock":int(request.data['stock_quantity']),
        "costoCompra":0,
        "precioVentaA":float(request.data['regular_price']),
        "precioVentaB":float(request.data['sale_price']),
        "precioVentaC":0,
        "precioVentaD":0,
        "precioVentaE":0,
        "precioVentaF":0,
        "canal":canal,
        "estado":'Activo',
        'fechaElaboracion':request.data['date_created'][:10],
        'fechaCaducidad':request.data['date_created'][:10],
        "created_at":request.data['date_created'],
        "stockVirtual": stock_virtual
    }


def mapeoActualizarProducto(request):
    # Lista de todos los canales disponibles en stockVirtual
    canales_stock_virtual = [
        "vittoria-test.netlify.app",
        "maxidescuento.megadescuento.com",
        "megabahia.megadescuento.com",
        "tiendamulticompras.megadescuento.com",
        "contraentrega.megadescuento.com",
        "mayorista.megadescuento.com",
        "megadescuento.com",
        "todomegacentro.megadescuento.com"
    ]

    # Generar la lista stockVirtual comparando el canal extraído con la lista de canales
    stock_virtual = [{"canal": sv_canal, "estado": sv_canal == canal} for sv_canal in canales_stock_virtual]

    return {
        "nombre":request.data['name'],
        "descripcion":request.data['description'],
        "stock":int(request.data['stock_quantity']),
        "costoCompra":0,
        "precioVentaA":float(request.data['regular_price']),
        "precioVentaB":float(request.data['sale_price']),
        "precioVentaC":0.00,
        "precioVentaD":0.00,
        "precioVentaE":0.00,
        "precioVentaF":0.00,
        "estado":'Activo',
        'fechaElaboracion':request.data['date_created'][:10],
        'fechaCaducidad':request.data['date_created'][:10],
        "updated_at":request.data['date_modified'],
        "stockVirtual": stock_virtual

    }


