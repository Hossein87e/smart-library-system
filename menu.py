def menu_start():
    print("\nwelcome to smart libary \n")
    print("1 - admin")
    print("2 - user register/login")
    return int(input("your choice : "))

def menu_admin():
    print("-----admin panel----\n")
    print("1 - add a book")
    print("2 - delete a book")
    print("3 - view members")
    print("4 - view logs")
    print("5 - book inventory chart")
    print("6 - send message to all")
    print("7 - filter books by quantity")
    print("8 - pin a book")
    print("9 - save all books to Excel")
    print("10 - show all tickets ")
    return int(input("your choice : "))


def menu_authentication():
    print("1 - register")
    print("2 - login")  
    return int(input("your choice : "))


def menu_user():
    print("\n--- User Menu ---")
    print("1 - Show book list")
    print("2 - Buy a book")
    print("3 - Submit a ticket to admin")
    print("4 - Delete my account")
    print("5 - suggest books")
    print("6 - log out")
    selection_user = input("Select an option (1-6): ")
    if selection_user in ["1", "2", "3", "4", "5","6"]:
        return int(selection_user)
    else:
        print("Invalid choice. Please enter a number from 1 to 5.")
            
