import telebot
import fileManipulations
import database
from telebot import apihelper
#Ключ бота.
botKey = "5922041651:AAF59La-ZXwZvRwQu-wJATJNN450bEbIO4g"

#Иницивализация бота
Bot = telebot.TeleBot(botKey, parse_mode = "HTML", threaded=True, num_threads=3)

#Обработка команды старт
@Bot.message_handler(commands = ["start"])
def start(message):
    try:
        if database.checkUser(message.chat.id) == False:
            database.addUser(message.chat.id, message.from_user.username)
            Bot.send_message(message.chat.id,"Вижу вас впервые...\n\nБот который позволяет получать информацию о файле.\n<b>Отправляй файл документом!</b>")
        else:
            Bot.send_message(message.chat.id,"С возвращением!\n\nБот который позволяет получать информацию о файле.\n<b>Отправляй файл документом!</b>")
    except Exception as error:
        print(f"Ошибка в процессе работы команды start!\n{str(error)}")
        Bot.send_message(message.chat.id, f"Произошла неизвестная ошибка.")
        
#Вывод информации о пользователе
@Bot.message_handler(commands = ["me"])
def info(message):
    try:
        userNum = database.getNum(message.chat.id)
        Bot.send_message(message.chat.id, f"Ваш ID: <code>{message.chat.id}</code>\n\nВы сделали <code>{userNum}</code> запросов.")
    except Exception as error:
        print(f"Ошибка в процессе вывода информации о пользователе!\n{str(error)}")
        Bot.send_message(message.chat.id, f"Произошла неизвестная ошибка.")
        
#Получение всех документов и их обработка
@Bot.message_handler(content_types=['document'])
def procssingDocument(message):
    try:
        #Скачивание файла с сервера телеграмм
        fileAdditionPath = "Files/"
        file_info = Bot.get_file(message.document.file_id)
        downloaded_file = Bot.download_file(file_info.file_path)
        file_name = message.document.file_name
        filePath = fileAdditionPath+file_name
        with open(filePath, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        #Получение данных (модуль fileManipulations)    
        fileHashes = fileManipulations.getHashes(filePath)
        fileMeta = fileManipulations.getFileMetadata(filePath)
        md5 = fileHashes["md5"]
        sha32 = fileHashes["sha32"]
    #бтв питон не любит форматстринги с такими обращениями(((
        fileSize = fileMeta["file_size"]
        lastModified = fileMeta["last_modified"]
        creationTime = fileMeta["creation_time"]
        #Логирование
        print(f"New task {message.chat.id} -> {filePath} ->\n\tMD5:{md5}\n\tSHA32:{sha32}\n\tРазмер:{fileSize}\n\tСоздан:{creationTime}\n\tПоследнее изменение:{lastModified}")
        #Отправка данных пользователю
        Bot.reply_to(message, f"""Информация:
    MD5-> <code>{md5}</code>
    SHA32-> <code>{sha32}</code>               
    Размер: <code>{fileSize}</code>

    <tg-spoiler>Используется для примера. Телеграмм чистит метаданные.</tg-spoiler>
    Создан: <code>{creationTime}</code>
    Последнее изменение: <code>{lastModified}</code>
    """)
        database.updateNum(message.chat.id)
    except Exception as error:
        print(f"Ошибка в процессе обрабтки файла!\n{str(error)}")
        Bot.send_message(message.chat.id, f"Произошла неизвестная ошибка.")

#Инфинити
Bot.infinity_polling(skip_pending=True)