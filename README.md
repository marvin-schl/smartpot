# SmartPot

SmartPot ist ein RaspberryPi Projekt um einen smarten Blumentopf/Gewächshaus umzusetzen. Es werden alle für 
Pflanzen wichtigen Parameter (Temperatur, Luft-/Bodenfeuchtigkeit und Lichtstärke) gemessen und 
auf verschiedenen Wegen zur Verfügung stellt. Die Visualisierung der Daten kann über einen Webserver des 
Raspberry Pi´s aufgerufen und analysiert werden. Alternativ können die Sensorwerte auch per 
Telegram manuell erfragt werden. Außerdem können für alle Parameter kritische Schwellenwerte programmiert werden, bei deren 
Unter- bzw. Überschreiten eine Benachrichtigung über Telegram abgeschickt wird.
Im Folgenden wird die Umsetzung des Projektes detailliert dokumentiert, sodass mit Hilfe dieser 
Anleitung ein Nachbau des SmartPots möglich wird. Es werden alle Softwareeinrichtungsschritte von der Erstellung des Telegram Bots bis zur Node-RED Einrichtung erklärt. Außerdem werden Schaltpläne bereitgestellt welche auf die Softwareimplementationen angepasst sind. Zusätzlich zu den Schaltplänen wird ebenso ein Leiterplattenlayout, sowie alle benötigten Komponenten zum Bestücken der Leiterplatte mit einer Preisübersicht zur Verfügung gestellt

Schaltungsseitig sind zur Zeit folgende Funktionalitäten implementiert:

- ein auf den RaspberryPi steckbares Shield mit integrierterm 12V/5V Linearregler zur Spannungsversorgung des Pi´s
- Anbindung eines Temperatur/Luftfeuchtigkeitssensors (DHT11/DHT22)
- Anbindung eines Bodenfeuchtigkeitssensors
- Anbindung eines Lichtsensors
- Drei schaltbare 12V/1,5A Leistungsausgänge mit PWM Unterstützung

Softwareseitig ist die aktuelle Version des SmartPots beinhaltet folgende Funktionen:

- _Temperatur_ messen, überwachen, auslesen und ausgeben
- _Luftfeuchtigkeit_ messen, überwachen,  auslesen und ausgeben
- _Bodenfeuchtigkeit_ messen, überwachen, auslesen und ausgeben
- _Lichtstärke_ messen, überwachen, auslesen und ausgeben
- Kommunikationsinterface über Telegram Web
- Node-RED Visualisierung der Sensorwerte (historisch/live)

Die Idee einen intelligenten Blumentopf zu entwickeln wurde durch zahlreiche Anleitungen aus dem
Web inspiriert (Bspw: [Automatisches Gewächshaus](https://tutorials-raspberrypi.de/automatisches-raspberry-pi-gewaechshaus-selber-bauen/)).

Der modulare Aufbau dieses Projektes eignet sich sehr gut für Gruppenarbeiten und kann dem
jeweiligen Wissensstand (Programmierung vom Raspberry Pi) durch Variation der
Funktionskomplexität angepasst werden.

In zukünftigen Versionen könnte unter einer optimierten Ausnutzung der verfügbaren Leistungsausgänge und Erweiterung von finanziellen Mitteln weitere Funktionen wie z.B. automatische Bewässerung, Lichtregelung sowie Belüftung realisiert werden, um so den Automatisierungsgrad weiter zu erhöhen.

## Gliederung

Diese Dokumentation glieder sich in folgende Schritte an denen unter Anderem die Inbetriebnahme des SmartPots erläutert wird:

1. Die Erstellung eines Telegram Bots 
2. Die Konfiguration des Telegram Bots für den SmartPot
3. Die Einrchtung von Node Red und der SmartPot Software selber 
    - 3.1 als manuelle Einichtung **oder**
    - 3.2  als automatische Einrchtung via docker und docker-compose
4. Die Bereitstellung der Schaltpläne und eines Leiterplattenlayout, zum Nachbau auf einem Bredboard oder zur Fertigung einer Leiterplatte, inklusive Stückliste aller benötigten Komponenten
5. Einer kurzen Übersicht der enthaltenen Klassen und Methoden 
6. Eine Übersicht, welche bekannten Schwachstellen und Verbesserungsideen für zukünftige Versionen des SmartPots existieren

## 1. Einrichtung des TelegramBots

Zunächst muss ein Chat mit dem Telegram-Bot „BotFather“ wie folgt erstellt werden:
Bei Telegram im Suchfeld „BotFather“ eingeben und unter Chats den BotFather auswählen.

![](https://github.com/marvin-schl/smartpot/raw/master/pictures/bot_1.png)

Im Chat des BotFathers kann nun ein Chatbot erstellt werden:

1. /newbot eingeben
2. Botname vergeben
3. Username vergeben
4. Bot-Token kopieren
5. Link für Chatbot anklicken

![](https://github.com/marvin-schl/smartpot/raw/master/pictures/bot_2.png)

Zum Abfragen neuer Nachrichten muss im Browser folgende Website aufgerufen werden:

https://api.telegram.org/botReplaceThisWithTheBotFatherToken/getUpdates

In Telegram Web dem erstellten Chatbot eine Nachricht senden. 

![](https://github.com/marvin-schl/smartpot/raw/master/pictures/bot_4.png)

Nach Neuladen der Website kann nun aus der geschickten Nachricht die Chat-ID
ermittelt werden.

![](https://github.com/marvin-schl/smartpot/raw/master/pictures/bot_3.png)

(Optional) Um den Chatbot einer Gruppe hinzufügen zu können, muss folgende Konfiguration im
BotFather vorgenommen werden:

1. /setprivacy eingeben
2. @Botname eingeben
3. Disable eingeben

![](https://github.com/marvin-schl/smartpot/raw/master/pictures/bot_6.png)

***Achtung:** Wenn sich der Chatbot in einer Gruppe befindet, muss die Chat-ID der Gruppe verwendet werden!*

## 2. Konfiguration des SmartPots

Es wird davon ausgegangen, dass auf dem RaspberryPi ein neu installiertes RaspianOS basierend auf Debian Buster installiert, ein Zugang zum Internet, sowie ein ssh Zugang vorhanden ist. Zunächst muss dieses Repository auf dem RaspberryPi geclonet werden:

    git clone https://git.haw-hamburg.de/aco732/smartpot.git

Für die Konfiguration steht eine smartpot.ini Datei zur Verfügung. 

``` ini
#############################################
# Smart Pot Version 1 - Configuration File  #
#############################################

[Telegram]

#Sets the telepot API token
chattoken = <your-token>

#Sets the telepot Chat-ID
chatid = <your-chat-id>

[Logging]

# Sets the loglevel, when not specified DEBUG is taken
# Possible Values: INFO, WARN, ERROR, DEBUG
level = DEBUG

# If set to 1 the logs will be printed on sys.stdout
# If set to 1 there will be no logging to a a logfile
stdout = 1

# Sets the logfile
# This options is ignored when logging to stdout
file = smartpot.log


[Soil Moisture]
# This section calibrates the soil moisture sensor. Keep in mind that any calibration action will only effect the
# python software. Depending on the Calibration it is possible that the Node-RED settings have to updated manually

# Calibration of the soil moisture sensor connected to adc channel 1.
# The calibrated output value is calculated from the Output value out [V]  follows:
#     calibrated_out = scaling*(out - offset)
# Calibration procedure:
#    1.) Set both Values to zero.
#    2.) Connect the sensor and make sure it's 100% dry.
#    3.) Measure the voltage offset and adjust offset_calibration value to get an calibrated_out of 0.
#    4.) Pull the sensor onto a defined soil moisture level.
#    5.) Adjust scaling in such a way that calibratet_out matches the desired value.
offset = 0.0
scaling = 1.9

# Defines the level at which calibrated_out is going into saturation. Comment out
# to disable saturation.
saturation = 1.9

# Defines the unit of the measured and calibrated value
unit = "%"

[Light]
# This section calibrates the light sensor. Keep in mind that any calibration action will only effect the
# python software. Depending on the Calibration it is possible that the Node-RED settings have to updated manually.

# Calibration of the light sensor connected to adc channel 2.
# The calibrated ouput value is calculated from the Output value out [V] as follows:
#     calibrated_out = scaling*(out - offset)
# Calibration procedure:
#    1.) Set both Values to zero.
#    2.) Connect the sensor and make sure it's completly dark.
#    3.) Measure the voltage offset and adjust offset_calibration value to get an calibrated_out of 0.
#    4.) Pull the sensor onto a defined brightness level.
#    5.) Adjust scaling in such a way that calibratet_out matches the desired value.

offset = 0.0
scaling = 1.8

# Defines the level at which calibrated_out is going into saturation. Comment out
# to disable saturation.
saturation = 1.8

# Defines the unit of the measured and calibrated value
unit = "%"
```

In der Konfiguationsdatei müssen nun der zuvor ermittelte Telegram API-Token unter chattoken und die ermittelte Chat-ID unter chatid eingetragen werden. Außerdem können das Log-Level, das Ausgabeformat der Logs und die Kalibration der analogen Sensoren angepasst werden. 

Alternativ kann das setup.sh Skript ausgeführt werden, um die Telegram Konfiguration durchzuführen. Auf die abschließende Frage, ob der SmartPot via docker-compose gestartet werden soll, muss in diesem Fall mit "n" geantwortet werden:

    bash setup.sh

## 3.1 manuelle Einrichtung des RaspberryPi's


Zuerst müssen über Python Paketmanager pip folgende Pakete installiert werden.

    pip3 install RPi.GPIO Adafruit_DHT smbus2 telepot

Desweiteren wird eine [Library für den MCP3426](https://github.com/coburnw/MCP342x) für den MCP3426 verwendet. Diese ist bereits in den Source Files enthalten.



### Einrichten von Node-RED

Das Installation von Node-RED erfolgt durch folgende Shell-Eingabe:

    bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered) --node16

Das Node-RED Dashboard zur Visualisierung der Sensorwerte wird mit folgender Eingabe installiert:

    npm i node-red-dashboard

Zusätzlich müssen in den Node-RED Einstellungen Parameter konfiguriert werden:

    cd ~/.node-red
    nano settings.js

@Line 253: „//“ entfernen

![node-red_settings](https://github.com/marvin-schl/smartpot/raw/master/pictures/node-red_settings.png)

Um Node-RED bei Systemstart automatisch auszuführen wird folgender Befehl verwendet:

    sudo systemctl enable nodered.service

Der Node-RED Editor ist über die IP-Adresse des Pi´s aufzurufen. Die IP wird wie folgt angezeigt:

    hostname -l

Node-RED ist standardmäßig auf Port 1880 erreichbar. Mit dem im vorherigen Schritt ermittelten <hostname> kann die Node-RED Konfiguration unter folgender Adresse im Interetbrowser aufgerufen werden:
    
    http://<hostname>:1880

Die vorbereitete Node-RED Visualisierung kann nun wie folgt installiert werden:

1. Menü-Reiter auswählen
2. Palette verwalten klicken

![](https://github.com/marvin-schl/smartpot/raw/master/pictures/dashboard_1.png)

3. „Dashboard“ in Suchfeld eingeben
4. Auf „Installieren“ klicken

![](https://github.com/marvin-schl/smartpot/raw/master/pictures/dashboard_2.png)

Die zur Verfügung gestellte Visualisierung des Node-RED Dashboards muss nun wie folgt kopiert werden:

    cp /home/pi/smartpot/resources/flows.json /home/pi/.node-red/lib/flows

Abschließend wird die flow-Datei in Node-RED importiert:

1. Menü-Reiter auswählen
2. Import klicken

![](https://github.com/marvin-schl/smartpot/raw/master/pictures/dashboard_3.png)

3. Lokal auswählen
4. „flows.json“ wählen

![](https://github.com/marvin-schl/smartpot/raw/master/pictures/dashboard_4.png)

5. Auf „Import“ klicken
6. „Übernahme (deploy)“ klicken

![](https://github.com/marvin-schl/smartpot/raw/master/pictures/dashboard_5.png)

Die Visualisierung kann nun unter 

    http://<hostname>:1880/ui

erreicht werden.

## 3.2 automatische Einrichtung des RaspberryPi's via Docker

Falls docker und docker-compose bereits installiert sein sollten kann der nächste Schritt übersprungen werden und direkt mit "Starten der Smartpot Umgebung" fortgefahren werden.

### Einrichtung von docker und docker-compose

Für die Einrichtung von docker und docker-compose müssen folgende Befehle ausfgeführt werden.

    sudo apt-get update
    curl -sSL https://get.docker.com | sh
    sudo apt-get install docker-compose
    sudo usermod -aG docker pi

Nachdem der letzte Befehl ausfgeführt worden ist muss der Pi neugstartet werden.

   sudo reboot

### Starten der Smartpot Umgebung

Vor dem ersten Start muss die setup.sh ausgeführt werden. Diese stellt sicher, dass die ini, log und csv Dateien vorhanden sind und die Telegrameinstellungen getätigt worden sind. Außerdem stellt diese sicher, dass die Container mit ausreichenden Rechten gestartet werden:
    
    bash setup.sh
    
Der SmartPot kann gleich im Anschluss darauf us dem Skript heraus gestartet werden. **Sollte der Start nicht direkt aus der setup.sh erfolgen muss zuerst ein Neustart oder Neulogin durchgeführt werden!**
Aus dem SmartPot Verzeichnis kann nach Neustart/Neulogin in Zukunft der SmartPot wie folgt gestartet werden:

    docker-compose up
    
Um den SmartPot als Hintergrunddienst laufen und automatisch starten zu lassen, muss zusätzlich das Flag -d/--detached (losgelöst) verwendet werden:
    
    docker-compose up -d

## 4. elektronischer Aufbau

Schaltplan des RaspberryPi Shields:

![Schaltplan](https://github.com/marvin-schl/smartpot/raw/master/pcb/Bilder/schematic.png)

Die Schaltung kann an einem handelsüblichen 12V Netzteil betrieben werden. Über einen 12V/5V Linearregler (uA78S05)
wird die Versorgnungsspannung für den RaspberryPi bereit gestellt. Auf dem Board ist eine dreipolige Buchsenleiste für einen DHT11 bzw DHT22 Sensor vorgesehen. Der Sensor kann einfach auf die Buchsenleiste gesteckt (Sensorseitig zur Platinenmitte zeigend) werden und per OneWire Protokoll ausgelesen werden. Für den analogen Lichtsensor und den analogen Bodenfeuchtigkeitssensors ist ein 2 Kanal Delta-Sigma AD-Wandler mit I2C Interface, der MCP3426, verbaut. Die drei Leistungsausgänge werden von drei P-Kanal Mosfets (AO3401A) geschaltet. Die Gate Signale werden durch einen Darlington-Array (ULN2003AD) getrieben, welches die Rohsignale des RaspberryPi verstärkt.
    
Für einen Betrieb des SmartPots über ein Bredboard muss in der aktuellen Version des SmartPots lediglich der DHT mit J1-12 und der MCP3426, zusätzlich zu seiner äußeren Beschaltung, mit den I2C-Pins J1-3 und J1-5 verbunden werden. Dann können die Sensoren analog zum o.g. Schaltplan ausgelesen werden. 

Das dazugehörige Layout wurde wie folgt umgesetzt:

![Layout](https://github.com/marvin-schl/smartpot/raw/master/pcb/Bilder/layout.png)


### Stückliste


Position    |Bezeichnung                        | Anzahl  |Stückpreis €| Positionspreis €
------------|-----------------------------------|-------- |------------|-----------------
1           | RaspberryPi 3B                    |1        |39,4        | 39,4
2           | RaspberryPi Staking Header        |1        |1,6         | 1,60
3           | ULN2003AD                         |1        |0,75        | 0,75
4           | 10k Kohleschichtwiderstand        |4        |0,1         | 0,4
5           | RPI LK Kabel 50                   |2        |2,75        | 5,50
6           | MCP3426                           |1        |3,10        | 3,10
7           | uA78S05                           |1        |0,45        | 0,45
8           | BD204                             |1        |0,41        | 0,41
9           | AO3401A                           |3        |0,25        | 0,75
10          | Widerstand 0805 1,0               |1        |0,03        | 0,03
11          | Widerstand 0805 2,0               |1        |0,02        | 0,02
12          | Widerstand 0805 51,0              |3        |0,02        | 0,06
13          | Widerstand 0805 5k                |2        |0,03        | 0,06
14          | Widerstand 0805 10k               |3        |0,03        | 0,09
15          | Keramikkondensator 0805 100nF     |1        |0,02        | 0,02
16          | Tantalkondensator 1210 10uF       |1        |0,32        | 0,32
17          | Elektrolytkondensator 2mm 1uF     |2        |0,02        | 0,04
18          | Elektrolytkondensator 5mm 1mF     |1        |0,29        | 0,29
19          | JST XH2P ST Buchse                |3        |0,20        | 0,60
20          | JST XH4P ST Buchse                |2        |0,25        | 0,50
21          | 3fach Buchsenleiste 2,54mm        |1        |0,14        | 0,14
22          | DC Buchse 2.1mm                   |1        |1,20        | 1,20
23          | DHT11                             |1        |4,50        | 4,50
24          | Joy-It Linker Kit Lichtsensor     |1        |1,01        | 1,01
25          | Joy-it sen-Moisture Sensorkit     |1        |4,99        | 4,99
26          | Leiterplatte                      |1        |2,00        | 2,00
27          | Gesamt                            |         |            | 68,23

(Reichelt Preise beispielhaft, Stand 06.01.22)


## 5. Software Implementation



Nachfolgend soll eine Klassenreferenz augestellt werden. Die einen Überblick über die implementierten Klassen und deren Methoden gib. Für eine genauere Beschreibung bitte die Methoden Kommentare beachten. Dort werden die einzelnen Argumente genauer beschrieben. 

**monitor.HysteresisMonitor**:
Diese Klasse implementiert die nicht blockierende Überwachung einer Ausgangsgröße. Es kann eine Funktion übergeben werden, welche den zu überwachenden Wert zurückgibt, ein oberer Grenzwert und ein unterer Grenzwert. Außerdem kann für das überschreiten des oberen und das unterschreiten des unteren Grenzwerts jeweils eine Callback Funktion übergeben werden. Diese Klasse erbt von threading.Thread. Eine Beispielhafte Verwendung dieser Klasse ist in example.py gegeben.

Öffentliche Methoden:
- start()
- stop()
- run()

**mointor.TimeBasedMonitor**:
Diese Klasse implementiert die nicht blockierende Überwachung einer Ausgangsgröße. Es kann eine Funktion übergeben werden, die die zu überwachende(n) Größe(n) zurückgibt. Diese Klasse erbt von threading.Thread. Eine Beispielhafte Verwendung dieser Klasse ist in example.py gegeben.

Öffentliche Methoden:
- start()
- stop()
- run()

**SmarPot.smartpot.SmartPot**:
Diese Klasse implementiert eine physikalische Repräsentation des SmartPots an sich und dient als Interface zum Backend. Es sind drei Konstanten vorhanden SmarPot.smarpot.SmartPot.X4, SmarPot.smarpot.SmartPot.X5 und SmarPot.smarpot.SmartPot.X6. Diese referenzieren die Leistungsausgänge auf dem SmartPot Raspberry Shield rev 1.1 und können den output_* Methoden als pin übergeben werden.
Öffentliche Methoden:
- output_on(pin)
- output_off(pin)
- output_pwm_on(pin, freq, dc)
- output_pwm_off(pin)
- output_pwm_change_freq(pin, freq)
- output_pwm_change_dc(pin, dc)
- read_temperature()
- read_humidity()
- read_light_intensity()
- read_soil_moisture()

**SmartPot.dht.DHT**:
Diese Klasse wrapped die Adafruit_DHT Library und stellt einen objektorientierten Zugriff zur Verfügung. Es kann bei der instanziierung festgelgt werden ob es sich um einen DHT11 oder DHT22 handelt.

Öffentliche Methoden:
- read_temperature()
- read_humidity()

**SmartPot.adc.MCP3426**:
Diese Klasse wrapped die verwendete [MCP342x](https://github.com/coburnw/MCP342x) Library für die hier benötigete Anwendung.

Öffentliche Methoden:
- read_ch1()
- read_ch2()


**SmartPot.output.PowerOutputPin**:
Diese Klasse verwendendet das RPi.GPIO Modul und implementiert die Funktionen der Leistungsausgänge. 

Öffentliche Methoden
- on()
- off()
- start_pwm(freq, dc)
- stop_pwm()
- change_freq(freq)
- change_dc(dc)


## 6. Ausblick

Hier werden bekannte Schwächen der aktuellen Version des SmartPots sowies des dazugehörige Shield aufgelistet, welche in folgenden Versionen überarbeitet werden sollten.

- Der Linearregler auf der pcb wird bei Betrieb mit einem 12V Netzteil und hohen Stromverbräuchen des Raspberrys sehr warm. Hier wäre eine Spannungswandlung über einen Schaltregler zu bevorzugen.

- Beim Ausschalten der Leistungsausgänge, also wenn das Gatesignal der Ausgangsmosfets (Q2, Q3, Q4) von 0V auf 12V gezogen wird. Findet die Entladung der Gatekapazität im unbelaseten Zustand über die Pullup Widerstände (R5, R6, R7) statt. Dies führt zumidest im unbelasteten Zustand zu sehr hohen Abfallszeit des Ausgangssignals. Ein Ansatz wäre kleinere Pullup Widerstände zu verwenden auf Kosten einer höheren Stromaufnahme bei eingeschaltetem Ausgang. Ein anderer Ansatz wäre die verwendung einer richtigen Mosfet Endstufe.

- In dem jetzigen Design wurden die positiven und negativen Ch2 Eingangspins des MCP3426 vertauscht. Die folgliche invertiert gemessene Spannung wurde Softwareseitig kompensiert.
    
- Die Ausgangssignale der analog Sensoren sind bis zu 4V hoch. Der MCP3426 kann jedoch nur +-2,048V messen. Eine Lösuing wäre ein auf der pcb befindlicher 1:1 Spannungsteiler, ein anderer AD-Wandler oder besser an den AD-Wandler angepasste Sensoren.

- Eine Verbesserung des Automatisierungsgrades durch die Nutzung der Hardwareseitig implementierten Schaltfunktionen

- Eine Erweiterung der Node-RED Oberflächen, sodass nicht nur ein passives Monitoring sondern auch eine aktive Kontrolle des SmartPots möglich ist


