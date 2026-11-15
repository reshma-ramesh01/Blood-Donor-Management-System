import sqlite3
from datetime import datetime
import donor
con = sqlite3.connect("blood_donor.db")
c = con.cursor()

    # ---------      REQUEST FOR BLOOD     ---------

def request_blood():
    c.execute("""
    CREATE TABLE IF NOT EXISTS blood_requests(
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,patient_name TEXT,
        blood_group TEXT,hospital_name TEXT,
        location TEXT, units_required INTEGER,
        request_date TEXT,status TEXT
    )
    """)
    print("---------- FILL THE FORM ------------")
    patient_name=input("Enter Patient Name : ").upper()
    if not patient_name.replace(" ","").isalpha():
        print("Invalid patient name")
        return
    blood_group=input("Enter Patient Blood Group : ").upper()
    VALID_BLOOD_GROUPS = ["A+VE","A-VE","B+VE","B-VE","AB+VE","AB-VE","O+VE","O-VE"]
    if blood_group not in VALID_BLOOD_GROUPS:
        print("Invalid blood group")
        return
    hospital_name=input("Enter Hospital Name : ").upper()
    location=input("Enter Location : ").upper()
    units_required=int(input("Enter Required Units : "))
    if units_required <= 0:
        print("Units must be greater than zero")
        return
    request_date=input("Enter Date (dd-mm-yyyy) : ")
    try:
        datetime.strptime(request_date,"%d-%m-%Y")
    except ValueError:
        print("Date format should be dd-mm-yyyy")
        exit()

    status="PENDING" #by default, later can change this to completed
    try:
        c.execute("""
            INSERT INTO blood_requests(patient_name,blood_group,hospital_name,location,
            units_required,request_date,status) VALUES(?,?,?,?,?,?,?)""",
            (patient_name,blood_group,hospital_name,location,units_required,request_date,status))
        con.commit()
        print("✅Blood Requested Successfully!")
    except sqlite3.IntegrityError:
        print("\n❎ Patient already registered!")


    # ---------      VIEW ALL BLOOD REQUESTS     ---------

def view_blood_requests():
    print("=========== BLOOD REQUESTS ============")
    result=c.execute("SELECT * FROM blood_requests WHERE status='PENDING'")
    for req in result:
        print("ID               : ",req[0])
        print("Name             : "+req[1])
        print("Blood Group      : "+req[2])
        print("Hospital         : "+req[3])
        print("Locaion          : "+req[4])
        print("Units            : ",req[5])
        print("Date(dd-mm-yyyy) : "+req[6])   
        print("Status           : "+req[7])
        print("-----------------------------------------")   
    con.commit()

def blood_donation_details():
    print("=========== BLOOD DONATION DETAILS ============")
    # Enable foreign key support in SQLite
    c.execute("PRAGMA foreign_keys = ON")
    con.commit()
    c.execute("""
    CREATE TABLE IF NOT EXISTS donation_details (
        donation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        donor_id INTEGER,
        donation_date TEXT NOT NULL,
        blood_group TEXT NOT NULL,
        units_donated INTEGER NOT NULL,
        donation_centre TEXT,
        FOREIGN KEY (donor_id) REFERENCES donors(donor_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE 
    );
    """) 
    con.commit()
    # id donor delete, donation details also be deleted.(using cascade)
    print("-------- DONATION DETAILS -----------")
    donor_id=int(input("Donor ID                     : "))
    request_id=int(input("Blood Request ID            : "))
    donation_date=input("Donation Date(dd-mm-yyyy)    : ")
    try:
        datetime.strptime(donation_date,"%d-%m-%Y")
    except ValueError:
        print("Date format should be dd-mm-yyyy")
    blood_group=input("Blood Group                  : ").upper()
    VALID_BLOOD_GROUPS = ["A+VE","A-VE","B+VE","B-VE","AB+VE","AB-VE","O+VE","O-VE"]
    if blood_group not in VALID_BLOOD_GROUPS:
        print("Invalid blood group")
        return
    units_donated=int(input("Units Donated                : "))
    donation_centre=input("Donation Center              : ").upper()

    # INSERTING DATA TO DONATION DETAILS TABLE

    try:
        c.execute("""
            INSERT INTO donation_details(donor_id, donation_date, blood_group, units_donated, donation_centre)
            VALUES (?, ?, ?, ?, ?)""",(donor_id,donation_date,blood_group,units_donated,donation_centre))
        con.commit()
    except sqlite3.IntegrityError:
        print("❎ Data Already Exists")

     # UPDATE REQUIRED UNITS IN BLOOD REQUESTS TABLE
    c.execute("""
        UPDATE blood_requests
        SET units_required = units_required - ?
        WHERE request_id = ?
        """, (units_donated, request_id))
    c.execute("""
    UPDATE blood_requests
    SET units_required =
    CASE
        WHEN units_required - ? < 0 THEN 0
        ELSE units_required - ?
    END
    WHERE request_id=?
    """,(units_donated,units_donated,request_id))
    query=c.execute(" UPDATE blood_requests SET status='COMPLETED' WHERE request_id=? AND units_required <= 0",(request_id,))
    con.commit()
    if query:
        print("✅Donation Completed")


def completed_donations():
    print("=========== BLOOD DONATION ============")
    result=c.execute("SELECT * FROM blood_requests WHERE status='COMPLETED'")
    #res=c.execute("SELECT donor_id FROM donation_details WHERE donor_id=")
    for req in result:
        print("ID               : ",req[0])
        print("Name             : "+req[1])
        print("Blood Group      : "+req[2])
        print("Hospital         : "+req[3])
        print("Locaion          : "+req[4])
        #print("Units            : ",req[5])
        print("Date(dd-mm-yyyy) : "+req[6])   
        print("Status           : "+req[7])
        print("-----------------------------------------")   
    con.commit()
