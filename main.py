import donor
import signin
import sqlite3

import os
import blood_request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "blood_donor.db")
con = sqlite3.connect(db_path)
c = con.cursor()
def main_menu():
    print("1. Sign In\n2. Sign Up\n3. Request for Blood\n4. Exit")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        exit()

    if choice == 1:
        signin.sign_in()
    elif choice == 2:
        donor.signup()
    elif choice==3:
        blood_request.request_blood()
    elif choice == 4:
        print("Exiting...")
        exit()
    else:
        print("Please enter a valid option (1–4).")
main_menu()

