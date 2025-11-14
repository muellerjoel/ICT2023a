
if __name__ == "__main__":
        
    p = Person()

    p.create_directory()
    p.sqlite_connect()
    p.ask_question()
    p.generate_password()
    p.save_credentials()
    p.generate_email()