### Setzungssystem

## Installation

Um das Setzungssystem benutzen zu können, wird Python benötigt. Das System wurde auf Python 3.14.0 geschrieben, also ist das die geeignetste Version. Zuerst sollte das GitHub repository geklont werden (also so kopiert, dass Änderungen einfach per Klick synchronisiert werden). Dazu sollte auch Git installiert sein. 

python3 --version 
git --version

Dann klonen:

git clone https://github.com/RobinMueller152/Setzungssystem.git
cd Setzungssystem

Dann ist es am besten, in eine virtual einvironment (venv) zu wechseln, um dort alle benötigten Packages zu installieren:

python3 -m venv venv

Hinweis: Manchmal ist der command auch python statt python3 etc

Dann aktivieren:
Mac/Linux:
source venv/bin/activate

Windows:
venv\Scripts\activate

Dann werden die Packages installiert, dafür gibt es die Datei requirements.txt
pip3 install -r requirements.txt

Jetzt ist das Paket bereit zum Starten!

Nutzung:
1. Kopiere eine CSV-Datei (Comnma Separated Values) in den Ordner INPUT (Google Sheets: Download > CSV)
2. Kopiere den Dateipfad (z.B. INPUT/Exampleinput.csv)
3. Füge das im Dokument oben bei inputname ein
4. Optional: Ändere die darunterstehenden Parameter je nach Gegebenheiten:
- min_rooms: Minimal zu füllende Räume 
- max_rooms: Maximal zu füllende Räume
5. Im Terminal: python3 Setzungssystem.py (Nach den Änderungen erst die Datei speichern, dann notfalls im Terminal die obigen Commands erneut ausführen, wenn noch Packages fehlen etc. Notfalls nach Fehlermeldungen gehen.)
6. In OUTPUT erscheint Setzung.CSV. Die Datei enthält die Setzung und ist mit jedem Tabellenprogramm lesbar (bei Excel muss man sich aber manchmal noch durch Warnungen klicken), man kann sie aber auch als Textdatei auslesen, dann ist nur die Formatierung etwas mäßig.

Fertig! Viel Spaß!

P.S.: per python3 Testdaten.py können Testdaten erstellt werden, es empfiehlt sich, alles vorab einmal mit solchen zu testen, ehe es ernst wird :) 
