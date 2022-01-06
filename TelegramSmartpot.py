from SmartPot.smartpot import SmartPot
from threading import Thread
from monitor import TimeBasedMonitor, HysteresisMonitor

import telepot
from telepot.loop import MessageLoop
import time

token="5001234212:AAEim1ICtmrC_SH0jm043CEv7X-RuIFuY4k"
chatid=-792038619


bot = telepot.Bot(token)

PotObject = SmartPot()
TemperaturObergrenze = 30

bot.getMe()
bot.getUpdates()

bot.sendMessage(chatid,"SmartPot_Bot wurde gestartet")
bot.sendMessage(chatid,"-----Befehle-----\n/Temperatur  # Gibt die aktuelle Temperatur wieder \n/Luftfeuchtigkeit  # Gibt die aktuelle Luftfeuchtigkeit wieder \n/Bodenfeuchtigkeit # Gibt die aktuelle Bodenfeuchtigkeit wieder \n/Lichtstaerke  # Gibt die aktuelle Lichtstaerke wieder \n/Info  # Gibt alle aktuellen Parameter wieder\n/Hilfe gibt diese Narchicht erneut wieder\n-----Monitore-----\n/LuftfeuchtigkeitMonitor XX YY # Erstellt einen Monitor XX ist eine Zahl fuer die Obergrenze und optional ist die Zahl fuer YY die die Untergrenze festlegt")

def handle(msg):
    message =msg['text']                    #Nur abgreifen des Textes
    if message == "/Hilfe":
        print(message)                          #Ausgabe des Textes
        bot.sendMessage(chatid,"------------Hilfe------------")
        bot.sendMessage(chatid,"-----Befehle-----\n/Temperatur  # Gibt die aktuelle Temperatur wieder \n/Luftfeuchtigkeit  # Gibt die aktuelle Luftfeuchtigkeit wieder \n/Bodenfeuchtigkeit # Gibt die aktuelle Bodenfeuchtigkeit wieder \n/Lichtstaerke  # Gibt die aktuelle Lichtstaerke wieder \n/Info  # Gibt alle aktuellen Parameter wieder\n/Hilfe gibt diese Narchicht erneut wieder\n-----Monitore-----\n/LuftfeuchtigkeitMonitor XX YY # Erstellt einen Monitor XX ist eine Zahl fuer die Obergrenze und optional ist die Zahl fuer YY die die Untergrenze festlegt")


    if message == "/Temperatur":
        print(message)                          #Ausgabe des Textes
        Temperatur = PotObject.read_temperature()
        bot.sendMessage(chatid,"Temperatur: %8.1f C" % (Temperatur))
    if message == "/Luftfeuchtigkeit":
        print(message)                          #Ausgabe des Textes
        Luftfeuchtigkeit = PotObject.read_humidity()
        bot.sendMessage(chatid,"Luftfeuchtigkeit: %8.1f %%" % (Luftfeuchtigkeit))
    if message == "/Bodenfeuchtigkeit":
        print(message)                          #Ausgabe des Textes
        Bodenfeuchtigkeit = PotObject.read_soil_moisture()
        bot.sendMessage(chatid,"Bodenfeuchtigkeit: %8.4f V" % (Bodenfeuchtigkeit))
        Bodenfeuchtigkeit = Bodenfeuchtigkeit * 24.4140625
        bot.sendMessage(chatid,"Bodenfeuchtigkeit: %8.4f %%" % (Bodenfeuchtigkeit))
    if message == "/Lichtstaerke":
        print(message)                          #Ausgabe des Textes
        Lichtstaerke = PotObject.read_light_intensity()
        bot.sendMessage(chatid,"Lichtstaerke: %8.4f V" % (Lichtstaerke))
        Lichtstaerke = Lichtstaerke * 24.4140625
        bot.sendMessage(chatid,"Lichtstaerke: %8.1f %%" % (Lichtstaerke))
    if message == "/Info":
        print(message)                          #Ausgabe des Textes
        Temperatur = PotObject.read_temperature()
        Luftfeuchtigkeit = PotObject.read_humidity()
        Bodenfeuchtigkeit = PotObject.read_soil_moisture()
        Lichtstaerke = PotObject.read_light_intensity()
        bot.sendMessage(chatid,"------------Info------------")
        bot.sendMessage(chatid,"Temperatur: %8.1f C" % (Temperatur))
        bot.sendMessage(chatid,"Luftfeuchtigkeit: %8.1f %%" % (Luftfeuchtigkeit))
        bot.sendMessage(chatid,"Bodenfeuchtigkeit: %8.4f irgendeineEinheit" % (Bodenfeuchtigkeit))
        bot.sendMessage(chatid,"Lichtstaerke: %8.4f irgendeineEinheit" % (Lichtstaerke))
        bot.sendMessage(chatid,"----------------------------")
   
    #Der Message String wird geteilt wenn ein Leerzeichen vorhanden ist und in die Liste der Einzeldaten geschrieben
    einzeldaten = message.split(" ")

    #Abfrage der Narchicht für den Luftfeuchtigkeitsmonitor mit überpruefung der Einzelnen Elemente der Liste mithilfe der HysteresisMonitorfunktion wird der Monitor erstellt
    if einzeldaten[0] == "/LuftfeuchtigkeitMonitor":
        if len(einzeldaten) == 1:
            bot.sendMessage(chatid,"Zu wenig Argumente")
        if len(einzeldaten) == 2:
            Obergrenze = einzeldaten[1]
            print("Starting Monitors...")
            humidity_mon = HysteresisMonitor("Humidity", PotObject.read_humidity, int(einzeldaten[1]), callback, callback_lw_thres=callback3)
            humidity_mon.start()
            bot.sendMessage(chatid,"LuftfeuchtigkeitsMonitor wurde gestartet mit der Obergrenze %s und ohne Untergrenze" % (einzeldaten[1]))
        if len(einzeldaten) == 3:
            Obergrenze = einzeldaten[1]
            Untergrenze = einzeldaten[2]
            print("Starting Monitors...")
            humidity_mon = HysteresisMonitor("Humidity", PotObject.read_humidity, int(einzeldaten[1]), callback, callback_lw_thres=callback3, lower_thres=int(einzeldaten[2]))
            humidity_mon.start()
            bot.sendMessage(chatid,"LuftfeuchtigkeitsMonitor wurde gestartet mit der Obergrenze %s und einer Untergrenze von %s" % (einzeldaten[1],einzeldaten[2]))
        if len(einzeldaten) >= 4:
            bot.sendMessage(chatid,"Zu viele Argumente")

MessageLoop(bot, handle).run_as_thread()

def callback(timestamp, value, threshold, name):
    print("Value "+ name + "=" +str(value)+ "passed threshold of " + str(threshold) + " at " + str(timestamp) +".")
    PotObject.output_on(SmartPot.X4)
    bot.sendMessage(chatid,"Ey viel zu Feucht im Raum hier Bruder")

def callback3(timestamp, value, threshold, name):
    PotObject.output_off(SmartPot.X4)
    bot.sendMessage(chatid,"Danke dir Raumfeuchtigkeit wieder im Gruenen Bereich")







while 1:
    time.sleep(10)


