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

        cred_path = os.path.join(script_dir, "..", "BackEnd", "cred.pkl") #It returns the dynamic path of the credentials file which is stored in the backend dir

        # This checks if the file is there, if it is there you can either modify it or delete it
        if os.path.isfile(cred_path):
            cont = input("Your credentials are already saved wanna re-use that? Enter to continue or m to modify the file or d to delete the file :) ")

            # For deleting and modifying the credential file
            if cont.lower() == "d":
                os.remove(cred_path)
                print("Credentials were sucessfully deleted!")
                continue
            elif cont.lower() == "m":
                with open(cred_path,"wb") as cred_file_w:
                    HOST, USER, PASSWORD = credentials_returner()
                    pickle.dump((HOST, USER, PASSWORD), cred_file_w)

            # This will read the file and updates the variable for login
            else:
                with open(cred_path, "rb") as cred_file_r:
                    HOST, USER, PASSWORD = pickle.load(cred_file_r)
        else:
            # This asks your permission to create a new file to store your credentials to a file to use it again and again
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

    # To log in as admin and add other admins and challenges
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

    # To exit
    elif mn_ch == 4: 
        exit()

# For admin privileges
def admin_init():
    print("You are now logged in ^_^")
    print("1. To alter admin credentials and add new admins\n2. To exit")
    while True:
        try:
            admin_ch = int(input("Enter a choice to proceed: "))
            if admin_ch == 1:
                upt_admin()
            elif admin_ch == 2:
                exit()
                
        except ValueError:
            print("Please enter a integer value! ")

# To add admins
def upt_admin():
    while True:
        try:
            admins_to_update = int(input("Enter how many admins to add: "))
            for _ in range(admins_to_update):
                admn_usr = input("Enter the admin's username: ")
                admn_email = input("Enter the admin's email address: ")
                admn_psd = input("Enter the admin's password: "); hashed_admn_psd = hashlib.sha256(admn_psd.encode()).hexdigest()
                cur.execute(
                    f"""INSERT INTO admins(username,email,admin_password_hash)
                    VALUES
                    ('{admn_usr}','{admn_email}','{hashed_admn_psd}');"""
                )
            break
        except ValueError:
            print("Please enter a int value here :<")
    print("Successfully added admins")

# This ensures that the program can run only when it is directly run and not imported
if __name__ == "__main__": main()