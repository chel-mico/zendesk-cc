from login import Login
from printer import Printer
import unittest
import math
import requests
import json

class TestPrinting(unittest.TestCase):

    login = None
    printer = None

    #setting up OAuth and Printer
    def setUp(self):
        self.login = Login()
        self.printer = Printer(self.login)
        do_post = input("You will need more than 25 pages to perform multi-page tests. Do you need to post some test tickets? (y/n)")
        if do_post == 'y':
            self.post_test()
            do_post = input("Wait until the test show up in your account (1-2 minutes) and then enter any character")

    #first print test
    def test_first_print(self):
        meta, response = self.printer.first()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(meta == "")

    #next tests
    def test_next_print(self):
        meta, response = self.printer.first()
        meta, response = self.printer.next(response.json()['meta'], 2)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(meta == "")

    def test_next_print_error(self):
        meta, response = self.printer.first()
        count = math.ceil(self.printer.count().json()['count']['value']/self.max)
        page = 2
        while page < count:
            meta, response = self.printer.next(response.json()['meta'], page)
            page += 1
        # no next page = no response
        self.assertTrue(response is None)

    #prev tests
    def test_prev_print(self):
        meta, response = self.printer.first()
        meta, response = self.printer.next(response.json()['meta'], 2)
        meta, response = self.printer.prev(response.json()['meta'], 1)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(meta == "")

    def test_prev_print_error(self):
        meta, response = self.printer.first()
        meta, response = self.printer.prev(response.json()['meta'], 0)
        # no previous page = no response
        self.assertTrue(response is None)

    #single print tests
    def test_single_print(self):
        meta, response = self.printer.print_single(16)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(meta == "")

    def test_single_print_error(self):
        # the response should return nothing
        meta, response = self.printer.print_single("sdfsdg")
        self.assertTrue(meta == "")
    
    #print page test
    def test_print_page(self):
        # testing first page printing
        response = self.printer.print_page(self.response)
        self.assertEqual(response.status_code, 200)

    #count test
    def test_count(self):
        count = self.printer.count()
        self.assertEqual(count.status_code, 200)

    #request test
    def test_request(self):
        response = self.printer.request("https://{}.zendesk.com/api/v2/tickets/count.json".format(self.printer.domain))
        self.assertEqual(response.status_code, 200)

    def post_test(self) -> None:
        """Function to add a set of test tickets for testing purposes"""
        with open('tickets.json') as f:
            data = json.load(f)
        headers = {
            "Authorization": "Bearer {}".format(self.printer.token),
            "Content-Type": "application/json"
        }
        response = requests.post(
            "https://{}.zendesk.com/api/v2/tickets/create_many.json".format(self.login.domain), 
            headers=headers,
            json=data
        )
        print("Response code: {}".format(response.status_code))

if __name__ == "__main__":
    unittest.main()