from .connection import APIConnection
from .utils import *


def libra() -> dict[str, str]:
    """
    Retorna a cotação da libra em BRL.

    Returns:
        Um dicionário com o valor da cotação. Ex.: {'value': 5.00000}

    Raises:
        ConnectionError: Caso não seja possível conectar com a API que nos daria o resultado.
        MissingSchema: Caso a url da API terceira esteja equivocada.

    Examples:
        >>> type(libra())
        <class 'dict'>
    """
    api = APIConnection('https://economia.awesomeapi.com.br/json/last')
    response = api.get('/GBP-BRL')
    data = response['GBPBRL']
    average = generate_average_value(data['high'], data['low'])
    return {'value': average}
