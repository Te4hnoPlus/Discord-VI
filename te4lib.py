import os, time, traceback, http.client

# Текущая рабочая директория
__mainPath__      = (__file__.replace("\\", "/")[0:__file__.rfind("/")+1])
# Текущая история ввода и вывода, предполагается что она не будет очень большой
__logField__ = ""
# Указатель на стандартную функцию печати
__basicPrinter__ = print
# Указатель на стандартную функцию ожидания ввода в консоль
__basicInputer__ = input
# Формат печати в консоли
__defFormat__ = " > {value}"
# Разрешена ли дозапись в лог файл
__canAdd__ = False
# Кодировки печати в файл, по умолчанию utf-8
__codecs__ = ["cp1252", "cp437", "utf-16be", "utf-16", "ascii", "utf-8"]


def setFormat(newFormat):
    """
    Задать новый формат печати в консоли
    """
    global __defFormat__
    __defFormat__ = newFormat


def p(o):
    """
    Сокращеннаый вызов функции печати в консоль
    """
    print(o)


def i(o):
    """
    Сокращеннай вызов функции ожидания ввода в консоль
    """
    return input(o)
    

def печать(o, __format__=__defFormat__):
    """
    'Русский' вариант функции печати в консоль
    """
    print(o, __format__)


def print(o, __format__=__defFormat__):
    """
    Переопределение стандартной функции печати в консоль
    для автоматической поддержки истории и логирования
    """
    global __logField__
    __basicPrinter__(__format__.format(value=o))
    toPrint = "{0}\n".format(o)
    __logField__ = __logField__ +toPrint
    return toPrint


def input(o):
    """
    Переопределение стандартной функции ожидания ввода в консоль
    для автоматической поддержки истории и логирования
    """
    global __logField__
    toPrint = "{0}\n".format(o)
    __logField__ = __logField__ +toPrint
    returnValue = __basicInputer__(toPrint)
    return returnValue


def regNums(numsMath=""):
    nums = []
    if numsMath == "":
        return nums
    mathes = numsMath.split("^")
    for m in mathes:
        if(m.startswith("!")):
            m = m[1:]
            if ":" in m:
                smath = m.split(":")
                for number in range(int(smath[0]), int(smath[1])+1):
                    if number in nums:
                        nums.remove(number)
            else:
                number = int(m)
                if number in nums:
                    nums.remove(number)
        else:
            if ":" in m:
                smath = m.split(":")
                nums += list(range(int(smath[0]), int(smath[1])+1))
            else:
                nums.append(int(m))
    return nums


def currentTime():
    """
    Возвращает текущее время в миллисекундах
    """
    return round(time.time() * 1000)


def testTime(func, logf=True, msg="Time spent: "):
    """
    Простая замерка времени выполнения функции
    """
    tTime1 = currentTime()
    result = func()
    if(logf):
        time = currentTime()-tTime1
        ms =  time%1000
        sec = (time%60000)//1000
        min = (time//60000000)
        if(min<0):
            p(msg+str(sec)+"sec, "+str(ms)+"ms")
        else:
            p(msg+str(min)+"min, "+str(sec)+"sec, "+str(ms)+"ms")
        return result
    else: return currentTime()-tTime1


def editPath(path):
    """
    Редактировать текущую рабочую директорию
    """
    global __mainPath__
    __mainPath__ = path.replace("\\", "/")


def logError():
    """
    Отображает сообщение об ошибке, предполагается что ошибка существует
    """
    format = "------------------------------------------------------------------------------------"
    ermsg = "| "+errMsg().replace("\n", "\n| ")
    print(format+"\n"+ermsg+"\n"+format)


def errMsg():
    """
    Возвращает сообщение об ошибке, предполагается что ошибка существует
    """
    return traceback.format_exc()
    

def saveLog(fileName="log.txt"):
    """
    Сохраняет историю ввода и вывода лог в файл
    """
    global __canAdd__, __logField__
    if len(__logField__)==0:
        return
    if __canAdd__:
        with open(fileName, "a") as file:
            file.write(__logField__)
            file.close()
    else:
        createFile(__mainPath__+fileName, __logField__)
    __logField__ = ""


def getSelfInetAdress(__format__=" * self ip: {value}", port=80):
    """
    Возвращает текущий IP-адрес этого устройства
    """
    suffix = ""
    prefix = None
    if port == 80:
        prefix = "http://"
    elif port == 443:
        prefix = "https://"
    else:
        suffix = ":"+str(port)
    try:
        conn = http.client.HTTPConnection("ifconfig.me")
        conn.request("GET", "/ip")
        data = conn.getresponse().read()
        return print(prefix+str(data)[2:-1]+suffix, __format__=__format__).replace("\n", "")
    except:
        return print(prefix+"localhost"+suffix, __format__=__format__).replace("\n", "")


def createForFileIfNeed(path):
    """
    Создает все необходимые дочерние директории для указанного файла, если они не существуют
    """
    pt = path.split("/")
    del pt[len(pt)-1]
    pt2 = __mainPath__+("/".join(pt))
    if not os.path.exists(pt2+"/"):
        pass
        os.makedirs(pt2)


def createFile(path, value="", encoding=5):
    """
    Создает файл и записывает туда указанную строку или перезывает его содержимое указанной строкой
    """
    createForFileIfNeed(path)
    with open(__mainPath__+path, "w+", encoding=__codecs__[encoding]) as file:
        file.write(value)
        file.close()


def getDeepFiles(pth, prefix = "", ignore=[]):
    """
    Возвращает полный список файлов в указанной директории (включая поддиректории)
    """
    fls = os.listdir(pth)
    fls2 = []
    for f in fls:
        if f in ignore:
            continue
        if "." in (pth+f):
            fls2.append(prefix+f)
        else:
            newdir = (pth+"/"+f).replace("//", "/")
            if prefix+f+"/" in ignore:
                continue
            fls3 = getDeepFiles(newdir, prefix+f+"/")
            for ff in fls3:
                fls2.append(ff)
    return fls2