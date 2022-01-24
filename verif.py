#!/usr/bin/python3
from paramiko import SSHClient, AutoAddPolicy
import json
import re
import subprocess


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
            client.connect(host, port, username, password, timeout=10)
            client.close()

            return {
                "status": True,
                "message": "connection success"
            }

        except Exception as err:
            return {
                "status": False,
                "message": str(err)
            }


    # ******************************* POUR VERIFIER LA STATUS D'UNE SERVICE *****************************************
    def servicesStatus(self, nom_service):
        status = False
        reponse = None
        try:
            demande = subprocess.run(['systemctl', 'status', nom_service],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.split('\n')
            for data in demande:
                if re.search(r"Active", data) is not None:
                    reponse = data
                    break
            if reponse is not None:
                resultats = reponse.split(':')
                messages = resultats[1] + ' '.join([resultats[i] for i in range(2, len(resultats))])
                if(re.search(r"running|start|active", messages) is not None):
                    status = True
                return json.dumps({'status': status, 'message': messages}, indent=3)
                
            else: raise ValueError("Service inconnu !!!")
        except ValueError:
            raise
