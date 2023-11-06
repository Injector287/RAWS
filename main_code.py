import pickle as b
from getpass import getpass
import mysql.connector as m
from datetime import date

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
    cur.execute("create table if not exists ResDet(Apt_No varchar(4) primary key NOT NULL,Block char(1),Name varchar(20) NOT NULL,ContactNo int NOT NULL,BloodGroup varchar(3),Occupation varchar(20))")
    cur.execute("create table if not exists MtnDet(Apt_No varchar(4) primary key,Block char(1),Sq_Feet int,Fees int,Due_Date date,Status varchar(10))")
    cur.execute("create table if not exists CompltDet(Apt_No varchar(4) primary key NOT NULL,Date_Lodged date,Complaint text,Status varchar(10))")
    mydb.commit()

def Res_Details():
  #* Inputs resident details into the ResDet table.
    print("1.Input\n2.Display\3.Update\n4.Delete")
    choice=input("Choice: ")
    if choice=="1":    
        while True:
            apt_no = input("Enter apartment number: ")
            block = input("Enter block: ")
            name = input("Enter name: ")
            contact_no = int(input("Enter contact number: "))
            blood_group = input("Enter blood group: ")
            occupation = input("Enter occupation: ")
            cur.execute("insert into ResDet values ('{}','{}','{}',{},'{}','{}')".format(apt_no, block, name, contact_no, blood_group, occupation))
            mydb.commit()
            con=input("Continue?(y/n):")
            if con=='n':
                break

    elif choice=="2":
        Enter_Aptno=input("Enter Apartment Number: ")
        cur.execute("select * from ResDet where Apt_No='{}'".format(Enter_Aptno))
        for i in cur:
            print(i)
  


def Complaint():
  #* Lodges a complaint into the CompltDet table.

  apt_no = input("Enter apartment number: ")
  date_lodged = date.today()
  complaint = input("Enter complaint: ")
  status = "Pending"

  cur.execute("insert into CompltDet values (?, ?, ?, ?)", (apt_no, date_lodged, complaint, status))
  mydb.commit()

def Maintenance():
  #* Manages maintenance details in the MtnDet table.

  apt_no = input("Enter apartment number: ")
  sq_feet = int(input("Enter square feet: "))
  fees = int(input("Enter fees: "))
  due_date = input("Enter due date: ")
  status = "Unpaid"

def inp():
    while True:
        print("Welcome to Resident Association Welfare System")
        print("1.Input Residents' Details\n2.Lodge a Complaint\n3.Manage Maintanence\n4.Exit")
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
