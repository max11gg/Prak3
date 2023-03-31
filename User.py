import pyodbc
from os import system, name
import os.path
import time
import pathlib
from pathlib import Path
import Order
cnxn = pyodbc.connect('Driver={SQL Server};Server=LAPTOP-KMTJ6QG7\MYNAME;Database=Burger;Trusted_Connection=yes;')
cursor = cnxn.cursor()

def Users(userId, adminId):
    _ = system('cls')
    for row in cursor.execute(f"select * from [User] inner join [Card_Loyality] on [Loyality_ID] = [ID_Loyality] where [ID_User] = '{userId}'"):
         balance = row.Balance_User

    print(f"У вас на счету {balance} рублей.\n")
    try:
        function = int(input("Выберите функцию\n"
        "1 - Заказать блюдо\n"
        "2 - История покупок\n"
        "3 - Карта лояльности\n"
        "4 - Выйти из аккаунта\n"))
    except ValueError:
        print("Введены неверные данные")
        time.sleep(2)
        Users(userId)

    if function > 0 and function <= 4:
        match function:
            case 1:
                Order.Orders(adminId, userId)
            case 2:
                UserHistory(adminId, userId)
            case 3:
                UserLoyality(adminId, userId)
            case 4:
                #Main.mainwindow()
                exit()
    else:
        print("Неправильная функция.")
        Users(userId)

def UserHistory(adminId, userId):
    print("Собираем историю...")
    time.sleep(2)
    checkId = []
    countFiles = 0
    for row in cursor.execute(f"select * from [Check] where [User_ID] = {userId}"):
        checkId.append(row.ID_Check)
    for i in range(len(checkId)):
        print(checkId[i])
    for id in range(len(checkId)):
        directory = Path(pathlib.Path.cwd(), 'Check', f'Check{checkId[id]}.txt')
        if (os.path.exists(directory)):
            file = open(directory, 'r')
            strings = file.readlines()
            file.close()
            for i in range(len(strings)):
                print(strings[i])
            countFiles += 1
    if countFiles == 0:
        print("У вас еще нет истории. \n")
    input("Выйти на главную")
    Users(adminId, userId)

def UserLoyality(adminId, userId):
    _ = system('cls')
    for row in cursor.execute(f"select * from [User] inner join [Card_Loyality] on [Loyality_ID] = [ID_Loyality] where [ID_User] = {userId}"):
        nameLoyality = row.Name_Loyality
        discountLoyality = row.Discount
        discount = discountLoyality * 100
    print(f"Ваша программа лояльности: {nameLoyality}, скидка: {discount}%\n")
    input("Выйти на главную")
    Users(adminId, userId)