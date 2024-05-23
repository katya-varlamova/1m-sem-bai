class Account:
    def __init__(self, id, login, password):
        self.id = id
        self.login = login
        self.password = password
    def GetLogin(self):
        return self.login
    def GetPassword(self):
        return self.password

class EmploeeAccount:
    def __init__(self, account, dateOfMedBookExp=None, expDateMedDirection = None, pathOfMedDirection=None, certMedBook=None, certMedDirection=None, pathOfMedBook=None):
        self.account = account
        self.dateOfMedBookExp = dateOfMedBookExp
        self.expDateMedDirection = expDateMedDirection
        self.MedDirection = pathOfMedDirection
        self.certMedBook = certMedBook
        self.certMedDirection = certMedDirection
        self.MedBook = pathOfMedBook
    def GetAccount(self):
        return self.account
    def GetDateOfMedBookExp(self):
        return self.dateOfMedBookExp
    def GetExpDateMedDirection(self):
        return self.expDateMedDirection
    def GetMedDirection(self):
        return (self.MedDirection, self.certMedDirection)

class HRAccount:
    def __init__(self, account, private_key):
        self.account = account
        self.private_key = private_key
    def GetPrivateKey(self):
        return self.private_key
