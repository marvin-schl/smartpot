# SmartPot

SmartPot ist ein RaspberryPi Projekt um einen smarten Blumentopf/Gewächshaus umzusetzen. Es werden alle für 
Pflanzen wichtigen Parameter (Temperatur, Luft-/Bodenfeuchtigkeit und Lichtstärke) gemessen und 
informativ zur Verfügung stellt. Die Visualisierung der Daten kann auf der Homepage des 
Raspberry Pi´s aufgerufen und analysiert werden. Alternativ können die Sensorwerte auch per 
Telegram manuell erfragt werden. Außerdem können für diese Parameter kritische Schwellenwerte programmiert werden, bei deren 
Unter- bzw. Überschreiten eine Benachrichtigung über Telegram abgeschickt wird.
Im Folgenden wird die Umsetzung des Projektes detailliert dokumentiert, sodass mit Hilfe dieser 
Anleitung ein Nachbau des SmartPots möglich wird.

Die Software ist Python basiert und wurde auf einen RaspberryPi 3 entwickelt, sollte aber unabhängig davon auf allen RaspberryPi's mit den selben Header Pinout funktionieren.

Der SmartPot an sich umfasst folgende Hardwarefunktionalitäten:

- ein auf den RaspberryPi steckbares Shield mit integrierterm 12V/5V Linearregler zur Spannungsversorgung des Pi´s
- Anbindung eines Temperatur/Luftfeuchtigkeitssensors (DHT11/DHT22)
- Anbindung eines Bodenfeuchtigkeitssensors
- Anbindung eines Lichtsensors
- Drei schaltbare 12V/1,5A Leistungsausgänge mit PWM Unterstützung

Die Idee einen intelligenten Blumentopf zu entwickeln wurde durch zahlreiche Anleitungen aus dem
Web inspiriert (Bspw: [Automatisches Gewächshaus](https://tutorials-raspberrypi.de/automatisches-raspberry-pi-gewaechshaus-selber-bauen/)).

Der modulare Aufbau dieses Projektes eignet sich sehr gut für Gruppenarbeiten und kann dem
jeweiligen Wissensstand (Programmierung vom Raspberry Pi) durch Variation der
Funktionskomplexität angepasst werden.
In der ersten Version des Frontends wurden unabhängig von den möglichen Hardwarefunktionen folgende Funktionen implementiert:

Die erste Version des SmartPots beinhaltet folgende Funktionen:
1) _Temperatur_ messen, überwachen, auslesen und ausgeben
2) _Luftfeuchtigkeit_ messen, überwachen,  auslesen und ausgeben
3) _Bodenfeuchtigkeit_ messen, überwachen, auslesen und ausgeben
4) _Lichtstärke_ messen, überwachen, auslesen und ausgeben
5) Kommunikation in Telegram Web
6) Node-RED Visualisierung der Sensorwerte (historisch/live)

Die Idee einen intelligenten Blumentopf zu entwickeln wurde durch zahlreiche Anleitungen aus dem 
Web inspiriert.[Link](https://tutorials-raspberrypi.de/automatisches-raspberry-pi-gewaechshaus-selber-bauen/)

In zukünftigen Versionen könnte unter einer optimierten Ausnutzung der verfügbaren Leistungsausgänge und Erweiterung von finanziellen Mitteln weitere Funktionen wie z.B. automatische Bewässerung, Lichtregelung sowie Belüftung realisiert werden, um so den Automatisierungsgrad weiter zu erhöhen.

## Gliederung

Diese Dokumentation glieder sich in folgende Schritte an denen unter Anderem die Inbetriebnahme des SmartPots erläutert wird:

1. Die Erstellung eines Telegram Bots 
2. Die Konfiguration des Telegram Bots für den SmartPot
3. Die Einrchtung von Node Red und der SmartPot Software selber 
    - 3.1 als manuelle Einichtung **oder**
    - 3.2  als automatische Einrchtung via Docker und Docker-Compose
4. Die Bereitstellung der Schaltpläne und Platinenlayouts, zum Nachbau auf einem Bredboard, Bestellung der Platine bzw. Eigenherstellung der Platine, inklusive Stückliste aller benötigten Komponenten
5. Einer kurzen Übersicht der enthaltenen Klassen und Methoden 
6. Eine Übersicht, welche bekannten Schwachstellen und Verbesserungsideen für zukünftige Versionen des SmartPots existieren

## 1. Einrichtung des TelegramBots

Zunächst muss ein Chat mit dem Telegram-Bot „BotFather“ wie folgt erstellt werden:
Bei Telegram im Suchfeld „BotFather“ eingeben und unter Chats den BotFather auswählen.

![](https://git.haw-hamburg.de/aco732/smartpot/-/raw/main/Dokubilder/bot_1.png?inline=false)

Im Chat des BotFather kann nun ein Chatbot erstellt werden:

1. /newbot eingeben
2. Botname vergeben
3. Username vergeben
4. Bot-Token kopieren
5. Link für Chatbot anklicken

![](https://git.haw-hamburg.de/aco732/smartpot/-/raw/main/Dokubilder/bot_2.png?inline=false)

Im Browser folgende Website aufrufen:

https://api.telegram.org/botReplaceThisWithTheBotFatherToken/getUpdates

In Telegram Web dem erstellten Chatbot eine Nachricht senden. 

![](https://git.haw-hamburg.de/aco732/smartpot/-/raw/main/Dokubilder/bot_4.png?inline=false)

Nach Neuladen der Website kann die Chat-ID
ermittelt werden.

![](https://git.haw-hamburg.de/aco732/smartpot/-/raw/main/Dokubilder/bot_3.png?inline=false)

(Optional) Um den Chatbot einer Gruppe hinzufügen zu können, muss folgende Konfiguration im
BotFather vorgenommen werden:

1. /setprivacy eingeben
2. @Botname eingeben
3. Disable eingeben

![](https://git.haw-hamburg.de/aco732/smartpot/-/raw/main/Dokubilder/bot_6.png?inline=false)

***Achtung:** Wenn sich der Chatbot in einer Gruppe befindet, muss die Chat-ID der Gruppe verwendet werden.*

## 2. Konfiguration des SmartPots

Es wird davon ausgegangen, dass auf dem RaspberryPi ein neu installiertes RaspianOS basierend auf Debian Buster installiert ist. Zunächst muss dieses Repository auf den RaspberryPi geclonet werden:

    git clone https://git.haw-hamburg.de/aco732/smartpot.git

Für die Konfiguration steht eine smartpot.ini Datei zur Verfügung. 

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
    stdout = 1

    #Sets the logfile
    file = smartpot.log

In der Konfiguationsdatei müssen nun der zuvor ermittelte Telegram API-Token unter chattoken und die ermittelte Chat-ID unter chatid eingetragen werden. Außerdem können das Log-Level und das Ausgabeformat der Logs festgelegt werden. 

## 3.1 manuelle Einrichtung des RaspberryPi's


Außerdem müssen über Python Paketmanager pip folgende Pakete installiert werden.

    pip install RPi.GPIO Adafruit_DHT smbus2 telepot

Desweiteren wird eine [Library für den MCP3426](https://github.com/coburnw/MCP342x) für den MCP3426 verwendet. Diese ist bereits in den Source Files enthalten.



### Einrichten von Node-RED

Das Installieren der Node-RED Editors erfolgt durch folgende Shell-Eingabe:

    bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered) --node16

Das Node-RED Dashboard wird mit folgender Eingabe installiert:

    npm i node-red-dashboard

Zusätzlich müssen in den Node-RED Einstellungen Parameter konfiguriert werden:

    cd ~/.node-red
    nano settings.js

@Line 253: „//“ entfernen

![node-red_settings](https://git.haw-hamburg.de/aco732/smartpot/-/raw/main/Dokubilder/node-red_settings.png)

Um Node-RED bei Systemstart automatisch auszuführen wird folgender Befehl verwendet:

    sudo systemctl enable nodered.service

Der Node-RED Editor ist über die IP-Adresse des Pi´s aufzurufen. Die IP wird wie folgt angezeigt:

    hostname -l

Node-RED ist per default auf Port 1880 erreichbar. Mit im vorherigen Schritt ermittelten <hostname> kann die Node-RED Konfiguration unter folgender Adresse im Interetbrowser aufgerufen werden:
Platzhalter <hostname> :

    http://<hostname>:1880

Die Node-RED Visualisierung kann nun wie folgt installiert werden:

1. Menü-Reiter auswählen
2. Palette verwalten klicken

![](https://git.haw-hamburg.de/aco732/smartpot/-/raw/main/Dokubilder/dashboard_1.png?inline=false)

3. „Dashboard“ in Suchfeld eingeben
4. Auf „Installieren“ klicken

![](https://git.haw-hamburg.de/aco732/smartpot/-/raw/main/Dokubilder/dashboard_2.png?inline=false)

Die zur Verfügung gestellte Visualisierung des Node-RED Dashboards muss nun wie folgt kopiert werden:

    cp /home/pi/smartpot/Node-Red/flows.json /home/pi/.node-red/lib/flows

Abschließend wird die flow-Datei in Node-RED importiert:

1. Menü-Reiter auswählen
2. Import klicken

![](https://git.haw-hamburg.de/aco732/smartpot/-/raw/main/Dokubilder/dashboard_3.png?inline=false)

3. Lokal auswählen
4. „SmartpotVflows.json“ wählen

![](https://git.haw-hamburg.de/aco732/smartpot/-/raw/main/Dokubilder/dashboard_4.png?inline=false)

5. Auf „Import“ klicken
6. „Übernahme (deploy)“ klicken

![](https://git.haw-hamburg.de/aco732/smartpot/-/raw/main/Dokubilder/dashboard_5.png?inline=false)


Die Visualisierung kann nun unter 

    http://<hostname>:1880/ui

erreicht werden.

## 3.2 automatische Einrichtung des RaspberryPi's via Docker

Falls Docker und Docker-Compose bereits installiert sein sollten kann dieser Schritt übersprungen werden.


### Einrichtung von Docker und Docker-Compose

Für die Einrichtung von Docker und Docker-Compose müssen folgende Befehle ausfgeführt werden.

    sudo apt-get update
    curl -sSL https://get.docker.com | sh
    sudo apt-get install docker-compose
    sudo usermod -aG docker pi

Nachdem der letzte Befehl ausfgeführt worden ist muss der Pi neugstartet werden.

   sudo reboot

### Starten der Smartpot Umgebung

Zunächst muss sichergestellt werden, dass im SmartPot Verzeichnis die smartpot.log sowie die smartpot.ini Datei vorhanden ist. Sollte dies nicht der Fall sein müssen beide Dateien erstellt werden.

    touch smartpot.log smartpot.ini

Die ini-Konfigurationsdatei muss anschließend nach Abschnitt 2 konfiguriert werden.
Aus dem smartpot Verzeichnis kann nun folgender Befehl die gesamte smartpot Umgebung gestartet werden

    docker-compose up

## 4. elektronischer Aufbau

Schaltplan des RaspberryPi Shields:

![Schaltplan](https://git.haw-hamburg.de/aco732/smartpot/-/raw/main/Platine/Bilder/schematic.png)

Die Schaltung kann an einem handelsüblichen 12V Netzteil betrieben werden. Über einen 12V/5V Linearregler wird die Betriebsspannung 
wird die Versorgnungsspannung für den RaspberryPi bereit gestellt. 

Auf dem Board ist eine dreipolige Buchsenleiste für einen DHT11 bzw DHT22 Sensor vorgesehen. Der Sensor kann einfach auf die Buchsenleiste gesteckt werden und per OneWire Protokoll ausgelesen werden.

Für den analogen Lichtsensor und den analogen Bodenfeuchtigkeitssensors ist ein 2 Kanal Delta-Sigma AD-Wandler mit I2C Interface, der MCP3426, verbaut.  

Für die Leistungsausgänge wird mit den GPIOs des RaspberryPis ein Darlington Array (ULN20003AD) angesteuert. Mit den verstärkten Ausgängen des Darlington Arrays werden drei P-Kanel Mosfets (AO3401A) angesteuert.


Das dazugehörige Layout wurde wie folgt umgesetzt:

![Layout](https://git.haw-hamburg.de/aco732/smartpot/-/raw/main/Platine/Bilder/layout.png)


### Stückliste


Position    |Bezeichnung                        | Anzahl  |Stückpreis €| Positionspreis €
------------|-----------------------------------|-------- |------------|-----------------
1           | RaspberryPi Staking Header        |1        |1,6         | 1,60
2           | ULN20003AD                        |1        |0,75        | 0,75
3           | MCP3426                           |1        |3,10        | 3,10
4           | uA78S05                           |1        |0,45        | 0,45
5           | BD204                             |1        |0,41        | 0,41
6           | AO3401A                           |3        |0,25        | 0,75
7           | Widerstand 0805 1,0               |1        |0,03        | 0,03
8           | Widerstand 0805 2,0               |1        |0,02        | 0,02
9           | Widerstand 0805 51,0              |3        |0,02        | 0,06
10          | Widerstand 0805 5k                |2        |0,03        | 0,06
11          | Widerstand 0805 10k               |3        |0,03        | 0,09
12          | Keramikkondensator 0805 100nF     |1        |0,02        | 0,02
13          | Tantalkondensator 1210 10uF       |1        |0,32        | 0,32
14          | Elektrolytkondensator 2mm 1uF     |2        |0,02        | 0,04
15          | Elektrolytkondensator 5mm 1mF     |1        |0,29        | 0,29
16          | JST XH2P ST Buchse                |3        |0,20        | 0,60
17          | JST XH4P ST Buchse                |2        |0,25        | 0,50
18          | 3fach Buchsenleiste 2,54mm        |1        |0,14        | 0,14
19          | DC Buchse 2.1mm                   |1        |1,20        | 1,20
20          | DHT11                             |1        |4,50        | 4,50
21          | Joy-It Linker Kit Lichtsensor     |1        |1,01        | 1,01
22          | Joy-it sen-Moisture Sensorkit     |1        |4,99        | 4,99
23          | Platine                           |1        |2,00        | 2,00
24          | Gesamt                            |         |            | 22,93

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

- Der Linearregler auf der Platine wird bei Betrieb mit einem 12V Netzteil und hohen Stromverbräuchen des Raspberrys sehr warm. Hier wäre eine Spannungswandlung über einen Schaltregler zu bevorzugen.

- Beim Ausschalten der Leistungsausgänge, also wenn das Gatesignal der Ausgangsmosfets (Q2, Q3, Q4) von 0V auf 12V gezogen wird. Findet die Entladung der Gatekapazität im unbelaseten Zustand über die Pullup Widerstände (R5, R6, R7) statt. Dies führt zumidest im unbelasteten Zustand zu sehr hohen Abfallszeit des Ausgangssignals. Ein Ansatz wäre kleinere Pullup Widerstände zu verwenden auf Kosten einer höheren Stromaufnahme bei eingeschaltetem Ausgang. Ein anderer Ansatz wäre die verwendung einer richtigen Mosfet Endstufe.

- Die Ausgangssignale der analog Sensoren sind bis zu 4V hoch. Der MCP3426 kann jedoch nur +-2,048V messen. Eine Lösuing wäre ein auf der Platine befindlicher 1:1 Spannungsteiler, ein anderer AD-Wandler oder besser an den AD-Wandler angepasste Sensoren.

- Eine Verbesserung des Automatisierungsgrades durch die Nutzung der Hardwareseitig implementierten Schaltfunktionen




