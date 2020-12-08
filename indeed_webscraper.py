import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}

    url=f'https://in.indeed.com/jobs?q=web+developer&l=mumbai&start={page}'
    re=requests.get(url,headers)
    soup = BeautifulSoup(re.content, 'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('div', class_ = 'jobsearch-SerpJobCard')
    for div in divs:
        title = div.find('a').text.strip()
        company = div.find('span' , class_ ='company').text.strip()
        try:
            salary = div.find('span',class_='salaryText').text.strip()
        except:
            salary = ''
        summary = div.find('div',{'class' : 'summary'}).text.strip().replace('\n','')
        job ={
            'title': title,
            'company': company,
            'salary':salary,
            'summary':summary
        }
        joblist.append(job)
    return

joblist = []
for i in range(0,40,10):
    print(f'Getting page, {i}')
    c = extract(0)
    transform(c)

# print(len(joblist))
# print(joblist)

df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('jobs.csv')
