### Setze die Programmiersprache auf den Interpeter python mit dem Shebang
#!/bin/python
# Importiere verschiedene Module u.a. Regex (re) und SQLite3 (sqlite3)
import sqlite3, os, sys, secrets, re

# Definiere die Klasse Person ohne Parameter
class Person:
    def __init__(self):
        # Initialisierung der Attribute bzw. Variablen mit keinem Wert (None), String ("") Integer (0) und Float (0.0) 
        self.connection = None
        self.primary_question = ""
        self.password = ""
        self.path = ""
        self.surname = ""
        self.name = ""
        self.position = ""
        self.age = 0
        self.gain = 0.0
        self.email = ""

    def create_directory(self):
        # Verzeichnis C:\M122 erstellen, falls es nicht existiert
        self.path = r"C:\M122"
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def sqlite_connect(self):
        # Pfad der Datenbank definieren
        db_path = os.path.join(self.path, "users.db")
        print("Der Pfad der Datenbank ist:", db_path)

        # Verbindung zur SQLite-Datenbank herstellen
        self.connection = sqlite3.connect(db_path)

        # Tabelle erstellen, falls sie noch nicht existiert. Die Zellen sind auf die Variablen abgestummen. Der Primarykey wird autoinkrementiert (+1)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                surname TEXT,
                name TEXT,
                position TEXT,
                age INTEGER,
                gain REAL,
                email TEXT,
                password TEXT
            )
        """)
        # Datenbankänderungen speichern
        self.connection.commit()

    def ask_question(self):
        # Frage stellen, ob ein User erstellt werden soll
        self.primary_question = input("Willst du ein User erstellen? [y/n] ")
        # Ist primary_question = y dann wird die Verzweigung der True Teil ausgeführt
        if self.primary_question == "y":
            self.surname = input("Wie ist der Vorname? ")
            self.name = input("Wie ist der Nachname? ")
            self.position = input("Was ist der Job von " + self.surname + " " + self.name +"? ")

            # Endlosschleifen bis ein richtiger Wert eingegeben wird für Alter (age) und Lohn (gain)
            while True:
                try:
                    self.age = int(input("Wie ist das Alter von " + self.surname + " " + self.name +"? "))
                    break
                except ValueError:
                    print("Gebe eine Ganzzahl für das Alter ein!")

            while True:
                try:
                    self.gain = float(input("Wie ist der Lohn von " + self.surname + " " + self.name +"? "))
                    break
                except ValueError:
                    print("Gebe eine Zahl für den Lohn ein!")
        # Ist die primary_queastion = n wird der else if Teil ausgeführt um zu Fragen ob er das Programm beenden will. Gibt er nicht y oder n ein wird eine richtige Antwort verlangt
        elif self.primary_question == "n":
            quit_program = input("Willst du das Programm beenden? [y/n] ")
            if quit_program == "y":
                sys.exit("Das Programm wird beendet")
            elif quit_program == "n":
                self.ask_question()
            else:
                print("Antworte mit y oder n")
        else:
            print("Antworte mit y oder n")

    def generate_password(self):
        # Das Passwort genrieren mit einer Länge von 8 Zeichen
        password_length = 8
        self.password = secrets.token_urlsafe(password_length)
        print("Das Passwort ist:", self.password)

    def generate_email(self):
        # E-Mail generieren
        base = f"{self.surname}.{self.name}".lower()

        # Definiierte Sonderzeichen vom Deutsch und Französisch im Namen ersetzen
        special_characters_map = {
            "ä": "ae",
            "ö": "oe",
            "ü": "ue",
            "ß": "ss",
            "Ä": "Ae",
            "Ö": "Oe",
            "Ü": "Ue",
            "é": "e",
            "è": "e",
            "ë": "e",
            "à": "a",
            "á": "a",
            "ç": "c",
            "ê": "e",
            "Ê": "E",
            "É": "E",   
            "Ê": "E",
            "Ë": "E",
            "À": "A",
            "Á": "A",
            "Ç": "C"}
        # for-Schleife durch die Zeichenkette des Namens
        for u, repl in special_characters_map.items():
            # Ersetzte aus Liste special_charactes_map mit der Kolummepostion u (Links) mit der Kolummepostion rep1 (Rechts)
            base = base.replace(u, repl)

        # Danach unerlaubte Zeichen entfernen (nur Buchstaben, Zahlen, Punkte) mit Regex
        base = re.sub(r'[^a-z0-9.]', '', base)

        # Wie viele Emails gibt es schon mit diesem Prefix? Addiere ein Integer ab 1 falls der Prefix existiert
        cursor = self.connection.execute(
            "SELECT COUNT(*) FROM users WHERE email LIKE ?",
            (base + "%@firma.net",)
        )
        count = cursor.fetchone()[0]

        if count > 0:
            self.email = f"{base}{count}@firma.net"
        else:
            self.email = f"{base}@firma.net"

        return self.email

    def save_credentials(self):
        # Useredaten in die Datenbank speichern
        self.connection.execute(
            'INSERT INTO users (surname, name, position, age, gain, email, password) VALUES (?,?,?,?,?,?,?)',
            (self.surname, self.name, self.position, self.age, self.gain, self.email, self.password)
        )
        # Datenbankänderungen speichern
        self.connection.commit()

    def print_table(self):
        # Gesamte Tabelle ausgeben
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        if not rows:
            print("Die Tabelle ist leer.")
            pass

        column_names = [description[0] for description in cursor.description]
        
        print_table_question = input("Möchtest du die gesamte Tabelle anzeigen? [y/n] ")

        # Tabelle ausgeben
        if print_table_question == "y":
            print(" | ".join(column_names))
            print("-" * 60)

            for row in rows:
                print(" | ".join(str(value) for value in row))
        elif print_table_question == "n":
            pass
        else:
            print("Antworte mit y oder n")


if __name__ == "__main__":
    # Kernprogramm startet hier
    # Klasse Person initialisieren
    p = Person()

    # Funktionen der Klasse Person aufrufen
    p.create_directory()
    p.sqlite_connect()
    p.ask_question()

    # Wenn die Antwort y ist weitere Funktione der Klasse Person aufrufen
    if p.primary_question == "y":
        p.generate_password()
        p.generate_email()
        p.save_credentials()
        print("User " + p.surname + " " + p.name + " wurde gespeichert mit E-Mail:", p.email)
        p.print_table()
        p.ask_question() 
