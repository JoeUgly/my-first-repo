#!/usr/bin/python3.7

# Description: Search the provided webpages for keyword and attempt crawling.

# To do: 
# Phase 1:
# keyword search
# crawl function
# Phase 2:
# prevent dups and checked pages
# blacklist
# Phase 3:
# parellelization
# user-defined levels of crawling
# Phase 4: GUI


import urllib.request, urllib.parse, urllib.error

keywordurlset = []
allcivurls = []
errorurls = []
abspath = 'aaa'

urllistgood = []
urllistomit = []

civfile = open('/home/joepers/code/current/civ_crawl/civil_ny')
for civline in civfile:
	allcivurls.append(civline)

for eachcivurl in allcivurls:
	alltags = set()
	print('\n\n\n\n ====================== Start =====================\n', eachcivurl)
	domain = eachcivurl.rsplit('/', 1)[0]
	print('domain = ', domain)


	# Get html from url
	try:
		html = urllib.request.urlopen(eachcivurl)
	except:
		print('url request error at', eachcivurl)
		errorurls.append(eachcivurl)
		continue

	# Decode if necessasry
	charset_encoding = html.info().get_content_charset()

	if charset_encoding == None:
		print('No char encoding detected.')
		#html = html.read().decode(errors='ignore')
		try:
			html = html.read().decode()
		except:
			print('Decode error at ', eachcivurl)
			errorurls.append(eachcivurl)
			continue
	else:
		print('Char encoding =', charset_encoding)
		html = html.read().decode(charset_encoding)

	html1 = html.lower()

	# Search for keyword on page
	keycheck = html1.find('correction officer')
	#keycheck = keycheck1.lower()

	# Append to the keywordurl set
	if keycheck != -1:
		print('\n~~~ Found keyword ~~~\n')
		keywordurlset.append(eachcivurl)
	else:
		print('\n~~~ Not today ~~~\n')

	# Seperate html into lines using <a delimiter
	htmllines = html1.split('<a')
	#htmllines.sort


	# End lines using </a> delimiter and append to alltags list
	for eachhtmlline in htmllines:

		## Remove?
		# Omit lengthy <!DOCTYPE tag
		if eachhtmlline.startswith('<!doctype'):
			print ('!DOCTYPE tag omitted\n')
			continue
		else:
			loc = eachhtmlline.find('</a>')
			result = eachhtmlline[:loc]
			#print(result)
			alltags.add(result)

	# Set jobwords and bunkwords
	jobwords = ['employment', 'job', 'opening', 'exam', 'test', 'postions', 'civil', 'career', 'human', 'personnel']
	bunkwords = ['javascript:', '.pdf', '.jpg', '.ico', '.doc', '^mailto:', '^tel:', 'description', 'specs', 'specification', 'guide', 'faq', 'images']

	# Determine if the tag contains a jobword
	for tag in alltags:
		if any(x in tag for x in jobwords):

			# If tag uses double quotes
			if tag.count('"') > 0:
		        
		        # Append only the url to the list
				try:
					urlline = tag.split('"')[1]
					print(tag, urlline)

					# Convert any rel paths to abs
					abspath = urllib.parse.urljoin(domain, urlline)
					urllistgood.append(abspath)
				except:
					print('error 1', tag)

		        # Exclude if the tag contains a bunkword
				try:
					if not any(x in tag for x in bunkwords):
						urllistomit.append(abspath)
				except:
					print('error 2', tag)


		    # If tag uses single quotes
			elif tag.count("'") > 0:
		                  
		        # Append only the url to the list
				try:
					urlline = tag.split("'")[1]

					# Convert any rel paths to abs
					abspath = urllib.parse.urljoin(domain, urlline)
					urllistgood.append(abspath)
				except:
					print('error 3', tag)

		        # Exclude if the tag contains a bunkword
				try:
					if not any(x in tag for x in bunkwords):
						urllistomit.append(abspath)
				except:
					print('error 4', tag)


		print('============= Begin crawl ==============', abspath)

		# Get html from url
		try:
			abspathhtml = urllib.request.urlopen(abspath)
		except:
			print('url request error at', abspath)
			errorurls.append(abspath)
			continue

		# Decode if necessasry
		charset_encoding = abspathhtml.info().get_content_charset()

		if charset_encoding == None:
			print('No char encoding detected.')
			#html = html.read().decode(errors='ignore')
			try:
				abspathhtml = abspathhtml.read().decode()
			except:
				print('Decode error at ', abspath)
				errorurls.append(abspath)
				continue
		else:
			print('Char encoding =', charset_encoding)
			abspathhtml = abspathhtml.read().decode(charset_encoding)

		abspathhtml1 = abspathhtml.lower()

		# Search for keyword on page
		keycheck = abspathhtml1.find('correction officer')

		# Append to the keywordurl set
		if keycheck != -1:
			print('\n~~~ Found keyword ~~~\n')
			keywordurlset.append(abspath)
		else:
			print('\n~~~ Not today ~~~\n')









	print('\n\n~~~~~~~~~~~~ ulgood length =', len(urllistgood), ' ~~~~~~~~~~~~\n', urllistgood)
	 
	print('\n\n~~~~~~~~~~~~ ulomit length =', len(urllistomit), ' ~~~~~~~~~~~~\n', urllistomit)

	urllistgood.clear()
	urllistomit.clear()

print('\n\n############### ', len(keywordurlset), ' matches found at: ', keywordurlset)

print('\n\n', len(errorurls), ' errors found at: ', errorurls)































