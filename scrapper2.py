## Implementing Scrapper to start getting Data

import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from pprint import pprint
import re

def extract_job_title_from_result(soup):
    jobs = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
      for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
          jobs.append(a["title"])
    return(jobs)


def extract_company_from_result(soup):
    companies = []
    recJobLoc = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        jobrecloc = div.find_all(name="div", attrs = {"class":"recJobLoc"})
        for jobid in jobrecloc:
            recJobLoc.append(jobid.get("id").replace("recJobLoc_", ""))
        company = div.find_all(name="span", attrs = {"class":"company"})
        if len(company) > 0:
            for b in company:
                companies.append(b.text.strip())
        else:
            sec_try = div.find_all(name="span", attrs = {"class":"result - link - source"})
            for span in sec_try:
                companies.append(span.text.strip())
    return (companies, recJobLoc)

def extract_location_from_result(soup):
  locations = []
  spans = soup.findAll("span", attrs={"class": "location"})
  for span in spans:
    locations.append(span.text)
  return(locations)

def extract_salary_from_result(soup):
  salaries = []
  qualificationKeywords = ['qualifications','qualify', 'required','requirements', 'nice to have', 'what we’re looking for','who we’re looking for']
  for div in soup.find_all(name="div", attrs={"id":"jobDescriptionText"}):
    for item in div.find_all('b'):
        print("ITEM: ",item.text)
        print(fuzz(item.text,'qualifications'))

    try:
      salaries.append(div.find("nobr").text)
    except:
      try:
        div_two = div.find(name="div", attrs={"class":"salaryText"})
        div_three = div_two.find("div")
        salaries.append(div_three.text.strip())
      except:
        salaries.append("Nothing_found")
  return(salaries)

def extract_summary_from_result(soup):
  summaries = []
  spans = soup.findAll("span", attrs={"class": "summary"})

  for span in spans:
    summaries.append(span.text.strip())
  return(summaries)


URL = "https://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=Toronto&start=10"

page = requests.get(URL)
soup = BeautifulSoup(page.text, "html.parser")
#print(extract_job_title_from_result(soup))
#print(extract_company_from_result(soup))
#print(extract_location_from_result(soup))
companyNames, indeedIdentification = extract_company_from_result(soup)
for i in range(len(companyNames)):
    cmpName = companyNames[i].replace(" ", "%20")
    cmpName = cmpName.replace("'", "%27")
    url1 = (f'https://www.indeed.com/viewjob?cmp={cmpName}&jk={indeedIdentification[i]}')
    print(url1)
    page = requests.get(url1)
    soup1 = BeautifulSoup(page.text, "html.parser")
    print(extract_salary_from_result(soup1))
    print(extract_summary_from_result(soup1))