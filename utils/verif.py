#!/usr/bin/python3
import json
import requests

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
        """
            Methode pour verifier la connectivite
            par ssh
        """
        try:
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(host, port, username, password, timeout=15)

            return client

        except Exception as err:
            return {
                "error": False,
                "message": str(err)
            }

    def database(self, host, username, password, db_name) -> bool:
        """
            Methode pour verifier la connectivite
            a une base de donnee
        """
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
        """
            Methode pour verifier le status
            d'un service linux en passant par ssh
        """
        try:
            output = ssh_client.exec_command(
                f"systemctl is-active {srv_name}")[1].read().decode()
            ssh_client.close()
            return True if("active" in output) else False

        except Exception as err:
            return str(err)

    def http(self, url, type="web") -> dict:
        """
            Methode pour verifier le bon fonctionnement
            des services http et https (web, api, ...)
        """
        try:
            req = requests.get(url)
            if req.status_code == 200:
                if "api" == type:
                    if not json.loads(req.text):
                        return {
                            "status_code": 200,
                            "message": "Pas de données",
                        }
                return False
            else:
                return {
                    "status_code": req.status_code,
                    "message": str(req.reason),
                }

        except Exception as err:
            return str(err)
