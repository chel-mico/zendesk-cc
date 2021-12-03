from login import Login
from printer import Printer

def main():
    #OAuth
    login = Login()
    token = login.token
    if token == "q":
        return

    running = True
    printer = Printer(login)
    printed_first = False
    while not printed_first:
        meta, response = printer.first()
        if response.status_code != 200:
            answer = input("Do you wish to try again? (y/n)".format(response.status_code))
            if answer != 'y':
                running = False
                printed_first = True
            else:
                continue
        else:
            printed_first = True
    page = 1
    while running:
        old_response = response
        count = printer.print_page(old_response)
        if count.status_code != 200:
            answer = process_error(response)
            if answer == "stop":
                running = False
        print("\nEnter next to go to the 'next' page or 'prev' to go to a previous page.")
        print("You can also enter 'details' to see the details of a ticket.")
        print("If you wish to leave, enter 'quit'.")
        command = input()
        #next command
        if command == 'next':
            meta, response = printer.next(meta, page+1)
            if response is None:
                print("You've gone too far forward!")
                response = old_response
            elif response.status_code != 200:
                answer = process_error(response)
                if answer == "stop":
                    running = False
                response = old_response
        #prev command
        if command == 'prev':
            meta, response = printer.prev(meta, page-1)
            if response is None:
                print("You've gone too far back!")
                response = old_response
            elif response.status_code != 200:
                answer = process_error(response)
                if answer == "stop":
                    running = False
                response = old_response
        #details command
        if command == 'details':
            id = input("Enter the ID of the ticket you wish to view: ")
            response = printer.print_single(id)
            if response.status_code != 200:
                answer = process_error(response)
                if answer == "stop":
                    running = False
            else:
                input("Enter any key to go back: ")
            response = old_response
        #exit
        elif command == 'quit':
            running = False
    print("Signing off...")

#function for processing errors
def process_error(response):
    answer = input("Do you wish to continue? (y/n)".format(response.status_code))
    if answer != 'y':
        return "stop"
    return "continue"

if __name__ == '__main__':
    main()