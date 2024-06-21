import requests

from ...config.config import FAC_URL, FAC_USER, FAC_PASS, FAC_AMBIENTE

from ...MDM.mdm_facturas.models import FacturasEncabezados

statusSRI = {
    'A': 'AUTORIZADA',
    'N': 'NO AUTORIZADA',
    'D': 'ERROR FIRMA'
}

def verificarEstadoFacturaLocal():
    resp = requests.post(f"{FAC_URL}/auth/login", json={
        "username": FAC_USER,
        "pass": FAC_PASS
    }, verify=False)
    token = resp.json()['data']['token']

    # Nota en el campo environment de la api de Facturacion Papagayodev 0 es para ambiente test y 1 para Produccion
    ambiente = '0' if '1' == FAC_AMBIENTE else '1'
    resp = requests.get(f"{FAC_URL}/receipt/invoices?environment={ambiente}", headers={"Authorization": token},
                        verify=False)
    data = resp.json()['data']

    for item in data:
        print('exteranl', item['externalId'])
        factura = FacturasEncabezados.objects.filter(id=item['externalId']).first()
        if factura:
            factura.estadoSRI = statusSRI[item['statusSri']]
            factura.save()

    print('Termino de consumir')