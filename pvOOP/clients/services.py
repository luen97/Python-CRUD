import csv
import os

from clients.models import Client

class ClientService:

    def __init__(self, table_name) -> None:
        # Recibe el nombre del archivo donde guardamos los datos
        self.table_name = table_name

    def create_client(self, client):
        # abrimos en modo append para agregar
        # así no cargamos todo el archivo
        with open(self.table_name, mode='a') as f:
            writer = csv.DictWriter(f, fieldnames=Client.schema())
            writer.writerow(client.to_dict())

    def list_clients(self):
        with open(self.table_name, mode='r') as f:
            reader = csv.DictReader(f,fieldnames=Client.schema())
                        
            return list(reader)

    def update_client(self, updated_client):
        """updated_client: Instancia de Client"""
        clients = self.list_clients()

        """cojame todos los clientes, pero cuando sea el actualizado,
        me lo pasa con las cosas nuevas.
        
        updated_clients: En plural (con s) es la lista de como quedan
        los clientes actualizados.
        
        updaate_client: es el cliente que se va a actualizar"""

        updated_clients = []
        for client in clients:
            if client['uid'] == updated_client.uid:
                updated_clients.append(updated_client.to_dict())
            else:
                updated_clients.append(client)

        self._save_to_disk(updated_clients)

    def delete_client(self,deleted_client):
        """Mismo proceso que en el update, cambia en el comando
        que no  hay que hacer todo el de flujo de actualización"""

        ## Así lo hicimos iterando
        # clients = self.list_clients()

        # deleted_clients = []
        # for client in clients:
        #     if client['uid'] == deleted_client.uid:
        #         pass
        #     else:
        #         deleted_clients.append(client)

        client_list = self.list_clients()
        # print(client_list[0])

        client_list.remove(deleted_client.to_dict())
        # print(client_list)

        self._save_to_disk(client_list)



    def _save_to_disk(self, clients):
        tmp_table_name = self.table_name + '.tmp'
        with open(tmp_table_name, mode='w') as f:
            writer = csv.DictWriter(f, fieldnames=Client.schema())
            writer.writerows(clients)

        os.remove(self.table_name)
        os.rename(tmp_table_name, self.table_name)
