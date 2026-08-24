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
        print("============== Welcome to CTF Administrator ==============")
        cont = input("Press Enter to Continue or something to exit ^_^ .")
        if cont:
            exit()

        cred_path = os.path.join(script_dir, "..", "BackEnd", "cred.pkl") #It returns the dynamic path of the credentials file which is stored in the backend dir

        # This checks if the file is there, if it is there you can either modify it or delete it
        if os.path.isfile(cred_path):
            cont = input("Your credentials are already saved wanna re-use that? Press return or something to continue or m to modify the file or d to delete the file :) ")

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
    print(f"====================== Welcome {USER} ======================")

    print("Choose an Option :) ")

    menu_choices = """1. Initialize for the first time\n2. Admin login \n3. Dropping the database\n4. To Exit"""

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

                print("Successfully created all the schemas required for the ctf;\n----------------------------------------------------------")

        except FileNotFoundError:
            print("File is missing please restore it via github repo: github.com/AtomTheDark/CTF_Administration")

    # To log in as admin and add other admins and challenges
    elif mn_ch == 2: 

        while True:
            exists,usr,psd = admin_auth()

            if exists:
                admin_init(usr)
            else:
                print(f"Invalid Username or Password\nEntered Username is {usr}, and Password is {psd}")

    elif mn_ch == 3:

        cur.execute(
            """SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.SCHEMATA
            WHERE SCHEMA_NAME = 'ctf';"""
        )

        exists, = cur.fetchone()

        if exists:
            cur.execute("DROP DATABASE ctf;")
            print("Successfully dropped the database !_!")
        else:
            print("There is no database to delete !_!")

        exit()

    # To exit
    elif mn_ch == 4: 
        exit()

def admin_auth():
    usr = input("Enter your username: ")
    psd = input("Enter your password: "); hashed_psd = hashlib.sha256(psd.encode()).hexdigest()
    cur.execute("USE ctf;")
    cur.execute(f"SELECT * FROM admins WHERE username = '{usr}' AND admin_password_hash = '{hashed_psd}'")
    exists = cur.fetchone()
    return exists,usr,psd

# For admin privileges
def admin_init(usr):
    print("You are now logged in ^_^")
    while True:
        print("----------------------------------------------------------")
        print("1. To add new admins\n2. To see all the admins\n3. Delete admins\n4. To create a competition\n5. To exit")

        try:
            admin_ch = int(input("Enter a choice to proceed: "))

            if admin_ch == 1:
                upt_admin()

            elif admin_ch == 2:
                see_admins()
            
            elif admin_ch == 3:
                admin_rm()

            elif admin_ch == 4:
                comp_init(usr)

            elif admin_ch == 5:
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

    if admins_to_update != 0:
        print("Successfully added admins <3 ")
    else:
        print("No new admins were added...")

# To see admins currently present in the server
def see_admins():
    cur.execute("SELECT * FROM admins;")
    admin_data = cur.fetchall()

    for admin_id, username, email, admin_password_hash, created_at in admin_data: # the variable admin_password_hash was left out intentionally to protect password you can print them if you want
        print(
            f"admin id = {admin_id}, username = {username}, email = {email}, created at = {created_at}"
        )

# To remove admin accounts
def admin_rm():
    while True:

        try:
            print("Do you want to remove other admins or do you want to remove the default login credentials")
            print("1. To remove other admins\n2. To remove the default login credential")
            admin_ch = int(input())
            break

        except ValueError:
            print("Enter a integer please !")

    if admin_ch == 1:
        cur.execute("DELETE FROM admins;")
        cur.execute("ALTER TABLE admins AUTO_INCREMENT = 1;") # To reset the AUT0_INCREMENT to 1
        cur.execute(
            """INSERT INTO admins(username,email,admin_password_hash)
    VALUES ("admin","admin@ctf.com","8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918");"""
        )
        print("Deleted admins defaulted to default admin login credentials")

    elif admin_ch == 2:
        cur.execute("SELECT * FROM admins WHERE admin_id_pk = 1;")
        exists = cur.fetchone()

        if exists:
            cur.execute("DELETE FROM admins WHERE admin_id_pk = 1;")
        else:
            print("There is no default admin to delete :( ")

def comp_init(usr):
    
    comp_name = input("Enter the competition name: ")
    comp_description = input("Enter the competition's description: ")
    comp_starting_time = input("Enter competition's starting time: format:(YYYY-MM-DD HH-MM-SS): ")
    comp_ending_time = input("Enter competition's ending time: format:(YYYY-MM-DD HH-MM-SS): ")
    comp_status = input("Enter competition's status: ")
    cur.execute(f"SELECT admin_id_pk FROM admins WHERE username = '{usr}'")
    admin_id, = cur.fetchone()
    cur.execute(
        f"""INSERT INTO competitions(competition_name,competition_description,admin_id_fk,start_time,end_time,competition_status)
        VALUES
        ('{comp_name}','{comp_description}',{admin_id},'{comp_starting_time}','{comp_ending_time}','{comp_status}');"""
    )

# This ensures that the program can run only when it is directly run and not imported
if __name__ == "__main__": main()