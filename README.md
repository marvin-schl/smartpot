# SmartPot

SmartPot ist ein RaspberryPi Projekt um einen smarten Blumentopf/Gewächshaus umzusetzen. Die Software ist Python basiert und wurde auf einen RaspberryPi 3 entwickelt, sollte aber unabhängig davon auf allen RaspberryPi's mit den selben Header Pinout funktionieren.

Das Projekt umfasst einen elektronischen Teil inklusive Schaltplänen, Platinenlayout, Stücklisten und Gerberdateien, um direkt mit der Bestellung bzw. ätzen los legen zu können. Außerdem wird eine exemplarische Aufbauanleitung bereit gestellt. Die Ansteuerung erfolgt über ein an die Schaltung angepasstes Python Modul.

Der SmartPot umfasst folgende Funktionalitäten:

- ein auf den RaspberryPi steckbares Shield mit integrierterm 12V/5V Linearregler
- Anbindung eines Temperatur/Luftfeuchtigkeitssensors (DHT11/DHT22)
- Anbindung eines Bodenfeuchtigkeitssensors
- Anbindung eines Lichtsensors
- Drei schaltbare 12V/1,5A Leistungsausgänge mit PWM Unterstützung

## Einleitung

Bei diesem Projekt handelt es sich um die Realisierung eines intelligenten Blumentopfes, der die für 
Pflanzen wichtigen Parameter (Temperatur, Luft-/Bodenfeuchtigkeit und Lichtstärke) misst und 
informativ zur Verfügung stellt. Die Visualisierung der Informationen kann auf der Homepage des 
Raspberry Pi´s aufgerufen und analysiert werden. Alternativ können die Sensorwerte auch per 
Telegram manuell erfragt werden.
Außerdem können für diese Parameter kritische Schwellenwerte programmiert werden, bei deren 
Unter- bzw. Überschreiten eine Benachrichtigung über Telegram abgeschickt wird.
Im Folgenden wird die Umsetzung des Projektes detailliert dokumentiert, sodass mit Hilfe dieser 
Anleitung ein Nachbau des SmartPots möglich wird.

## Projektidee

Die Idee einen intelligenten Blumentopf zu entwickeln wurde durch zahlreiche Anleitungen aus dem 
Web inspiriert.[Link](https://tutorials-raspberrypi.de/automatisches-raspberry-pi-gewaechshaus-selber-bauen/)

Der modulare Aufbau dieses Projektes eignet sich sehr gut für Gruppenarbeiten und kann dem 
jeweiligen Wissensstand (Programmierung vom Raspberry Pi) durch Variation der 
Funktionskomplexität angepasst werden.

Die erste Version des SmartPots beinhaltet folgende Funktionen:

Die erste Version des SmartPots beinhaltet folgende Funktionen:
1) _Temperatur_ messen, auslesen und ausgeben
2) _Luftfeuchtigkeit_ messen, auslesen und ausgeben
3) _Bodenfeuchtigkeit_ messen, auslesen und ausgeben
4) _Lichtstärke_ messen, auslesen und ausgeben
5) Kommunikation in Telegram Web
6) Node-RED Visualisierung der Sensorwerte (historisch/live)

In zukünftigen Versionen könnten je nach Wissensstand und finanziellen Mitteln weitere Funktionen 
wie z.B. automatische Bewässerung, Lichtregelung sowie Belüftung realisiert werden.

## Einrichtung des RaspberryPi's

Es wird davon ausgegangen, dass auf dem RaspberryPi ein neu installiertes RaspianOS basierend auf Debian Buster installiert ist. Zunächst muss dieses Repository auf den RaspberryPi geclonet werden:

`git clone https://git.haw-hamburg.de/aco732/smartpot.git`

Außerdem müssen über Python Paketmanager pip folgende Pakete installiert werden.

`pip install RPi.GPIO Adafruit_DHT smbus2`

Desweiteren wird eine [Library für den MCP3426](https://github.com/coburnw/MCP342x) für den MCP3426 verwendet. Diese ist bereits in den Source Files enthalten.

## Einrichten Node-RED Editors

Das Installieren der Node-RED Editors erfolgt durch folgende Shell-Eingabe:

`bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered) --node16`

Das Node-RED Dashboard wird mit folgender Eingabe installiert:

`npm i node-red-dashboard`

Zusätzlich müssen in den Node-RED Einstellungen Parameter konfiguriert werden:

`cd ~/.node-red`

`nano settings.js`

@Line 253: „//“ entfernen

![node-red_settings](https://git.haw-hamburg.de/aco732/smartpot/-/blob/main/Dokubilder/node-red_settings.png)

Um Node-RED bei Systemstart automatisch auszuführen wird folgender Befehl verwendet:

`sudo systemctl enable nodered.service`

Der Node-RED Editor ist über die IP-Adresse des Pi´s aufzurufen. Die IP wird wie folgt angezeigt:

`hostname -l`

Anschließend wird der folgende Link im Browser aufgerufen und die IP-Adresse ersetzt den 
Platzhalter <hostname> :

`http://<hostname>:188`

## elektronischer Aufbau

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
********24          | Gesamt                            |         |            | 22,93

(Reichelt Preise beispielhaft, Stand 06.01.22)


## Software Implementation



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


## Ausblick

Hier werden bekannte Schwächen der aktuellen Version des SmartPots sowies des dazugehörige Shield aufgelistet, welche in folgenden Versionen überarbeitet werden sollten.

- Der Linearregler auf der Platine wird bei Betrieb mit einem 12V Netzteil und hohen Stromverbräuchen des Raspberrys sehr warm. Hier wäre eine Spannungswandlung über einen Schaltregler zu bevorzugen.

- Beim Ausschalten der Leistungsausgänge, also wenn das Gatesignal der Ausgangsmosfets (Q2, Q3, Q4) von 0V auf 12V gezogen wird. Findet die Entladung der Gatekapazität im unbelaseten Zustand über die Pullup Widerstände (R5, R6, R7) statt. Dies führt zumidest im unbelasteten Zustand zu sehr hohen Abfallszeit des Ausgangssignals. Ein Ansatz wäre kleinere Pullup Widerstände zu verwenden auf Kosten einer höheren Stromaufnahme bei eingeschaltetem Ausgang. Ein anderer Ansatz wäre die verwendung einer richtigen Mosfet Endstufe.

- Die Ausgangssignale der analog Sensoren sind bis zu 4V hoch. Der MCP3426 kann jedoch nur +-2,048V messen. Eine Lösuing wäre ein auf der Platine befindlicher 1:1 Spannungsteiler, ein anderer AD-Wandler oder besser an den AD-Wandler angepasste Sensoren.





