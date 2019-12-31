
# Description: Crawl webpages and rank links based on likelihood of containing job postings.



# To do:
# AP and wnyric are not totally centralized? eg: https://www.applitrack.com/saugertiesk12/onlineapp/jobpostings/view.asp
# output all 4 items +
# use redirects instead of original URLs
# checked_pages has no jbw conf values. only None, redirect, or error
# dont output dups +








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

['Academy For Jewish Religion', '', 'http://ajrsem.org', (40.9364060697, -73.898634461)],

['Adelphi University', 'https://hr.adelphi.edu/position-openings', 'http://www.adelphi.edu', (40.7222430099, -73.6510515826)],

['Albany College of Pharmacy And Health Sciences', 'https://employment.acphs.edu/postings/search', 'http://www.acphs.edu', (42.6521801281, -73.7785803492)],

['Albany Law School', '', 'http://www.albanylaw.edu', (42.6500456455, -73.7775088575)],

['Albany Medical College', '', 'http://www.amc.edu', (42.6532407287, -73.7739752764)],

['Alfred University', '', 'http://www.alfred.edu', (42.2561789656, -77.7882588252)],

['Amer Academy of Dramatic Arts', '', 'http://www.aada.edu', (40.7455070816, -73.9847588977)],

['American Acad McAllister Inst', '', 'http://www.funeraleducation.org', (40.7689206361, -73.9938294193)],

['Bank Street College of Education', 'https://www.bankstreet.edu/about-bank-street/job-opportunities', 'http://www.bankstreet.edu', (40.805678904, -73.966576371)],

['Bard College', 'http://www.bard.edu/employment/employment', 'http://www.bard.edu', (42.0212190417, -73.9065792655)],

['Bard College at Brooklyn Public Central Library', 'http://www.bard.edu/employment/employment', 'http://bpi.bard.edu', (40.672385107, -73.9681647537)],

['Bard Grad Ctr For Decorative Arts', 'http://www.bard.edu/employment/employment', 'http://www.bgc.bard.edu', (40.7856118202, -73.9705318395)],

['Barnard College', 'https://careers.barnard.edu', 'http://www.barnard.edu', (40.8088109366, -73.9635231179)],

['Boricua College', '', 'http://www.boricuacollege.edu', (40.8333897817, -73.9456977179)],

['Boricua College - Bronx', '', 'http://www.boricuacollege.edu', (40.823585313, -73.9110466197)],

['Boricua College - Brooklyn', '', 'http://www.boricuacollege.edu', (40.7167069894, -73.9576172706)],

['Brooklyn Law School', 'https://www.brooklaw.edu/about-us/job-opportunities.aspx', 'http://www.brooklaw.edu', (40.6921576493, -73.9898297028)],

['Canisius College', 'http://careers.canisius.edu/cw/en-us/listing', 'http://www.canisius.edu/', (42.9255866422, -78.8534827977)],

['Cazenovia College', 'http://www.cazenovia.edu/campus-resources/human-resources/employment-opportunities', 'http://www.cazenovia.edu', (42.9318683477, -75.8540739167)],

['Christ the King Seminary', '', 'http://www.cks.edu', (42.7766998662, -78.6566123121)],

['City Seminary of New York Graduate Center', '', 'http://www.cityseminaryny.org', (40.7390307143, -73.9668120498)],

['Clarkson University', 'https://clarkson.peopleadmin.com', 'http://www.clarkson.edu/', (44.6668978047, -74.9941051289)],

['Clarkson University Capital Region', 'https://clarkson.peopleadmin.com', 'http://www.clarkson.edu', (42.8138873062, -73.9341950475)],

['Cochran Sch Nursing St John Rvrdl Ho', '', 'http://www.cochranschoolofnursing.us', (40.9687964271, -73.8863259432)],

['Cold Spring Harbor--watson School of Biological Sciences', '', 'http://www.cshl.edu/gradschool', (40.8611650109, -73.4691350824)],

['Colgate University', 'http://www.colgate.edu/working-at-colgate', 'http://www.colgate.edu', (42.8165164934, -75.5325655086)],

['Colgate-Rochester Divinity School', '', 'http://www.crcds.edu', (43.1321158158, -77.6000675596)],

['Coll New Rochelle Dist Coun 31 Cmps', 'https://www.cnr.edu/employment-opportunities', 'http://www.cnr.edu', (40.7147732989, -74.0128284296)],

['Coll New Rochelle Rosa Parks Campus', 'https://www.cnr.edu/employment-opportunities', 'http://www.cnr.edu', (40.8084367094, -73.947492888)],

['Coll of New Rochelle at NY Theo Semi', 'https://www.cnr.edu/employment-opportunities', 'http://www.cnr.edu', (40.7457240089, -73.9875609033)],

['Coll of New Rochelle Brooklyn Campus', 'https://www.cnr.edu/employment-opportunities', 'http://www.cnr.edu', (40.6800585075, -73.9458815453)],

['College of Mt St Vincent', 'https://mountsaintvincent.edu/campus-life/campus-services/human-resources/employment-opportunities', 'http://www.mountsaintvincent.edu', (40.9136881584, -73.9087379397)],

['College of New Rochelle', 'https://www.cnr.edu/employment-opportunities', 'http://www.cnr.edu', (40.901372521, -73.7815964899)],

["College of New Rochelle John Cardinal O'Connor Campus", 'https://www.cnr.edu/employment-opportunities', 'http://www.cnr.edu', (40.8166075558, -73.9203497842)],

['College of Saint Rose', 'https://strose.interviewexchange.com/jobsrchresults.jsp', 'http://www.strose.edu', (42.6646075556, -73.7860610659)],

['Columbia University', '', 'http://www.columbia.edu', (40.8079890307, -73.9620177274)],

['Concordia College', '', 'http://www.concordia-ny.edu', (40.9425657208, -73.8207636546)],

['Cooper Union For the Advancement of Science And Art', 'http://cooper.edu/work/employment-opportunities', 'http://www.cooper.edu', (40.7280657627, -73.9914604017)],

['Cornell Univ Medical Campus', 'https://hr.cornell.edu/jobs', 'http://www.weill.cornell.edu', (40.7648896034, -73.9549391409)],

['Cornell University', '', 'http://www.cornell.edu', (42.4470150296, -76.4823949559)],

['Cornell University - Cornellnyc Tech Campus', 'https://hr.cornell.edu/jobs', 'http://tech.cornell.edu', (0.0, 0.0)],

['Crouse-Irving Memorial Hospital School of Nursing', '', 'http://www.crouse.org/nursing', (43.0409937183, -76.1379398537)],

['Culinary Institute of America 697', '', 'http://www.ciachef.edu', (41.745751189, -73.9331335732)],

["D'Youville College", 'http://www.dyc.edu/about/administrative-offices/human-resources/career-opportunities.aspx', 'http://www.dyc.edu', (42.9022574547, -78.8904776633)],

['Daemen College', 'https://daemen.applicantpro.com/jobs', 'http://www.daemen.edu', (42.9640165422, -78.7899685237)],

['Davis College', 'https://www.davisny.edu/jobs', 'http://www.davisny.edu', (0.0, 0.0)],

['Dominican Coll of Blauvelt', 'https://www.dc.edu/human-resources', 'http://www.dc.edu', (41.0512617261, -73.9527385505)],

['Dowling College', '', 'http://www.dowling.edu', (40.7415915528, -73.1474167819)],

['Dowling College - Brookhaven Center', '', 'http://www.dowling.edu', (40.8278969864, -72.8819429176)],

['Elim Bible Institute & College', '', 'http://www.elim.edu', (42.908518804, -77.6147357204)],

['Ellis Medicine-Thebelanger School of Nursing', '', 'http://www.ellisbelangerschoolofnursing.org', (42.8055884888, -73.9168545562)],

['Elmira College', 'https://www.elmira.edu/Student/Offices_Resources/Employment_Opportunities/index.html', 'http://www.elmira.edu', (42.1196260543, -76.8231759498)],

['Elyon College', '', 'http://www.elyon.edu', (40.6110547033, -73.9804759397)],

['Excelsior College', 'https://jobs.excelsior.edu', 'http://www.excelsior.edu/', (42.705436733, -73.8630575803)],

['The Elmezzi Graduate School of Molecular Medicine', '', 'http://www.elmezzigraduateschool.org/', (40.7819201717, -73.7039516746)],

['Fei Tian College', '', 'http://www.feitian.edu', (41.4529346524, -74.5891858298)],

['Finger Lakes Health College of Nursing & Health Sciences', '', 'http://www.flhcon.edu', (42.8762578081, -76.9876894515)],

['Fordham Univ (Rose Hill-Lincoln Ctr)', 'https://www.fordham.edu/info/23411/job_opportunities', 'http://www.fordham.edu', (40.8611039429, -73.8875646756)],

['Fordham University - Westchester Campus', 'https://www.fordham.edu/info/23411/job_opportunities', 'http://www.fordham.edu', (41.0292387951, -73.7288980026)],

['Gamla College', '', 'http://gamlacollege.com', (40.6171572317, -73.9621890813)],

['General Theological Seminary', 'http://gts.edu/job-postings', 'http://www.gts.edu', (40.7456283873, -74.0036644478)],

['Glasgow Caledonian New York College', '', 'http://www.gcnyc.com', (40.7390307143, -73.9668120498)],

['Hamilton College', 'https://www.hamilton.edu/offices/human-resources/employment/job-opportunities', 'http://www.hamilton.edu', (43.0514413048, -75.402117956)],

['Hartwick College', 'https://www.hartwick.edu/about-us/employment/human-resources/employment-opportunities', 'http://www.hartwick.edu', (42.4610282773, -75.0701668682)],

['Hebrew Union College - Jewish Institute of Religion', 'http://huc.edu/about/employment-opportunities', 'http://www.huc.edu', (40.7288012661, -73.9948235492)],

['Helene Fuld College of Nursing', 'https://www.helenefuld.edu/employment', 'http://www.helenefuld.edu', (40.8028611543, -73.9438474104)],

['Hilbert College', 'https://www.hilbert.edu/about/human-resources/hilbert-job-openings', 'http://www.hilbert.edu', (42.7548232015, -78.8245211425)],

['Hobart & Wm Smith Colleges', 'https://www.hws.edu/offices/hr/employment/index.aspx', 'http://www.hws.edu', (42.8589157462, -76.9858302479)],

['Hofstra University-Main Campus', '', 'http://www.hofstra.edu', (40.7163803809, -73.5995207899)],

['Holy Trinity Orthodox Seminary', '', 'http://www.hts.edu', (42.9277195844, -74.9336856615)],

['Houghton College', 'http://www.houghton.edu/campus/human-resources/employment', 'http://www.houghton.edu', (42.4280063974, -78.1547581109)],

['Inst of Design & Construction', '', 'http://www.idc.edu', (40.6921634518, -73.9830600399)],

['Iona College', 'https://iona-openhire.silkroad.com/epostings/index.cfm?fuseaction=app.jobsearch', 'http://www.iona.edu', (40.9252432042, -73.7882413524)],

['Iona College Rockland Campus', '', 'http://www.iona.edu/rockland/', (41.0485317405, -73.9525586308)],

['Ithaca College', 'https://ithaca.peopleadmin.com', 'http://www.ithaca.edu', (42.4221514807, -76.5000368308)],

['Jewish Theological Semnry of America', 'http://www.jtsa.edu/jobs-at-jts', 'http://www.jtsa.edu', (40.8118490724, -73.9606737505)],

['The Juilliard School', 'https://www.juilliard.edu/jobs', 'http://www.juilliard.edu/', (40.7733956594, -73.9828002776)],

['Keuka College', 'https://www.keuka.edu/hr/employment-opportunities', 'http://www.keuka.edu', (42.6151105935, -77.0906192216)],

['Keuka College-Corning CC Campus', 'https://www.keuka.edu/hr/employment-opportunities', 'http://www.keuka.edu', (42.1166659128, -77.071690501)],

['Keuka-Onondaga Community College Branch', 'https://www.keuka.edu/hr/employment-opportunities', 'http://www.keuka.edu', (43.0061837356, -76.1981302617)],

["The King's College", 'https://www.tkc.edu/careers-at-kings', 'http://www.tkc.edu', (40.7634337245, -73.9287215064)],

['Le Moyne College', 'https://www.lemoyne.edu/Work-at-Le-Moyne', 'http://www.lemoyne.edu', (43.0491913085, -76.0848876812)],

['Long Island College Hospital Sch Nursing', '', '', (40.6830878574, -74.0000432328)],

['Long Island College Hospital School of Nursing', '', 'http://www.futurenurselich.org', (40.6908534019, -73.9977410887)],

['Long Island University - New York University Campus', '', 'http://www.liu.edu', (40.7294899346, -73.9972596293)],

['Long Island University - Riverhead', '', 'http://www.liu.edu', (40.8766617264, -72.7002490474)],

['Long Island University Central Administration', '', 'http://www.liu.edu', (40.8126010433, -73.6167466338)],

['Long Island University-Brentwood Campus', '', 'http://liu.edu/brentwood', (40.8029993911, -73.285274135)],

['Long Island University-Brooklyn Campus', '', 'http://www.liu.edu', (40.6916867462, -73.9814831539)],

['Long Island University-CW Post Campus', '', 'http://www.liu.edu', (40.8126541126, -73.616525216)],

['Long Island University-Southampton Campus', '', 'http://www.liu.edu', (40.8853530054, -72.478100023)],

['Long Island University-Westchester Campus', '', 'http://www.liu.edu', (41.039038225, -73.6962345232)],

['Louis V. Gerstner Grad Scho of Biomed Sci, Memorial Sloan-Kettering Cancer Center', '', 'http://www.sloankettering.edu', (40.7640369956, -73.9560230672)],

['Manhattan College', '', 'http://www.manhattan.edu', (40.890237552, -73.9012322052)],

['Manhattan School of Music', 'https://www.msmnyc.edu/about/employment-at-msm', 'http://msmnyc.edu', (40.8124890622, -73.9617394867)],

['Manhattanville College', 'https://www.mville.edu/about-manhattanville/human-resources', 'http://www.mville.edu', (41.0310593009, -73.7148083319)],

['Maria College of Albany', '', 'http://www.mariacollege.edu', (42.6583265456, -73.8076581449)],

['Marist College', 'http://careers.marist.edu/cw/en-us/listing', 'http://www.marist.edu', (41.7233294164, -73.9320898598)],

['Marymount Manhattan College', 'https://www.mmm.edu/offices/human-resources/Employment', 'http://www.mmm.edu', (40.7686329247, -73.9598045844)],

['Medaille College', 'http://jobs.medaille.edu', 'http://www.medaille.edu', (42.9296313432, -78.8552047502)],

['Medaille College - Rochester Campus', 'http://jobs.medaille.edu', 'http://www.medaille.edu', (43.1086317223, -77.5720499965)],

['Memorial Hospital School of Nursing', '', 'http://www.sphp.com/sons', (42.6741639047, -73.7486829022)],

['Mercy College', 'https://jobs.mercy.edu/postings/search', 'http://www.mercy.edu', (41.0213716724, -73.8699690554)],

['Mercy College - Manhattan Campus', 'https://jobs.mercy.edu/postings/search', 'http://www.mercy.edu', (40.7501618927, -73.9868612518)],

['Mercy College Bronx Campus', 'https://jobs.mercy.edu/postings/search', 'http://www.mercy.edu', (40.8524534315, -73.8378911685)],

['Mercy College-Yorktown Hts Campus', 'https://jobs.mercy.edu/postings/search', 'http://www.mercy.edu', (41.2944448671, -73.8191852919)],

['Metropolitan College of New York', 'http://www.mcny.edu/index.php', 'http://www.mcny.edu', (40.7088727965, -74.0147720915)],

['Metropolitan College of Ny-Brc', '', 'http://www.mcny.edu/mcny-bronx/', (40.8153862021, -73.9158630335)],

['Mid-America Baptist Theol Seminary - NE Branch', '', 'http://www.mabtsne.edu', (42.7513005326, -73.9177628057)],

['Molloy College', 'https://www.molloy.edu/about-molloy-college/human-resources/careers-at-molloy', 'http://www.molloy.edu', (40.6811769793, -73.628967714)],

['Montefiore School of Nursing', '', 'http://www.montefiorehealthsystem.org', (40.91208021, -73.8404194)],

['Mount Saint Mary College', 'https://www.msmc.edu/employment', 'http://www.msmc.edu', (41.513007242, -74.0147427736)],

['Mt Sinai School of Medicine', '', 'http://icahn.mssm.edu', (40.7903736896, -73.9533895103)],

['Nazareth College of Rochester', 'https://jobs.naz.edu/postings/search', 'http://www.naz.edu', (43.1039850232, -77.5234477002)],

['New School University - NYS Office of Mental Health', '', 'http://www.newschool.edu/', (42.6478465136, -73.774182006)],

['New York College of Health Professions', '', 'http://www.nycollege.edu', (40.8100017735, -73.5169487481)],

['New York College of Podiatric Medicine', '', 'http://www.nycpm.edu', (40.8049396848, -73.9406042039)],

['New York College of Traditional Chinese Medicine', '', 'http://www.nyctcm.edu', (40.7394968641, -73.6388842048)],

['New York Graduate School of Psychoanalysis', '', 'http://www.nygsp.bgsp.edu/', (40.7337598681, -73.9965400551)],

['New York Institute For Technology-Manhattan Campus', 'https://careers-nyit.icims.com/jobs/search?ss=1', 'http://www.nyit.edu', (40.7696286804, -73.982398747)],

['New York Institute of Technology - Islip Campus', 'https://careers-nyit.icims.com/jobs/search?ss=1', 'http://www.nyit.edu', (40.790602046, -73.202009032)],

['New York Institute of Technology Old Westbury Campus', 'https://careers-nyit.icims.com/jobs/search?ss=1', 'http://www.nyit.edu', (40.8101610875, -73.6032821778)],

['New York Law School', '', 'http://www.nyls.edu', (40.7180828612, -74.0071048348)],

['New York Studio School', '', 'http://www.nyss.org', (40.7325102354, -73.9972369615)],

['New York Theological Seminary', 'http://www.nyts.edu', 'http://www.nyts.edu', (40.810939099, -73.9640163243)],

['New York University', '', 'http://www.nyu.edu', (40.7296504349, -73.9970161424)],

['New York University - St. Thomas Aquinas College', '', 'http://www.nyu.edu', (41.0420416981, -73.9364386301)],

['New York University at Manhattanville College', '', 'http://www.nyu.edu', (41.0310593009, -73.7148083319)],

['Niagara University', '', 'http://www.niagara.edu', (43.1371098129, -79.0380449288)],

['Northeaster Seminary at Roberts Wesleyan College', '', 'http://www.nes.edu/', (43.1260918496, -77.7974158143)],

['NY Chiropractic College', 'http://www.nycc.edu/employment-opportunities', 'http://www.nycc.edu', (42.9114587441, -76.7538967241)],

['NY Medical College', '', 'http://www.nymc.edu', (41.08500151, -73.81006245)],

['NY School of Interior Design', '', 'http://www.nysid.edu', (40.7686703487, -73.9623794411)],

['Nyack College', 'https://www.nyack.edu/site/employment-opportunities', 'http://www.nyack.edu', (41.0861216895, -73.9300085756)],

['The New School', '', 'http://www.newschool.edu/', (40.73557935, -73.9969989)],

['The New York Academy of Art', '', 'http://www.nyaa.edu', (40.7184411618, -74.0059019288)],

['Pace University - NYC Campus', 'https://careers.pace.edu/postings/search', 'http://www.pace.edu', (40.7116591422, -74.0054227605)],

['Pace University College at White Plains', 'https://careers.pace.edu/postings/search', 'http://www.pace.edu', (41.0395773844, -73.766694506)],

['Pace University Pleasantville', 'https://careers.pace.edu/postings/search', 'http://www.pace.edu', (41.1284649279, -73.80838717)],

['Paul Smiths College', 'http://www.paulsmiths.edu/humanresources/employment', 'http://www.paulsmiths.edu', (44.4373167524, -74.2529946064)],

['Phillips Beth Israel Sch of Nursing', '', 'http://www.pson.edu', (40.7448494113, -73.9912907691)],

['Polytechnic Inst of NY - Westchester Campus', 'https://sunypoly.interviewexchange.com/static/clients/511SPM1/hiring.jsp', 'http://www.poly.edu/', (41.0939312216, -73.8147736623)],

['Polytechnic Institute of NY - Main Campus', 'https://sunypoly.interviewexchange.com/static/clients/511SPM1/hiring.jsp', 'http://www.poly.edu/', (40.6943573162, -73.9864574955)],

['Polytechnic Institute of NYU - Long Island Center', 'https://sunypoly.interviewexchange.com/static/clients/511SPM1/hiring.jsp', 'http://www.poly.edu/', (40.7726011592, -73.4129140464)],

['Pratt Institute', '', 'http://www.pratt.edu', (40.6918957425, -73.9639616366)],

['Pratt Institute Manhattan Center', '', 'http://www.pratt.edu', (40.7380983369, -73.9990084787)],

['Professional Business College', '', 'http://www.pbcny.edu', (40.7189568257, -74.0020664246)],

['Rabbi Isaac Elchanan Theo Seminary', '', 'http://www.yu.edu/riets/', (40.8515810832, -73.9285990394)],

['Relay School of Education', '', 'http://www.relay.edu', (40.7405456779, -73.9932910229)],

['Rensselaer Polytech Institute', 'https://rpijobs.rpi.edu', 'http://www.rpi.edu', (42.7296105935, -73.6802067256)],

['Roberts Wesleyan College', 'https://www.roberts.edu/employment', 'http://www.roberts.edu', (43.1256048122, -77.8013082192)],

['Rochester Institute of Technology', '', 'http://www.rit.edu', (43.0847578962, -77.6753621235)],

['Rockefeller University', '', 'http://www.rockefeller.edu/', (40.7629956519, -73.9564672926)],

["Saint Joseph's Seminary And College", '', 'http://dunwoodie.edu/', (40.9201600754, -73.8630100825)],

['Saint Lawrence University', 'https://employment.stlawu.edu/postings/search', 'http://www.stlawu.edu', (44.5883474893, -75.1598172519)],

['Salvation Army College For Officer Training', '', 'http://www.tsacfotny.edu', (41.1137143951, -74.1407862011)],

['Samaritan Hospital School of Nursing', '', 'http://sphp.com/son', (42.74282684, -73.67644282)],

['Sarah Lawrence College', 'https://www.sarahlawrence.edu/human-resources/job-openings.html', 'http://www.sarahlawrence.edu', (40.9354310286, -73.8436968994)],

['Siena College', '', 'http://www.siena.edu/', (42.717915027, -73.7553350204)],

['Skidmore College', 'https://careers.skidmore.edu/postings/search', 'http://www.skidmore.edu', (43.094951787, -73.7800194799)],

['St Bonaventure University', '', 'http://www.sbu.edu', (42.0795050049, -78.4849799242)],

['St Elizabeth Hospital College of Nursing', '', 'http://www.secon.edu', (43.0834478231, -75.2674174685)],

['St Francis College', 'https://www.sfc.edu/about/careers', 'http://www.sfc.edu', (40.6932834665, -73.9920614542)],

['St John Fisher College', 'https://jobs.sjfc.edu', 'http://www.sjfc.edu', (43.1175935637, -77.5166739799)],

['St Johns University-Staten Island', 'https://www.stjohns.edu/about/administrative-offices/human-resources/recruitment', 'http://www.stjohns.edu', (40.6221249432, -74.089553458)],

["St Joseph's College", 'https://www.sjcny.edu/employment', 'http://www.sjcny.edu', (40.6903589538, -73.9679493284)],

["St Joseph's College - Suffolk Campus", 'https://www.sjcny.edu/employment', 'http://www.sjcny.edu', (40.7746849948, -73.0233178286)],

["St Joseph's College of Nursing at St Joseph's Hospital Health Center", '', 'http://www.sjhcon.edu/', (43.0547501798, -76.1484215884)],

['St Thomas Aquinas College', 'https://www.stac.edu/about-stac/jobs-stac', 'http://www.stac.edu', (41.0420293949, -73.9384034211)],

["St Vladimir's Orthodox Theol Seminry", '', 'http://www.svots.edu/', (40.96988799, -73.82415561)],

["St. Bernard's School of Theology And Ministry", '', 'http://www.stbernards.edu', (43.1021829757, -77.5264984514)],

["St. John's University", 'https://www.stjohns.edu/about/administrative-offices/human-resources/recruitment', 'http://www.stjohns.edu', (40.7256720182, -73.7918247118)],

["St. John's University - Manhattan Branch", 'https://www.stjohns.edu/about/administrative-offices/human-resources/recruitment', 'http://www.stjohns.edu', (40.7300709717, -73.992834118)],

["St. Joseph's Seminary & College-Douglaston", '', 'http://cathedralseminary.org/', (40.74636212, -73.73310234)],

["St. Joseph's Seminary & College-Huntington", '', 'http://www.icseminary.edu', (40.90515869, -73.47090101)],

["St. Joseph's Seminary & College-Somers", '', '', (0.0, 0.0)],

['Syracuse University', '', 'http://syracuse.edu', (43.0402401915, -76.1369455708)],

['The Sage Colleges', 'https://www.sage.edu/about/human-resources/employment-opportunities', 'http://www.sage.edu', (42.7282013924, -73.6937086081)],

['The Sage Colleges -  Albany Campus', 'https://www.sage.edu/about/human-resources/employment-opportunities', 'http://www.sage.edu', (42.6527156078, -73.7831997513)],

['Teachers College', '', 'http://www.tc.columbia.edu/', (40.8100945923, -73.9606417774)],

['Touro College', '', 'http://www.touro.edu', (40.75313425, -73.98929738)],

['Touro College', '', 'http://tourocom.touro.edu/about-us/contact', (40.75313425, -73.98929738)],

['Touro College - Bayshore', '', 'http://www.touro.edu', (40.7244854646, -73.2513380684)],

['Touro College - Flatbush', '', 'http://www.touro.edu', (40.6251624576, -73.9599657735)],

['Touro College - Harlem', '', 'http://www.touro.edu', (40.8015644265, -73.9351031801)],

['Touro College - Kew Gardens', '', 'http://www.touro.edu', (40.7248816812, -73.8158841816)],

['Touro College - Valhalla', '', 'http://dental.touro.edu/', (41.0853086341, -73.8175326375)],

['Touro College-Central Islip', '', 'http://www.touro.edu', (40.76197743, -73.1876853439)],

['Trocaire College', 'https://trocaire.applicantpro.com/jobs', 'http://www.trocaire.edu', (42.8467543251, -78.8119072161)],

['Unification Theological Seminary', 'https://utsnyc.edu/about/careers-at-union', 'http://uts.edu/', (0.0, 0.0)],

['Union College', '', 'http://www.union.edu', (42.8175712882, -73.9285185308)],

['Union Graduate College', '', 'http://www.uniongraduatecollege.edu', (42.8135812884, -73.9344484824)],

['Union Theological Seminary', 'https://utsnyc.edu/about/careers-at-union', 'http://www.utsnyc.edu', (40.8112300852, -73.961898663)],

['University of Rochester', '', 'http://www.rochester.edu', (43.1263561927, -77.6311742772)],

['Utica College', 'http://utica.edu/hr/employment.cfm', 'http://www.utica.edu', (43.0970213153, -75.2706579866)],

['Vassar College', 'http://humanresources.vassar.edu/jobs', 'http://www.vassar.edu', (41.6865376709, -73.897705087)],

['Vaughn College of Aeronautics And Technology', 'https://www.vaughn.edu/jobs', 'http://www.vaughn.edu', (40.7786150523, -73.839777103)],

['Villa Maria College of Buffalo', 'https://www.villa.edu/about-us/employment-opportunities', 'http://www.villa.edu/', (42.9127511236, -78.7971828612)],

['Wagner College', 'https://wagner.edu/hr/hr_openings', 'http://www.wagner.edu/', (40.6149084222, -74.0942924431)],

['Webb Insttitute', 'http://www.webb.edu/employment', 'http://www.webb.edu', (40.8826862651, -73.6462725744)],

['Wells College', 'https://www.wells.edu/jobs', 'http://www.wells.edu', (42.7436626701, -76.6992195176)],

['Yeshiva University', '', 'http://www.yu.edu', (40.8506479647, -73.9298665465)]

]







    # Advanced options
    max_crawl_depth = 2
    num_procs = 8


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


    # Display results sorted by jbw conf
    with lock:
        for i in sort_dict:
            w_l = []

            # Display original full entry
            for orig_entry in all_list:
                if i == orig_entry[2]:
                    print("\n\n" + str(orig_entry) + ',')
                    break

            temp = sorted(sort_dict[i], key = lambda x: int(x[1]), reverse=True)
            for ii in temp: # List each em URL
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
















