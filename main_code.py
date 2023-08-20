import pickle as b
from getpass import getpass
import mysql.connector as m

#! PART-1 User Creation and Login

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

#! PART-2

mydb=m.connect(host="localhost",user="root",password="root")
cur=mydb.cursor()

def opndb():
    cur.execute("create database if not exists ALMS;")
    cur.execute("use ALMS")
    cur.execute("create table if not exists AirDet(PlaneID char(10) NOT NULL,Name varchar(50),Date date,DepTime time,DeptLoc varchar(15),ArrTime time,ArrLoc varchar(15),Primary Key(PlaneID)) ")
    cur.execute("create table if not exists PackDet(PackageID char(10) NOT NULL,PlaneID char(10) NOT NULL,Type varchar(50),Weight int,Priorty char(1),Date date,Location varchar(15),Cost int,Primary Key(PackageID)) ")
    cur.execute("create table if not exists CusDet(CustomerID char(10) NOT NULL,Name varchar(50),PackageID varchar(10) NOT NULL,Address varchar(15),Primary Key(CustomerID)) ")
    mydb.commit()

def inp():
    pass

opndb()
