import psycopg2
import os
#from scrapper import formatted
import time
from scrapper2 import mainMethod
titlesOfInterest = ['data+engineer','data+science','database+architect',\
                        'database+developer','data+analyst','BI+developer']


#titlesOfInterest = ['data+analyst']
USER = os.environ.get("USER")
HOST = os.environ.get("HOST")
PASSWORD = os.environ.get("PASSWORD")

"""
Postgres table format: 
    CREATE TABLE INDEEDJOBS (
        id              SERIAL, 
        url        char(10485760),
        title      varchar(50) NOT NULL,
        company    varchar(100) NOT NULL,
        location   varchar(100), 
        salary     varchar(50),
        summary    varchar(10485760),
        timestamp timestamp default current_timestamp,
        PRIMARY KEY(id ,url)
    );
"""

# Open a cursor to perform database operations
for title in titlesOfInterest:
    data = mainMethod(title)
    success = 0
    failed = 0
    duplicateKeyErr = 0
    print("********************************")
    print("Title being added: {}".format(title))
    for entry in data:
        engine = psycopg2.connect(
            database="TestDB",
            user=USER,
            password=PASSWORD,
            host=HOST,
            port='5432'
        )
        time.sleep(2)
        cur = engine.cursor()
        try:
            query = "INSERT INTO INDEEDJOBS (field, url, title, company, location, salary, summary) VALUES ({})".format(entry)
            cur.execute(query)
            time.sleep(1)
            engine.commit()
            success += 1
        except psycopg2.errors.IntegrityError as err:
            # print the pgcode and pgerror exceptions
            if err.pgcode == 23505:
                duplicateKeyErr += 1
            failed += 1
            print("DuplicateKey")
        except psycopg2.errors.InFailedSqlTransaction as err:
            print("PROBLEMATIC ERROR: ")
            failed += 1
        engine.close()
        time.sleep(1)

    print("{} entries made for {} ".format(success, title))
    print("{} entries failed for {} ".format(failed, title))
