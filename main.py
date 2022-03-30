#!/usr/bin/python3
import os
import yaml
from utils import verif
from utils.webdriver import WebBrowser


def send_message(message):
    driver = WebBrowser()
    driver.connexion()
    driver.send_msg("4349594458421719", message)
    driver.browser.close()


if __name__ == "__main__":
    USER = os.environ.get("SSH_USER")
    PASS = os.environ.get("SSH_PASS")

    with open('check-list.yaml', 'r') as file:
        check_list = yaml.safe_load(file)
        v = verif.Verif()

        for url in check_list["api"]:
            verif_api = v.http(url, type="api")
            if verif_api is not True:
                send_message(f"{url} : {str(verif_api)}")
            else:
                print(f"[API CHECKED] {url}")

        for url in check_list["web"]:
            verif_web = v.http(url, type="web")
            if verif_web is not True:
                send_message(f"{url} : {str(verif_web)}")
            else:
                print(f"[SITE CHECKED] {url}")

        ssh_client = v.ssh("iteam-s.mg", USER, PASS)
        if type(ssh_client) == str:
            send_message(f"SSH: {str(ssh_client)} :-(")
        else:
            print("[SSH CONNECTED xD]")
            for service in check_list["services"]:
                verif_srv = v.service(service, ssh_client)
                if verif_srv is not True:
                    send_message(f"{service} : INACTIVE or DEAD")
                else:
                    print(f"[ACTIVE] {service}")

            for pm2_app in check_list["pm2"]:
                verif_pm2 = v.service(pm2_app, ssh_client)
                if verif_pm2 is not True:
                    send_message(pm2_app + str(verif_pm2))
                else:
                    print(f"[ONLINE] {pm2_app}")
        ssh_client.close()

    print("[ANALYSE DONE]")
