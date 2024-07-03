
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

def capitalize_city(city_name):
    # Palabras que no deberían capitalizarse completamente, excepto si son la primera palabra
    exceptions = {"el", "la", "los", "las","un", "una", "unos", "unas", "de", "y"}

    # Divide la ciudad en palabras y procesa cada una condicionalmente
    words = city_name.lower().split()
    capitalized_words = [word if word in exceptions and i != 0 else word.capitalize() for i, word in enumerate(words)]

    # Une las palabras de nuevo en una cadena
    return ' '.join(capitalized_words)


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
            "ciudad": capitalize_city(request.data['billing']['city']),
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
            "ciudad": capitalize_city(request.data['shipping']['city']),
            "callePrincipal": request.data['shipping']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_shipping_wooccm9'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_shipping_wooccm10'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_shipping_wooccm11'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_shipping_wooccm12'), None),
            "canalEnvio": 'https://todomegacentro.megadescuento.com',
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
            "ciudad": capitalize_city(request.data['billing']['city']),
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
            "nombres": request.data['billing']['first_name'],
            "apellidos": request.data['billing']['last_name'],
            "correo": request.data['billing']['email'],
            "identificacion": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm12'), None),
            "telefono": request.data['billing']['company'],
            "pais": "Ecuador",
            "provincia": provincias[request.data['billing']['state']],
            "ciudad": capitalize_city(request.data['billing']['city']),
            "callePrincipal": request.data['billing']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm15'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm14'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_billing_wooccm13'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_billing_wooccm16'), None),
            "canalEnvio": 'https://todomegacentro.megadescuento.com',
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

    nombres = request.data['billing']['first_name']
    apellidos = request.data['billing']['last_name']
    correo = request.data['billing']['email']
    identificacion = next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm15'), None)
    telefono = request.data['billing']['company']
    pais = "Ecuador"
    provincia = provincias[request.data['billing']['state']]
    ciudad = capitalize_city(request.data['billing']['city'])
    callePrincipal = request.data['billing']['address_1']
    numero = next((objeto['value'] for objeto in request.data['meta_data'] if
                    objeto["key"] == '_billing_wooccm11'), None)
    calleSecundaria = next((objeto['value'] for objeto in request.data['meta_data'] if
                             objeto["key"] == '_billing_wooccm12'), None)
    referencia = next((objeto['value'] for objeto in request.data['meta_data'] if
                        objeto["key"] == '_billing_wooccm13'), None)
    gps = next((objeto['value'] for objeto in request.data['meta_data'] if
                 objeto["key"] == '_billing_wooccm14'), None)

    return {
        "estado": 'Pendiente',
        "envioTotal": request.data['shipping_total'],
        "total": total,
        "subtotal": total,
        "facturacion": {
            "nombres": nombres,
            "apellidos": apellidos,
            "correo": correo,
            "identificacion": identificacion,
            "telefono": telefono,
            "pais": pais,
            "provincia": provincia,
            "ciudad": ciudad,
            "callePrincipal": callePrincipal,
            "numero": numero,
            "calleSecundaria": calleSecundaria,
            "referencia": referencia,
            "gps": gps,
            "codigoVendedor": codigoVendedor,
            "nombreVendedor": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm17'), None),
            "correoVendedor": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm19'), None),
            "comprobantePago": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm18'), None),
        },
        "envio": {
            "nombres": nombres,
            "apellidos": apellidos,
            "correo": correo,
            "identificacion": identificacion,
            "telefono": telefono,
            "pais": pais,
            "provincia": provincia,
            "ciudad": ciudad,
            "callePrincipal": callePrincipal,
            "numero": numero,
            "calleSecundaria": calleSecundaria,
            "referencia": referencia,
            "gps": gps,
            "canalEnvio": 'https://mayorista.megadescuento.com/',
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
            "ciudad": capitalize_city(request.data['billing']['city']),
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
            "nombres": request.data['billing']['first_name'],
            "apellidos": request.data['billing']['last_name'],
            "correo": request.data['billing']['email'],
            "identificacion": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm13'), None),
            "telefono": request.data['billing']['company'],
            "pais": "Ecuador",
            "provincia": provincias[request.data['billing']['state']],
            "ciudad": capitalize_city(request.data['billing']['city']),
            "callePrincipal": request.data['billing']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm15'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm14'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_billing_wooccm13'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_billing_wooccm16'), None),
            "canalEnvio": 'https://mayorista.megadescuento.com/',
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
            "ciudad": capitalize_city(request.data['billing']['city']),
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
            "ciudad": capitalize_city(request.data['shipping']['city']),
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

    nombres = request.data['billing']['first_name']
    apellidos = request.data['billing']['last_name']
    correo = request.data['billing']['email']
    identificacion = next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm12'), None)
    telefono = request.data['billing']['company']
    pais = "Ecuador"
    provincia = provincias[request.data['billing']['state']]
    ciudad = capitalize_city(request.data['billing']['city'])
    callePrincipal = request.data['billing']['address_1']
    numero = next((objeto['value'] for objeto in request.data['meta_data'] if
                    objeto["key"] == '_billing_wooccm13'), None)
    calleSecundaria = next((objeto['value'] for objeto in request.data['meta_data'] if
                             objeto["key"] == '_billing_wooccm16'), None)
    referencia = next((objeto['value'] for objeto in request.data['meta_data'] if
                        objeto["key"] == '_billing_wooccm14'), None)
    gps = next((objeto['value'] for objeto in request.data['meta_data'] if
                 objeto["key"] == '_billing_wooccm15'), None)

    return {
        "estado": 'Pendiente',
        "envioTotal": request.data['shipping_total'],
        "total": total,
        "subtotal": total,
        "facturacion": {
            "nombres": nombres,
            "apellidos": apellidos,
            "correo": correo,
            "identificacion": identificacion,
            "telefono": telefono,
            "pais": pais,
            "provincia": provincia,
            "ciudad": ciudad,
            "callePrincipal": callePrincipal,
            "numero": numero,
            "calleSecundaria": calleSecundaria,
            "referencia": referencia,
            "gps": gps,
            "codigoVendedor": '',
            "nombreVendedor": '',
            "comprobantePago": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm11'), None),
        },
        "envio": {
            "nombres": nombres,
            "apellidos": apellidos,
            "correo": correo,
            "identificacion": identificacion,
            "telefono": telefono,
            "pais": pais,
            "provincia": provincia,
            "ciudad": ciudad,
            "callePrincipal": callePrincipal,
            "numero": numero,
            "calleSecundaria": calleSecundaria,
            "referencia": referencia,
            "gps": gps,
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

def mapeoTodoContraEntrega(request, articulos):
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
                                    objeto["key"] == '_billing_wooccm11'), None),
            "telefono": request.data['billing']['company'],
            "pais": "Ecuador",
            "provincia": provincias[request.data['billing']['state']],
            "ciudad": capitalize_city(request.data['billing']['city']),
            "callePrincipal": request.data['billing']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm12'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm13'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_billing_wooccm14'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_billing_wooccm15'), None),
            "codigoVendedor": codigoVendedor,
            "nombreVendedor": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm17'), None),
            "correoVendedor": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm19'), None),
            "comprobantePago": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm18'), None),
        },
        "envio": {
            "nombres": request.data['billing']['first_name'],
            "apellidos": request.data['billing']['last_name'],
            "correo": request.data['billing']['email'],
            "identificacion": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm11'), None),
            "telefono": request.data['billing']['company'],
            "pais": "Ecuador",
            "provincia": provincias[request.data['billing']['state']],
            "ciudad": capitalize_city(request.data['billing']['city']),
            "callePrincipal": request.data['billing']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm12'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm13'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_billing_wooccm14'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_billing_wooccm15'), None),
            "canalEnvio": 'https://contraentrega.megadescuento.com/',
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

def mapeoTodoTiendaMulticompras(request, articulos):
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
                                    objeto["key"] == '_billing_wooccm11'), None),
            "telefono": request.data['billing']['company'],
            "pais": "Ecuador",
            "provincia": provincias[request.data['billing']['state']],
            "ciudad": capitalize_city(request.data['billing']['city']),
            "callePrincipal": request.data['billing']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm12'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm13'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_billing_wooccm14'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_billing_wooccm15'), None),
            "codigoVendedor": codigoVendedor,
            "nombreVendedor": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm17'), None),
            "correoVendedor": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_address_2'), None),
            "comprobantePago": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_postcode'), None),
        },
        "envio": {
            "nombres": request.data['shipping']['first_name'],
            "apellidos": request.data['shipping']['last_name'],
            "correo": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_shipping_wooccm9'), None),
            "identificacion": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_shipping_wooccm10'), None),
            "telefono": next((objeto['value'] for objeto in request.data['meta_data'] if
                              objeto["key"] == '_shipping_wooccm11'), None),
            "pais": "Ecuador",
            "provincia": provincias[request.data['shipping']['state']],
            "ciudad": capitalize_city(request.data['shipping']['city']),
            "callePrincipal": request.data['shipping']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_shipping_wooccm12'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_shipping_wooccm13'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_shipping_wooccm14'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_shipping_wooccm15'), None),
            "canalEnvio": 'https://tiendamulticompras.megadescuento.com',
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

def mapeoTodoMaxiDescuento(request, articulos):
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
                                    objeto["key"] == '_billing_wooccm11'), None),
            "telefono": request.data['billing']['company'],
            "pais": "Ecuador",
            "provincia": provincias[request.data['billing']['state']],
            "ciudad": capitalize_city(request.data['billing']['city']),
            "callePrincipal": request.data['billing']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm18'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm12'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_billing_wooccm13'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_billing_wooccm14'), None),
            "codigoVendedor": codigoVendedor,
            "nombreVendedor": '',
            "correoVendedor": '',
            "comprobantePago": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm17'), None),
        },
        "envio": {
            "nombres": request.data['billing']['first_name'],
            "apellidos": request.data['billing']['last_name'],
            "correo": request.data['billing']['email'],
            "identificacion": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm11'), None),
            "telefono": request.data['billing']['company'],
            "pais": "Ecuador",
            "provincia": provincias[request.data['billing']['state']],
            "ciudad": capitalize_city(request.data['billing']['city']),
            "callePrincipal": request.data['billing']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm18'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm12'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_billing_wooccm13'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_billing_wooccm14'), None),
            "canalEnvio": 'https://maxidescuento.megadescuento.com',
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

def mapeoTodoMegaBahia(request, articulos):
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
                                    objeto["key"] == '_billing_wooccm11'), None),
            "telefono": request.data['billing']['company'],
            "pais": "Ecuador",
            "provincia": provincias[request.data['billing']['state']],
            "ciudad": capitalize_city(request.data['billing']['city']),
            "callePrincipal": request.data['billing']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm12'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm13'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_billing_wooccm14'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_billing_wooccm15'), None),
            "codigoVendedor": '',
            "nombreVendedor": '',
            "correoVendedor": '',
            "comprobantePago": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm18'), None),
        },
        "envio": {
            "nombres": request.data['billing']['first_name'],
            "apellidos": request.data['billing']['last_name'],
            "correo": request.data['billing']['email'],
            "identificacion": next((objeto['value'] for objeto in request.data['meta_data'] if
                                    objeto["key"] == '_billing_wooccm11'), None),
            "telefono": request.data['billing']['company'],
            "pais": "Ecuador",
            "provincia": provincias[request.data['billing']['state']],
            "ciudad": capitalize_city(request.data['billing']['city']),
            "callePrincipal": request.data['billing']['address_1'],
            "numero": next((objeto['value'] for objeto in request.data['meta_data'] if
                            objeto["key"] == '_billing_wooccm12'), None),
            "calleSecundaria": next((objeto['value'] for objeto in request.data['meta_data'] if
                                     objeto["key"] == '_billing_wooccm13'), None),
            "referencia": next((objeto['value'] for objeto in request.data['meta_data'] if
                                objeto["key"] == '_billing_wooccm14'), None),
            "gps": next((objeto['value'] for objeto in request.data['meta_data'] if
                         objeto["key"] == '_billing_wooccm15'), None),
            "canalEnvio": 'https://megabahia.megadescuento.com/',
        },
        "metodoPago": request.data['payment_method_title'],
        "numeroPedido": request.data['number'],
        "articulos": articulos,
        "envios": request.data['shipping_lines'],
        "json": request.data,
        "canal": request.data['_links']['collection'][0]['href'],
        "created_at": request.data['date_created'],
        "codigoVendedor": '',
    }

def mapeoCrearProductoWoocommerce(request, stock_nuevo, canal_pedido, fecha):

    productos_procesados={}
    index = canal_pedido.find('.com')
    if index != -1:
        canal = canal_pedido[:index + 4]
    else:
        canal = canal_pedido

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
        "todomegacentro.megadescuento.com",
        "superbarato.megadescuento.com"
    ]
    print('STOCK', stock_nuevo)
    # Generar la lista stockVirtual comparando el canal extraído con la lista de canales
    stock_virtual = [{"canal": sv_canal, "estado": sv_canal == canal} for sv_canal in canales_stock_virtual]
    for prod in request:
        productos_procesados = {
            "woocommerceId": int(prod['product_id']),
            "nombre": prod['name'],
            "codigoBarras": prod['sku'],
            "stock": stock_nuevo,
            "costoCompra": float(prod['price']),
            "precioVentaA": float(prod['price']),
            "precioVentaB": float(prod['price']),
            "precioVentaC": 0,
            "precioVentaD": 0,
            "precioVentaE": 0,
            "precioVentaF": 0,
            "precioVentaBultos":0,
            "canal": canal,
            "estado": 'Activo',
            "created_at": fecha,
            "stockVirtual": stock_virtual,
        }

    return productos_procesados
