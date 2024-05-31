from .connection import APIConnection
from .utils import *


def bitcoin() -> dict[str, str]:
    """
    Retorna a cotação do bitcoin em BRL.

    Returns:
        Um dicionário com o valor da cotação. Ex.: {'value': 5.00000}

    Raises:
        ConnectionError: Caso não seja possível conectar com a API que nos daria o resultado.
        MissingSchema: Caso a url da API terceira esteja equivocada.

    Examples:
        >>> type(bitcoin())
        <class 'dict'>
    """
    api = APIConnection('https://economia.awesomeapi.com.br/json/last')
    response = api.get('/BTC-BRL')
    data = response['BTCBRL']
    average = generate_average_value(data['high'], data['low'])
    return {'value': average}
