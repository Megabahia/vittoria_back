
def mapeoCrearProducto(request):
    index = request.data['permalink'].find('.com')
    if index != -1:
        canal = request.data['permalink'][:index + 4]
    else:
        canal = request.data['permalink']

    canal = canal.replace('https://', '')

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
    }


def mapeoActualizarProducto(request):

    return {
        "nombre":request.data['name'],
        "descripcion":request.data['description'],
        "stock":int(request.data['stock_quantity']),
        "costoCompra":float(request.data['price']),
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
    }

