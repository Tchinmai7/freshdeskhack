from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from dateutil.parser import parse
from datetime import date
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import re
from dateutil import parser
from datetime import datetime
import datetime
from dateutil.relativedelta import relativedelta
import json
import numpy as np
from pprint import pprint
import dateparser
import urllib3.request

def get_difference(date1,date2):
	special_char='-/'
	count=0
	if date2 in ['current','present']:
		end_date=datetime.datetime.now()
	else: 
		for i in special_char:
        		count=count+ date2.count(i)
		if count<2:
			date2='21/'+date2
		end_date=dateparser.parse(date2)
	count=0
	for i in special_char:
        	count=count+ date1.count(i)
        if count<2:
        	 date1='21/'+date1

	start_date=dateparser.parse(date1)		
	#print 'sd',start_date
	#print 'ed',end_date	
	#diff=dateparser.parse(date2)-dateparser.parse(date1)
	if start_date != None and end_date!= None:
		diff=(end_date-start_date).days
		#print diff
		return diff/365.0
	return 0
def get_experience(filename):	
	special_char='-/'
	buffer=20
	words=[]
	pagenums = set()
	output = StringIO()
	manager = PDFResourceManager()
	converter = TextConverter(manager, output, laparams=LAParams())
	interpreter = PDFPageInterpreter(manager, converter)
	infile = file(filename, 'rb')
	for page in PDFPage.get_pages(infile, pagenums):
	        interpreter.process_page(page)
	infile.close()
	converter.close()
	text = output.getvalue()
	output.close
	words = text.split()  
	years=[]
	x=[]
	today = datetime.date.today()	
	count=0
	workex=0
  	for i in words:
  		# print i
                count=count+1
                if count>buffer:
                        count=0
                        del years[:]
                try:
                        parse(i)
			#if i not in [',','-','and','or','of','at','on']:
                        years.append(i)

                except:
                        pass
		try:
                  if i.lower() in ['current','present','ongoing']:

                        diff=get_difference(years[-1],'current')
                        #print 'in current'
                        #print 'years[-1]',years[-1]
                        if diff>0.8:
                                workex=workex+1;
                        del years[:]
                        count=0
                  if len(years) == 2:
  			end_date=years[-1]
                        start_date=years[-2]
                        diff=get_difference(start_date,end_date)
                        if diff>0.8:
                                workex=workex+1;
                        del years[:]
                        count=0
		except:
			pass
        return workex





def get_labels(json_filename,pdf_filename):
	current_work_ex=get_experience(pdf_filename)
	print 'current work ex',current_work_ex
	partial = ''
	sample=[]

        pagenums = set()
        output = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, converter)
        infile = file(pdf_filename, 'rb')
        for page in PDFPage.get_pages(infile, pagenums):
                interpreter.process_page(page)
        infile.close()
        converter.close()
        text = output.getvalue()
        output.close
        words = text.split()
        years=[]
        x=[]
        today = datetime.date.today()
        count=0
        workex=0
	resume_keywords=[]
        job_weightage={}
	final_labels=[]
	for i in words:
		resume_keywords.append(i.lower())

	with open(json_filename) as json_data:
		min_work_ex=0
        	d = json.load(json_data)	
		for job in d["jobs"]:
			flag=0
                	sample=job["keywords"]
		   	if job.has_key("experience"):
				  exp=job["experience"]
				  if exp=='years':
					min_work_ex=5
				  else:
				  	exp1=re.findall('\d+',exp)	
					min_work_ex=exp1[0]		 
				  	#print int(exp1[0])
			 	  flag=1
			print 'job title',job["title"]
			print 'flag',flag
			print 'current work ex',current_work_ex
			print 'min work ex',min_work_ex
			if flag == 0 or ( flag == 1 and current_work_ex > min_work_ex):
                	  print 'true'
			  for keyword in sample:
				cnt=1
				if keyword.lower() in resume_keywords:
					#pprint(job["title"])
					#print job["title"]
					#print keyword
					#print '------'
					if keyword.lower() in ['ios','testing','qa','designer','android','customer','marketing','sales']:
						cnt=3
					else:
						cnt=1
					if job["title"] not in job_weightage:
						job_weightage[job["title"]]=cnt
					else:
						job_weightage[job["title"]]=job_weightage[job["title"]]+cnt
	print '------------',len(job_weightage)
	if len(job_weightage)==0:
		ret={}
		ret["labels"]="None"
		return ret
	else:
		max_job=max(job_weightage, key=job_weightage.get)
		max_weight=job_weightage[max_job]
		for job in job_weightage:
			print job,job_weightage[job]

		print 'max'
	
		for job in job_weightage:
			if job_weightage[job] >= int(max_weight) - 1:
				final_labels.append(job)
	
		for label in final_labels:
			print label
		ret={}
		ret["labels"]=final_labels
		return ret

def parsePDF(pdffile):
	http = urllib3.PoolManager()
	#url = 'http://139.59.57.104:8000/test/?url=https://freshdesk.com/company/careers/'
	#r = http.request('GET', url, preload_content=False)
	#connection_pool = urllib3.PoolManager()
	#resp = connection_pool.request('GET',url )
	#f = open('sample2.json', 'wb')
	#f.write(resp.data)
	#f.close()
	label=get_labels('/Users/sangeethaswaminathan/Desktop/sample2.json',pdffile)
	return json.dumps(label)

#get_labels('sample2.json','/Users/sangeethaswaminathan/Desktop/resume.pdf')								
#get_labels('/Users/sangeethaswaminathan/Desktop/op.json','/Users/sangeethaswaminathan/Desktop/Sanjeev_Resume(16).pdf')
#get_labels('/Users/sangeethaswaminathan/Desktop/op.json','/Users/sangeethaswaminathan/Desktop/Tarun_Resume1.pdf')

parsePDF('/Users/sangeethaswaminathan/Desktop/ResumeSample/5.pdf')
