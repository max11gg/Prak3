import pyodbc
from os import system, name
import os.path
import time
import pathlib
from pathlib import Path
import toAdmin
cnxn = pyodbc.connect('Driver={SQL Server};Server=LAPTOP-KMTJ6QG7\MYNAME;Database=Burger;Trusted_Connection=yes;')
cursor = cnxn.cursor()
def Supply(adminId):
    _ = system('cls')
    for row in cursor.execute(f"select * from [Admin] where [ID_Admin] = {adminId}"):
        balance = row.Balance_Admin

    print(f"На счету {balance} рублей.\n")

    nameIngridient, costIngridient, typeIngridient, countIngridient = [], [], [], []
    for row in cursor.execute("select * from [Ingridient] inner join [Type_Ingridient] on [Type_ID] = [ID_Type]"):
        nameIngridient.append(row.Name_Ingridient)
        costIngridient.append(row.Cost_Ingridient)
        typeIngridient.append(row.Name_Type)
        countIngridient.append(row.Count_Ingridient)

    for i in range(len(nameIngridient)):
        print(f"{i+1}-{typeIngridient[i]}-{nameIngridient[i]}-{countIngridient[i]} шт.-{costIngridient[i]} Рублей")
                        
    for count in range(len(nameIngridient)):
        countIngridients = count+1
    
    try:
        idIngridient = int(input("Выберите ингридиент для поставки: \n"))
    except ValueError:
        print("Введены неверные данные")
        time.sleep(2)
        Supply(adminId)

    if (idIngridient > 0 and idIngridient <= countIngridients):
        try:
            count = int(input("Введите количество поставки: \n"))
        except ValueError:
            print("Введены неверные данные")
            time.sleep(2)
            Supply(adminId)

        for row in cursor.execute(f"select * from [Ingridient] inner join [Type_Ingridient] on [Type_ID] = [ID_Type] where [ID_Ingridient] = {idIngridient}"):
            currentName = row.Name_Ingridient
            currentCount = row.Count_Ingridient
            currentCost = row.Cost_Ingridient
            currentType = row.Name_Type

        endCount = currentCount + count
        sum = count * currentCost

        confirm = input(f"Поставка {currentType} - {currentName} в количестве {count} шт. - {sum} Рублей\n"
                        "'+'- добавить еще. '-' - завершить заказ?\n").lower()
        
        if confirm == "+":
            balance -= sum
            if balance >= 0:
                cursor.execute(f"update [Admin] set [Balance_Admin] = {balance} where [ID_Admin] = {adminId}")
                cnxn.commit()
                print("Выполняется заказ...")
                cursor.execute(f"update [Ingridient] set [Count_Ingridient] = {endCount} where [ID_Ingridient] = {idIngridient}")
                cnxn.commit()
                
                time.sleep(2)
                print("Заказ выполнен!")
                Supply(adminId)
            else:
                print("Недостаточно средств на счету.")
                time.sleep(2)
                Supply(adminId)
        elif confirm == "-":
            print("Отмена заказа...")
            time.sleep(2)
            Supply(adminId)
        else:
            print("Неправильный ввод.")
            time.sleep(2)
            Supply(adminId)
    elif idIngridient == 0:
        toAdmin.toAdmin(adminId)
    else:
        print("Некорректные данные")
        time.sleep(2)
        Supply(adminId)