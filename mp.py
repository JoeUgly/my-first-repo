#!/usr/bin/python3.7

# Description: Search civil service webpages for keyword(s) and attempt relavent crawling.

# To do:
# Phase 3: Advanced features
# implement locks
# scope of all objects
# follow errors 1 and 4 +
# effects of no scheme
# doctype
# retry url request
# timeout to errorlog
# Phase 4: Distribution
# enable cross-platform
# pathlib
# options eg verbose
# Phase 5: GUI


# Start timer
import datetime
startTime = datetime.datetime.now()

import urllib.request, urllib.parse, urllib.error, os, platform, time, queue, webbrowser
from multiprocessing import Process, Queue, Lock, Manager, Value



keyword = ['plant operator']
num_threads = 36
baseurllimit = 1
crawl_level = 1



# Set OS
osname = platform.system()

# Set blacklist
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


## change to pathlib
# Clear errorlog
if osname == 'Windows':
    errorfile = open(r'''C:\Users\jschiffler\Desktop\Text_n_Stuff\current\errorlog.txt''', "w")
elif osname == 'Linux':
    errorfile = open(r'''/home/joepers/code/current/civ_crawl/errorlog''', "w")
elif osname == 'Darwin':
    errorfile = open(r'''/home/joepers/code/current/civ_crawl/errorlog''', "w")
    
errorfile.write('')

# Clear results
#if osname == 'Windows':
 #   comp_hand = open(r'''C:\Users\jschiffler\Desktop\Text_n_Stuff\current\results.txt''', "w")
#elif osname == 'Linux':
 #   comp_hand = open(r'''/home/joepers/code/current/civ_crawl/results''', "w")

#comp_hand.write('')

# Get portal URLs from file
if osname == 'Windows':
    civfile = open(r'''C:\Users\jschiffler\Desktop\Text_n_Stuff\current\sar.txt''')
elif osname == 'Linux':
    civfile = open(r'''/home/joepers/code/current/civ_crawl/civil_ny''')
elif osname == 'Darwin':
    civfile = open(r'''/home/joepers/code/current/civ_crawl/civil_ny''')

# Store portal urls in queue
allcivurls = Queue()
for civline in civfile:
    civline = civline.strip()
    allcivurls.put(civline)

# Set jobwords and bunkwords
jobwords = ['employment', 'job', 'opening', 'exam', 'test', 'postions', 'civil', 'career', 'human', 'personnel']
bunkwords = ['javascript:', '.pdf', '.jpg', '.ico', '.doc', 'mailto:', 'tel:', 'description', 'specs', 'specification', 'guide', 'faq', 'images']






######  Define the crawling function  ######
def civ_crawler(allcivurls, tasks_that_are_done, keywordurl_man_list, checkedurls_man_set, errorurls_man_dict, skipped_pages):
    print('\n\n\n\n ============================ Start function =========================== PID =', os.getpid())

    while True:

        # Get a portal url from queue    
        try:
            eachcivurl = allcivurls.get_nowait()

        # Exit function if queue is empty
        except queue.Empty:
            break

        # Begin fetching
        else:
            try:
                current_level = 0
                
                print('eachcivurl = ', eachcivurl)

                # Skip checked pages
                if eachcivurl in checkedurls_man_set:
                    skipped_pages.value += 1
                    print(skipped_pages.value, 'Skipping', eachcivurl)
                    continue

                eachcivurl = eachcivurl.lower()


                

                print('\n\n ~~~~~~~~~~~~~~~~~~~~~~~~~~ Next civurl ~~~~~~~~~~~~~~~~~~~~~~~~~~  \n PID =', os.getpid())

                # Get html
                try:
                    # Spoof user agent
                    request = urllib.request.Request(eachcivurl,headers={'User-Agent': user_agent})
                    html = urllib.request.urlopen(request, timeout=10)

                except Exception as errex:
                    print('error 1: url request at', eachcivurl)
                    errorurls_man_dict[eachcivurl] = 'error 1: ' + str(errex)
                    checkedurls_man_set.append(eachcivurl)
                    continue

                # Decode if necessary
                charset_encoding = html.info().get_content_charset()
                
                try:
                    if charset_encoding == None:
                        dechtml = html.read().decode()
                    else:
                        dechtml = html.read().decode(charset_encoding)

                # Attempt latin-1 charset encoding
                except Exception as errex:
                    try:
                        print('Attempting latin-1 charset encoding')
                        dechtml = html.read().decode('latin-1')
                        print('latin-1 success')
                    except Exception as errex:
                        print('error 2:', charset_encoding, 'decode at', eachcivurl)
                        errorurls_man_dict[eachcivurl] = 'error 2: ', str(errex)[:999]
                        checkedurls_man_set.append(eachcivurl)
                        continue
                        
                dechtml1 = dechtml.lower()

                # Search for keyword on page
                if any(zzzz in dechtml1 for zzzz in keyword):
                    print('\n~~~~~~ Keyword match ~~~~~~\n')
                    
                    # Remove trailing slash
                    if eachcivurl.endswith('/'):
                        eachcivurl = eachcivurl.rsplit('/', 1)[0]

                    keywordurl_man_list.append(eachcivurl)

                # Add to checked pages set
                checkedurls_man_set.append(eachcivurl)
                


                # Start relavent_crawler
                if current_level < crawl_level:
                    relavent_crawler(dechtml1, eachcivurl, keywordurl_man_list, checkedurls_man_set, errorurls_man_dict, current_level, skipped_pages)


                print('------------ End of function ------------  PID =', os.getpid())

            # Put portal url in the finished queue
            finally:         
                tasks_that_are_done.put(eachcivurl)



######   End of function   ######








######   Begin relavent_crawler   ######
def relavent_crawler(dechtml1, workingurl0, keywordurl_man_list, checkedurls_man_set, errorurls_man_dict, current_level, skipped_pages):
    current_level += 1
    print('\ncurrent_level =', current_level, 'of', crawl_level)

    baseurllimitset.clear
    urllistgood = {}
    urllistgood.clear
    urllistgood.setdefault(workingurl0, [])
    urllistprefilter = []
    urllistprefilter.clear()
    urllist1 = []
    urllist1.clear()
    urllist2 = []
    urllist2.clear()
    alltags = set()
    alltags.clear()
    abspath = None

    # Seperate html into lines using <a delimiter
    htmllines = dechtml1.split('<a ')

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
            alltags.add(result)


    # Append only the url to the list
    for tag in alltags:

        # Split by href
        if tag.count('href') < 1:
            continue

        urlline0 = tag.split('href')[1]

        # Determine if the tag contains a jobword
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
            #print('quovar = ', quovar) 

            urlline = urlline0.split(quovar)[1]

            # Convert any rel paths to abs
            domain = []
            domain = workingurl0.split('/', 3)[:3]
            domain = '/'.join(domain)
            abspath = urllib.parse.urljoin(domain, urlline)
            print('domain =', domain)

            ## keep queries?
            # Remove queries and fragments from url
            abspath = abspath.split('?')[0].split('#')[0]
            abspath = abspath.lower()
            urllistprefilter.append(abspath)

            # Exclude if the tag contains a bunkword
            if not any(yyy in tag for yyy in bunkwords):
                urllist1.append(abspath)

            #else:
                #print('Bunkword detected in:', tag)

                # Exclude if the abspath is on the Blacklist
                if not abspath in blacklist:
                    urllist2.append(abspath)

                #else:
                    #print('Blacklist invoked at:', abspath)

                    # Exclude if the abspath is a checked page
                    if not abspath in checkedurls_man_set:

                        # Remove trailing slash
                        if abspath.endswith('/'):
                            abspath = abspath.rsplit('/', 1)[0]
                            #print('Trailing slash prevented at:', abspath)
                        
                        urllistgood.setdefault(workingurl0, []).append(abspath)                                        

    # Display excluded urls
    excludedbybw = list(set(urllistprefilter) - set(urllist1))
    excludedbybl = list(set(urllist1) - set(urllist2))
    excludedbydups = list(set(urllist2) - set(urllistgood[workingurl0]))
    print('excluded by bunkwords = ', len(excludedbybw), '\nexcluded by blacklist = ', len(excludedbybl), excludedbybl, '\nexcluded by dups = ', len(excludedbydups), excludedbydups, '\nul1nbw = ', len(urllist1), '\nul2nbl = ', len(urllist2), '\nulgndups = ', len(urllistgood[workingurl0]))


    # Begin crawl
    print('\n-------------------- Begin crawl ----------------------  \n PID =', os.getpid(), '\n', workingurl0)

    for workingurl in urllistgood[workingurl0]:
        
        # Skip checked pages
        if workingurl in checkedurls_man_set:
            skipped_pages.value += 1
            print(skipped_pages.value, 'Skipping', workingurl)
            continue
    
        print('\n',workingurl)

        # Get html from url
        try:
            # Spoof user agent
            workingrequest = urllib.request.Request(workingurl,headers={'User-Agent': user_agent})
            workinghtml = urllib.request.urlopen(workingrequest, timeout=10)

        except Exception as errex:         
            print('error 4: url request at', workingurl)
            errorurls_man_dict[workingurl] = 'error 4: ' + str(errex)
            checkedurls_man_set.append(workingurl)
            continue

        # Decode if necessary
        charset_encoding = workinghtml.info().get_content_charset()

        try:
            if charset_encoding == None:
                decworkinghtml = workinghtml.read().decode()
            else:
                decworkinghtml = workinghtml.read().decode(charset_encoding)

        # Attempt latin-1 charset encoding
        except Exception as errex:
            try:
                print('Attempting latin-1 charset encoding')
                decworkinghtml = workinghtml.read().decode('latin-1')
                print('latin-1 success')
            except Exception as errex:
                print('error 5:', charset_encoding, 'decode at', workingurl)
                errorurls_man_dict[workingurl] = 'error 5: ', str(errex)[:999]
                checkedurls_man_set.append(workingurl)
                continue
            
        decworkinghtml1 = decworkinghtml.lower()
        
        # Search for keyword on page
        if any(zzz in decworkinghtml1 for zzz in keyword):
            print('\n~~~~~~ Keyword match ~~~~~~\n')

            baseurllimitset[workingurl] = {}
            if len(baseurllimitset[workingurl]) < baseurllimit:
                keywordurl_man_list.append(workingurl)
            else:
                print('Match omitted. Baseurl limit exceeded.')
                baseurllimitset[workingurl].add(workingurl)

        # Add to checked pages set
        checkedurls_man_set.append(workingurl)

        # Start relavent_crawler
        if current_level < crawl_level:
            print('going in')
            relavent_crawler(dechtml1, workingurl, keywordurl_man_list, checkedurls_man_set, errorurls_man_dict, current_level, skipped_pages)

    print('beam up')
    current_level -= 1

######   End of function   ######




qlength = allcivurls.qsize()
baseurllimitset = {}
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'

# Multiprocessing
if __name__ == '__main__':
    with Manager() as manager:

        # Objects to pass in
        skipped_pages = Value('i', 0)
        tasks_that_are_done = Queue()
        prev_ttad = 0
        
        # Create manager lists to pass into the child processes
        keywordurl_man_list = manager.list()
        checkedurls_man_set = manager.list()
        errorurls_man_dict = manager.dict()

        # Create child processes
        for ii in range(num_threads):
            worker = Process(target=civ_crawler, args=(allcivurls, tasks_that_are_done, keywordurl_man_list, checkedurls_man_set, errorurls_man_dict, skipped_pages))
            worker.start()

        # Wait until all child processes are done
        while True:
            if tasks_that_are_done.qsize() >= qlength:
                print('\nAll processes have finished.\n')
                break
            else:
                if tasks_that_are_done.qsize() != prev_ttad:
                    print('\nWaiting for all processes to finish. Progress =', tasks_that_are_done.qsize(), 'of', qlength)
                    prev_ttad = tasks_that_are_done.qsize()
                    time.sleep(2)
                else:
                    time.sleep(2)


        print(' ==========================================================')





        # Remove scheme from final results to prevent dups
        finalkeywordurl_set = set()
        for kk in keywordurl_man_list:
            kk = kk.split('://')[1]
            kk = str(kk)

        # Remove 'www.' and ']'
            if kk.count('www.') > 0:
                kk = kk.split('www.')[1]

            kk = kk.strip("']")
            kk = kk.strip()

            # Move results from manager list to final set
            finalkeywordurl_set.add(kk)


        finalkeywordurl_set = sorted(list(finalkeywordurl_set))

        # Create handle for results and errorlog
        if osname == 'Windows':
            #writeresults = open(r'''C:\Users\jschiffler\Desktop\Text_n_Stuff\current\results.txt''', "a")
            writeerrors = open(r'''C:\Users\jschiffler\Desktop\Text_n_Stuff\current\errorlog.txt''', "a")

        elif osname == 'Linux':
            #writeresults = open(r'''/home/joepers/code/current/civ_crawl/results''', "a")
            writeerrors = open(r'''/home/joepers/code/current/civ_crawl/errorlog''', "a")

        # Write results and errorlog
        #for kk in finalkeywordurl_set:
         #   kws = str(kk + '\n')
          #  writeresults.write(kws)

        for k, v in errorurls_man_dict.items():
            vk = str((v, '::', k))
            writeerrors.write(vk + '\n\n')

        # Calculate error rate        
        try:
            error_rate = len(errorurls_man_dict) / len(checkedurls_man_set)
            if error_rate < 0.02:
                error_rate_desc = '(low)'
            elif error_rate < 0.1:
                error_rate_desc = '(medium)'
            else:
                error_rate_desc = '(high)'
        except:
            error_rate_desc = '(data unavailable)'

        # Stop timer and display stats
        duration = datetime.datetime.now() - startTime
        print('\n\n\nPages checked =', len(checkedurls_man_set), '\nPages skipped =', skipped_pages.value, '\nDuration =', duration.seconds, 'seconds \nErrors detected =', len(errorurls_man_dict), error_rate_desc)


        # Display results
        print('\n\n\n   ################  ', len(finalkeywordurl_set), ' matches found ', '  ################\n')
        for i in finalkeywordurl_set:
            print(i.strip())


        
        # Display baseurl limit exceedances
        if len(baseurllimitset.values()) > 0:
            print('\n\nBaseurl limit exceedances at:\n', baseurllimitset.values())
            writeresults.write('\n\nBaseurl limit exceedances at:\n' + str(baseurllimitset.values()))

        # Open results in browser
        if len(finalkeywordurl_set) > 0:
            print('\n\nOpen all', len(finalkeywordurl_set), 'matches in browser?\ny/n\n')
            browserresp = input()
            if browserresp.lower() == 'y' or browserresp.lower() == 'yes':
                for eachbrowserresult in finalkeywordurl_set:
                    webbrowser.open(eachbrowserresult)

        # Open error urls in browser
        brow_e_non404 = []
        for eachbrowserresult_e, val in errorurls_man_dict.items():
            if not 'HTTP Error 404: Not Found' in val:
               brow_e_non404.append(eachbrowserresult_e)
        
        if len(brow_e_non404) > 0:
            print('\n\nOpen all', len(brow_e_non404), 'error urls in browser?\ny/n\n')
            browserresp_e = input()
            if browserresp_e.lower() == 'y' or browserresp_e.lower() == 'yes':
                for i in brow_e_non404:
                    webbrowser.open(i)
                
        























