#!/usr/bin/python
from paramiko import SSHClient, AutoAddPolicy
import requests


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
            
            
    def verif_api(self, method, url, **kwargs):
        
        """
            Methode pour verifier avec des 
            tests les API disponible dans le serveur
        """
        
        if method == "GET":
            try: 
                testing = requests.get(url)
                if testing.status_code == 200:
                    return {
                        "error":False,
                        "message":"OK"
                    }
                else:
                    return {
                        "error": True,
                        "status_code":testing.status_code,
                        "raison":str(testing.reason),
                        "message":f"Probléme sur l'API <{url}> du methode GET"
                    }
                    
            except Exception as err:
                return {
                    "error":True,
                    "url":url,
                    "message":str(err)
                }
                
        elif method == "POST":
            try:
                header = {'content-type': 'application/json; charset=utf-8'}
                data = kwargs.get("data")
                if data:
                    testing = requests.post(url,json=data,headers=header)
                    if testing.status_code==200:
                        return {
                            "error":False,
                            "message":"OK"
                        }
                        
                    else:
                        return {
                            "error": True,
                            "status_code":testing.status_code,
                            "raison":str(testing.reason),
                            "message":f"Probléme sur l'API <{url}> du methode POST"
                        }
                else:
                    return {
                        "error":True,
                        "message": "Aucune donnée pour la verification de la faisabilité de cet API"
                    }
                    
            except Exception as err:
                return {
                    "error":True,
                    "url":url,
                    "message":str(err)
                }
                
        elif method == "PUT":
            try:
                header = {'content-type': 'application/json; charset=utf-8'}
                data = kwargs.get("data")
                if data:
                    testing = requests.put(url,json=data,headers=header)
                    if testing.status_code==200:
                        return {
                            "error":False,
                            "message":"OK"
                        }
                        
                    else:
                        return {
                            "error": True,
                            "status_code":testing.status_code,
                            "raison":str(testing.reason),
                            "message":f"Probléme sur l'API <{url}> du methode PUT"
                        }
                else:
                    return {
                        "error":True,
                        "message": "Aucune donnée pour la verification de la faisabilité de cet API"
                    }
                    
            except Exception as err:
                return {
                    "error":True,
                    "url":url,
                    "message":str(err)
                }
            
    
    def verif_service_web(self,url):
        try:
            testing = requests.get(url)
            if testing.status_code == 200:
                return {
                    "error":False,
                    "message":"OK"
                }
            else:
                return {
                    "error": True,
                    "status_code":testing.status_code,
                    "raison":str(testing.reason),
                    "message":f"Probléme sur le site WEB <{url}>"
                }
        except Exception as err:
            return {
                "error":True,
                "message":str(err)
            }        