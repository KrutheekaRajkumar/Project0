## Implementing Scrapper to start getting Data

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re


searchedTitle = ['Data Engineer','Data Scientist','data science']
SearchLocation = 'Ontario'
location = []
title = []

value_props = []
rating = []
companyname = []

page = requests.get((f'https://ca.indeed.com/jobs?q={searchedTitle}'.format(searchedTitle)))
#company = {'SearchedTitle':searchedTitle}

company = {} #dict(searchedTitle)
companyfinal = {}
soup = BeautifulSoup(page.text, 'html.parser')
jobids = [tag.get('id') for tag in soup.find_all(class_="unifiedRow")]


def scrape(searchedTitle, job):
    company = {}
    job = job.split('_')[1]
    #company["JobID"] = job
    eachdesc = f'https://ca.indeed.com/viewjob?jk={job}'.format(job)
    # eachdesc = f'https://ca.indeed.com/jobs?q=Data%20Engineer&vjk={job}'.format(job.split('_')[1])
    print("******** LINK ********")
    print(eachdesc)
    eachjob = requests.get(eachdesc)
    eachsoup = BeautifulSoup(eachjob.text, 'html.parser')
    try:
        cName = (eachsoup.find(class_='jobsearch-InlineCompanyRating').text).split('-')[0]
        lName = (eachsoup.find(class_='jobsearch-InlineCompanyRating').text).split('-')[1]
        company['CompanyName']=cName
        company['Location']=lName
        companyname.append(cName)
        location.append(lName)
    except:
        pass
    tName = eachsoup.find(class_='jobsearch-JobInfoHeader-title').text
    company['SearchedTitle'] = searchedTitle
    company['Title'] = tName
    title.append(tName)
    vProps = []
    desc = eachsoup.find(id='jobDescriptionText').find_all('p')
    for d in desc:
        try:
            prop = (d.find('b').text).replace("\n", "")
            if re.search('[a-zA-Z]', prop):
                vProps.append(prop)
        except:
            pass
    value_props.append(vProps)
    company['ValueProps'] = vProps
    return company

def formatted():
    companies = []
    for search in searchedTitle:
        for j in jobids:
            #company["JobID" + j] = dict(scrape(j))
            companies.append(dict(scrape(searchedTitle, j)))
    return companies
    #return company
    #companyfinal[searchedTitle] = company


"""
*** STRUCTURE OF DATA TO BE LOADED TO DB: ***
Job title Search:[
    { 
        jobid#X:
            { 
            jobid: #X,  
            jobtitle: T,
            Companies: C,
            Locations: L, 
            ValueProp: V
            }
    }, 
        jobid#Y:
            {
                ....
            }
]
"""
"""
if ("__main__"):
    pprint(formatted())
"""