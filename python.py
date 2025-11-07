#!/bin/python
import sqlite3, os, sys, secrets

class Person:
    def __init__(self, path, connection, filename):
        self.path = path
        self.connection = connection
        self.filename = filename
        self.primary_question = primary_question
        self.password = password

    def create_directory(self, path, filename):
        self.path = "C:\M122\"

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.filename = users + '.db'

        with open(os.path.join(self.path, self.filename), 'wb') as temp_file:
            temp_file.write(buff)


    def sqlite_connect(self, path):
        self.connection = sqlite3.connect(self.path+"users.db")


    def ask_question(self, primary_question, surname):
        self.primary_question = input("Willst du ein User erstellen?" [y/n])
        if self.primary_question == y:
            self.surname = input("Wie ist der Vorname?")
            self.name = input("Wie ist der Nachname?")
            self.postion = input("Was ist der Job von" +self.surname" "+self.name+"?")
            while(1):
                self.age = input("Wie ist das Alter von" +self.surname" "+self.name"?")
                    if isinstance(self.age, int) == 1:
                        break
                    else:
                        print("Gebe eine Ganzzahl ein!")
            while(1):
                self.gain = input("Wie ist der Lohn von" +self.surname" "+self.name"?")
                    if isinstance(self.gain, int) == 1:
                        break
                    else:
                        print("Gebe eine Ganzzahl ein!")
            
        elif self.primary_question == n:
            self.quit_program = input("Willst du das Programm beenden?" [y/n])
            if self.quit_program == y:
                sys.exit("Das Programm wird beendet")
            else:
                pass
        else:
            print("Antworte mit y oder n")

    def generate_password(self, password):
        password_length = 8
        self.password = secrets.token_urlsafe(password_length)
        print("Das Passwort ist"+" "+self.password)

    def save_credentials():


    def generate_email(self, surname, name):


