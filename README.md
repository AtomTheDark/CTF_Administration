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

### To move the data back into another database

```cmd
mysql -u root -p ctf_new < ctf.sql
```

#### Credentials

- The first credential for your admin log in is
- User = 'admin'
- Password = 'admin'