#!/usr/bin/python3.7

# Description: Search the provided webpages for keyword and attempt relavent crawling.

# To do:
# Phase 1: Basic function
# proper html parsing - 404 and 403 error 7 +
# spoof user agent +
# Phase 2: Basic optimization
# prevent dups and checked pages +
# error log +
# open in browser
# limit 10 results per domain +
# multiple keywords
# Phase 3: Advanced features
# parellelization
# user-defined levels of crawling
# Phase 4: Distribution
# enable cross-platform
# Phase 5: GUI

#error 3,4,6 - 9

# Start timer
from datetime import datetime
startTime = datetime.now()

import urllib.request, urllib.parse, urllib.error, os

keyword = 'plant operator'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'
progresscount = 0
pagecount = 0


allcivurls = []
errorurls = {}
abspath = None
blacklisthand = open(r'''/home/joepers/code/current/civ_crawl/blacklist''')
blacklist = blacklisthand.read()

## review and print this somewhere
domainlimit = {}
domainlimitset = set()

keywordurlset = set()
urllistprefilter = []
urllist1 = []
urllist2 = []
urllistgood = set()
alltags = set()
checkedurls = set()



# Clear errorlog
f = open("/home/joepers/code/current/civ_crawl/errorlog", "w")
f.write('')

# Get portal URLs from file
civfile = open(r'''/home/joepers/code/current/civ_crawl/civil_ny''')
for civline in civfile:
    allcivurls.append(civline)
numcivurls = len(allcivurls)

for eachcivurl in allcivurls:
    alltags.clear()
    urllist1.clear()
    urllist2.clear()
    urllistgood.clear()
    urllistprefilter.clear()
    print('\n\n\n\n ============================= Start ============================\n', eachcivurl)
    progresscount += 1
    pagecount += 1
    domain = eachcivurl.rsplit('/', 1)[0]
    domainlimit[domain] = 0
    print('Progress =', progresscount, 'of', numcivurls, '\ndomain = ', domain)

    # Get html from url
    try:
        #html = urllib.request.urlopen(eachcivurl)
        #html = response.read()
        
        # Spoof user agent
        request = urllib.request.Request(eachcivurl,headers={'User-Agent': user_agent})
        html = urllib.request.urlopen(request)
        
    except Exception as errex:
        print('error 1: url request at', eachcivurl)
        errorurls[eachcivurl] = 'error 1', errex
        continue

    # Decode if necessary
    charset_encoding = html.info().get_content_charset()
    print('Char encoding =', charset_encoding)

    if charset_encoding == None:
        try:
            #dechtml = html.read().decode(errors='ignore')
            dechtml = html.read().decode()
        except Exception as errex:
            print('error 2: decode at ', eachcivurl, str(errex)[:99])
            errorurls[eachcivurl] = 'error 2', str(errex)[:99]
            continue

    else:
        try:
            dechtml = html.read().decode(charset_encoding)
        except Exception as errex:
            print('error 2: decode at ', eachcivurl, str(errex)[:99])
            errorurls[eachcivurl] = 'error 2', str(errex)[:99]
            continue

    dechtml1 = dechtml.lower()

    # Search for keyword on page
    #keycheck = None
    #keycheck = html1.find(keyword)

    # Add to the keywordurl set
    if keyword in dechtml1:
        print('\n~~~~~~ Keyword match ~~~~~~\n')
        keywordurlset.add(eachcivurl)
    else:
        print('\n~~~ No match ~~~\n')

    # Add to checked pages set
    checkedurls.add(eachcivurl)
    
    ## href= as delimiter?
    # Seperate html into lines using <a delimiter
    htmllines = dechtml1.split('<a ')
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
    bunkwords = ['javascript:', '.pdf', '.jpg', '.ico', '.doc', 'mailto:', 'tel:', 'description', 'specs', 'specification', 'guide', 'faq', 'images']

    # Determine if the tag contains a jobword
    for tag in alltags:


        # Append only the url to the list
        if tag.count('href') > 0:
            urlline0 = tag.split('href')[1]
            #print('ul0 = ', urlline0)

            if any(xxx in urlline0 for xxx in jobwords):

                # Determine if double or single quote comes first in tag
                dqloc = urlline0.find('"')
                sqloc = urlline0.find("'")

                if dqloc < sqloc:
                    if dqloc > -1:
                        quovar = '"'
                    else: quovar = "'"
                elif dqloc > sqloc:
                    if sqloc > -1:
                        quovar = "'"
                    else: quovar = '"'
                else:
                    print('error 3: tag quote at ', tag)
                    errorurls[tag] = 'error 3: tag quote'

                
                urlline = urlline0.split(quovar)[1]

                # Convert any rel paths to abs
                abspath = urllib.parse.urljoin(domain, urlline)
                urllistprefilter.append(abspath)

                # Exclude if the tag contains a bunkword
                if not any(yyy in tag for yyy in bunkwords):
                    urllist1.append(abspath)

                    # Exclude if the abspath is on the Blacklist
                    if not abspath in blacklist:
                        urllist2.append(abspath)

                        # Exclude if the abspath is a checked page
                        if not abspath in checkedurls:
                            urllistgood.add(abspath)    
            

        ## error 5 should not be an error
        else:
            print('error 5: no "href=" at ', tag)
            #errorurls[tag] = 'error 5: no "href="'
            #continue

    # Show excluded urls
    excludedbybw = list(set(urllistprefilter) - set(urllist1))
    excludedbybl = list(set(urllist1) - set(urllist2))
    excludedbydups = list(set(urllist2) - set(urllistgood))

    print('excluded by bunkwords = ', excludedbybw, '\nexcluded by blacklist = ', excludedbybl, '\nexcluded by dups = ', excludedbydups)
    #print('ul2 = ', urllist2, 'ulg = ', urllistgood)



    try:
        print('\nul1nbw = ', len(urllist1), '\nul2nbl = ', len(urllist2), '\nulgndups = ', len(urllistgood))
    except:
        print('error 6:')


    # Begin crawl
    print('\n-------------------- Begin crawl ----------------------\n')
    for workingurl in urllistgood:
        pagecount += 1
        print('\n', workingurl)

        # Get html from url
        try:

            # Spoof user agent
            workingrequest = urllib.request.Request(eachcivurl,headers={'User-Agent': user_agent})
            workinghtml = urllib.request.urlopen(workingrequest)


            #workinghtml = urllib.request.urlopen(workingurl)
        except Exception as errex:
            print('error 7: url request at', workingurl, errex)
            errorurls[workingurl] = 'error 7', errex
            continue

        # Decode if necessasry
        charset_encoding = workinghtml.info().get_content_charset()
        if charset_encoding == None:
            try:
                decworkinghtml = html.read().decode(errors='ignore')
            except Exception as errex:
                print('error 8: decode at ', workingurl, str(errex)[:99])
                errorurls[workingurl] = 'error 8', str(errex)[:99]
                continue
        else:
            try:
                decworkinghtml = workinghtml.read().decode(charset_encoding)
            except Exception as errex:
                print('error 9: decode at ', workingurl, str(errex)[:99])
                errorurls[workingurl] = 'error 9', str(errex)[:99]
                continue

        decworkinghtml1 = decworkinghtml.lower()

        # Search for keyword on page
        #keycheck = None
        #keycheck = decworkinghtml1.find(keyword)
        #print('8888888888', decworkinghtml1)

        # Add to the keywordurl set
        if keyword in decworkinghtml1:
            print('\n~~~~~~ Keyword match ~~~~~~\n')
            if domainlimit[domain] < 12:
                keywordurlset.add(workingurl)
                domainlimit[domain] += 1
            else:
                print('Match omitted. Domain limit reached.')
                domainlimitset.add(workingurl)
        else:
            print('~~~ No match ~~~\n')

        # Add to checked pages set
        checkedurls.add(workingurl)


# Results
print('\n\n\n ################################ ', len(keywordurlset), ' matches found at: ###################\n')
for i in sorted(list(keywordurlset)):
    print(i + '\n')

# Display and write errorlog
writeerrors = open("/home/joepers/code/current/civ_crawl/errorlog", "a")
print('\n\n', len(errorurls), ' errors found at: \n',)
for k, v in errorurls.items():
    print(v, '::', k, '\n')
    vk = str((v, '::', k))
    writeerrors.write(vk + '\n\n')

# Stop timer
print('churls = ', len(checkedurls), 'Number of pages checked = ', pagecount, '\nDuration = ', datetime.now() - startTime)


















