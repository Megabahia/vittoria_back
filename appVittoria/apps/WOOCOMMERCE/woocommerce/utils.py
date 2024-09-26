from ...ADM.vittoria_usuarios.models import Usuarios
from ...config.util import sendEmail
from ...config.util2 import sendEmail as sendEmail2
from urllib.parse import urlparse

def cortar_url(canal):
    # Verifica si la cadena parece una URL (comienza con http:// o https://)
    if canal.startswith('http://') or canal.startswith('https://'):
        parsed_url = urlparse(canal)
        dominio = parsed_url.netloc

        # Elimina 'www.' si está presente para mantener la consistencia
        if dominio.startswith('www.'):
            dominio = dominio[4:]
        return dominio
    else:
        # Si no parece una URL, devolver el canal tal como está
        return canal

def enviarCorreoVendedorVentaConcreta(data):
    usuario = Usuarios.objects.filter(username=(data['facturacion']['codigoVendedor'] or '').upper()).first()
    nuevoTexto = '''<p style="color:rgb(255,0,0)">El pedido ya fue despachado, está pendiente la confirmación de recepción y pago del pedido por parte del cliente.</p>
                                                <p style="color:rgb(255,0,0)">SE LE INFORMARÁ CUANDO LA VENTA HAYA SIDO CONCRETADA Y EL PAQUETE HAYA SIDO ENTREGADO.</p>'''
    canalPedido=cortar_url(data['canal'])
    if usuario and 'Asesor comercial' == usuario.idRol.nombre or usuario and 'Director GCN' == usuario.idRol.nombre:
        subject, from_email, to = f"Su pedido {data['numeroPedido']} desde el canal {canalPedido} ha sido despachado", "08d77fe1da-d09822@inbox.mailtrap.io", usuario.email
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
                    <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:40%;margin-left:0px;margin-right:0px"></p>
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
                                                    <p style="margin:0 0 16px">Pedido desde el canal {canalPedido}.</p>
                                                    <p style="margin:0 0 16px">Felicidades, la venta fue concreta.</p>
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

def enviarCorreoVendedorDevolucion(data):
    usuario = Usuarios.objects.filter(username=(data['facturacion']['codigoVendedor'] or '').upper()).first()
    nuevoTexto = '''<p style="color:rgb(255,0,0)">El pedido ya fue despachado, está pendiente la confirmación de recepción y pago del pedido por parte del cliente.</p>
                                                <p style="color:rgb(255,0,0)">SE LE INFORMARÁ CUANDO LA VENTA HAYA SIDO CONCRETADA Y EL PAQUETE HAYA SIDO ENTREGADO.</p>'''
    canalPedido = cortar_url(data['canal'])
    if usuario and 'Asesor comercial' == usuario.idRol.nombre or usuario and 'Director GCN' == usuario.idRol.nombre:
        subject, from_email, to = f"Su pedido {data['numeroPedido']} desde el canal {canalPedido} ha sido despachado", "08d77fe1da-d09822@inbox.mailtrap.io", usuario.email
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
                    <p style="margin-top:0"><img src="data:image/png;base64,UklGRowfAABXRUJQVlA4TIAfAAAv5wNnEH+hqG0jad+dGf5M721xsI0kqdFAAloEQP5BYYrX3lvLIJIkJ//Ah1kB+PeFhMyugfmPR/HlUpCQgoQwKYjJGGXiR37SjzykEznUt6tH6pN+hv6GfJp6u3qburt6NnU1dW1qNjVW+TfJxkFYsY5osCQeYQEe4E7g4R7m4B7mYB4cxW3bRvL+Yydpc/4jYgK4VMkvPJApGQoAJb+QwecbGcp+WNrbbVtZa2vbhi9RY1QGanxXxvH+fhz///etrEyBMYhnoZQzEf2fAN+y7datbdsWPqWAN5EUSfz/9zVXAYRkj26Pl4j+T4D4+v/r/6//v/7/+v/r/6//v/7/+v/r/6//v/7/+v/r//+/eJKmeVEU1U+LoijSNAnCkrS4VzWYr6t7cUsCrfhWVA3Y3lTFLQmpoltRSXC4Km5RABVnZQMUNmUWh0y3ewOUNvdbFCLF2QMofuRxWBTnNdBd53EoFOU1UF/ncQB0ewCPjyzsie8S+JT3ONi5VcBtlYU4Ud4Ax00RBTbxXQLXsowDmrgE3ss4kIlL4L+MA5i4BD8s48AlKsEfyzhgiQoJPimLKFTJGvBNmQUpSQU+WqfBSXQHXy2jsOQmwV9lFpDEFfhtFYciuQTflXkQElfgw1Ucftwk+LHMAo/oAf78iEKOpAGfbtJwIwffLgKN6AH+/YhCjKQGH2+S8CKT4OcyCy0K8Pd7UBGV4POPKJyIavD7OgolkgZ8XyZhRCLB/2USQmQSPsIsfMjgU8xChww+xyxsyOCTzEKGDD7LMlzI4NMsQ4UMPs8sTMjgE81ChAw+0yw8yOBTzUKDRH4skIYFiYTPVSYhQdTAJysjikYOUHLKdd5i1RyhjWX8rEQ1fLZ1RI5kGIfuTjKMj1+VEj7dBzkZ9kl8TYZ5/U0p4PO9EzOwM4onYdiz/KJk8AlntJQtODwl7Ow/KIl0oe/7nrO27/vONpmQkvZg+BnYWn9Pogas7oZ50/hbvc1Dy0w/rRv+ft+mp7IGmogSbM5+0p70e/IAi5/LgScey5MLNax45j62lkDFB5aXid+aHKxtZ42nH3PLQL/i+ftgBxR8NC/ltyYBW9sFDS8tccOBZvWkbICUjeiFf2qixhK1oIWLIqzf0bwebJARF1g+TvzUPMDOUaOVeqRKrWjn3pmDBxvVR/mpycDKdkNrN0XSU6O1kznIuQguBL80sbSi12ix7gia0eZNGZMxE5ge+k9NBTYOaLfuyFnQ7qMzBRUXxUP8pcnBxgVt3xUxC9quO1OQE5VV7GBBm39ZYmnDgvbvtAxov+5MyZimrsK571CdvywVWLigiwslPbqoO0NQ0USsyvuCJo8flhtYOKCbEx2ddgJ1awhymooKsuuEtv+wRNKCHl0dqFAHOrorQzIi6dT1XUXD8sNyB/NKO6M7InZ0djEEJUnEqrhJoC10Jxkv5xsbr+eXIgULN3RXtyQs6PDTEKQkFRXWnq467zJqCriacpveRjtSxMuYcj2Xs9mPFHA5pKPNb0NlwYgu74qACV3WylBN0qmre6KG6Q7SM0y5DDfSMww5WRYxWS0zjLmc34QMzCvtFK7uDej2YghyiohVYcuC9rjBKgz70F2swvCbdKtF7OUq34JIWjCj44trHbreGZIRRUWFueNQTXdyYHM4t8kB30sxMhxy+xIUYL5F5we3Wu3cZggKiqau7GBNIG8nY3+WPSfDeb80Epwm+QbE0oLFPXy6pHZ0vzcEMUEUVLzhhLZ6K3AZ5o4D7usFyfAb5hegBPMKCdSdQxsSuJgqKTpUOO2yavmSCKc87QpuJBGeeV1+MVg4UYCHcmZBEltDEBM0dcVMoI3kSiLc8rQquNMB3/HyK204SMBdOTIijaOpB0EUVBCrpmquJMIxT5uGW7Ez/O3ii8HCDolc3HgikbspSAk6dN0qqsRVhOsoFhO3mnD/32uvtGGmAmcXOk0FtqYqgqYuGU1oM3k64PywiPdofwx/f730YrBxJwMH+5RGMkdTkNBDQYVlc6i6pxPGnKIVhq7DNsVd4z74vyuvtEEhoZ1takc6V2MlQU3XbFjD4kiCBR+D/pWzsEXSBYN0ChHR6mlDoC2cXpr948KLwcYnJbqzbEVCtTGI6Vm6YHJCW8hRhWEVuiiHAYamQx0GXRzB7LTLbdDfq0WTP194pRUTJbgrq2YktTVW0kNRhWmRVaejBT1PUnaDrMmqKHRZoiaNl4v+XtfySeqTDfC6i6QVKym42zQgrb0xiOhpusNAoGVyVHQ8Sd11WApoWUgprMAgNf8VmpDlZIN/X3YFWLnRgos9PRI7mivoWTo2aKrDkbBukuGha9eGqpO6a5IuvwqdrLvBPy67xg6kdrSl09RM5iQ9FFU4dVE1HTWoK1kKq9K1qglkGBRYqvFP6LQx6P5+1WXAEg52qAOpnc1BRk/TFdWENpCjqGIxoaqCXCqaw6JomopGLp22Nt2fr7qKKd1ZsSO5mwU1PaKDaIrqcLSgPsh26calpDktuubQ7Z/fghiYQt1asCBHkJBDWdc1rFqOmm4ZUVDVHdNiaJI/0v3poruzhbsyNiFPJT1dlxQd2kiOkiqQdVHlHfRIQYUXneQLV1MDMiUjckSHdS2rmieoi1lVxXeTvgMZMIaLmQ65gowcyrp2aUG9HA1dMxsq7FgW55fowRoOJlrNV0VP14VLTZXJUdONJxgW9TsUA2/4PE/tyBfE5IgO80pQdU9Ft/yMDYdF1NQvTc6d7k7bkLOcHMq648KEWjwl3TBvW6omGAxo25em5g4PddKCrDX0nDq+UFSFPLHO8aWuQdMl1dg3R6s1XeZvQAzs4a5OGZA3SMghVuH8i1WnKzzDUvHUNKhp62wlwuMVl3sALmc8kbs7PUVX/ujQMvFDUQOe1xrUecNZGF6vuNoHcP5Zp9lr6Dl1kFdZVVyNp+gqoMpfK0HfraQGOL7gYvACHH6iNLIHMTnEuv5iQT3fkbAOyHWMcdYIQyZbqQzXF1zuCdi9p3b0gJyeoksvmirQO6JusbPajADnF9zDF3T31oI+UNNz6rD+CarjbcxrlDwFMq1wf71F4Au4qzdm9AKIyCHWNSIaUK93EUi52NEwKfh+3PwB998N6AkZPYcuEFFRRXoXVUOT3VSyLPiClB6By6sefaGkZ+owSVjV3kUhdYHXQpYnviGNT+D4S6e9oaGHgu6gDvW6XfJ5DFI3eC1kKfwNicErcABQO3oDJPQcOqakyuRsGdBNT3itZFpgyrmOSRfTf36ZZ+AyH+gROT1ThwZ190ZPsdhJGGQqsEwnaf/7K32DR0cPeijoWCf3G/dIcMmVjJsBn6T/76+5NCRBh05fyF16hg5lDiaxC1lHHU/6PsRwaUBMz9p3PkC9RVBEop75Gue2yF6gP+kLcbs4Mnoo7mLyV3X5DieUg/6dvR4plVrbWLR36BJ9I+4Xx52gtqvc4NTxHYoikveu61+J6uKoCVq7xg2WDucNgiK5q7rxlYCLAwiiuCfQDSjo0g3wNPSNSBjal2maNhf2eZqm9WAnJajtOW5RdBjupgbyjcq40XMLr4fDLj218LrfmMkIWnvmLbpBEG9DFeVuw6TjP76CmbWFd0dt0drCu0/Nyp0gijsi3UIMUO6G0OVezaLjv76KlxF+2GlrRvih2jmpKOo72j2oGKDIDukZKNdEByCmVOrLc7zc0XTRoOM/v4aVAX7caUsG+LHaGZEUyY51k2GBOM3Owvh3XiK2sE25DpOhQ1cV/PcHnAxwYqetGOBEtfMBEUGU7RLdhJIFUKbBbJnxZ79WvLzMXVRiwPPaivjvL+VkhlN7G2Y4tdV8pBR1u36bYQOEo48/5ug1MS7Xa8MVwGUpKOiAKn+tCutr7cbIDidP5nY4+clHRpHYyW0oGW1WUPIFcFUcFuDSxxijZthfawUj/VlwGOvPgpWNgiLKVpnus/h2k50BUS5NE4/XWsnHAqf3phY4vWXjQVK3Om9E/XbU3YHnFUrfj4qP9jzYDLXnwcJFRZIYMd2Jyu3oZG/gdWV8Pxo2FjDYm1nBYMuFJImKTbkXldvRit4Qr9Dx9QA2WhNwGHmagIUJoOm0GTej4m3oOrtDvSLRA7cv2AZGRxMHGO25iEkitgh0NzqcLVXDDVku0OR9PMd/eCkbgxllYjYDBxMpTcXiuB+d7CmTtuCW9QpN3hUnfcOUGVgNdIZmnzst5gOQFD9FNA1qTi/jpnCJVtxzCP2nd+NiBcPjeQcY7pnI7QqqaEZBl8hcdGUD0cguuCzSnlCHSdfnqNEE8xJRZbs4iIimgv9TK7gYTXXnzaZA81DYdbKCh91MmjjtqGvC2kK0jrAplJP0wqooZDiiRVPQKmwTOr2O145vVGcK9GlPY5uHEI1a0utSB22d7Uh/5nrSVjlrTq+PNsnhrMkqHX2RaYGWhWyzwaEhkp5UXE76W/qRXuc66RsFxrfTlLHJSz7G2WtJKb7glFKtY5H5hHqQsbAu6f4dtaT0T0ylDfoOlkxs5qazDjD+5KHyNN9FVcj8cPKVrJiYzQ1nbea6i0igXnbj12Ey1581mYOL6FRF+tl4mlNnjRboa6iq0oauyz8GvTk4q7dgu4ayo6Kr/1+VVNFOWHf+GHQWHP+3gGV2QL9+DMDC7SSwcL6oklWHPtLPzHQNZR2yWMgBw/5/VtUAXJdGWoAhy69B50xvwXwNDQsAsZ5DXsxRM2wr/Rr0hG3XEAUbj5F+MI6Lr96E5y8GnjxcZsL36PR7MDozWYAXEZ236PSDMJnrz1rNqcuIqj/u9F0tmVjMDWft5vrriJq3MOnLWjCxmZvPQmVs5OFu2yppc61trA+ETnZ1CP0maHPbab2xhYfCsgansbT5YZAUP2XR95ULbI3h6ZOxw0MGPHPu8kkQrcIeuCz6xt64GE09z9tNtchDbldx9W85Pwki6XlX7kLf2ZSLzdR8HipDIxOpXdEdEPon8e+oOdhwqoO+t2xga+gwMBjafQS3DP2zeDlGq/VIr2ut5xD67kZsTGZ6NLiaaZGJmD4gjo/jv00ZtdaUUqq1DvmUBBvazGICWyMTF4ID4PiiHFAen1LDBQ4mWjQ6GTmYkEwgrm9Jh7p/SBUbh4nJjDYxIBMVF+D5Jam6+iGVbOBwntJmcDRwcPFgA+g/LQVFep22Mw512oyGtTptxDP3rn2u5BSMoP+yZARNCgDWE3A6q0Pj81mtPqUFAOg1MTknGD8sKTm6g1/7M7A/R+3m8HnShqfCS6VpSVnh+bsiyOnBgFanLGih7k6Z8Nz2BXS0RK4l+nuNMXotcQui/K5IYhZ4qfZTcFcnLGjlrk4Y8OT9qX6BhRIp6Lh4HmyH/LtSEdO+WDSevKsfLWjp3v5owPP3Fy0lFUVE1JMZzp+VgpYVXnan4dG9p1a0VvfvqQXP1+oF7ITciSLqwSrIr0pGy/gKOn0W4qTeGDTavLRvPA88X3fweiEkJ4vkMEL9VUlo6X8DnT4N9fJsAVQ/H2j78mwBoB8PNKg7+O1ESEoXUWcbXj8qgqAnAECnTyN97wAAemoEZTTZBIenNca61RhDPrk1xnyQNYa8lzGGvJuKlAEAhuUX6DQ/u4JftwlAHXTUtNFkExYPo5XE+DvleoorOWuO+Dum2pcjGTUnxuuU63hHs5XE+Dumeq57nTUxXsfc5sPJqCUxLsZU+3wXd1L0/JwR1S+gdm5WBb92iMeGxm0qiaNugratZ4ZlbOJEWoJlKKeL1RIMcxcT6SUxXqfclp30khivU26y7ywMy1jXJmk54mVITS6twtCGJja9vk66VK+PLatG2HLu8g4yUl5PL0CtvMzwekErbcqoo8Mk7FkHw74sB6vAPlTZNTKs+Vg6iVDysJIIJc89UgPs09gScZnlr5lgys2iw+2w6xFby3y+mCCtXgCMjOgBXrdITUKeBAvMDXJgc1mbpGAv9y0jYeshmgF1sRpQ1y2VsTdNuwHleCUHzOPURT+HVQ/YnubTiYYenH4D/cHF3sFvF2qkII9Ok8PuZGzntuVkbO92cmA3j13pAUbA/uprBGzkroLfZDMCXB7ycA+CtPoNqJWHGX7fIjUPBihZBCspcJnF7oDDYDYDHPanO+AyiqOKzV2xHMFCDngN89lygnD6HcBT03f08OZCTs7BaYFlIxFOo1gVuBSjzvDI69EkwSlPL5KwfVwbt5oRjvujxRRp9QaohboJ3m2RnIQDChbdZDLcRrGp8DlsOpy2J5MItzx9SMR+Xk8xGa77k4mGIJzfAeh3yrYW3t7IkYKFw6JYLIbjaHLiRh1e84NJhOMgHiTCY3qIyXDen6ykCLu3AIaDqq2H959ITsnDtIgGEuH6MBC+0YTb9GAJrpODM8Ln+QiT4X48WEbS9gOA4aDoGOCH6qAn44GCAQwynJ+6ivsIfwAHnLd9DKfhCSTAP8tzRSTh+BOA4aBmG+DHM9ITM1EspqrBexCN8I0y/MbHGvDOa5vf8wI5ioqEO+bnEhVJuv0RwLBRsvTw8w7pqQUTzWJoFlvwcQoR0WjRAlXTYJj7pH9HL2HLCc9PJcGCy7mIiEZLFiiPka8EP/lawz3Hc+Uk4XYCQLdoGo6phRPVTlDBxbComgw9V6GLIxqwKKIuLro8j2AmwSymlFgTn6rC8BC6uJIB1lNALhQ//dJiI061jlFrZqvwXDFNOJ4BAMPqnF56OHdGghIuaN+APk5SFh3aNYE6Cql7eiGqClM+Br2Us/CV9FALeh6kbAbFV0wpmfULi71EulxgmjpdHMkG/bFETZPuzgFQw+qQXp5w9hMJagQbbJAVSReF1EUXrg3dIsuRgERaYZND6Ko0frqi40nqpmPxE7rQvz3ZlAsk43XRlXGdLi9Y8knKEUzic91pwl2d9OtzPlzYpg7ObzVFdz6SQbo2oeZFhlGFeamqMhnPIaoOQz5JK/WP/EzCukGGSYXuhTtdbCbxyt9VV8m+WMRFaokWmI+VEIWrAQBon/Nukd6mHoyqHSlKvKHoGlkO3bGlWllGi0GGM75oz9SgPshy6bKTuOhyt8C9FgyDkKFEi+OxRE0UjkZe9uO8aVP7Nj1bML4gRY3go+5iVSDbqIqPMGHYyPYAwPJMQcViQkXFPoqQMluMWzWLSabTIjxXThUOxl73/TSt27a/pbdtm6ahb8HOEUm6e8MJdTfqKsiO4uYwSGQ9SjrpkSbUB9kOFaaHQmrhh4kGlYyrASZZMVm6s8P9AWmKvaGoWIxEN3aweAkGw0z/HFW3jIhV/7CgkOFhUO+0oGexEjZoZImKKtQdBx3SVAtvYFUm66iqO5CdLOgjvZ2oimSdVX81V8hyPkszqGR+GGS6MrLwUPR1mqjMGybUzSyrypWmQxIX3aC/HYH6MKuqPxuLYkLhUbLBslsGTFckycJdUddpJCryhqYbZlWVrgwDcPdwGMjbGbpu1lV/MPUHIdusS3diXaSNQYf/kSVKunBXtHUaiSqFNxQduQlXyAIIfV/SRXo7VTfMhgpN/ZmM65NM6OuOw+DfdCWE4a4o6zRSlbJy7En3waVsAoS6NkF/vJ+sIz//c6M9yWkwdnSDf9AlasLw6OjqNFLVCFbSHqjjMC9buhGA2GXDMujvJ+mGedP9243xJNWAdg6DvxOWUYa6o2pAV2cLMu7KBdF5vkTBDEAZZsNgvB/cmL+sC1vI4G+ECUkZ6oGmEZ2dzMmIl2BQL4yn6DuA0I1OA/ovJemSsz9TVtixuYI4UbSgu6O5u+AF74DiFoCrWNQPYH5yUVf2pLcS27G6g6uipt3R4d5czMu0GBfOx1i8BwjdA7+f8clBXz8HUVoxOYR7R0uv0eXWWCl46XvqY9DcBaS1L32LYiueLqEeKZnQaQ3GE2YOC3oiGrwLfH7LRGmDcgpxVVS0O7q9GqsEM9EgPBPNsAvo/0v899JIbYDdLdRPGkaNjo/GUmYWDPMzZB1J2Yb+v8MfxaUhKhtmxxBX5V63ofOtqUow0y3qM5wGRCPtwvif4e8XR2pD5xzq0TE1ofs7mE65SRbjEQoZ97ApyBZ8UEVcHKKyAA7nEPfeJXUggaOpSjCzYElXm46TzzzIfqQtqJ9O8pk7+UjZE3V/oS6xYSQAR5eAhNZUys1hkS4NXaIHXAdvYNkiHwDdlCXWpT3Q/506UVqgCNDKqYGABQw/BDPCFm1PeAIi6tkMdct4O/LJJV3YIm8otgAW9yZwWmn3OlMxNwWW69LU4SGIVg1G4cIwaG+HDNYHhy3D4N/kibsFrXNauQWTcxsYLgUzE5aJrhvIUxBRDyZYO8r7Yd34nA6DsaMZ/Je+SJqD2bUJHFeHa60hGTEj0aQrWDcehKixxfmXGIQ78U2Srn1O1aDtyDoWDOYWKO3WoVyDwbEZDBeCmQJLJmXStUehGQzqX8Q6rBtBjMquQ1c+p2GQd7AucSAac/B06wnub05pZagRzBSYVs2hy89Ck3ckg3qn06ZiV9OFz0kMIHYd+spCagGsLq1AYKtdeoLhlJkCUxZN10GehbouXzgMgp9lcJh0bBs6zI+JgkGzSwaTBfGwQGl3DkUBDA7NYPghWJEM20raZVAfRnTpwmmAbldDXJfIgC069pFB+TySWTEIZgN6Jh4jaQ46Z3QHNC7O7GBYxqyMAFsWFQUdy7OQrlwQCxYjSQDKJjRdh4esw/o42KwboFklg/ImRG4BDK4MQOXmiFamCsHITLDupD90OB6uXqBogGwzGADitWTAomlw0QzSx4FpJRa8bCoMx7sQlQUwuTEAmWp3QndguBZsSE8wT2Q4DNDdSUlVzNaWZoFiIAdeX8sGiHJJCnwsAxxv7jQoVpQNEMWiwzDQ20xsgMWFAQhVuwO6A9MJDzJqxkZeFhQM0Pf0HEJXNABcxajqzivLBFk0PcCkWiDOCyPACSUD1D1nCdwebRhgWHULRNF1WPb3IQobYLJvAFLVbp3uwHQhaAr1akoJu08yrRY4xOwsDACsyPiXq1hM1q0rlE3AVS5ID7h4bZgAZf4jPcFe1y2QxWweAf+uJ1sW3P+YhXleILYAn4qVYRnondY2wGDbAMSq1bK9BdO1IMp5JVthC3ATg9UL4895Lb0A+FiqyVAHujxsAKR6jjF6Tbg+LpERgJQituooWIDrMpCzBPw5nowsgFBqrTkAwHGlmgCxr7/OAtv+VhJpA/TaJt0BvZNVqwLjiQ8Usq4mAHIbF+aoOeDyuMZ/AIhtXZkFhsc1SlbWimy23aCbAMhtyF9z1BJxuT1aMrmcrgjbAAip1JoSrCO919wKUJs9qwKKe22NHsF8ITygkLmw0UtOKcJUAWVI9WUJMF2KcaP+GBSNXnJKEab10eouvkLNbPd8M6KyAmDUdugnEK0WS7YWzFfCAwptPHfYb9mcSFtcyTUKjzF22D/b2IVLlG5R6d1G0g5Qiw2zArr7zYJjAAtl7AGdtuY3MlXCnkhZvfA+qh8GBU+Lb5Dp/aaWALSLqaUF2ofd0DGAlTfBXpi0V+LNgqOD9OM+EnzwdEDpw6ie6PQX5Q2JwhaAdjrOOyYF9PeLgW0AO++CvUNo9+J7JT+RLLufqKHTBU/yINHd+WzCnqh7i0JvubIGAJ7zccYxd8CkGlZ9xja2YGktuIuDHE72tq4VN0FM6HBzqKg44EkuSKK38WxUXVH3FYXecyQtAoB2mLa3p2cLvPbjsr27Tj3YK2PmQiefEn0xXe9e4iTj5oSXTuK2uMgJSXYmD0dxS1BRZ0dF6F0ndnl8KihN/vJJbuVwVRUSfCQh884ewiRDiZuykBui6irT0y3ekXQ0gxdu9MazjygXpB7OYlvkegQ/B2ln8FBp50r7DiFTSTu40UsvNJOfJI9Hkzc0A5LqIy966+UHVApaF/sJuS/y34MLLov0UnlXXrS5hz1lkXm1y4ucEfXgIw8yvFG2IklmvCyIVtmXBr376uOpBbUzeEi5novu2vMuLl3IVnrcUSY57MGMy6KdM9mkQX8f13juIBp5F+cuZJs0fFpR0vA0I+rBhk+yXgfv4DLp/Uf1h9NE5BCddWcfY9LtV89sFUqbtHW1ZMK5CzmdRzAI5aTto7CGy6TL40iJAYSUm9Bu6SVYhVwHbZw1pfgPp1SakP2oKcV/OKXShbaeWZe70M6zBJtQutBHmMiPRibC09dZS4oXYsq1D/I52pHiXynVPsn3OmtO8QWnXM9FTkfN6VVIddDd11lLShdCSrUNobc82pH+rG2QwzVqSfGvkHI9F32OifxkEhEU3j6YTASG2ceSieAw+1ByESDeP5JSBInlB1KKQLH8OEoRLJYfRikCxvKjKEXQeP8gShE4Zh9DLoLH7EPIRACZyU8gE0FkIr1PJiKQTGrPaxIRTEa119WRCClLjytFYJl5Wy6Cy0R6mUxFgBnVHlbHIsy8e9ddBJs36VXyJgLOqPKoKhZhZ+5NhQg+k9qL6kSEoIUHFSIQTWrPqRMRjubSY2QhgtL44S1VLELTtPGS5iZC1EJ6hyxEoBqVnlFGIlyNHx5RxSJsTStPqFIRvqaVB1SpCGPTirkqFeFsUjJWpiKsje+SJXmPRXgbZQ07TR6JQDctWSlTEfJGWc1EnUci+I3vDXnNPRGBcHJvCGvuiQiKk6Imqb4nIkCOs4ckRT6yWITLSf6QJMhHnojwOcnL2qm6zBMRUKd5WTlQlXkqguw4zYuqsqKqijyNRfidpGlRFGX18kX1siyKIk0T8fX/1/9f/3/9//X/1/9f/3/9//X/1/9f/3/9//X/1//fxQI=" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:40%;margin-left:0px;margin-right:0px"></p>
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
                                                    <p style="margin:0 0 16px; color:rgb(255,0,0)">Pedido desde el canal {canalPedido}.</p>
                                                    <p style="margin:0 0 16px; color:rgb(255,0,0)">El paquete fue devuelto y no fue concretada la venta.</p>
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

def enviarCorreoAdminAutorizador(data):
    # Obtener 'codigoVendedor' de forma segura
    codigo_vendedor = data.get('facturacion', {}).get('codigoVendedor', '')

    canalPedido = cortar_url(data['canal'])

    # Convertir el valor a mayúsculas (si es necesario)
    codigo_vendedor_upper = codigo_vendedor.upper() if codigo_vendedor else ''
    usuario = Usuarios.objects.filter(username=codigo_vendedor_upper).first()

    #if usuario and 'Asesor comercial' == usuario.idRol.nombre or usuario and 'Director GCN' == usuario.idRol.nombre:
    subject, from_email, to = f"Su pedido {data['numeroPedido']} desde el canal {canalPedido} ha sido generado", "08d77fe1da-d09822@inbox.mailtrap.io", (usuario.email if usuario else '')
    txt_content = f"""
            Registro de Pedido
            Se ha generado un pedido a su nombre {usuario.nombres if usuario else ''} {usuario.apellidos if usuario else ''}
            Atentamente,
            Equipo Vittoria.
    """

    articulos = ""

    for item in data['articulos']:
        articulos += f"""
            <tr>
                <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                    {item['articulo']}
                    <br/>
                    {item['caracteristicas']}
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
                <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:40%;margin-left:0px;margin-right:0px"></p>
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
                                    Se ha generado su pedido desde el canal {canalPedido}.
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
                                                <p style="margin:0 0 16px;color:rgb(255,0,0)">Hemos recibido tu pedido, está por confirmar para ser procesado</p>
                                                <p style="margin:0 0 16px">Hola {usuario.nombres if usuario else ''} {usuario.apellidos if usuario else ''},</p>
                                                <p style="margin:0 0 16px">Hemos recibido correctamente tu pedido # {data['numeroPedido']} y lo estamos procesando:</p>
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
                                                                Envío:</th>
                                                            <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                <span><span>$</span>{data['envioTotal']}</span>
                                                            </td>
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

    emailsEnviados=[]
    superAdmins=Usuarios.objects.filter(idRol_id=1)
    autorizadores=Usuarios.objects.filter(idRol_id=51)
    #emailsEnviados.append(to)
    for admin in superAdmins:
        emailsEnviados.append(admin.email)

    for autorizador in autorizadores:
        emailsEnviados.append(autorizador.email)

    for email in emailsEnviados:
        print('EMAILS',email)
        sendEmail(subject, txt_content, from_email, email, html_content)

def enviarCorreoAdministradorGDC(data):
    canalPedido = cortar_url(data['canal'])

    subject, from_email, to = f"Su pedido {data['numeroPedido']} desde el canal {canalPedido} ha sido generado", "08d77fe1da-d09822@inbox.mailtrap.io", \
    data['facturacion']['correo']
    txt_content = f"""
                Registro de Pedido
                Se ha generado un pedido a su nombre {data['facturacion']['nombres']} {data['facturacion']['apellidos']}
                Atentamente,
                Equipo Vittoria.
        """

    articulos = ""

    for item in data['articulos']:
        articulos += f"""
            <tr>
                <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                    {item['articulo']}
                    <br/>
                    { item['caracteristicas'] if 'caracteristicas' in item  else ''}
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
                <p style="margin-top:0"><img src="data:image/png;base64,UklGRowfAABXRUJQVlA4TIAfAAAv5wNnEH+hqG0jad+dGf5M721xsI0kqdFAAloEQP5BYYrX3lvLIJIkJ//Ah1kB+PeFhMyugfmPR/HlUpCQgoQwKYjJGGXiR37SjzykEznUt6tH6pN+hv6GfJp6u3qburt6NnU1dW1qNjVW+TfJxkFYsY5osCQeYQEe4E7g4R7m4B7mYB4cxW3bRvL+Yydpc/4jYgK4VMkvPJApGQoAJb+QwecbGcp+WNrbbVtZa2vbhi9RY1QGanxXxvH+fhz///etrEyBMYhnoZQzEf2fAN+y7datbdsWPqWAN5EUSfz/9zVXAYRkj26Pl4j+T4D4+v/r/6//v/7/+v/r/6//v/7/+v/r/6//v/7/+v/r//+/eJKmeVEU1U+LoijSNAnCkrS4VzWYr6t7cUsCrfhWVA3Y3lTFLQmpoltRSXC4Km5RABVnZQMUNmUWh0y3ewOUNvdbFCLF2QMofuRxWBTnNdBd53EoFOU1UF/ncQB0ewCPjyzsie8S+JT3ONi5VcBtlYU4Ud4Ax00RBTbxXQLXsowDmrgE3ss4kIlL4L+MA5i4BD8s48AlKsEfyzhgiQoJPimLKFTJGvBNmQUpSQU+WqfBSXQHXy2jsOQmwV9lFpDEFfhtFYciuQTflXkQElfgw1Ucftwk+LHMAo/oAf78iEKOpAGfbtJwIwffLgKN6AH+/YhCjKQGH2+S8CKT4OcyCy0K8Pd7UBGV4POPKJyIavD7OgolkgZ8XyZhRCLB/2USQmQSPsIsfMjgU8xChww+xyxsyOCTzEKGDD7LMlzI4NMsQ4UMPs8sTMjgE81ChAw+0yw8yOBTzUKDRH4skIYFiYTPVSYhQdTAJysjikYOUHLKdd5i1RyhjWX8rEQ1fLZ1RI5kGIfuTjKMj1+VEj7dBzkZ9kl8TYZ5/U0p4PO9EzOwM4onYdiz/KJk8AlntJQtODwl7Ow/KIl0oe/7nrO27/vONpmQkvZg+BnYWn9Pogas7oZ50/hbvc1Dy0w/rRv+ft+mp7IGmogSbM5+0p70e/IAi5/LgScey5MLNax45j62lkDFB5aXid+aHKxtZ42nH3PLQL/i+ftgBxR8NC/ltyYBW9sFDS8tccOBZvWkbICUjeiFf2qixhK1oIWLIqzf0bwebJARF1g+TvzUPMDOUaOVeqRKrWjn3pmDBxvVR/mpycDKdkNrN0XSU6O1kznIuQguBL80sbSi12ix7gia0eZNGZMxE5ge+k9NBTYOaLfuyFnQ7qMzBRUXxUP8pcnBxgVt3xUxC9quO1OQE5VV7GBBm39ZYmnDgvbvtAxov+5MyZimrsK571CdvywVWLigiwslPbqoO0NQ0USsyvuCJo8flhtYOKCbEx2ddgJ1awhymooKsuuEtv+wRNKCHl0dqFAHOrorQzIi6dT1XUXD8sNyB/NKO6M7InZ0djEEJUnEqrhJoC10Jxkv5xsbr+eXIgULN3RXtyQs6PDTEKQkFRXWnq467zJqCriacpveRjtSxMuYcj2Xs9mPFHA5pKPNb0NlwYgu74qACV3WylBN0qmre6KG6Q7SM0y5DDfSMww5WRYxWS0zjLmc34QMzCvtFK7uDej2YghyiohVYcuC9rjBKgz70F2swvCbdKtF7OUq34JIWjCj44trHbreGZIRRUWFueNQTXdyYHM4t8kB30sxMhxy+xIUYL5F5we3Wu3cZggKiqau7GBNIG8nY3+WPSfDeb80Epwm+QbE0oLFPXy6pHZ0vzcEMUEUVLzhhLZ6K3AZ5o4D7usFyfAb5hegBPMKCdSdQxsSuJgqKTpUOO2yavmSCKc87QpuJBGeeV1+MVg4UYCHcmZBEltDEBM0dcVMoI3kSiLc8rQquNMB3/HyK204SMBdOTIijaOpB0EUVBCrpmquJMIxT5uGW7Ez/O3ii8HCDolc3HgikbspSAk6dN0qqsRVhOsoFhO3mnD/32uvtGGmAmcXOk0FtqYqgqYuGU1oM3k64PywiPdofwx/f730YrBxJwMH+5RGMkdTkNBDQYVlc6i6pxPGnKIVhq7DNsVd4z74vyuvtEEhoZ1takc6V2MlQU3XbFjD4kiCBR+D/pWzsEXSBYN0ChHR6mlDoC2cXpr948KLwcYnJbqzbEVCtTGI6Vm6YHJCW8hRhWEVuiiHAYamQx0GXRzB7LTLbdDfq0WTP194pRUTJbgrq2YktTVW0kNRhWmRVaejBT1PUnaDrMmqKHRZoiaNl4v+XtfySeqTDfC6i6QVKym42zQgrb0xiOhpusNAoGVyVHQ8Sd11WApoWUgprMAgNf8VmpDlZIN/X3YFWLnRgos9PRI7mivoWTo2aKrDkbBukuGha9eGqpO6a5IuvwqdrLvBPy67xg6kdrSl09RM5iQ9FFU4dVE1HTWoK1kKq9K1qglkGBRYqvFP6LQx6P5+1WXAEg52qAOpnc1BRk/TFdWENpCjqGIxoaqCXCqaw6JomopGLp22Nt2fr7qKKd1ZsSO5mwU1PaKDaIrqcLSgPsh26calpDktuubQ7Z/fghiYQt1asCBHkJBDWdc1rFqOmm4ZUVDVHdNiaJI/0v3poruzhbsyNiFPJT1dlxQd2kiOkiqQdVHlHfRIQYUXneQLV1MDMiUjckSHdS2rmieoi1lVxXeTvgMZMIaLmQ65gowcyrp2aUG9HA1dMxsq7FgW55fowRoOJlrNV0VP14VLTZXJUdONJxgW9TsUA2/4PE/tyBfE5IgO80pQdU9Ft/yMDYdF1NQvTc6d7k7bkLOcHMq648KEWjwl3TBvW6omGAxo25em5g4PddKCrDX0nDq+UFSFPLHO8aWuQdMl1dg3R6s1XeZvQAzs4a5OGZA3SMghVuH8i1WnKzzDUvHUNKhp62wlwuMVl3sALmc8kbs7PUVX/ujQMvFDUQOe1xrUecNZGF6vuNoHcP5Zp9lr6Dl1kFdZVVyNp+gqoMpfK0HfraQGOL7gYvACHH6iNLIHMTnEuv5iQT3fkbAOyHWMcdYIQyZbqQzXF1zuCdi9p3b0gJyeoksvmirQO6JusbPajADnF9zDF3T31oI+UNNz6rD+CarjbcxrlDwFMq1wf71F4Au4qzdm9AKIyCHWNSIaUK93EUi52NEwKfh+3PwB998N6AkZPYcuEFFRRXoXVUOT3VSyLPiClB6By6sefaGkZ+owSVjV3kUhdYHXQpYnviGNT+D4S6e9oaGHgu6gDvW6XfJ5DFI3eC1kKfwNicErcABQO3oDJPQcOqakyuRsGdBNT3itZFpgyrmOSRfTf36ZZ+AyH+gROT1ThwZ190ZPsdhJGGQqsEwnaf/7K32DR0cPeijoWCf3G/dIcMmVjJsBn6T/76+5NCRBh05fyF16hg5lDiaxC1lHHU/6PsRwaUBMz9p3PkC9RVBEop75Gue2yF6gP+kLcbs4Mnoo7mLyV3X5DieUg/6dvR4plVrbWLR36BJ9I+4Xx52gtqvc4NTxHYoikveu61+J6uKoCVq7xg2WDucNgiK5q7rxlYCLAwiiuCfQDSjo0g3wNPSNSBjal2maNhf2eZqm9WAnJajtOW5RdBjupgbyjcq40XMLr4fDLj218LrfmMkIWnvmLbpBEG9DFeVuw6TjP76CmbWFd0dt0drCu0/Nyp0gijsi3UIMUO6G0OVezaLjv76KlxF+2GlrRvih2jmpKOo72j2oGKDIDukZKNdEByCmVOrLc7zc0XTRoOM/v4aVAX7caUsG+LHaGZEUyY51k2GBOM3Owvh3XiK2sE25DpOhQ1cV/PcHnAxwYqetGOBEtfMBEUGU7RLdhJIFUKbBbJnxZ79WvLzMXVRiwPPaivjvL+VkhlN7G2Y4tdV8pBR1u36bYQOEo48/5ug1MS7Xa8MVwGUpKOiAKn+tCutr7cbIDidP5nY4+clHRpHYyW0oGW1WUPIFcFUcFuDSxxijZthfawUj/VlwGOvPgpWNgiLKVpnus/h2k50BUS5NE4/XWsnHAqf3phY4vWXjQVK3Om9E/XbU3YHnFUrfj4qP9jzYDLXnwcJFRZIYMd2Jyu3oZG/gdWV8Pxo2FjDYm1nBYMuFJImKTbkXldvRit4Qr9Dx9QA2WhNwGHmagIUJoOm0GTej4m3oOrtDvSLRA7cv2AZGRxMHGO25iEkitgh0NzqcLVXDDVku0OR9PMd/eCkbgxllYjYDBxMpTcXiuB+d7CmTtuCW9QpN3hUnfcOUGVgNdIZmnzst5gOQFD9FNA1qTi/jpnCJVtxzCP2nd+NiBcPjeQcY7pnI7QqqaEZBl8hcdGUD0cguuCzSnlCHSdfnqNEE8xJRZbs4iIimgv9TK7gYTXXnzaZA81DYdbKCh91MmjjtqGvC2kK0jrAplJP0wqooZDiiRVPQKmwTOr2O145vVGcK9GlPY5uHEI1a0utSB22d7Uh/5nrSVjlrTq+PNsnhrMkqHX2RaYGWhWyzwaEhkp5UXE76W/qRXuc66RsFxrfTlLHJSz7G2WtJKb7glFKtY5H5hHqQsbAu6f4dtaT0T0ylDfoOlkxs5qazDjD+5KHyNN9FVcj8cPKVrJiYzQ1nbea6i0igXnbj12Ey1581mYOL6FRF+tl4mlNnjRboa6iq0oauyz8GvTk4q7dgu4ayo6Kr/1+VVNFOWHf+GHQWHP+3gGV2QL9+DMDC7SSwcL6oklWHPtLPzHQNZR2yWMgBw/5/VtUAXJdGWoAhy69B50xvwXwNDQsAsZ5DXsxRM2wr/Rr0hG3XEAUbj5F+MI6Lr96E5y8GnjxcZsL36PR7MDozWYAXEZ236PSDMJnrz1rNqcuIqj/u9F0tmVjMDWft5vrriJq3MOnLWjCxmZvPQmVs5OFu2yppc61trA+ETnZ1CP0maHPbab2xhYfCsgansbT5YZAUP2XR95ULbI3h6ZOxw0MGPHPu8kkQrcIeuCz6xt64GE09z9tNtchDbldx9W85Pwki6XlX7kLf2ZSLzdR8HipDIxOpXdEdEPon8e+oOdhwqoO+t2xga+gwMBjafQS3DP2zeDlGq/VIr2ut5xD67kZsTGZ6NLiaaZGJmD4gjo/jv00ZtdaUUqq1DvmUBBvazGICWyMTF4ID4PiiHFAen1LDBQ4mWjQ6GTmYkEwgrm9Jh7p/SBUbh4nJjDYxIBMVF+D5Jam6+iGVbOBwntJmcDRwcPFgA+g/LQVFep22Mw512oyGtTptxDP3rn2u5BSMoP+yZARNCgDWE3A6q0Pj81mtPqUFAOg1MTknGD8sKTm6g1/7M7A/R+3m8HnShqfCS6VpSVnh+bsiyOnBgFanLGih7k6Z8Nz2BXS0RK4l+nuNMXotcQui/K5IYhZ4qfZTcFcnLGjlrk4Y8OT9qX6BhRIp6Lh4HmyH/LtSEdO+WDSevKsfLWjp3v5owPP3Fy0lFUVE1JMZzp+VgpYVXnan4dG9p1a0VvfvqQXP1+oF7ITciSLqwSrIr0pGy/gKOn0W4qTeGDTavLRvPA88X3fweiEkJ4vkMEL9VUlo6X8DnT4N9fJsAVQ/H2j78mwBoB8PNKg7+O1ESEoXUWcbXj8qgqAnAECnTyN97wAAemoEZTTZBIenNca61RhDPrk1xnyQNYa8lzGGvJuKlAEAhuUX6DQ/u4JftwlAHXTUtNFkExYPo5XE+DvleoorOWuO+Dum2pcjGTUnxuuU63hHs5XE+Dumeq57nTUxXsfc5sPJqCUxLsZU+3wXd1L0/JwR1S+gdm5WBb92iMeGxm0qiaNugratZ4ZlbOJEWoJlKKeL1RIMcxcT6SUxXqfclp30khivU26y7ywMy1jXJmk54mVITS6twtCGJja9vk66VK+PLatG2HLu8g4yUl5PL0CtvMzwekErbcqoo8Mk7FkHw74sB6vAPlTZNTKs+Vg6iVDysJIIJc89UgPs09gScZnlr5lgys2iw+2w6xFby3y+mCCtXgCMjOgBXrdITUKeBAvMDXJgc1mbpGAv9y0jYeshmgF1sRpQ1y2VsTdNuwHleCUHzOPURT+HVQ/YnubTiYYenH4D/cHF3sFvF2qkII9Ok8PuZGzntuVkbO92cmA3j13pAUbA/uprBGzkroLfZDMCXB7ycA+CtPoNqJWHGX7fIjUPBihZBCspcJnF7oDDYDYDHPanO+AyiqOKzV2xHMFCDngN89lygnD6HcBT03f08OZCTs7BaYFlIxFOo1gVuBSjzvDI69EkwSlPL5KwfVwbt5oRjvujxRRp9QaohboJ3m2RnIQDChbdZDLcRrGp8DlsOpy2J5MItzx9SMR+Xk8xGa77k4mGIJzfAeh3yrYW3t7IkYKFw6JYLIbjaHLiRh1e84NJhOMgHiTCY3qIyXDen6ykCLu3AIaDqq2H959ITsnDtIgGEuH6MBC+0YTb9GAJrpODM8Ln+QiT4X48WEbS9gOA4aDoGOCH6qAn44GCAQwynJ+6ivsIfwAHnLd9DKfhCSTAP8tzRSTh+BOA4aBmG+DHM9ITM1EspqrBexCN8I0y/MbHGvDOa5vf8wI5ioqEO+bnEhVJuv0RwLBRsvTw8w7pqQUTzWJoFlvwcQoR0WjRAlXTYJj7pH9HL2HLCc9PJcGCy7mIiEZLFiiPka8EP/lawz3Hc+Uk4XYCQLdoGo6phRPVTlDBxbComgw9V6GLIxqwKKIuLro8j2AmwSymlFgTn6rC8BC6uJIB1lNALhQ//dJiI061jlFrZqvwXDFNOJ4BAMPqnF56OHdGghIuaN+APk5SFh3aNYE6Cql7eiGqClM+Br2Us/CV9FALeh6kbAbFV0wpmfULi71EulxgmjpdHMkG/bFETZPuzgFQw+qQXp5w9hMJagQbbJAVSReF1EUXrg3dIsuRgERaYZND6Ko0frqi40nqpmPxE7rQvz3ZlAsk43XRlXGdLi9Y8knKEUzic91pwl2d9OtzPlzYpg7ObzVFdz6SQbo2oeZFhlGFeamqMhnPIaoOQz5JK/WP/EzCukGGSYXuhTtdbCbxyt9VV8m+WMRFaokWmI+VEIWrAQBon/Nukd6mHoyqHSlKvKHoGlkO3bGlWllGi0GGM75oz9SgPshy6bKTuOhyt8C9FgyDkKFEi+OxRE0UjkZe9uO8aVP7Nj1bML4gRY3go+5iVSDbqIqPMGHYyPYAwPJMQcViQkXFPoqQMluMWzWLSabTIjxXThUOxl73/TSt27a/pbdtm6ahb8HOEUm6e8MJdTfqKsiO4uYwSGQ9SjrpkSbUB9kOFaaHQmrhh4kGlYyrASZZMVm6s8P9AWmKvaGoWIxEN3aweAkGw0z/HFW3jIhV/7CgkOFhUO+0oGexEjZoZImKKtQdBx3SVAtvYFUm66iqO5CdLOgjvZ2oimSdVX81V8hyPkszqGR+GGS6MrLwUPR1mqjMGybUzSyrypWmQxIX3aC/HYH6MKuqPxuLYkLhUbLBslsGTFckycJdUddpJCryhqYbZlWVrgwDcPdwGMjbGbpu1lV/MPUHIdusS3diXaSNQYf/kSVKunBXtHUaiSqFNxQduQlXyAIIfV/SRXo7VTfMhgpN/ZmM65NM6OuOw+DfdCWE4a4o6zRSlbJy7En3waVsAoS6NkF/vJ+sIz//c6M9yWkwdnSDf9AlasLw6OjqNFLVCFbSHqjjMC9buhGA2GXDMujvJ+mGedP9243xJNWAdg6DvxOWUYa6o2pAV2cLMu7KBdF5vkTBDEAZZsNgvB/cmL+sC1vI4G+ECUkZ6oGmEZ2dzMmIl2BQL4yn6DuA0I1OA/ovJemSsz9TVtixuYI4UbSgu6O5u+AF74DiFoCrWNQPYH5yUVf2pLcS27G6g6uipt3R4d5czMu0GBfOx1i8BwjdA7+f8clBXz8HUVoxOYR7R0uv0eXWWCl46XvqY9DcBaS1L32LYiueLqEeKZnQaQ3GE2YOC3oiGrwLfH7LRGmDcgpxVVS0O7q9GqsEM9EgPBPNsAvo/0v899JIbYDdLdRPGkaNjo/GUmYWDPMzZB1J2Yb+v8MfxaUhKhtmxxBX5V63ofOtqUow0y3qM5wGRCPtwvif4e8XR2pD5xzq0TE1ofs7mE65SRbjEQoZ97ApyBZ8UEVcHKKyAA7nEPfeJXUggaOpSjCzYElXm46TzzzIfqQtqJ9O8pk7+UjZE3V/oS6xYSQAR5eAhNZUys1hkS4NXaIHXAdvYNkiHwDdlCXWpT3Q/506UVqgCNDKqYGABQw/BDPCFm1PeAIi6tkMdct4O/LJJV3YIm8otgAW9yZwWmn3OlMxNwWW69LU4SGIVg1G4cIwaG+HDNYHhy3D4N/kibsFrXNauQWTcxsYLgUzE5aJrhvIUxBRDyZYO8r7Yd34nA6DsaMZ/Je+SJqD2bUJHFeHa60hGTEj0aQrWDcehKixxfmXGIQ78U2Srn1O1aDtyDoWDOYWKO3WoVyDwbEZDBeCmQJLJmXStUehGQzqX8Q6rBtBjMquQ1c+p2GQd7AucSAac/B06wnub05pZagRzBSYVs2hy89Ck3ckg3qn06ZiV9OFz0kMIHYd+spCagGsLq1AYKtdeoLhlJkCUxZN10GehbouXzgMgp9lcJh0bBs6zI+JgkGzSwaTBfGwQGl3DkUBDA7NYPghWJEM20raZVAfRnTpwmmAbldDXJfIgC069pFB+TySWTEIZgN6Jh4jaQ46Z3QHNC7O7GBYxqyMAFsWFQUdy7OQrlwQCxYjSQDKJjRdh4esw/o42KwboFklg/ImRG4BDK4MQOXmiFamCsHITLDupD90OB6uXqBogGwzGADitWTAomlw0QzSx4FpJRa8bCoMx7sQlQUwuTEAmWp3QndguBZsSE8wT2Q4DNDdSUlVzNaWZoFiIAdeX8sGiHJJCnwsAxxv7jQoVpQNEMWiwzDQ20xsgMWFAQhVuwO6A9MJDzJqxkZeFhQM0Pf0HEJXNABcxajqzivLBFk0PcCkWiDOCyPACSUD1D1nCdwebRhgWHULRNF1WPb3IQobYLJvAFLVbp3uwHQhaAr1akoJu08yrRY4xOwsDACsyPiXq1hM1q0rlE3AVS5ID7h4bZgAZf4jPcFe1y2QxWweAf+uJ1sW3P+YhXleILYAn4qVYRnondY2wGDbAMSq1bK9BdO1IMp5JVthC3ATg9UL4895Lb0A+FiqyVAHujxsAKR6jjF6Tbg+LpERgJQituooWIDrMpCzBPw5nowsgFBqrTkAwHGlmgCxr7/OAtv+VhJpA/TaJt0BvZNVqwLjiQ8Usq4mAHIbF+aoOeDyuMZ/AIhtXZkFhsc1SlbWimy23aCbAMhtyF9z1BJxuT1aMrmcrgjbAAip1JoSrCO919wKUJs9qwKKe22NHsF8ITygkLmw0UtOKcJUAWVI9WUJMF2KcaP+GBSNXnJKEab10eouvkLNbPd8M6KyAmDUdugnEK0WS7YWzFfCAwptPHfYb9mcSFtcyTUKjzF22D/b2IVLlG5R6d1G0g5Qiw2zArr7zYJjAAtl7AGdtuY3MlXCnkhZvfA+qh8GBU+Lb5Dp/aaWALSLqaUF2ofd0DGAlTfBXpi0V+LNgqOD9OM+EnzwdEDpw6ie6PQX5Q2JwhaAdjrOOyYF9PeLgW0AO++CvUNo9+J7JT+RLLufqKHTBU/yINHd+WzCnqh7i0JvubIGAJ7zccYxd8CkGlZ9xja2YGktuIuDHE72tq4VN0FM6HBzqKg44EkuSKK38WxUXVH3FYXecyQtAoB2mLa3p2cLvPbjsr27Tj3YK2PmQiefEn0xXe9e4iTj5oSXTuK2uMgJSXYmD0dxS1BRZ0dF6F0ndnl8KihN/vJJbuVwVRUSfCQh884ewiRDiZuykBui6irT0y3ekXQ0gxdu9MazjygXpB7OYlvkegQ/B2ln8FBp50r7DiFTSTu40UsvNJOfJI9Hkzc0A5LqIy966+UHVApaF/sJuS/y34MLLov0UnlXXrS5hz1lkXm1y4ucEfXgIw8yvFG2IklmvCyIVtmXBr376uOpBbUzeEi5novu2vMuLl3IVnrcUSY57MGMy6KdM9mkQX8f13juIBp5F+cuZJs0fFpR0vA0I+rBhk+yXgfv4DLp/Uf1h9NE5BCddWcfY9LtV89sFUqbtHW1ZMK5CzmdRzAI5aTto7CGy6TL40iJAYSUm9Bu6SVYhVwHbZw1pfgPp1SakP2oKcV/OKXShbaeWZe70M6zBJtQutBHmMiPRibC09dZS4oXYsq1D/I52pHiXynVPsn3OmtO8QWnXM9FTkfN6VVIddDd11lLShdCSrUNobc82pH+rG2QwzVqSfGvkHI9F32OifxkEhEU3j6YTASG2ceSieAw+1ByESDeP5JSBInlB1KKQLH8OEoRLJYfRikCxvKjKEXQeP8gShE4Zh9DLoLH7EPIRACZyU8gE0FkIr1PJiKQTGrPaxIRTEa119WRCClLjytFYJl5Wy6Cy0R6mUxFgBnVHlbHIsy8e9ddBJs36VXyJgLOqPKoKhZhZ+5NhQg+k9qL6kSEoIUHFSIQTWrPqRMRjubSY2QhgtL44S1VLELTtPGS5iZC1EJ6hyxEoBqVnlFGIlyNHx5RxSJsTStPqFIRvqaVB1SpCGPTirkqFeFsUjJWpiKsje+SJXmPRXgbZQ07TR6JQDctWSlTEfJGWc1EnUci+I3vDXnNPRGBcHJvCGvuiQiKk6Imqb4nIkCOs4ckRT6yWITLSf6QJMhHnojwOcnL2qm6zBMRUKd5WTlQlXkqguw4zYuqsqKqijyNRfidpGlRFGX18kX1siyKIk0T8fX/1/9f/3/9//X/1/9f/3/9//X/1/9f/3/9//X/1//fxQI=" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:40%;margin-left:0px;margin-right:0px"></p>
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
                                    Se ha generado su pedido desde el canal {canalPedido}.
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
                                                <p style="margin:0 0 16px">Hemos recibido correctamente tu pedido # {data['numeroPedido']} y lo estamos procesando:</p>
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
                                                                Envío:</th>
                                                            <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                <span><span>$</span>{data['envioTotal']}</span>
                                                            </td>
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
                                                                <a href="mailto:{data['facturacion']['correo']}" target="_blank">{data['facturacion']['correo']}</a> </address>
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

    emailsEnviados=[]
    adminsGdc=Usuarios.objects.filter(idRol_id=59)
    #emailsEnviados.append(to)
    for admin in adminsGdc:
        emailsEnviados.append(admin.email)

    for email in emailsEnviados:
        sendEmail(subject, txt_content, from_email, email, html_content)

def enviarCorreoVendedor(data):
    usuario = Usuarios.objects.filter(username=(data['facturacion']['codigoVendedor'] or '').upper()).first()
    canalPedido = cortar_url(data['canal'])
    if usuario and 'Asesor comercial' == usuario.idRol.nombre or usuario and 'Director GCN' == usuario.idRol.nombre:
        subject, from_email, to = f"Su pedido {data['numeroPedido']} desde el canal {canalPedido} ha sido generado", "08d77fe1da-d09822@inbox.mailtrap.io", usuario.email
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
                        <br/>
                        {item['caracteristicas']}
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
                    <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:40%;margin-left:0px;margin-right:0px"></p>
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
                                        Se ha generado su pedido desde el canal {canalPedido}.
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
                                                    <p style="margin:0 0 16px;color:rgb(255,0,0)">Hemos recibido tu pedido, está por confirmar para ser procesado</p>
                                                    <p style="margin:0 0 16px">Hola {usuario.nombres} {usuario.apellidos},</p>
                                                    <p style="margin:0 0 16px">Hemos recibido correctamente tu pedido # {data['numeroPedido']} y lo estamos procesando:</p>
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
                                                                    Envío:</th>
                                                                <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    <span><span>$</span>{data['envioTotal']}</span>
                                                                </td>
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

        emailsEnviados=[]
        superAdmins=Usuarios.objects.filter(idRol_id=1)
        autorizadores=Usuarios.objects.filter(idRol_id=51)
        emailsEnviados.append(to)
        for admin in superAdmins:
            emailsEnviados.append(admin.email)

        for autorizador in autorizadores:
            emailsEnviados.append(autorizador.email)

        for email in emailsEnviados:
            print('EMAILS',email)
            sendEmail(subject, txt_content, from_email, email, html_content)

def enviarCorreoTodosClientes(data):
    canalPedido = cortar_url(data['canal'])

    subject, from_email, to = f"Su pedido {data['numeroPedido']} desde el canal {canalPedido} ha sido generado", "08d77fe1da-d09822@inbox.mailtrap.io", data['facturacion']['correo']
    txt_content = f"""
            Registro de Pedido
            Se ha generado un pedido a su nombre {data['facturacion']['nombres']} {data['facturacion']['apellidos']}
            Atentamente,
            Equipo Vittoria.
    """

    articulos = ""

    for item in data['articulos']:
        articulos += f"""
            <tr>
                <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                    {item['articulo']}
                    <br/>
                    {item['caracteristicas']}
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
                <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:40%;margin-left:0px;margin-right:0px"></p>
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
                                    Se ha generado su pedido desd el canal {canalPedido}.
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
                                                <p style="margin:0 0 16px;color:rgb(255,0,0)">Hemos recibido tu pedido, está por confirmar para ser procesado</p>
                                                <p style="margin:0 0 16px">Hola {data['facturacion']['nombres']} {data['facturacion']['apellidos']},</p>
                                                <p style="margin:0 0 16px">Hemos recibido correctamente tu pedido # {data['numeroPedido']} y lo estamos procesando:</p>
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
                                                                Envío:</th>
                                                            <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                <span><span>$</span>{data['envioTotal']}</span>
                                                            </td>
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
    canalPedido = cortar_url(data['canal'])

    subject, from_email, to = f"Su pedido {data['numeroPedido']} desde el canal {canalPedido} ha sido empacado", "08d77fe1da-d09822@inbox.mailtrap.io", data['facturacion'][
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
                    <br/>
                    {item['caracteristicas']}
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
                <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:40%;margin-left:0px;margin-right:0px"></p>
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
                                                <p style="margin:0 0 16px">Su pedido desde el canal {canalPedido} ha sido empacado.</p>
                                                <p style="margin:0 0 16px">Aquí están las evidencias de su pedido esta empacado.</p>
                                                <a href="{data['fotoEmpaque']}" target="_blank">Foto del empaque</a>
                                                <p style="margin:0 0 16px">Si no puede visualizar copie y pegue el link:</p>
                                                {data['fotoEmpaque']}
                                                { '' if data['videoEmpaque'] is None else f'<br><a href="{data["videoEmpaque"]}" target="_blank">Video del empaque</a><br>' }
                                                { '' if data['videoEmpaque'] is None else f'Si no puede visualizar copie y pegue el link:<br>{data["videoEmpaque"]}<br>' }
                                                <h2 style="display:block;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:18px;font-weight:bold;line-height:130%;margin:0px 0px 18px;text-align:left;color:rgb(35,85,225)">
                                                    [Pedido #{data['numeroPedido']}] </h2>
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
                                                                Envío:</th>
                                                            <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                <span><span>$</span>{data['envioTotal']}</span>
                                                            </td>
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

def enviarCorreoVendedorEmpacado(data):
    canalPedido = cortar_url(data['canal'])

    subject, from_email, to = f"El pedido {data['numeroPedido']} desde el canal {canalPedido} ha sido empacado", "08d77fe1da-d09822@inbox.mailtrap.io", data['facturacion'][
        'correo']
    txt_content = f"""
            Registro de Pedido
            Se ha generado un pedido al nombre de {data['facturacion']['nombres']} {data['facturacion']['apellidos']}
            El pedido será enviado en pocos momentos, sera despachado.
            Atentamente,
            Equipo Vittoria.
    """

    articulos = ""

    for item in data['articulos']:
        articulos += f"""
            <tr>
                <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                    {item['articulo']}
                    <br/>
                    {item['caracteristicas']}
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
                <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:40%;margin-left:0px;margin-right:0px"></p>
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
                                    Hola {data['nombreVendedor']}
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
                                                <p style="margin:0 0 16px">El pedido desde el canal {canalPedido} ha sido empacado.</p>
                                                <p style="margin:0 0 16px">Aquí están las evidencias del pedido empacado.</p>
                                                <a href="{data['fotoEmpaque']}" target="_blank">Foto del empaque</a>
                                                <p style="margin:0 0 16px">Si no puede visualizar copie y pegue el link:</p>
                                                {data['fotoEmpaque']}
                                                { '' if data['videoEmpaque'] is None else f'<br><a href="{data["videoEmpaque"]}" target="_blank">Video del empaque</a><br>' }
                                                { '' if data['videoEmpaque'] is None else f'Si no puede visualizar copie y pegue el link:<br>{data["videoEmpaque"]}<br>' }
                                                <h2 style="display:block;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:18px;font-weight:bold;line-height:130%;margin:0px 0px 18px;text-align:left;color:rgb(35,85,225)">
                                                    [Pedido #{data['numeroPedido']}] </h2>
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
                                                                Envío:</th>
                                                            <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                <span><span>$</span>{data['envioTotal']}</span>
                                                            </td>
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
    canalPedido = cortar_url(data['canal'])

    subject, from_email, to = f"Su pedido {data['numeroPedido']} desde el canal {canalPedido} ha sido despachado", "08d77fe1da-d09822@inbox.mailtrap.io", data['envio']['correo']
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
                    <br/>
                    {item['caracteristicas']}
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
                <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:40%;margin-left:0px;margin-right:0px"></p>
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
                                                <p style="margin:0 0 16px">Hola, tu pedido fue hecho desde el canal {canalPedido}</p>
                                                <br>
                                                <p style="margin:0 0 16px">Aquí tienes el link del archivo de guia</p>
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
                                                                Envío:</th>
                                                            <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                <span><span>$</span>{data['envioTotal']}</span>
                                                            </td>
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
    canalPedido = cortar_url(data['canal'])

    subject, from_email, to = f"Su pedido {data['numeroPedido']} desde el canal {canalPedido} ha sido despachado", "08d77fe1da-d09822@inbox.mailtrap.io", data['correoCourier']
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
                <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:40%;margin-left:0px;margin-right:0px"></p>
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
                                                
                                                <p style="margin:0 0 16px">Por favor señor courier: aqui tiene el link del archivo de guia</p>
                                                <br>
                                                <p style="margin:0 0 16px">Pedido hecho desde canal: {canalPedido}</p>
                                                <br>
                                                <a href="{data['archivoGuia']}" target="_blank">Ver archivo</a>
                                                <p style="margin:0 0 16px">Hola aqui tienes el link del gps</p>
                                                {'No hay ubicacion' if data['facturacion']['gps'] is None else f'<a href="{data["facturacion"]["gps"]}" target="_blank">Ver</a>'}
                                                <p style="margin:0 0 16px">Ingresa al siguiente link e ingresa las evidencias de la entrega</p>
                                                https://vittoria-test.netlify.app/#/gde/gestionEntrega/woocommerce/enviado
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
    usuario = Usuarios.objects.filter(username=(data['facturacion']['codigoVendedor'] or '').upper()).first()
    nuevoTexto='''<p style="color:rgb(255,0,0)">El pedido ya fue despachado, está pendiente la confirmación de recepción y pago del pedido por parte del cliente.</p>
                                                <p style="color:rgb(255,0,0)">SE LE INFORMARÁ CUANDO LA VENTA HAYA SIDO CONCRETADA Y EL PAQUETE HAYA SIDO ENTREGADO.</p>'''

    canalPedido = cortar_url(data['canal'])

    if usuario and 'Asesor comercial' == usuario.idRol.nombre or usuario and 'Director GCN' == usuario.idRol.nombre:

        subject, from_email, to = f"Su pedido {data['numeroPedido']} desde el canal {canalPedido} ha sido despachado", "08d77fe1da-d09822@inbox.mailtrap.io", usuario.email
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
                    <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:40%;margin-left:0px;margin-right:0px"></p>
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
                                                {nuevoTexto if 'Contra-Entrega' in data['metodoPago'] else ''}
                                                    <p style="margin:0 0 16px">Pedido desde canal {canalPedido}</p>
                                                    <br/>
                                                    <p style="margin:0 0 16px">Aqui tienes el link del archivo de guia {data['archivoGuia']}</p>
                                                    
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
    canalPedido = cortar_url(data['canal'])

    subject, from_email, to = f"Envio de despacho desde el canal {canalPedido}", "08d77fe1da-d09822@inbox.mailtrap.io", data['envio']['correo']
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
                    <br/>
                    {item['caracteristicas']}
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
                <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:40%;margin-left:0px;margin-right:0px"></p>
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
                                    Hola su pedido desde el canal {canalPedido} ha sido rechazado por:
                                </h1>
                                <h1 style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:30px;font-weight:300;line-height:150%;margin:0px;text-align:left;color:rgb(255,0,0)">
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
                                                                Envío:</th>
                                                            <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                <span><span>$</span>{data['envioTotal']}</span>
                                                            </td>
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
    usuario = Usuarios.objects.filter(username=(data['facturacion']['codigoVendedor'] or '').upper()).first()

    canalPedido = cortar_url(data['canal'])

    if usuario and 'Vendedor' == usuario.idRol.nombre:
        subject, from_email, to = f"Envio de pedido desde el canal {canalPedido}, rechazado", "08d77fe1da-d09822@inbox.mailtrap.io", data['correoCourier']
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
                        <br/>
                        {item['caracteristicas']}
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
                    <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:40%;margin-left:0px;margin-right:0px"></p>
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
                                        Hola su pedido desde el canal {canalPedido} ha sido rechazado por:
                                    </h1>
                                    <h1 style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:30px;font-weight:300;line-height:150%;margin:0px;text-align:left;color:rgb(255,0,0)">
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
                                                                    Envío:</th>
                                                                <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    <span><span>$</span>{data['envioTotal']}</span>
                                                                </td>
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

def enviarCorreoNotificacionProductos(data):
    usuarios = Usuarios.objects.filter(idRol=53).values('email')

    canalPedido = cortar_url(data['canal'])

    if usuarios:
        emails = [usuario['email'] for usuario in usuarios]
        subject, from_email, to = f"Su pedido {data['numeroPedido']} desde el canal {canalPedido} ha sido generado", "08d77fe1da-d09822@inbox.mailtrap.io", emails
        txt_content = f"""
                Registro de Pedido
                Se ha generado un pedido a su nombre {data['numeroPedido']}
                Atentamente,
                Equipo Vittoria.
        """

        articulos = ""

        for item in data['articulos']:
            articulos += f"""
                <tr>
                    <td align="left" style="border:1px solid rgb(229,229,229);padding:12px;text-align:left;vertical-align:middle;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;color:rgb(99,99,99)">
                        {item['articulo']}
                        <br/>
                        {item['caracteristicas']}
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
                    <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:40%;margin-left:0px;margin-right:0px"></p>
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
                                        Se ha generado su pedido desde el canal {canalPedido}.
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
                                                    <p style="margin:0 0 16px">Hay inconsistencias de los precios de los productos,</p>
                                                    <h2 style="display:block;font-family:&quot;Helvetica Neue&quot;,Helvetica,Roboto,Arial,sans-serif;font-size:18px;font-weight:bold;line-height:130%;margin:0px 0px 18px;text-align:left;color:rgb(35,85,225)">
                                                        [Pedido #{data['numeroPedido']}] </h2>
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
                                                                    Envío:</th>
                                                                <td align="left" style="border:1px solid rgb(229,229,229);vertical-align:middle;padding:12px;text-align:left;color:rgb(99,99,99)">
                                                                    <span><span>$</span>{data['envioTotal']}</span>
                                                                </td>
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
                                                                    {data['facturacion']['callePrincipal'] if 'callePrincipal' in data['facturacion'] else ''}<br>
                                                                    {data['facturacion']['numero'] if 'numero' in data['facturacion'] else ''}<br>
                                                                    {data['facturacion']['calleSecundaria'] if 'calleSecundaria' in data['facturacion'] else ''}<br>
                                                                    {data['facturacion']['referencia'] if 'referencia' in data['facturacion'] else ''} <br>
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
        for email in emails:
            sendEmail(subject, txt_content, from_email, email, html_content)


def enviarCodigoCorreo(data, emailCod):

    if emailCod is not None:
        subject, from_email, to = f"Su codigo ha sido generado","", data['correo']
        txt_content = f"""
                Codigo de verificación
                Atentamente,
                Equipo Vittoria.
        """

        html_content = f"""
        <html>
            <body>

                <div id="m_-2286063398718872391template_header_image">
                    <p style="margin-top:0"><img src="data:image/png;base64,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" alt="Mega Descuento" border="0" style="display:inline-block;font-size:14px;font-weight:bold;height:auto;text-decoration:none;text-transform:capitalize;vertical-align:middle;max-width:40%;margin-left:0px;margin-right:0px"></p>
                </div>
                <p style="margin:0 0 16px">El código es: {emailCod}.</p>
            </body>
        </html>
        """
        sendEmail(subject, txt_content, from_email, to, html_content)