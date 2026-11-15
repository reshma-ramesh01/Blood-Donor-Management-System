import sqlite3
import re
con = sqlite3.connect("blood_donor.db")
c = con.cursor()


    # ---------      SIGN UP     ---------
def signup():
    c.execute("""
    CREATE TABLE IF NOT EXISTS donors(
        donor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        blood_group TEXT,
        phone TEXT UNIQUE,
        username TEXT UNIQUE,
        password TEXT,
        location TEXT,
        availability TEXT
    )
    """)

    name =input("Enter Name          : ").upper()
    if not name.replace(" ","").isalpha():
        print("Name must contain only letters")
        return

    age = int(input("Enter Age           : "))
    if age < 18 or age > 65:
        print("Age must be between 18 and 65")
        return

    gender =input("Enter Gender(F/M)   : ").upper()
    if gender not in ["F","M"]:
        print("Enter F or M only")
        return
    blood_group =input("Enter Blood Group   : ").upper()
    VALID_BLOOD_GROUPS = ["A+VE","A-VE","B+VE","B-VE","AB+VE","AB-VE","O+VE","O-VE"]
    if blood_group not in VALID_BLOOD_GROUPS:
        print("Invalid blood group")
        return
    phone =input("Enter Phone         : ")
    if not phone.isdigit():
        print("Phone must contain digits only")
        return
    if len(phone) != 10:
        print("Phone must be 10 digits")
        return
    username =input("Enter Username      : ")
    if len(username) < 5:
        print("Username must contain at least 5 characters")
        return
    password =input("Enter Password      : ")
    if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{6,}$',password):
        print("Stronger password must have minimum 6 characters. Contain upper, lower and number")
        exit()
    location = input("Enter Location      : ").upper()
    avail = input("Availability (Y/N)  : ").upper()
    if avail not in ["Y","N"]:
        print("Enter Y or N")
        return

    try:
        c.execute("""
        INSERT INTO donors(name, age, gender, blood_group, phone, username, password, location, availability)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, age, gender, blood_group, phone, username, password, location, avail))

        con.commit()
        print("✅ Registration successful")

    except sqlite3.IntegrityError:
        print("\n❎ Username or Phone already registered!")



    # ---------      VIEW ALL DONORS     ---------

def all_donors():
    print("========== DONOR DETAILS ==========")
    print("\nID | Name | Blood Group |   Phone Number   |   Location   | Availability ")
    query = """
    SELECT donor_id,name, blood_group, phone, location, availability FROM donors
    """
    c.execute(query)
    results = c.fetchall()
    for donor in results:
        donor_id,name, blood_group, phone, location, availability = donor
        print(f"{donor_id} | {name} | {blood_group} | {phone} | {location} | {availability}")
    print()
    return 


        # ---------      SEARCH BY BLOOD GROUP & LOCATION    ---------           
    

def search_blood_group():
    blood_group=input("Enter Blood Group : ").upper().strip()
    location=input("Enter the location   : ").upper().strip()
    # Validate input
    if not blood_group:
        print("You entered nothing.")
    elif len(blood_group) < 2:
        print(f"Enter atleast 2 characters (eg : b+ve/a-ve/o+ve etc.) ")
    else:
        blood_group = blood_group.upper()
        #print(blood_group)
        c.execute("""
        SELECT donor_id,name, blood_group, phone, location, availability FROM donors 
        WHERE blood_group=? AND location=? AND availability = 'Y'""",(blood_group,location))
        results=c.fetchall()
        if results:
            print("---------DONOR DETAILS---------")
            for res in results:
                donor_id,name, blood_group, phone, location, availability = res
                print(f"{donor_id} | {name} | {blood_group} | {phone} | {location} | {availability}")
        else:
            print("Sorry! None is Available Now")
    return

    # ---------      UPDATE DONOR'S PASSWORD     ---------
def change_password(username):
    c.execute("SELECT password FROM donors where username=?",[username])
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
            c.execute("UPDATE donors SET password=? WHERE username=?", (new_pass, username))
            con.commit()
            print("\n✅Password updated.")
            print("Login With New Password..")
        exit()
    else:
        print("\n❎Password Not Matched.")
    return


    # ---------      UPDATE DONOR'S AVAILABILITY     ---------

def update_availability(username):
    #username=input("Enter Donor's Username :")
    avail = input("Enter your availability (Y/N): ").upper()
    if avail not in ['Y','N']:
        print("Invalid Updation")
    else:
        c.execute("UPDATE donors SET availability=? WHERE username=?", (avail, username))
        con.commit()
        if c.rowcount>0:
            print("\n✅Availability updated.")
        else:
            print("\n❎User not Found")


    # ---------      DELETE DONOR USING USERNAME     ---------

def delete_donor():
    username=input("Enter Username to Delete :")
    query=c.execute("DELETE FROM donors WHERE username=?",[username])
    con.commit()
    if c.rowcount>0:
        print("\n✅Deleted Successfully!")
    else:
        print("\nUser Not Found!")



    # ---------      VIEW PARTICULAR DONOR'S DETAILS     ---------

def view_donor(username):
    c.execute("SELECT * FROM donors WHERE username = ?", (username,))
    data = c.fetchone()
    if data is None:
        print("❎Donor not Found!")
        return
    else:
        print("\n=====Profile Details======\n")
        print(f"ID          : {data[0]}")
        print(f"Name        : {data[1]}")
        print(f"Age         : {data[2]}")
        print(f"Gender      : {data[3]}")
        print(f"Blood Group : {data[4]}")
        print(f"Phone       : {data[5]}")
        #print(f"Username   : {data[6]}")
        #print(f"Password   : {data[7]}")
        print(f"Location    : {data[8]}")
        print(f"Availability: {data[9]}")
        print("")


    # ---------       DONOR'S MENU     ---------

def donor_menu(username):
    c.execute("SELECT * FROM donors WHERE username = ?", (username,))
    result = c.fetchone()

    print("\nWelcome,", result[1])
    while True:
        print("1. View Profile\n2. Edit Availability\n3. Change Password\n4. Delete Account\n5. Logout")
        try:
            choice = int(input("Enter choice : "))
        except ValueError:
            print("Enter numbers only")
            continue
        if choice == 1:
            view_donor(username)
        elif choice == 2:
            update_availability(username)
        elif choice == 3:
            change_password(username)
        elif choice==4:
            delete_donor()
            break
        elif choice==5:
            print("\n✅Logged out successfully")
            break
        else:
            print("❌ Option not implemented yet.")

