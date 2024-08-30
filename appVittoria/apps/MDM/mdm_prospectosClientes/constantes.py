
def mapeoProspectoCliente(data, articulos):
    total = data['total']
    return {
        "estado": 'Pendiente',
        "envioTotal": 0,
        "total": data['total'],
        "subtotal": data['total'],
        "facturacion": {
            "nombres": data['nombres'],
            "apellidos": data['apellidos'],
            "correo": data['correo1'],
            "identificacion": data['identificacion'],
            "telefono": data['whatsapp'],
            "pais": data['pais'],
            "provincia": data['provincia'],
            "ciudad": data['ciudad'],
            "callePrincipal": data['callePrincipal'],
            "numero": data['numeroCasa'],
            "calleSecundaria": data['calleSecundaria'],
            "referencia": data['referencia'],
            "gps": '',
            "codigoVendedor": 'nombreVendedor',
            "nombreVendedor": 'nombreVendedor',
            "correoVendedor": '',
            "comprobantePago": '',
        },
        "envio": {
            "nombres": data['nombres'],
            "apellidos": data['apellidos'],
            "correo": data['correo1'],
            "identificacion": data['identificacion'],
            "telefono": data['whatsapp'],
            "pais": data['pais'],
            "provincia": data['provincia'],
            "ciudad": data['ciudad'],
            "callePrincipal": data['callePrincipal'],
            "numero": data['numeroCasa'],
            "calleSecundaria": data['calleSecundaria'],
            "referencia": data['referencia'],
            "gps": '',
            "canalEnvio": data['canal'],
        },
        "metodoPago": data['metodoPago'],
        "numeroPedido": data['id'],
        "articulos": articulos,
        "envios": data,
        "json": data,
        "canal": data['canalOrigen'],
        "created_at": data['created_at'],
        "fechaHoraConfirmacion": data['updated_at'],
        "codigoVendedor": None,
        "gestion_pedido": "omniglobal"
    }

