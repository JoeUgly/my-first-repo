#!/usr/bin/python3.7

<<<<<<< HEAD
# Description: Search civil service webpages for keyword(s) and attempt relavent crawling.

# To do:
# Phase 1: Basic function +
# Phase 2: Basic optimization +
# Phase 3: Advanced features
# parellelization
# global vars - . Use keyvalue instead? +
# implement locks
# move misc under main?
# make checked pages a dict??
# user-defined levels of crawling
# Phase 4: Distribution
# enable cross-platform
# pathlib
# Phase 5: GUI

# errors to remove = 3
=======
# Description: Search the provided webpages for keyword and attempt relavent crawling.

# To do:
# Phase 1: Basic function +
# proper html parsing - 404 and 403 error 4 +
# Phase 2: Basic optimization +
# limit results per baseurl. Overload to seperate set.
# global vars - . Use keyvalue instead?
# pathlib
# implement locks
# move misc under main
# Phase 3: Advanced features
# parellelization 
# user-defined levels of crawling
# Phase 4: Distribution
# enable cross-platform
# Phase 5: GUI

#error 3, 5, 6
>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007

# Start timer
import datetime
startTime = datetime.datetime.now()

<<<<<<< HEAD
import urllib.request, urllib.parse, urllib.error, os, platform, time, queue, webbrowser
=======
import urllib.request, urllib.parse, urllib.error, os, platform, webbrowser, traceback, time, queue
>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
from multiprocessing import Process, Queue, Lock, Manager



keyword = ['plant operator', 'librarian']
<<<<<<< HEAD
num_threads = 16
=======
num_threads = 66
>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
baseurllimit = 5


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
if osname == 'Windows':
    comp_hand = open(r'''C:\Users\jschiffler\Desktop\Text_n_Stuff\current\results.txt''', "w")
elif osname == 'Linux':
    comp_hand = open(r'''/home/joepers/code/current/civ_crawl/results''', "w")

comp_hand.write('')

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
    allcivurls.put(civline)





<<<<<<< HEAD

######  Define the crawling function  ######
def crawler(allcivurls, tasks_that_are_done, keywordurl_man_list, checkedurls_man_set, errorurls_man_dict):
=======
tasks_that_are_done = Queue()
qlength = allcivurls.qsize()
checkedurls_man_set = set()
errorurls_man_list = {}
baseurllimitset = {}
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'




######  Define the crawling function  ######
def crawler(allcivurls, tasks_that_are_done, keywordurl_man_list, checkedurls_man_set, errorurls_man_list):
>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
    while True:
        print('\n\n\n\n ============================ Start function =========================== PID =', os.getpid())
        progresscount = 1

        # Get a portal url from queue    
        try:
            eachcivurl = allcivurls.get_nowait()

        # Exit function if queue is empty
        except queue.Empty:
            break

        # Begin fetching
        else:
            try:
                print('eachcivurl = ', eachcivurl)

                # Skip checked pages
                if eachcivurl in checkedurls_man_set:
                    print('Skipping', eachcivurl)
                    continue
                    

                eachcivurl = eachcivurl.lower()
                baseurllimitset.clear
                urllistgood = {}
                urllistgood.clear
                urllistgood.setdefault(eachcivurl, [])
                urllistprefilter = []
                urllistprefilter.clear()
                urllist1 = []
                urllist1.clear()
                urllist2 = []
                urllist2.clear()
                alltags = set()
                alltags.clear()
                abspath = None
                progresscount += 1
                baseurl = eachcivurl

                print('\n\n ~~~~~~~~~~~~~~~~~~~~~~~~~~ Next civurl ~~~~~~~~~~~~~~~~~~~~~~~~~~  \n PID =', os.getpid(), 'Progress = ', progresscount)

<<<<<<< HEAD
                # Get html
                try:
=======

                # Get html
                try:
                    
>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
                    # Spoof user agent
                    request = urllib.request.Request(eachcivurl,headers={'User-Agent': user_agent})
                    html = urllib.request.urlopen(request, timeout=15)

                except Exception as errex:
                    print('error 1: url request at', eachcivurl)
<<<<<<< HEAD
                    errorurls_man_dict[eachcivurl] = 'error 1: ' + str(errex)
=======
                    errorurls_man_list[eachcivurl] = 'error 1: ' + str(errex)
>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
                    checkedurls_man_set.append(eachcivurl)
                    continue

                # Decode if necessary
                charset_encoding = html.info().get_content_charset()
                print('Char encoding =', charset_encoding)
                
                try:
                    if charset_encoding == None:
                        dechtml = html.read().decode()
                    else:
                        dechtml = html.read().decode(charset_encoding)
                except Exception as errex:
<<<<<<< HEAD
                    print('error 2: decode at', eachcivurl)
                    errorurls_man_dict[eachcivurl] = 'error 2: ', str(errex)[:999]
=======
                    print('error 2: decode at ', eachcivurl)
                    errorurls_man_list[eachcivurl] = 'error 2: ', str(errex)[:999]
>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
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
                
                ## href= as delimiter?
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

                # Set jobwords and bunkwords
                jobwords = ['employment', 'job', 'opening', 'exam', 'test', 'postions', 'civil', 'career', 'human', 'personnel']
                bunkwords = ['javascript:', '.pdf', '.jpg', '.ico', '.doc', 'mailto:', 'tel:', 'description', 'specs', 'specification', 'guide', 'faq', 'images']

<<<<<<< HEAD
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
                        
                        urlline = urlline0.split(quovar)[1]

                        # Convert any rel paths to abs
                        abspath = urllib.parse.urljoin(baseurl, urlline)

                        ## keep queries?
                        # Remove queries and fragments from url
                        abspath = abspath.split('?')[0].split('#')[0]
                        abspath = abspath.lower()
                        urllistprefilter.append(abspath)

                        # Exclude if the tag contains a bunkword
                        if not any(yyy in tag for yyy in bunkwords):
                            urllist1.append(abspath)

                            # Exclude if the abspath is on the Blacklist
                            if not abspath in blacklist:
                                urllist2.append(abspath)

                                # Exclude if the abspath is a checked page
                                if not abspath in checkedurls_man_set:

                                    # Remove trailing slash
                                    if abspath.endswith('/'):
                                        abspath = abspath.rsplit('/', 1)[0]
                                    
                                    urllistgood.setdefault(eachcivurl, []).append(abspath)                                        

                # Display excluded urls
                excludedbybw = list(set(urllistprefilter) - set(urllist1))
                excludedbybl = list(set(urllist1) - set(urllist2))
                excludedbydups = list(set(urllist2) - set(urllistgood[eachcivurl]))
                print('excluded by bunkwords = ', len(excludedbybw), '\nexcluded by blacklist = ', len(excludedbybl), excludedbybl, '\nexcluded by dups = ', len(excludedbydups), excludedbydups, '\nul1nbw = ', len(urllist1), '\nul2nbl = ', len(urllist2), '\nulgndups = ', len(urllistgood[eachcivurl]))

=======
                # Determine if the tag contains a jobword
                for tag in alltags:

                    # Append only the url to the list
                    if tag.count('href') > 0:
                        urlline0 = tag.split('href')[1]

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
                            
                            urlline = urlline0.split(quovar)[1]

                            # Convert any rel paths to abs
                            abspath = urllib.parse.urljoin(baseurl, urlline)

                            ## keep queries?
                            # Remove queries and fragments from url
                            abspath = abspath.split('?')[0].split('#')[0]
                            abspath = abspath.lower()
                            urllistprefilter.append(abspath)

                            # Exclude if the tag contains a bunkword
                            if not any(yyy in tag for yyy in bunkwords):
                                urllist1.append(abspath)

                                # Exclude if the abspath is on the Blacklist
                                if not abspath in blacklist:
                                    urllist2.append(abspath)

                                    # Exclude if the abspath is a checked page
                                    if not abspath in checkedurls_man_set:

                                        # Remove trailing slash
                                        if abspath.endswith('/'):
                                            abspath = abspath.rsplit('/', 1)[0]
                                        
                                        urllistgood.setdefault(eachcivurl, []).append(abspath)
                                    #else:
                                        #checkedurls_man_set.put(abspath)
                                        
                    ## reverse this up there
                    #else:
                        #errorurls_man_list[tag] = 'error 5: no "href="'
                     #   continue

                # Show excluded urls
                excludedbybw = list(set(urllistprefilter) - set(urllist1))
                excludedbybl = list(set(urllist1) - set(urllist2))
                try:
                    excludedbydups = list(set(urllist2) - set(urllistgood[eachcivurl]))

                    print('excluded by bunkwords = ', len(excludedbybw), '\nexcluded by blacklist = ', len(excludedbybl), excludedbybl, '\nexcluded by dups = ', len(excludedbydups), excludedbydups, '\nul1nbw = ', len(urllist1), '\nul2nbl = ', len(urllist2), '\nulgndups = ', len(urllistgood[eachcivurl]))

                except Exception as errex:
                    print('error 3: excludedbydups at', abspath)
                    errorurls_man_list[abspath] = 'error 3: ', errex
>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
                    




<<<<<<< HEAD
=======

>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
                # Begin crawl
                print('\n-------------------- Begin crawl ----------------------  \n PID =', os.getpid(), '\n', eachcivurl,)

                for workingurl in urllistgood[eachcivurl]:
                    
                    # Skip checked pages
                    if workingurl in checkedurls_man_set:
                        print('Skipping', workingurl)
                        continue
                
                    print('\n',workingurl)

                    # Get html from url
                    try:
                        # Spoof user agent
                        workingrequest = urllib.request.Request(workingurl,headers={'User-Agent': user_agent})
                        workinghtml = urllib.request.urlopen(workingrequest, timeout=15)

                    except Exception as errex:
                        print('error 4: url request at', workingurl)
<<<<<<< HEAD
                        errorurls_man_dict[workingurl] = 'error 4: ' + str(errex)
                        checkedurls_man_set.append(workingurl)
                        continue

                    # Decode if necessary
=======
                        errorurls_man_list[workingurl] = 'error 4: ' + str(errex)
                        checkedurls_man_set.append(workingurl)
                        continue

                    # Decode if necessasry
>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
                    charset_encoding = workinghtml.info().get_content_charset()
                    print('Char encoding =', charset_encoding)

                    try:
                        if charset_encoding == None:
                            decworkinghtml = workinghtml.read().decode()
                        else:
                            decworkinghtml = workinghtml.read().decode(charset_encoding)
                
                    except Exception as errex:
<<<<<<< HEAD
                        print('error 5: decode at', workingurl)
                        errorurls_man_dict[workingurl] = 'error 5: ', str(errex)[:999]
=======
                        print('error 9: decode at ', workingurl)
                        errorurls_man_list[workingurl] = 'error 9: ', str(errex)[:999]
>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
                        checkedurls_man_set.append(workingurl)
                        continue

                    decworkinghtml1 = decworkinghtml.lower()
<<<<<<< HEAD
                    
                    # Search for keyword on page
                    if any(zzz in decworkinghtml1 for zzz in keyword):
                        print('\n~~~~~~ Keyword match ~~~~~~\n')

=======
                    # Search for keyword on page
                    if any(zzz in decworkinghtml1 for zzz in keyword):
                        print('\n~~~~~~ Keyword match ~~~~~~\n')
            ## review                
>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
                        baseurllimitset[baseurl] = {}
                        if len(baseurllimitset[baseurl]) < baseurllimit:
                            keywordurl_man_list.append(workingurl)
                        else:
                            print('Match omitted. Baseurl limit exceeded.')
                            baseurllimitset[baseurl].add(workingurl)
<<<<<<< HEAD
=======
                    #else:
                        #print('~~~ No match ~~~\n')
>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007

                    # Add to checked pages set
                    checkedurls_man_set.append(workingurl)


                print('------------ End of function ------------  PID =', os.getpid())

            # Put portal url in queue
            finally:         
                tasks_that_are_done.put(eachcivurl + str(os.getpid()))

####   End of function   ####




<<<<<<< HEAD


# Objects to pass in
baseurllimitset = {}
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'

# Multiprocessing
if __name__ == '__main__':
    with Manager() as manager:

        # Objects to not pass in
        finalkeywordurl_set = set()
        tasks_that_are_done = Queue()
        qlength = allcivurls.qsize()
        prev_ttad = 0
=======
# Multiprocessing
if __name__ == '__main__':
    with Manager() as manager:
>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
        
        # Create manager lists to pass into the child processes
        keywordurl_man_list = manager.list()
        checkedurls_man_set = manager.list()
<<<<<<< HEAD
        errorurls_man_dict = manager.dict()

        # Create child processes
        for ii in range(num_threads):
            worker = Process(target=crawler, args=(allcivurls, tasks_that_are_done, keywordurl_man_list, checkedurls_man_set, errorurls_man_dict))
=======
        errorurls_man_list = manager.dict()

        # Create child processes
        for ii in range(num_threads):
            worker = Process(target=crawler, args=(allcivurls, tasks_that_are_done, keywordurl_man_list, checkedurls_man_set, errorurls_man_list))
>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
            worker.start()

        # Wait until all child processes are done
        while True:
            if tasks_that_are_done.qsize() >= qlength:
<<<<<<< HEAD
                print('All processes have finished.')
                break
            else:
                if tasks_that_are_done.qsize() != prev_ttad:
                    print('Waiting for all processes to finish. Progress =', tasks_that_are_done.qsize(), 'of', qlength)
                    prev_ttad = tasks_that_are_done.qsize()
                    time.sleep(2)
                else:
                    time.sleep(2)


        print(' ==========================================================')
=======
                print('Done', tasks_that_are_done.qsize(), qlength)
                break
            else:
                print('Waiting for all processes to finish. Progress =', tasks_that_are_done.qsize(), 'of', qlength)
                time.sleep(2)

        print(' +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007





<<<<<<< HEAD
=======
        finalkeywordurl_list = set()

>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
        # Remove scheme from final results to prevent dups
        for kk in keywordurl_man_list:
            kk = kk.split('://')[1]
            kk = str(kk)

<<<<<<< HEAD
        # Remove 'www.' and ']'
=======
        # Remove 'www.'
>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
            if kk.count('www.') > 0:
                kk = kk.split('www.')[1]

            kk = kk.strip("']")
            kk = kk.strip()
<<<<<<< HEAD

            # Move results from manager list to final set
            finalkeywordurl_set.add(kk)

        finalkeywordurl_set = sorted(list(finalkeywordurl_set))
=======
            finalkeywordurl_list.add(kk)

        finalkeywordurl_list = sorted(list(finalkeywordurl_list))
>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007

        # Create handle for results and errorlog
        if osname == 'Windows':
            writeresults = open(r'''C:\Users\jschiffler\Desktop\Text_n_Stuff\current\results.txt''', "a")
            writeerrors = open(r'''C:\Users\jschiffler\Desktop\Text_n_Stuff\current\errorlog.txt''', "a")

        elif osname == 'Linux':
            writeresults = open(r'''/home/joepers/code/current/civ_crawl/results''', "a")
            writeerrors = open(r'''/home/joepers/code/current/civ_crawl/errorlog''', "a")

        # Write results and errorlog
<<<<<<< HEAD
        for kk in finalkeywordurl_set:
            kws = str(kk + '\n')
            writeresults.write(kws)

        for k, v in errorurls_man_dict.items():
=======
        for kk in finalkeywordurl_list:
            kws = str(kk + '\n')
            writeresults.write(kws)

        for k, v in errorurls_man_list.items():
>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
            vk = str((v, '::', k))
            writeerrors.write(vk + '\n\n')

        # Calculate error rate        
        try:
<<<<<<< HEAD
            error_rate = len(errorurls_man_dict) / len(checkedurls_man_set)
=======
            error_rate = len(errorurls_man_list) / len(checkedurls_man_set)
>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
            if error_rate < 0.02:
                error_rate_desc = '(low)'
            elif error_rate < 0.2:
                error_rate_desc = '(medium)'
            else:
                error_rate_desc = '(high)'
        except:
            error_rate_desc = '(data unavailable)'

        # Stop timer and display stats
        duration = datetime.datetime.now() - startTime
<<<<<<< HEAD
        print('\n\n\nPages checked =', len(checkedurls_man_set), '\nDuration =', duration.seconds, 'seconds', '\nErrors detected =', len(errorurls_man_dict), error_rate_desc)


        # Display results
        print('\n\n\n   ################  ', len(finalkeywordurl_set), ' matches found ', '  ################\n')
        for i in finalkeywordurl_set:
=======
        print('\n\n\nPages checked =', len(checkedurls_man_set), '\nDuration =', duration.seconds, 'seconds', '\nErrors detected =', len(errorurls_man_list), error_rate_desc)


        # Display results
        print('\n\n\n   ################ ', len(finalkeywordurl_list), ' matches found ', ' ################\n')
        for i in finalkeywordurl_list:
>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
            print(i.strip())


        # Display baseurl limit exceedances
        if len(baseurllimitset.values()) > 0:
            print('\n\nBaseurl limit exceedances at:\n', baseurllimitset.values())
            writeresults.write('\n\nBaseurl limit exceedances at:\n' + str(baseurllimitset.values()))

<<<<<<< HEAD
        # Open results in browser
        '''
        if len(finalkeywordurl_set) > 0:
            browserresp = input('\n\nOpen all results in browser?\ny/n\n')
            if browserresp.lower() == 'y' or browserresp.lower() == 'yes':
                for eachbrowserresult in finalkeywordurl_set:
                    webbrowser.open(eachbrowserresult)


        # Open error urls in browser
        if len(errorurls_man_dict) > 0:
            browserresp_e = input('\n\nOpen all error urls in browser?\ny/n\n')
            if browserresp_e.lower() == 'y' or browserresp_e.lower() == 'yes':
                for eachbrowserresult_e in errorurls_man_dict:
                    webbrowser.open(eachbrowserresult_e)
=======
        # Open in browser
        '''
        if len(finalkeywordurl_list) > 0:
            browserresp = input('\n\nOpen all results in browser?\ny/n\n')
            if browserresp.lower() == 'y' or browserresp.lower() == 'yes':
                for eachbrowserresult in finalkeywordurl_list:
                    webbrowser.open(eachbrowserresult)

>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
        '''












<<<<<<< HEAD
=======




>>>>>>> f79c087dd6fd65dc669310408fa5306cf8944007
