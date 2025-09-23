'''
Modulo que controla las operaciones asociadas a transbank, a nivel backend.

Actualmente: contiene boilerplate y operaciones basicas
'''

from transbank.webpay.webpay_plus.transaction import Transaction

from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys

URL_RETORNO = 'https://prueba.com/'

class Pago:
    id: int
    total: int

    def __init__(self, id, valor):
        self.id = id
        self.total = valor

ejemplo = Pago(id=1, valor=15000)

def enviar_pago(pago):
    tx = Transaction.build_for_integration(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY)
    respuesta = tx.create(str(pago.id), 'sesion', pago.total, URL_RETORNO)
    return respuesta