import requests
import os
from dotenv import load_dotenv

class Login:
    """Constructor for a Login class to help with authentication"""
    def __init__(self):
        load_dotenv()
        self.ID = os.getenv("ID")
        self.secret = os.getenv("SECRET")
        self.domain = os.getenv("DOMAIN")
        self.redirect = os.getenv("REDIRECT")
        self.url = "https://{}.zendesk.com/oauth/authorizations/new?response_type=code&redirect_uri={}&client_id={}&scope=read%20write".format(self.domain, self.redirect, self.ID)
        self.token = self.auth()

    def auth(self) -> str:
        """Function to authenticate a user with OAuth"""
        auth = False
        print("Welcome to the Ticket Viewer!\n")
        print("Before we begin, please log in here: {}".format(self.url))
        print("Once you're done, you'll get an error, but don't worry! This is normal.")
        print("Simply input the URL that's in your search bar below.\n")
        while not auth:
            try:
                #getting the auth code
                response = input("URL (or q to leave): ")
                if response == "q":
                    return response
                if "code" not in response:
                    print("You may have done the authentication wrong, please try again.\n")
                    continue
                #fetching the token
                auth_code = response.split('=')[1]
                parameters = {
                    "grant_type": "authorization_code",
                    "code": auth_code,
                    "client_id": self.ID,
                    "client_secret": self.secret,
                    "redirect_uri": self.redirect,
                    "scope": "read%20write"
                }
                res = requests.post(url="https://{}.zendesk.com/oauth/tokens".format(self.domain), params=parameters)
                if res.status_code != 200:
                    self.error_check()
                    continue
                auth = True
            except:
                print("There's been an unexpected error in your authentication, please try again.")
                continue
        return res.json()['access_token']

    def error_check(self, code) -> None:
        """Function to check a bad response code and print an accurate explanation."""
        if code == 403:
            print("403 Forbidden\nSorry, but you don't have the right permissions to do this :(")
        elif code == 404:
            print("404 Not Found\nSorry, but we couldn't find what you were looking for :(")
        elif code == 409:
            print("409 Merge Conflict\nSomething collided in making your request :(, please try again.")
        elif code == 422:
            print("422 Unprocessable Entity\nWe couldn't process the request due to it being impossible :(, please try something else.")
        elif code == 429:
            print("429 Rate Limit Exceded\nYou've used the API too much! Try again in 24 hours.")
        elif code >= 500:
            print("500 Server Unavailable\nThere's been a problem with the server :(.\nTry again in a few seconds, but if the problem persists, the server may be down")

