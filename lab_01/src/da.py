import sqlite3
from structs import *
from datetime import datetime
class EmploeeAccountRepository:
    def __init__(self):
        self.conn = sqlite3.connect('hr_system.db')
        self.cursor = self.conn.cursor()
    def ExistsEmploeeWithLogin(self, login):
        query = f"SELECT * FROM account JOIN EmploeeAccount ON account.id=EmploeeAccount.id_acc WHERE login='{login}' "
        result = self.cursor.execute(query).fetchone()
        return result is not None
    def GetEmploeeAccount(self, login, password):
        self.UpdateMedBooks()
        self.UpdateDirections()
        query = f"SELECT * FROM account JOIN EmploeeAccount ON account.id=EmploeeAccount.id_acc WHERE login='{login}' AND pass='{password}'"
        result = self.cursor.execute(query).fetchone()
        if result is None:
            return None
        else:
            account = Account(result[0], result[1], result[2])
            emploeeAccount = EmploeeAccount(account, result[4], result[5], result[6], result[7], result[8], result[9])
            return emploeeAccount

    def CreateAccount(self, login, password):
        query = f"INSERT INTO account (login, pass) VALUES ('{login}', '{password}')"
        self.cursor.execute(query)
        account_id = self.cursor.lastrowid
        query = f"INSERT INTO EmploeeAccount (id_acc) VALUES ({account_id})"
        self.cursor.execute(query)
        self.conn.commit()

    def UploadMedBook(self, login, dateOfMedBookExp, MedBook, certMedBook):
        query = "UPDATE EmploeeAccount SET dateOfMedBookExp= ?, MedBook = ?, certMedBook= ? WHERE id_acc=(SELECT id FROM account WHERE login= ? )"
        self.cursor.execute(query, (dateOfMedBookExp, MedBook, certMedBook, login))
        self.conn.commit()

    def UploadDirection(self, login, expDateMedDirection, MedDirection, certMedDirection):
        query = "UPDATE EmploeeAccount SET expDateMedDirection = ?, MedDirection=?, certMedDirection=? WHERE id_acc=(SELECT id FROM account WHERE login=?)"
        self.cursor.execute(query, (expDateMedDirection, MedDirection, certMedDirection, login))
        self.conn.commit()
    def UpdateDirections(self):
        query = "SELECT id_acc, expDateMedDirection, MedDirection, certMedDirection FROM EmploeeAccount WHERE expDateMedDirection < ?"
        self.cursor.execute(query, (datetime.now(),))
        rows = self.cursor.fetchall()

        for row in rows:
            query = "UPDATE EmploeeAccount SET expDateMedDirection = NULL, MedDirection = NULL, certMedDirection = NULL WHERE id_acc = ?"
            self.cursor.execute(query, (row[0],))
    def UpdateMedBooks(self):
        query = "SELECT id_acc, dateOfMedBookExp, MedBook, certMedBook FROM EmploeeAccount WHERE dateOfMedBookExp < ?"
        self.cursor.execute(query, (datetime.now(),))
        rows = self.cursor.fetchall()

        for row in rows:
            query = "UPDATE EmploeeAccount SET dateOfMedBookExp = NULL, MedBook = NULL, certMedBook = NULL WHERE id_acc = ?"
            self.cursor.execute(query, (row[0],))
    def GetEmploeesInfo(self):
        self.UpdateMedBooks()
        self.UpdateDirections()
        query = "SELECT * FROM account JOIN EmploeeAccount ON account.id=EmploeeAccount.id_acc"
        results = self.cursor.execute(query).fetchall()
        emploees = []
        for result in results:
            account = Account(result[0], result[1], result[2])
            emploeeAccount = EmploeeAccount(account, result[4], result[5], result[6], result[7], result[8], result[9])
            emploees.append(emploeeAccount)
        return emploees
class HRAccountRepository:
    def __init__(self):
        self.conn = sqlite3.connect('hr_system.db')
        self.cursor = self.conn.cursor()
        
    def GetHRAccount(self, login, password):
        query = f"SELECT * FROM account JOIN HRAccount ON account.id=HRAccount.id_acc WHERE login='{login}' AND pass='{password}'"
        result = self.cursor.execute(query).fetchone()
        if result is None:
            return None
        else:
            account = Account(result[0], result[1], result[2])
            hrAccount = HRAccount(account, result[4])
            return hrAccount
    def CreateAccount(self, login, password, private_key):
        query = f"INSERT INTO account (login, pass) VALUES ('{login}', '{password}')"
        self.cursor.execute(query)
        account_id = self.cursor.lastrowid
        query = f"INSERT INTO HRAccount (id_acc, private_key) VALUES ({account_id}, '{private_key}')"
        self.cursor.execute(query)
        self.conn.commit()
class OrganizationPublicKeysRepository:
    def __init__(self):
        self.conn = sqlite3.connect('hr_system.db')
        self.cursor = self.conn.cursor()
        
    def GetKeys(self):
        query = f"SELECT public_key FROM OrganizationPublicKeys"
        results = self.cursor.execute(query).fetchall()
        keys = []
        for result in results:
            keys.append(result[0])
        return keys
