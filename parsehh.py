from dbmigrations import *
import logging
from bs4 import BeautifulSoup as bs
import requests as r




headers = {"accept": "*/*",
           "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.2.169 Yowser/2.5 Safari/537.36"}

allsalaries=[]


def parsehh(job):
    logging.info("ok")
    global allsalaries
    numofpagestoparse=10
    allsalaries=[]
    logging.info("start parserind")
    for place in range (1, len(places_dict)+1):
        for page in range (numofpagestoparse):
            base_url = "https://hh.ru/search/vacancy?search_period=30&clusters=true&area=%s&text=%s&page=%s"%(place,job,page)
            session = r.Session()
            request = session.get(base_url, headers=headers)
            if request.status_code == 200:
                logging.info(f'url place={place}, page={page} is working okay')
                get_salarydivs(request)
            else:
                logging.warning(f'url place={place}, page={page} not working')
            #print(sum(allsalaries) / len(allsalaries))
        try:
            avg_salary=sum(allsalaries)/len(allsalaries)
            insert_salaries_and_place(job, place, int(avg_salary))
        except:
            logging.warning("division by zero")
            insert_salaries_and_place(job, place, 0)

        allsalaries = []


def get_salarydivs(request):
    soup = bs(request.content, "html.parser")
    divs = soup.find_all("div", attrs={"class": "vacancy-serp-item-body__main-info"})
    #print(divs[0].find('a', attrs={'data-qa': 'serp-item__title'}))
    parsedivsforsalary(divs)
    #print(divs[0].find( attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text)


def parsedivsforsalary(divs):
    global allsalaries
    for div in divs:
        try:
            salary=get_correct_salary(div.find(attrs={'class':'bloko-header-section-3','data-qa': 'vacancy-serp__vacancy-compensation'}).text)
            allsalaries.append(salary)
        except:
            continue



def get_correct_number(salary):
    correctsalary=''
    for i in range(len(salary)):
        if salary[i].isdigit():
            correctsalary+=salary[i]
    return int(correctsalary)


def get_correct_salary(salary):
    liste = salary.split()
    if liste[0].lower() == 'от' or liste[0].lower() == 'до':
        salary = str(get_correct_number(salary))
    else:
        salary = str(((get_correct_number(liste[0]) + get_correct_number(liste[3]))/2)*1000)
    # Transfer from EUR or USD to RUB
    if liste[-1] == 'EUR':
        salary = str(float(salary) * 71)
    elif liste[-1] == 'USD':
        salary = str(float(salary) * 63)
    return float(salary)
