# SmartPot

SmartPot ist ein RaspberryPi Projekt um einen smarten Blumentopf/Gewächshaus umzusetzen. Die Software ist Python basiert und wurde auf einen RaspberryPi 3 entwickelt, sollte aber unabhängig davon auf allen RaspberryPi's mit den selben Header Pinout funktionieren.

Das Projekt umfasst einen elektronischen Teil inklusive Schaltplänen, Platinenlayout, Stücklisten und Gerberdateien, um direkt mit der Bestellung bzw. ätzen los legen zu können. Außerdem wird eine exemplarische Aufbauanleitung bereit gestellt. Die Ansteuerung erfolgt über ein an die Schaltung angepasstes Python Modul.

Der SmartPot umfasst folgende Funktionalitäten:

- ein auf den RaspberryPi steckbares Shield mit integrierterm 12V/5V Linearregler
- Anbindung eines Temperatur/Luftfeuchtigkeitssensors (DHT11/DHT22)
- Anbindung eines Bodenfeuchtigkeitssensors
- Anbindung eines Lichtsensors
- Drei schaltbare 12V/1,5A Leistungsausgänge mit PWM Unterstützung

## Einrichtung des RaspberryPi's

Es wird davon ausgegangen, dass auf dem RaspberryPi ein neu installiertes RaspianOS basierend auf Debian Buster installiert ist. Zunächst muss dieses Repository auf den RaspberryPi geclonet werden:

`git clone https://git.haw-hamburg.de/aco732/smartpot.git`

Außerdem müssen über Python Paketmanager pip folgende Pakete installiert werden.

`pip install RPi.GPIO Adafruit_DHT smbus2`

Desweiteren wird eine [Library für den MCP3426](https://github.com/coburnw/MCP342x) für den MCP3426 verwendet. Diese ist bereits in den Source Files enthalten.

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
------------|-----------------------------------|---------|------------|--------------------
24          | Gesamt                            |         |            | 22,93

(Reichelt Preise beispielhaft, Stand 06.01.22)


## Software Implementation


