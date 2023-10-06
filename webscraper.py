import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from time import sleep

pd.set_option('display.max_colwidth', 255)
main_site='https://itc.gymkhana.iitb.ac.in/wncc'
main_cont=requests.get(main_site, verify=False).content

database=[]

for i in range(224,350):
    url='https://itc.gymkhana.iitb.ac.in/wncc/soc/projects/2023/project{}.html'.format(i)
    project={"Title": None, "Mentor": None, "Mentees": None, "Project_ID": None}
    print(url)
    request_content=requests.get(url, verify=False).content
    if (request_content==main_cont):
        continue
    soup=BeautifulSoup(request_content,'html.parser')

    try:
        title=soup.select_one('.project-title').text
    except:
        continue
    project['Title']=title
    mentors_block=soup.select('body > div.container-fluid > div > div.col-sm-10.col-md-8 > div:nth-child(4) > ul:nth-child(5) .lead')
    str=''
    for name in mentors_block:
        str=str+name.text.strip(" : ")+' / '
    project['Mentor']=str.strip(' / ')
    menteecount=soup.select_one('body > div.container-fluid > div > div.col-sm-10.col-md-8 > div:nth-child(4) > ul:nth-child(7) > li > p').text.strip()
    project['Mentees']=menteecount.replace('-',' to ')
    project['Project_ID']=i
    database.append(project)
    sleep(1)

with open('database.json', 'w') as f:
    json.dump(database, f)
    f.close()

df=pd.read_json(open('database.json','r'))
df.to_csv('wncc_projects.csv')

print(df.head(50))