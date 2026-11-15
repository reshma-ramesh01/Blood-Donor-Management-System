import adminpage
import donor
import sqlite3

con = sqlite3.connect("blood_donor.db")
c = con.cursor()

def sign_in():
    name = input("Enter your Username : ")
    if not name.strip():
        print("Username cannot be empty")
        return
    password = input("Enter a password : ")
    if not password:
        print("Password cannot be empty")
        return
    c.execute("SELECT * FROM admin_table WHERE admin_username = ? AND admin_password = ?", (name, password,))
    result = c.fetchone()
    if result:
        adminpage.op(name)
        return  

    c.execute("SELECT * FROM donors WHERE username = ? AND password = ?", (name, password,))
    result = c.fetchone()
    if result:
        print("\n✅ Login Successful!")
        username=result[6]
        donor.donor_menu(username)   # username
    else:
        print("\n❎ Invalid username or password!")
    return

