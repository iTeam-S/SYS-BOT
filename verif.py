#!/usr/bin/python3
from paramiko import SSHClient, AutoAddPolicy
import mysql.connector


class Verif:
    '''
        Objet de verification des erreurs et problemes des
        applications et outils dans le serveur
    '''
    def __init__(self) -> None:
        pass

    def ssh(self, host, username, password, port=22) -> SSHClient:
        try:
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(host, port, username, password, timeout=10)

            return client

        except Exception as err:
            return {
                "error": False,
                "message": str(err)
            }

    def database(self, host, username, password, db_name) -> bool:
        try:
            mysql.connector.connect(
                host=host,
                user=username,
                password=password,
                database=db_name
            ).is_connected()

            return True

        except Exception as err:
            return str(err)

    def service(self, srv_name, ssh_client) -> bool:
        try:
            output = ssh_client.exec_command(
                f"systemctl is-active {srv_name}")[1].read().decode()

            return True if("active" in output) else False

        except Exception as err:
            return str(err)
