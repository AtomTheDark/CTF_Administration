# Required
Please check your DBMS if there's any database named ctf if so it will be dropped and new one will be created
if you want that database to exists in a different name please execute these below commands in cmd

## On cmd
- Replace your username with root near -u flag

```cmd
mysqldump -u root -p ctf > ctf.sql  
```

### To move the data

```cmd
mysql -u root -p ctf_new < ctf.sql
```