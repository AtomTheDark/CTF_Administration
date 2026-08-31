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

    menu_choices = """1. Initialize for the first time\n2. Admin login \n3. Dropping the database\n4. Team login\n5. To see all the teams registered\n6. To exit"""
    print(menu_choices)

    while True:

        try:
            choice = int(input("Enter your choice here! : "))

            if choice in (1, 2, 3, 4, 5, 6):
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

                print("----------------------------------------------------------\nSuccessfully created all the schemas required for the ctf;\n----------------------------------------------------------")

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

    # To check whether there is a database named ctf and if so delete it else it will print a message stating that there is no database to delete
    elif mn_ch == 3:

        # Apparently this database contains all the meta-data, which is pretty wild!!!!
        cur.execute(
            """SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.SCHEMATA
            WHERE SCHEMA_NAME = 'ctf';"""
        )

        # It receives the value as well as unpacks it like if i just use exists the result will be: (data,) using comma after it unpacks it and just gives us the data
        exists, = cur.fetchone()

        if exists:
            del_ch = "N"
            del_ch = input("Do you want to delete the database?\nThis is a one way process once deleted the data can't be recovered: (y/N): ")

            # This prevents from accidental dropping of the database
            if del_ch.lower() == "y":
                cur.execute("DROP DATABASE ctf;")
                print("Successfully dropped the database !_!")
                print("Please re-initialize before using the CTF ADMINISTRATOR")
            else:
                print("Process aborted")

        else:
            print("There is no database to delete !_!")

        exit()

    # To log in as a team
    elif mn_ch == 4:

        team_auth()

    # To see potential rivals lol
    elif mn_ch == 5:

        cur.execute("USE ctf;")
        disp_teams()

    # To exit
    elif mn_ch == 6: 
        exit()

# To authenticate admins and passout the username to multiple functions
def admin_auth():

    usr = input("Enter your username: ")
    psd = input("Enter your password: "); hashed_psd = hashlib.sha256(psd.encode()).hexdigest()
    cur.execute("USE ctf;")
    cur.execute(f"SELECT * FROM admins WHERE username = '{usr}' AND admin_password_hash = '{hashed_psd}'")
    exists = cur.fetchone()

    return exists,usr,psd
    # The administrator login intentionally contains an SQL injection vulnerability as part of the CTF's attack surface.

# For admin privileges
def admin_init(usr):

    print("You are now logged in ^_^")

    while True:
        print("----------------------------------------------------------")
        print(f"============== Welcome {usr} ==============")
        print("1. To add new admins\n2. To see all the admins\n3. Delete admins\n4. To create a competition\n5. To see all the registered competitions\n6. Ultimate Flag\n7. To register teams\n8. To exit")

        try:
            admin_ch = int(input("Enter a choice to proceed: "))

            if admin_ch == 1:
                upt_admin() # To add admins

            elif admin_ch == 2:
                see_admins() # To see admins
            
            elif admin_ch == 3:
                admin_rm() # To remove admins

            elif admin_ch == 4:
                comp_init(usr) # To initiate a competition

            elif admin_ch == 5:
                see_comps() # To see all the competitions

            elif admin_ch == 6:
                # Its just an easter egg for my program players can find using sqli and if players entered it they might get an bonus, i mean who knows ¯\_(ツ)_/¯
                # this flag here represents google plus code for Santhanam Vidhyalaya
                mod_ult_flag()

            elif admin_ch == 7:
                reg_team() # To register teams                    

            elif admin_ch == 8:
                exit()

            # Catches invalid choice
            else:
                print("Invalid choice")
                
        except ValueError:
            print("Please enter a integer value! ")

# To add admins
def upt_admin():
    while True:

        try:
            admins_to_update = int(input("Enter how many admins to add: "))

            # Used underscore here as a variable/identifier cuz im a programmer, lol
            for _ in range(admins_to_update):
                admn_usr = input("Enter the admin's username: ")
                admn_email = input(f"Enter the {admn_usr}'s email address: ")
                admn_psd = input(f"Enter the {admn_usr}'s password: "); hashed_admn_psd = hashlib.sha256(admn_psd.encode()).hexdigest()

                cur.execute(
                    """INSERT INTO admins(username,email,admin_password_hash)
                    VALUES
                    (%s,%s,%s);""",(admn_usr,admn_email,hashed_admn_psd)
                )

            # break is implemented here to break the while True loop
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

    for admin_id, username, email, _admin_password_hash, created_at in admin_data: # the variable admin_password_hash was left out intentionally to protect password you can print them if you want
        print("----------------------------------------------------------")
        print(
            f"admin id = {admin_id}, username = {username}, email = {email}, created at = {created_at}"
        )

# To remove admin accounts
def admin_rm():
    while True:

        # Used a menu kind of thing here to remove the default login cred and to remove all other admins
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

        # To reinsert the default admin credential
        cur.execute(
            """INSERT INTO admins(username,email,admin_password_hash)
    VALUES ("admin","admin@ctf.com","8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918");"""
        )

        print("Deleted admins defaulted to default admin login credentials")

    # I have included this option to prevent players from knowing that there is a admin cred if the host want to remove it they can here
    elif admin_ch == 2:

        cur.execute("SELECT * FROM admins WHERE admin_id_pk = 1;")
        exists = cur.fetchone()

        print("----------------------------------------------------------")
        if exists:
            cur.execute("DELETE FROM admins WHERE admin_id_pk = 1;")
            print("Successfully deleted the default login credential")
        else:
            print("There is no default admin to delete :( ")

# To create competition
def comp_init(usr):
    
    comp_name = input("Enter the competition name: ")
    comp_description = input("Enter the competition's description: ")
    comp_starting_time = input("Enter competition's starting time: format:(YYYY-MM-DD HH:MM:SS): ")
    comp_ending_time = input("Enter competition's ending time: format:(YYYY-MM-DD HH:MM:SS): ")
    comp_status = input("Enter competition's status: ")

    # To get the admin id of the logged in host
    cur.execute(f"SELECT admin_id_pk FROM admins WHERE username = '{usr}'")

    admin_id, = cur.fetchone()

    cur.execute(
        """INSERT INTO competitions(competition_name,competition_description,admin_id_fk,start_time,end_time,competition_status)
        VALUES
        (%s,%s,%s,%s,%s,%s);"""
        ,(comp_name,comp_description,admin_id,comp_starting_time,comp_ending_time,comp_status)
    )

# To see all the competitions that are going to happen or happened in the past which was conducted via this program
def see_comps():

    cur.execute(
        """SELECT C.*, A.username
        FROM competitions C, admins A
        WHERE C.admin_id_fk = A.admin_id_pk;"""
    )
    comps = cur.fetchall()

    for competition_id_pk, competition_name, competition_description, _admin_id_fk, start_time, end_time, competition_status, created_at, admin_user in comps: # _admin_id_fk is left out intentionally

        print("----------------------------------------------------------")
        print(
            f"Competition id: {competition_id_pk}\nCompetition name: {competition_name}\nCompetition description: {competition_description}\
                \nCompetition admin: {admin_user}\nCompetiton starting time: {start_time}\ncompetition ending time: {end_time}\
                \nCompetition status: {competition_status}\nCompetition creation time: {created_at}"
        )

# To register teams with their password so that players can login according to their teams
def reg_team():

    while True:

        try:
            team_cnt = int(input("Enter how many teams you want to register: "))

            # Same as there cuz im a programmer
            for _ in range(team_cnt):

                team_name = input("Enter the team's name: ")
                team_password = input("Enter the team's password: "); team_password_hashed = hashlib.sha256(team_password.encode()).hexdigest()

                cur.execute(
                    """INSERT INTO teams(team_name, team_password_hash)
                    VALUES
                    (%s,%s);"""
                    ,(team_name,team_password_hashed)
                )

            break
        
        except ValueError:
            print("Please enter an integer value")

# To display all the teams which are registed in the admin menu
def disp_teams():
    cur.execute("SELECT team_name FROM teams;")
    teams = cur.fetchall()

    if teams:
        for team, in teams:
            print("----------------------------------------------------------")
            print(team)
    else:
        print("----------------------------------------------------------")
        print("No teams are registered")

def mod_ult_flag():
    print("----------------------------------------------------------")
    print("Here you can add many ultimate flags\nThe default one is: SV{8RJP+X8}")
    ch = "n"
    ch = input("Do you want to edit the ultimate flag? (Y/n): ")
    if ch in "Yy":
        ult_flag = input("Enter the Ultimate flag: ")
        cur.execute("INSERT INTO ultimate_flags VALUES (%s)",(ult_flag,))

def team_auth():

    while True:
        team_name = input("Enter team's name: ")
        team_psd = input("Enter team's password: "); team_psd_hashed = hashlib.sha256(team_psd.encode()).hexdigest()

        cur.execute("USE ctf;")
        cur.execute("SELECT * FROM teams WHERE team_name = %s AND team_password_hash = %s",(team_name,team_psd_hashed))
        exists = cur.fetchone()

        if exists:
            team_init(team_name)
            break
        else:
            print(f"Invalid Team name or Password\nEntered Username is {team_name}, and Password is {team_psd}")


# To login via team credentials
def team_init(team_name):
    print("----------------------------------------------------------")
    print(f"============== Welcome {team_name} ==============")
    print("1. To register players")

    while True:
        try:
            tm_ch = int(input("Enter your choice: "))

            if tm_ch == 1:
                upt_players()

        except ValueError:
            print("Please enter a numerical value ╰（‵□′）╯")

def upt_players():
    while True:

        try:
            players_to_update = int(input("Enter how many players to add: "))

            # Same as upt_admin()
            for _ in range(players_to_update):
                player_name = input("Enter the player's name: ")
                player_username = input(f"Enter the {player_name}'s username: ")
                player_passwd = input(f"Enter the {player_name}'s password: "); hashed_player_passwd = hashlib.sha256(player_passwd.encode()).hexdigest()

                cur.execute(
                    """INSERT INTO players(player_name,player_username,player_passwd_hash)
                    VALUES
                    (%s,%s,%s)""",(player_name,player_username,hashed_player_passwd)
                )

            # break is implemented here to break the while True loop
            break

        except ValueError:
            print("Not a valid choice !!!")

    if players_to_update != 0:
        print("Successfully added all the players :)")
    else:
        print("No new players were added !!!")


# This ensures that the program can run only when it is directly run and not imported
if __name__ == "__main__": main()