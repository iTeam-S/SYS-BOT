#!/usr/bin/python
import json
import requests
from paramiko import SSHClient, AutoAddPolicy


class Verif:
    '''
        Objet de verification des erreurs et problemes des
        applications et outils dans le serveur
    '''
    def __init__(self) -> None:
        pass

    def ssh(self, host, username, password, port=22) -> dict:
        try:
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(host, port, username, password, timeout=20)
            client.close()

            return False

        except Exception as err:
            return str(err)

    def http(self, url, type="web"):
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
