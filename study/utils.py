import requests

def get_link(x, y='G'):
	from bs4 import BeautifulSoup
	if y.upper() == 'N':
		try:
			r = requests.get(x)
		except Exception as e:
			print("1. Check your internet connection.\n")
			print("2. Sample URL feed:", "https://nofile.io/f/bYSgA8rqIYt\n")
			print("3. Something Went Wrong!", e)
			return
		else:
			print("Status:", "OK", "Response:", r.status_code)
			soup = BeautifulSoup(r.content, 'html5lib')
			link = "https://nofile.io"+soup.find_all('a', attrs={'class': "downloadButton"})[0]['href'][:-1]
			return link
	elif y.upper() == 'G':
		try:
			r = requests.get("https://api.gofile.io/createLink.php?"+x.split('?')[1])
		except Exception as e:
			print("1. Check your internet connection.\n2. Sample URL feed:", "https://gofile.io/?c=Gez7cn")
			print("3. Something went wrong!", e)
			return
		else:
			print("Status:", "OK", "Response:", r.status_code)
			r = r.json()
			link = r["data"][0]['link']
			return link

def activate_link(url):
	try:
		temp = "https://api.gofile.io/createLink.php?"+url.split('?')[1]
		r = requests.get(temp)
		data = r.json()['status']
		r = requests.get(url)
		return data == 'ok'
	except Exception:
		return False


def get_details(imdb_id):
	PARAMS = {'i': imdb_id, 'apikey': 'BanMePlz'}
	r = requests.get('http://www.omdbapi.com', params=PARAMS)
	r = r.json()
	return r

def custom_pagination(request, obj):
	from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
	no_of_objects_per_page = 8
	paginator = Paginator(obj, no_of_objects_per_page)
	try:
		page = int(request.GET.get('page', 1))
	except:
		page = 1

	try:
		instance = paginator.page(page)
	except(EmptyPage, InvalidPage):
		instance = paginator.page(1)

	# Get the index of the current page
	index = instance.number - 1  # edited to something easier without index
	# This value is maximum index of your pages, so the last page - 1
	max_index = len(paginator.page_range)
	# You want a range of 7, so lets calculate where to slice the list
	start_index = index - 3 if index >= 3 else 0
	end_index = index + 3 if index <= max_index - 3 else max_index
	# Get our new page range. In the latest versions of Django page_range returns 
	# an iterator. Thus pass it to list, to make our slice possible again.
	page_range = list(paginator.page_range)[start_index:end_index]

	return (instance, page_range)

import string
from random import choice
def random_text(length=10, chars=string.digits+string.ascii_letters+'-_'):
	return ''.join([choice(chars) for _ in range(length)])