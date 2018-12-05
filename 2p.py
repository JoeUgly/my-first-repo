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
# limit 10 results per domain. Overload to seperate set?
# multiple keywords
# Phase 3: Advanced features
# parellelization
# user-defined levels of crawling
# Phase 4: Distribution
# enable cross-platform
# Phase 5: GUI

#error 3,4,6 - 9

# Start timer
import datetime
startTime = datetime.datetime.now()

import urllib.request, urllib.parse, urllib.error, os, platform, time
from threading import Thread
import threading

keyword = 'plant operator'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'


allcivurls = []
errorurls = {}
abspath = None

# Set OS
osname = platform.system()

if osname == 'Windows':
    blacklisthand = open(r'''C:\Users\jschiffler\Desktop\Text_n_Stuff\current\blacklist.txt''')
elif osname == 'Linux':
    blacklisthand = open(r'''/home/joepers/code/current/civ_crawl/blacklist''')
elif osname == 'Darwin':
    blacklisthand = open(r'''/home/joepers/code/current/civ_crawl/blacklist''')
else:
    print(osname, 'Unknown OS platform. Exiting...')
    exit()



blacklist = blacklisthand.read()

## review and print this somewhere
domainlimit = {}
domainlimitset = set()
urllistgood = {}
keywordurlset = set()
urllistprefilter = []
urllist1 = []
urllist2 = []
all_comp = []

alltags = set()
checkedurls = set()

## change to pathlib

# Clear errorlog
if osname == 'Windows':
    f = open(r'''C:\Users\jschiffler\Desktop\Text_n_Stuff\current\errorlog.txt''', "w")
elif osname == 'Linux':
    f = open(r'''/home/joepers/code/current/civ_crawl/errorlog''', "w")
elif osname == 'Darwin':
    f = open(r'''/home/joepers/code/current/civ_crawl/errorlog''', "w")
    
f.write('')

comp_hand = open(r'''/home/joepers/code/current/civ_crawl/results''', "w")
comp_hand.write('')

# Get portal URLs from file
if osname == 'Windows':
    civfile = open(r'''C:\Users\jschiffler\Desktop\Text_n_Stuff\current\sar.txt''')
elif osname == 'Linux':
    civfile = open(r'''/home/joepers/code/current/civ_crawl/civil_ny''')
elif osname == 'Darwin':
    civfile = open(r'''/home/joepers/code/current/civ_crawl/civil_ny''')

# Store portal urls as a list
for civline0 in civfile:
    civline = civline0.strip()
    allcivurls.append(civline)

numcivurls = len(allcivurls)
num_shell = 5
block_size = int(numcivurls / num_shell + 1)
block_count = 0
block_begin = 0
block_end = block_size
urlblock = {}
pagecount = 0




######  Define the crawling function  ######
def crawler(urlblock, block_count, pagecount):
    print('\n\n\n\n ============================= Start ============================')
    print('block_count = ', block_count, '\nurlblock length =', len(urlblock), '\n', urlblock, '\n')
    progresscount = 0

    for eachcivurl in urlblock:
        print('\eachcivurl = ', eachcivurl)

        # Begin fetching
        alltags.clear()
        urllist1.clear()
        urllist2.clear()
        urllistgood[eachcivurl] = []
        urllistprefilter.clear()
        print('\n\n ~~~~~~~~~~~~~~~~~~~~~~~~~~ Next civurl ~~~~~~~~~~~~~~~~~~~~~~~~~~', progresscount, 'of', block_size, '\nblock_count =', block_count, '\n', eachcivurl)
        progresscount += 1
        pagecount += 1
        domain = eachcivurl.rsplit('/', 1)[0]
        domainlimit[domain] = 0
        #print('Progress =', progresscount, 'of', numcivurls, '\ndomain = ', domain)

        # Get html from url
        try:
            #html = urllib.request.urlopen(eachcivurl)
            #html = response.read()
            
            # Spoof user agent
            request = urllib.request.Request(eachcivurl,headers={'User-Agent': user_agent})
            html = urllib.request.urlopen(request)
            
        except Exception as errex:
            print('error 1: url request at', eachcivurl)
            errorurls[eachcivurl] = 'error 1:', errex
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
                errorurls[eachcivurl] = 'error 2:', str(errex)[:99]
                continue

        else:
            try:
                dechtml = html.read().decode(charset_encoding)
            except Exception as errex:
                print('error 2: decode at ', eachcivurl, str(errex)[:99])
                errorurls[eachcivurl] = 'error 2:', str(errex)[:99]
                continue

        dechtml1 = dechtml.lower()

        # Search for keyword on page
        #keycheck = None
        #keycheck = html1.find(keyword)

        # Add to the keywordurl set
        if keyword in dechtml1:
            print('\n~~~~~~ Keyword match ~~~~~~\n')
            keywordurlset.add(eachcivurl)
        #else:
            #print('\n~~~ No match ~~~')

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
                                urllistgood.setdefault(eachcivurl, []).append(abspath)             

            ## error 5 should not be an error
            else:
                #print('error 5: no "href=" at ', tag)
                errorurls[tag] = 'error 5: no "href="'
                continue

        # Show excluded urls
        excludedbybw = list(set(urllistprefilter) - set(urllist1))
        excludedbybl = list(set(urllist1) - set(urllist2))
        #excludedbydups = list(set(urllist2) - set(urllistgood[eachcivurl]))
        excludedbydups = 'aaa'


        print('excluded by bunkwords = ', len(excludedbybw), '\nexcluded by blacklist = ', len(excludedbybl), excludedbybl, '\nexcluded by dups = ', len(excludedbydups), excludedbydups)
        #print('ul2 = ', urllist2, 'ulg = ', urllistgood)



        try:
            print('\nul1nbw = ', len(urllist1), '\nul2nbl = ', len(urllist2), '\nulgndups = ', len(urllistgood[eachcivurl]))
        except:
            print('error 6:')


        # Begin crawl
        print('\n-------------------- Begin crawl ----------------------  ', block_count, '\n', eachcivurl, '\n')

        for workingurl in urllistgood[eachcivurl]:
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
                errorurls[workingurl] = 'error 7:', errex
                continue

            # Decode if necessasry
            charset_encoding = workinghtml.info().get_content_charset()
            if charset_encoding == None:
                try:
                    decworkinghtml = html.read().decode(errors='ignore')
                except Exception as errex:
                    print('error 8: decode at ', workingurl, str(errex)[:99])
                    errorurls[workingurl] = 'error 8:', str(errex)[:99]
                    continue
            else:
                try:
                    decworkinghtml = workinghtml.read().decode(charset_encoding)
                except Exception as errex:
                    print('error 9: decode at ', workingurl, str(errex)[:99])
                    errorurls[workingurl] = 'error 9:', str(errex)[:99]
                    continue

            decworkinghtml1 = decworkinghtml.lower()

            # Search for keyword on page
            #keycheck = None
            #keycheck = decworkinghtml1.find(keyword)
            #print('8888888888', decworkinghtml1)

            # Add to the keywordurl set
            if keyword in decworkinghtml1:
                print('\n~~~~~~ Keyword match ~~~~~~\n')
                if domainlimit[domain] < 10:
                    keywordurlset.add('block number '+ str(block_count) + '\n' + workingurl)
                    domainlimit[domain] += 1
                    
                    
                else:
                    print('Match omitted. Domain limit reached.')
                    domainlimitset.add(workingurl)
            #else:
                #print('~~~ No match ~~~\n')

            # Add to checked pages set
            checkedurls.add(workingurl)

    print('End of function', block_count, '\n\n')

    writeresults = open(r'''/home/joepers/code/current/civ_crawl/results''', "a")
    for kk in keywordurlset:
        kws = str(kk + '\n')
        writeresults.write('xxxxxx\n' + kws)



####   End of function   ####



t = {}
wait_count = 0

# Create blocks of URLs
while block_count <= num_shell:
    urlblock[block_count] = allcivurls[block_begin:block_end]
    
    # Assign blocks to new threads until empty
    if urlblock[block_count]:
        t[block_count] = threading.Thread(target=crawler, args=(urlblock[block_count], block_count, pagecount))
        t[block_count].start()
        block_begin += block_size
        block_end += block_size
        block_count += 1
    else:
        print('Empty block at:', block_count)
        break

for ooo in range(block_count):
    t[wait_count].join()
    print('Waiting for threads ...', wait_count)
    wait_count += 1


# Results
print('\n\n\n\n\n ########################## ', len(keywordurlset), ' matches found ', '##########################\n')
for i in sorted(list(keywordurlset)):
    print(i + '\n')

# Display and write errorlog
if osname == 'Windows':
    writeerrors = open(r'''C:\Users\jschiffler\Desktop\Text_n_Stuff\current\errorlog.txt''', "a")
if osname == 'Linux':
    writeerrors = open(r'''/home/joepers/code/current/civ_crawl/errorlog''', "a")
if osname == 'Darwin':
    writeerrors = open(r'''/home/joepers/code/current/civ_crawl/errorlog''', "a")

print('\n\n', len(errorurls), 'errors found\n\n')
for k, v in errorurls.items():
    #print(v, '::', k, '\n\n')
    vk = str((v, '::', k))
    writeerrors.write(vk + '\n\n')




# Stop timer
duration = datetime.datetime.now() - startTime
print('churls = ', len(checkedurls), 'Number of pages checked = ', pagecount, '\nDuration = ', duration.seconds)























