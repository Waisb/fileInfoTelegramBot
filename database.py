import sqlite3
import threading

#Путь до базы данных
dbPath = "database.db"


#Коннект к базе и создание рабочего курсора
connection = sqlite3.connect(dbPath,check_same_thread=False)
cursor = connection.cursor()

#Создание ячеек и таблицы в случае если ее нет (бд не создавалась или пуста)
cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
userid INTEGER PRIMARY_KEY,
username TEXT NOT NULL,
num INTEGER)
''')

#Лок потоков для работы в многопоточности 
lock = threading.Lock()

#Добавление пользователя в базу
def addUser(userid, username):
    cursor.execute("INSERT INTO Users (userid,username,num) VALUES (?,?,?)",(userid, f"@{username}",0))
    connection.commit()
    
#Проверка есть ли пользователь в базе
def checkUser(userid):
    with lock:
        cursor.execute("SELECT * FROM Users WHERE userid=(?)", (userid,))
        result = cursor.fetchone()
        if result is None:
            return False
        if len(result) > 0:
            return True  
        
#Обновление количества запросов                   
def updateNum(userid):
    with lock:
        cursor.execute("SELECT num FROM Users WHERE userid=(?)", (userid,))
        result = cursor.fetchone()
        newNum =  result[0] + 1
        cursor.execute("UPDATE Users SET num = ? WHERE userid = ?",(newNum, userid)) 
        connection.commit()    
        
#Получение количетсва запросов
def getNum(userid):
    with lock:
        cursor.execute("SELECT num FROM Users WHERE userid=(?)", (userid,))
        result = cursor.fetchone()
        return result[0]
    
