#!/bin/bash
sudo apt install  sqlite3 -y
touch /home/morta/m122.db
sqlite3 /home/morta/m122.db "CREATE TABLE IF NOT EXISTS WORKERS (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Vorname TEXT NOT NULL,
    Name TEXT NOT NULL,
    Age INT CHECK(Age >= 0),
    Email TEXT NOT NULL,
    Job TEXT,
    Lohn INT CHECK(Lohn >= 0),
    Passwort TEXT NOT NULL
    )"


while IFS= read -n1 -r -p "Wollen sie einen neuen Mitarbeiter erstellen? Antworte mit [y]es oder [n]o" Replay && [[ $Replay != q ]] ; do
    echo $Replay
    case $Replay in
    y)  read -p "Wie ist der Vorname des Mitarbeiters? " Vorname
        read -p "Wie ist der Nachname des Mitarbeiters? " Nachname
        Email="$Vorname"."$Nachname"@firma.net""
        Email="${Email,,}"
        Email="$Email | tr -dc '[:alnum:]\n\r' | tr '[:upper:]' '[:lower:]"
        echo "Die Email von Mitarbeiter $Vorname $Nachname ist $Email"
        Passwort=$(tr -dc 'A-Za-z0-9!?%=@' < /dev/urandom | head -c 8)
        echo "Das Passwort von Mitarbeiter $Vorname $Nachname ist $Passwort"

        sqlite3 m122.db "insert into todo (Vorname,Name,Age,Email,Job,Lohn,Passwort) \
         values (\"$Vorname\",\"$Name\",\"$Age\",\"$Email"\",\"$Job"\",\"$Lohn\");"
        ;;
    n)  exit 1
        ;;
    *)  echo "Gebe y oder n ein ?"
        ;;
        esac
done