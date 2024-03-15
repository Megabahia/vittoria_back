from ...ADM.vittoria_usuarios.models import Usuarios
from ...config.util import sendEmail


def enviarCorreoVendedor(data):
    usuario = Usuarios.objects.filter(username=data['facturacion']['codigoVendedor'].upper()).first()

    if usuario and 'Vendedor' == usuario.idRol.nombre:
        subject, from_email, to = 'Solicitud de Pedido', "08d77fe1da-d09822@inbox.mailtrap.io", usuario.email
        txt_content = f"""
                Registro de Pedido
                Se ha generado un pedido a su nombre {usuario.nombres} {usuario.apellidos}
                Atentamente,
                Equipo Vittoria.
        """

        articulos = ""

        for item in data['articulos']:
            articulos += f"""
                <tr>
                    <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                        {item['articulo']}
                    </td>
                    <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                        {item['cantidad']} </td>
                    <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                        <span><span>$</span>{item['precio']}</span>
                    </td>
                </tr>
            """

        html_content = f"""
        <html>
            <body>
                <div id="m_-2286063398718872391template_header_image">
                    <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:100%;margin-left:0px;margin-right:0px"></p>
                </div>
                <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_container" style="border:1px solid rgb(222,222,222);border-radius:3px;background-color:rgb(255,255,255)">
                <tbody>
                <tr>
                    <td align="center" valign="top">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_header" style="border-bottom:0px;font-weight:bold;line-height:100%;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;border-radius:3px 3px 0px 0px;color:rgb(255,255,255);background-color:rgb(35,85,225)">
                            <tbody>
                            <tr>
                                <td id="m_-2286063398718872391header_wrapper" style="padding:36px 48px;display:block">
                                    <h1 style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:30px;font-weight:300;line-height:150%;margin:0px;text-align:left;color:rgb(255,255,255)">
                                        Se ha generado su pedido.
                                    </h1>
                                </td>
                            </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td align="center" valign="top">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_body">
                            <tbody>
                            <tr>
                                <td valign="top" id="m_-2286063398718872391body_content" style="background-color:rgb(255,255,255)">
                                    <table border="0" cellpadding="20" cellspacing="0" width="100%">
                                        <tbody>
                                        <tr>
                                            <td valign="top" style="padding:48px 48px 32px">
                                                <div id="m_-2286063398718872391body_content_inner" align="left" style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:14px;line-height:150%;text-align:left;color:rgb(99,99,99)">
                                                    <p style="margin:0 0 16px">Hola {usuario.nombres} {usuario.apellidos},</p>
                                                    <p style="margin:0 0 16px">Se ha generado su pedido.</p>
                                                    <p style="margin:0 0 16px">Está en espera hasta que confirmemos que se ha recibido el pago.</p>
                                                    <h2 style="display:block;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:18px;font-weight:bold;line-height:130%;margin:0px 0px 18px;text-align:left;color:rgb(35,85,225)">
                                                        [Pedido #{data['numeroPedido']}] ({data['created_at']})</h2>
                                                    <div style="margin-bottom:40px">
                                                        <table cellspacing="0" cellpadding="6" border="1" width="100%" style="border:1px solid rgb(229,229,229);vertical-align:middle;width:100%;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                                                            <thead>
                                                            <tr>
                                                                <th scope="col" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    Producto</th>
                                                                <th scope="col" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    Cantidad</th>
                                                                <th scope="col" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    Precio a pagar por cliente</th>
                                                            </tr>
                                                            </thead>
                                                            <tbody>
                                                            {articulos}
                                                            </tbody>
                                                            <tfoot>
                                                            <tr>
                                                                <th scope="row" colspan="2" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    Métodos de pago:</th>
                                                                <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    {data['metodoPago']}</td>
                                                            </tr>
                                                            <tr>
                                                                <th scope="row" colspan="2" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    Total a pagar por el cliente:</th>
                                                                <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    <span><span>$</span>{data['total']}</span></td>
                                                            </tr>
                                                            </tfoot>
                                                        </table>
                                                    </div>
                                                    <table id="m_-2286063398718872391addresses" cellspacing="0" cellpadding="0" border="0" width="100%" style="width:100%;vertical-align:top;margin-bottom:40px;padding:0">
                                                        <tbody>
                                                        <tr>
                                                            <td valign="top" width="50%" align="left" style="text-align:left;font-family:'Helvetica Neue',Helvetica,Roboto,Arial,sans-serif;border:0;padding:0">
                                                                <h2 style="display:block;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:18px;font-weight:bold;line-height:130%;margin:0px 0px 18px;text-align:left;color:rgb(35,85,225)">
                                                                    Datos de facturación</h2>
                                                                <address style="padding:12px;border:1px solid rgb(229,229,229);color:rgb(99,99,99)">
                                                                    {data['facturacion']['nombres']} {data['facturacion']['apellidos']}<br>
                                                                    {data['facturacion']['correo']}<br>
                                                                    {data['facturacion']['identificacion']}<br>
                                                                    {data['facturacion']['telefono']}<br>
                                                                    {data['facturacion']['pais']}<br>
                                                                    {data['facturacion']['provincia']}<br>
                                                                    {data['facturacion']['ciudad']}<br>
                                                                    {data['facturacion']['callePrincipal']}<br>
                                                                    {data['facturacion']['numero']}<br>
                                                                    {data['facturacion']['calleSecundaria']}<br>
                                                                    {data['facturacion']['referencia']} <br>
                                                                    <a href="mailto:{data['facturacion']['correo']}" target="_blank">{data['facturacion']['correo']}</a> </address>
                                                            </td>
                                                            <td valign="top" width="50%" align="left" style="text-align:left;font-family:'Helvetica Neue',Helvetica,Roboto,Arial,sans-serif;padding:0">
                                                                <h2 style="display:block;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:18px;font-weight:bold;line-height:130%;margin:0px 0px 18px;text-align:left;color:rgb(35,85,225)">
                                                                    Datos de envío</h2>
                                                                <address style="padding:12px;border:1px solid rgb(229,229,229);color:rgb(99,99,99)">
                                                                    {data['envio']['nombres']} {data['envio']['apellidos']}<br>
                                                                    {data['envio']['correo']}<br>
                                                                    {data['envio']['identificacion']}<br>
                                                                    {data['envio']['telefono']}<br>
                                                                    {data['envio']['pais']}<br>
                                                                    {data['envio']['provincia']}<br>
                                                                    {data['envio']['ciudad']}<br>
                                                                    {data['envio']['callePrincipal']}<br>
                                                                    {data['envio']['numero']}<br>
                                                                    {data['envio']['calleSecundaria']}<br>
                                                                    {data['envio']['referencia']} </address>
                                                            </td>
                                                        </tr>
                                                        </tbody>
                                                    </table>
                                                    <p style="margin:0 0 16px">Esperamos poder cumplir pronto tu pedido.</p>
                                                </div>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </td>
                            </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
                </tbody>
            </table>
            </body>
        </html>
        """
        sendEmail(subject, txt_content, from_email, to, html_content)


def enviarCorreoCliente(data):
    subject, from_email, to = f"Su pedido {data['numeroPedido']} ha sido empacado", "08d77fe1da-d09822@inbox.mailtrap.io", data['facturacion'][
        'correo']
    txt_content = f"""
            Registro de Pedido
            Se ha generado un pedido a su nombre {data['facturacion']['nombres']} {data['facturacion']['apellidos']}
            Su pedido ha sido enviado en pocos momentos sera despachado.
            Atentamente,
            Equipo Vittoria.
    """

    articulos = ""

    for item in data['articulos']:
        articulos += f"""
            <tr>
                <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                    {item['articulo']}
                </td>
                <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                    {item['cantidad']} </td>
                <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                    <span><span>$</span>{item['precio']}</span>
                </td>
            </tr>
        """

    html_content = f"""
    <html>
        <body>
            <div id="m_-2286063398718872391template_header_image">
                <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:100%;margin-left:0px;margin-right:0px"></p>
            </div>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_container" style="border:1px solid rgb(222,222,222);border-radius:3px;background-color:rgb(255,255,255)">
            <tbody>
            <tr>
                <td align="center" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_header" style="border-bottom:0px;font-weight:bold;line-height:100%;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;border-radius:3px 3px 0px 0px;color:rgb(255,255,255);background-color:rgb(35,85,225)">
                        <tbody>
                        <tr>
                            <td id="m_-2286063398718872391header_wrapper" style="padding:36px 48px;display:block">
                                <h1 style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:30px;font-weight:300;line-height:150%;margin:0px;text-align:left;color:rgb(255,255,255)">
                                    Hola {data['facturacion']['nombres']} {data['facturacion']['apellidos']}
                                </h1>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
            <tr>
                <td align="center" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_body">
                        <tbody>
                        <tr>
                            <td valign="top" id="m_-2286063398718872391body_content" style="background-color:rgb(255,255,255)">
                                <table border="0" cellpadding="20" cellspacing="0" width="100%">
                                    <tbody>
                                    <tr>
                                        <td valign="top" style="padding:48px 48px 32px">
                                            <div id="m_-2286063398718872391body_content_inner" align="left" style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:14px;line-height:150%;text-align:left;color:rgb(99,99,99)">
                                                <p style="margin:0 0 16px">Su pedido ha sido empacado.</p>
                                                <p style="margin:0 0 16px">Aquí están las evidencias de su pedido esta empacado.</p>
                                                <br>
                                                <a href="{data['fotoEmpaque']}" target="_blank">Foto del empaque</a>
                                                <br>
                                                <p style="margin:0 0 16px">Si no puede visualizar copie y pegue el link:</p>
                                                <br>
                                                {data['fotoEmpaque']}
                                                <br>
                                                { '' if data['videoEmpaque'] is None else f'<br><a href="{data["videoEmpaque"]}" target="_blank">Video del empaque</a><br>' }
                                                { '' if data['videoEmpaque'] is None else f'Si no puede visualizar copie y pegue el link:<br>{data["videoEmpaque"]}<br>' }
                                                <h2 style="display:block;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:18px;font-weight:bold;line-height:130%;margin:0px 0px 18px;text-align:left;color:rgb(35,85,225)">
                                                    [Pedido #{data['numeroPedido']}] ({data['created_at']})</h2>
                                                <div style="margin-bottom:40px">
                                                    <table cellspacing="0" cellpadding="6" border="1" width="100%" style="border:1px solid rgb(229,229,229);vertical-align:middle;width:100%;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                                                        <thead>
                                                        <tr>
                                                            <th scope="col" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                Producto</th>
                                                            <th scope="col" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                Cantidad</th>
                                                            <th scope="col" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                Precio a pagar por cliente</th>
                                                        </tr>
                                                        </thead>
                                                        <tbody>
                                                        {articulos}
                                                        </tbody>
                                                        <tfoot>
                                                        <tr>
                                                            <th scope="row" colspan="2" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                Métodos de pago:</th>
                                                            <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                {data['metodoPago']}</td>
                                                        </tr>
                                                        <tr>
                                                            <th scope="row" colspan="2" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                Total a pagar por el cliente:</th>
                                                            <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                <span><span>$</span>{data['total']}</span></td>
                                                        </tr>
                                                        </tfoot>
                                                    </table>
                                                </div>
                                                <table id="m_-2286063398718872391addresses" cellspacing="0" cellpadding="0" border="0" width="100%" style="width:100%;vertical-align:top;margin-bottom:40px;padding:0">
                                                    <tbody>
                                                    <tr>
                                                        <td valign="top" width="50%" align="left" style="text-align:left;font-family:'Helvetica Neue',Helvetica,Roboto,Arial,sans-serif;padding:0">
                                                            <h2 style="display:block;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:18px;font-weight:bold;line-height:130%;margin:0px 0px 18px;text-align:left;color:rgb(35,85,225)">
                                                                Datos de envío</h2>
                                                            <address style="padding:12px;border:1px solid rgb(229,229,229);color:rgb(99,99,99)">
                                                                {data['envio']['nombres']} {data['envio']['apellidos']}<br>
                                                                {data['envio']['correo']}<br>
                                                                {data['envio']['identificacion']}<br>
                                                                {data['envio']['telefono']}<br>
                                                                {data['envio']['pais']}<br>
                                                                {data['envio']['provincia']}<br>
                                                                {data['envio']['ciudad']}<br>
                                                                {data['envio']['callePrincipal']}<br>
                                                                {data['envio']['numero']}<br>
                                                                {data['envio']['calleSecundaria']}<br>
                                                                {data['envio']['referencia']} </address>
                                                        </td>
                                                    </tr>
                                                    </tbody>
                                                </table>
                                                <p style="margin:0 0 16px; color: red;">
                                                En un momento su pedido será despachado a traves del courier. Enseguida recibiría un correo con la foto de la guía de entrega del courier.
                                                </p>
                                            </div>
                                        </td>
                                    </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
            </tbody>
        </table>
        </body>
    </html>
    """
    sendEmail(subject, txt_content, from_email, to, html_content)


def enviarCorreoClienteDespacho(data):
    subject, from_email, to = f"Su pedido {data['numeroPedido']} ha sido despachado", "08d77fe1da-d09822@inbox.mailtrap.io", data['envio']['correo']
    txt_content = f"""
            Registro de Pedido
            Hola aqui tienes el link del archivo de guia {data['archivoGuia']}
            Atentamente,
            Equipo Vittoria.
    """

    articulos = ""

    for item in data['articulos']:
        articulos += f"""
            <tr>
                <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                    {item['articulo']}
                    <ul style="font-size:small;margin:1em 0 0;padding:0;list-style:none">
                        <li style="margin:.5em 0 0;padding:0"><strong style="float:left;margin-right:.25em;clear:both">Precio:</strong>
                            <p style="margin:0">{item['valorUnitario']} unidad</p>
                        </li>
                    </li></ul>
                </td>
                <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                    {item['cantidad']} </td>
                <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                    <span><span>$</span>{item['precio']}</span>
                </td>
            </tr>
        """

    html_content = f"""
    <html>
        <body>
            <div id="m_-2286063398718872391template_header_image">
                <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:100%;margin-left:0px;margin-right:0px"></p>
            </div>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_container" style="border:1px solid rgb(222,222,222);border-radius:3px;background-color:rgb(255,255,255)">
            <tbody>
            <tr>
                <td align="center" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_header" style="border-bottom:0px;font-weight:bold;line-height:100%;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;border-radius:3px 3px 0px 0px;color:rgb(255,255,255);background-color:rgb(35,85,225)">
                        <tbody>
                        <tr>
                            <td id="m_-2286063398718872391header_wrapper" style="padding:36px 48px;display:block">
                                <h1 style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:30px;font-weight:300;line-height:150%;margin:0px;text-align:left;color:rgb(255,255,255)">
                                    Hola {data['facturacion']['nombres']} {data['facturacion']['apellidos']}
                                </h1>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
            <tr>
                <td align="center" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_body">
                        <tbody>
                        <tr>
                            <td valign="top" id="m_-2286063398718872391body_content" style="background-color:rgb(255,255,255)">
                                <table border="0" cellpadding="20" cellspacing="0" width="100%">
                                    <tbody>
                                    <tr>
                                        <td valign="top" style="padding:48px 48px 32px">
                                            <div id="m_-2286063398718872391body_content_inner" align="left" style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:14px;line-height:150%;text-align:left;color:rgb(99,99,99)">
                                                <p style="margin:0 0 16px">Hola aqui tienes el link del archivo de guia</p>
                                                <br>
                                                <a href="{data['archivoGuia']}" target="_blank">Ver archivo</a>
                                                <br>
                                                <p style="margin:0 0 16px">Si no puede visualizar copie y pegue el link:</p>
                                                <br>
                                                {data['archivoGuia']}
                                                <br>
                                                <h2 style="display:block;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:18px;font-weight:bold;line-height:130%;margin:0px 0px 18px;text-align:left;color:rgb(35,85,225)">
                                                    [Pedido #{data['numeroPedido']}] ({data['created_at']})</h2>
                                                <div style="margin-bottom:40px">
                                                    <table cellspacing="0" cellpadding="6" border="1" width="100%" style="border:1px solid rgb(229,229,229);vertical-align:middle;width:100%;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                                                        <thead>
                                                        <tr>
                                                            <th scope="col" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                Producto</th>
                                                            <th scope="col" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                Cantidad</th>
                                                            <th scope="col" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                Precio a pagar por cliente</th>
                                                        </tr>
                                                        </thead>
                                                        <tbody>
                                                        {articulos}
                                                        </tbody>
                                                        <tfoot>
                                                        <tr>
                                                            <th scope="row" colspan="2" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                Métodos de pago:</th>
                                                            <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                {data['metodoPago']}</td>
                                                        </tr>
                                                        <tr>
                                                            <th scope="row" colspan="2" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                Total a pagar por el cliente:</th>
                                                            <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                <span><span>$</span>{data['total']}</span></td>
                                                        </tr>
                                                        </tfoot>
                                                    </table>
                                                </div>
                                                <table id="m_-2286063398718872391addresses" cellspacing="0" cellpadding="0" border="0" width="100%" style="width:100%;vertical-align:top;margin-bottom:40px;padding:0">
                                                    <tbody>
                                                    <tr>
                                                        <td valign="top" width="50%" align="left" style="text-align:left;font-family:'Helvetica Neue',Helvetica,Roboto,Arial,sans-serif;padding:0">
                                                            <h2 style="display:block;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:18px;font-weight:bold;line-height:130%;margin:0px 0px 18px;text-align:left;color:rgb(35,85,225)">
                                                                Datos de envío</h2>
                                                            <address style="padding:12px;border:1px solid rgb(229,229,229);color:rgb(99,99,99)">
                                                                {data['envio']['nombres']} {data['envio']['apellidos']}<br>
                                                                {data['envio']['correo']}<br>
                                                                {data['envio']['identificacion']}<br>
                                                                {data['envio']['telefono']}<br>
                                                                {data['envio']['pais']}<br>
                                                                {data['envio']['provincia']}<br>
                                                                {data['envio']['ciudad']}<br>
                                                                {data['envio']['callePrincipal']}<br>
                                                                {data['envio']['numero']}<br>
                                                                {data['envio']['calleSecundaria']}<br>
                                                                {data['envio']['referencia']} </address>
                                                        </td>
                                                    </tr>
                                                    </tbody>
                                                </table>
                                                <p style="margin:0 0 16px">Esperamos poder cumplir pronto tu pedido.</p>
                                            </div>
                                        </td>
                                    </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
            </tbody>
        </table>
        </body>
    </html>
    """
    sendEmail(subject, txt_content, from_email, to, html_content)


def enviarCorreoCourierDespacho(data):
    subject, from_email, to = f"Su pedido {data['numeroPedido']} ha sido despachado", "08d77fe1da-d09822@inbox.mailtrap.io", data['correoCourier']
    txt_content = f"""
            Registro de Pedido
            Se ha generado un pedido a su nombre {data['facturacion']['nombres']} {data['facturacion']['apellidos']}
            Su pedido ha sido enviado en pocos momentos sera despachado.
            Atentamente,
            Equipo Vittoria.
    """

    html_content = f"""
    <html>
        <body>
            <div id="m_-2286063398718872391template_header_image">
                <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:100%;margin-left:0px;margin-right:0px"></p>
            </div>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_container" style="border:1px solid rgb(222,222,222);border-radius:3px;background-color:rgb(255,255,255)">
            <tbody>
            <tr>
                <td align="center" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_header" style="border-bottom:0px;font-weight:bold;line-height:100%;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;border-radius:3px 3px 0px 0px;color:rgb(255,255,255);background-color:rgb(35,85,225)">
                        <tbody>
                        <tr>
                            <td id="m_-2286063398718872391header_wrapper" style="padding:36px 48px;display:block">
                                <h1 style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:30px;font-weight:300;line-height:150%;margin:0px;text-align:left;color:rgb(255,255,255)">
                                    Hola {data['nombreCourier']}
                                </h1>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
            <tr>
                <td align="center" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_body">
                        <tbody>
                        <tr>
                            <td valign="top" id="m_-2286063398718872391body_content" style="background-color:rgb(255,255,255)">
                                <table border="0" cellpadding="20" cellspacing="0" width="100%">
                                    <tbody>
                                    <tr>
                                        <td valign="top" style="padding:48px 48px 32px">
                                            <div id="m_-2286063398718872391body_content_inner" align="left" style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:14px;line-height:150%;text-align:left;color:rgb(99,99,99)">
                                                <p style="margin:0 0 16px">Hola aqui tienes el link del archivo de guia</p>
                                                <br>
                                                <a href="{data['archivoGuia']}" target="_blank">Ver archivo</a>
                                                <br>
                                                <p style="margin:0 0 16px">Hola aqui tienes el link del gps</p>
                                                <br>
                                                {'No hay ubicacion' if data['facturacion']['gps'] is None else f'<a href="{data["facturacion"]["gps"]}" target="_blank">Ver</a>'}
                                                <br>
                                                <p style="margin:0 0 16px">Ingresa al siguiente link e ingresa las evidencias de la entrega</p>
                                                https://vittoria-test.netlify.app/#/gde/gestionEntrega/woocommerce/enviado
                                            </div>
                                        </td>
                                    </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
            </tbody>
        </table>
        </body>
    </html>
    """
    sendEmail(subject, txt_content, from_email, to, html_content)


def enviarCorreoVendedorDespacho(data):
    usuario = Usuarios.objects.filter(username=data['facturacion']['codigoVendedor'].upper()).first()

    if usuario and 'Vendedor' == usuario.idRol.nombre:
        subject, from_email, to = f"Su pedido {data['numeroPedido']} ha sido despachado", "08d77fe1da-d09822@inbox.mailtrap.io", usuario.email
        txt_content = f"""
                Registro de Pedido
                Se ha generado un pedido a su nombre {data['facturacion']['nombres']} {data['facturacion']['apellidos']}
                Su pedido ha sido enviado en pocos momentos sera despachado.
                Atentamente,
                Equipo Vittoria.
        """

        html_content = f"""
        <html>
            <body>
                <div id="m_-2286063398718872391template_header_image">
                    <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:100%;margin-left:0px;margin-right:0px"></p>
                </div>
                <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_container" style="border:1px solid rgb(222,222,222);border-radius:3px;background-color:rgb(255,255,255)">
                <tbody>
                <tr>
                    <td align="center" valign="top">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_header" style="border-bottom:0px;font-weight:bold;line-height:100%;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;border-radius:3px 3px 0px 0px;color:rgb(255,255,255);background-color:rgb(35,85,225)">
                            <tbody>
                            <tr>
                                <td id="m_-2286063398718872391header_wrapper" style="padding:36px 48px;display:block">
                                    <h1 style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:30px;font-weight:300;line-height:150%;margin:0px;text-align:left;color:rgb(255,255,255)">
                                        Hola {usuario.nombres} {usuario.apellidos}
                                    </h1>
                                </td>
                            </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td align="center" valign="top">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_body">
                            <tbody>
                            <tr>
                                <td valign="top" id="m_-2286063398718872391body_content" style="background-color:rgb(255,255,255)">
                                    <table border="0" cellpadding="20" cellspacing="0" width="100%">
                                        <tbody>
                                        <tr>
                                            <td valign="top" style="padding:48px 48px 32px">
                                                <div id="m_-2286063398718872391body_content_inner" align="left" style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:14px;line-height:150%;text-align:left;color:rgb(99,99,99)">
                                                    <p style="margin:0 0 16px">Hola aqui tienes el link del archivo de guia {data['archivoGuia']}</p>
                                                    
                                                    <p style="margin:0 0 16px">Esperamos poder cumplir pronto tu pedido.</p>
                                                </div>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </td>
                            </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
                </tbody>
            </table>
            </body>
        </html>
        """
        sendEmail(subject, txt_content, from_email, to, html_content)


def enviarCorreoClienteRechazado(data):
    subject, from_email, to = 'Envio de despacho', "08d77fe1da-d09822@inbox.mailtrap.io", data['envio']['correo']
    txt_content = f"""
            Registro de Pedido
            Hola aqui tienes el link del archivo de guia {data['archivoGuia']}
            Atentamente,
            Equipo Vittoria.
    """

    articulos = ""

    for item in data['articulos']:
        articulos += f"""
            <tr>
                <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                    {item['articulo']}
                    <ul style="font-size:small;margin:1em 0 0;padding:0;list-style:none">
                        <li style="margin:.5em 0 0;padding:0"><strong style="float:left;margin-right:.25em;clear:both">Precio:</strong>
                            <p style="margin:0">{item['valorUnitario']} unidad</p>
                        </li>
                    </li></ul>
                </td>
                <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                    {item['cantidad']} </td>
                <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                    <span><span>$</span>{item['precio']}</span>
                </td>
            </tr>
        """

    html_content = f"""
    <html>
        <body>
            <div id="m_-2286063398718872391template_header_image">
                <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:100%;margin-left:0px;margin-right:0px"></p>
            </div>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_container" style="border:1px solid rgb(222,222,222);border-radius:3px;background-color:rgb(255,255,255)">
            <tbody>
            <tr>
                <td align="center" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_header" style="border-bottom:0px;font-weight:bold;line-height:100%;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;border-radius:3px 3px 0px 0px;color:rgb(255,255,255);background-color:rgb(35,85,225)">
                        <tbody>
                        <tr>
                            <td id="m_-2286063398718872391header_wrapper" style="padding:36px 48px;display:block">
                                <h1 style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:30px;font-weight:300;line-height:150%;margin:0px;text-align:left;color:rgb(255,255,255)">
                                    Hola su pedido ha sido rechazado por:
                                </h1>
                                <h1 style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:30px;font-weight:300;line-height:150%;margin:0px;text-align:left;color:rgb(255,255,255)">
                                    {data['motivo']}
                                </h1>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
            <tr>
                <td align="center" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_body">
                        <tbody>
                        <tr>
                            <td valign="top" id="m_-2286063398718872391body_content" style="background-color:rgb(255,255,255)">
                                <table border="0" cellpadding="20" cellspacing="0" width="100%">
                                    <tbody>
                                    <tr>
                                        <td valign="top" style="padding:48px 48px 32px">
                                            <div id="m_-2286063398718872391body_content_inner" align="left" style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:14px;line-height:150%;text-align:left;color:rgb(99,99,99)">
                                                <p style="margin:0 0 16px">Hola {data['facturacion']['nombres']} {data['facturacion']['apellidos']},</p>
                                                <p style="margin:0 0 16px">Se ha generado un pedido. Está en espera hasta que confirmemos que se ha recibido el pago.</p>
                                                <h2 style="display:block;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:18px;font-weight:bold;line-height:130%;margin:0px 0px 18px;text-align:left;color:rgb(35,85,225)">
                                                    [Pedido #{data['numeroPedido']}] ({data['created_at']})</h2>
                                                <div style="margin-bottom:40px">
                                                    <table cellspacing="0" cellpadding="6" border="1" width="100%" style="border:1px solid rgb(229,229,229);vertical-align:middle;width:100%;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                                                        <thead>
                                                        <tr>
                                                            <th scope="col" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                Producto</th>
                                                            <th scope="col" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                Cantidad</th>
                                                            <th scope="col" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                Precio</th>
                                                        </tr>
                                                        </thead>
                                                        <tbody>
                                                        {articulos}
                                                        </tbody>
                                                        <tfoot>
                                                        <tr>
                                                            <th scope="row" colspan="2" align="left" style="border-width:4px 1px 1px;border-style:solid;border-color:rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                Subtotal:</th>
                                                            <td align="left" style="border-width:4px 1px 1px;border-style:solid;border-color:rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                <span><span>$</span>{data['subtotal']}</span></td>
                                                        </tr>
                                                        <tr>
                                                            <th scope="row" colspan="2" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                Envío:</th>
                                                            <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                <span><span>$</span>5.00</span>&nbsp;<small>vía Cantonal</small>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <th scope="row" colspan="2" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                Métodos de pago:</th>
                                                            <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                {data['metodoPago']}</td>
                                                        </tr>
                                                        <tr>
                                                            <th scope="row" colspan="2" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                Total:</th>
                                                            <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                <span><span>$</span>{data['total']}</span></td>
                                                        </tr>
                                                        </tfoot>
                                                    </table>
                                                </div>
                                                <table id="m_-2286063398718872391addresses" cellspacing="0" cellpadding="0" border="0" width="100%" style="width:100%;vertical-align:top;margin-bottom:40px;padding:0">
                                                    <tbody>
                                                    <tr>
                                                        <td valign="top" width="50%" align="left" style="text-align:left;font-family:'Helvetica Neue',Helvetica,Roboto,Arial,sans-serif;border:0;padding:0">
                                                            <h2 style="display:block;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:18px;font-weight:bold;line-height:130%;margin:0px 0px 18px;text-align:left;color:rgb(35,85,225)">
                                                                Datos de facturación</h2>
                                                            <address style="padding:12px;border:1px solid rgb(229,229,229);color:rgb(99,99,99)">
                                                                {data['facturacion']['nombres']} {data['facturacion']['apellidos']}<br>
                                                                    {data['facturacion']['correo']}<br>
                                                                    {data['facturacion']['identificacion']}<br>
                                                                    {data['facturacion']['telefono']}<br>
                                                                    {data['facturacion']['pais']}<br>
                                                                    {data['facturacion']['provincia']}<br>
                                                                    {data['facturacion']['ciudad']}<br>
                                                                    {data['facturacion']['callePrincipal']}<br>
                                                                    {data['facturacion']['numero']}<br>
                                                                    {data['facturacion']['calleSecundaria']}<br>
                                                                    {data['facturacion']['referencia']} <br>
                                                                <a href="mailto:{data['facturacion']['correo']}" target="_blank">{data['facturacion']['correo']}</a> </address>
                                                        </td>
                                                        <td valign="top" width="50%" align="left" style="text-align:left;font-family:'Helvetica Neue',Helvetica,Roboto,Arial,sans-serif;padding:0">
                                                            <h2 style="display:block;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:18px;font-weight:bold;line-height:130%;margin:0px 0px 18px;text-align:left;color:rgb(35,85,225)">
                                                                Datos de envío</h2>
                                                            <address style="padding:12px;border:1px solid rgb(229,229,229);color:rgb(99,99,99)">
                                                                {data['envio']['nombres']} {data['envio']['apellidos']}<br>
                                                                {data['envio']['correo']}<br>
                                                                {data['envio']['identificacion']}<br>
                                                                {data['envio']['telefono']}<br>
                                                                {data['envio']['pais']}<br>
                                                                {data['envio']['provincia']}<br>
                                                                {data['envio']['ciudad']}<br>
                                                                {data['envio']['callePrincipal']}<br>
                                                                {data['envio']['numero']}<br>
                                                                {data['envio']['calleSecundaria']}<br>
                                                                {data['envio']['referencia']} </address>
                                                        </td>
                                                    </tr>
                                                    </tbody>
                                                </table>
                                                <p style="margin:0 0 16px">Esperamos poder cumplir pronto tu pedido.</p>
                                            </div>
                                        </td>
                                    </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
            </tbody>
        </table>
        </body>
    </html>
    """
    sendEmail(subject, txt_content, from_email, to, html_content)


def enviarCorreoVendedorRechazado(data):
    usuario = Usuarios.objects.filter(username=data['facturacion']['codigoVendedor'].upper()).first()

    if usuario and 'Vendedor' == usuario.idRol.nombre:
        subject, from_email, to = 'Envio de pedido rechazado', "08d77fe1da-d09822@inbox.mailtrap.io", data['correoCourier']
        txt_content = f"""
                Registro de Pedido
                Se ha generado un pedido a su nombre {data['facturacion']['nombres']} {data['facturacion']['apellidos']}
                Su pedido ha sido enviado en pocos momentos sera despachado.
                Atentamente,
                Equipo Vittoria.
        """

        articulos = ""

        for item in data['articulos']:
            articulos += f"""
                <tr>
                    <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                        {item['articulo']}
                        <ul style="font-size:small;margin:1em 0 0;padding:0;list-style:none">
                            <li style="margin:.5em 0 0;padding:0"><strong style="float:left;margin-right:.25em;clear:both">Precio:</strong>
                                <p style="margin:0">{item['valorUnitario']} unidad</p>
                            </li>
                        </li></ul>
                    </td>
                    <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                        {item['cantidad']} </td>
                    <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                        <span><span>$</span>{item['precio']}</span>
                    </td>
                </tr>
            """

        html_content = f"""
        <html>
            <body>
                <div id="m_-2286063398718872391template_header_image">
                    <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:100%;margin-left:0px;margin-right:0px"></p>
                </div>
                <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_container" style="border:1px solid rgb(222,222,222);border-radius:3px;background-color:rgb(255,255,255)">
                <tbody>
                <tr>
                    <td align="center" valign="top">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_header" style="border-bottom:0px;font-weight:bold;line-height:100%;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;border-radius:3px 3px 0px 0px;color:rgb(255,255,255);background-color:rgb(35,85,225)">
                            <tbody>
                            <tr>
                                <td id="m_-2286063398718872391header_wrapper" style="padding:36px 48px;display:block">
                                    <h1 style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:30px;font-weight:300;line-height:150%;margin:0px;text-align:left;color:rgb(255,255,255)">
                                        Hola su pedido ha sido rechazado por:
                                    </h1>
                                    <h1 style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:30px;font-weight:300;line-height:150%;margin:0px;text-align:left;color:rgb(255,255,255)">
                                        {data['motivo']}
                                    </h1>
                                </td>
                            </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td align="center" valign="top">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" id="m_-2286063398718872391template_body">
                            <tbody>
                            <tr>
                                <td valign="top" id="m_-2286063398718872391body_content" style="background-color:rgb(255,255,255)">
                                    <table border="0" cellpadding="20" cellspacing="0" width="100%">
                                        <tbody>
                                        <tr>
                                            <td valign="top" style="padding:48px 48px 32px">
                                                <div id="m_-2286063398718872391body_content_inner" align="left" style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:14px;line-height:150%;text-align:left;color:rgb(99,99,99)">
                                                    <p style="margin:0 0 16px">Hola {data['facturacion']['nombres']} {data['facturacion']['apellidos']},</p>
                                                    <p style="margin:0 0 16px">Se ha generado un pedido. Está en espera hasta que confirmemos que se ha recibido el pago.</p>
                                                    <h2 style="display:block;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:18px;font-weight:bold;line-height:130%;margin:0px 0px 18px;text-align:left;color:rgb(35,85,225)">
                                                        [Pedido #{data['numeroPedido']}] ({data['created_at']})</h2>
                                                    <div style="margin-bottom:40px">
                                                        <table cellspacing="0" cellpadding="6" border="1" width="100%" style="border:1px solid rgb(229,229,229);vertical-align:middle;width:100%;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                                                            <thead>
                                                            <tr>
                                                                <th scope="col" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    Producto</th>
                                                                <th scope="col" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    Cantidad</th>
                                                                <th scope="col" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    Precio</th>
                                                            </tr>
                                                            </thead>
                                                            <tbody>
                                                            {articulos}
                                                            </tbody>
                                                            <tfoot>
                                                            <tr>
                                                                <th scope="row" colspan="2" align="left" style="border-width:4px 1px 1px;border-style:solid;border-color:rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    Subtotal:</th>
                                                                <td align="left" style="border-width:4px 1px 1px;border-style:solid;border-color:rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    <span><span>$</span>{data['subtotal']}</span></td>
                                                            </tr>
                                                            <tr>
                                                                <th scope="row" colspan="2" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    Envío:</th>
                                                                <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    <span><span>$</span>5.00</span>&nbsp;<small>vía Cantonal</small>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <th scope="row" colspan="2" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    Métodos de pago:</th>
                                                                <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    {data['metodoPago']}</td>
                                                            </tr>
                                                            <tr>
                                                                <th scope="row" colspan="2" align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    Total:</th>
                                                                <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    <span><span>$</span>{data['total']}</span></td>
                                                            </tr>
                                                            </tfoot>
                                                        </table>
                                                    </div>
                                                    <table id="m_-2286063398718872391addresses" cellspacing="0" cellpadding="0" border="0" width="100%" style="width:100%;vertical-align:top;margin-bottom:40px;padding:0">
                                                        <tbody>
                                                        <tr>
                                                            <td valign="top" width="50%" align="left" style="text-align:left;font-family:'Helvetica Neue',Helvetica,Roboto,Arial,sans-serif;border:0;padding:0">
                                                                <h2 style="display:block;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:18px;font-weight:bold;line-height:130%;margin:0px 0px 18px;text-align:left;color:rgb(35,85,225)">
                                                                    Datos de facturación</h2>
                                                                <address style="padding:12px;border:1px solid rgb(229,229,229);color:rgb(99,99,99)">
                                                                    {data['facturacion']['nombres']} {data['facturacion']['apellidos']}<br>
                                                                    {data['facturacion']['correo']}<br>
                                                                    {data['facturacion']['identificacion']}<br>
                                                                    {data['facturacion']['telefono']}<br>
                                                                    {data['facturacion']['pais']}<br>
                                                                    {data['facturacion']['provincia']}<br>
                                                                    {data['facturacion']['ciudad']}<br>
                                                                    {data['facturacion']['callePrincipal']}<br>
                                                                    {data['facturacion']['numero']}<br>
                                                                    {data['facturacion']['calleSecundaria']}<br>
                                                                    {data['facturacion']['referencia']} <br>
                                                                    <a href="mailto:{data['facturacion']['correo']}" target="_blank">{data['facturacion']['correo']}</a> </address>
                                                            </td>
                                                            <td valign="top" width="50%" align="left" style="text-align:left;font-family:'Helvetica Neue',Helvetica,Roboto,Arial,sans-serif;padding:0">
                                                                <h2 style="display:block;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:18px;font-weight:bold;line-height:130%;margin:0px 0px 18px;text-align:left;color:rgb(35,85,225)">
                                                                    Datos de envío</h2>
                                                                <address style="padding:12px;border:1px solid rgb(229,229,229);color:rgb(99,99,99)">
                                                                    {data['envio']['nombres']} {data['envio']['apellidos']}<br>
                                                                    {data['envio']['correo']}<br>
                                                                    {data['envio']['identificacion']}<br>
                                                                    {data['envio']['telefono']}<br>
                                                                    {data['envio']['pais']}<br>
                                                                    {data['envio']['provincia']}<br>
                                                                    {data['envio']['ciudad']}<br>
                                                                    {data['envio']['callePrincipal']}<br>
                                                                    {data['envio']['numero']}<br>
                                                                    {data['envio']['calleSecundaria']}<br>
                                                                    {data['envio']['referencia']} </address>
                                                            </td>
                                                        </tr>
                                                        </tbody>
                                                    </table>
                                                    <p style="margin:0 0 16px">Esperamos poder cumplir pronto tu pedido.</p>
                                                </div>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </td>
                            </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
                </tbody>
            </table>
            </body>
        </html>
        """
        sendEmail(subject, txt_content, from_email, to, html_content)