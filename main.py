from login import Login
import json

def main():
    login = Login()
    response = login.auth()
    token = response.json()['access_token']

    running = True
    while running:
        return


if __name__ == '__main__':
    main()