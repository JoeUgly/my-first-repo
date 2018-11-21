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


allcivurls = []
errorurls = []
abspath = 'aaa'

keywordurlset = set()
urllistprefilter = []
urllistgood = set()
alltags = set()

civfile = open('/home/joepers/code/current/civ_crawl/civil_ny')
for civline in civfile:
	allcivurls.append(civline)

for eachcivurl in allcivurls:
	alltags.clear()
	urllistgood.clear()
	urllistprefilter.clear()
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

	# Add to the keywordurl set
	if keycheck != -1:
		print('\n~~~ Found keyword ~~~\n')
		keywordurlset.add(eachcivurl)
	else:
		print('\n~~~ Not today ~~~\n')

	# Seperate html into lines using <a delimiter
	htmllines = html1.split('<a')
	#htmllines.sort


	# End lines using </a> delimiter and add to alltags set
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

				if tag.count('href="') > 0:
				#try:
		
					urlline0 = tag.split('href="')[1]
					urlline = urlline0.split('"')[0]
					print(tag, urlline)

					# Convert any rel paths to abs
					abspath = urllib.parse.urljoin(domain, urlline)
					urllistprefilter.append(abspath)

				#except:
					#print('error 1', tag)

				    # Exclude if the tag contains a bunkword
					try:
						if not any(x in tag for x in bunkwords):
							urllistgood.add(abspath)
					except:
						print('error 2', tag)
				else:
					print('no href')


		    # If tag uses single quotes
			elif tag.count("'") > 0:
		                  
		        # Append only the url to the list
				try:
					urlline = tag.split("'")[1]

					# Convert any rel paths to abs
					abspath = urllib.parse.urljoin(domain, urlline)
					urllistprefilter.append(abspath)
				except:
					print('error 3', tag)

		        # Exclude if the tag contains a bunkword
				try:
					if not any(x in tag for x in bunkwords):
						urllistgood.add(abspath)
				except:
					print('error 4', tag)


	print('============= Begin crawl ==============', abspath)

	for workingurl in urllistgood:

		## This causes many errors
		# Get html from url
		try:
			abspathhtml = urllib.request.urlopen(workingurl)
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

		try:
			abspathhtml = abspathhtml.read().decode(charset_encoding)
		except:
			print('Decode error 2 at ', abspath)
			errorurls.append(abspath)
			continue

		abspathhtml1 = abspathhtml.lower()

		# Search for keyword on page
		keycheck = abspathhtml1.find('correction officer')

		# Add to the keywordurl set
		if keycheck != -1:
			print('\n~~~ Found keyword ~~~\n')
			keywordurlset.add(abspath)
		else:
			print('\n~~~ Not today ~~~\n')







	print('\n\n~~~~~~~~~~~~ urllistprefilter length =', len(urllistprefilter), ' ~~~~~~~~~~~~\n', urllistprefilter)
	 
	print('\n\n~~~~~~~~~~~~ urllistgood length =', len(urllistgood), ' ~~~~~~~~~~~~\n', urllistgood)

		


print('\n\n############### ', len(keywordurlset), ' matches found at: ', keywordurlset)

print('\n\n', len(errorurls), ' errors found at: ', errorurls)































