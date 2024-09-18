from te4stdapp import stdApp, DiscordTracker
from te4lib import errMsg
import json


def main():
    """
    Приложение для установки произвольного игрового статуса в Discord
    Для использование укажите ID приложения и свои данные, если необходимо
    """
    tracker: DiscordTracker = None
    prevId: str = None

    # Сброс состояния кнопки на значение по умолчанию
    def onStart(app: stdApp):
        app["btn1"] = "Start"


    # Обработка нажатия кнопки
    def enableTracker(app: stdApp):
        try:
            global tracker, prevId
            needStart = False

            if(tracker == None):
                # Запуск трекера, где ID = ID приложения
                prevId = id = app["id"]
                if (id == ""):
                    app.visualError("Укажите id")
                    return
                
                app["btn1"] = "Update"
                tracker = DiscordTracker(id)
                needStart = True
            else:
                # Перезапуск трекера при изменении id
                id = app["id"]
                if(id != prevId):
                    prevId = id
                    tracker.destroy()
                    tracker = DiscordTracker(id)
                    needStart = True

            # Обновление информации в трекере
            tracker["logo_url"]  = app["logo_url"]
            tracker["logo_name"] = app["logo_name"]
            tracker["detals"]    = app["detals"]
            tracker["state"]     = app["state"]

            # Разбор кода кнопок
            buttons = app["buttons"]
            if(buttons != None and buttons != ""):
                tracker["buttons"] = json.loads(buttons)

            if(needStart):
                tracker.startTrack()
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
        ).buttom(enableTracker, "Start", var="btn1"
        ).onStart(onStart
        ).ico().start()


if __name__ == "__main__":
    main()