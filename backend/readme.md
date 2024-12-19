first!!! open mysql and please run in the order create -> load ->prepare -> foreign keys.
DONT FORGET TO HAVE LATEST VERSION OF CSV'S FROM WHATSAPP!!!!!!!

If you are having problems in rerunning the files, use this code in your local SQL first:

```sql
-- Drop tables (order doesn't matter now since foreign key checks are disabled)
drop database basketball ; 

-- recreate database
create database basketball ;

-- come to directory of table initilizations and run each file
source create_tables.sql ;

```
sql does not have access to csv files other than directory that I specified. You can change your version name accordingly!!!!

change app/config.py's database values according to yours. Later it will be deleted from github and will be gitignored as it will be different in everybody.

then run the run.py

download postman app and open new request for whatever operation you wanna do.

for update and create you need to fill body in json format

TODO: create route files and from your models files, update "update", "create" functions and allow varabiles to take NULL values (look my code). **init**.py add the register_blueprint

We may further .gitignore "load_tables.sql" file to not push different directories in the future

backend/app/config.py *********************************************

```python
class Config:
    DB_HOST = "127.0.0.1"
    DB_PORT = 3306
    DB_USER = "root"
    DB_PASSWORD = "yourpassword"
    DB_NAME = "basketball"
    DEBUG = True
```
