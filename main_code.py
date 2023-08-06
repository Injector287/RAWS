import pickle as b
from getpass import getpass

# PART-1 User Creation and Login

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

login()
