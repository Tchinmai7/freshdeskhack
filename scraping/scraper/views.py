from django.http import HttpResponse
from freshdeskhack import scrapper as fs
# Create your views here.

def scrapper(request):
	url = request.GET.get('url', '')
	response = fs.get_jobs(url)
	return HttpResponse(response)
