#!/usr/bin/python3
from SmartPot.smartpot import SmartPot
from threading import Thread
from monitor import TimeBasedMonitor, HysteresisMonitor
import configparser
import telepot
from telepot.loop import MessageLoop
import time

#Config datei einlesen
config = configparser.ConfigParser()
config.read("smartpot.ini")

#Bot token und Chatid aus Config Datei holen
token=config["Telegram"]["chattoken"]
chatid=int(config["Telegram"]["chatid"])

bot = telepot.Bot(token)

PotObject = SmartPot()

bot.getMe()
bot.getUpdates()

#Bot Start Message und /Help wiedergabe
bot.sendMessage(chatid,"SmartPot_Bot wurde gestartet")
bot.sendMessage(chatid,"-----Befehle-----\n/Temperatur  # Gibt die aktuelle Temperatur wieder \n/Luftfeuchtigkeit  # Gibt die aktuelle Luftfeuchtigkeit wieder \n/Bodenfeuchtigkeit # Gibt die aktuelle Bodenfeuchtigkeit wieder \n/Lichtstaerke  # Gibt die aktuelle Lichtstaerke wieder \n/Info  # Gibt alle aktuellen Parameter wieder\n/Hilfe gibt diese Narchicht erneut wieder\n-----Monitore-----\n---Starten---\n Beim erstellen der Monitore gibt das XX die Zahl fuer die Obergrenze und YY die Zahl fuer die Untergrenze an\n/LuftfeuchtigkeitMonitor XX YY #Angabe in %% \n/TemperaturMonitor XX YY # Angabe in Grad C\n/BodenfeuchtigkeitMonitor XX YY\n# Angabe in % von 0-50%\n----Stoppen----\nDie Befehle Stoppen den ausgewaelten Monitor\n/LuftfeuchtigkeitMonitorSTOP \n/TemperaturMonitorSTOP\n/BodenfeuchtigkeitMonitorSTOP\n/LichtstaerkeMonitorSTOP")


#Monitore fuer Ueberwachung vorconfigurieren
licht_mon = None
boden_mon = None
temperatur_mon = None
humidity_mon =None


#Message Handler fuer Empfangene Telegramnarchichten
def handle(msg):
    global licht_mon
    global boden_mon
    global temperatur_mon
    global humidity_mon

    message =msg['text']                    #Nur abgreifen des Textes
    if message == "/Hilfe":
#Empfangsnarchicht vom Bot senden
        bot.sendMessage(chatid,"-----Befehle-----\n/Temperatur  # Gibt die aktuelle Temperatur wieder \n/Luftfeuchtigkeit  # Gibt die aktuelle Luftfeuchtigkeit wieder \n/Bodenfeuchtigkeit # Gibt die aktuelle Bodenfeuchtigkeit wieder \n/Lichtstaerke  # Gibt die aktuelle Lichtstaerke wieder \n/Info  # Gibt alle aktuellen Parameter wieder\n/Hilfe gibt diese Narchicht erneut wieder\n-----Monitore-----\n---Starten---\n Beim erstellen der Monitore gibt das XX die Zahl fuer die Obergrenze und YY die Zahl fuer die Untergrenze an\n/LuftfeuchtigkeitMonitor XX YY #Angabe in %% \n/TemperaturMonitor XX YY # Angabe in Grad C\n/BodenfeuchtigkeitMonitor XX YY\n# Angabe in % von 0-50%\n----Stoppen----\nDie Befehle Stoppen den ausgewaelten Monitor\n/LuftfeuchtigkeitMonitorSTOP \n/TemperaturMonitorSTOP\n/BodenfeuchtigkeitMonitorSTOP\n/LichtstaerkeMonitorSTOP")

#Temperaturbefehl abfangen der Narchicht und auslesen des DHT11 Sensors
    if message == "/Temperatur":
        Temperatur = PotObject.read_temperature()
        bot.sendMessage(chatid,"Temperatur: %8.1f C" % (Temperatur))

#Luftfeuchtigkeitsbefehl abfangen der Narchicht und auslesen des DHT11 Sensors
    if message == "/Luftfeuchtigkeit":
        Luftfeuchtigkeit = PotObject.read_humidity()
        bot.sendMessage(chatid,"Luftfeuchtigkeit: %8.1f %%" % (Luftfeuchtigkeit))

#Bodenfeuchtigkeitsbefehl abfangen der Narchicht und auslesen des Lichtstaerkesensor bzw. AD Wandler mit I2C Bus
    if message == "/Bodenfeuchtigkeit":
        Bodenfeuchtigkeit = PotObject.read_soil_moisture()
        bot.sendMessage(chatid,"Bodenfeuchtigkeit: %8.4f %%" % (Bodenfeuchtigkeit))

#Lichtstaerkebefehl abfangen der Narchicht und auslesen des Lichtstaerkesensor bzw. AD Wandler mit I2C Bus
    if message == "/Lichtstaerke":
        Lichtstaerke = PotObject.read_light_intensity()
        bot.sendMessage(chatid,"Lichtstaerke: %8.1f %%" % (Lichtstaerke))

#Info Befehl abfangen und alle Daten ausgeben
    if message == "/Info":
        print(message)                          #Ausgabe des Textes
        Temperatur = PotObject.read_temperature()
        Luftfeuchtigkeit = PotObject.read_humidity()
        Bodenfeuchtigkeit = PotObject.read_soil_moisture()
        Lichtstaerke = PotObject.read_light_intensity()
        bot.sendMessage(chatid,"------------Info------------\n" + "Temperatur: %8.1f C\n" % (Temperatur) + "Luftfeuchtigkeit: %8.1f %% \n" % (Luftfeuchtigkeit) + "Bodenfeuchtigkeit: %8.4f %% \n" % (Bodenfeuchtigkeit) + "Lichtstaerke: %8.4f %% \n" % (Lichtstaerke) + "----------------------------")
   
#Der Message String wird geteilt wenn ein Leerzeichen vorhanden ist und in die Liste der Einzeldaten geschrieben
    einzeldaten = message.split(" ")

#Abfrage der Narchicht fuer den Luftfeuchtigkeitsmonitor mit ueberpruefung der Einzelnen Elemente der Liste mithilfe der HysteresisMonitorfunktion wird der Monitor erstellt
    if einzeldaten[0] == "/LuftfeuchtigkeitMonitor":
#Wenn zu wenig Argumente angegebne worden sind
        if len(einzeldaten) == 1:
            bot.sendMessage(chatid,"Zu wenig Argumente")
#Wenn ein Monitor ohne Untergrenze erstellt werden soll
        if len(einzeldaten) == 2:
            if humidity_mon != None:
                humidity_mon.stop()
                humidity_mon.join()
            Obergrenze = einzeldaten[1]
            print("Starting Luftfeuchtigkeits Monitors...")
            humidity_mon = HysteresisMonitor("Humidity", PotObject.read_humidity, int(einzeldaten[1]), callbackhumi, callback_lw_thres=callbackhumi2)
            humidity_mon.start()
            bot.sendMessage(chatid,"LuftfeuchtigkeitsMonitor wurde gestartet mit der Obergrenze %s und ohne Untergrenze" % (einzeldaten[1]))
#Wenn ein  Monitor mit Untergrenze erstelllt werden soll
        if len(einzeldaten) == 3:
            if humidity_mon != None:
                humidity_mon.stop()
                humidity_mon.join()
            Obergrenze = einzeldaten[1]
            Untergrenze = einzeldaten[2]
            print("Starting Luftfeuchtigkeits Monitors...")
            humidity_mon = HysteresisMonitor("Humidity", PotObject.read_humidity, int(einzeldaten[1]), callbackhumi, callback_lw_thres=callbackhumi2, lower_thres=int(einzeldaten[2]))
            humidity_mon.start()
            bot.sendMessage(chatid,"LuftfeuchtigkeitsMonitor wurde gestartet mit der Obergrenze %s und einer Untergrenze von %s" % (einzeldaten[1],einzeldaten[2]))
#Wenn ein Monitor erstellt werden soll jedoch zu viele Argumente angegeben worden sind
        if len(einzeldaten) >= 4:
            bot.sendMessage(chatid,"Zu viele Argumente")

#Abfrage der Narchicht fuer den Temperaturmonitor mit ueberpruefung der Einzelnen Elemente der Liste mithilfe der HysteresisMonitorfunktion wird der Monitor erstellt
    if einzeldaten[0] == "/TemperaturMonitor":
        if len(einzeldaten) == 1:
            bot.sendMessage(chatid,"Zu wenig Argumente")
        if len(einzeldaten) == 2:
            if temperatur_mon != None:
                temperatur_mon.stop()
                temperatur_mon.join()
            Obergrenze = einzeldaten[1]
            print("Starting Temperatur Monitors...")
            temperatur_mon = HysteresisMonitor("Temperatur", PotObject.read_temperature, int(einzeldaten[1]), callbacktemp, callback_lw_thres=callbacktemp2)
            temperatur_mon.start()
            bot.sendMessage(chatid,"TemperaturMonitor wurde gestartet mit der Obergrenze %s und ohne Untergrenze" % (einzeldaten[1]))
        if len(einzeldaten) == 3:
            if temperatur_mon != None:
                temperatur_mon.stop()
                temperatur_mon.join()
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
            if boden_mon != None:
                boden_mon.stop()
                boden_mon.join()
            Obergrenze = einzeldaten[1]
            print("Starting Bodenfeuchtigkeit Monitors...")
            boden_mon = HysteresisMonitor("Bodenfeuchtigkeit", PotObject.read_soil_moisture, int(einzeldaten[1]), callbackboden, callback_lw_thres=callbackboden2)
            boden_mon.start()
            bot.sendMessage(chatid,"BodenfeuchtigkeitMonitor wurde gestartet mit der Obergrenze %s und ohne Untergrenze" % (einzeldaten[1]))
        if len(einzeldaten) == 3:
            if boden_mon != None:
                boden_mon.stop()
                boden_mon.join()            
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
            if licht_mon != None:
                licht_mon.stop()
                licht_mon.join()
            Obergrenze = einzeldaten[1]
            print("Starting Lichstaerke Monitors...")
            licht_mon = HysteresisMonitor("Lichstaerke", PotObject.read_light_intensity, int(einzeldaten[1]), callbacklicht, callback_lw_thres=callbacklicht2)
            licht_mon.start()
            bot.sendMessage(chatid,"LichstaerkeMonitor wurde gestartet mit der Obergrenze %s und ohne Untergrenze" % (einzeldaten[1]))
        if len(einzeldaten) == 3:
            if licht_mon != None:
                licht_mon.stop()
                licht_mon.join()
            Obergrenze = einzeldaten[1]
            Untergrenze = einzeldaten[2]
            print("Starting Bodenfeuchtigkeit Monitors...")
            licht_mon = HysteresisMonitor("Lichstaerke", PotObject.read_light_intensity, int(einzeldaten[1]), callbacklicht, callback_lw_thres=callbacklicht2, lower_thres=int(einzeldaten[2]))
            licht_mon.start()
            bot.sendMessage(chatid,"LichstaerkeMonitor wurde gestartet mit der Obergrenze %s und einer Untergrenze von %s" % (einzeldaten[1],einzeldaten[2]))
        if len(einzeldaten) >= 4:
            bot.sendMessage(chatid,"Zu viele Argumente")

#Auswerten des Monitor Stop Befehls fuer den Luftfeuchtigkeits Monitor
    if message == "/LuftfeuchtigkeitMonitorSTOP":
        print(message)                          #Ausgabe des Textes
        if humidity_mon == None:
            bot.sendMessage(chatid,"Es war kein Luftfeuchtigkeit Monitor gestaret.")
        if humidity_mon != None:
            humidity_mon.stop()
            humidity_mon.join()
            humidity_mon = None
            bot.sendMessage(chatid,"Luftfeuchtigkeit Monitor wurde erfolgreich gestopt.")
        
#Auswerten des Monitor Stop Befehls fuer den Temperatur Monitor
    if message == "/TemperaturMonitorSTOP":
        print(message)                          #Ausgabe des Textes
        if temperatur_mon == None:
            bot.sendMessage(chatid,"Es war kein Temperatur Monitor gestaret.")
        if temperatur_mon != None:
            temperatur_mon.stop()
            temperatur_mon.join()
            temperatur_mon = None
            bot.sendMessage(chatid,"Temperatur Monitor wurde erfolgreich gestopt.")
        
#Auswerten des Monitor Stop Befehls fuer den Bodenfeuchtigkeits Monitor
    if message == "/BodenfeuchtigkeitMonitorSTOP":
        print(message)                          #Ausgabe des Textes
        if boden_mon == None:
            bot.sendMessage(chatid,"Es war kein Bodenfeuchtigkeit Monitor gestaret.")
        if boden_mon != None:
            boden_mon.stop()
            boden_mon.join()
            boden_mon = None
            bot.sendMessage(chatid,"Bodenfeuchtigkeit Monitor wurde erfolgreich gestopt.")
        
#Auswerten des Monitor Stop Befehls fuer den Lichtstaerke Monitor
    if message == "/LichstaerkeMonitorSTOP":
        print(message)                          #Ausgabe des Textes
        if licht_mon == None:
            bot.sendMessage(chatid,"Es war kein Lichstaerke Monitor gestaret.")
        if licht_mon != None:
            licht_mon.stop()
            licht_mon.join()
            licht_mon = None
            bot.sendMessage(chatid,"Lichstaerke Monitor wurde erfolgreich gestopt.")
        
#Starten des Messageloops zur ueberwachung und Auswertung der Telegrameingabe als Thread
MessageLoop(bot, handle).run_as_thread()

#Callback fuer Monitor oberen Grenzwert Luftfeuchtigkeit
def callbackhumi(timestamp, value, threshold, name):
    print("Value "+ name + "=" +str(value)+ "passed threshold of " + str(threshold) + " at " + str(timestamp) +".")
    PotObject.output_on(SmartPot.X4)
    bot.sendMessage(chatid,"Es ist eine zu hohe Luftfeuchtigkeit im Raum diese liegt bei %3.0f%%" % (value))

#Callback fuer Monitor unteren Grenzwert Luftfeuchtigkeit
def callbackhumi2(timestamp, value, threshold, name):
    PotObject.output_off(SmartPot.X4)
    bot.sendMessage(chatid,"Die Luftfeuchtigkeit im Raum ist wieder gut sie liegt bei %3.0f%%" % (value))

#Callback fuer Monitor oberen Grenzwert Temperatur
def callbacktemp(timestamp, value, threshold, name):
    print("Value "+ name + "=" +str(value)+ "passed threshold of " + str(threshold) + " at " + str(timestamp) +".")
    PotObject.output_on(SmartPot.X4)
    bot.sendMessage(chatid,"Es ist zu warm im Raum die Temperatur betraegt %3.0f Grad C" % (value))

#Callback fuer Monitor unteren Grenzwert Temperatur
def callbacktemp2(timestamp, value, threshold, name):
    PotObject.output_off(SmartPot.X4)
    bot.sendMessage(chatid,"Die Temperatur ist wieder gut sie betraegt %3.0f Grad C" % (value))

#Callback fuer Monitor oberen Grenzwert Bodenfeuchtigkeit
def callbackboden(timestamp, value, threshold, name):
    print("Value "+ name + "=" +str(value)+ "passed threshold of " + str(threshold) + " at " + str(timestamp) +".")
    PotObject.output_on(SmartPot.X4)
    bot.sendMessage(chatid,"Der Boden ist genug gewaessert die Bodenfeuchtigkeit liegt bei %3.2f%%" % (value))

#Callback fuer Monitor unteren Grenzwert Bodenfeuchtigkeit
def callbackboden2(timestamp, value, threshold, name):
    PotObject.output_off(SmartPot.X4)
    bot.sendMessage(chatid,"Der Boden ist zu trocken ich benoetige Wasser die Bodenfeuchtigkeit liegt bei %3.2f%%" % (value))

#Callback fuer Monitor Oberen Grenzwert Lichstaerke
def callbacklicht(timestamp, value, threshold, name):
    print("Value "+ name + "=" +str(value)+ "passed threshold of " + str(threshold) + " at " + str(timestamp) +".")
    PotObject.output_on(SmartPot.X4)
    bot.sendMessage(chatid,"Die Lichtstaerke ist absolut ausreichend sie betraegt %3.2f%%" % (value))

#Callback fuer Monitor unteren Grenzwert Lichstaerke
def callbacklicht2(timestamp, value, threshold, name):
    PotObject.output_off(SmartPot.X4)
    bot.sendMessage(chatid,"Es ist zu dunkel im Raum die Lichtstaerke betraegt %3.2f%%" % (value))

#Definierung welche Werte vom Zetlichen Monitor abgefragt werden
def  monitor_getter():
   return PotObject.read_humidity(), PotObject.read_temperature(), PotObject.read_soil_moisture(), PotObject.read_light_intensity()

#Callback Funktion zum Logging mit dem Zetlichen Monitor
def callbackBackup(now, val, name):
    print(str(now) + " - " +name+"="+str(val))
    zeit = str(int(time.mktime(now.timetuple())))
    humi = str(val[0])
    temp = str(val[1])
    moisture = str(round(val[2],0))
    light = str(round(val[3],0))
    
    file = open("Logging.csv","a")

    file.write(zeit + ";" + humi + ";" + temp + ";" + moisture + ";" + light + "\n")
    
    file.close()

#Erstellen des Monitors der alle 5 sek Logging Daten sammelt
time_mon = TimeBasedMonitor("Info", monitor_getter, callbackBackup, 5)
time_mon.start()




while 1:
    time.sleep(10)


