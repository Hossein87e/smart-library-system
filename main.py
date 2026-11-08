from menu import *
from defs import *
import os
import datetime

while True:
    create_json_file()
    selection = menu_start()
    if selection == 1:
        selection_admin = menu_admin()
        if selection_admin == 1:
            add_book()
        elif selection_admin == 2:
            delete_book()
        elif selection_admin == 3:
            show_user()
        elif selection_admin == 4:
            show_log()
        elif selection_admin == 5:
            draw_chart()
        elif selection_admin == 6:
            message = input("send message to all :")
            add_message_by_admin(message)
        elif selection_admin == 7:
            filter_books_by_count()
        elif selection_admin == 8:
            pin_book()
        elif selection_admin == 9:
            save_books_to_excel()
        elif selection_admin == 10:
            show_all_tickets()

    elif selection == 2:
        selection_user = menu_authentication()
        if selection_user == 1:
            register()
        elif selection_user == 2:
            username = login()
            if username:
                suggest_book()
                show_broadcast_messages()
                while True:
                    user_choice = menu_user()
                    if user_choice == 1:
                        list_book_sorted()
                    elif user_choice == 2:
                        buy_book()
                    elif user_choice == 3:
                        submit_ticket(username)
                    elif user_choice == 4:
                        delete_account()
                        break
                    elif user_choice == 5:
                        suggest_book()
                    elif user_choice == 6:
                        break
                    else:
                        print("Invalid option.")
                break
            else:
                print("Login failed.")