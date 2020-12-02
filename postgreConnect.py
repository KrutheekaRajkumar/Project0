import psycopg2
import os
#from scrapper import formatted
import time
import datetime
from scrapper2 import mainMethod

titlesOfInterest = ['data+engineer','data+science','database+architect',\
                        'database+developer','data+analyst','BI+developer']


USER = os.environ.get("USER")
HOST = os.environ.get("HOST")
PASSWORD = os.environ.get("PASSWORD")



"""
Postgres table format: 
    CREATE TABLE INDEEDJOBS (
        id         SERIAL, 
        label      char(100)
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

def writeReport(title, report):
    try:
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        yesterday_report = "Report-{}.txt".format(yesterday)
        os.remove(yesterday_report)
    except:
        pass
    reportTitle = "Report-{}.txt".format(datetime.date.today())
    with open(reportTitle, "w+") as file_object:
        for info in report:
            file_object.write(info)
    file_object.close()

report = []
# Open a cursor to perform database operations
for title in titlesOfInterest:
    data = mainMethod(title)
    success = 0
    failed = 0
    duplicateKeyErr = 0
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
            duplicateKeyErr += 1
            failed += 1
            print("DuplicateKey")
        except psycopg2.errors.InFailedSqlTransaction as err:
            print("PROBLEMATIC ERROR: ")
            failed += 1
        engine.close()
        time.sleep(1)
    reporttitle = "------- {} -------\n".format(title)
    report.append(reporttitle)
    reportstr = "Successfully inserted: {} \n".format(success)
    report.append(reportstr)
    reportstr = ''
    reportstr = "Failed due to duplicate entries: {}\n".format(duplicateKeyErr)
    report.append(reportstr)
    reportstr = ''
    reportstr = "Total failed entries: {}\n".format(failed)
    report.append(reportstr)
    report.append("\n-------------------------------------------\n")
writeReport(title, report)

from sendDailyReport import mainMethod
mainMethod()
