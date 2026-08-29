# Ultimate flag
It has an ultimate flag in the admin login if players stumble upon it, it might give them extra points ^_~

# Required
Please check your DBMS if there's any database named ctf if so it will be dropped and new one will be created
if you want that database to exists in a different name please execute these below commands in cmd

- Older versions of the package mysql.connector needs a important change
- That is it can't execute multi line sql commands so you have to alter the cur.execute func and add 'multi = True' argument there to make it work

## On cmd to move the data from the ctf database to a .sql file
- Replace your username with root near -u flag -p promts for the password
- It will ask the password enter it and your ctf.sql file will be in your working directory

```cmd
mysqldump -u root -p ctf > ctf.sql  
```

### Project Retrospective
**Modules Imported**
```python
mysql.connector
os
pickle
hashlib
```
***Walkthrough***
I have made a global variable called script_dir to get the absolute path of main.py

later I have used that absolute path to make a dynamic path for my backend sql file

I have used a function named credentials_returner that returns the user input values, this is done to minimise code redundancy

Now I want to create caching for my project because we can't just hand our sql server passwords to players so a caching might be a good idea
For caching I have coded everything in the __main__ to represent that I know LEGB rule

I have used a function main to initialize but later found my way across passing through multiple functions

Used a function menu to welcome users with choices

Next I proceeded to develop initializing the project by creating a .sql file which will be used to create schema objects in the server

But I faced an error: Commands aren't in sync
To tackle it I used cur.nextset() in a for loop and cleaned the environment by using cur.fetchall()

Then I proceeded to make admin page
For logging into the admin page I have put a default credential inside the .sql file itself it acts as a default credential for the first login then hosts can make multiple admin accounts for futher use and drop the default admin credential

Then I proceeded to work on dropping the database, then I found about the database inside MySQL called INFORMATION_SCHEMA this database stores all the database, tables created and much more
So I used that to fetch if the ctf database is present or not to avoid errors that may occur when dropping a database which is not present

Then I have added a conformation to delete the database

***Admin login page***
Here admins can either create,see or remove other admins well the admin page is like an infinity gauntlet but its my design

Admins can also create a competition and view all the competitions present

I have added a ULTIMATE FLAG to make this program not just a ctf administrator but rather a challenge itself

Here admins can also register teams and teams registered here reflect on the menu page and if no teams are registered it will print an respective message

#### To move the data back into another database

```cmd
mysql -u root -p ctf_new < ctf.sql
```

#### Credentials

- The first credential for your admin log in is
- User = 'admin'
- Password = 'admin'