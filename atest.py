#!/usr/bin/python3.7

# Description: 


import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

alltags = []
urllist1 = []
urllist2 = []


eachurl = 'http://www.townofunion.com/index.php/departments/human-resources'

# Get html from url
try:
	html0 = urllib.request.urlopen(eachurl)

	html = html0.geturl()

except Exception as e: 
	a = str(e)
	if a.startswith('HTTP Error 403'):
		print('caught it')
	else:
		print('iiiiiii')


charset_encoding = html.info().get_content_charset()

if charset_encoding == None:
	print('No char encoding detected.')
	html = html.read().decode()
else:
	print('Char encoding =', charset_encoding)
	html = html.read().decode(charset_encoding)

# Convert to lowercase
html1 = html.lower()

# Seperate html into lines using <a delimiter
htmllines = html1.split('<a')
htmllines.sort

# End lines using </a> delimiter and append to alltags list
for i in htmllines:

	# Omit lengthy <!DOCTYPE' tag
	#print('i=', i)
	#i = i.strip()
	if i.startswith('<!doctype'):
		print ('!DOCTYPE tag omitted\n')
		continue
	else:
		loc = i.find('</a>')
		result = i[:loc]
		print(result)
		alltags.append(result)

		soup = BeautifulSoup(html, 'html.parser')

		alltags = soup.find_all('a')



for tag in alltags:
	domain = eachurl.rsplit('/', 1)[0]
	path = (tag.get('href', None))
	print('d=', domain, 'p=', path)
	abspath = urllib.parse.urljoin(domain, path)
	urllist1.append(abspath)

print(len(urllist1), urllist1)















