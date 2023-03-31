import pyodbc
from os import system, name
import os.path
import time
import pathlib
from pathlib import Path
import Supply
cnxn = pyodbc.connect('Driver={SQL Server};Server=LAPTOP-KMTJ6QG7\MYNAME;Database=Burger;Trusted_Connection=yes;')
cursor = cnxn.cursor()
checkId = []
def Admin(adminId):
    _ = system('cls')
    for row in cursor.execute(f"select * from [Admin] where [ID_Admin] = '{adminId}'"):
         balance = row.Balance_Admin

    print(f"У вас на счету {balance} рублей.\n")
    try:
        function = int(input("Выберите функцию\n"
        "1 - Заказать ингридиент\n"
        "2 - История покупок пользователей\n"
        "3 - Карты лояльности пользователей\n"
        "4 - Выйти из аккаунта\n"
        "5 - Изменение цены\n"))
    except ValueError:
        print("Введены неверные данные")
        time.sleep(2)
        Admin(adminId)

    if function > 0 and function <= 5:
        match function:
            case 1:
                Supply.Supply(adminId)
            case 2:
                AdminUsersHistory(adminId)
            case 3:
                AdminUsersLoyality(adminId)
            case 4:
                exit()
            case 5:
                AdminUpdateIngredients(adminId)
    else:
        print("Неправильная функция.")
        Admin(adminId)


def AdminUsersHistory(adminId):
    _ = system('cls')
    userId, phoneUser, passwordUser, balanceUser, chequeId = [], [], [], [], []
    countFiles = 0
    for row in cursor.execute("select * from [User]"):
        userId.append(row.ID_User)
        phoneUser.append(row.Email_User)
        passwordUser.append(row.Password_User)
        balanceUser.append(row.Balance_User)

    print("Пользователи:\n")
    for i in range(len(userId)):
        print(f"{userId[i]} - {phoneUser[i]} - {passwordUser[i]} - {balanceUser[i]}")
    
    try:
        idUser = int(input("Выберите пользователя для просмотра истории: \n"
                           "0 - Выйти на главную.\n"))
    except ValueError:
        print("Введены неверные данные")
        time.sleep(2)
        AdminUsersHistory(adminId)

    if idUser > 0 and idUser <= len(userId) and userId.count(idUser) > 0:
        for row in cursor.execute(f"select * from [Check] where [User_ID] = {idUser}"):
            checkId.append(row.ID_Check)
        for id in range(len(checkId)):
            directory = Path(pathlib.Path.cwd(), 'Check', f'Check{checkId[id]}.txt')
            if (os.path.exists(directory)):
                file = open(directory, 'r')
                strings = file.readlines()
                file.close()
                print("\n")
                for i in range(len(strings)):
                    print(strings[i])
                countFiles += 1
        if countFiles == 0:
            print("У пользователя еще нет истории. \n")
        input("Выйти на главную.")
        Admin(adminId)
    elif (idUser == 0):
        Admin(adminId)
    else:
        print("Неверное действие")
        time.sleep(2)
        AdminUsersHistory(adminId)

def AdminUsersLoyality(adminId):
    _ = system('cls')
    userId, phoneUser, passwordUser, balanceUser = [], [], [], []
    for row in cursor.execute("select * from [User]"):
        userId.append(row.ID_User)
        phoneUser.append(row.Email_User)
        passwordUser.append(row.Password_User)
        balanceUser.append(row.Balance_User)

    print("Пользователи:\n")
    for i in range(len(userId)):
        print(f"{userId[i]} - {phoneUser[i]} - {passwordUser[i]} - {balanceUser[i]}")
    
    try:
        idUser = int(input("\nВыберите пользователя для просмотра карты лояльности: \n"))
    except ValueError:
        print("Введены неверные данные")
        time.sleep(2)
        AdminUsersLoyality(adminId)

    if (idUser > 0 and idUser <= len(userId) and userId.count(idUser) > 0):
        for row in cursor.execute(f"select * from [User] inner join [Card_Loyality] on [Loyality_ID] = [ID_Loyality] where [ID_User] = {idUser}"):
            nameLoyality = row.Name_Loyality
            discountLoyality = row.Discount
            discount = discountLoyality * 100
        print(f"Ваша программа лояльности: {nameLoyality}, скидка: {discount}%\n")
        input("Выйти на главную")
        Admin(adminId)
    elif (idUser == 0):
        Admin(adminId)
    else:
        print("Неверное действие.")
        time.sleep(2)
        AdminUsersLoyality(adminId)
        
def AdminUpdateIngredients(adminId):
    _ = system('cls')


    for row in cursor.execute("select * from [Ingridient]"):
        nameIngridient = row.Name_Ingridient
        costIngridient = row.Cost_Ingridient
        countIngridient = row.Count_Ingridient
        print(" Название: ", nameIngridient, ", Количество: ", costIngridient, ", Цена: ", countIngridient)

    try:
        idIngridient = int(input("\nВыберите ингредиент: \n"))
    except ValueError:
        Admin(adminId)
    try:
        IngridientPrice = int(input("\nВведите цену ингредиента \n"))
    except ValueError:
        print("Ошибка!")
        AdminUpdateIngredients(adminId)
    if (idIngridient > 0):
        cursor.execute(f"update [Ingridient] set [Cost_Ingridient] = {IngridientPrice} where [ID_Ingridient] = {idIngridient}")
        cnxn.commit()
        input("Вернуться к функциям")
        Admin(adminId)
    else:
        print("Ошибка! Такого ингредиента нет.")
        time.sleep(2)
        AdminUsersLoyality(adminId)