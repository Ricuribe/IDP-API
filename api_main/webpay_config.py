from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType

def webpay_config():
    commerce_code = '597055555532'
    api_key = '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
    Transaction.configure_for_integration(IntegrationType.TEST, commerce_code= commerce_code, api_key= api_key)
    return Transaction