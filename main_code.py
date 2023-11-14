import pickle as b
from getpass import getpass
import mysql.connector as m
from datetime import date
from uuid import uuid4 as uid
import time
import sys

mydb=m.connect(host="localhost",user="root",password="root")
cur=mydb.cursor()

usn=""

def opndb():
    dbname=str(usn)+"_raws"
    cur.execute("create database if not exists {}".format(dbname))
    cur.execute("use {}".format(dbname))
    cur.execute("create table if not exists ResDet(Apt_No varchar(10) primary key NOT NULL,Block char(2),Sq_Feet int,Name varchar(100) NOT NULL,ContactNo bigint NOT NULL,BloodGroup varchar(10),Occupation varchar(100))")
    cur.execute("create table if not exists CompltDet(Complaint_ID varchar(50) Primary Key NOT NULL,Apt_No varchar(10) NOT NULL,Date_Lodged date,Complaint text,Status varchar(50))")
    mydb.commit()

def credits():
    print("Thank You for Your Delightful support")
    print("A Shyaam and Team Project")
    sys.exit()
    
def Home_Screen():

    def Res_Details():
        def check_apartment_exists(apt_no):
            cur.execute("select count(*) from ResDet where Apt_No = '{}'".format(apt_no,))
            count = cur.fetchone()[0]

            if count == 0:
                return False
            else:
                return True
        
        def input_resdet():
            while True:
                apt_no = input("Enter apartment number: ")            
                block = input("Enter block: ")
                sq_feet = int(input("Enter square feet: "))
                
                print("Owner's Details:")
                name = input("Enter name: ")
                contact_no = int(input("Enter contact number: "))
                blood_group = input("Enter blood group: ")
                occupation = input("Enter occupation: ")
                
                cur.execute("insert into ResDet values ('{}','{}',{},'{}',{},'{}','{}')".format(apt_no, block,sq_feet,name, contact_no, blood_group, occupation))
                mydb.commit()
                con=input("Continue?(y/n):")
                
                if con=='n':
                    break
        
        def view_resdet():
            apt_no=input("Enter Apartment Number: ")
            cur.execute("select * from ResDet where Apt_No='{}'".format(apt_no))
            show_aptdet=cur.fetchone()

            if not show_aptdet:
                print("Enter Correct Details!!")
                return
            else:
                print("Apartment No:",show_aptdet[0],"\nBlock:",show_aptdet[1],"\nSquare Feet:",show_aptdet[2],"\nOwner's Details\nName:",show_aptdet[3],"\nContact No:",show_aptdet[4],"\nBlood Group:",show_aptdet[5],"\nOccupation:",show_aptdet[6])

        def update_aptdet():
            apt_no=input("Enter Apartment Number: ")
            if not check_apartment_exists(apt_no):
                    print("Apartment number does not exist.")
                    return
            else:
                print("Update Owner's Details: ")
                new_name=input("Name:")
                new_contct=int(input("Contact Number: "))
                new_bldgrp=input("Blood Group: ")
                new_occup=input("Occupation: ")
                cur.execute("update ResDet set Name='{}',ContactNo={},BloodGroup='{}',Occupation='{}' where Apt_No='{}'".format(new_name,new_contct,new_bldgrp,new_occup,apt_no))
                mydb.commit()    

        print("---------------------------------------")
        choice=input("1. Input\n2. Display\n3. Update\n4. Back\n")
        if choice=="1":    
            input_resdet()
        elif choice=="2":  
            view_resdet()
        elif choice=="3":
            update_aptdet()
        elif choice=="4":
            Home_Screen()
        else:
            print("Invalid choice")

    def Complaint():
    #* Lodges a complaint into the CompltDet table.

        def check_complaint_exists(complaint_id):
            cur.execute("select count(*) from CompltDet where Complaint_ID = '{}'".format(complaint_id))
            count = cur.fetchone()[0]
    
            if count == 0:
                return False
            else:
                return True

        def check_apartment_exists(apt_no):
            cur.execute("select count(*) from ResDet where Apt_No = '{}'".format(apt_no))
            count = cur.fetchone()[0]

            if count == 0:
                return False
            else:
                return True
            
        def register_complaint():
            complaint_id = uid()
            apt_no = input("Enter apartment number: ")

            if not check_apartment_exists(apt_no):
                print("Incorrect Apartment Number")
                return

            date_lodged = date.today()
            complaint = input("Enter complaint: ")
            status = "Pending"

            cur.execute("insert into CompltDet values ('{}','{}','{}','{}','{}')".format(complaint_id,apt_no, date_lodged, complaint, status))
            mydb.commit()
            print("Complaint lodged successfully!")

        def view_complaint():
            apt_no = input("Enter apartment number: ")
            cur.execute("select * from CompltDet where Apt_No = '{}'".format(apt_no,))

            rows = cur.fetchall()
            if not rows:
                print("No complaints found for this apartment.")
            else:
                print("Existing complaints:")
            for row in rows:
                print("Complaint ID: {} | Apartment No: {} | Date Lodged: {} | Complaint: {} | Status: {}".format(row[0], row[1], row[2], row[3], row[4]))

        def update_complaint():
            complaint_id = input("Enter complaint ID: ")

            if not check_complaint_exists(complaint_id):
                print("Complaint ID does not exist.")
                return

            new_complaint = input("Enter new complaint: ")

            cur.execute("update CompltDet set Complaint = '{}' where Complaint_ID = '{}'".format(new_complaint, complaint_id))
            mydb.commit()
            print("Complaint updated successfully!")
        
        def delete_complaint():
            complaint_id = input("Enter complaint ID: ")

            if not check_complaint_exists(complaint_id):
                print("Complaint ID does not exist.")
                return

            cur.execute("delete from CompltDet where Complaint_ID = '{}'".format(complaint_id))
            mydb.commit()
            print("Complaint deleted successfully!")
        
        def update_status():
            complaint_id = input("Enter complaint ID: ")
            if not check_complaint_exists(complaint_id):
                print("Complaint ID does not exist.")
                return
            new_status = input("Enter new status: ")

            cur.execute("update CompltDet set Status = '{}' where Complaint_ID = '{}'".format(new_status, complaint_id))
            mydb.commit()
            print("Complaint status updated successfully!")

        print("---------------------------------------")
        choice = input("Choose one of the following:\n1. Lodge a complaint\n2. View existing complaints\n3. Update an existing complaint\n4. Delete an existing complaint\n5. Update Status of an existing complaint\n6. Back\n")

        if choice == "1":
            register_complaint() 
        elif choice == "2":
            view_complaint()
        elif choice == "3":
            update_complaint()
        elif choice == "4":
            delete_complaint()
        elif choice == "5":
            update_status()
        elif choice == "6":
            Home_Screen()
        else:
            print("Invalid choice.")

    def Maintenance():

        #* Manages maintenance details in the MtnDet table.

        print("---------------------------------------")
        choice = input("Choose one of the following:\n1. Input\n2. Update\n3. Search\n4. Delete\n5. Back\n")

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

        elif choice == "5":
            Home_Screen()

        else:
            print("Invalid choice.")

    while True:
        print("---------------------------------------")
        print("Main Menu")
        choice = input("1. Flat and Resident Details\n2. Complaints\n3. Maintanence\n4. Exit\n")

        if choice == "1":
            Res_Details()
        elif choice == "2":
            Complaint()
        elif choice == "3":
            Maintenance()
        elif choice == "4":
            credits()
        else:
            print("Invalid choice. Please try again.")
        

def login():

    def newid():
        print("Creating New User",end='')
        for i in " ...\n":
            time.sleep(0.7)
            print(i,end='')

        nus=input("Enter New UserID:")
        npas=getpass("Enter New Password:")
        rpas=getpass("Re-enter Password:")
        if npas==rpas:
            with open("Credential.dat","rb") as cred:
                cred.seek(0)
                r=b.load(cred)
                r[nus]=npas
            with open("Credential.dat","wb") as cred:
                cred.seek(0)
                b.dump(r,cred)
            login()

    print("Login")
    print("Enter 'new' for New User")

    global usn 
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
            opndb()
            Home_Screen()
    except KeyError:
        print("UserID not Found")

login()
