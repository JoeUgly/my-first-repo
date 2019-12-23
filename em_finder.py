
# Description: Crawl webpages and rank links based on likelihood of containing job postings.



# To do:
# AP and wnyric are not totally centralized? eg: https://www.applitrack.com/saugertiesk12/onlineapp/jobpostings/view.asp
# output all 4 items
# use redirects instead of original URLs









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

    # Clear list to free up memory
    all_list2 = None




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


    # Display results sorted by jbw conf?
    with lock:
        for i in sort_dict:
            print("\n\n['" + i + "', ''],") # display results in "list format"
            temp = sorted(sort_dict[i], key = lambda x: int(x[1]), reverse=True)
            for ii in temp:
                print(ii[0]) # exclude jbw conf?





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
















