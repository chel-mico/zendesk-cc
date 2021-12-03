import requests
import os
from dotenv import load_dotenv

class Login:

    def __init__(self):
        load_dotenv()
        self.ID = os.getenv("ID")
        self.secret = os.getenv("SECRET")
        self.domain = os.getenv("DOMAIN")
        self.redirect = os.getenv("REDIRECT")
        self.url = "https://{}.zendesk.com/oauth/authorizations/new?response_type=code&redirect_uri={}&client_id={}&scope=tickets:read".format(self.domain, self.redirect, self.ID)
        self.token = self.auth()

    
    def auth(self):
        auth = False
        print("Welcome to the Ticket Viewer!\n")
        print("Before we begin, please log in here: {}".format(self.url))
        print("Once you're done, you'll get an error, but don't worry! This is normal.")
        print("Simply input the URL that's in your search bar below.\n")
        while not auth:
            try:
                response = input("URL: ")
                if "code" not in response:
                    print("There's been an error in your authentication, please try again.\n")
                    continue
                auth_code = response.split('=')[1]
                parameters = {
                    "grant_type": "authorization_code",
                    "code": auth_code,
                    "client_id": self.ID,
                    "client_secret": self.secret,
                    "redirect_uri": self.redirect,
                    "scope": "tickets:read"}
                res = requests.post(url="https://{}.zendesk.com/oauth/tokens".format(self.domain), params=parameters)
                auth = True
            except:
                print("There's been an error in your authentication, please try again.")
                print("If the issue persists, the Zendesk API may be down")
                continue
        return res.json()['access_token']

