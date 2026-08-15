import mysql.connector as sqltor

while True:
    try:
        print("========== Welcome to CTF Administrator ==========")
        cont = input("Press Enter to Continue and something to exit ^_^ .")
        if cont:
            exit()
        HOST = input("Enter Host: ")
        USER = input("Enter User: ")
        PASSWORD = input("Enter Password: ")
        conn = sqltor.connect(host = HOST, user = USER, passwd = PASSWORD)
        cur = conn.cursor()
        break
    except sqltor.errors.ProgrammingError:
        print("Access denied check your credentials again like user and password !!")
        continue
    except sqltor.errors.DatabaseError:
        print("Check your credentials especially host :) ")
    

def main():
    menu()

def menu():
    print(f"========== Welcome {USER} ==========")
    print("Choose an Option :) ")
    menu_choices = """1. Something\n2. To something"""
    print(menu_choices)
    while True:
        try:
            choice = int(input("Enter your choice here! : "))
            if choice in (1,2):
                break
            else:
                print("Enter a integer within the range")
        except ValueError:
            print("Enter an integer, here try again")

if __name__ == "__main__": main()