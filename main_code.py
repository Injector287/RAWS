import pickle as b

def newid():
    nus=input("Enter New UserID:")
    npas=input("Enter New Password:")
    rpas=input("Re-enter Password:")
    if npas==rpas:
        with open("D:\\Shyaam\\Project\\The_Ultimate_Project\\Credential.dat","rb") as cred:
            cred.seek(0)
            r=b.load(cred)
            r[nus]=npas
        with open("D:\\Shyaam\\Project\\The_Ultimate_Project\\Credential.dat","wb") as cred:
            cred.seek(0)
            b.dump(r,cred)

                   
newid()
