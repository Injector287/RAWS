import pickle as b
from getpass import getpass
import mysql.connector as m
from datetime import date
from uuid import uuid4 as uid

#* PART-1 User Creation and Login

def newid():
    print("Creating New User...")
    nus=input("Enter New UserID:")
    npas=getpass("Enter New Password:")
    rpas=getpass("Re-enter Password:")
    if npas==rpas:
        print(npas,rpas)
        with open("Credential.dat","rb") as cred:
            cred.seek(0)
            r=b.load(cred)
            r[nus]=npas
        with open("Credential.dat","wb") as cred:
            cred.seek(0)
            b.dump(r,cred)

def login():
    print("Login")
    print("Enter 'new' for New User")
    usn=input("Enter UserID:")
    if usn=='new':
        newid()
    pas=getpass("Enter Password:")
    with open("Credential.dat","rb") as cred:
            cred.seek(0)
            r=b.load(cred)
    try:
        if r[usn]==pas:
            print('Access Granted')
    except KeyError:
        print("UserID not Found")
    else:
        print("Password Incorrect")
#login()

#* PART-2 

mydb=m.connect(host="localhost",user="root",password="root")
cur=mydb.cursor()

def opndb():
    cur.execute("create database if not exists RAWS;")
    cur.execute("use RAWS")
    cur.execute("create table if not exists ResDet(Apt_No varchar(4) primary key NOT NULL,Block char(1),Sq_Feet int,Name varchar(20) NOT NULL,ContactNo int NOT NULL,BloodGroup varchar(3),Occupation varchar(20))")
    cur.execute("create table if not exists CompltDet(Complaint_ID varchar(50) Primary Key NOT NULL,Apt_No varchar(4) NOT NULL,Date_Lodged date,Complaint text,Status varchar(10))")
    mydb.commit()

def Res_Details():
  #* Inputs resident details into the ResDet table.
    print("1.Input\n2.Display\n3.Update")
    choice=input("Choice: ")
    if choice=="1":    
        while True:
            apt_no = input("Enter apartment number: ")
            block = input("Enter block: ")
            sq_feet = int(input("Enter square feet: "))
            
            name = input("Enter name: ")
            contact_no = int(input("Enter contact number: "))
            blood_group = input("Enter blood group: ")
            occupation = input("Enter occupation: ")
            
            cur.execute("insert into ResDet values ('{}','{}',{},'{}',{},'{}','{}')".format(apt_no, block,sq_feet,name, contact_no, blood_group, occupation))
            mydb.commit()
            con=input("Continue?(y/n):")
            
            if con=='n':
                break

    elif choice=="2":
        Enter_Aptno=input("Enter Apartment Number: ")
        cur.execute("select * from ResDet where Apt_No='{}'".format(Enter_Aptno))
        show_aptdet=cur.fetchone()
        print("Apartment No:",show_aptdet[0],"\nBlock:",show_aptdet[1],"\nSquare Feet:",show_aptdet[2],"\nOwner's Details\nName:",show_aptdet[3],"\nContact No",show_aptdet[4],"\nBlood Group",show_aptdet[5],"\nOccupation No",show_aptdet[6])

    elif choice=="3":
        Enter_Aptno=input("Enter Apartment Number: ")
        print("Update Owner's Details: ")
        new_name=input("Name:")
        new_contct=int(input("Contact Number: "))
        new_bldgrp=input("Blood Group: ")
        new_occup=input("Occupation: ")
        cur.execute("update ResDet set Name='{}',ContactNo={},BloodGroup='{}',Occupation='{}' where Apt_No='{}'".format(new_name,new_contct,new_bldgrp,new_occup,Enter_Aptno))
        mydb.commit()

def Complaint():
  #* Lodges a complaint into the CompltDet table.

    choice = input("Choose one of the following:\n1. Lodge a complaint\n2. View existing complaints\n3. Update an existing complaint\n4. Delete an existing complaint\n5.Update Status of an existing complaint\n")

    if choice == "1":
        # Lodge a complaint
        complaint_id = uid()
        apt_no = input("Enter apartment number: ")
        date_lodged = date.today()
        complaint = input("Enter complaint: ")
        status = "Pending"

        cur.execute("insert into CompltDet values ('{}','{}','{}','{}','{}')".format(complaint_id,apt_no, date_lodged, complaint, status))
        mydb.commit()
        print("Complaint lodged successfully!")

    elif choice == "2":
        # View existing complaints
        apt_no = input("Enter apartment number: ")
        cur.execute("select * from CompltDet where Apt_No = '{}'".format(apt_no,))

        rows = cur.fetchall()
        if not rows:
            print("No complaints found for this apartment.")
        else:
            print("Existing complaints:")
        for row in rows:
            print("Complaint ID: {} | Apartment No: {} | Date Lodged: {} | Complaint: {} | Status: {}".format(row[0], row[1], row[2], row[3], row[4]))

    elif choice == "3":
        # Update an existing complaint
        complaint_id = input("Enter complaint ID: ")
        new_complaint = input("Enter new complaint: ")

        cur.execute("update CompltDet set Complaint = {} where Complaint_ID = {}".format(new_complaint, complaint_id))
        mydb.commit()
        print("Complaint updated successfully!")

    elif choice == "4":
        # Delete an existing complaint
        complaint_id = input("Enter complaint ID: ")

        cur.execute("delete from CompltDet where Complaint_ID = '{}'".format(complaint_id))
        mydb.commit()
        print("Complaint deleted successfully!")

    elif choice == "5":
    # Update status of existing complaint
        complaint_id = input("Enter complaint ID: ")
        new_status = input("Enter new status: ")

        cur.execute("update CompltDet set Status = '{}' where Complaint_ID = '{}'".format(new_status, complaint_id))
        mydb.commit()
        print("Complaint status updated successfully!")


    else:
        print("Invalid choice.")

def Maintenance():

    #* Manages maintenance details in the MtnDet table.

    choice = input("Choose one of the following:\n1. Input maintenance details\n2. Update maintenance details\n3. Search maintenance details\n4. Delete maintenance details via apartment\n")

    if choice == "1":
        # Input maintenance details
        cur.execute("drop table if exists MtnDet")
        cur.execute("create table MtnDet as select Apt_No,Sq_Feet from ResDet")
        cur.execute("alter table MtnDet add column Due_Date date,add column Fees int,add column Status varchar(20)")
        
        Due_date=input("Enter Common Due Date:")
        CPSF=int(input("Enter Cost Per Square Feet:"))
        status='Unpaid'

        cur.execute("update MtnDet set Due_Date='{}',Fees=Sq_Feet*{},Status='{}'".format(Due_date,CPSF,status))
        mydb.commit()
        print("Maintenance details input successfully!")

    elif choice == "2":
        # Update maintenance details
        apt_no = input("Enter apartment number: ")
        new_fees = input("Enter new fees: ")
        new_due_date = input("Enter new due date: ")
        new_status=input("Enter Status:")

        cur.execute("update MtnDet set Fees = '{}', Due_Date = '{}', Status = '{}' where Apt_No = '{}'".format(new_fees, new_due_date,new_status,apt_no))
        mydb.commit()
        print("Maintenance details updated successfully!")

    elif choice == "3":
        # Search maintenance details
        status = input("Enter status: ")

        cur.execute("select * from MtnDet where Status = '{}'".format(status))
        rows = cur.fetchall()

        if not rows:
            print("No maintenance details found for this status.")
        else:
            print("Maintenance details:")
        for row in rows:
            print("Apartment No: {} | Square Feet: {} | Due Date: {} | Fees: {} | Status: {}".format(row[0], row[1], row[2], row[3], row[4]))

    elif choice == "4":
        # Delete maintenance details
        apt_no = input("Enter apartment number: ")

        cur.execute("delete from MtnDet where Apt_No = '{}'".format(apt_no))
        mydb.commit()
        print("Maintenance details deleted successfully!")

    else:
        print("Invalid choice.")

def inp():
    while True:
        print("Welcome to Resident Association Welfare System")
        print("1. Flat and Resident Details\n2. Complaints\n3. Maintanence\n4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            Res_Details()
        elif choice == "2":
            Complaint()
        elif choice == "3":
            Maintenance()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")
            break

opndb()
inp()
