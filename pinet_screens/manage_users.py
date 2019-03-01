import getpass
import sys

import main
import database
import util


def choose_user():
    users = database.get_all_users()
    print("Select a user")
    print("-------------")
    for index, user in enumerate(users):
        print("{} - {}".format(index + 1, user.username))
    user_choice = input("Option: ")
    if not user_choice or not user_choice.isdigit() or (user_choice.isdigit() and (int(user_choice) < 1 or int(user_choice) > len(users)) ):
        print("")
        print("***************")
        print("Invalid choice!")
        print("***************")
        print("")
        return
    else:
        return users[int(user_choice) -1]


def remove_user():
    user = choose_user()
    if user:
        database.remove_user(user.user_id)


def change_password():
    user = choose_user()
    if user:
        password = getpass.getpass("Enter new password: ")
        util.change_password(user.user_id, password)

while True:
    print("Select an option")
    print("----------------")
    print("")
    print("1. Create user")
    print("2. Remove user")
    print("3. Change password")
    print("Enter q to quit")

    choice = input("Option: ")
    if not choice:
        continue
    elif choice == "q":
        sys.exit(0)
    elif choice == "1":
        main.validate_startup(override_first_time_check=True)
    elif choice == "2":
        remove_user()
    elif choice == "3":
        change_password()