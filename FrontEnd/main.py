# Required imports
import mysql.connector as sqltor
import os
import pickle
import hashlib

# Global Variables
script_dir = os.path.dirname(os.path.abspath(__file__))

# Made this as a function and defined above to remove redundant code
def credentials_returner():
    HOST = input("Enter Host: ")
    USER = input("Enter User: ")
    PASSWORD = input("Enter Password: ")
    return HOST, USER, PASSWORD

# connection in __main__ cuz it requires the variables to be in global so no func is used
while True:

    try: # To connect to the database
        print("========== Welcome to CTF Administrator ==========")
        cont = input("Press Enter to Continue or something to exit ^_^ .")
        if cont:
            exit()

        cred_path = os.path.join(script_dir, "..", "BackEnd", "cred.pkl")

        if os.path.isfile(cred_path):
            cont = input("Your credentials are already saved wanna re-use that? Enter to continue or m to modify the file or d to delete the file :) ")
            if cont.lower() == "d":
                os.remove(cred_path)
                print("Credentials were sucessfully deleted!")
                continue
            elif cont.lower() == "m":
                with open(cred_path,"wb") as cred_file_w:
                    HOST, USER, PASSWORD = credentials_returner()
                    pickle.dump((HOST, USER, PASSWORD), cred_file_w)
            
            else:
                with open(cred_path, "rb") as cred_file_r:
                    HOST, USER, PASSWORD = pickle.load(cred_file_r)
        else:
            cont = input("Do you wanna store your credentials to a file and use it as cache? Enter to continue or something to don't create it: ")
            if not cont:
                with open(cred_path, "wb") as cred_file_w:
                    HOST, USER, PASSWORD = credentials_returner()
                    pickle.dump((HOST, USER, PASSWORD), cred_file_w)
            else:
                HOST, USER, PASSWORD = credentials_returner()

        conn = sqltor.connect(host = HOST, user = USER, passwd = PASSWORD, autocommit = True)
        cur = conn.cursor()
        break

    except sqltor.errors.ProgrammingError: # For incorrect user or incorrect password
        print("Access denied check your credentials again like user and password !!")
        
    except sqltor.errors.DatabaseError: # For every error that raises during any execution here used as a catcher to catch host error since that is the only exception here
        print("Check your credentials especially host :) ")
         
# Main function to understand the flow
def main():
    while True:
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

            if choice in (1, 2, 3, 4):
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
            file_path = os.path.join(script_dir, "..", "BackEnd", "init_queries.sql")
            with open(file_path, "r") as init_query:
                exe_queries = init_query.read()
                cur.execute(exe_queries)

                # To remove the redundant empty lists returned by excecuting the ddl commands otherwise it will raise mysql.connector.errors.DatabaseError
                while cur.nextset():
                    cur.fetchall()
                print("Done!")

        except FileNotFoundError:
            print("File is missing please restore it via github repo: github.com/AtomTheDark/CTF_Administration")

    elif mn_ch == 2:
        while True:
            usr = input("Enter your username: ")
            psd = input("Enter your password: "); hashed_psd = hashlib.sha256(psd.encode()).hexdigest()
            cur.execute("USE ctf;")
            cur.execute(f"SELECT * FROM admins WHERE username = '{usr}' AND admin_password_hash = '{hashed_psd}'")
            place_holder_for_bool = cur.fetchall()
            if place_holder_for_bool:
                admin_init()
            else:
                print(f"Invalid Username or Password\nEntered Username is {usr}, and Password is {psd}")

    elif mn_ch == 3:
        ...

    elif mn_ch == 4: # To exit
        exit()

def admin_init():
    print("You are now logged in ^_^")

# This ensures that the program can run only when it is directly run and not imported
if __name__ == "__main__": main()