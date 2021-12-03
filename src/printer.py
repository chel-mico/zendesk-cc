import requests
import json
import math
from typing import Union, Dict

class Printer:
    """Constructor for a Printer class to print and return tickets"""
    def __init__(self, login, max=25):
        self.login = login
        self.token = login.token
        self.domain = login.domain
        self.max = max
    
    def first(self) -> Union[Dict[str, object],requests.Response]:
        """Function to get the first page of tickets"""
        response = self.request("https://{}.zendesk.com/api/v2/tickets.json?page[size]={}".format(self.domain, self.max))
        if response.status_code != 200:
            self.login.error_check(response.status_code)
            return "", response
        return response.json()['meta'], response

    def next(self, meta, max_id) -> Union[Dict[str, object],requests.Response]:
        """Function to get the next page of tickets"""
        if not meta['has_more']:
            return "", None
        response = self.request("https://{}.zendesk.com/api/v2/tickets.json?page[size]={}&page[after]={}".format(self.domain, self.max, meta['after_cursor']))
        if response.status_code != 200:
            self.login.error_check(response.status_code)
            return "", response
        self.print_page(response, max_id)
        return response.json()['meta'], response

    def prev(self, meta, max_id) -> Union[Dict[str, object],requests.Response]:
        """Function to get the previous page of tickets"""
        if max_id <= 25:
            return "", None
        response = self.request("https://{}.zendesk.com/api/v2/tickets.json?page[size]={}&page[before]={}".format(self.domain, self.max, meta['before_cursor']))
        if response.status_code != 200:
            self.login.error_check(response.status_code)
            return "", response
        self.print_page(response, max_id)
        return response.json()['meta'], response

    def print_single(self, ticket_id) -> requests.Response:
        """Function to print a single ticket"""
        response = self.request("https://{}.zendesk.com/api/v2/tickets/{}".format(self.domain, ticket_id))
        if response.status_code != 200:
            self.login.error_check(response.status_code)
            return response
        ticket = response.json()['ticket']
        return_string = "ID: {id}      \'{subject}\', requested by {requester_id} on {created_at} and assigned to {assignee_id}\n".format(**ticket)
        return_string += "Description: {}".format(ticket['description'])
        print(return_string)
        return response

    def print_page(self, response, max_id=25) -> requests.Response:
        """Function to print a single page of tickets"""
        count = self.count()
        if count.status_code != 200:
            self.login.error_check(count.status_code)
            return count
        tickets = response.json()['tickets']
        return_string = ""
        print("Viewing up to {} of {}".format(max_id, count.json()['count']['value']))
        for i in tickets:
            return_string += "ID: {id:<6} Subject: '{subject}', requested by {requester_id:} on {created_at:} and assigned to {assignee_id:}\n".format(**i)
        print(return_string)
        return count
    
    def request(self, url) -> requests.Response:
        """Helper function to request a response from the Zendesk API"""
        headers = {"Authorization": "Bearer {}".format(self.token)}
        response = requests.get(url, headers=headers)
        return response
    
    def count(self) -> requests.Response:
        """Function to get the number of tickets for a user"""
        count = self.request("https://{}.zendesk.com/api/v2/tickets/count.json".format(self.domain))
        return count