import click
# Importamos los commands que creamos
from clients import commands as clients_commands

# Nombre del archivo donde guardamos la info
CLIENTS_TABLE = '.clients.csv'

# definimos el punto de entrada
@click.group
@click.pass_context # nos da el objeto contexto que le pasamos a la función
def cli(ctx): #command line interface?
    ctx.obj = {}
    ctx.obj['clients_table'] = CLIENTS_TABLE


cli.add_command(clients_commands.all)