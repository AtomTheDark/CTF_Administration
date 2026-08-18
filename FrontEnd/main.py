# Required imports
import mysql.connector as sqltor
import os

# connection in __main__ cuz it requires the variables to be in global so no func is used
while True:

    try:
        print("========== Welcome to CTF Administrator ==========")
        cont = input("Press Enter to Continue or something to exit ^_^ .")
        if cont:
            exit()
        HOST = input("Enter Host: ")
        USER = input("Enter User: ")
        PASSWORD = input("Enter Password: ")
        conn = sqltor.connect(host = HOST, user = USER, passwd = PASSWORD, autocommit = True)
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

    menu_choices = """1. Initialize for the first time\n2. Admin login \n3. Team login\n4. To Exit"""

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

# Log them in according to their roles and init the schema
def init(mn_ch):

    # To initialize required db, tables, and relations within it
    if mn_ch == 1:

        # Used try-except to make sure the file is present helps to reduce the occurence of exceptions
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, "..", "BackEnd", "init_queries.sql")
            with open(file_path, "r") as init_query:
                exe_queries = init_query.read()
                cur.execute(exe_queries)
                print("Done!")

        except FileNotFoundError:
            print("File is missing please restore it via github repo CTF_Administration.")

    if mn_ch == 2:
        ...

    if mn_ch == 3:
        ...

    if mn_ch == 4:
        exit()

# This ensures that the program can run only when it is directly run and not imported
if __name__ == "__main__": main()