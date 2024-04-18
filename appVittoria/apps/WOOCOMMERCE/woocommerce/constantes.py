provincias = {
    "EC-A": "Azuay",
    "EC-C": "Carchi",
    "EC-O": "El Oro",
    "EC-G": "Guayas",
    "EC-R": "Los Ríos",
    "EC-N": "Napo",
    "EC-P": "Pichincha",
    "EC-U": "Sucumbíos",
    "EC-B": "Bolívar",
    "EC-H": "Chimborazo",
    "EC-E": "Esmeraldas",
    "EC-I": "Imbabura",
    "EC-M": "Manabí",
    "EC-D": "Orellana",
    "EC-SE": "Santa Elena",
    "EC-T": "Tungurahua",
    "EC-F": "Cañar",
    "EC-X": "Cotopaxi",
    "EC-W": "Galápagos",
    "EC-L": "Loja",
    "EC-S": "Morona-Santiago",
    "EC-Y": "Pastaza",
    "EC-SD": "Santo Domingo de los Tsáchilas",
    "EC-Z": "Zamora-Chinchipe",
}


def mapeoTodoMegaDescuento(request, articulos):
    total = request.data['total']
    codigoVendedor = next((objeto['value'] for objeto in request.data['meta_data'] if
          objeto["key"] == '_billing_wooccm17'), None)
    return {
        "estado": 'Pendiente',
        "envioTotal": request.data['shipping_total'],
        "total": total,
        "subtotal": total,
        "facturacion": {
            "nombres": request.data['billing']['first_name'],
            "apellidos": request.data['billing']['last_name'],
            "correo": request.data['billing']['email'],
            "identificacion": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm12'), None),
            "telefono": request.data['billing']['company'],
            "pais": "Ecuador",
            "provincia": provincias[request.data['billing']['state']],
            "ciudad": request.data['billing']['city'],
            "callePrincipal": request.data['billing']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm15'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm14'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_billing_wooccm13'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_billing_wooccm16'), None),
            "codigoVendedor": codigoVendedor,
            "nombreVendedor": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm18'), None),
            "correoVendedor": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm19'), None),
            "comprobantePago": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm11'), None),
        },
        "envio": {
            "nombres": request.data['shipping']['first_name'],
            "apellidos": request.data['shipping']['last_name'],
            "correo": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_shipping_wooccm13'), None),
            "identificacion": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_shipping_wooccm14'), None),
            "telefono": next((objeto['value'] for objeto in request.data['meta_data'] if
                              objeto["key"] == '_shipping_wooccm15'), None),
            "pais": "Ecuador",
            "provincia": provincias[request.data['shipping']['state']],
            "ciudad": request.data['shipping']['city'],
            "callePrincipal": request.data['shipping']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_shipping_wooccm9'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_shipping_wooccm10'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_shipping_wooccm11'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_shipping_wooccm12'), None),
            "canalEnvio": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_shipping_wooccm12'), None),
        },
        "metodoPago": request.data['payment_method_title'],
        "numeroPedido": request.data['number'],
        "articulos": articulos,
        "envios": request.data['shipping_lines'],
        "json": request.data,
        "canal": request.data['_links']['collection'][0]['href'],
        "created_at": request.data['date_created'],
        "codigoVendedor": codigoVendedor,
    }

def mapeoTodoMegaDescuentoSinEnvio(request, articulos):
    total = request.data['total']
    codigoVendedor = next((objeto['value'] for objeto in request.data['meta_data'] if
          objeto["key"] == '_billing_wooccm17'), None)
    return {
        "estado": 'Pendiente',
        "envioTotal": request.data['shipping_total'],
        "total": total,
        "subtotal": total,
        "facturacion": {
            "nombres": request.data['billing']['first_name'],
            "apellidos": request.data['billing']['last_name'],
            "correo": request.data['billing']['email'],
            "identificacion": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm12'), None),
            "telefono": request.data['billing']['company'],
            "pais": "Ecuador",
            "provincia": provincias[request.data['billing']['state']],
            "ciudad": request.data['billing']['city'],
            "callePrincipal": request.data['billing']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm15'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm14'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_billing_wooccm13'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_billing_wooccm16'), None),
            "codigoVendedor": codigoVendedor,
            "nombreVendedor": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm18'), None),
            "correoVendedor": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm19'), None),
            "comprobantePago": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm11'), None),
        },
        "envio": {
            "nombres": request.data['shipping']['first_name'],
            "apellidos": request.data['shipping']['last_name'],
            "correo": request.data['billing']['email'],
            "identificacion": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm12'), None),
            "telefono": request.data['billing']['company'],
            "pais": "Ecuador",
            "provincia": provincias[request.data['billing']['state']],
            "ciudad": request.data['billing']['city'],
            "callePrincipal": request.data['billing']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm15'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm14'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_billing_wooccm13'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_billing_wooccm16'), None),
            "canalEnvio": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_shipping_wooccm12'), None),
        },
        "metodoPago": request.data['payment_method_title'],
        "numeroPedido": request.data['number'],
        "articulos": articulos,
        "envios": request.data['shipping_lines'],
        "json": request.data,
        "canal": request.data['_links']['collection'][0]['href'],
        "created_at": request.data['date_created'],
        "codigoVendedor": codigoVendedor,
    }

def mapeoTodoMayorista(request, articulos):
    total = request.data['total']
    codigoVendedor = next((objeto['value'] for objeto in request.data['meta_data'] if
          objeto["key"] == '_billing_wooccm16'), None)
    return {
        "estado": 'Pendiente',
        "envioTotal": request.data['shipping_total'],
        "total": total,
        "subtotal": total,
        "facturacion": {
            "nombres": request.data['billing']['first_name'],
            "apellidos": request.data['billing']['last_name'],
            "correo": request.data['billing']['email'],
            "identificacion": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm15'), None),
            "telefono": request.data['billing']['company'],
            "pais": "Ecuador",
            "provincia": provincias[request.data['billing']['state']],
            "ciudad": request.data['billing']['city'],
            "callePrincipal": request.data['billing']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm11'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm12'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_billing_wooccm13'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_billing_wooccm14'), None),
            "codigoVendedor": codigoVendedor,
            "nombreVendedor": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm17'), None),
            "correoVendedor": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm19'), None),
            "comprobantePago": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm11'), None),
        },
        "envio": {
            "nombres": request.data['shipping']['first_name'],
            "apellidos": request.data['shipping']['last_name'],
            "correo": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_shipping_wooccm13'), None),
            "identificacion": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_shipping_wooccm14'), None),
            "telefono": next((objeto['value'] for objeto in request.data['meta_data'] if
                              objeto["key"] == '_shipping_wooccm15'), None),
            "pais": "Ecuador",
            "provincia": provincias[request.data['shipping']['state']],
            "ciudad": request.data['shipping']['city'],
            "callePrincipal": request.data['shipping']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_shipping_wooccm9'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_shipping_wooccm10'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_shipping_wooccm11'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_shipping_wooccm12'), None),
            "canalEnvio": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_shipping_wooccm12'), None),
        },
        "metodoPago": request.data['payment_method_title'],
        "numeroPedido": request.data['number'],
        "articulos": articulos,
        "envios": request.data['shipping_lines'],
        "json": request.data,
        "canal": request.data['_links']['collection'][0]['href'],
        "created_at": request.data['date_created'],
        "codigoVendedor": codigoVendedor,
    }

def mapeoTodoMayoristaSinEnvio(request, articulos):
    total = request.data['total']
    codigoVendedor = next((objeto['value'] for objeto in request.data['meta_data'] if
          objeto["key"] == '_billing_wooccm16'), None)
    return {
        "estado": 'Pendiente',
        "envioTotal": request.data['shipping_total'],
        "total": total,
        "subtotal": total,
        "facturacion": {
            "nombres": request.data['billing']['first_name'],
            "apellidos": request.data['billing']['last_name'],
            "correo": request.data['billing']['email'],
            "identificacion": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm15'), None),
            "telefono": request.data['billing']['company'],
            "pais": "Ecuador",
            "provincia": provincias[request.data['billing']['state']],
            "ciudad": request.data['billing']['city'],
            "callePrincipal": request.data['billing']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm11'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm12'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_billing_wooccm13'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_billing_wooccm14'), None),
            "codigoVendedor": codigoVendedor,
            "nombreVendedor": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm17'), None),
            "correoVendedor": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm19'), None),
            "comprobantePago": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm11'), None),
        },
        "envio": {
            "nombres": request.data['shipping']['first_name'],
            "apellidos": request.data['shipping']['last_name'],
            "correo": request.data['billing']['email'],
            "identificacion": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_shipping_wooccm13'), None),
            "telefono": request.data['billing']['company'],
            "pais": "Ecuador",
            "provincia": provincias[request.data['billing']['state']],
            "ciudad": request.data['billing']['city'],
            "callePrincipal": request.data['billing']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm15'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm14'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_billing_wooccm13'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_billing_wooccm16'), None),
            "canalEnvio": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_shipping_wooccm12'), None),
        },
        "metodoPago": request.data['payment_method_title'],
        "numeroPedido": request.data['number'],
        "articulos": articulos,
        "envios": request.data['shipping_lines'],
        "json": request.data,
        "canal": request.data['_links']['collection'][0]['href'],
        "created_at": request.data['date_created'],
        "codigoVendedor": codigoVendedor,
    }

def mapeoMegaDescuento(request, articulos):
    total = request.data['total']
    codigoVendedor = next((objeto['value'] for objeto in request.data['meta_data'] if
          objeto["key"] == ''), None)
    return {
        "estado": 'Pendiente',
        "envioTotal": request.data['shipping_total'],
        "total": total,
        "subtotal": total,
        "facturacion": {
            "nombres": request.data['billing']['first_name'],
            "apellidos": request.data['billing']['last_name'],
            "correo": request.data['billing']['email'],
            "identificacion": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm12'), None),
            "telefono": request.data['billing']['company'],
            "pais": "Ecuador",
            "provincia": provincias[request.data['billing']['state']],
            "ciudad": request.data['billing']['city'],
            "callePrincipal": request.data['billing']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm13'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm16'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_billing_wooccm14'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_billing_wooccm15'), None),
            "codigoVendedor": '',
            "nombreVendedor": '',
            "comprobantePago": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm11'), None),
        },
        "envio": {
            "nombres": request.data['shipping']['first_name'],
            "apellidos": request.data['shipping']['last_name'],
            "correo": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_shipping_wooccm13'), None),
            "identificacion": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_shipping_wooccm14'), None),
            "telefono": next((objeto['value'] for objeto in request.data['meta_data'] if
                              objeto["key"] == '_shipping_wooccm15'), None),
            "pais": "Ecuador",
            "provincia": provincias[request.data['shipping']['state']],
            "ciudad": request.data['shipping']['city'],
            "callePrincipal": request.data['shipping']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_shipping_wooccm9'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_shipping_wooccm10'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_shipping_wooccm11'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_shipping_wooccm12'), None),
        },
        "metodoPago": request.data['payment_method_title'],
        "numeroPedido": request.data['number'],
        "articulos": articulos,
        "envios": request.data['shipping_lines'],
        "json": request.data,
        "canal": next((objeto['value'] for objeto in request.data['meta_data'] if
                       objeto["key"] == '_wc_order_attribution_session_entry'), None),
        "created_at": request.data['date_created'],
        "codigoVendedor": '',
    }


def mapeoMegaDescuentoSinEnvio(request, articulos):
    total = request.data['total']
    codigoVendedor = next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm16'), None)
    return {
        "estado": 'Pendiente',
        "envioTotal": request.data['shipping_total'],
        "total": total,
        "subtotal": total,
        "facturacion": {
            "nombres": request.data['billing']['first_name'],
            "apellidos": request.data['billing']['last_name'],
            "correo": request.data['billing']['email'],
            "identificacion": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm12'), None),
            "telefono": request.data['billing']['company'],
            "pais": "Ecuador",
            "provincia": provincias[request.data['billing']['state']],
            "ciudad": request.data['billing']['city'],
            "callePrincipal": request.data['billing']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm13'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm16'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_billing_wooccm14'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_billing_wooccm15'), None),
            "codigoVendedor": '',
            "nombreVendedor": '',
            "comprobantePago": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm11'), None),
        },
        "envio": {
            "nombres": request.data['shipping']['first_name'],
            "apellidos": request.data['shipping']['last_name'],
            "correo": request.data['billing']['email'],
            "identificacion": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm12'), None),
            "telefono": request.data['billing']['company'],
            "pais": "Ecuador",
            "provincia": provincias[request.data['billing']['state']],
            "ciudad": request.data['billing']['city'],
            "callePrincipal": request.data['billing']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm13'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm16'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_billing_wooccm14'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_billing_wooccm15'), None),
        },
        "metodoPago": request.data['payment_method_title'],
        "numeroPedido": request.data['number'],
        "articulos": articulos,
        "envios": request.data['shipping_lines'],
        "json": request.data,
        "canal": next((objeto['value'] for objeto in request.data['meta_data'] if
                       objeto["key"] == '_wc_order_attribution_session_entry'), None),
        "created_at": request.data['date_created'],
        "codigoVendedor": '',
    }
