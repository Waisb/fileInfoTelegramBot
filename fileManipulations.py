import hashlib
import os
import datetime

#Получение хешей файла (md5, sha32)
def getHashes(filePath):
    MD5HashHashLib = hashlib.md5()
    #Проход по чанкам и обновление данных (md5)
    with open(filePath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            MD5HashHashLib.update(chunk)
    fileMD5Hash = MD5HashHashLib.hexdigest()
    #Проход по чанкам и обновление данных (sha32)
    with open(filePath, "rb") as file:
        SHA32HashHash = hashlib.sha256()
        while chunk := file.read(4096):
            SHA32HashHash.update(chunk)
    fileSha32Hash = SHA32HashHash.hexdigest()
    #Возврат значений
    return {
        "md5" : fileMD5Hash,
        "sha32" : fileSha32Hash}

#Получение метадаты файла. 
def getFileMetadata(filePath):
    #Получение метаданных средствами os
    fileStat = os.stat(filePath)
    
    #Привод в нормальный вид даты последнего изменения
    last_modified = datetime.datetime.fromtimestamp(fileStat.st_mtime)
    formatted_last_modified = last_modified.strftime('%Y-%m-%d %H:%M:%S')
    #Привод в нормальный вид даты создания   
    creation_time = datetime.datetime.fromtimestamp(fileStat.st_ctime)
    formatted_creation_time = creation_time.strftime('%Y-%m-%d %H:%M:%S')
    
    #Привод в нормальный вид размера
    size = fileStat.st_size
    power = 2**10
    n = 0
    #Список размеров основываясь на проходах
    power_labels = {0 : '', 1: 'Кило', 2: 'Мега', 3: 'Гига', 4: 'Тера'} #Не дай боже терабайты и гигабайты
    while size > power:
        size /= power
        n += 1
    #Для красоты. Приписывает тип размера на основе итераций    
    sizeLabel = power_labels[n]+'Байт'
    #Возвращение значений.
    return {
        "file_size": f"{size} {sizeLabel}",
        "last_modified": formatted_last_modified,
        "creation_time": formatted_creation_time
    }