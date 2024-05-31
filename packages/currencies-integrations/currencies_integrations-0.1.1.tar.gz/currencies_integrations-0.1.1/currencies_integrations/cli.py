from rich.console import Console
from rich.table import Table
from typer import Typer

from currencies_integrations.bitcoin import bitcoin as _bitcoin
from currencies_integrations.dolar import dolar_comercial as _dolar_comercial
from currencies_integrations.dolar import dolar_turismo as _dolar_turismo
from currencies_integrations.libra import libra as _libra

console = Console()
app = Typer()


def print_infos(title, value):
    table = Table()
    table.add_column(title)
    table.add_row(f'R$ {value}')
    console.print(table)


@app.command()
def dolar_comercial():
    print_infos('USD Comercial', _dolar_comercial()['value'])


@app.command()
def dolar_turismo():
    print_infos('USD Turismo', _dolar_turismo()['value'])


@app.command()
def bitcoin():
    print_infos('Bitcoin', _bitcoin()['value'])


@app.command()
def libra():
    print_infos('Libra', _libra()['value'])
