import psycopg2
import os
from scrapper import formatted
import time

USER = os.environ.get("USER")
HOST = os.environ.get("HOST")
PASSWORD = os.environ.get("PASSWORD")


engine = psycopg2.connect(
    database="TestDB",
    user=USER,
    password=PASSWORD,
    host=HOST,
    port='5432'
)

data = formatted()
# Open a cursor to perform database operations
cur = engine.cursor()

# Retrieve query results
successes = 0
fails = 0
records = []
JobIDs = []
"""highlights = []
companyName = []
locations = []
titles = []"""
#records = cur.fetchall()
for f in data:
    print("RECORDS: ", records)
    JobIDs.append(f['JobID'])
    highlight = str(f['ValueProps']).replace("'","")
    highlights = highlight.replace('"', '')
    companyName = str(f['CompanyName']).replace("'","")
    locations = str(f['Location']).replace("'","")
    titles = str(f['Title']).replace("'","")
    records.append((f['JobID'], companyName, locations,titles, highlights))
    record = (f['JobID'], companyName, locations,titles, highlights)
    queryString = f"Insert into Jobs (jobid, company, location, title, misc) values ('{f['JobID']}','{f['CompanyName']}','{f['Location']}','{f['Title']}','{highlights}')"
    print("QUERY STRING: ", queryString)
    try:
        #queryString = "INSERT INTO Jobs (jobid, company, location, title, misc) VALUES (%s,%s,%s,%s,%s)"
        cur.executemany(queryString)# ,record)
        time.sleep(1)
        engine.commit()
        time.sleep(1)
        successes += 1
    except:
        fails += 1
    time.sleep(1)
print("Success: ", cur.rowcount)
print("Fails: ", fails)
print("Number of sites scraped: ", len(JobIDs))
print("Number of unique jobs available: ", len(set(JobIDs)))