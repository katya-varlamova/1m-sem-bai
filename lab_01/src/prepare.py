import sqlite3
import csv
from sign import *
import os
from os import listdir
from os.path import isfile, join
import random
def PrepareData():
    signature = Signature()
    N = 10
    BOOKS_DIR = "./books"
    KEYS_DIR = "./keys"
    CERTS_DIR = "./certs"
    pubs = []
    for i in range(1, N + 1):
        pub, pri = signature.GenerateKeys()
        pubs.append(pub)
        with open(join(KEYS_DIR, "pub_{}.txt".format(i)), "w") as f:
            f.write(pub)
        with open(join(KEYS_DIR, "pri_{}.txt".format(i)), "w") as f:
            f.write(pri)
    with open("keys.csv", "w") as f:
        f.write("private_key,\n")
        for pub in pubs:
            f.write(pub + ",\n")
        
    filenames = [f for f in listdir(BOOKS_DIR) if isfile(join(BOOKS_DIR, f))]

    for fn in filenames:
        data = None
        with open(join(BOOKS_DIR, fn), "rb") as file:
            data = file.read()
        i = random.randint(1, N)
        private_key = ""
        with open(join(KEYS_DIR, "pri_{}.txt".format(i))) as file:
            private_key = file.readline()
        cert = signature.sign(data, private_key)
        with open(join(CERTS_DIR, os.path.splitext(fn)[0] + "_cert.key".format(i)), "wb") as file:
            file.write(cert)
        
def CreateDatabase():
    # Создание соединения с базой данных
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()

    # Создание таблицы Account
    c.execute('''CREATE TABLE IF NOT EXISTS account
                 (id INTEGER PRIMARY KEY,
                  login TEXT NOT NULL,
                  pass TEXT NOT NULL)''')

    # Создание таблицы EmploeeAccount
    c.execute('''CREATE TABLE IF NOT EXISTS EmploeeAccount
                 (id_acc INTEGER PRIMARY KEY,
                  dateOfMedBookExp DATE,
                  expDateMedDirection DATE,
                  MedDirection BLOB,
                  certMedBook BLOB,
                  certMedDirection BLOB,
                  MedBook BLOB,
                  FOREIGN KEY (id_acc) REFERENCES account(id))''')

    # Создание таблицы OrganizationPublicKeys
    c.execute('''CREATE TABLE IF NOT EXISTS OrganizationPublicKeys
                 (public_key TEXT)''')
    
    with open('keys.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            c.execute(f"INSERT INTO OrganizationPublicKeys (public_key) VALUES ('{row[0]}')")

    # Создание таблицы HRAccount
    c.execute('''CREATE TABLE IF NOT EXISTS HRAccount
                 (id_acc INTEGER PRIMARY KEY,
                  private_key TEXT,
                  FOREIGN KEY (id_acc) REFERENCES account(id))''')


    # Сохранение изменений и закрытие соединения с базой данных
    conn.commit()
    conn.close()
PrepareData()
CreateDatabase()
