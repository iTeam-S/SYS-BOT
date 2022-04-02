import os
import pickle
import re
import time
import requests
from bs4 import BeautifulSoup

import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By


class WebBrowser:
    def __init__(self) -> None:
        self.crm_options = uc.ChromeOptions()
        self.crm_options.add_argument('--headless')
        self.crm_options.add_argument('--no-sandbox')
        self.crm_options.add_argument('--disable-dev-shm-usage')

        self.browser = uc.Chrome(version_main=98, options=self.crm_options)

    def page_loaded(self) -> bool:
        """
            Pour verifier qu'un driver a fini de charger la page...
            True dans ce cas , sinon False
        """
        status = self.browser.execute_script('return document.readyState;')
        return status == 'complete'

    def connexion(self):
        """
            fonction de connexion pour le driver donnee en parametre
            avec verification de presence de cookie.
        """
        self.browser.get('https://mbasic.facebook.com/')

        if os.path.isfile('cookies.pkl'):
            with open("cookies.pkl", "rb") as fcookies:
                cookies = pickle.load(fcookies)
                for cookie in cookies:
                    try:
                        self.browser.add_cookie(cookie)
                    except Exception as err:
                        print(err)
                        os.remove('cookies.pkl')
                        self.connexion(self.browser)
            self.browser.get('https://mbasic.facebook.com/')
            while not self.page_loaded():
                time.sleep(0.5)
            if 'login' in self.browser.current_url:
                try:
                    os.remove('cookies.pkl')
                except FileNotFoundError:
                    pass
                finally:
                    self.connexion(self.browser)
            return
        self.browser.get('https://mbasic.facebook.com/')
        # Login to the fb account
        if '/cookie/' in self.browser.current_url:
            self.browser.find_element(
                by=By.XPATH, value='//button[@type="submit"]').click()

        # Enter username
        username_ipt = self.browser.find_element(
            by=By.ID, value="m_login_email")
        username_ipt.send_keys(os.environ.get("FB_USER"))
        # Enter password
        password_ipt = self.browser.find_element(by=By.NAME, value="pass")
        password_ipt.send_keys(os.environ.get("FB_PASS"))
        # Press login button
        self.browser.find_element(by=By.NAME, value="login").click()

        while not self.page_loaded():
            time.sleep(0.5)
        print("connexion success")
        with open("cookies.pkl", "wb") as fcookies:
            pickle.dump(self.browser.get_cookies(), fcookies)

    def send_msg(self, userID, message):
        """
            Fonction pour envoyer un message specifique à utilisateur Facebook
            avec trois parametres: webdriver, userID (ex: 100000144), message.
        """
        # Connecter le driver à Facebook
        while not self.page_loaded():
            time.sleep(0.5)

        # Redirect to the message page of the user
        self.browser.get(
            'https://mbasic.facebook.com/messages/thread/' + userID)
        while not self.page_loaded():
            time.sleep(0.5)
        time.sleep(2)
        # If the user is not a friend
        try:
            message_ipt = self.browser.find_element(
                by=By.ID, value="composerInput")
            message_ipt.send_keys(message)
        except Exception:
            print("[URL] ", self.browser.current_url)
            pass

        # Send the message
        try:
            self.browser.find_element(by=By.NAME, value="send").click()
        except Exception as err:
            print(err)
            self.browser.find_element(by=By.NAME, value="Send").click()

    def get_user_id(self, username):
        """
            A partir d'un username du profil facebook,
                retourne l'userID sinon None si Not found
        """

        # Les données du cookies du navigateur

        cookies = {
            cookie['name']: cookie['value']
            for cookie in self.browser.get_cookies()
        }

        s = requests.Session()
        r = s.get("https://mbasic.facebook.com/" + username, cookies=cookies)
        print(r)
        if r.status_code == 404:
            return

        src_code = BeautifulSoup(r.text, 'html.parser')

        for balise_a in src_code.find_all('a'):
            link = balise_a.get('href')
            if link is not None and (
                link.startswith('/r.php?') or 'profile_id' in link or
                    'owner_id' in link or 'thread' in link):
                res = re.findall(r"1000[0-9]{11}", link)
                if len(res) > 0:
                    return res[0]
