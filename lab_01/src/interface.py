from bl import *

class ConsoleInterface:
    
    def __init__(self):
        self.facade = BLFacade()
        
    def Registration(self):
        print("Логин: ")
        login = input()
        print("Пароль: ")
        password = input() 
        print("Роль (работник / HR): ")
        role = input()
        wrong = True
        while wrong:
            if role == 'работник':
                self.facade.Registration(login, password, role)
                wrong = False
            elif role == "HR":
                file=self.facade.Registration(login, password, role)
                print(("Ваш публичный ключ был сохранен в файл " + file).format(login) + ". передайте его в организацию, проводящую медосмотры.")
                wrong = False
            else:
                print("Неверно, попробуйте снова. Роль (работник / HR): ")
                role = input()
        
        print("Регистрация завершена успешно")
        
    def Login(self):
        print("Логин: ")
        login = input()
        print("Пароль: ")
        password = input()
        pair = self.facade.Login(login, password)
        if pair[0] == "hr":
            print("Вход в аккаунт HR завершен успешно")
        elif pair[0] == "emp":
            print("Вход в аккаунт работника завершен успешно")
        else:
            print("Вход не удался")
        return pair
        
    def HRAccount(self, hrAcc):
        self.HRAccountMenu()
        com = int(input())
        while com != 0:
            if com == 1:
                print("Имя работника: ")
                login = input()
                while not self.facade.ExistsEmploeeWithLogin(login):
                    print("Неверно. Имя работника: ")
                    login = input()
                
                print("Путь к файлу направления: ")
                path = input()  
                while not os.path.isfile(path):
                    print("Неверно. Путь к файлу направления: ")
                    path = input()
                    
                date = datetime.now() + timedelta(seconds=60)
                self.facade.CreateMedDirection(hrAcc, login, path, date)
                print("Направление для работника {} успешно загружено с датой истечения {}".format(login, date))
            elif com == 2:
                res = self.facade.GetEmploeesInfo()
                for emp in res:
                    print("Работник: ", emp.GetAccount().GetLogin())
                    date_format = "%Y-%m-%d %H:%M:%S.%f"
                    if emp.GetDateOfMedBookExp() != None:
                        dt = datetime.strptime(emp.GetDateOfMedBookExp(), date_format)
                        print("Медкнижка действует, до завершения:", dt - datetime.now())
                    else:
                        print("Медкнижка просрочена")
                    if emp.GetExpDateMedDirection() != None:
                        dt = datetime.strptime(emp.GetExpDateMedDirection(), date_format)
                        print("Направление действует, до завершения:", dt - datetime.now())
                    else:
                        print("Нет направлений")
                    print("------------------------------------------")
                print("Напоминиаем, что текущим законодательством предусмотрены штрафы с соответствии с КоАП от 20000 до 30000 на организацию")
            self.HRAccountMenu()
            com = int(input())
        print("Выход из аккаунта прошел успешно")

    def EmploeeAccount(self, empAcc):
        self.EmploeeAccountMenu()
        com = int(input())
        while com != 0:
            if com == 1:
                emp = self.facade.GetEmploeeAccount(empAcc.GetAccount().GetLogin(),
                                                empAcc.GetAccount().GetPassword())
                date_format = "%Y-%m-%d %H:%M:%S.%f"
                if emp.GetDateOfMedBookExp() != None:
                    dt = datetime.strptime(emp.GetDateOfMedBookExp(), date_format)
                    print("Медкнижка действует, до завершения:", dt - datetime.now())
                else:
                    print("Медкнижка просрочена")
                    print("Напоминиаем, что текущим законодательством предусмотрены штрафы с соответствии с КоАП:")
                    print("- отсутствие медицинской книжки: от 5000 до 15000 рублей")
                    print("- несвоевременное оформление медицинской книжки: от 1000 до 5000 рублей")
                    print("- Наличие фактов заболевания инфекционными заболеваниями, опасными для окружающих: от 3000 до 10000 рублей")
                if emp.GetExpDateMedDirection() != None:
                    dt = datetime.strptime(emp.GetExpDateMedDirection(), date_format)
                    print("Направление действует, до завершения:", dt - datetime.now())
                else:
                    print("Нет направлений")
            elif com == 2:
                emp = self.facade.GetEmploeeAccount(empAcc.GetAccount().GetLogin(),
                                                empAcc.GetAccount().GetPassword())
                md, cert = emp.GetMedDirection()
                with open("direction.pdf", "wb") as file:
                    file.write(md)
                with open("cert.key", "wb") as file:
                    file.write(cert)
                print("Направление выгружено в файлы direction.pdf и cert.key . Предоставьте ОБА файла в медицинскую организацию.")
            elif com == 3:

                    print("Путь к файлу медицинской книжки: ")
                    pathMB = input()  
                    while not os.path.isfile(pathMB):
                        print("Неверно. Путь к файлу медицинской книжки: ")
                        pathMB = input()
                        
                    print("Путь к файлу сертификата медицинской книжки: ")
                    pathCert = input()  
                    while not os.path.isfile(pathCert):
                        print("Неверно. Путь к файлу сертификата медицинской книжки: ")
                        pathCert = input()
                        
                    with open(pathMB, "rb") as file:
                        MedBook = file.read()
                    with open(pathCert, "rb") as file:
                        certMedBook = file.read()
                    
                    date = datetime.now() + timedelta(seconds=120)
                    res = self.facade.CheckMedBook(empAcc, MedBook, certMedBook, date)
                    if res:
                        print("Проверка достоверности медицинской книжки была пройдена успешно")
                    else:
                        print("Проверка достоверности медицинской книжки не была пройдена. Обратитесь в медицинскую организацию, предоставляющую книжку.")

            self.EmploeeAccountMenu()
            com = int(input())
        print("Выход из аккаунта прошел успешно")
        
    def MainMenu(self):
        print("1. Пройти регистрацию")
        print("2. Войти")
        print("0. Закончить")
        
    def HRAccountMenu(self):
        print("1. Выписать направление работнику")
        print("2. Просмотреть статус медкнижек всех работников")
        print("0. Выйти")
        
    def EmploeeAccountMenu(self):
        print("1. Просмотреть статус медкнижки")
        print("2. Скачать направление")
        print("3. Загрузить медкнижку")
        print("0. Выйти")
        
    def EmploeeAccountMenu(self):
        print("1. Просмотреть статус медкнижки")
        print("2. Скачать направление")
        print("3. Загрузить медкнижку")
        print("0. Выйти")
        
    def Run(self):
        self.MainMenu()
        res = int(input())
        while res != 0:
            if res == 1:
                self.Registration()
            elif res == 2:
                role, acc = self.Login()
                if role == None:
                    print("Попробуйте снова.")
                elif role == "emp":
                    self.EmploeeAccount(acc)
                elif role == "hr":
                    self.HRAccount(acc)
            self.MainMenu()
            res = int(input())
        
ConsoleInterface().Run()       
    
    
        
