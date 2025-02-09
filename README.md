# Flugrobotik_WS202425

## Installation

- ROS, crazyflies installieren
- [Fields2Cover]() installieren (Voraussetzung für `F2CRoute.py`)
- Projekt bauen: `colcon build`

## Auswahl von Algorithmus

- Andere Unterklasse von RoutePlanner in main.py nutzen, um Positionen des Pfads für `drone.move_to()` zu erzeugen.
- Projekt bauen: `colcon build`

## Ausführen von Algorithmen

- Sicherstellen, dass `ID`, `Type`, `Backend`, `Channel` und 'Pfad zu `arena.json`' korrekt definiert sind

### Ausführen mit Drohne über ROS:

- Drohne aktivieren
- Drohne an Startposition (0,0) platzieren
- CrazyRadio einstecken
- ROS-Framework starten: `launch-hardware`
- Skript starten: `ros2 run roboss roboss`

### Ausführen mit Webots über ROS

*Funktioniert nicht?*
- ROS-Framework starten: `launch-webots`
- Skript starten: `ros2 run roboss roboss`

### Ausführen mit Webots direkt

*Funktioniert nicht?*
- Skript starten: `webots-controller main.py`

