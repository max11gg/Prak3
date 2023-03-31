import pyodbc
import CloseOrder
from os import system, name
import os.path
import time
import pathlib
from pathlib import Path
import Check
import OrderCompletion
cnxn = pyodbc.connect('Driver={SQL Server};Server=LAPTOP-KMTJ6QG7\MYNAME;Database=Burger;Trusted_Connection=yes;')
cursor = cnxn.cursor()
endIdBurgers = []
def Orders(adminId, userId):
    _ = system('cls')
    try:
        count = int(input("Сколько блюд?\n"))
    except ValueError:
        print("Введены неверные данные")
        time.sleep(2)
        Orders(userId)
    if (count > 0):
        Check.Cheque(userId, count)

        for i in range(count):
            print(f"Собираем блюдо №{i+1}... \n")

            ingridients = []
            addIngridients = True

            while addIngridients ==True:
                nameIngridient, costIngridient, typeIngridient = [], [], []
                print("Ингридиенты: \n")

                for row in cursor.execute("select * from [Ingridient] inner join [Type_Ingridient] on [Type_ID] = [ID_Type]"):
                    nameIngridient.append(row.Name_Ingridient)
                    costIngridient.append(row.Cost_Ingridient)
                    typeIngridient.append(row.Name_Type)


                print("0 - Не выбирать ингридиент\n")
                for i in range(len(nameIngridient)):
                    print(i+1, "-", typeIngridient[i], "-", nameIngridient[i], "-", costIngridient[i], "Рублей")
                            
                for count in range(len(nameIngridient)):
                    countIngridient = count+1

                print("Выберите ингридиент: \n")
                try:
                    ingridient = int(input())
                except ValueError:
                    print("Введены неверные данные")
                    time.sleep(2)
                    Orders(userId)
                        
                if (ingridient <= countIngridient and ingridient > 0):
                    ingridients.append(ingridient-1)
                elif ingridient == 0:
                    print("Пожелания учтены\n")
                else:
                    print("Неправильный ингридиент.")
                    Orders(userId)

                continueAdd = input("'+', чтобы продолжить.'-', чтобы остановиться.\n").lower()
                if continueAdd == "+":
                    addIngridients = True
                elif continueAdd == "-":
                    addIngridients = False
                else:
                    print("Ошибка выбора\n")
                    time.sleep(2)
                    Orders(userId)

            print("Заканчиваем сборку... \n")
            for i in range(len(ingridients)):
                print(nameIngridient[ingridients[i]], " - ", costIngridient[ingridients[i]], "Рублей \n")
                    
            time.sleep(5)

            cursor.execute(f"insert into [Burgers] ([Cost_Burgers]) values (100)")
            cnxn.commit()

            for row in cursor.execute(f"select top 1 * from [Burgers] order by [ID_Burgers] desc"):
                idBurgers = row.ID_Burgers

            endIdBurgers.append(idBurgers)
            idCurrentBurgers = idBurgers

            for ingrid in range(len(ingridients)):
                cursor.execute(f"insert into [Burgers_Ingridient] ([Burgers_ID], [Ingridient_ID]) values (?, ?)", (idCurrentBurgers, ingridients[ingrid]+1))
                cnxn.commit()
                
            idCheck = []

            for row in cursor.execute("select * from [Check]"):
                idCheck.append(row.ID_Check)

            for id in range(len(idCheck)):
                currentIdCheck = idCheck[id]

            Check.ChequeSumUpd(userId, currentIdCheck, endIdBurgers)
            
            print("Собрали блюдо:)")

        commit = input("'+', чтобы завершить.'-', чтобы продолжить.\n").lower()

        if commit == "+":
            print("Завершаем оформление заказа...\n")
            time.sleep(2)
            count = 1        
            OrderCompletion.CloseOrder(adminId, userId, currentIdCheck, endIdBurgers, count)
        elif commit == "-":
            try:
                toOrder = int(input("Выберите действие: \n"
                    "1 - Продолжить оформление заказа\n"
                    "2 - Сбросить заказ\n"))
            except ValueError:
                print("Введены неверные данные")
                Check.DropCheque(userId, currentIdCheck)
                time.sleep(2)
                Orders(userId)
            if toOrder > 0 and toOrder <= 2:
                match toOrder:
                    case '1':
                        print("Продолжаем заказ...\n")
                        time.sleep(2)
                        Orders(userId)
                    case '2':
                        print("Сбрасываем заказ...\n")
                        time.sleep(2)
                        Check.DropCheque(userId, currentIdCheck)
                    case _:
                        print("Сбрасываем заказ...\n")
                        time.sleep(2)
                        Check.DropCheque(userId, currentIdCheck)
            else:
                print("Неверное действие.")
                time.sleep(2)
                Check.DropCheque(userId, currentIdCheck)
                Orders(userId)
        else:
            print("Неверное действие.")
            Check.DropCheque(userId, currentIdCheck)
            time.sleep(2)
            Orders(userId)
    elif count == 0:
        CloseOrder.CloseOrder(adminId, userId, currentIdCheck, endIdBurgers, count)
    else:
        print("Введены неверные данные")
        time.sleep(2)
        Orders(userId)