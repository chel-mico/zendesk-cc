import requests
import json
import math

class Printer:

    def __init__(self, login, max=25):
        self.login = login
        self.token = login.token
        self.domain = login.domain
        self.max = max
    
    def first(self):
        response = self.request("https://{}.zendesk.com/api/v2/tickets.json?page[size]={}".format(self.domain, self.max))
        if response.status_code != 200:
            self.login.error_check(response.status_code)
            return "", response
        return response.json()['meta'], response

    def next(self, meta, page):
        if not meta['has_more']:
            return "", None
        response = self.request("https://{}.zendesk.com/api/v2/tickets.json?page[size]={}&page[after]={}".format(self.domain, self.max, meta['after_cursor']))
        if response.status_code != 200:
            self.login.error_check(response.status_code)
            return "", response
        self.print_page(response, page)
        return response.json()['meta'], response

    def prev(self, meta, page):
        if meta['before_cursor'] == "":
            return "", None
        response = self.request("https://{}.zendesk.com/api/v2/tickets.json?page[size]={}&page[before]={}".format(self.domain, self.max, meta['after_cursor']))
        if response.status_code != 200:
            self.login.error_check(response.status_code)
            return "", response
        self.print_page(response, page)
        return response.json()['meta'], response

    def print_single(self, ticket_id):
        response = self.request("https://{}.zendesk.com/api/v2/tickets/{}".format(self.domain, ticket_id))
        if response.status_code != 200:
            self.login.error_check(response.status_code)
            return response
        ticket = response.json()['ticket']
        return_string = "ID: {id}      \'{subject}\', requested by {requester_id} on {created_at} and assigned to {assignee_id}\n".format(**ticket)
        return_string += "Description: {}".format(ticket['description'])
        print(return_string)
        return response

    def print_page(self, response, page=1):
        count = self.count()
        if count.status_code != 200:
            self.login.error_check(count.status_code)
            return count
        tickets = response.json()['tickets']
        return_string = ""
        print("Page {} of {}".format(page, math.ceil(count.json()['count']['value']/self.max)))
        for i in tickets:
            return_string += "ID: {id}      \'{subject}\', requested by {requester_id} on {created_at} and assigned to {assignee_id}\n".format(**i)
        print(return_string)
        return count
    
    def request(self, url):
        headers = {"Authorization": "Bearer {}".format(self.token)}
        response = requests.get(url, headers=headers)
        return response
    
    def count(self):
        count = self.request("https://{}.zendesk.com/api/v2/tickets/count.json".format(self.domain))
        return count

    def post_test(self):
        with open('tickets.json') as f:
            data = json.load(f)
        headers = {
            "Authorization": "Bearer {}".format(self.token),
            "Content-Type": "application/json"
        }
        response = requests.post(
            "https://{}.zendesk.com/api/v2/tickets/create_many.json".format(self.domain), 
            headers=headers,
            json=data
        )
        print("Response code: {}".format(response.status_code))