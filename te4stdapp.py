import json, os, shutil, time
from tkinter import ttk, Tk, filedialog, Toplevel, Wm, PhotoImage, BooleanVar
import tkinter.messagebox as msgbox
from te4lib import *
from pypresence import Presence 
from threading import Thread
from typing import Self


"""
Библиотека для быстрой разработки и прототипирования простых (стандартных) приложений с использованием Tkinter
Все элементы по умолчанию размещаются сверху вниз и выравниваются по центру
Встроенные поддерживаемые компоненты:
- Текст
- Кнопка
- Поле ввода
- Переключатель
Дополнительные частоиспользуемые инструменты для разработки:
- Визуальное получение файлов и папок
- Отображение диалоговых окон и сообщений
- Автоматическое управление данными переменных и конфигурацией
- Дочерние окна
- Прослушивание событий

Использование

def function(app:stdApp):
    var = app["var"]
    app["var2"] = var

stdApp("Имя").buttom("Кнопка", function).start()

tracker = DiscordTracker(APP_ID).startTrack()
time.sleep(30)

tracker["buttons"] = [{
    "label": "Example", 
    "url": "https://eample.ru"
}]
"""


class baseApp:
    """
    Базовая единица приложения
    """
    def __init__(self, root: Wm, name="Std Te4hno Python APP", width=30) -> None:
        self.root = root
        self.config = None
        self.defWidth = width
        self.title = name
        self.root.title(name)
        self.frm = ttk.Frame(self.root, padding=20)
        self.frm.grid()
        self.cursor = 0
        self.__components__ = {}
        self.__components__["__onclose__"] = []
        self.__components__["__onstart__"] = []

        # Выполнение функций перед закрытием окна
        def onClose():
            cansel = None
            for func in self.__components__["__onclose__"]: func(self)
            if not (cansel == True): self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", onClose)

        self.addVarComp(var="title", funcGet=lambda:self.title, funcSet=self.setTitle)
        def setSize(val):self.root.size = val
        self.addVarComp(var="size", funcGet=lambda:self.root.size, funcSet=setSize)


    def setTitle(self, title) -> Self:
        """
        Редактирование заголовка окна
        """
        self.title = title
        self.root.title(title)
        return self
            

    def text(self, text="Text", var:str=None, pos=None, padding=10, width=None) -> Self:
        """
        Добавить текстовый компонент в конец окна
        """
        label = ttk.Label(self.frm, text=text, padding=padding, width=width)
        self.__onAddLabel__(label=label, var=var, pos=pos)
        return self
    

    def checkBtn(self, var, text=None, func=lambda app:None, pos=None, padding=10, width=None) -> Self:
        """
        Добавить переключатель в конец окна
        """
        if(text == None): text = var
        bVar = BooleanVar()
        def command(**kwargs):
           self.config[var] = bVar.get()
           func(self)

        label = ttk.Checkbutton(self.frm, text=text, padding=padding, command=command, variable=bVar, width=width)
        self.__onAddLabel__(label=label, pos=pos)

        self.addVarComp(var=var, 
            funcSet=lambda v:bVar.set(v), 
            funcGet=lambda  :bVar.get()
        )
        return self
    

    def onStart(self, task=lambda:None) -> Self:
        """
        Добавление функций, которые будут вызваны перед открытием окна
        """
        self.__components__["__onstart__"].append(task)
        return self


    def onClose(self, task=lambda:None) -> Self:
        """
        Добавление функций, которые будут вызваны непосредственно перед закрытием окна
        """
        self.__components__["__onclose__"].append(task)
        return self


    def __onAddLabel__(self, label, var=None, pos=None):
        """
        Добавить компонент в окно в указанную позицию, по умолчанию в конец
        Позиция задается в виде словаря с ключами "c", "r", где "c" - колонка, "r" - строка
        При изменении указанной переменной, значение на экране будет автоматически обновлено
        """
        column = 0
        row = self.cursor
        next = True
        if pos != None:
            column = pos["c"] if "c" in pos else 0
            row = pos["r"] if "r" in pos else self.cursor
            next = row == self.cursor
        label.grid(column=column, row=row)
        if next: self.cursor+=1
        if var == None: return
        self.addVarComp(var=var, 
            funcSet=lambda v:label.config(text=v), 
            funcGet=lambda  :label.cget("text")
        )
    

    def addVarComp(self, var:str, funcGet, funcSet):
        """
        Добавить прокси доступ к указанной переменной
        """
        self.__components__[var]=(funcGet, funcSet)


    def buttom(self, func=lambda app:None, name="Buttom", var=None, style=None, pos=None, padding=10, width=None) -> Self:
        """
        Добавить кнопку в конец окна
        """
        if(width == None):
            width = self.defWidth
        label = ttk.Button(self.frm, text=name, command=lambda:func(self), padding=padding, style=style, width=width)
        self.__onAddLabel__(label=label, var=var, pos=pos)
        return self
    

    def nw(self) -> Self:
        """
        Добавить отступ (пустой текстовый компонент) в конец окна
        """
        return self.text("")
    



    def input(self, var:str, default=None, focusTask=lambda app:None, unfocusTask=lambda app:None, width=None, height=1, pos=None) -> Self:
        """
        Добавить поле ввода в конец окна
        """
        label, funcSet, funcGet = None, None, None
        if(width == None):
            width = self.defWidth
        if height > 1:
            from tkinter.scrolledtext import ScrolledText
            label = ScrolledText(self.frm, width=width, height=height, font = ("Times New Roman",11))
            self.__onAddLabel__(label=label, var=None, pos=pos)

            def funcSet(val):
                label.delete("1.0", 'end-1c')
                if val == None:return
                label.insert("1.0", val)
                
            funcGet = lambda: label.get("1.0", 'end-1c')
        else:
            label = ttk.Entry(self.frm, width=width, font = ("Times New Roman",11))

            def funcSet(val):
                label.delete(0, 'end')
                if val == None: return
                label.insert(0, val)

            funcGet = label.get

        self.__onAddLabel__(label, pos=pos)

        if type(default) == tuple:
            self.onStart(lambda a:funcSet(self[(default[0], default[0])]))
        else: 
            funcSet(default)

        def unfocus(event):
            self.config[var] = funcGet()
            unfocusTask(self)

        def focus(event):
            focusTask(self)

        label.bind("<FocusOut>", unfocus)
        label.bind("<FocusIn>", focus)

        self.addVarComp(var=var, funcGet=funcGet, funcSet=funcSet)
        return self


    def start(self) -> Self:
        """
        Запустить окно
        """
        for task in self.__components__["__onstart__"]: task(self)
        del self.__components__["__onstart__"]
        self.root.mainloop()
        return self
    

    def config(self, config=None) -> Self:
        """
        Получить или изменить файл конфигурации
        """
        if(config==None):return self.config
        self.config = config
        return self


    def __getitem__(self, name):
        val = None
        if type(name) == tuple:
            val = name[1]
            name = name[0]
        if name in self.config:
            return self.config[name]
        if name in self.__components__:
            result = self.__components__[name][0]()
            if result != None: return result
        return val
    

    def __setitem__(self, name, val):
        if name in self.__components__:
            self.__components__[name][1](val)
        self.config[name] = val


    def __contains__(self, name):
        return name in self.config or name in self.__components__


    def __delitem__(self, name):
        del self.__components__[name]


    def visualGetDir(self, name:str=None):
        """
        Заблокировать текущий поток и открыть окно выбора директории
        После закрытия окна разблокирует текущий поток и вернет путь к выбранной директории
        """
        return filedialog.askdirectory(
            title=self.title if name == None else f"{self.title}: {name}"
        )


    def visualGetFile(self, name:str=None, default=None, filter=None, multi=False):
        """
        Заблокировать текущий поток и открыть окно выбора файлов
        После закрытия окна разблокирует текущий поток и вернет путь к выбранному файлу
        """
        openFunc = None
        if(multi):
            openFunc = filedialog.askopenfilenames
        else:
            openFunc = filedialog.askopenfilename

        return openFunc(
            title=self.title if name == None else f"{self.title}: {name}",
            defaultextension=filter, initialfile=default
        )


    def visualInfo(self, text:str, title:str=None):
        """
        Отображение информационного окна с указанным сообщением
        """
        if title == None: title = self.title
        msg = msgbox.showinfo(title=title, message=text, parent=self.root)


    def visualError(self, text:str, title:str=None):
        """
        Отображение окна с указанной ошибкой
        """
        if title == None: title = self.title
        msg = msgbox.showerror(title=title, message=text, parent=self.root)


    def visualWarning(self, text:str, title:str=None):
        """
        Отображение окна с предупреждением
        """
        if title == None: title = self.title
        msg = msgbox.showwarning(title=title, message=text, parent=self.root)


    def visualAsk(self, text:str, title:str=None):
        """
        Заблокировать текущий поток и отобразить окно с подтверждением действия
        После закрытия окна разблокирует текущий поток и вернет ответ пользователя
        """
        if title == None: title = self.title
        return msgbox.askyesno(title=title, message=text, parent=self.root)


    def __call__(self, *args, **kwds):
        return self.start()
    

def readJson(fileName:str, default={}):
    """
    Чтение JSON-файла в словарь
    """
    data = default
    if os.path.exists(fileName):
        with open(fileName, "r") as file: 
            data = json.load(file)
    return data
    

def clearDir(folder):
    """
    Очистка папки
    """
    if(not os.path.exists(folder)):return
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path): os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


class stdApp(baseApp): 
    """
    Главное окно библиотеки стандартных приложений
    """
    def __init__(self, name="Std Te4hno Python APP", config={}, width=30):
        super().__init__(Tk(), name, width=width)

        if type(config) == str:
            self.config = {}
            def scanCfg(app: stdApp):
                for k, v in readJson(config).items():
                    self[k] = v

            def onClose0(app: stdApp):
                with open(config, "w+") as file: 
                    json.dump(self.config, file, indent=1)

            self.onStart(scanCfg)
            self.onClose(onClose0)
        else:
            self.config = config


    def ico(self, path="icon.png") -> Self:
        """
        Установка иконки, по умолчанию из файла icon.png
        """
        try:
            if(path.endswith(".ico")):
                self.root.iconbitmap(bitmap=path)
            else:
                self.root.call("wm", "iconphoto", self.root._w, PhotoImage(file=path))
        except:
            print(f"Can't set icon [{path}]")
            logError()
        return self


class subWindow(baseApp):
    """
    Дочернее окно библиотеки стандартных приложений
    """
    def __init__(self, parent: stdApp, name="Window", size=None):
        super().__init__(Toplevel(), name, size)
        self.config = parent.config

        # Клонирование доступов к переменным из родительского окна
        def copyVars(app):
            for name in self.config:
                if name in self.__components__:
                    self.__components__[name][1](self.config[name])

        self.onStart(copyVars)


def repeatEvery(task, repeat=1):
    """
    Запуск повторяющейся задачи с заданным интервалом
    Если задача вернет False, то завершить повторное выполнение задачи
    """
    while True:
        result = task()
        if(result == False):return
        time.sleep(repeat)


class DiscordTracker:
    """
    Трекер статуса в Discord, отслеживает изменение значений и обновляет статус с минимальной задержкой
    и без лишних запросов к Discord
    ID приложения должен быть указан в конструкторе
    """
    def __init__(self, client_id):
        self.proc =  None
        self.start = int(time.time())
        self.RPC = Presence(client_id)
        self.RPC.connect()
        self.active = False
        self.timer = 0
        self.__data__ = {
            "logo_url"  : None,
            "logo_name" : None,
            "buttons"   : None,
            "detals"    : "Waiting ...",
            "state"     : "Te4 STD App"
        }


    def destroy(self):
        """
        Отключиться от серверов Discord и ожидать завершения фоновых задач
        """
        self.stopTrack()
        self.RPC.close()
        self.RPC = None


    def update(self):
        """
        Сообщить трекеру, что статус необходимо отправить немедленно
        """
        self.timer = 0


    def startTrack(self) -> Self:
        """
        Запуск фоновой задачи по автоматическому отслеживанию и обновлению статуса
        """
        if(self.proc != None or self.RPC == None):
            return
        self.active = True
        self.proc = Thread(target=repeatEvery, daemon=True, args=(lambda:self.__updateIfNeed__(), 1))
        self.proc.start()
        return self
    

    def stopTrack(self):
        """
        Остановить фоновую задачу по отслеживанию и обновлению статуса
        """
        self.active = False
        if(self.proc == None):
            return
        self.proc.join()
        self.proc = None


    def __updateIfNeed__(self):
        """
        Обновить статус, если давно не было обновления
        """
        self.timer -= 1
        if(self.timer < 0):
            self.timer = 30
            self.__update__()
        return self.active


    def __getitem__(self, item):
        return self.__data__[item]
    

    def __setitem__(self, item, value):
        prev = self.__data__[item]
        if(prev != value):
            self.__data__[item] = value
            self.timer = 0


    def __contains__(self, item):
        return item in self.__data__


    def __update__(self):
        """
        Отправить на сервера Discord новый статус
        """
        # Фильтрация пустых значений
        def getNonEmpty(key:str) -> str:
            result = self.__data__[key]
            if(result == None or result == ""):return None
            return result
        
        # Отправка нового статуса
        self.RPC.update(
            large_image = getNonEmpty("logo_url"), 
            large_text  = getNonEmpty("logo_name"),
            details     = getNonEmpty("state"),
            state       = getNonEmpty("detals"),
            start       = self.start,
            buttons     = self.__data__["buttons"]
        )