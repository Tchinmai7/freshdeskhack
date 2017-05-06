from bs4 import BeautifulSoup
import dryscrape
import re
import string
import freshdeskhack.rake as rake
import json
from operator import itemgetter, attrgetter, methodcaller
def get_jobs(url):
    ret = { }
    jobs = []
    rake_object = rake.Rake("/root/freshack/Jobscraper/freshdeskhack/SmartStoplist.txt", 3, 2, 1)
    dryscrape.start_xvfb()
    session = dryscrape.Session()
    session.visit(url)
    html_page = session.body()
    soup = BeautifulSoup(html_page, 'lxml')
    master_tag = soup.find_all("div",class_="fd-posdesc")

    for tag in master_tag:
        job = { }
        job["title"] = tag.h3.string
        div_list = tag.find_all("div")
        job_desc = ""
        for childdiv in div_list:
            text = childdiv.string
            if text:
                job_desc = job_desc+text

        keywords = rake_object.run(job_desc)
        words = []
        for word in keywords:
            if "year" not in word[0]:
                words.append(word[0])
            else:
                job["experience"] = word[0]
        job["keywords"] = words
        jobs.append(job)
    ret["jobs"] = jobs
    return json.dumps(ret)
