from da import *
from sign import *
from structs import *
from datetime import datetime, timedelta
import os
import os.path

class BLFacade():
    def __init__(self):
        self.empRepo = EmploeeAccountRepository()
        self.hrRepo = HRAccountRepository()
        self.signature = Signature()
        self.keysRepo = OrganizationPublicKeysRepository()
        
    def Registration(self, login, password, role):
        if role == 'работник':
            self.empRepo.CreateAccount(login, password)
            return None
        elif role == "HR":
            pub, pri = self.signature.GenerateKeys()
            self.hrRepo.CreateAccount(login, password, pri)
            with open("pub_{}.txt".format(login), "w") as f:
                f.write(pub)
            return "pub_{}.txt"
        
    def Login(self, login, password):
        empacc = self.empRepo.GetEmploeeAccount(login, password)
        hracc = self.hrRepo.GetHRAccount(login, password)
        if hracc != None:
            return ("hr", hracc)
        if empacc != None:
            return ("emp", empacc)
        return (None, None)
    
    def ExistsEmploeeWithLogin(self, login):
        return self.empRepo.ExistsEmploeeWithLogin(login)
    
    def CreateMedDirection(self, hrAcc, login, path, date):     
        MedDirection = None
        with open(path, "rb") as file:
            MedDirection = file.read()
        certMedDirection = self.signature.sign(MedDirection, hrAcc.GetPrivateKey())
        self.empRepo.UploadDirection(login, date, MedDirection, certMedDirection)

    def GetEmploeesInfo(self):
        return self.empRepo.GetEmploeesInfo()

    def GetEmploeeAccount(self, login, password):
        return self.empRepo.GetEmploeeAccount(login, password)

    def CheckMedBook(self, empAcc, MedBook, certMedBook, date):       
        keys = self.keysRepo.GetKeys()
        for public_key in keys:
            if self.signature.check(MedBook, certMedBook, public_key):
                self.empRepo.UploadMedBook(empAcc.GetAccount().GetLogin(),
                                  date, MedBook, certMedBook)
                return True
        return False
    
    
        
