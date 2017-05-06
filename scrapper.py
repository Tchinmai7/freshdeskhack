from bs4 import BeautifulSoup
import dryscrape
import re
import string
import rake
import json
from operator import itemgetter, attrgetter, methodcaller
def get_jobs(url):
    ret = { }
    jobs = []
    rake_object = rake.Rake("SmartStoplist.txt", 3, 2, 1)
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
            words.append(word[0])

        job["keywords"] = words
        jobs.append(job)
    ret["jobs"] = jobs
    return ret

if __name__ == "__main__":
    ret = get_jobs("https://freshdesk.com/company/careers")
    print(json.dumps(ret))
