import pyodbc
from os import system, name
import os.path
import time
import toOrder
import random
import datetime
now = datetime.datetime.now()
cnxn = pyodbc.connect('Driver={SQL Server};Server=LAPTOP-KMTJ6QG7\MYNAME;Database=Burger;Trusted_Connection=yes;')
cursor = cnxn.cursor()

def ChequeSumUpd(userId, currentIdCheck, endIdBurgers):
    for row in cursor.execute(f"select * from [Check] inner join [User] on [User_ID] = [ID_User] where [ID_Check] = {currentIdCheck}"):
        count = row.Count_Burgers
        cost = row.Cost_Burgers
        sum = row.Sum_Order
    sum = 0
    sum += count * cost
    ingridientId = []
    for i in range(len(endIdBurgers)):
        for row in cursor.execute(f"select * from [Burgers_Ingridient] where [Burgers_ID] = {endIdBurgers[i]}"):
            ingridientId.append(row.Ingridient_ID)
    
    for id in range(len(ingridientId)):
        for row in cursor.execute(f"select * from [Ingridient] where [ID_Ingridient] = {ingridientId[id]}"):
            costIngridient = row.Cost_Ingridient
        sum += costIngridient

    cursor.execute(f"update [Check] set [Sum_Order] = {sum} where [ID_Check] = {currentIdCheck}")
    cnxn.commit()


def Cheque(userId, count):
    for row in cursor.execute("select * from [Burgers]"):
        cost = row.Cost_Burgers
    sum = count * cost
    currentTime = now.strftime("%d-%m-%Y %H:%M")
    random.seed()
    if random.randint(1, 10) > 5:
        ear = True
        random.seed()
        if random.randint(1, 10) > 5:
            detected = True
        else:
            detected = False
    else:
        ear = False
        detected = False
    
    
    cursor.execute("insert into [Check] ([User_ID], [Count_Burgers], [Cost_Burgers], [Sum_Order], [Time_Order], [Ear], [Noticed]) values (?, ?, ?, ?, ?, ?, ?)", 
                   (userId, count, cost, sum, currentTime, (1 if ear else 0), (1 if detected else 0)))
    cnxn.commit()

def DropCheque(userId, currentIdCheck):
    burgers = []
    for row in cursor.execute(f"select * from [Check_Burgers] where [Check_ID] = {currentIdCheck}"):
        burgers.append(row.Burgers_ID)
    for id in range(len(burgers)):
        cursor.execute(f"delete [Burgers] where [ID_Burgers] = {burgers[id]}")
        cnxn.commit()
    cursor.execute(f"delete [Check] where [ID_Check] = {currentIdCheck}")
    cnxn.commit()
    
    print("Возвращаемся в главное меню...")
    time.sleep(2)
    toOrder.toOrder(userId)