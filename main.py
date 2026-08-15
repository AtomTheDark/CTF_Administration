# Required imports
import mysql.connector as sqltor

# connection in __main__ cuz it requires the variables to be in global so no func is used
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
        

    except sqltor.errors.DatabaseError:
        print("Check your credentials especially host :) ")
        
    
# Main function to understand the flow
def main():
    mn_ch = menu()
    init(mn_ch)

# Menu function that return the val
def menu():
    print(f"========== Welcome {USER} ==========")
    print("Choose an Option :) ")
    menu_choices = """1. Initialize for the first time\n2. Admin login \n3. Team login"""
    print(menu_choices)

    while True:
        try:
            choice = int(input("Enter your choice here! : "))

            if choice in (1,2,3):
                return choice
            else:
                print("Enter a integer within the range")

        except ValueError:
            print("Enter an integer, here try again")

# Log them in according to their roles
def init(mn_ch):
    if mn_ch == 1:
        db_cred_query = """CREATE DATABASE IF NOT EXISTS ctf;"""
        cur.execute(db_cred_query)

    if mn_ch == 2:
        ...

    if mn_ch == 3:
        ...

if __name__ == "__main__": main()