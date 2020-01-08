
# Description: Crawl webpages and rank links based on likelihood of containing job postings.



# To do:
# AP and wnyric are not totally centralized? eg: https://www.applitrack.com/saugertiesk12/onlineapp/jobpostings/view.asp
# output all 4 items +
# use redirects instead of original URLs
# checked_pages has no jbw conf values. only None, redirect, or error
# dont output dups +

# modify for use with civs. ie: 
# dont output if only result is orignal URL








import datetime, requests, psutil, gzip, os, queue, re, socket, time, traceback, urllib.parse, urllib.request, webbrowser, ssl
from os.path import expanduser
from multiprocessing import active_children, Lock, Manager, Process, Queue, Value
from math import sin, cos, sqrt, atan2, radians
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup




# Start timer
startTime = datetime.datetime.now()

# Make jorbs directory in user's home directory
jorb_home = '/home/joepers/jj_em_finder'
if not os.path.exists(jorb_home):
    os.makedirs(jorb_home)


# Make date dir to put results into
dater = datetime.datetime.now().strftime("%x").replace('/', '_')
dater_path = os.path.join(jorb_home, dater)
if not os.path.exists(dater_path):
    os.makedirs(dater_path)


# User agent
user_agent_str = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'

# Compile regex paterns for finding hidden HTML elements
style_reg = re.compile("(display\s*:\s*(none|block);?|visibility\s*:\s*hidden;?)")
#class_reg = re.compile('(hidden-sections?|sw-channel-dropdown)')
class_reg = re.compile('(hidden-sections?|dropdown|has-dropdown|sw-channel-dropdown|dropdown-toggle)')

## unn?
# Omit these pages
blacklist = ('cc.cnyric.org/districtpage.cfm?pageid=112', 'co.essex.ny.us/personnel', 'co.ontario.ny.us/94/human-resources', 'countyherkimer.digitaltowpath.org:10069/content/departments/view/9:field=services;/content/departmentservices/view/190', 'countyherkimer.digitaltowpath.org:10069/content/departments/view/9:field=services;/content/departmentservices/view/35', 'cs.monroecounty.gov/mccs/lists', 'herkimercounty.org/content/departments/view/9:field=services;/content/departmentservices/view/190', 'herkimercounty.org/content/departments/view/9:field=services;/content/departmentservices/view/35', 'jobs.albanyny.gov/default/jobs', 'monroecounty.gov/hr/lists', 'monroecounty.gov/mccs/lists', 'mycivilservice.rocklandgov.com/default/jobs', 'niagaracounty.com/employment/eligible-lists', 'ogdensburg.org/index.aspx?nid=345', 'penfield.org/multirss.php', 'tompkinscivilservice.org/civilservice/jobs', 'tompkinscivilservice.org/civilservice/jobs')

# Omit these domains
blacklist_domains = ('twitter.com')

# Include links that include any of these
# High confidence civ jbws
jobwords_civ_high = ('continuous recruitment', 'employment', 'job listing', 'job opening', 'job posting', 'job announcement', 'job opportunities', 'jobs available', 'available positions', 'open positions', 'available employment', 'career opportunities', 'employment opportunities', 'current vacancies', 'current job', 'current employment', 'current opening', 'current posting', 'current opportunities', 'careers at', 'jobs at', 'jobs @', 'work at', 'employment at', 'find your career', 'browse jobs', 'search jobs', 'continuous recruitment', 'vacancy postings', 'prospective employees', 'upcoming exam', 'exam announcement', 'examination announcement', 'civil service opportunities', 'civil service exam', 'civil service test', 'current civil service','open competitive', 'open-competitive')

# Low confidence civ jbws
jobwords_civ_low = ('open to', 'job', 'job seeker', 'job title', 'civil service', 'exam', 'examination', 'test', 'positions', 'careers', 'human resource', 'personnel', 'vacancies', 'current exam', 'posting', 'opening', 'vacancy')


# High confidence sch and uni jbws
jobwords_su_high = ('continuous recruitment', 'employment', 'job listing', 'job opening', 'job posting', 'job announcement', 'job opportunities', 'job vacancies', 'jobs available', 'available positions', 'open positions', 'available employment', 'career opportunities', 'employment opportunities', 'current vacancies', 'current job', 'current employment', 'current opening', 'current posting', 'current opportunities', 'careers at', 'jobs at', 'jobs @', 'work at', 'employment at', 'find your career', 'browse jobs', 'search jobs', 'continuous recruitment', 'vacancy postings', 'prospective employees')

# Low confidence sch and uni jbws
jobwords_su_low = ('join', 'job seeker', 'job', 'job title', 'positions', 'careers', 'human resource', 'personnel', 'vacancies', 'posting', 'opening', 'recruitment', '>faculty<', '>staff<', '>adjunct<', '>academic<', '>support<', '>instructional<', '>administrative<', '>professional<', '>classified<', '>coaching<', 'vacancy')

# Worst offenders
#offenders = ['faculty', 'staff', 'professional', 'management', 'administrat', 'academic', 'support', 'instructional', 'adjunct', 'classified', 'teach', 'coaching']

## switching to careers solves all these
# career services, career peers, career prep, career fair, volunteer
## application
# Exclude links that contain any of these
bunkwords = ('academics', 'professional development', 'career development', 'javascript:', '.pdf', '.jpg', '.ico', '.rtf', '.doc', 'mailto:', 'tel:', 'icon', 'description', 'specs', 'specification', 'guide', 'faq', 'images', 'exam scores', 'resume-sample', 'resume sample', 'directory', 'pupil personnel')

# olas
# https://schoolapp.wnyric.org/ats/job_board
# recruitfront

# Multiprocessing lock for shared objects
lock = Lock()





# Removes extra info from urls to prevent duplicate pages from being checked more than once
def dup_checker_f(dup_checker):
    print(os.getpid(), 'start dup check:', dup_checker)

    # Remove scheme
    if dup_checker.startswith('http://') or dup_checker.startswith('https://'):
        dup_checker = dup_checker.split('://')[1]
    else:
        print('__Error__ No scheme at:', dup_checker)


    '''
    ## unn
    ## and must supply errorurls_man_dict as arg
    # Catch no scheme error
    else:
        with lock:
            print(os.getpid(), '\njj_error 2: No scheme:', dup_checker)
            errorurls_man_dict[dup_checker] = ['jj_error 2', 'No scheme', 111]
            outcome(checkedurls_man_list, dup_checker, 'jj_error 2')

        return dup_checker
    '''

    # Remove www. and variants
    if dup_checker.startswith('www.'):
        dup_checker = dup_checker.split('www.')[1]
    elif dup_checker.startswith('www2.'):
        dup_checker = dup_checker.split('www2.')[1]
    elif dup_checker.startswith('www3.'):
        dup_checker = dup_checker.split('www3.')[1]

    # Remove fragments
    dup_checker = dup_checker.split('#')[0]

    ## Remove double forward slashes?
    dup_checker = dup_checker.replace('//', '/')

    # Remove trailing whitespace and slash and then lowercase it
    dup_checker = dup_checker.strip().strip('/').lower()

    return dup_checker


# Determine if url has been checked already and optionally add to queue
def proceed_f(abspath, working_list, checkedurls_man_list, skipped_pages, current_crawl_level, all_urls_q, total_count, add_to_queue_b):

    # Call dup checker function before putting in queue
    dup_checker = dup_checker_f(abspath)

    # Exclude checked pages
    for i in checkedurls_man_list:
        if i == None:
            print('__ error. None in cml', checkedurls_man_list)
            continue
        if dup_checker == i[0]:
            print(os.getpid(), 'Skipping:', dup_checker)
            with lock:
                try:
                    skipped_pages.value += 1
                except Exception as errex: print(errex)

            # Declare not to proceed
            return False

    '''
    ##if dup_checker in checkedurls_man_list or dup_checker in blacklist:
    # Exclude checked pages
    if dup_checker in checkedurls_man_list:
        print(os.getpid(), 'Skipping:', dup_checker)
        with lock:
            skipped_pages.value += 1

        # Declare not to proceed
        return False
    '''

    # Exclude if the abspath is on the Blacklist
    if dup_checker in blacklist:
        print(os.getpid(), 'Blacklist invoked:', dup_checker)
        try:
            with lock:
                skipped_pages.value += 1
        except Exception as errex:
            print(errex)
        return False    


    # Form domain by splitting after 3rd slash
    domain = '/'.join(abspath.split('/')[:3])
    domain_dup = dup_checker_f(domain)

    # Exclude if the abspath is on the Blacklist
    if domain_dup in blacklist_domains:
        print(os.getpid(), 'Domain blacklist invoked:', domain_dup)
        try:
            with lock:
                skipped_pages.value += 1
        except Exception as errex:
            print(errex)
        return False


    # Add abspath to queue if add_to_queue_b is True
    if add_to_queue_b:

        # Create new working list: [URL, crawl level, portal URL, jbw type]
        new_working_list = [abspath, current_crawl_level, working_list[2], working_list[3]]
        print(os.getpid(), 'Putting list into queue:', new_working_list)

        # Put new working list in queue
        with lock:
            try:
                all_urls_q.put(new_working_list)
                total_count.value += 1
            except Exception as errex:
                print(errex)

    # Add dup_checker, jbw type, and jbw confidence placeholder to checked pages list
    print(os.getpid(), 'Adding to cml with None:', dup_checker)
    with lock:
        try:
            checkedurls_man_list.append([dup_checker, None])
        except Exception as errex:
            print(errex)


    # Declare to proceed
    return True



# Update outcome of each URL with jbw conf
def outcome(checkedurls_man_list, url, conf_val):

    # Convert URL to dup checker
    url = dup_checker_f(url)

    ## Catch multiple matches?
    # Attach jbw conf to URL in checkedurls_man_list
    #with lock:
    for each_url in checkedurls_man_list:
        if each_url[0] == url:
            remover = each_url
            break

            # Manager will not be aware of updates to items. Must append new item.

    # Catch no match
    else:
        print(os.getpid(), '__Error__ (1) not found in checkedurls_man_list:', url)
        return

    ## combine next two sections
    ## Remove old entry
    with lock:
        try:
            checkedurls_man_list.remove(remover)
        except Exception as errex:
            print(os.getpid(), '__Error__ (2) not found in checkedurls_man_list:', url)
            print(errex)
            return
            
    ## Append new entry
    new_i = [url, conf_val]
    with lock:
        try:
            checkedurls_man_list.append(new_i)
            print(os.getpid(), 'Updated outcome for / with:', url, conf_val)
        except Exception as errex:
            print(os.getpid(), '__Error__ (3) not found in checkedurls_man_list:', url)
            print(errex)
            

# Define HTML request function
def html_requester_f(workingurl, current_crawl_level, jbw_type, errorurls_man_dict, portalurl, sort_dict):

    ## Ignore SSL certificate errros
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context

    '''
    >>> context = ssl.SSLContext()
    >>> context.verify_mode = ssl.CERT_REQUIRED
    >>> context.check_hostname = True
    >>> context.load_verify_locations("/etc/ssl/certs/ca-bundle.crt")
    '''


    # Request html using a spoofed user agent, cookiejar, and timeout
    try:
        cj = CookieJar()
        ##
        req = urllib.request.Request(workingurl, headers={'User-Agent': user_agent_str}, unverifiable=False)
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        html = opener.open(req, timeout=10)
        
        # Catch new redirected url
        red_url = html.geturl()
        return html, red_url

    # Catch and log HTTP request errors
    except Exception as errex:

        # Retry on timeout error
        if 'timed out' in str(errex):
            print('jj_error 3: Request timeout:', workingurl)

            # Append to error log
            add_errorurls_f(workingurl, 'jj_error 3', str(errex), current_crawl_level, jbw_type, portalurl, errorurls_man_dict)

            # Declare a retry is needed
            return True, workingurl

        # Don't retry on 404 or 403 error
        elif 'HTTP Error 404:' in str(errex) or 'HTTP Error 403:' in str(errex):
            print('jj_error 4: HTTP 404/403 request:', workingurl)
            add_errorurls_f(workingurl, 'jj_error 4', str(errex), current_crawl_level, jbw_type, portalurl, errorurls_man_dict)

            # Declare not to retry
            return False, workingurl

        # Retry on other error
        else:
            print('jj_error 5: Other request', workingurl)
            add_errorurls_f(workingurl, 'jj_error 5', str(errex), current_crawl_level, jbw_type, portalurl, errorurls_man_dict)
            return True, workingurl




# Add URLs and info to the errorlog. Allows multiple errors (values) to each URL (key)
def add_errorurls_f(workingurl, err_code, err_desc, current_crawl_level, jbw_type, portalurl, errorurls_man_dict):

    # Append more values to key if key exists
    if workingurl in errorurls_man_dict:

        # Manager will not be aware of update to dict item unless you do this
        prev_item = errorurls_man_dict[workingurl]
        prev_item.append([err_code, err_desc, current_crawl_level])

        with lock:
            try:
                errorurls_man_dict[workingurl] = prev_item
            except Exception as errex:
                print(errex)

        '''
        # Assign a number to urls already in errorurls_man_dict
        num = 0
        while workingurl in errorurls_man_dict:
            num += 1
            workingurl = workingurl + '___' + str(num)

        with lock:
            errorurls_man_dict[workingurl] = [err_code, err_desc, current_crawl_level]
        print(os.getpid(), 'innn', errorurls_man_dict)
        '''

    # Create key if key doesn't exist
    else:
        with lock:
            try:
                errorurls_man_dict[workingurl] = [err_code, err_desc, current_crawl_level, jbw_type, portalurl]
            except Exception as errex:
                print(errex)

        outcome(checkedurls_man_list, workingurl, err_code)


# Define the crawling function
def scraper(all_urls_q, max_crawl_depth, checkedurls_man_list, errorurls_man_dict, skipped_pages, prog_count, total_count, jbw_tally_man_l, sort_dict):
    print(os.getpid(), os.getpid(), '====== Start scraper function ======')
    while True:

        # Get a url list from the queue
        try:
            with lock:
                working_list = all_urls_q.get(False)

        # If queue is empty wait and try again
        except queue.Empty:
            time.sleep(2)
            try:
                with lock:
                    working_list = all_urls_q.get(False)

            # Exit function if queue is empty again
            except queue.Empty:
                print(os.getpid(), os.getpid(), 'Queue empty. Closing process...')
                break



        # Begin fetching
        else:
            try:
                print(os.getpid(), 'working_list =', working_list)
                #for x in checkedurls_man_list: print(os.getpid(), x)
                # working_list contents: [workingurl, current_crawl_level, portal URL, jbw type]
                # Seperate working list
                workingurl = working_list[0]
                current_crawl_level = working_list[1]
                portalurl = working_list[2]
                jbw_type = working_list[3]

                ## remove this?
                ## there will never be a dup in the queue
                # Skip checked pages
                #add_to_queue_b = False
                #proceed_pass = proceed_f(workingurl, working_list, checkedurls_man_list, skipped_pages, current_crawl_level, all_urls_q, total_count, add_to_queue_b, blacklist)

                #if not proceed_pass: continue

                # Form domain by splitting after 3rd slash
                domain = '/'.join(workingurl.split('/')[:3])



                # Retry loop on request and decode errors
                loop_success = False
                for loop_count in range(3):

                    # Get html and red_url tuple
                    html_url_t = html_requester_f(workingurl, current_crawl_level, jbw_type, errorurls_man_dict, portalurl, sort_dict)


                    # Get HTML and redirected URL
                    html = html_url_t[0]
                    red_url = html_url_t[1]

                    # Prevent trivial changes (eg: https upgrade) from being viewed as different urls
                    workingurl_dup = dup_checker_f(workingurl)
                    red_url_dup = dup_checker_f(red_url)

                    # Follow redirects
                    if workingurl_dup != red_url_dup:
                        print(os.getpid(), 'Redirect from/to:', workingurl, red_url)

                        # Update checked pages conf value to redirected
                        conf_val = 'redirected'
                        outcome(checkedurls_man_list, workingurl, conf_val)

                        # Assign new redirected url
                        workingurl = red_url

                        # Skip checked pages using redirected URL
                        add_to_queue_b = False
                        proceed_pass = proceed_f(red_url, working_list, checkedurls_man_list, skipped_pages, current_crawl_level, all_urls_q, total_count, add_to_queue_b)

                        # Break request loop if redirected URL has been checked already
                        if not proceed_pass: break                   




                    # html_requester_f returns True to indicate a needed retry
                    if html_url_t[0] == True:
                        print(os.getpid(), 'Retry request loop:', workingurl)
                        continue

                    # html_requester_f returns False to indicate don't retry
                    elif html_url_t[0] == False:
                        print(os.getpid(), 'Break request loop:', workingurl)
                        break

                    # Declare successful and exit loop
                    else:
                        loop_success = True
                        print(os.getpid(), 'HTML request success:', workingurl)
                        #for x in checkedurls_man_list: print(os.getpid(), x)
                        break


                # Skip to next URL if loop is exhausted
                else:
                    print(os.getpid(), 'Loop exhausted:', workingurl)
                    #continue

                # Fatal error detection
                if loop_success == False:
                    print(os.getpid(), 'Loop failed:', workingurl)

                    ## not final if using domain as fallback?
                    # Append a final error designation
                    prev_item = errorurls_man_dict[workingurl]
                    prev_item.append('jj_final_error')

                    #with lock:
                    #    try:
                    errorurls_man_dict[workingurl] = prev_item
                    #    except Exception as errex:
                    #print(errex)


                    # If portal request failed, use domain as fallback one time
                    if current_crawl_level == 0:

                        # Skip if url is same as the domain
                        if workingurl != domain:

                            # Put fallback url into queue
                            #with lock:

                            add_to_queue_b = True
                            proceed_f(domain, working_list, checkedurls_man_list, skipped_pages, current_crawl_level, all_urls_q, total_count, add_to_queue_b)

                            #all_urls_q.put([domain, -1, portalurl, jbw_type])

                            # Add dup_checker and jbw confidence placeholder to checked pages list
                            #domain_dup = dup_checker_f(domain)
                            #checkedurls_man_list.append([domain_dup, None])

                            # Increment queue length to use as progress report
                            #total_count.value += 1

                    # Skip to next URL on fatal error
                    continue

                '''
                # Get HTML and redirected URL
                html = html_url_t[0]
                red_url = html_url_t[1]
                #print(os.getpid(), 'origandred:', workingurl, red_url)

                # Prevent trivial changes (eg: https upgrade) from being viewed as different urls
                workingurl_dup = dup_checker_f(workingurl)
                red_url_dup = dup_checker_f(red_url)

                # Follow redirects
                if workingurl_dup != red_url_dup:
                    print(os.getpid(), 'Redirect from/to:', workingurl, red_url)

                    # Skip checked pages using redirected URL
                    add_to_queue_b = False
                    proceed_pass = proceed_f(red_url, working_list, checkedurls_man_list, skipped_pages, current_crawl_level, all_urls_q, total_count, add_to_queue_b)

                    # Skip if redirected URL has been checked already
                    if not proceed_pass: continue

                    # Update checked pages conf value to redirected
                    conf_val = 'redirected'
                    outcome(checkedurls_man_list, workingurl, conf_val)

                    # Assign new redirected url
                    workingurl = red_url
                '''
                
                if html == True or html == False: 
                    print('how???', workingurl)
                    continue

                # Select body
                soup = BeautifulSoup(html, 'html5lib')
                soup = soup.find('body')

                # Clear old html to free up memory
                html = None

                if soup is None:
                    print(os.getpid(), '__Empty soup0:', workingurl)
                    continue

                # Keep a soup for finding links and another for saving visible text
                vis_soup = soup

                # Remove script, style, and empty elements
                for i in vis_soup(["script", "style"]):
                    i.decompose()

                ## unn
                # Iterate through and remove all of the hidden style attributes
                r = vis_soup.find_all('', {"style" : style_reg})
                for x in r:
                    #print(os.getpid(), 'Decomposed:', workingurl, x)
                    x.decompose()

                # Type="hidden" attribute
                r = vis_soup.find_all('', {"type" : 'hidden'})
                for x in r:
                    #print(os.getpid(), 'Decomposed:', workingurl, x)
                    x.decompose()

                # Hidden section(s) and dropdown classes
                for x in vis_soup(class_=class_reg):
                    #print(os.getpid(), 'Decomposed:', workingurl, x)
                    x.decompose()

                
                ## This preserves whitespace across lines. Prevents: 'fire departmentapparatuscode compliance'
                # Remove unnecessary whitespace. eg: multiple newlines, spaces, and all tabs
                vis_soup = str(vis_soup.text)

                ##
                vis_soup = re.sub("\s{2,}", " ", vis_soup)
                '''
                regex here
                '''


                # Use lowercase visible text for comparisons
                vis_soup = vis_soup.lower()

                if vis_soup is None:
                    print(os.getpid(), '__Empty soup1:', workingurl)

                    ## there may be links to get
                    continue


                # Set jbw type based on portal jbw type
                if working_list[3] == 'civ':
                    jobwords_high_conf = jobwords_civ_high
                    jobwords_low_conf = jobwords_civ_low
                else:
                    jobwords_high_conf = jobwords_su_high
                    jobwords_low_conf = jobwords_su_low

                # Count jobwords on the page
                jbw_count = 0
                for i in jobwords_low_conf:
                    if i in vis_soup: jbw_count += 1
                for i in jobwords_high_conf:
                    if i in vis_soup: jbw_count += 2


                # Append URL and jobword confidence to portal URL dict key
                with lock:
                    if portalurl in sort_dict.keys():
                        prev_item = sort_dict[portalurl]
                        prev_item.append([workingurl, jbw_count])
                        sort_dict[portalurl] = prev_item

                    else:
                        sort_dict[portalurl] = [[workingurl, jbw_count]]

                


                '''
                ## Catch multiple matches?
                # Attach jbw conf to URL in checkedurls_man_list
                with lock:
                    for i in checkedurls_man_list:
                        if i[0] == red_url_dup:

                            # Manager will not be aware of updates to items. Must append new item.
                            checkedurls_man_list.remove(i)
                            new_i = [red_url_dup, jbw_count]
                            checkedurls_man_list.append(new_i)
                            print(os.getpid(), i)
                            break

                    # Catch no match
                    else: print(os.getpid(), red_url_dup, 'not found in checkedurls_man_list. __Error__\n\n', 'cml=', checkedurls_man_list)
                '''




                # Search for pagination class before checking crawl level
                for i in soup.find_all(class_='pagination'):

                    # Find anchor tags
                    for ii in i.find_all('a'):

                        # Find "next" page url
                        if ii.text.lower() == 'next':

                            #Get absolute url
                            abspath = urllib.parse.urljoin(domain, ii.get('href'))

                            # Add to queue
                            print(os.getpid(), workingurl, 'Adding pagination url:', abspath)
                            add_to_queue_b = True
                            proceed_f(abspath, working_list, checkedurls_man_list, skipped_pages, current_crawl_level, all_urls_q, total_count, add_to_queue_b)



                # Start relavent crawler
                if current_crawl_level >= max_crawl_depth:
                    continue

                # Increment crawl level
                print(os.getpid(), 'Starting crawler:', working_list)
                current_crawl_level += 1

                # Seperate soup into anchor tags
                alltags = []
                for i in soup.find_all('a'):

                    # Build list of anchors and parents of single anchors
                    pp = i.parent
                    if len(pp.find_all('a')) == 1:
                        alltags.append(pp)
                    else:
                        alltags.append(i)


                # Free up some memory
                soup = None

                # Set jbws confidence based on element content
                for tag in alltags:

                    # Get element content
                    bs_contents = str(tag.text).lower()

                    # Set high conf if match is found
                    if any(www in bs_contents for www in jobwords_high_conf):
                        #print(os.getpid(), 'High conf found:', workingurl, bs_contents)
                        jobwords_ephemeral = jobwords_high_conf
                        break
                    else:
                        jobwords_ephemeral = jobwords_low_conf


                # Parse elements
                fin_l = []
                for tag in alltags:

                    # Skip elements without content
                    if tag.name == 'a':
                        if not tag.text.strip():
                            continue
                    else:
                        if not tag.a.text.strip():
                            continue

                    # Help worst offenders
                    if tag.name == 'a':
                        tag.insert(0, '>')
                        tag.insert(4, '<')
                    else:
                        tag.a.insert(0, '>')
                        tag.a.insert(4, '<')

                    # Use lower tag for bunkwords search only
                    lower_tag = str(tag).lower()

                    # Get the tag contents
                    bs_contents = str(tag.text).lower()

                    # Skip these exclusions if all links is invoked
                    ## all links should remain as an option
                    #if not all_links_arg:

                    # Proceed if the tag contents contain a high confidence jobword
                    if not any(xxx in bs_contents for xxx in jobwords_ephemeral):
                        #print(os.getpid(), 'No job words detected:', workingurl, bs_contents[:99])
                        continue
                    #else: print(os.getpid(), 'jbw match:', workingurl, bs_contents)

                    # Exclude if the tag contains a bunkword
                    if any(yyy in lower_tag for yyy in bunkwords):
                        print(os.getpid(), 'Bunk word detected:', workingurl, lower_tag[:99])
                        continue

                    # Build list of successful anchors
                    fin_l.append(tag)


                # Prepare the URL for entry into the queue
                for fin_tag in fin_l:

                    lower_tag = str(fin_tag).lower()

                    # Jbw tally
                    for i in jobwords_low_conf:
                        if i in lower_tag:
                            with lock:
                                jbw_tally_man_l.append(i)

                    for i in jobwords_high_conf:
                        if i in lower_tag:
                            with lock:
                                jbw_tally_man_l.append(i)

                    # Get url from anchor tag
                    if fin_tag.name == 'a':
                        bs_url = fin_tag.get('href')

                    # Get url from child anchor tag
                    else:
                        bs_url = fin_tag.find('a').get('href')

                    # Convert relative paths to absolute
                    abspath = urllib.parse.urljoin(domain, bs_url)

                    # Add to queue
                    add_to_queue_b = True
                    proceed_f(abspath, working_list, checkedurls_man_list, skipped_pages, current_crawl_level, all_urls_q, total_count, add_to_queue_b)




            # Catch all other errors
            except Exception as errex:
                print(os.getpid(), os.getpid(), '---- Unknown error detected. Skipping...', str(traceback.format_exc()), workingurl)
                add_errorurls_f(workingurl, 'jj_error 1', str(errex), current_crawl_level, jbw_type, portalurl, errorurls_man_dict)
                prev_item = errorurls_man_dict[workingurl]
                prev_item.append('jj_final_error')
                conf_val = 'jj_error 1'
                outcome(checkedurls_man_list, workingurl, conf_val)
                continue


            # Declare the task has finished
            finally:
                prog_count.value += 1





# Multiprocessing
if __name__ == '__main__':

    all_list = [


['City of Albany', '', 'http://www.albanyny.org', (42.6573000189, -73.7464300179)],
['City of Amsterdam', '', 'http://www.amsterdamny.gov/', (42.9387508724, -74.1884322486)],
['City of Auburn', 'http://www.auburnny.gov/public_documents/auburnny_civilservice/index', 'http://www.auburnny.gov', (42.9173899379, -76.5582099703)],
['City of Batavia', 'http://www.batavianewyork.com/fire-department/pages/employment', 'http://www.batavianewyork.com', (42.9969599591, -78.2176699417)],
['City of Beacon', '', 'http://www.cityofbeacon.org', (41.4929950346, -73.9591150045)],
['City of Binghamton', '', 'http://www.cityofbinghamton.com', (42.096111616, -75.9118477851)],
['County of Bronx', '', '', (40.8261051448, -73.9233181992)],
['County of Kings', '', '', (40.6938822504, -73.9892071663)],
['City of Buffalo', '', 'http://www.city-buffalo.com', (42.8817749713, -78.8815099994)],
['City of Canandaigua', '', 'http://www.canandaiguanewyork.gov', (42.8455649254, -77.3076599588)],
['City of Cohoes', 'http://www.cohoes.com', 'http://www.cohoes.com', (42.7746069035, -73.6996130879)],
['City of Corning', '', 'http://www.cityofcorning.com', (42.1302750887, -77.0356949537)],
['City of Cortland', '', 'http://www.cortland.org/', (42.5990905595, -76.1783437374)],
['City of Dunkirk', '', 'http://www.dunkirktoday.com/', (42.4811850595, -79.3101899642)],
['City of Elmira', 'http://www.cityofelmira.net/personnel', 'http://cityofelmira.net', (42.0915386753, -76.8030461605)],
['City of Fulton', '', 'http://www.cityoffulton.com', (43.3208530475, -76.4154790307)],
['City of Geneva', '', 'http://visitgenevany.com', (42.8676953111, -76.9826892272)],
['City of Glen Cove', '', 'http://www.glencove-li.com/', (40.8641440348, -73.6314768796)],
['City of Glens Falls', 'http://www.cityofglensfalls.com/index.aspx?nid=55', 'http://www.cityofglensfalls.com', (43.3108212205, -73.6442385422)],
['City of Gloversville', '', 'http://www.cityofgloversville.com', (43.0511472971, -74.348809909)],
['City of Hornell', '', 'http://www.cityofhornell.com', (42.3277498303, -77.6614328321)],
['City of Hudson', '', 'http://www.cityofhudson.org', (42.2492858918, -73.785717693)],
['City of Ithaca', '', 'http://www.ci.ithaca.ny.us/', (42.4388861499, -76.4984806831)],
['City of Jamestown', '', 'http://www.jamestownny.net', (42.0963517584, -79.238406786)],
['City of Johnstown', '', 'http://www.cityofjohnstown-ny.com', (43.007121272, -74.3700183349)],
['City of Kingston', 'http://kingston-ny.gov/employment', 'http://www.kingston-ny.gov', (41.927146491, -73.9961675891)],
['City of Lackawanna', 'http://www.lackawannany.gov/departments/civil-service', 'http://www.lackawannany.gov/', (42.8258990287, -78.8248276162)],
['City of Little Falls', '', 'http://cityoflittlefalls.net/', (43.0445112722, -74.8555181491)],
['City of Lockport', '', 'http://elockport.com/city-index.php', (43.1695629342, -78.695646266)],
['City of Long Beach', 'http://www.longbeachny.org/index.asp?type=b_basic&amp;sec={9c88689c-135f-4293-a9ce-7a50346bea23}', 'http://www.longbeachny.org', (40.5900218115, -73.6656186719)],
['County of New York', '', '', (40.7137100168, -74.0084949972)],
['City of Mechanicville', '', 'http://www.mechanicvilleny.gov', (42.9036815273, -73.6852842975)],
['City of Middletown', 'http://www.middletown-ny.com/departments/civil-service.html?_sm_au_=ivvrlpv4fvqpnjqj', 'http://www.middletown-ny.com', (41.4458479641, -74.4213628065)],
['City of Mount Vernon', '', 'http://www.cmvny.com', (40.9117545133, -73.8392403148)],
['City of Newburgh', 'http://www.cityofnewburgh-ny.gov/civil-service', 'http://www.CityofNewburgh-ny.gov', (41.4996853241, -74.0100472883)],
['City of New Rochelle', 'http://www.newrochelleny.com/index.aspx?nid=362', 'http://newrochelleny.com/', (40.9200100003, -73.7861600252)],
['City of New York City', '', 'http://www.nyc.gov', (0.0, 0.0)],
['City of Niagara Falls', 'http://niagarafallsusa.org/government/city-departments/human-resources-department', 'http://www.niagarafallsusa.org', (43.0958918917, -79.0551239216)],
['City of North Tonawanda', '', 'http://www.northtonawanda.org/', (43.029631249, -78.8698685116)],
['City of Norwich', 'http://www.norwichnewyork.net/human_resources.html', 'http://www.norwichnewyork.net', (42.5472650104, -75.5339550684)],
['City of Ogdensburg', 'http://www.ogdensburg.org/index.aspx?nid=97', 'http://www.ogdensburg.org', (44.6983160149, -75.4920106633)],
['City of Olean', '', 'http://www.cityofolean.org/', (42.0701950675, -78.4165549339)],
['City of Oneida', 'http://oneidacity.com/civil-servic', 'http://www.oneidacity.com/', (43.0964362165, -75.6532163874)],
['City of Oneonta', 'http://www.oneonta.ny.us/departments/personnel', 'http://www.oneonta.ny.us', (42.4550014772, -75.0601782007)],
['City of Oswego', 'http://www.oswegony.org/government/personnel', 'http://www.oswegony.org', (43.4554020797, -76.511214423)],
['City of Peekskill', 'http://www.cityofpeekskill.com/human-resources/pages/about-human-resources', 'http://www.cityofpeekskill.com', (41.2916486594, -73.9224745274)],
['City of Plattsburgh', '', 'http://www.cityofplattsburgh.com', (44.6922362704, -73.4544196285)],
['City of Port Jervis', '', 'http://www.portjervisny.org', (41.3750386924, -74.6909888012)],
['City of Poughkeepsie', 'http://cityofpoughkeepsie.com/personnel', 'http://www.cityofpoughkeepsie.com', (41.7070900861, -73.9280500496)],
['County of Queens', '', '', (40.7047341302, -73.8091406243)],
['City of Rensselaer', '', 'http://www.rensselaerny.gov', (42.6386513986, -73.7450785548)],
['City of Rochester', 'http://www.cityofrochester.gov/article.aspx?id=8589936759', 'http://www.cityofrochester.gov/', (43.1570755002, -77.6150790944)],
['City of Rome', 'https://romenewyork.com/civil-service', 'http://www.romenewyork.com', (43.2121413109, -75.4587679929)],
['City of Rye', 'http://www.ryeny.gov', 'http://www.ryeny.gov', (40.9811187479, -73.6842288189)],
['City of Salamanca', '', 'http://www.salmun.com', (42.1568122724, -78.7074083921)],
['City of Saratoga Springs', 'http://www.saratoga-springs.org/jobs.aspx', 'http://www.saratoga-springs.org', (43.0833372744, -73.7840689417)],
['City of Schenectady', 'http://www.cityofschenectady.com/208/human-resources', 'http://www.cityofschenectady.com', (42.8159999546, -73.9424600046)],
['City of Sherrill', '', 'http://www.sherrillny.org', (43.0690666949, -75.6018829703)],
['County of Richmond', '', '', (40.6430332331, -74.0771124146)],
['City of Syracuse', '', 'http://www.syrgov.net/', (43.0499913768, -76.1490777002)],
['City of Tonawanda', '', 'http://www.ci.tonawanda.ny.us/', (43.0197513973, -78.8869886541)],
['City of Troy', 'http://www.troyny.gov/departments/personnel-department', 'http://www.troyny.gov', (42.7371713848, -73.6873786047)],
['City of Utica', 'http://www.cityofutica.com/departments/civil-service/index', 'http://www.cityofutica.com', (43.1017328064, -75.2363561071)],
['City of Watertown', 'https://www.watertown-ny.gov/index.asp?nid=791', 'http://www.watertown-ny.gov/', (43.9725894821, -75.9100070734)],
['City of Watervliet', 'http://watervliet.com/city/civil-service.htm', 'http://www.watervliet.com', (42.7257595931, -73.6999508073)],
['City of White Plains', '', 'http://www.cityofwhiteplains.com', (41.0333599116, -73.7655056043)],
['City of Yonkers', 'http://www.yonkersny.gov/work/jobs-civil-service-exams', 'http://www.yonkersny.gov', (40.9317428094, -73.8972508174)],
['Town of Berne', '', 'http://berneny.org', (42.6211800914, -74.2250550942)],
['Town of Bethlehem', 'http://www.townofbethlehem.org/137/human-resources?_sm_au_=ivv8z8lp1wffsnv6', 'http://www.townofbethlehem.org', (42.6202071962, -73.8396694786)],
['Village of Ravena', '', 'http://www.villageofRavena.com', (42.4730475749, -73.8148364099)],
['Town of Coeymans', '', 'http://www.coeymans.org', (42.4693388844, -73.8091313941)],
['Village of Colonie', '', 'http://www.colonievillage.org', (42.7209845616, -73.8323003383)],
['Village of Menands', '', 'http://www.villageofmenands.com', (42.6932700928, -73.7236974306)],
['Town of Colonie', 'https://www.colonie.org/departments/civilservice', 'http://www.colonie.org', (42.7194463695, -73.7560201183)],
['Village of Green Island', '', 'http://www.villageofgreenisland.com/village/', (42.7420715022, -73.692098092)],
['Town of Green Island', '', 'http://www.villageofgreenisland.com/town/', (42.741554656, -73.6910802677)],
['Village of Altamont', '', 'http://www.altamontvillage.org/', (42.7030407847, -74.0247829213)],
['Town of Knox', '', 'http://www.knoxny.org', (42.6699854459, -74.1189933789)],
['Village of Voorheesville', '', 'http://www.villageofvoorheesville.com/', (42.6517985725, -73.9282599671)],
['Town of New Scotland', '', 'http://www.townofnewscotland.com', (42.6313429755, -73.9078152892)],
['Town of Rensselaerville', '', 'http://www.rensselaerville.com', (42.4568758048, -74.1369822302)],
['Town of Westerlo', '', 'http://townofwesterlony.com', (42.5098452965, -74.0463150929)],
['County of Albany', 'http://www.albanycounty.com/civilservice', 'http://www.albanycounty.com', (42.6500423313, -73.7542171363)],
['Village of Alfred', '', 'http://www.alfredny.org', (42.2537259067, -77.7912654453)],
['Town of Alfred', '', 'http://www.townofalfred.com/', (42.2534100076, -77.7674649392)],
['Town of Allen', '', 'http://www.alleganyco.com/local_govt/Allen/', (42.3494299997, -77.987814909)],
['Town of Alma', '', 'http://www.townofalma.org', (42.0844100067, -78.0641449635)],
['Village of Almond', '', 'http://www.alleganyco.com/local_govt/villages/Almond/', (42.3107450281, -77.8451049549)],
['Town of Almond', '', 'http://www.almondny.us', (42.3167121717, -77.7412362542)],
['Village of Belmont', '', 'http://www.belmontny.org/', (42.2229763901, -78.0344413242)],
['Town of Amity', '', 'http://www.townofamity-ny.com', (42.22322186, -78.0345899342)],
['Village of Andover', '', 'http://www.alleganyco.com/local_govt/villages/Andover/', (42.1529200271, -77.8014599238)],
['Town of Andover', '', 'http://www.alleganyco.com/local_govt/Andover/', (42.157626977, -77.7952459146)],
['Village of Angelica', '', 'http://www.angelicany.com/', (42.3066039785, -78.0157489249)],
['Town of Angelica', '', 'http://www.alleganyco.com/local_govt/Angelica/', (42.3494299997, -77.987814909)],
['Town of Belfast', '', 'http://www.alleganyco.com/local_govt/Belfast/', (42.3440569704, -78.1136709551)],
['Town of Birdsall', '', 'http://www.alleganyco.com/local_govt/Birdsall/', (42.4169000308, -77.8567649246)],
['Village of Bolivar', '', 'http://www.alleganyco.com/local_govt/villages/Bolivar/', (42.0541500429, -78.1058649788)],
['Village of Richburg', '', 'http://www.alleganyco.com/local_govt/villages/Richburg/', (42.0885000223, -78.1528299965)],
['Town of Bolivar', '', 'http://www.townofbolivar.com', (42.0678309988, -78.1673581523)],
['Village of Canaseraga', '', 'http://www.alleganyco.com/local_govt/villages/Canseraga/', (42.4605070836, -77.7839228939)],
['Town of Burns', '', 'http://www.townofburnsny.com', (42.4169000308, -77.8567649246)],
['Town of Caneadea', '', 'http://townofcaneadea.org/', (42.3878185214, -78.1534238663)],
['Town of Centerville', '', 'http://centerville.wordpress.com/', (42.4797900838, -78.2497449156)],
['Town of Clarksville', '', 'http://www.alleganyco.com/local_govt/Clarksville/', (42.2709550195, -78.3352249491)],
['Village of Cuba', '', 'http://www.cubany.org/html/vofficials.html', (42.2709550195, -78.3352249491)],
['Town of Cuba', '', 'http://www.cubany.org/', (42.2709550195, -78.3352249491)],
['Town of Friendship', '', 'http://www.townoffriendship-ny.com/', (42.1914700176, -78.1464299168)],
['Town of Genesee', '', 'http://www.alleganyco.com/local_govt/Genesee/', (41.999889095, -78.2663889579)],
['Town of Granger', '', 'http://www.grangerny.org/', (42.5241450893, -78.1724199194)],
['Town of Grove', '', 'http://townofgrove.com/', (42.4891666171, -77.9510257746)],
['Town of Hume', '', 'http://www.humetown.org', (42.4663161199, -78.1118385647)],
['Town of Independence', '', 'http://independenceny.org', (42.0365899209, -77.7682863267)],
['Town of New Hudson', '', 'http://www.newhudsonny.org', (42.2859900341, -78.2533949147)],
['Town of Rushford', '', 'http://www.rushfordny.org', (42.3839600177, -78.2481499118)],
['Town of Scio', '', 'http://townofsciony.org/', (42.1556350441, -78.0261149249)],
['Town of Ward', '', 'http://www.alleganyco.com/local_govt/Ward/', (42.2460150903, -77.9812799385)],
['Village of Wellsville', '', 'http://wellsvilleny.com', (42.1223672121, -77.9487899052)],
['Town of Wellsville', '', 'http://townofwellsvilleny.org', (42.1187388795, -77.9512214399)],
['Town of West Almond', '', 'http://www.alleganyco.com/local_govt/WAlmond/', (42.3107450281, -77.8451049549)],
['Town of Willing', '', 'http://willingny.org', (42.0575165342, -77.9161613671)],
['Town of Wirt', '', 'http://www.alleganyco.com/local_govt/Wirt/', (42.1914700176, -78.1464299168)],
['County of Allegany', 'http://www.alleganyco.com/departments/human-resources-civil-service', 'http://www.alleganyco.com', (42.2460150903, -77.9812799385)],
['Town of Barker', '', 'http://www.gobroomecounty.com/files/community/pdfs/TownofBarker.pdf', (42.2531900918, -75.9071249281)],
['Town of Binghamton', '', 'http://www.townofbinghamton.com', (42.0686416183, -75.9110877708)],
['Town of Chenango', '', 'http://www.townofchenango.com/', (42.1744271365, -75.8861303927)],
['Town of Colesville', '', 'http://townofcolesville.org/', (42.2646950057, -75.673000038)],
['Town of Conklin', '', 'http://www.townofconklin.org', (42.0331000009, -75.8186400293)],
['Village of Port Dickinson', '', 'http://www.portdickinsonny.us/', (42.1383415793, -75.8951578505)],
['Town of Dickinson', '', 'http://www.townofdickinson.com', (42.1192815531, -75.9109978392)],
['Town of Fenton', '', 'http://www.townoffenton.com', (42.1985900785, -75.7638950331)],
['Town of Kirkwood', '', 'http://www.townofkirkwood.org', (42.0904780165, -75.823344977)],
['Village of Lisle', '', '', (42.3332200204, -76.0438549349)],
['Town of Lisle', '', 'http://www.gobroomecounty.com/community/municipalities/lisle', (42.3332200204, -76.0438549349)],
['Town of Maine', '', 'http://townofmaine.org/', (42.2364600713, -76.0557149238)],
['Town of Nanticoke', '', 'http://townofnanticokeny.com', (42.2364600713, -76.0557149238)],
['Village of Deposit', '', 'http://www.villageofdeposit.org/', (42.0604616119, -75.4256780975)],
['Town of Sanford', '', '', (42.0604616119, -75.4256780975)],
['Village of Whitney Point', '', 'http://www.whitneypoint.org', (42.3355450776, -75.9413549145)],
['Town of Triangle', '', 'http://www.gobroomecounty.com/files/legis/County%20Guides/TOWN%20OF%20TRIANGLE.pdf', (42.3290650823, -75.9656850214)],
['Village of Endicott', '', 'http://www.endicottny.com', (42.0977455903, -76.0502180091)],
['Village of Johnson City', '', 'http://www.villageofjc.com/', (42.1153868841, -75.9552031604)],
['Town of Union', 'http://www.townofunion.com', 'http://www.townofunion.com', (42.1063786671, -76.0262464043)],
['Town of Vestal', 'http://www.vestalny.com/departments/human_resources/job_opportunities.php', 'http://www.vestalny.com/', (42.0826216281, -76.0652077881)],
['Village of Windsor', '', '', (42.0579599995, -75.5658100352)],
['Town of Windsor', '', 'http://www.windsorny.org', (42.0779615648, -75.6394680088)],
['County of Broome', 'http://www.gobroomecounty.com/personnel/cs', 'http://www.gobroomecounty.com', (42.0965522359, -75.910754661)],
['Village of Allegany', '', 'http://www.allegany.org/index.php?Village%20of%20Allegany', (42.0866911608, -78.4897490579)],
['Town of Allegany', '', 'http://www.allegany.org/index.php?Town%20of%20Allegany', (42.0912623873, -78.4956287121)],
['Town of Ashford', '', 'http://ashfordny.org', (42.4214000838, -78.6416749168)],
['Town of Carrollton', '', 'http://www.carrolltonny.org/index.htm', (42.0491000722, -78.6465699268)],
['Town of Coldspring', '', 'http://www.cold-springny.org/', (42.1103805301, -78.9037920001)],
['Town of Conewango', '', '', (42.1486850452, -78.9442349873)],
['Village of South Dayton', '', '', (42.3605150822, -79.0837199675)],
['Town of Dayton', '', 'http://daytonny.org', (42.3975141603, -79.0011372859)],
['Town of East Otto', '', 'http://www.eastottony.org/', (42.3910997966, -78.754543364)],
['Village of Ellicottville', '', 'http://www.ellicottvillegov.com', (42.2753569189, -78.6732948711)],
['Town of Ellicottville', '', 'http://www.ellicottvillegov.com', (42.2753569189, -78.6732948711)],
['Town of Farmersville', '', 'http://farmersvilleny.org', (42.3863171837, -78.3774224167)],
['Village of Franklinville', '', 'http://franklinvilleny.org', (42.3322479936, -78.461222759)],
['Town of Franklinville', '', 'http://franklinvilleny.org', (42.3336850136, -78.4333549939)],
['Town of Freedom', '', 'http://www.freedomny.org', (42.4980672618, -78.3705102901)],
['Town of Great Valley', '', 'http://www.greatvalleyny.org', (42.1943500062, -78.6579789542)],
['Town of Hinsdale', '', 'http://hinsdaleny.org', (42.2538621085, -78.4154698957)],
['Town of Humphrey', '', 'http://humphreytownship.com', (42.2132550189, -78.595034911)],
['Town of Ischua', '', '', (42.2054550602, -78.4066399194)],
['Town of Leon', '', 'http://www.leonny.org', (42.2223850153, -79.0717098986)],
['Village of Little Valley', '', 'http://www.villageoflittlevalley.org/', (42.2488904361, -78.7988972638)],
['Town of Little Valley', '', 'http://www.littlevalleyny.org/', (42.2495188986, -78.7963717379)],
['Town of Lyndon', '', 'http://lyndontown.org', (42.305111125, -78.3494486226)],
['Town of Machias', '', 'http://www.machiasny.org/', (42.4189658219, -78.4951916735)],
['Town of Mansfield', '', 'http://mansfieldny.org', (42.2360400371, -78.8135349038)],
['Town of Napoli', '', 'http://www.napoliny.org/', (42.2030549332, -78.8914773577)],
['Village of Cattaraugus', '', 'http://www.cattaraugusny.org/html/vgov.html', (42.330066068, -78.8686291691)],
['Town of New Albion', '', 'http://www.cattaraugusny.org/html/tgove.html', (42.330066068, -78.8686291691)],
['Town of Olean', '', '', (42.0627022203, -78.4423418414)],
['Town of Otto', '', 'http://www.ottony.org/', (42.4353880298, -78.8376479306)],
['Town of Perrysburg', '', 'http://www.perrysburgny.org/', (42.45648108, -79.00406993)],
['Village of Gowanda', '', 'http://www.villageofgowanda.com', (42.4634697488, -78.9343601051)],
['Town of Persia', '', 'http://www.persiany.org/', (42.4627883432, -78.9356114561)],
['Village of Portville', '', 'http://www.portvilleny.net/', (42.0385176769, -78.3401795447)],
['Town of Portville', '', 'http://www.portville-ny.org', (42.0415100242, -78.3313999027)],
['Town of Randolph', '', 'http://randolphny.net/', (42.1627566482, -78.973160715)],
['Town of Red House', '', '', (42.0535950252, -78.8093599693)],
['Town of Salamanca', '', 'http://townofsalamanca.org', (42.0535950252, -78.8093599693)],
['Town of South Valley', '', 'http://southvalleyny.org', (42.032853544, -78.9946116554)],
['Village of Delevan', '', '', (42.4300180233, -78.4843919237)],
['Town of Yorkshire', '', 'http://yorkshireny.org', (42.5271512307, -78.4699741233)],
['County of Cattaraugus', 'http://www.cattco.org/jobs', 'http://www.cattco.org', (42.2521553173, -78.8005762825)],
['Village of Cayuga', '', 'http://www.cayugacounty.us/towns/A-G/VillageofCayuga.aspx', (42.9178123288, -76.7298148094)],
['Town of Aurelius', '', 'http://www.cayugacounty.us/portals/1/Aurelius/', (42.9173899379, -76.5582099703)],
['Village of Weedsport', '', 'http://villageofweedsport.org/', (43.0479236644, -76.5612696579)],
['Town of Brutus', '', 'http://townofbrutus.org/', (43.0543711922, -76.5591678415)],
['Village of Cato', '', 'http://www.villageofcatony.com/', (43.1830999263, -76.5682399762)],
['Village of Meridian', '', '', (43.1664523476, -76.5411349915)],
['Town of Cato', '', 'http://www.cayugacounty.us/portals/1/Townofcato', (43.157537901, -76.5470230161)],
['Town of Conquest', '', 'http://www.cayugacounty.us/portals/1/conquest', (43.058139911, -76.6582449516)],
['Town of Fleming', '', 'http://www.cayugacounty.us/portals/1/fleming', (42.861587053, -76.5787164409)],
['Town of Genoa', '', 'http://www.cayugacounty.us/portals/1/genoa', (42.6769843437, -76.5875818602)],
['Town of Ira', '', 'http://www.cayugacounty.us/portals/1/ira', (43.1830999263, -76.5682399762)],
['Village of Aurora', '', 'http://www.auroranewyork.us/', (42.7580387155, -76.7032500194)],
['Town of Ledyard', '', 'http://www.cayugacounty.us/towns/H-P/Ledyard.aspx', (42.7356632048, -76.6668674628)],
['Town of Locke', '', 'http://www.cayugacounty.us/portals/1/locke', (42.6172200655, -76.4924449414)],
['Village of Port Byron', '', '', (43.0350670149, -76.6232129574)],
['Town of Mentz', '', 'http://www.townofmentz.com/', (43.058139911, -76.6582449516)],
['Town of Montezuma', '', 'http://www.cayugacounty.us/portals/1/montezuma/', (43.0103919408, -76.7013727203)],
['Village of Moravia', '', 'http://www.cayugacounty.us/portals/1//villageofmoravia', (42.7519949842, -76.3924849035)],
['Town of Moravia', '', 'http://www.cayugacounty.us/towns/H-P/TownofMoravia.aspx', (42.7519949842, -76.3924849035)],
['Town of Niles', '', 'http://www.cayugacounty.us/portals/1/niles', (42.7982349588, -76.3496888077)],
['Town of Owasco', '', 'http://www.cayugacounty.us/towns/H-P/Owasco.aspx', (42.9183585504, -76.5450114511)],
['Town of Scipio', '', 'http://www.cayugacounty.us/portals/1/scipio', (42.7834287413, -76.5578285915)],
['Town of Sempronius', '', 'http://www.cayugacounty.us/portals/1/sempronius', (42.7519949842, -76.3924849035)],
['Town of Sennett', '', 'http://www.cayugacounty.us/portals/1/sennett', (42.9173899379, -76.5582099703)],
['Village of Union Springs', '', 'http://unionspringsny.com/', (42.8426355443, -76.6966262298)],
['Town of Springport', '', 'http://www.cayugacounty.us/portals/1/springport', (42.8590378096, -76.6821271759)],
['Village of Fair Haven', '', 'http://www.cayugacounty.us/portals/1/fairhaven', (43.3162849352, -76.7046749342)],
['Town of Sterling', '', 'http://www.cayugacounty.us/portals/1/sterling', (43.3235037372, -76.6471275581)],
['Town of Summerhill', '', 'http://www.cayugacounty.us/portals/1/summerhill', (42.6431432985, -76.343528268)],
['Town of Throop', '', 'http://www.cayugacounty.us/portals/1/throop', (42.9956849064, -76.6774568853)],
['Town of Venice', '', 'http://www.cayugacounty.us/portals/1/venice/', (42.7464800152, -76.6759099624)],
['Town of Victory', '', 'http://www.cayugacounty.us/portals/1/townofvictory/', (43.2494549386, -76.7366299155)],
['County of Cayuga', 'http://www.cayugacounty.us/community/civilservicecommission/examannouncementsvacancies.aspx', 'http://www.cayugacounty.us/', (42.9296365304, -76.5697542093)],
['Town of Arkwright', '', 'http://www.arkwrightny.org', (42.3926916755, -79.2357567333)],
['Village of Lakewood', '', 'http://www.lakewoodny.com', (42.1036416945, -79.3284567676)],
['Town of Busti', '', 'http://www.townofbusti.com', (42.10206311, -79.3256404693)],
['Town of Carroll', '', 'http://carrollny.org/', (42.0529141909, -79.1599119511)],
['Village of Sinclairville', '', '', (42.263671665, -79.2588367032)],
['Town of Charlotte', '', 'http://www.charlotteny.org/', (42.263009019, -79.2583801208)],
['Village of Mayville', '', 'http://www.villageofmayville.com/', (42.2374150269, -79.5003899753)],
['Town of Chautauqua', '', 'http://www.townofchautauqua.com/', (42.2536116964, -79.5047366211)],
['Village of Cherry Creek', '', '', (42.3091400317, -79.1395299292)],
['Town of Cherry Creek', '', 'http://cherrycreekny.org/', (42.3091400317, -79.1395299292)],
['Town of Clymer', '', 'http://www.townofclymer.org/', (42.0208140612, -79.6278259288)],
['Town of Dunkirk', '', 'http://www.dunkirkny.org/', (42.4641042489, -79.3683189189)],
['Village of Bemus Point', '', 'http://www.bemuspointny.org/', (42.157798107, -79.3934899864)],
['Town of Ellery', '', 'http://www.elleryny.org', (42.159260957, -79.3907878507)],
['Village of Celoron', '', 'http://celoronny.org/', (42.1098600859, -79.2819999891)],
['Village of Falconer', '', 'http://falconerny.org/', (42.11741174, -79.1992667464)],
['Town of Ellicott', '', 'http://www.townofellicott.com', (42.1163817232, -79.1924267821)],
['Town of Ellington', '', 'http://ellingtonny.org', (42.2169500752, -79.1077749786)],
['Town of French Creek', '', 'http://frenchcreekny.org', (42.0516000768, -79.6695299528)],
['Town of Gerry', '', 'http://gerryny.us/', (42.2272750209, -79.1734199104)],
['Village of Forestville', '', '', (42.4711016351, -79.1801467718)],
['Village of Silver Creek', '', 'http://www.silvercreekny.com/', (42.5456716108, -79.1694566975)],
['Town of Hanover', '', 'http://www.townofhanover.org', (42.5239200857, -79.1708899292)],
['Village of Panama', '', 'http://www.panamany.org/', (42.0750052239, -79.4805407269)],
['Town of Harmony', '', 'http://thetownofharmony.com', (42.0438176931, -79.4125474131)],
['Town of Kiantone', '', 'http://kiantoneny.org', (42.0639317596, -79.2060667857)],
['Town of Turin', '', '', (43.6275423897, -75.4098533951)],
['Town of Mina', '', 'http://www.townofmina.info/', (42.1245950703, -79.7401149527)],
['Town of North Harmony', '', 'http://www.townofnorthharmony.com', (42.1550150911, -79.406039923)],
['Town of Poland', '', 'http://www.polandny.org/', (42.1582217389, -79.1014368089)],
['Village of Fredonia', '', '', (42.4138950659, -79.3277049103)],
['Town of Pomfret', '', 'http://www.townofpomfretny.com/', (42.4408616576, -79.3313166939)],
['Village of Brocton', '', 'http://www.villageofbrocton.com/', (42.3972730962, -79.4521148693)],
['Town of Portland', '', 'http://www.town.portland.ny.us/', (42.382120035, -79.4334249001)],
['Town of Ripley', '', 'http://www.ripley-ny.com/', (42.2285750799, -79.6962149495)],
['Town of Sheridan', '', '', (42.4879350443, -79.2371199445)],
['Village of Sherman', '', '', (42.1567863239, -79.5972793356)],
['Town of Sherman', '', '', (42.1598450514, -79.6002499052)],
['Village of Cassadaga', '', 'http://www.cassadaganewyork.org/', (42.3425300248, -79.3111541755)],
['Town of Stockton', '', '', (42.3454716652, -79.3082567058)],
['Town of Villenova', '', '', (42.3751560759, -79.1262230217)],
['Village of Westfield', '', 'http://www.villageofwestfield.org/', (42.3222016965, -79.5760065773)],
['Town of Westfield', '', 'http://www.townofwestfield.org', (42.3222016965, -79.5760065773)],
['County of Chautauqua', 'http://www.co.chautauqua.ny.us/314/human-resources', 'http://www.co.chautauqua.ny.us', (42.2542873629, -79.505121387)],
['Village of Wellsburg', '', 'http://villageofwellsburg.com/blog/', (42.0115259327, -76.7287556661)],
['Town of Ashland', '', 'http://www.townofashland.net', (42.0220900548, -76.7656799332)],
['Town of Baldwin', '', 'http://www.chemungcounty.com/index.asp?pageId=231', (42.0900150877, -76.692244932)],
['Town of Big Flats', '', 'http://www.bigflatsny.gov', (42.1410521878, -76.9350312079)],
['Town of Catlin', '', 'http://townofcatlin.com', (42.2526830657, -77.0340368918)],
['Town of Chemung', '', 'http://www.townofchemung.com', (42.0723193921, -76.5773407709)],
['Village of Elmira Heights', '', 'http://www.elmiraheights.org/', (42.1278013373, -76.8221350781)],
['Town of Elmira', '', 'http://www.townofelmira.com', (42.0778886082, -76.8443424656)],
['Town of Erin', '', 'http://townoferin.org', (42.1789459081, -76.692547363)],
['Village of Horseheads', '', 'http://horseheads.org/', (42.1666852708, -76.8205623367)],
['Town of Horseheads', '', 'http://www.townofhorseheads.org', (42.189701836, -76.8247573485)],
['Town of Southport', '', 'http://townofsouthport.com/', (42.0554070686, -76.8184223825)],
['Village of Van Etten', '', '', (42.2526600623, -76.6294349116)],
['Town of Van Etten', '', 'http://www.chemungcounty.com/index.asp?pageId=242', (42.2526600623, -76.6294349116)],
['Village of Millport', '', 'http://vlgmillport-ny.webs.com/', (42.2640133848, -76.8341197242)],
['Town of Veteran', '', '', (42.252195001, -76.8265438763)],
['County of Chemung', 'http://www.chemungcountyny.gov/departments/a_-_f_departments/civil_service_personnel/index.php', 'http://www.chemungcounty.com', (42.090074049, -76.8020720024)],
['Village of Afton', '', '', (42.2248651946, -75.5283303376)],
['Town of Afton', '', 'http://townofafton.com', (42.2403750327, -75.5434350608)],
['Village of Bainbridge', '', 'http://bainbridgeny.org/', (42.2940429101, -75.4786615592)],
['Town of Bainbridge', '', 'http://bainbridgeny.org', (42.2940429101, -75.4786615592)],
['Town of Columbus', '', 'http://www.columbusny.us/', (42.6828800835, -75.4590800354)],
['Town of Coventry', '', 'http://townofcoventryny.com/', (42.3105728597, -75.6385938941)],
['Town of German', '', '', (42.5068100881, -75.7730950625)],
['Village of Greene', '', 'http://www.nygreene.com/villageofgreene.htm', (42.3784250739, -75.868599911)],
['Town of Greene', '', 'http://www.nygreene.com/', (42.3297871951, -75.7709636724)],
['Town of Guilford', '', 'http://www.guilfordny.com/', (42.4020415061, -75.4531280101)],
['Town of Lincklaen', '', '', (42.6594150689, -75.7700200595)],
['Town of McDonough', '', 'http://mcdonoughny.com', (42.5068100881, -75.7730950625)],
['Village of New Berlin', '', 'http://thevillageofnewberlin.org/', (42.6022050317, -75.3575400824)],
['Town of New Berlin', '', 'http://www.townofnewberlin.org', (42.6237311531, -75.3323014041)],
['Town of North Norwich', '', '', (42.6166150947, -75.5270900909)],
['Town of Norwich', '', 'http://www.townofnorwich.homestead.com', (42.5205477763, -75.5106178428)],
['Town of Otselic', '', '', (42.6475115011, -75.7846578611)],
['Village of Oxford', '', 'http://www.oxfordny.com/government/village/index.php', (42.440460069, -75.6294900965)],
['Town of Oxford', '', 'http://www.townofoxfordny.com', (42.440460069, -75.6294900965)],
['Town of Pharsalia', '', '', (42.6181650396, -75.6629850223)],
['Town of Pitcher', '', '', (42.5991500145, -75.8400849184)],
['Town of Plymouth', '', '', (42.5972447348, -75.5923254743)],
['Town of Preston', '', '', (42.5051256423, -75.5973663456)],
['Village of Earlville', '', '', (42.7402425003, -75.5449032275)],
['Village of Sherburne', '', 'http://www.sherburne.org', (42.6782768738, -75.4999970008)],
['Town of Sherburne', '', 'http://www.townofsherburne.net/', (42.6788514318, -75.5001079766)],
['Town of Smithville', '', 'http://smithvilleny.com', (42.4421050338, -75.8732699219)],
['Village of Smyrna', '', '', (42.6836600063, -75.6225500848)],
['Town of Smyrna', '', '', (42.6836600063, -75.6225500848)],
['County of Chenango', 'http://www.co.chenango.ny.us/personnel/examinations', 'http://www.co.chenango.ny.us', (42.5472650104, -75.5339550684)],
['Town of Altona', '', 'http://www.townofaltonany.com/', (44.8540849847, -73.6535900305)],
['Village of Keeseville', '', 'http://www.co.essex.ny.us/keeseville.asp', (44.5050099083, -73.5240900963)],
['Town of Ausable', '', '', (44.5046206188, -73.4829774354)],
['Town of Beekmantown', '', 'http://townofbeekmantown.com', (44.7750539963, -73.4801651811)],
['Town of Black Brook', '', '', (44.4424876159, -73.6746890752)],
['Village of Champlain', '', 'http://www.vchamplain.com', (44.983472492, -73.445344456)],
['Village of Rouses Point', '', 'http://www.rousesptny.com', (44.9921349273, -73.3720450307)],
['Town of Champlain', '', '', (44.9619199256, -73.439565011)],
['Town of Chazy', '', 'http://www.townofchazy.com', (44.8871625643, -73.4369157927)],
['Town of Clinton', '', 'http://www.townofclinton.com/', (44.9558861473, -73.9282292229)],
['Village of Dannemora', '', 'http://www.villageofdannemora.com/', (44.7191156936, -73.7239459385)],
['Town of Dannemora', '', 'http://www.townofdannemora.org', (44.7224699078, -73.7168650456)],
['Town of Ellenburg', '', 'http://www.nnyacgs.com/town_of_ellenburgh.html', (44.8940249646, -73.838045075)],
['Town of Mooers', '', 'http://www.mooersny.com', (44.9596049518, -73.576320087)],
['Town of Peru', '', 'http://www.perutown.com', (44.5821033279, -73.5239635555)],
['Town of Plattsburgh', '', 'http://townofplattsburgh.com', (44.7054116351, -73.5402666892)],
['Town of Saranac', '', 'http://www.townofsaranac.com', (44.6416920204, -73.7496456087)],
['Town of Schuyler Falls', '', 'http://www.schuylerfallsny.com', (44.6904610419, -73.5611959403)],
['County of Clinton', 'http://www.clintoncountygov.com/departments/personnel/personnelhomepage.htm', 'http://www.clintoncountygov.com', (44.6991863371, -73.4539137749)],
['Town of Ancram', '', 'http://www.townofancram.org', (42.0806850715, -73.6552250891)],
['Town of Austerlitz', '', 'http://www.austerlitzny.com', (42.3176250948, -73.4910200906)],
['Town of Canaan', '', 'http://www.canaannewyork.org', (42.4072000406, -73.4253600693)],
['Village of Chatham', '', 'http://www.villageofchatham.com', (42.3636263566, -73.594797144)],
['Town of Chatham', '', 'http://www.chathamnewyork.us/', (42.4790150601, -73.6635050318)],
['Village of Philmont', '', 'http://www.philmont.org/', (42.2494829071, -73.648551709)],
['Town of Claverack', '', 'http://www.townofclaverack.com', (42.2162100289, -73.7086900071)],
['Town of Clermont', '', 'http://www.clermontny.org', (42.0868587674, -73.8252404562)],
['Town of Copake', '', 'http://townofcopake.org/', (42.1113584739, -73.5567071322)],
['Town of Gallatin', '', 'http://www.gallatin-ny.org', (42.0867050963, -73.7556200535)],
['Town of Germantown', '', 'http://www.germantownny.org', (42.1219250088, -73.8590800243)],
['Town of Ghent', '', 'http://townofghent.org', (42.2969750046, -73.6406850448)],
['Town of Greenport', '', 'http://www.townofgreenport.com', (42.2562749185, -73.7588276667)],
['Town of Hillsdale', '', 'http://hillsdaleny.com', (42.2110400634, -73.5386400331)],
['Village of Kinderhook', '', 'http://villageofkinderhook.org/', (42.3956527131, -73.697588012)],
['Village of Valatie', '', 'http://www.valatievillage.com/', (42.4134025896, -73.6728977092)],
['Town of Kinderhook', '', 'http://www.kinderhook-ny.gov', (42.4428035992, -73.6635574639)],
['Town of Livingston', '', 'http://livingstontown.com', (42.1422400946, -73.7783600142)],
['Town of New Lebanon', '', 'http://www.townofnewlebanon.com', (42.4784438456, -73.3742657188)],
['Town of Stockport', '', 'http://townofstockport.org', (42.2869671206, -73.7474060922)],
['Town of Stuyvesant', '', 'http://www.stuyvesantny.us/', (42.3895900749, -73.7776022414)],
['Town of Taghkanic', '', 'http://www.taghkanic.org', (42.0867050963, -73.7556200535)],
['County of Columbia', 'https://sites.google.com/a/columbiacountyny.com/civilservice', 'http://www.columbiacountyny.com', (42.2520890389, -73.7869867318)],
['Town of Cincinnatus', '', 'http://www.cortland-co.org/Towns/Cincinnatus.htm', (42.5453970238, -75.9041289393)],
['Village of Homer', '', 'http://www.homerny.org', (42.6345615223, -76.1787241408)],
['Village of McGraw', '', 'http://www.cortland-co.org/towns/Mcgrawvillage.htm', (42.6027250772, -76.0640349282)],
['Town of Cortlandville', '', 'http://www.cortlandville.org/', (42.5807410972, -76.2102795201)],
['Town of Cuyler', '', 'http://www.cortland-co.org/towns/Cuyler.htm', (42.7560549193, -75.9280499856)],
['Town of Freetown', '', 'http://www.cortland-co.org/towns/Freetown.htm', (42.5217422356, -76.0364855967)],
['Town of Harford', '', 'http://www.cortland-co.org/towns/Harford.htm', (42.4269005957, -76.2283205081)],
['Town of Homer', '', 'http://www.townofhomer.org/', (42.6360652893, -76.1785501315)],
['Town of Lapeer', '', 'http://www.cortland-co.org/towns/Lapeer.htm', (42.4478050312, -76.0754699027)],
['Village of Marathon', '', 'http://www.cortland-co.org/towns/Marathonvillage.htm', (42.4427382852, -76.0393814303)],
['Town of Marathon', '', 'http://www.cortland-co.org/towns/Marathon.htm', (42.4478050312, -76.0754699027)],
['Town of Preble', '', 'http://www.preble-ny.org', (42.74118403, -76.1459639901)],
['Town of Scott', '', 'http://townofscott.org', (42.7327623547, -76.2443772716)],
['Town of Solon', '', 'http://www.cortland-co.org/towns/Solon.htm', (42.6027250772, -76.0640349282)],
['Town of Taylor', '', 'http://www.cortland-co.org/towns/Taylor.htm', (42.5609550109, -75.9476149203)],
['Town of Truxton', '', 'http://townoftruxton.com/', (42.7106400455, -75.9766349791)],
['Town of Virgil', '', 'http://www.virgilny.com', (42.5086887088, -76.1981164684)],
['Town of Willet', '', 'http://www.cortland-co.org/towns/Willet.htm', (42.5609550109, -75.9476149203)],
['County of Cortland', 'http://www.cortland-co.org/263/personnel-civil%20service', 'http://www.cortland-co.org/', (42.6011975211, -76.1768105767)],
['Town of Andes', '', 'http://townofandes.com', (42.1904416478, -74.7872194641)],
['Town of Bovina', '', 'http://www.bovinany.org', (42.2753150897, -74.7428550162)],
['Town of Colchester', '', 'http://www.colchesterchamber.com/', (42.0591300755, -75.0174800933)],
['Town of Davenport', '', 'http://www.delawarecounty.org/davenport.lasso', (42.4615150111, -74.8824500056)],
['Village of Delhi', '', 'http://www.co.delaware.ny.us/external/villages/delhivillage.htm', (42.3063450843, -74.9248850898)],
['Town of Delhi', '', 'http://townofdelhiny.com/', (42.2721151238, -74.9212571887)],
['Town of Deposit', '', 'http://www.delawarecounty.org/deposit.lasso', (42.0780250056, -75.4633700729)],
['Village of Franklin', '', 'http://www.co.delaware.ny.us/external/villages/franklinvillage.htm', (42.3694350548, -75.1827050963)],
['Town of Franklin', '', 'http://www.townoffranklin.com', (42.3694350548, -75.1827050963)],
['Town of Hamden', '', 'http://www.hamdenny.com', (42.138350008, -74.9731900326)],
['Village of Hancock', '', 'http://www.co.delaware.ny.us/external/villages/hancockvillage.htm', (41.9539545685, -75.2775754579)],
['Town of Hancock', '', 'http://www.hancockny.org', (41.9563795833, -75.2937408259)],
['Village of Stamford', '', 'http://www.stamfordny.com', (42.4085860437, -74.6170301692)],
['Town of Harpersfield', '', 'http://www.delawarecounty.org/harpersfield.lasso', (42.4429050335, -74.6985700573)],
['Town of Kortright', '', 'http://www.delawarecounty.org/kortright.lasso', (42.3686350596, -74.790680079)],
['Town of Masonville', '', 'http://www.masonville-ny.us/', (42.2500800235, -75.2573850043)],
['Town of Meredith', '', 'http://townofmeredith.com', (42.4236450207, -74.8312650861)],
['Village of Fleischmanns', '', 'http://www.catskill.net/fleisch', (42.1830300213, -74.5412150382)],
['Village of Margaretville', '', '', (42.1597350485, -74.6665650163)],
['Town of Middletown', '', 'http://middletowndelawarecountyny.org', (42.1391390894, -74.6602740649)],
['Town of Roxbury', '', 'http://www.roxburyny.com', (42.2952000548, -74.5812300495)],
['Village of Sidney', '', '', (42.3164895875, -75.3903805974)],
['Town of Sidney', '', 'http://www.sidneychamber.org/', (42.3221350379, -75.3956900218)],
['Village of Hobart', '', 'http://www.co.delaware.ny.us/external/villages/hobartvillage.htm', (42.3331400882, -74.6459900663)],
['Town of Stamford', '', 'http://townofstamfordny.us/', (42.3686350596, -74.790680079)],
['Town of Tompkins', '', 'http://townoftompkins.org', (42.1644600052, -75.1664750267)],
['Village of Walton', '', 'http://www.villageofwalton.com/', (42.1688318878, -75.128287858)],
['Town of Walton', '', 'http://www.townofwalton.org', (42.1676170573, -75.128930986)],
['County of Delaware', 'http://www.co.delaware.ny.us/departments/pers/jobs.htm', 'http://www.co.delaware.ny.us', (42.2775092032, -74.9160315161)],
['Town of Amenia', '', 'http://www.ameniany.gov', (41.8631900059, -73.5644650848)],
['Town of Beekman', '', 'http://www.townofbeekman.com', (41.6106931389, -73.6804454511)],
['Town of Clinton', '', 'http://www.townofclinton.com', (44.9558861473, -73.9282292229)],
['Town of Dover', '', 'http://www.TownofDoverNY.us', (41.6971665644, -73.5778413253)],
['Town of East Fishkill', 'http://www.eastfishkillny.org/government/employment.htm', 'http://www.eastfishkillny.org', (41.5733857347, -73.8067873589)],
['Village of Fishkill', '', 'http://www.vofishkill.com', (41.5356456714, -73.9028927917)],
['Town of Fishkill', '', 'http://www.fishkill-ny.gov', (41.5261876574, -73.9224022956)],
['Town of Hyde Park', '', 'http://www.hydeparkny.us', (41.7796900263, -73.9204350286)],
['Town of LaGrange', '', 'http://www.lagrangeny.org', (41.6618733165, -73.7964687716)],
['Town of Milan', '', 'http://www.milan-ny.gov', (41.9550242074, -73.7655031529)],
['Village of Millerton', '', 'http://www.villageofmillerton.com/', (41.9552465996, -73.5097033308)],
['Town of North East', '', 'http://www.townofnortheastny.gov', (41.9974650529, -73.5453650384)],
['Village of Pawling', '', 'http://www.villageofpawling.org/', (41.5624500776, -73.600667761)],
['Town of Pawling', '', 'http://www.pawling.org', (41.5691937853, -73.5995282143)],
['Town of Pine Plains', '', 'http://www.pineplains-ny.gov', (41.9724844107, -73.6327752702)],
['Town of Pleasant Valley', '', 'http://pleasantvalley-ny.gov', (41.7427226147, -73.82839409)],
['Village of Wappingers Falls', '', 'http://www.wappingersfallsny.gov/', (41.5970243403, -73.9175311838)],
['Town of Poughkeepsie', 'http://www.townofpoughkeepsie.com/human_resources/index.html?_sm_au_=ivv8z8lp1wffsnv6', 'http://www.townofpoughkeepsie.com', (41.6934697227, -73.8886993083)],
['Village of Red Hook', '', 'http://www.redhooknyvillage.org/', (41.9792069627, -73.8831240169)],
['Village of Tivoli', '', 'http://www.tivoliny.org', (42.0524549591, -73.9113811057)],
['Town of Red Hook', '', 'http://www.redhook.org', (41.9792069627, -73.8831240169)],
['Town of Stanford', '', 'http://www.townofstanford.org', (41.8699776708, -73.7038511328)],
['Town of Wappinger', '', 'http://www.townofwappinger.us', (41.5852810099, -73.9183699215)],
['Village of Millbrook', '', 'http://www.village.millbrook.ny.us/', (41.7866626033, -73.6921995111)],
['Town of Washington', '', 'http://www.washingtonny.org', (41.7896150258, -73.678160088)],
['County of Dutchess', '', 'http://www.dutchessny.gov', (41.7035996228, -73.9296264246)],
['Village of Alden', '', 'http://www2.erie.gov/village_alden/', (42.9001712214, -78.4910883099)],
['Town of Alden', '', 'http://www.alden.erie.gov', (42.9396224062, -78.548675907)],
['Village of Williamsville', '', 'http://www.village.williamsville.ny.us', (42.9624030704, -78.7457478671)],
['Town of Amherst', 'http://www.amherst.ny.us', 'http://www.amherst.ny.us', (42.9625609177, -78.7447535978)],
['Village of East Aurora', '', 'http://www.east-aurora.ny.us', (42.7676955077, -78.6134360486)],
['Town of Aurora', '', 'http://www.townofaurora.com', (42.7599617828, -78.6123372215)],
['Town of Boston', '', 'http://www.townofboston.com', (42.6523899673, -78.7445255027)],
['Village of Farnham', '', '', (42.5932091339, -79.0830689469)],
['Town of Brant', '', 'http://brantny.com', (42.5887297556, -79.0135760829)],
['Village of Depew', '', 'http://www.villageofdepew.org/', (42.9047156665, -78.6862756783)],
['Village of Sloan', '', 'http://www.villageofsloan.org/', (42.8953534819, -78.7937737094)],
['Town of Cheektowaga', '', 'http://tocny.org', (42.9035640605, -78.7525961014)],
['Town of Clarence', '', 'http://www2.erie.gov/clarence/', (42.9887349781, -78.6086899406)],
['Town of Colden', '', 'http://townofcolden.com', (42.6434242255, -78.6846651717)],
['Town of Collins', '', 'http://www.townofcollins.com', (42.5047950539, -78.8725099862)],
['Village of Springville', '', 'http://www.villageofspringvilleny.com/', (42.5088250316, -78.6675810286)],
['Town of Concord', '', 'http://townofconcordny.com/', (42.5095087985, -78.6662587197)],
['Town of Eden', '', 'http://www.edenny.gov', (42.652218051, -78.8954131397)],
['Town of Elma', '', 'http://www.elmanewyork.com', (42.8144495427, -78.6386479206)],
['Village of Angola', '', 'http://www.villageofangola.org/', (42.6375457755, -79.028767845)],
['Town of Evans', '', 'http://townofevans.org', (42.6465615815, -79.0418825569)],
['Town of Grand Island', '', 'http://www.grand-island.ny.us', (43.0228965799, -78.9650837465)],
['Village of Blasdell', '', 'http://wwvillageofblasdell.com', (42.7979907414, -78.8301465474)],
['Village of Hamburg', '', 'http://www.villagehamburg.com', (42.716052715, -78.8333786123)],
['Town of Hamburg', '', 'http://www.townofhamburgny.com/', (42.7295660126, -78.8254812756)],
['Town of Holland', '', 'http://www.townofhollandny.com', (42.642860282, -78.5422023955)],
['Village of Lancaster', '', 'http://www.lancastervillage.org/', (42.9003064951, -78.6701676619)],
['Town of Lancaster', '', 'http://www.lancasterny.gov', (42.9011803771, -78.6700997753)],
['Town of Marilla', '', 'http://townofmarilla.com', (42.8277969312, -78.5548739844)],
['Village of Akron', '', 'http://www.erie.gov/akron', (43.0197698751, -78.5018929943)],
['Town of Newstead', '', 'http://www.erie.gov/newstead', (43.0121069072, -78.5032533414)],
['Village of North Collins', '', 'http://www.northcollinsny.org/', (42.5948492044, -78.9405290148)],
['Town of North Collins', '', 'http://www.northcollinsny.org', (42.5941035007, -78.9406039587)],
['Village of Orchard Park', '', 'http://www.orchardparkvillage.org/', (42.7665492307, -78.7434387695)],
['Town of Orchard Park', '', 'http://www.orchardparkny.org', (42.7665492115, -78.743438805)],
['Town of Sardinia', '', 'http://www.erie.gov/sardinia/', (42.5428912805, -78.5087036506)],
['Village of Kenmore', '', 'http://www.villageofkenmore.org/', (42.9636910128, -78.8697615625)],
['Town of Tonawanda', '', 'http://www.tonawanda.ny.us/', (42.9636910128, -78.8697615625)],
['Town of Wales', '', 'http://www.townofwales.com', (42.7684139896, -78.5332259367)],
['Town of West Seneca', '', 'http://www.westseneca.net', (42.8334249546, -78.7547809834)],
['County of Erie', 'http://www.erie.gov/employment', 'http://www2.erie.gov/', (42.8840200109, -78.876696021)],
['Town of Chesterfield', '', 'http://www.co.essex.ny.us/chesterfield.asp', (44.5032949446, -73.4808040496)],
['Town of Crown Point', '', 'http://townofcrownpoint.com/', (43.9572549501, -73.5189050382)],
['Town of Elizabethtown', '', 'http://etownny.com/', (44.2148610309, -73.5938684886)],
['Town of Essex', '', 'http://www.essexnewyork.org', (44.3094459904, -73.3516430421)],
['Town of Jay', '', 'http://www.jayny.com', (44.4391169518, -73.6777500385)],
['Town of Keene', '', 'http://www.townofkeeneny.com/', (44.2653849381, -73.7956100828)],
['Town of Lewis', '', 'http://www.lewisny.com', (44.2761210406, -73.5626885381)],
['Town of Minerva', '', 'http://www.townofminerva.com', (43.8560599874, -74.0418000911)],
['Village of Port Henry', '', 'http://www.porthenrymoriah.com/living-here/village-port-henry', (44.0344089422, -73.4622130751)],
['Town of Moriah', '', 'http://www.townofmoriah.com/', (44.043178603, -73.4582392108)],
['Town of Newcomb', '', 'http://www.newcombny.com/', (44.0048299293, -74.1379450763)],
['Village of Lake Placid', '', 'http://villageoflakeplacid.ny.gov/', (44.2822734829, -73.9824911064)],
['Village of Saranac Lake', '', 'http://www.saranaclakeny.gov/', (44.3241392077, -74.1319860191)],
['Town of North Elba', '', 'http://www.northelba.org', (44.2823310033, -73.9823284079)],
['Town of North Hudson', '', 'http://northhudsonny.com', (43.998849973, -73.7997100944)],
['Town of Schroon', '', 'http://www.schroon.net/', (43.8367049578, -73.7611950669)],
['Town of St Armand', '', 'http://www.co.essex.ny.us/starmand.asp', (44.4078096998, -74.0866613061)],
['Town of Ticonderoga', '', 'http://www.townofticonderoga.com', (43.8488190028, -73.4237901363)],
['Town of Westport', '', 'http://www.westportny.net', (44.1858079741, -73.435536252)],
['Town of Willsboro', '', 'http://www.townofwillsboro.com', (44.3714509733, -73.3966785941)],
['Town of Wilmington', '', 'http://www.townofwilmington.org', (44.3779249515, -73.8409750013)],
['County of Essex', 'http://www.co.essex.ny.us/jobs.asp', 'http://www.co.essex.ny.us/', (44.2071799834, -73.6125850881)],
['Town of Bangor', '', '', (44.7870149025, -74.4135700726)],
['Town of Bellmont', '', 'http://www.nnyacgs.com/town_of_belmont.html', (44.8580349274, -74.0336850122)],
['Town of Bombay', '', 'http://www.bombayny.us', (44.9231578063, -74.5770906645)],
['Town of Brandon', '', 'http://www.nnyacgs.com/town_of_brandon.html', (44.7870149025, -74.4135700726)],
['Town of Brighton', 'http://www.townofbrighton.org/index.aspx?nid=219&amp;_sm_au_=ivv8z8lp1wffsnv6', 'http://www.townofbrighton.org', (44.4763099718, -74.3058500443)],
['Village of Burke', '', '', (44.9033154295, -74.1728924443)],
['Town of Burke', '', '', (44.9214526174, -74.1477666963)],
['Village of Chateaugay', '', '', (44.8194049979, -74.0589850282)],


]







    # Advanced options
    max_crawl_depth = 2
    num_procs = 16


    # URL queues
    all_urls_q = Queue() # Put all portal and working URLs in this queue

    # Create manager to share objects between processes
    manager = Manager()

    # Debugging
    jbw_tally_man_l = manager.list() # Used to determine the frequency that jbws are used

    # Set paths to files
    queue_path = os.path.join(dater_path, 'queue.txt')
    checked_path = os.path.join(dater_path, 'checked_pages.txt')
    error_path = os.path.join(dater_path, 'errorlog.txt')



    all_urls_q = Queue() # Put all portal and working URLs in this queue
    checkedurls_man_list = manager.list() # URLs that have been checked and their outcome. eg: jbw conf or error
    errorurls_man_dict = manager.dict() # URLs that have resulted in an error
    sort_dict = manager.dict() # Put URLs and there jbw conf

    
    # Put school URLs in queue
    for i in all_list:

        em_url = i[1]
        homepage = i[2]

        # Skip if home page is missing
        if not homepage.strip(): continue

        # Skip if em URL is present
        if em_url.strip(): continue

        # Skip if em URL is marked
        if em_url.startswith('_'): continue

        # Add scheme if necessary
        if not homepage.startswith('http'):
            homepage = 'http://' + homepage

        # Put civil service URLs, initial crawl level, portal url, and jbws type into queue
        all_urls_q.put([homepage, 0, homepage, 'sch'])

        # Put portal URL into checked pages
        dup_checker = dup_checker_f(homepage)
        checkedurls_man_list.append([dup_checker, None])






    # Integers to be shared between processes
    qlength = all_urls_q.qsize() # Length of the primary queue
    skipped_pages = Value('i', 0) # Number of pages that have been skipped
    prog_count = Value('i', 0) # Number of pages checked
    total_count = Value('i', qlength) # Number of pages to be checked
    waiting_procs = Value('i', 0) # Used to tell manager that proc is waiting


    # Create child processes
    for arb_var in range(num_procs):
        worker = Process(target=scraper, args=(all_urls_q, max_crawl_depth, checkedurls_man_list, errorurls_man_dict, skipped_pages, prog_count, total_count, jbw_tally_man_l, sort_dict))
        worker.start()

    # Wait until all tasks are done
    current_prog_c = None
    while len(active_children()) > 1:
        if current_prog_c != prog_count.value:
            #tmp = os.system('clear||cls')
            print(os.getpid(), ' Number of processes running =', len(active_children()), '\n Max crawl depth =', max_crawl_depth)
            print(os.getpid(), '\n\n\n\n Searching in:')
            print(os.getpid(), 'Civil Service')
            print(os.getpid(), 'School districts and charter schools')
            print(os.getpid(), 'Universities and colleges')

            print(os.getpid(), '\n\n Waiting for all processes to finish. Progress =', prog_count.value, 'of', total_count.value)
            current_prog_c = prog_count.value

           
        time.sleep(6)


        



    print(os.getpid(), '\n =======================  Search complete  =======================')



    '''
    # jbw tally
    for i in jobwords_civ_low:
        r_count = jbw_tally_man_l.count(i)
        print(os.getpid(), i, '=', r_count)

    for i in jobwords_su_low:
        r_count = jbw_tally_man_l.count(i)
        print(os.getpid(), i, '=', r_count)

    print(os.getpid(), '\n')

    for i in jobwords_civ_high:
        r_count = jbw_tally_man_l.count(i)
        print(os.getpid(), i, '=', r_count)

    for i in jobwords_su_high:
        r_count = jbw_tally_man_l.count(i)
        print(os.getpid(), i, '=', r_count)
    '''


    # Clear checked pages
    with open(checked_path, "w") as checked_file:
        checked_file.write('')

    # Write checked pages to file
    with open(checked_path, "a") as checked_file:
        for kk in checkedurls_man_list:
            checked_file.write(str(kk) + ',\n')


    # Clear errorlog
    with open(error_path, "w") as error_file:
        error_file.write('')

    # errorurls_man_dict contents: {workingurl = [err_code, err_desc, current_crawl_level, jbw_type, portalurl]}
    # Write errorlog
    with open(error_path, "a", encoding='utf8') as writeerrors:

        ## do you want a heading? needs updating
        #writeerrors.write(' Error Code \t\t\t Error Description \t\t\t current_crawl_level \t\t :: \t\t URL\n\n')

        # Replace superfluous characters and make pretty formatting
        for k, v in errorurls_man_dict.items():
            k = k.replace('[', '').replace(']', '').replace("'", '')
            writeerrors.write(k + ', ')

            v = str(v).replace('[', '').replace(']', '').replace("'", '')
            writeerrors.write(v)
            writeerrors.write('\n\n')

    # Calculate error rate
    try:
        error_rate = len(errorurls_man_dict) / len(checkedurls_man_list)
        if error_rate < 0.05: error_rate_desc = '(low error rate)'
        elif error_rate < 0.15: error_rate_desc = '(medium error rate)'
        else: error_rate_desc = '(high error rate)'
    except: error_rate_desc = '(error rate unavailable)'

    # Build portal URL errors list
    portal_error_list = []
    if len(errorurls_man_dict.items()) > 0:
        for v,k in errorurls_man_dict.items():

            # Must have current crawl level in every errorurls_man_dict entry or you'll get error here
            # List based on crawl level
            if k[2] < 1:
                portal_error_list.append(v)

    # Stop timer and display stats
    duration = datetime.datetime.now() - startTime
    print(os.getpid(), '\n\nPages checked =', len(checkedurls_man_list))
    #for x in checkedurls_man_list: print(os.getpid(), x)
    print(os.getpid(), 'Pages skipped =', skipped_pages.value, '\nDuration =', duration.seconds, 'seconds\nPage/sec/proc =', str((len(checkedurls_man_list) / duration.seconds) / num_procs)[:4], '\nErrors detected =', len(errorurls_man_dict), error_rate_desc, '\nPortal errors =', len(portal_error_list), '\n')

    # Display errors
    if len(errorurls_man_dict.values()) > 0:

        # Create tally vars as a batch
        error1_tally, error2_tally, error3_tally, error4_tally, error5_tally, error6_tally, error7_tally = (0,)*7

        # Tally error frequencies
        for i in errorurls_man_dict.values():
            if 'jj_error 1' in i: error1_tally += 1
            elif 'jj_error 2' in i: error2_tally += 1
            elif 'jj_error 3' in i: error3_tally += 1
            elif 'jj_error 4' in i: error4_tally += 1
            elif 'jj_error 5' in i: error5_tally += 1
            elif 'jj_error 6' in i: error6_tally += 1
            elif 'jj_error 7' in i: error7_tally += 1


        print(os.getpid(), '   Error code:     Description | Frequency')
        print(os.getpid(), '  -----------------------------|-------------')
        print(os.getpid(), '      Error 1:   Unknown error |', error1_tally)
        print(os.getpid(), '      Error 2:        Non-HTML |', error2_tally)
        print(os.getpid(), '      Error 3: Request timeout |', error3_tally)
        print(os.getpid(), '      Error 4:  HTTP 404 / 403 |', error4_tally)
        print(os.getpid(), '      Error 5:   Other request |', error5_tally)
        print(os.getpid(), '      Error 6:  Splash failure |', error6_tally)
        print(os.getpid(), '      Error 7:           Misc. |', error7_tally)


    print(sort_dict)


    # Display results
    with lock:
        for i in sort_dict:
            w_l = []

            # Display original full entry
            for orig_entry in all_list:
                if i == orig_entry[2]:
                    print("\n\n" + str(orig_entry) + ',')
                    break

            # Sort by jbw conf
            temp = sorted(sort_dict[i], key = lambda x: int(x[1]), reverse=True)

            for ii in temp: # List each em URL

                if i == ii[0]: continue # Exclude URL if same as homepage
                if ii in w_l: continue # Exclude dups
                print(ii[0]) # Exclude jbw conf
                w_l.append(ii)





'''
# Find matching URLs from old db
for i in sort_dict.items():
    print('\n\n=', i[0])
    for ii in i[1]:
        for iii in uni_list:
            if iii == ii[0]:
                print('Match:', iii)
'''


'''
# To include centralized services
# olas = omit. centralized and dynamic. all at: https://www.pnwboces.org/olas/#!/jobs
# recruitfront = omit. centralized. all at: https://monroe2boces.recruitfront.com/JobBoard
# interviewexchange = keep. decentralized. captcha prompt
# wnyric = keep. decentralized. omit all at: https://schoolapp.wnyric.org/ats/job_board?start_index=200
# use regex to determine pages = '<a href="/ats/job_board\?start_index=\d+">'

# Fetch from wnyric
if school_arg or uni_arg:
    wnyric_pages = re.findall('<a href="/ats/job_board\?start_index=\d+">', html, flags=re.DOTALL)

    for i in set(wnyric_pages):
        i = i.split('job_board')[1]
        i = i.split('"')[0]
        i = 'https://schoolapp.wnyric.org/ats/job_board' + i
        print(os.getpid(), i)

'''
















