from ...ADM.vittoria_usuarios.models import Usuarios
from ...config.util import sendEmail


def enviarCorreoVendedor(data):
    usuario = Usuarios.objects.filter(username=data['facturacion']['codigoVendedor']).first()

    if 'Vendedor' == usuario.idRol.nombre:
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
                                        Se ha generado un pedido</h1>
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
                                                                    Dirección de facturación</h2>
                                                                <address style="padding:12px;border:1px solid rgb(229,229,229);color:rgb(99,99,99)">
                                                                    {data['facturacion']['nombres']} {data['facturacion']['apellidos']}<br>
                                                                    {data['facturacion']['telefono']}<br>
                                                                    {data['facturacion']['callePrincipal']}<br>
                                                                    {data['facturacion']['ciudad']}<br>
                                                                    {data['facturacion']['provincia']} <br>
                                                                    <a href="mailto:{data['facturacion']['correo']}" target="_blank">{data['facturacion']['correo']}</a> </address>
                                                            </td>
                                                            <td valign="top" width="50%" align="left" style="text-align:left;font-family:'Helvetica Neue',Helvetica,Roboto,Arial,sans-serif;padding:0">
                                                                <h2 style="display:block;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:18px;font-weight:bold;line-height:130%;margin:0px 0px 18px;text-align:left;color:rgb(35,85,225)">
                                                                    Dirección de envío</h2>
                                                                <address style="padding:12px;border:1px solid rgb(229,229,229);color:rgb(99,99,99)">
                                                                    {data['envio']['nombres']} {data['envio']['apellidos']}<br>
                                                                    {data['envio']['callePrincipal']}<br>
                                                                    {data['envio']['ciudad']}<br>
                                                                    {data['envio']['provincia']} </address>
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
    subject, from_email, to = 'Solicitud de Pedido', "08d77fe1da-d09822@inbox.mailtrap.io", data['facturacion']['correo']
    txt_content = f"""
            Envio de Pedido
            Hola {data['facturacion']['nombres']} {data['facturacion']['apellidos']}
            Atentamente,
            Equipo Vittoria.
    """
    html_content = f"""
        <html>
            <body>
            <div>
                <h1>
                Envio de Pedido
                </h1>
                <h2>
                Hola {data['facturacion']['nombres']} {data['facturacion']['apellidos']}
                </h2>
                Su pedido ha sido enviado
            </div>
            <br>
            Atentamente,
            <br>
            Equipo Vittoria.
            <br>
            </body>
        </html>
    """
    sendEmail(subject, txt_content, from_email, to, html_content)


def enviarCorreoCourier(data):
    subject, from_email, to = 'Solicitud de Pedido', "08d77fe1da-d09822@inbox.mailtrap.io", data['correoCourier']
    txt_content = f"""
        Envio de Pedido
        Hola {data['nombreCourier']}
        Atentamente,
        Equipo Vittoria.
    """
    html_content = f"""
        <html>
            <body>
            <div>
                <h1>
                Envio de Pedido
                </h1>
                <h2>
                Hola {data['nombreCourier']}
                </h2>
                Su pedido ha sido enviado
            </div>
            <br>
            Atentamente,
            <br>
            Equipo Vittoria.
            <br>
            </body>
        </html>
    """
    sendEmail(subject, txt_content, from_email, to, html_content)
