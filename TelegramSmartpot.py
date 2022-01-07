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
bot.sendMessage(chatid,"-----Befehle-----\n/Temperatur  # Gibt die aktuelle Temperatur wieder \n/Luftfeuchtigkeit  # Gibt die aktuelle Luftfeuchtigkeit wieder \n/Bodenfeuchtigkeit # Gibt die aktuelle Bodenfeuchtigkeit wieder \n/Lichtstaerke  # Gibt die aktuelle Lichtstaerke wieder \n/Info  # Gibt alle aktuellen Parameter wieder\n/Hilfe gibt diese Narchicht erneut wieder\n-----Monitore-----\n Beim erstellen der Monitore gibt das XX die Zahl fuer die Obergrenze und YY die Zahl fuer die Untergrenze an\n/LuftfeuchtigkeitMonitor XX YY \n# Angabe in % \n/TemperaturMonitor XX YY \n# Angabe in Grad C\n/BodenfeuchtigkeitMonitor XX YY\n# Angabe in % von 0-50%\n/LichstaerkeMonitor XX YY\n# Angabe in % von 0-50%")

def handle(msg):
    message =msg['text']                    #Nur abgreifen des Textes
    if message == "/Hilfe":
        print(message)                          #Ausgabe des Textes
        bot.sendMessage(chatid,"-----Befehle-----\n/Temperatur  # Gibt die aktuelle Temperatur wieder \n/Luftfeuchtigkeit  # Gibt die aktuelle Luftfeuchtigkeit wieder \n/Bodenfeuchtigkeit # Gibt die aktuelle Bodenfeuchtigkeit wieder \n/Lichtstaerke  # Gibt die aktuelle Lichtstaerke wieder \n/Info  # Gibt alle aktuellen Parameter wieder\n/Hilfe gibt diese Narchicht erneut wieder\n-----Monitore-----\n Beim erstellen der Monitore gibt das XX die Zahl fuer die Obergrenze und YY die Zahl fuer die Untergrenze an\n/LuftfeuchtigkeitMonitor XX YY #Angabe in %% \n/TemperaturMonitor XX YY # Angabe in Grad C\n/BodenfeuchtigkeitMonitor XX YY\n# Angabe in % von 0-50%")


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

    #Abfrage der Narchicht fuer den Luftfeuchtigkeitsmonitor mit ueberpruefung der Einzelnen Elemente der Liste mithilfe der HysteresisMonitorfunktion wird der Monitor erstellt
    if einzeldaten[0] == "/LuftfeuchtigkeitMonitor":
        if len(einzeldaten) == 1:
            bot.sendMessage(chatid,"Zu wenig Argumente")
        if len(einzeldaten) == 2:
            Obergrenze = einzeldaten[1]
            print("Starting Luftfeuchtigkeits Monitors...")
            humidity_mon = HysteresisMonitor("Humidity", PotObject.read_humidity, int(einzeldaten[1]), callbackhumi, callback_lw_thres=callbackhumi2)
            humidity_mon.start()
            bot.sendMessage(chatid,"LuftfeuchtigkeitsMonitor wurde gestartet mit der Obergrenze %s und ohne Untergrenze" % (einzeldaten[1]))
        if len(einzeldaten) == 3:
            Obergrenze = einzeldaten[1]
            Untergrenze = einzeldaten[2]
            print("Starting Luftfeuchtigkeits Monitors...")
            humidity_mon = HysteresisMonitor("Humidity", PotObject.read_humidity, int(einzeldaten[1]), callbackhumi, callback_lw_thres=callbackhumi2, lower_thres=int(einzeldaten[2]))
            humidity_mon.start()
            bot.sendMessage(chatid,"LuftfeuchtigkeitsMonitor wurde gestartet mit der Obergrenze %s und einer Untergrenze von %s" % (einzeldaten[1],einzeldaten[2]))
        if len(einzeldaten) >= 4:
            bot.sendMessage(chatid,"Zu viele Argumente")

    #Abfrage der Narchicht fuer den Temperaturmonitor mit ueberpruefung der Einzelnen Elemente der Liste mithilfe der HysteresisMonitorfunktion wird der Monitor erstellt
    if einzeldaten[0] == "/TemperaturMonitor":
        if len(einzeldaten) == 1:
            bot.sendMessage(chatid,"Zu wenig Argumente")
        if len(einzeldaten) == 2:
            Obergrenze = einzeldaten[1]
            print("Starting Temperatur Monitors...")
            temperatur_mon = HysteresisMonitor("Temperatur", PotObject.read_temperature, int(einzeldaten[1]), callbacktemp, callback_lw_thres=callbacktemp2)
            temperatur_mon.start()
            bot.sendMessage(chatid,"TemperaturMonitor wurde gestartet mit der Obergrenze %s und ohne Untergrenze" % (einzeldaten[1]))
        if len(einzeldaten) == 3:
            Obergrenze = einzeldaten[1]
            Untergrenze = einzeldaten[2]
            print("Starting Temperatur Monitors...")
            temperatur_mon = HysteresisMonitor("Temperatur", PotObject.read_temperature, int(einzeldaten[1]), callbacktemp, callback_lw_thres=callbacktemp2, lower_thres=int(einzeldaten[2]))
            temperatur_mon.start()
            bot.sendMessage(chatid,"TemperaturMonitor wurde gestartet mit der Obergrenze %s und einer Untergrenze von %s" % (einzeldaten[1],einzeldaten[2]))
        if len(einzeldaten) >= 4:
            bot.sendMessage(chatid,"Zu viele Argumente")

    #Abfrage der Narchicht fuer den BodenfeuchtigkeitsMonitor mit ueberpruefung der Einzelnen Elemente der Liste mithilfe der HysteresisMonitorfunktion wird der Monitor erstellt
    if einzeldaten[0] == "/BodenfeuchtigkeitMonitor":
        if len(einzeldaten) == 1:
            bot.sendMessage(chatid,"Zu wenig Argumente")
        if len(einzeldaten) == 2:
            Obergrenze = einzeldaten[1]
            print("Starting Bodenfeuchtigkeit Monitors...")
            boden_mon = HysteresisMonitor("Bodenfeuchtigkeit", PotObject.read_soil_moisture, int(einzeldaten[1]), callbackboden, callback_lw_thres=callbackboden2)
            boden_mon.start()
            bot.sendMessage(chatid,"BodenfeuchtigkeitMonitor wurde gestartet mit der Obergrenze %s und ohne Untergrenze" % (einzeldaten[1]))
        if len(einzeldaten) == 3:
            Obergrenze = einzeldaten[1]
            Untergrenze = einzeldaten[2]
            print("Starting Bodenfeuchtigkeit Monitors...")
            boden_mon = HysteresisMonitor("Bodenfeuchtigkeit", PotObject.read_soil_moisture, int(einzeldaten[1]), callbackboden, callback_lw_thres=callbackboden2, lower_thres=int(einzeldaten[2]))
            boden_mon.start()
            bot.sendMessage(chatid,"BodenfeuchtigkeitMonitor wurde gestartet mit der Obergrenze %s und einer Untergrenze von %s" % (einzeldaten[1],einzeldaten[2]))
        if len(einzeldaten) >= 4:
            bot.sendMessage(chatid,"Zu viele Argumente")
    
    
    #Abfrage der Narchicht fuer den LichstaerkeMonitor mit ueberpruefung der Einzelnen Elemente der Liste mithilfe der HysteresisMonitorfunktion wird der Monitor erstellt
    if einzeldaten[0] == "/LichstaerkeMonitor":
        if len(einzeldaten) == 1:
            bot.sendMessage(chatid,"Zu wenig Argumente")
        if len(einzeldaten) == 2:
            Obergrenze = einzeldaten[1]
            print("Starting Lichstaerke Monitors...")
            licht_mon = HysteresisMonitor("Lichstaerke", PotObject.read_light_intensity, int(einzeldaten[1]), callbacklicht, callback_lw_thres=callbacklicht2)
            licht_mon.start()
            bot.sendMessage(chatid,"LichstaerkeMonitor wurde gestartet mit der Obergrenze %s und ohne Untergrenze" % (einzeldaten[1]))
        if len(einzeldaten) == 3:
            Obergrenze = einzeldaten[1]
            Untergrenze = einzeldaten[2]
            print("Starting Bodenfeuchtigkeit Monitors...")
            licht_mon = HysteresisMonitor("Lichstaerke", PotObject.read_light_intensity, int(einzeldaten[1]), callbacklicht, callback_lw_thres=callbacklicht2, lower_thres=int(einzeldaten[2]))
            licht_mon.start()
            bot.sendMessage(chatid,"LichstaerkeMonitor wurde gestartet mit der Obergrenze %s und einer Untergrenze von %s" % (einzeldaten[1],einzeldaten[2]))
        if len(einzeldaten) >= 4:
            bot.sendMessage(chatid,"Zu viele Argumente")




MessageLoop(bot, handle).run_as_thread()

def callbackhumi(timestamp, value, threshold, name):
    print("Value "+ name + "=" +str(value)+ "passed threshold of " + str(threshold) + " at " + str(timestamp) +".")
    PotObject.output_on(SmartPot.X4)
    bot.sendMessage(chatid,"Ey viel zu Feucht im Raum hier Bruder %3.0f%%" % (value))

def callbackhumi2(timestamp, value, threshold, name):
    PotObject.output_off(SmartPot.X4)
    bot.sendMessage(chatid,"Danke dir Raumfeuchtigkeit wieder im Gruenen Bereich %3.0f%%" % (value))

def callbacktemp(timestamp, value, threshold, name):
    print("Value "+ name + "=" +str(value)+ "passed threshold of " + str(threshold) + " at " + str(timestamp) +".")
    PotObject.output_on(SmartPot.X4)
    bot.sendMessage(chatid,"Ey viel zu Heiss im Raum hier Bruder %3.0f Grad C" % (value))

def callbacktemp2(timestamp, value, threshold, name):
    PotObject.output_off(SmartPot.X4)
    bot.sendMessage(chatid,"Danke dir alles wieder cool %3.0f Grad C" % (value))

def callbackboden(timestamp, value, threshold, name):
    print("Value "+ name + "=" +str(value)+ "passed threshold of " + str(threshold) + " at " + str(timestamp) +".")
    PotObject.output_on(SmartPot.X4)
    bot.sendMessage(chatid,"Wasser reicht mir danke, ist bei %3.2f%%" % (value))

def callbackboden2(timestamp, value, threshold, name):
    PotObject.output_off(SmartPot.X4)
    bot.sendMessage(chatid,"Ey brauche Wasser bin auf %3.2f%%" % (value))

def callbacklicht(timestamp, value, threshold, name):
    print("Value "+ name + "=" +str(value)+ "passed threshold of " + str(threshold) + " at " + str(timestamp) +".")
    PotObject.output_on(SmartPot.X4)
    bot.sendMessage(chatid,"Licht ist absolut ausreichend, habe %3.2f%%" % (value))

def callbacklicht2(timestamp, value, threshold, name):
    PotObject.output_off(SmartPot.X4)
    bot.sendMessage(chatid,"Ist viel zu dunkel hier, mach Licht an bin bei %3.2f%%" % (value))










while 1:
    time.sleep(10)


