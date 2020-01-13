#!/usr/bin/python3.7

# Description: Search NYS civil service and school webpages for street address and attempt relavent crawling.
# after first pass. write and all links always on

# To do:
# get remaining locs



import datetime, os, queue, re, socket, time, urllib.parse, urllib.request, webbrowser
from multiprocessing import active_children, Lock, Manager, Process, Queue, Value
from urllib.error import URLError


# Global variables
keyword_reg = "(?:\w+\s+){0,4}\w+,?\s+(?:ny|new\s+york)\s+\d{5}"                
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'
blacklist = []

## remove about
addr_words = ['contact', 'about', 'faq', 'home']
        
lock = Lock()



######  Define the crawling function  ######
def scraper(allcivurls_q, max_crawl_depth, keywordurl_man_list, checkedurls_man_list, errorurls_man_dict, skipped_pages, prog_count, total_count, all_links_arg, verbose_arg, prevent_man_list, domain_excess_man_list, domain_man_dict):
    if verbose_arg: print(os.getpid(), '\n\n =================== Start function ===================')
    
    # Get a url tuple from the queue    
    while True:
        try:
            with lock:
                workingurl_tup = allcivurls_q.get_nowait()
                if workingurl_tup[1] < 1:
                    workingurl_tup = workingurl_tup[0], workingurl_tup[1], workingurl_tup[0]
                #print('workingurl_tup =', workingurl_tup)

        # Exit function if queue is empty
        except queue.Empty:
            if verbose_arg: print(os.getpid(), 'Queue empty. Closing process...')
            break

        # Begin fetching
        else:
            try:
                
                
                if verbose_arg: print('\n\n', os.getpid(), 'workingurl_tup =', workingurl_tup)

                workingurl = workingurl_tup[0]
                running_t = 0
           
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
                #if verbose_arg: print(os.getpid(), 'charset_encoding =', charset_encoding)

                # Convert HTML to lowercase
                dec_html = dec_html.lower()
                
                # Create domain
                domain = []
                domain = workingurl_tup[0].split('/', 3)[:3]
                domain = '/'.join(domain)
                domain = domain.strip()
                if not domain in domain_man_dict:
                    domain_man_dict[domain] = 0
                        
                # Exclude first page of schools
                if workingurl_tup[1] != -2:
                    
                    # Search for address on page
                    addr_list = re.findall(keyword_reg, dec_html, flags=re.DOTALL)
                    
                    if addr_list:
                        
                        if verbose_arg: print(os.getpid(), ' ~~~~~~ Keyword match ~~~~~~\n')
                        if domain_man_dict[domain] < 6:
                            if not any(workingurl_tup[2] in s for s in keywordurl_man_list):

                                bb = len(addr_list), 'level =', workingurl_tup[1], workingurl_tup[2], '::', str(addr_list)
                                with lock:
                                    keywordurl_man_list.append(bb)
                                    domain_man_dict[domain] += 1
                        else:
                            print('domain limit exceeded at:', workingurl)
                            with lock:
                                domain_excess_man_list.append(bb)
                                
                        





                # Start relavent_crawler
                if workingurl_tup[1] < max_crawl_depth:
                    if not any(workingurl_tup[2] in s for s in keywordurl_man_list):


                        #print(workingurl_tup[2], 'not in', keywordurl_man_list)
                        
                        # Seperate tuple and increment
                        if verbose_arg: print(os.getpid(), 'Starting crawler at', workingurl_tup)
                        

                        workingurl_tup = (workingurl_tup[0], workingurl_tup[1] + 1, workingurl_tup[2])    
                        if verbose_arg: print(os.getpid(), '\n workingurl_tup =', workingurl_tup)

                        # Seperate html into a set of tags using href= and </a> regex
                        regex = 'href=.*?</a>'
                        alltags = re.findall(regex, dec_html, flags=re.DOTALL)
                        alltags_set = set(alltags)

                        for tag in alltags_set:

                            if not all_links_arg:
                                
                                # Proceed if the tag contains a address word
                                if not any(xxx in tag for xxx in addr_words):
                                    #if verbose_arg: print(os.getpid(), 'No address words detected at:', tag[:99])
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
                            abspath = urllib.parse.urljoin(domain, urlline)
                            #if verbose_arg: print(os.getpid(), 'domain =', domain)

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
                            new_tup = (abspath, workingurl_tup[1], workingurl_tup[2])
                            if verbose_arg: print(os.getpid(), 'new tuple =', new_tup)
                            with lock:
                                allcivurls_q.put(new_tup)
                                total_count.value += 1
                                prevent_man_list.append(abspath)



            # Declare the task has finished
            finally:
                prog_count.value += 1

######   End of function   ######






# Multiprocessing
if __name__ == '__main__':
    print('\n     ~~~  Joe\'s Jorbs  ~~~ \n  Find jobs in New York State \n')

    # Arguments include -a, -c, -s, -u, -v, and -w
    print('\n\n Enter "c" to search Civil Service websites \n Enter "s" to search school district and charter school websites \n Enter "u" to search university and college websites \n or any combination thereof. Example: scu')
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

    write_arg = True
    if 'w' in arg_resp:
        write_arg = True
        print('Write to file option invoked.')

    



    # Set the number of processes to run
    while True:
        try:
            num_threads = input('\n\n Enter the number of processes to run in parallel \n or leave blank to use the recommended value \n')
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
            max_crawl_depth = input('\n\n Enter the number of levels to crawl \n or leave blank to use the recommended value \n')
            if max_crawl_depth == '':
                max_crawl_depth = 0
                break
            max_crawl_depth = int(max_crawl_depth)
            if max_crawl_depth >= 0: break
            else: print('\n____ Error. Your input was not a postive number. ____')
        except:
            print('\n____ Error. Your input was not an integer. ____')


    # Start timer
    startTime = datetime.datetime.now()

    # Use school disctrict, charter school, and/or civil service URLs 
    civ_list = []
    
    
    
    schools_list = ['http://www.easthamptonschools.org', 'http://www.edinburgcs.org', 'http://www.evcsbuffalo.org', 'http://www.frontier.wnyric.org', 'http://www.gateschili.org', 'http://www.gccschool.org', 'http://www.genvalley.org', 'http://www.hamburgschools.org', 'http://www.hcsk12.org', 'http://www.hufsd.edu', 'http://www.johnstownschools.org', 'http://www.kipptechvalley.org', 'http://www.lafargevillecsd.org', 'http://www.letchworth.k12.ny.us', 'http://www.moriahk12.org', 'http://www.nfschools.net', 'http://www.oceansideschools.org', 'http://www.sacketspatriots.org', 'http://www.slcs.org', 'http://www.starpointcsd.org', 'http://www.ticonderogak12.org', 'http://www.urbanchoicecharter.org', 'http://www.yonkerspublicschools.org', 'http://www.youngwomenscollegeprep.org', 'https://sbecacs.org', 'https://sites.google.com/a/northvillecsd.org/ncsd', 'https://urbanassembly.org', 'https://www.hdcsk12.org', 'https://www.heuvelton.k12.ny.us', 'https://www.prattsburghcsd.org', 'https://www.webutuckschools.org', 'http://ccny.cuny.edu/csom', 'http://engineering.nyu.edu', 'http://lcm.touro.edu', 'http://www.berkeleycollege.edu/index.htm', 'http://www.delhi.edu', 'http://www.mercy.edu', 'http://www.qcc.cuny.edu']





    uni_list = []
    
    
    q_dict = {}

    # Store school URls in the dictionary
    if school_districts_arg:

        # Assign a lower starting crawl level
        for each_line in schools_list:
            q_dict[each_line] = 0
            

    # Store universites URLs in the dict
    if uni_arg:
        for each_line in uni_list:
            q_dict[each_line] = 0
            
        
    # Store civil service URLs in the dict
    if civ_arg:
        for each_line in civ_list:
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
    prevent_man_list = manager.list()
    domain_excess_man_list = manager.list()
    domain_man_dict = manager.dict()

    # Create child processes
    for ii in range(num_threads):
        worker = Process(target=scraper, args=(allcivurls_q, max_crawl_depth, keywordurl_man_list, checkedurls_man_list, errorurls_man_dict, skipped_pages, prog_count, total_count, all_links_arg, verbose_arg, prevent_man_list, domain_excess_man_list, domain_man_dict))
        worker.start()

    # Wait until all tasks are done
    current_prog_c = None
    while len(active_children()) > 1:
        if not verbose_arg:
            if current_prog_c != prog_count.value:
                tmp = os.system('clear||cls')
                print(' Number of processes running =', len(active_children()), '\n Max crawl depth =', max_crawl_depth, '\n\n\n\n\n Now searching for keyword(s)', '\n\n Waiting for all processes to finish. Progress =', prog_count.value, 'of', total_count.value)
                current_prog_c = prog_count.value
        time.sleep(3)

    print(' ============================================')

    for i in keywordurl_man_list:
        print(i)


    '''
    # Remove scheme from final results to prevent dups
    keywordurl_dict = {}
    keywordurl_man_list.sort()
    for entry in keywordurl_man_list:
        ## http:// or https://
        result = entry.split('://')[1]

        # Remove 'www.' and ']'
        if result.count('www.') > 0:
            result = result.split('www.')[1]
        result = result.strip("']")
        result = result.strip()

        # Move results to dict to remove dups
        keywordurl_dict[result] = entry

    # Move results to final list
    finalkeywordurl_list = []
    for i in keywordurl_dict.values():
        finalkeywordurl_list.append(i)

    finalkeywordurl_list.sort()
    '''
    finalkeywordurl_list = keywordurl_man_list

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
            
            for kk in keywordurl_man_list:
                writeresults.write(str(kk) + "\n\n")
            '''
            for kk in checkedurls_man_list:
                writeresults.write(kk)
                print(kk)
            '''
        
        # Write errorlog
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


    # Display results
    print('\n\n\n   ################  ', len(finalkeywordurl_list), ' matches found ', '  ################\n')
    for i in finalkeywordurl_list:
        print(i)

    # Open results in browser
    if len(finalkeywordurl_list) > 0:
        print('\n\n Open all', len(finalkeywordurl_list), 'matches in browser?\ny/n\n')
        browserresp = input()
        if browserresp.lower() == 'y' or browserresp.lower() == 'yes':
            for eachbrowserresult in finalkeywordurl_list:
                webbrowser.open(eachbrowserresult)
                
    # Display domain_excess_man_list
    print('\n domain exceedances at:')
    for i in domain_excess_man_list:
        print(i)
                
    # Display errors
    if len(errorurls_man_dict.values()) > 0:
        error1_tally, error2_tally, error3_tally, error4_tally = (0,)*4

        for i in errorurls_man_dict.values():
            if 'error 1: ' in i: error1_tally += 1
            if 'error 2: ' in i: error2_tally += 1
            if 'error 3: ' in i: error3_tally += 1
            if 'error 4: ' in i: error4_tally += 1

        print('   Error code: Description | Frequency')
        print('---------------------------|-------------')
        print('      Error 1: URL request |', error1_tally)
        print('      Error 2: HTTP decode |', error2_tally)
        print('      Error 3: URL timeout |', error3_tally)
        print('      Error 4:    HTTP 404 |', error4_tally)


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













