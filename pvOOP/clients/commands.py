from tabulate import tabulate

import click

from clients.services import ClientService
from clients.models import Client

# usamos la función clients para definir el grupo al que perteneceran todas las otras funciones
@click.group() # Me convierte la función client en un decorador
def clients():
    """Manages the clients lifecycle"""
    pass


@clients.command() #De esta manera convertimos las funciones en comandos
@click.option('-n', '--name',
              type=str,
              prompt=True, # Si no dan la opción, se la pedimos al usuario
              help='The client name')
@click.option('-c', '--company',
              type=str,
              prompt=True, 
              help='The client company')
@click.option('-e', '--email',
              type=str,
              prompt=True,
              help='The client email')
@click.option('-p', '--position', # La opción que sale aquí es la que muestra el prompt cuando pide la info
              type=str,
              prompt=True,
              help='The client position')
@click.pass_context
def create(ctx, name, company, email, position):
    """Create a new client"""
    client = Client(name, company, email, position) # creamos el cliente con el modelo
    # instanciamos el obj servicio con el nombre de la tabla donde se guardan los datos
    client_service = ClientService(ctx.obj['clients_table']) 
    # Creamos el cliente en la bd
    client_service.create_client(client)



@clients.command()
@click.pass_context
def list(ctx):
    """List all clients"""

    client_service = ClientService(ctx.obj['clients_table'])
    clients_list = client_service.list_clients()

    headers = [field.upper() for field in Client.schema()]
    table = []

    for client in clients_list:
        table.append(
            [client['name'],
             client['company'],
             client['email'],
             client['position'],
             client['uid']])

    # Usamos echo para que sirve en todos los OS
    click.echo(tabulate(table, headers))


@clients.command()
@click.argument('client_uid',
                type=str)
@click.pass_context
def update(ctx, client_uid):
    """Update a client"""
    client_service = ClientService(ctx.obj['clients_table'])

    """list_clients devuelve un dict (JSON) de los clientes que tenemos que convertir a 
    instancia de Cliente"""
    clients_list = client_service.list_clients()

    """La creación de la instancia cliente con SQL se buscaría 
    con los select, la iteración y la eficiencia del algoritmo 
    se la dejamos al motor de búsqueda, no a list comprehension
    dde python"""
    client = [client for client in clients_list if client['uid'] == client_uid]

    # Si encontramos el cliente, le pedimos al user ¿qué modificaciones quiere hacer?
    # para eso creamos un flujo de actualización
    if client:
        # Por uid únicas, solo habrá 1 cliente, lo sacamos de la pos [0]
        """Tomo el objeto cliente"""
        client = _update_client_flow(Client(**client[0]))
        client_service.update_client(client)

        click.echo('Client updated')
    else:
        click.echo('Client not found')


def _update_client_flow(client):

    click.echo('Leave empty if you dont want to modify the value')

    client.name = click.prompt('New name', type=str, default=client.name) 
    client.company = click.prompt('New company', type=str, default=client.company) 
    client.email = click.prompt('New email', type=str, default=client.email) 
    client.position = click.prompt('New position', type=str, default=client.position) 

    return client


@clients.command()
@click.argument('client_uid',
                type=str)
@click.pass_context
def delete(ctx, client_uid):
    """Deletes a client"""
    
    # inicio el ClientService con el ctx obj que guarda el nombre del archivo BD en clients_table
    client_service = ClientService(ctx.obj['clients_table'])
    # Consigo la lista de los clientes y la pongo en clients_list, esto es una lista de diccionatios
    clients_list = client_service.list_clients()

    client = [client for client in clients_list if client['uid'] == client_uid]

    if client:
        # Por uid únicas, solo habrá 1 cliente, lo sacamos de la pos [0]
        # recuerda que client es una lista de dicts, cada fila es un dict
        client_service.delete_client(Client(**client[0]))

        click.echo('Client deleted')
    else:
        click.echo('Client not found')


# Creamos un alias para que sea fácil declarar las funciones
all = clients