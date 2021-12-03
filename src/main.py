from login import Login
from printer import Printer

class Main :
    """Constructor for a main class which will run the ticket viewer"""
    def main(self):
        #OAuth
        login = Login()
        token = login.token
        if token == "q":
            return

        #printing the first page and setting up the printer
        running = True
        printer = Printer(login)
        printed_first = False
        while not printed_first:
            meta, response = printer.first()
            if response.status_code != 200:
                answer = input("Do you wish to try again? (y/n)")
                if answer != 'y':
                    running = False
                    printed_first = True
                else:
                    continue
            else:
                printed_first = True
        max_id = 25
        reprint = True

        #run through
        while running:
            old_response = response
            old_meta = meta
            if reprint:
                count = printer.print_page(old_response, max_id)
                if count.status_code != 200:
                    answer = self.process_error(count)
                    if answer == "stop":
                        running = False
                reprint = False
            print("\nEnter next to go to the 'next' page or 'prev' to go to a previous page.")
            print("You can also enter 'details' to see the details of a ticket.")
            print("If you wish to leave, enter 'quit'.")
            command = input()
            #next command
            if command == 'next':
                max_id += 25
                meta, response = printer.next(meta, max_id)
                if response is None:
                    max_id -= 25
                    print("You've gone too far forward!")
                    response = old_response
                    meta = old_meta
                elif response.status_code != 200:
                    max_id -= 25
                    answer = self.process_error(response)
                    if answer == "stop":
                        running = False
                    response = old_response
                    meta = old_meta
                    reprint = True
            #prev command
            elif command == 'prev':
                max_id -= 25
                meta, response = printer.prev(meta, max_id)
                if response is None:
                    max_id += 25
                    print("You've gone too far back!")
                    response = old_response
                    meta = old_meta
                elif response.status_code != 200:
                    max_id += 25
                    answer = self.process_error(response)
                    if answer == "stop":
                        running = False
                    response = old_response
                    meta = old_meta
                    reprint = True
            #details command
            elif command == 'details':
                id = input("Enter the ID of the ticket you wish to view: ")
                response = printer.print_single(id)
                if response.status_code != 200:
                    answer = self.process_error(response)
                    if answer == "stop":
                        running = False
                else:
                    input("Enter any key to go back: ")
                response = old_response
                reprint = True
            #exit
            elif command == 'quit':
                running = False
            else:
                print("Not a valid command!")
        print("Signing off...")

    def process_error(response):
        answer = input("Do you wish to continue? (y/n)")
        if answer != 'y':
            return "stop"
        return "continue"

if __name__ == '__main__':
    Main.main(Main)