import os
import pickle
import re
import time
import requests
from bs4 import BeautifulSoup

import undetected_chromedriver as uc


class WebBrowser:
    def __init__(self) -> None:
        self.crm_options = uc.ChromeOptions()
        self.crm_options.add_argument('--no-sandbox')
        self.crm_options.add_argument('--headless')
        self.crm_options.add_argument('--disable-dev-shm-usage')

        self.browser = uc.Chrome(options=self.crm_options)

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
            while not self.page_loaded(self.browser):
                time.sleep(0.5)
            if 'login' in self.browser.current_url:
                print('Je me login encore')
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
            self.browser.find_element_by_xpath(
                '//button[@type="submit"]').click()
        self.browser.find_element_by_tag_name('body').screenshot("conn1.png")
        username_ipt = self.browser.find_element_by_id("m_login_email")
        username_ipt.send_keys(os.environ.get("ITEAMS_LOGIN"))
        print("Variable env => ", os.environ.get("ITEAMS_LOGIN"))

        password_ipt = self.browser.find_element_by_name("pass")
        password_ipt.send_keys(os.environ.get("ITEAMS_PASS"))

        self.browser.find_element_by_name("login").click()
        while not self.page_loaded(self.browser):
            time.sleep(0.5)
        self.browser.find_element_by_tag_name('body').screenshot("conn1.png")
        print("connexion success")
        with open("cookies.pkl", "wb") as fcookies:
            pickle.dump(self.browser.get_cookies(), fcookies)

    def send_msg(self, userID, message):
        """
            Fonction pour envoyer un message specifique à utilisateur Facebook
            avec trois parametres: webdriver, userID (ex: 100000144), message.
        """
        # Connecter le driver à Facebook
        while not self.page_loaded(self.browser):
            time.sleep(0.5)
        # Redirect to the message page of the user
        self.browser.find_element_by_tag_name('body').screenshot("conn_m.png")
        self.browser.get(
            'https://mbasic.facebook.com/messages/thread/' + userID)
        while not self.page_loaded(self.browser):
            time.sleep(0.5)
        time.sleep(2)
        # If the user is not a friend
        try:
            message_ipt = self.browser.find_element_by_name("body")
        # If the user is a friend
        except Exception as err:
            print(err)
            message_ipt = self.browser.find_element_by_id("composerInput")

        self.browser.find_element_by_tag_name('body').screenshot("test_m.png")
        # message_ipt = self.browser.find_element_by_tag_name('textarea')

        message_ipt.send_keys(message)

        # Send the message
        try:
            self.browser.find_element_by_name("Send").click()
        except Exception as err:
            print(err)
            self.browser.find_element_by_name("send").click()
        self.browser.find_element_by_tag_name('body').screenshot("fara.png")

    def get_user_id(username, driver):
        """
            A partir d'un username du profil facebook,
                retourne l'userID sinon None si Not found
        """

        # Les données du cookies du navigateur

        cookies = {
            cookie['name']: cookie['value']
            for cookie in driver.browser.get_cookies()
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
