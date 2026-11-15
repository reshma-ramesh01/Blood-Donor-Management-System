
import sqlite3
import re
import donor
import blood_request
con=sqlite3.connect("blood_donor.db")
c=con.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS admin_table(
    admin_id INTEGER PRIMARY KEY,
    admin_username TEXT ,
    admin_password TEXT)
    """)
#query=c.execute("INSERT INTO admin_table(admin_id,admin_username,admin_password) VALUES(1,'ad@123','ad123')")
#con.commit()
def change_password(username):
    c.execute("SELECT admin_password FROM admin_table where admin_username=?",[username])
    res=c.fetchone()
    current_password=res[0]
    #print(current_password)
    your_password = input("Enter Your Current Password : ")
    
    if current_password==your_password:
        new_pass = input("Enter New Password : ")
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{6,}$',new_pass):
            print("Stronger password must have minimum 6 characters. Contain upper, lower and number")
            exit()
        else:
            c.execute("UPDATE admin_table SET admin_password=? WHERE admin_username=?", (new_pass, username))
            con.commit()
            print("\n✅Password updated.")
            print("Login With New Password..")
            exit()
    else:
        print("\n❎Password Not Matched.")
    return

def op(name):
    while True:
        print("\n===============  WELCOME ADMIN   ===============")
        print("1. View Donors Details\n2. Add Donor\n3. Edit Donor Availability\n4. Search by Blood Group & Location\n5. Delete Donor")
        print("6. View Blood Request\n7. Edit Blood Donation Details\n8. View Completed Donations\n9. Change Password\n10. Logout")
        try:
            choice = int(input("Enter choice : "))
        except ValueError:
            print("Enter numbers only")
            continue
        if choice == 1:
            #username = input("Enter donor username: ")
            #donor.view_donor(username)
            res=donor.all_donors()
            print(res)
        elif choice==2:
            donor.signup()
        elif choice==3:
            username=input("Enter Donor's Username :")
            donor.update_availability(username)
        elif choice==4:
            donor.search_blood_group()
        elif choice==5:
            #username=input("Enter Donor's Username :")
            donor.delete_donor()
        elif choice == 6:
            blood_request.view_blood_requests()
        elif choice==7:
            blood_request.blood_donation_details()
        elif choice==8:
            blood_request.completed_donations()
        elif choice==9:
            change_password(name)
        elif choice==10:
            print("Logged out.")
            break
        else:
            print("Option not implemented yet.")
    return
