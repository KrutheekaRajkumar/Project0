## Implementing Scrapper to start getting Data

"""
Scrapper 2 is using a different strategy to get information than scrapper 1
This is a stage level document and the dev level document is
AnalysisTextScrapped > Exploration.ipynb
"""

# ---- LIBRARIES ---- #

import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import re
import csv

#Natural Language Processing Packages
import re
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer

# List of commonly occuring stop words from http://www.nltk.org/nltk_data/
stopwords = open("AnalysisTextScrapped/english", "r")
stopwords = [word for word in stopwords]


# ---- Function to extract job titles ---- #
def extract_job_title_from_result(soup):
    jobs = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            jobs.append(a["title"])
    return(jobs)

# ---- Function to extract company names and the associated identification value ---- #
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

# ---- Function to get Location ---- #
def extract_job_locations_from_result(soup):
    div = soup.find(name="div", attrs={"class":"jobsearch-InlineCompanyRating"})
    return (div.text)

# ---- Function to identify if text in consideration is talking about required qualification ---- #
def isQualification(text):
    tokenizer = RegexpTokenizer(r'\w+')
    porter = PorterStemmer()
    keywords = ['experi','requir','qualif','skill', 'educ']
    # Cleaning text
    clean_text = []
    new_text = re.sub('\n', '', text)
    new_text = re.sub('%', '', new_text)
    new_text = re.sub('@', '', new_text)
    new_text = re.sub(r'[0-9]', '', new_text)
    new_text = new_text.lower()
    new_text = tokenizer.tokenize(new_text)
    #print(new_text)
    for nt in new_text:
        if nt in stopwords:
            pass
        else:
            clean_text.append(nt)
            #stemmedword.append(porter.stem(nt))
            if porter.stem(nt) in keywords:
                return True

# ---- Extract job requirements ---- #
def extract_job_requirements_from_result(soup):
    salaries = []
    desiredQualifications = []
    desiredQualificationsDescription = []
    desiredQualificationslists = []

    if len(desiredQualifications) == 0:
        for headers in soup.find_all(name='h1'):
            if isQualification(headers.text):
                desiredQualifications.append(headers.parent.next_sibling.text)
    elif len(desiredQualifications) == 0:
        for headers in soup.find_all(name='h2'):
            if isQualification(headers.text):
                desiredQualifications.append(headers.parent.next_sibling.text)
    else:
        for headers in soup.find_all(name='h3'):
            if isQualification(headers.text):
                desiredQualifications.append(headers.parent.next_sibling.text)

    for div in soup.find_all(name="div", attrs={"id": "jobDescriptionText"}):
        for item in div.find_all('b'):
            if isQualification(item.text):
                for tag in item.parent.next_siblings:
                    try:
                        desiredQualificationsDescription.append(tag.text)
                    except:
                        pass

    if len(desiredQualifications) < 50 and len(desiredQualificationsDescription) < 50:
        for div in soup.find_all(name="div", attrs={"id": "jobDescriptionText"}):
            for item in div.find_all("li"):
                if isQualification(item.text):
                    desiredQualificationslists.append(item.text)
        return (desiredQualificationslists)

    else:
        desiredQualifications.extend(desiredQualificationsDescription)
        if len(desiredQualifications) >= len(desiredQualificationsDescription):
            return (desiredQualifications)
        else:
            return (desiredQualificationsDescription)
        #print(desiredQualifications)
    # return(desiredQualifications)#, salaries)

# ---- Function to extract Salary from job description ---- #
def extract_salary_from_result(soup):
    salary = "None found"
    for div in soup.find_all(name="div", attrs={"id": "jobDescriptionText"}):
        for item in div.find_all("p"):
            if re.search('\$\d+', item.text):
                salary = item.text

    if re.search('\$\d+', salary) == False:
        for item in div.find_all("b"):
            if re.search('\$\d+', item.text):
                salary = item.text

    if re.search('\$\d+', salary) == False:
        for item in div.find_all("span"):
            if re.search('\$\d+', item.text):
                salary = item.text

    if re.search('\$\d+', salary) == False:
        for item in div.find_all("il"):
            if re.search('\$\d+', item.text):
                salary = item.text

    return salary

def dataIntakeClean(text):
    singleEntry = ""
    for t in text:
        t = t.replace("'","")
        t = t.replace("\n","")
        singleEntry+=t
    return (singleEntry)


def mainMethod(title):
    print(" ----- Scrapper2 Method called -----")

    # ---- Start of the  main scrapping tool ---- #
    URL = "https://www.indeed.com/jobs?q={}+%2420%2C000&l=Toronto&start=10".format(title)

    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")
    titles = extract_job_title_from_result(soup)
    companyNames, indeedIdentification = extract_company_from_result(soup)
    # Structure of data to be passed: link, title, company, location, salary, summary
    ScrappedInfoFinal = []
    for i in range(len(companyNames)):
        cmpName = companyNames[i].replace(" ", "%20")
        cmpName = cmpName.replace("'", "%27")
        url1 = (f'https://www.indeed.com/viewjob?cmp={cmpName}&jk={indeedIdentification[i]}')
        page = requests.get(url1)
        soup1 = BeautifulSoup(page.text, "html.parser")

        formatString = "'{}','{}','{}','{}','{}','{}','{}'".format(title,\
                                            str(url1),\
                                            str(titles[i].replace("'","")),\
                                            str(cmpName.replace("'","")),\
                                            dataIntakeClean(extract_job_locations_from_result(soup1)),\
                                            dataIntakeClean(extract_salary_from_result(soup1)),\
                                            dataIntakeClean(extract_job_requirements_from_result(soup1)))
        #return(formatString)
        ScrappedInfoFinal.append(formatString)
    print("Successfully scrapped {} for title: {}".format(len(ScrappedInfoFinal),title))
    return(ScrappedInfoFinal)