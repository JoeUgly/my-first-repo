#!/usr/bin/python3.7

# Description: Search NYS civil service and school webpages for keyword(s) and attempt relavent crawling.

# To do:
# Phase 4: Distribution
# multithreading version
# beautiful soup version
# manually improve civil_ny file
# don't search first school page +
# civfile external?
# put relavent urls into queue? use dict to attach crawl level to url +
# documentation
# Phase 5: GUI

import datetime, os, queue, re, socket, time, urllib.parse, urllib.request, webbrowser
from multiprocessing import active_children, Lock, Manager, Process, Queue, Value
from urllib.error import URLError


# Global variables
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'
blacklist = ['herkimercounty.org/content/departments/view/9:field=services;/content/departmentservices/view/190', 'herkimercounty.org/content/departments/view/9:field=services;/content/departmentservices/view/35', 'http://cs.monroecounty.gov/mccs/lists', 'https://cs.monroecounty.gov/mccs/lists', 'https://countyherkimer.digitaltowpath.org:10069/content/departments/view/9:field=services;/content/departmentservices/view/190', 'https://countyherkimer.digitaltowpath.org:10069/content/departments/view/9:field=services;/content/departmentservices/view/35', 'https://www.cs.ny.gov/testing/localtestguides.cfm', 'https://www.cs.ny.gov/testing/testguides.cfm', 'https://www.monroecounty.gov/mccs/lists', 'https://www.tompkinscivilservice.org/civilservice/jobs', 'http://www2.erie.gov/employment/index.php?q=civil-service-study-guides', 'http://www.co.essex.ny.us/personnel/', 'http://www.cs.ny.gov/testing/localtestguides.cfm', 'http://www.cs.ny.gov/testing/testguides.cfm', 'http://www.monroecounty.gov/hr/lists', 'http://www.niagaracounty.com/employment/eligible-lists', 'http://www.ogdensburg.org/index.aspx?nid=345', 'http://www.ongov.net/employment/job_specs/', 'http://www.orleansny.com/departments/operations/personnel/job-specifications', 'http://www.putnamcountyny.com/personneldept/jobspecs/', 'http://www.tompkinscivilservice.org/civilservice/jobs', 'ocgov.net//oneida/personnel/jobclassspecs', 'ocgov.net/oneida/personnel/jobclassspecs', 'www.clintoncountygov.com/employment/job_description_list', 'www.co.genesee.ny.us/departments/humanresources/jobspecs.php', 'www.penfield.org/multirss.php', 'https://jobs.albanyny.gov/default/jobs']
jobwords = ['employment', 'job', 'opening', 'exam', 'test', 'postions', 'civil service', 'career', 'human resource', 'personnel']
bunkwords = ['javascript:', '.pdf', '.jpg', '.ico', '.doc', 'mailto:', 'tel:', 'description', 'specs', 'specification', 'guide', 'faq', 'images']           
lock = Lock()



######  Define the crawling function  ######
def scraper(keyword_list, allcivurls_q, max_crawl_depth, keywordurl_man_list, checkedurls_man_list, errorurls_man_dict, skipped_pages, no_jobword_url_man_list, bunkword_tag_man_list, blacklist_url_man_list, prog_count, total_count, all_links_arg, verbose_arg, prevent_man_list):
    if verbose_arg: print(os.getpid(), '\n\n =================== Start function ===================')
    while True:

        # Get a url tuple from the queue    
        try:
            with lock:
                workingurl_tup = allcivurls_q.get_nowait()

        # Exit function if queue is empty
        except queue.Empty:
            if verbose_arg: print(os.getpid(), 'Queue empty. Closing process...')
            break

        # Begin fetching
        else:
            try:
                if verbose_arg: print('\n\n', os.getpid(), 'workingurl_tup =', workingurl_tup)

                workingurl = workingurl_tup[0]
           
                # Skip checked pages
                if workingurl in checkedurls_man_list:
                    if verbose_arg: print(os.getpid(), 'Skipping(1)', workingurl)
                    with lock:
                        skipped_pages.value += 1
                    continue
                
                # Add to checked pages list
                with lock:
                    checkedurls_man_list.append(workingurl)

                # Spoof user agent
                try:
                    request = urllib.request.Request(workingurl, headers={'User-Agent': user_agent})
                    html = urllib.request.urlopen(request, timeout=10)

                except Exception as errex:
                    if 'timed out' in str(errex):
                        if verbose_arg: print(os.getpid(), 'error 3: url timeout at', workingurl)
                        with lock:
                            errorurls_man_dict[workingurl] = 'error 3: ' + str(errex)
                        continue

                    elif 'HTTP Error 404' in str(errex):
                        if verbose_arg: print(os.getpid(), 'error 4: url request at', workingurl)
                        with lock:
                            errorurls_man_dict[workingurl] = 'error 4: ' + str(errex)
                        continue
                    
                    else:
                        if verbose_arg: print(os.getpid(), 'error 1:', workingurl)
                        with lock:
                            errorurls_man_dict[workingurl] = 'error 1: ' + str(errex)
                        continue

                # Decode html
                charset_encoding = html.info().get_content_charset()
                try:
                    if charset_encoding == None:
                        dec_html = html.read().decode()
                    else:
                        dec_html = html.read().decode(charset_encoding)

                # Attempt latin-1 charset encoding
                except Exception as errex:
                    try:
                        dec_html = html.read().decode('latin-1')                        
                    except Exception as errex:
                        if verbose_arg: print(os.getpid(), 'error 2:', charset_encoding, 'decode at', workingurl)
                        with lock:
                            errorurls_man_dict[workingurl] = 'error 2: ', str(errex)[:999]
                        continue
                if verbose_arg: print(os.getpid(), 'charset_encoding =', charset_encoding)

                # Convert HTML to lowercase
                dec_html = dec_html.lower()
                        
                # Exclude first page of schools
                if workingurl_tup[1] != -1:
                    
                    # Search for keyword on page
                    if any(zzzz in dec_html for zzzz in keyword_list):
                        if verbose_arg: print(os.getpid(), '\n~~~~~~ Keyword match ~~~~~~\n')
                        with lock:
                            keywordurl_man_list.append(workingurl)

                # Start relavent_crawler
                if workingurl_tup[1] < max_crawl_depth:
                    
                    # Seperate tuple and increment
                    #workingurl_tup = (workingurl, workingurl_tup[1] + 1)
                    if verbose_arg: print(os.getpid(), 'Starting crawler at', workingurl_tup)
                    
                    relavent_crawler(dec_html, workingurl_tup, checkedurls_man_list, errorurls_man_dict, skipped_pages, no_jobword_url_man_list, bunkword_tag_man_list, blacklist_url_man_list, all_links_arg, verbose_arg, prevent_man_list)

                else:
                    if verbose_arg: print(os.getpid(), '--- End of crawl at', workingurl_tup, '\n')

            # Catch all other errors
            except Exception as errex:
                print(os.getpid(), 'Fatal error detected. Killing process ...', str(errex)[:999])
                with lock:
                    errorurls_man_dict[workingurl] = os.getpid() + 'error 0: ' + str(errex)
                break

            # Declare the task has finished
            finally:
                prog_count.value += 1


######   End of function   ######







######   Begin relavent_crawler   ######
def relavent_crawler(dec_html, workingurl_tup, checkedurls_man_list, errorurls_man_dict, skipped_pages, no_jobword_url_man_list, bunkword_tag_man_list, blacklist_url_man_list, all_links_arg, verbose_arg, prevent_man_list):

    workingurl_tup = (workingurl_tup[0], workingurl_tup[1] + 1)    
    if verbose_arg: print(os.getpid(), '\n workingurl_tup =', workingurl_tup)

    # Seperate html into a set of tags using href= and </a> regex
    regex = 'href=.*?</a>'
    alltags = re.findall(regex, dec_html, flags=re.DOTALL)
    alltags_set = set(alltags)

    for tag in alltags_set:

        if not all_links_arg:
            
            # Proceed if the tag contains a jobword
            if not any(xxx in tag for xxx in jobwords):
                #if verbose_arg: print(os.getpid(), 'No job words detected at:', tag[:99])
                with lock:            
                    no_jobword_url_man_list.append(tag)
                continue

            # Exclude if the tag contains a bunkword
            if any(yyy in tag for yyy in bunkwords):
                if verbose_arg: print(os.getpid(), 'Bunk word detected at:', tag[:99])
                with lock:
                    bunkword_tag_man_list.append(tag)
                continue

        # Determine if double or single quote comes first in tag
        dqloc = tag.find('"')
        sqloc = tag.find("'")

        if dqloc == sqloc:
            if verbose_arg: print(os.getpid(), dqloc, 'Malformed quotes at', tag[:99])
            continue
        elif dqloc < sqloc:
            if dqloc > -1:
                quovar = '"'
            else: quovar = "'"
        elif dqloc > sqloc:
            if sqloc > -1:
                quovar = "'"
            else: quovar = '"'
        #if verbose_arg: print(os.getpid(), 'quovar =', quovar) 

        # Use the quote as the tag delimiter to form the url
        urlline = tag.split(quovar)[1]

        # Convert any rel paths to abs
        domain = []
        domain = workingurl_tup[0].split('/', 3)[:3]
        domain = '/'.join(domain)
        domain = domain.strip()
        abspath = urllib.parse.urljoin(domain, urlline)
        if verbose_arg: print(os.getpid(), 'domain =', domain)

        # Remove fragments from url
        abspath = abspath.strip()
        abspath = abspath.split('#')[0]

        # Remove trailing slash
        if abspath.endswith('/'):
            abspath = abspath.rsplit('/', 1)[0]

        # Convert URL to lowercase
        abspath = abspath.lower()
        #print(os.getpid(), 'abspath =', abspath, '\n')

        # Exclude if the abspath is a checked page
        if abspath in checkedurls_man_list:
            if verbose_arg: print(os.getpid(), 'Skipping(2)', abspath)
            with lock:
                skipped_pages.value += 1
            continue

        # Prevent dups in queue
        if abspath in prevent_man_list:
            if verbose_arg: print(os.getpid(), 'Skipping(3)', abspath)
            with lock:
                skipped_pages.value += 1
            continue

        # Exclude if the abspath is on the Blacklist
        if abspath in blacklist:
            if verbose_arg: print(os.getpid(), 'Blacklist invoked at:', abspath)
            with lock:
                blacklist_url_man_list.append(abspath)
            continue

        # Create new URL tuple and put in queue
        new_tup = (abspath, workingurl_tup[1])
        if verbose_arg: print(os.getpid(), 'new tuple =', new_tup)
        with lock:
            allcivurls_q.put(new_tup)
            total_count.value += 1
            prevent_man_list.append(abspath)
            

               
######   End of function   ######





# Multiprocessing
if __name__ == '__main__':
    print('     ~~~  Joe\'s Jorbs  ~~~ \n  Find jobs in New York State \n')

    # Arguments include -a, -c, -s, -u, -v, and -w
    print('\n Enter "c" to search Civil Service websites \n Enter "s" to search school district and charter school websites \n Enter "u" to search university and college websites \n or any combination thereof. Example: scu')
    arg_resp = input()
    print('\n')

    if 'help' in arg_resp:
        print('help doc here')
    
    all_links_arg = False
    if 'a' in arg_resp:
        all_links_arg = True
        print('All URL links option invoked.')

    civ_arg = False
    if 'c' in arg_resp:
        civ_arg = True
        print('Civil Service option invoked.')        

    school_districts_arg = False
    if 's' in arg_resp:
        school_districts_arg = True
        print('School districts option invoked.')

    uni_arg = False
    if 'u' in arg_resp:
        uni_arg = True
        print('Universities and colleges option invoked.')

    verbose_arg = False
    if 'v' in arg_resp:
        verbose_arg = True
        print('Verbose option invoked.')

    write_arg = False
    if 'w' in arg_resp:
        write_arg = True
        print('Write to file option invoked.')

    
    # Set the keyword(s)
    keyword_list = []
    keyword_resp = input('\n\n Enter the first keyword to search for \n')
    keyword_list.append(keyword_resp.lower())
    while True:
        keyword_resp = input('\n Enter the next keyword or leave blank to finish \n')
        if keyword_resp == '': break
        else: keyword_list.append(keyword_resp.lower())

    # Set the number of processes to run
    while True:
        try:
            num_threads = input('\n Enter the number of processes to run in parallel \n or leave blank to use the recommended value \n')
            if num_threads == '':
                num_threads = 32
                break
            num_threads = int(num_threads)
            if num_threads > 0: break
            else: print('\n____ Error. Your input was not greater than zero. ____')
        except:
            print('\n____ Error. Your input was not an integer. ____')

    # Set the crawl level
    while True:
        try:
            max_crawl_depth = input('\n Enter the number of levels to crawl \n or leave blank to use the recommended value \n')
            if max_crawl_depth == '':
                max_crawl_depth = 2
                break
            max_crawl_depth = int(max_crawl_depth)
            if max_crawl_depth >= 0: break
            else: print('\n____ Error. Your input was not a postive number. ____')
        except:
            print('\n____ Error. Your input was not an integer. ____')


    # Start timer
    startTime = datetime.datetime.now()

    # Use school disctrict, charter school, and/or civil service URLs
    civ_list_h = open('/home/joepers/code/civ_list')
    schools_h = open('/home/joepers/code/school_list')
    uni_list_h = open('/home/joepers/code/uni_list')
    q_dict = {}

    # Store school URls in the dictionary
    if school_districts_arg:

        # Assign a lower starting crawl level
        for each_line in schools_h:
            q_dict[each_line] = -1

    # Store universites URLs in the dict
    if uni_arg:
        for each_line in uni_list_h:
            q_dict[each_line] = -1
        
    # Store civil service URLs in the dict
    if civ_arg:
        for each_line in civ_list_h:
            q_dict[each_line] = 0

    # Move dict items to a queue
    allcivurls_q = Queue()

    for kv in q_dict.items():
        allcivurls_q.put(kv)

    # Misc objects
    qlength = allcivurls_q.qsize()
    skipped_pages = Value('i', 0)
    prog_count = Value('i', 0)
    total_count = Value('i', qlength)

    # Create manager lists
    manager = Manager()
    keywordurl_man_list = manager.list()
    checkedurls_man_list = manager.list()
    errorurls_man_dict = manager.dict()
    no_jobword_url_man_list = manager.list()
    bunkword_tag_man_list = manager.list()
    blacklist_url_man_list = manager.list()
    prevent_man_list = manager.list()

    # Create child processes
    for ii in range(num_threads):
        worker = Process(target=scraper, args=(keyword_list, allcivurls_q, max_crawl_depth, keywordurl_man_list, checkedurls_man_list, errorurls_man_dict, skipped_pages, no_jobword_url_man_list, bunkword_tag_man_list, blacklist_url_man_list, prog_count, total_count, all_links_arg, verbose_arg, prevent_man_list))
        worker.start()

    # Wait until all tasks are done
    current_prog_c = None
    while len(active_children()) > 1:
        if current_prog_c != prog_count.value:
            tmp = os.system('clear||cls')
            print(' Number of processes running =', len(active_children()), '\n Max crawl depth =', max_crawl_depth, '\n\n\n\n\n Now searching for keyword(s):', keyword_list, '\n\n Waiting for all processes to finish. Progress =', prog_count.value, 'of', total_count.value)
            current_prog_c = prog_count.value
        else: time.sleep(3)


    print(' ============================================')




    # Remove scheme from final results to prevent dups
    keywordurl_dict = {}
    keywordurl_man_list.sort()
    for entry in keywordurl_man_list:
        result = entry.split('://')[1]
        result = str(result)

        # Remove 'www.' and ']'
        if result.count('www.') > 0:
            result = result.split('www.')[1]
        result = result.strip("']")
        result = result.strip()

        # Move results fto dict to remove dups
        keywordurl_dict[result] = entry

    # Move results to final list
    finalkeywordurl_list = []
    for i in keywordurl_dict.values():
        finalkeywordurl_list.append(i)

    finalkeywordurl_list.sort()

    # Write results and errorlog
    if write_arg:
        from os.path import expanduser  

        # Make jorbs directory in home
        jorb_home = os.path.join(expanduser("~"), 'jorbs')
        if not os.path.exists(jorb_home):
            os.makedirs(jorb_home)

        # Clear errorlog
        error_path = os.path.join(jorb_home, 'errorlog.txt')
        with open(error_path, "w") as error_file:
            error_file.write('')

        # Clear results
        results_path = os.path.join(jorb_home, 'results.txt')
        with open(results_path, "w") as results_file:
            results_file.write('')
   
        # Write results using original man_list
        with open(results_path, "a") as writeresults:
            '''
            for kk in keywordurl_man_list:
                kws = str(kk + '\n')
                writeresults.write(kws)
            '''
            for kk in checkedurls_man_list:
                #kws = str(kk + '\n')
                writeresults.write(kk)
                print(kk)
           
        
        #write errorlog
        with open(error_path, "a") as writeerrors:
            for k, v in errorurls_man_dict.items():
                #vk = str((v, '::', k))
                writeerrors.write(v + ' :: ' + k + '\n\n')

    # Calculate error rate        
    try:
        error_rate = len(errorurls_man_dict) / len(checkedurls_man_list)
        if error_rate < 0.05:
            error_rate_desc = '(low error rate)'
        elif error_rate < 0.15:
            error_rate_desc = '(medium error rate)'
        else:
            error_rate_desc = '(high error rate)'
    except Exception as errex:
        error_rate_desc = '(error rate unavailable)'
        print(errex)

    # Stop timer and display stats
    duration = datetime.datetime.now() - startTime
    print('\n\n\nPages checked =', len(checkedurls_man_list))
    if verbose_arg:
        for i in checkedurls_man_list: print(i)
    
    print('Pages skipped =', skipped_pages.value, '\nDuration =', duration.seconds, 'seconds \nErrors detected =', len(errorurls_man_dict), error_rate_desc)

    print('Bunkword exclusions =', len(bunkword_tag_man_list))
    '''if verbose_arg:
        for i in bunkword_tag_man_list: print(i[:127])
    '''
    print('Blacklist exclusions =', len(blacklist_url_man_list))
    '''if verbose_arg:
        for i in blacklist_url_man_list: print(i)
    '''
    # Display results
    print('\n\n\n   ################  ', len(finalkeywordurl_list), ' matches found ', '  ################\n')
    for i in finalkeywordurl_list:
        print(i.strip())

    # Open results in browser
    if len(finalkeywordurl_list) > 0:
        print('\n\n Open all', len(finalkeywordurl_list), 'matches in browser?\ny/n\n')
        browserresp = input()
        if browserresp.lower() == 'y' or browserresp.lower() == 'yes':
            for eachbrowserresult in finalkeywordurl_list:
                webbrowser.open(eachbrowserresult)

    error1_tally, error2_tally, error3_tally, error4_tally = (0,)*4

    for i in errorurls_man_dict.values():
        if 'error 1: ' in i: error1_tally += 1
        if 'error 2: ' in i: error2_tally += 1
        if 'error 3: ' in i: error3_tally += 1
        if 'error 4: ' in i: error4_tally += 1

    print(' \033[4m Error code: Description | Frequency \033[0m')
    print('     Error 1: URL request |', error1_tally)
    print('     Error 2: HTTP decode |', error2_tally)
    print('     Error 3: URL timeout |', error3_tally)
    print('     Error 4:    HTTP 404 |', error4_tally)


    # Remove 404 error urls
    brow_e_non404 = []
    for eachbrowserresult_e, val in errorurls_man_dict.items():
        if not 'HTTP Error 404' in val:
           brow_e_non404.append(eachbrowserresult_e)

    # Open non 404 error urls in browser
    if len(brow_e_non404) > 0:
        print('\n\n Open', len(brow_e_non404), 'non 404 error URLs in browser?\ny/n\n')
        browserresp_e = input()
        if browserresp_e.lower() == 'y' or browserresp_e.lower() == 'yes':
            for i in brow_e_non404:
                webbrowser.open(i)









'''
  How to use this program


~~~  Keyword input section  ~~~

Type the job title you wish to find and then press enter.
Don't worry about uppercase or lowercase letters.
Each keyword can include spaces.


Example 1: Search for one keyword
 Enter the first keyword to search for
registered nurse

 Enter the next keyword or enter nothing to finish

(just hit enter)


Example 2: Multiple keywords
 Enter the first keyword to search for
librarian

 Enter the next keyword or enter nothing to finish
library clerk

 Enter the next keyword or enter nothing to finish
library aide

 Enter the next keyword or enter nothing to finish

(just hit enter)


For a job posting to match successfully it must contain the entire exact keyword. For example:
A job posting for a "Water Plant Operator" would NOT match the keyword "wastewater plant operator", because it doesn't include "wastewater".
However, it would match the keyword "plant operator".

This program can not find results if they are similar or synonyms to your keyword. For example:
A job posting for a "Correctional Officer" would NOT match the keyword "corrections officer", because of the difference in spelling.
In this case you should input all synonyms. E.g. Correctional officer, corrections officer, prison guard, etc.

Using a less specific keyword will help get more results. For example:
A job posting for a "Correctional Officer" would match the keyword "correction".



~~~  Processes input section  ~~~

The number you enter here will determine how fast your search is performed. A higher number will take less time, but will use more of your computer's resources.

If you are unsure, use a number around 10 for a laptop or 20 for a desktop.

I would not use a number much higher than 30 due to diminishing returns and the possiblity of crashing.

Example 3:
 Enter the number of processes to run in parallel
15



~~~  Crawl level input section  ~~~

The number you enter here will determine how thorough of a serach to perform. A higher number should find more results, but will take more time.

If you are unsure, use 2.

I would not use a number over 3 due to diminishing returns and the expotential increase in number of pages searched.

You may want to go one number higher if you will be using the school districts search because that URL list is not optimized for finding jobs.

Example 4:
 Enter the number of levels to crawl
2




~~~  Optional arguments  ~~~


-a      All URL links
            This will search all links found on each webpage, not just the links most likely to contain job postings.
            Use this to perform a very thorough search.

-sa     School districts also
            This will search all available NYS school district webpages in addition to all available NYS civil service webpages.

-so     School districts only
            This will search all available NYS school district webpages, instead of NYS civil service webpages.

-v      Verbose
            This will print lots of info to the console.
            Use this for debugging.

-w      Write to file
            This will save the search results and an error log as text files in a directory called "Jorbs" in the user's home directory.
            Use this for debugging.
    



'''






