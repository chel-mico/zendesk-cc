from login import Login
from printer import Printer
import unittest
import requests
import json

class TestPrinting(unittest.TestCase):

    login = None
    printer = None

    def setUp(self):
        self.login = Login()
        self.printer = Printer(self.login)
        do_post = input("You will need more than 25 pages to perform multi-page tests. Do you need to post some test tickets? (y/n)")
        if do_post == 'y':
            self.printer.post_test()
            do_post = input("Wait until the test show up in your account (1-2 minutes) and then enter any character")

    def test_first_print(self):
        tickets, response = self.printer.print_first()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(tickets == "")

    def test_next_print(self):
        tickets, response = self.printer.print_all()
        tickets, response = self.printer.print_next(response.json()['meta'], 2)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(tickets == "")

    def test_prev_print(self):
        tickets, response = self.printer.print_all()
        tickets, response = self.printer.print_prev(response.json()['meta'], 0)
        # no previous page = no response
        self.assertTrue(response is None)

    def test_single_print(self):
        tickets, response = self.printer.print_single(16)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(tickets == "")
    
    def test_print_page(self):
        # testing first page printing
        self.printer.print_page(self.response)
    


if __name__ == "__main__":
    unittest.main()