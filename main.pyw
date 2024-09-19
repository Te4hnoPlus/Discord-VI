from te4stdapp import stdApp, DiscordTracker
from te4lib import errMsg
import json


__tracker__: DiscordTracker = None
__prevId__: str = None
def main():
    """
    Приложение для установки произвольного игрового статуса в Discord
    Для использование укажите ID приложения и свои данные, если необходимо
    """
    # Сброс состояния на значение по умолчанию
    def onStart(app: stdApp):
        app["btn1"] = "Start"
        if(app["enable-defaults"] == True):
            enableTracker(app)


    # Обработка нажатия кнопки
    def enableTracker(app: stdApp):
        global __tracker__, __prevId__
        needStart = False
        try:
            if(__tracker__ == None):
                # Запуск трекера, где ID = ID приложения
                __prevId__ = id = app["id"]
                if (id == ""):
                    app.visualError("Укажите id")
                    return
                
                timeShift = app["time-shift"]
                if(timeShift != None):
                    timeShift = int(timeShift)
                
                app["btn1"] = "Update"
                __tracker__ = DiscordTracker(id, start=timeShift)
                needStart = True
            else:
                # Перезапуск трекера при изменении id
                id = app["id"]
                if(id != __prevId__):
                    __prevId__ = id
                    __tracker__.destroy()
                    timeShift = app["time-shift"]
                    if(timeShift != None):
                        timeShift = int(timeShift)
                    __tracker__ = DiscordTracker(id, timeShift)
                    needStart = True

            # Обновление информации в трекере
            __tracker__["logo_url"]  = app["logo_url"]
            __tracker__["logo_name"] = app["logo_name"]
            __tracker__["detals"]    = app["detals"]
            __tracker__["state"]     = app["state"]

            # Разбор кода кнопок
            buttons = app["buttons"]
            if(buttons != None and buttons != ""):
                __tracker__["buttons"] = json.loads(buttons)

            if(needStart):
                __tracker__.startTrack()
                app.visualInfo("Отображение активировано")
            else:
                app.visualInfo("Информация обновлена")
        except:
            app.visualError(errMsg(), "Что-то пошло не так ...")


    # GUI и запуск приложения
    stdApp(name="Discord GAME", config="dsvi.json", width=45
        ).text("APP ID"
        ).input("id"
        ).text("Ссылка на иконку"
        ).input("logo_url", height=2
        ).text("Название иконки"
        ).input("logo_name", "Te4 STD App"
        ).text("Состояние"
        ).input("state", "Te4 STD App"
        ).text("Описание"
        ).input("detals", "Waiting ...",
        ).text("Код кнопок"
        ).input("buttons", height=6
        ).text("Сдвиг").input(var="time-shift").nw(
        ).buttom(enableTracker, "Start", var="btn1"
        ).onStart(onStart
        ).ico().start()


if __name__ == "__main__":
    main()