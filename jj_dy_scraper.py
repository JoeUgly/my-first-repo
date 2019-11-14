
# Description: Search NYS civil service and school webpages for keywords using a CLI.
# Version: 2.0


# To do:
# timeout +
# non dynamic html request as fallback -
# function for checked_pages outcome +
# put all errors in add_errorurls_f?
# distinguish final errors and loop retry errors +
# dont retry non html responses. eg text files +
# outcome list may not recognize redirects. "None" value remains
# jbw_type and portalurl should be written only once per errorlog entry +
# dups in checked pages +
# reduce redundant dup checker calls
# cml must keep orig url and add red_url +
# results hyperlinks should display org name
# only add needed urls during orignal queue creation. ie resume progress after previous failed scraping
# investigate multi proc
# dropdown menus persist. decompose all classes containing dropdown +
# twitter posts show up in results
# urls not found in cml
# save all redirects to cml using resp.history
# broken pipe and connection reset by peer errors persists
# rewrite errorlog




# Later versions:
# comprehensive db = org name, home url, employ url or centralized service, address, geopy location, coords
# false positives: search visible text only https://www.friendship.wnyric.org/domain/9 +
# true negatives: dynamic pages https://www.applitrack.com/penfield/onlineapp/default.aspx?all=1 +
# test other BS parsers -
# compare Selenium to Splash
# jbws back to count but limit to x occurrences?
# combine high conf scan and jbw search into one for loop
# weighted jbws
# pass interviewexchange captcha
# document which orgs use a centralized service and exlude or include them from jj search
# phase out blacklist



# Concerns:
# Dup checker: removing fragments and trailing slash
# case sensitivity

# High conf: exclude good low conf links
# https://www.cityofnewburgh-ny.gov/civil-service = upcoming exams
# http://www.albanycounty.com/Government/Departments/DepartmentofCivilService.aspx = exam announcement
# have seperate high conf jbw lists?

# Bunkwords: search entire element or just contents?
# must search url to exclude .pdf, etc

# Decompose: drop down menus?
# dont decompose menus for anchor tag search








import datetime, docker, requests, psutil, json, gzip, os, queue, re, socket, time, traceback, urllib.parse, urllib.request, webbrowser, ssl
from os.path import expanduser
from multiprocessing import active_children, Lock, Manager, Process, Queue, Value
from math import sin, cos, sqrt, atan2, radians
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup




# Start timer
startTime = datetime.datetime.now()

# Global variables
user_agent_str = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'


# Make jorbs directory in user's home directory
jorb_home = os.path.join('/home/joepers/', 'joes_jorbs')
if not os.path.exists(jorb_home):
    os.makedirs(jorb_home)

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
jobwords_su_high = ('continuous recruitment', 'employment', 'job listing', 'job opening', 'job posting', 'job announcement', 'job opportunities', 'jobs available', 'available positions', 'open positions', 'available employment', 'career opportunities', 'employment opportunities', 'current vacancies', 'current job', 'current employment', 'current opening', 'current posting', 'current opportunities', 'careers at', 'jobs at', 'jobs @', 'work at', 'employment at', 'find your career', 'browse jobs', 'search jobs', 'continuous recruitment', 'vacancy postings', 'prospective employees')

# Low confidence sch and uni jbws
jobwords_su_low = ('join', 'job seeker', 'job', 'job title', 'positions', 'careers', 'human resource', 'personnel', 'vacancies', 'posting', 'opening', 'recruitment', '>faculty<', '>staff<', '>adjunct<', '>academic<', '>support<', '>instructional<', '>administrative<', '>professional<', '>classified<', '>coaching<', 'vacancy')

# Worst offenders
#offenders = ['faculty', 'staff', 'professional', 'management', 'administrat', 'academic', 'support', 'instructional', 'adjunct', 'classified', 'teach', 'coaching']

## switching to careers solves all these
# career services, career peers, career prep, career fair, volunteer
## application
# Exclude links that contain any of these
bunkwords = ('academics', 'pnwboces.org', 'recruitfront.com', 'schoolapp.wnyric.org', 'professional development', 'career development', 'javascript:', '.pdf', '.jpg', '.ico', '.rtf', '.doc', 'mailto:', 'tel:', 'icon', 'description', 'specs', 'specification', 'guide', 'faq', 'images', 'exam scores', 'resume-sample', 'resume sample', 'directory', 'pupil personnel')

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
    else: print('No scheme at:', dup_checker)

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

    # Remove trailing whitespace and slash and then lowercase it
    dup_checker = dup_checker.strip().strip('/').lower()

    ## Remove double forward slashes?
    dup_checker = dup_checker.replace('//', '/')
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
            print(os.getpid(), 'Updating outcome for:', url)
            remover = each_url
            break
            #print(os.getpid(), 11111)
            #for x in checkedurls_man_list: print(os.getpid(), x)

            # Manager will not be aware of updates to items. Must append new item.

    # Catch no match
    else:
        print(os.getpid(), url, 'not found in checkedurls_man_list. __Error__')
        return


    with lock:
        try:
            checkedurls_man_list.remove(remover)
        except Exception as errex:
            print(errex)
    #print(os.getpid(), 22222, i)
    #for x in checkedurls_man_list: print(os.getpid(), x)
    new_i = [url, conf_val]
    with lock:
        try:
            checkedurls_man_list.append(new_i)
        except Exception as errex:
            print(errex)
    #print(os.getpid(), 33333)
    #for x in checkedurls_man_list: print(os.getpid(), x)


# Define HTML request function
def html_requester(workingurl, current_crawl_level, jbw_type, errorurls_man_dict, portalurl, dock_pause):

    try:

        # Local waiting state
        im_waiting = False

        # Check if Splash needs to restart
        while dock_pause.value > 0:

            # Set current state to waiting
            if not im_waiting:
                im_waiting = True

                # Report to the manager that this process is waiting
                waiting_procs.value += 1

            time.sleep(2)

        time.sleep(2)
        # Make request on port 8050 so Splash handles it
        ## "connection reset by peer" and "broken pipe" errors fixed by lowering json wait
        resp = requests.post('http://localhost:8050/render.json', json={
            'url': workingurl,
            'headers': {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'}, # Spoof user agent
            'plugins_enabled': 'true', # May help with rendering
            'indexeddb_enabled': 'true', # May help with rendering
            'wait': 0.1, # Wait for dyanamic content to render.
            'render_all': 1, # Render the entire page
            'html': 1, # Static HTML
            'iframes': 1, # Dynamic content. JSON element is called 'childFrames'
            'images': 0, # Disable images for speed
            'geometry': 0, # Exclude unnecessary items
            'timeout': 20 # 
            #'js_source': 'window.close();' ## Release memory
        })

        # Get status code
        stat_code = resp.status_code

        # Catch errors
        if stat_code != 200:
            print('stat_code=', stat_code, workingurl)

            # Get relevant error info
            ## stat_info for timeout errors will be a dict, not a string. Also it will not have ['info']['text']
            try:
                stat_info = json.loads(resp.text)['info']['text']
            except:
                stat_info = str(json.loads(resp.text)['info'])
            print('status=', stat_info, workingurl)

            ## unnecessary?
            # Must use ['info']['url'] when non 200 status to get redirected url
            try:
                red_url = json.loads(resp.text)['info']['url']
                print('red=', red_url) 
            except:
                red_url = workingurl

            ## dup check

            # Don't retry on 404 or 403 error
            if stat_info.endswith('not found'):
                print(os.getpid(), 'jj_error 4: HTTP 404/403 request:', workingurl)
                add_errorurls_f(workingurl, 'jj_error 4', 'Host not found', current_crawl_level, jbw_type, portalurl, errorurls_man_dict)

                # Declare not to retry
                return False

            # Retry on timeout errors
            elif stat_info.startswith("{'remaining': -"):
                print(os.getpid(), 'jj_error 3: HTTP timeout:', workingurl)
                add_errorurls_f(workingurl, 'jj_error 3', 'HTTP timeout', current_crawl_level, jbw_type, portalurl, errorurls_man_dict)

                # Declare to retry
                return True

            # Don't retry on non HTML errors
            elif stat_info == 'Frame load interrupted by policy change':
                print(os.getpid(), 'jj_error 2: non-HTML detected:', red_url)
                add_errorurls_f(workingurl, 'jj_error 2', 'Forbidden content type', current_crawl_level, jbw_type, portalurl, errorurls_man_dict)

                ## add red_url

                # Declare not to retry
                return False


            # Retry on other error
            else:
                print(os.getpid(), 'jj_error 5b: Other request', workingurl)
                stat_info = str(stat_code) + ' ' + stat_info
                add_errorurls_f(workingurl, 'jj_error 5', stat_info, current_crawl_level, jbw_type, portalurl, errorurls_man_dict)
                return True



        ## if no html then retry?
        # Get HTML and dynamic content
        html_text = json.loads(resp.text)['html']
        dy_text = json.loads(resp.text)['childFrames']

        # Red url
        print(333333)
        red_url = json.loads(resp.text)['url']
        print(444444)
        #print(os.getpid(), '\n\n workingurl=', workingurl, '\n html_text=', html_text, '\n\n dy_text=', dy_text)

        ## dy content is list. exclude unnecessary list items
        # Combine HTML and dynamic content
        rendered_html = html_text + str(dy_text)
        return rendered_html, red_url


    # Catch and log HTTP request errors
    except Exception as errex:

        # Retry on other error
        print(os.getpid(), 'jj_error 5a: Other request', workingurl, errex)
        add_errorurls_f(workingurl, 'jj_error 5', str(errex), current_crawl_level, jbw_type, portalurl, errorurls_man_dict)
        return True




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
def scraper(all_urls_q, max_crawl_depth, checkedurls_man_list, errorurls_man_dict, skipped_pages, prog_count, total_count, jbw_tally_man_l, dock_pause):
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
                #proceed_pass = proceed_f(workingurl, working_list, checkedurls_man_list, verbose_arg, skipped_pages, current_crawl_level, all_urls_q, total_count, add_to_queue_b, blacklist)

                #if not proceed_pass: continue

                # Form domain by splitting after 3rd slash
                domain = '/'.join(workingurl.split('/')[:3])



                # Retry loop on request and decode errors
                loop_success = False
                for loop_count in range(3):

                    # Get html from function
                    html_url = html_requester(workingurl, current_crawl_level, jbw_type, errorurls_man_dict, portalurl, dock_pause)

                    # html_requester returns True to indicate a needed retry
                    if html_url == True:
                        print(os.getpid(), 'Retry request loop:', workingurl)
                        continue

                    # html_requester returns False to indicate don't retry
                    elif html_url == False:
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

                    ## not final if using domain as fallback
                    # Append a final error designation
                    prev_item = errorurls_man_dict[workingurl]
                    prev_item.append('jj_final_error')

                    with lock:
                        try:
                            errorurls_man_dict[workingurl] = prev_item
                        except Exception as errex:
                            print(errex)


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


                # Get HTML and redirected URL
                html = html_url[0]
                red_url = html_url[1]
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


                # Select body
                soup = BeautifulSoup(html, 'html5lib')
                soup = soup.find('body')

                # Clear old html to free up memory
                html = None

                if soup is None:
                    print(os.getpid(), 'Empty soup0:', workingurl)
                    continue

                # Remove script, style, and empty elements
                for i in soup(["script", "style"]):
                    i.decompose()

                ## unn
                # Iterate through and remove all of the hidden style attributes
                r = soup.find_all('', {"style" : style_reg})
                for x in r:
                    #print(os.getpid(), 'Decomposed:', workingurl, x)
                    x.decompose()

                # Type="hidden" attribute
                r = soup.find_all('', {"type" : 'hidden'})
                for x in r:
                    #if verbose_arg print(os.getpid(), 'Decomposed:', workingurl, x)
                    x.decompose()

                # Hidden section(s) and dropdown classes
                for x in soup(class_=class_reg):
                    #print(os.getpid(), 'Decomposed:', workingurl, x)
                    x.decompose()

                '''
                ## This preserves whitespace across lines. Prevents: 'fire departmentapparatuscode compliance'
                # Remove unnecessary whitespace. eg: multiple newlines, spaces, and all tabs
                vis_soup = ''
                temp_soup = str(soup.text)
                for i in temp_soup.split('\n'):
                    i = i.replace('\t', ' ').replace('  ', '')
                    if i: 
                        vis_soup = vis_soup + i
                '''

                # Remove unnecessary whitespace
                vis_soup = ''
                temp_soup = str(soup.text)
                for i in temp_soup.split('\n'):
                    i = i.strip()
                    if i:
                        vis_soup = vis_soup + i


                # Use lowercase visible text for comparisons
                vis_soup = vis_soup.lower()

                if vis_soup is None:
                    print(os.getpid(), 'Empty soup1:', workingurl)
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

                # Update outcome in checkedurls_man_list
                outcome(checkedurls_man_list, workingurl, jbw_count)

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

                # Don't search the fallback domain
                if current_crawl_level > -1:

                    # Make date dir to put results into
                    dater = datetime.datetime.now().strftime("%x").replace('/', '_')

                    ## make results dir

                    # Make jbw type dirs inside date dir
                    dated_results_path = os.path.join(jorb_home, 'results', dater, jbw_type)
                    if not os.path.exists(dated_results_path):
                        print(1111)
                        os.makedirs(dated_results_path)

                    # Replace forward slashes so they aren't read as directory boundaries
                    portal_url_path = portalurl.replace('/', '\\')

                    # Make directory using portal name
                    portal_path = os.path.join(dated_results_path, portal_url_path)
                    if not os.path.exists(portal_path):
                        os.makedirs(portal_path)

                    # Write HTML to text file using url name (max length is 255)
                    url_path = workingurl.replace('/', '\\')
                    html_path = os.path.join(portal_path, url_path)
                    with open(html_path[:254], "w", encoding='utf8') as write_html:
                        write_html.write(vis_soup)
                    print(os.getpid(), 'write success:', workingurl)


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
                conf_val = 'jj_error 1'
                outcome(checkedurls_man_list, workingurl, conf_val)
                continue


            # Declare the task has finished
            finally:
                prog_count.value += 1





# Multiprocessing
if __name__ == '__main__':


    civ_list2 = (
'http://cityofpoughkeepsie.com/personnel/',
'http://www.tiogacountyny.com/departments/personnel-civil-service'
)

    # Civil Service URLs, initial crawl levels, and coordinates database
    civ_list = (
'http://cityofpoughkeepsie.com/personnel/',
'http://www.greenegovernment.com/departments/human-resources-and-civil-service',
'http://humanresources.westchestergov.com/job-seekers/civil-service-exams',
'https://kingston-ny.gov/employment',
'http://niagarafallsusa.org/government/city-departments/human-resources-department/',
'https://www.cityofwhiteplains.com/98/Personnel',
'http://ocgov.net/personnel',
'http://oneidacity.com/473-2/',
'http://oswegocounty.com/humanresources/openings.php',
'http://oysterbaytown.com/departments/human-resources/',
'http://rocklandgov.com/departments/personnel/civil-service-examinations',
'http://sullivanny.us/index.php/Departments/Personnel',
'http://tompkinscountyny.gov/personnel',
'https://www.villageofhempstead.org/197/Employment-Opportunities',
'http://watervliet.com/city/civil-service.htm',
'https://web.co.wayne.ny.us/',
'http://www.albanycounty.com/Government/Departments/DepartmentofCivilService.aspx',
'http://www.alleganyco.com/departments/human-resources-civil-service/',
'http://www.amherst.ny.us',
'http://www.auburnny.gov/public_documents/auburnny_civilservice/index',
'https://www.batavianewyork.com/fire-department/pages/employment',
'http://www.binghamton-ny.gov/departments/personnel/employment/employment',
'https://www.brookhavenny.gov/',
'https://www.cattco.org/human-resources/jobs',
'https://www.chemungcountyny.gov/departments/a_-_f_departments/civil_service_personnel/index.php',
'https://www.buffalony.gov/1001/Employment-Resources',
'http://www.ci.webster.ny.us/85/Human-Resources',
'http://www.cityofelmira.net/personnel',
'http://www.cityofglencoveny.org/index.htm',
'http://www.cityofglensfalls.com/55/Human-Resources-Department',
'https://ithaca-portal.mycivilservice.com/',
'https://www.cityofnewburgh-ny.gov/civil-service',
'https://www.cityofpeekskill.com/human-resources/pages/about-human-resources',
'https://www.cityofrochester.gov/article.aspx?id=8589936759',
'http://www.cityofschenectady.com/208/Human-Resources',
'http://www.cityofutica.com/departments/civil-service/index',
'https://www.cliftonpark.org/services/employment-applications.html',
'https://www.clintoncountygov.com/employment',
'http://www.co.chautauqua.ny.us/314/Human-Resources',
'http://www.co.chenango.ny.us/personnel/examinations/',
'http://www.co.delaware.ny.us/departments/pers/jobs.htm',
'http://www.co.dutchess.ny.us/civilserviceinformationsystem/applicantweb/frmannouncementlist.aspx?aspxerrorpath=/civilserviceinformationsystem/applicantweb/frmuserlogin',
'https://www.dutchessny.gov/Departments/Human-Resources/Human-Resources.htm',
'http://www.co.essex.ny.us/jobs.asp',
'http://www.co.genesee.ny.us/departments/humanresources/index.php',
'https://co.jefferson.ny.us/',
'https://www.livingstoncounty.us/207/Personnel-Department',
'http://www.co.ontario.ny.us/jobs.aspx',
'https://www.stlawco.org/departments/humanresources/examinationschedule',
'https://ulstercountyny.gov/personnel/index.html',
'https://www.ci.cohoes.ny.us/',
'http://www.cortland-co.org/263/Personnel-Civil-Service',
'https://www.cs.ny.gov/',
'https://www2.cuny.edu/employment/civil-service/',
'http://www.eastchester.org/departments/comptoller.php',
'http://eastfishkillny.gov/government/employment.htm',
'http://www2.erie.gov/employment/',
'https://www.fultoncountyny.gov/node/5',
'http://www.gobroomecounty.com/personnel/cs',
'http://www.greenburghny.com',
'https://www.hamiltoncounty.com/government/departments-services',
'http://www.huntingtonny.gov/content/13753/13757/17478/17508/default.aspx?_sm_au_=ivvt78qz5w7p2qhf',
'http://www.irondequoit.org/town-departments/human-resources/town-employment-opportunities?_sm_au_=ivv8z8lp1wffsnv6',
'http://lackawannany.gov/government/civil-service/',
'https://www.lockportny.gov/current-exams-and-openings/',
'https://www.longbeachny.gov/index.asp?type=b_basic&amp;sec={9c88689c-135f-4293-a9ce-7a50346bea23}',
'http://www.mechanicville.com/index.aspx?nid=563',
'https://www.middletown-ny.com/en/departments/civil-service.html?_sm_au_=ivvrlpv4fvqpnjqj',
'http://www.nassaucivilservice.com/nccsweb/homepage.nsf/homepage?readform',
'https://www.newrochelleny.com/362/Civil-Service',
'http://www.niagaracounty.com/Departments/Civil-Service',
'https://www.northhempsteadny.gov/employment-opportunities',
'https://www.norwichnewyork.net/government/human-resources.php',
'http://www.ogdensburg.org/index.aspx?nid=97',
'http://www.oneonta.ny.us/departments/personnel',
'http://www.ongov.net/employment/civilService.html',
'http://www.ongov.net/employment/jurisdiction.html',
'http://www.ongov.net/employment/jurisdiction.html?_sm_au_=ivvrlpv4fvqpnjqj',
'http://www.orleansny.com/personnel',
'http://www.oswegony.org/government/personnel',
'http://www.otsegocounty.com/depts/per/',
'http://www.penfield.org',
'http://www.perinton.org/departments/finpers',
'https://www.putnamcountyny.com/personneldept/',
'https://www.putnamcountyny.com/personneldept/exam-postings/',
'http://www.ramapo.org/page/personnel-30.html?_sm_au_=ivvt78qz5w7p2qhf',
'http://www.rensco.com/county-job-assistance/',
'http://www.rvcny.us/jobs.html?_sm_au_=ivv8z8lp1wffsnv6',
'https://www.ryeny.gov/',
'http://www.saratoga-springs.org/jobs.aspx',
'https://www.saratogacountyny.gov/departments/personnel/',
'https://www.schenectadycounty.com/',
'https://www4.schohariecounty-ny.gov/',
'http://www.schuylercounty.us/119/Civil-Service',
'http://www.smithtownny.gov/jobs.aspx?_sm_au_=ivvt78qz5w7p2qhf',
'http://www.southamptontownny.gov/jobs.aspx',
'https://www.steubencony.org/pages.asp?pgid=32',
'https://www.suffolkcountyny.gov/Departments/Civil-Service',
'http://www.tiogacountyny.com/departments/personnel-civil-service',
'https://www.tonawandacity.com/residents/civil_service.php',
'http://www.townofbethlehem.org/137/Human-Resources?_sm_au_=ivv8z8lp1wffsnv6',
'https://www.townofbrighton.org/219/Human-Resources',
'http://www.townofchili.org/notice-category/job-postings/',
'http://www.townofcortlandt.com',
'https://www.townofguilderland.org/human-resource-department?_sm_au_=ivv8z8lp1wffsnv6',
'https://www.townofossining.com/cms/resources/human-resources',
'http://www.townofpittsford.org/home-hr?_sm_au_=ivv8z8lp1wffsnv6',
'https://www.townofriverheadny.gov/pview.aspx?id=2481&amp;catid=118&amp;_sm_au_=ivvt78qz5w7p2qhf',
'https://www.townofunion.com/',
'https://www.townofwallkill.com/index.php/departments/human-resources',
'http://www.troyny.gov/departments/personnel-department/',
'https://www.usajobs.gov/',
'https://www.vestalny.com/departments/human_resources/job_opportunities.php',
'https://www.villageofossining.org/personnel-department',
'https://www.vsvny.org/index.asp?type=b_job&amp;sec=%7b05c716c7-40ee-49ee-b5ee-14efa9074ab9%7d&amp;_sm_au_=ivv8z8lp1wffsnv6',
'http://www.warrencountyny.gov/civilservice/exams.php',
'http://www.washingtoncountyny.gov/jobs.aspx',
'http://www.wyomingco.net/164/Civil-Service',
'https://www.yatescounty.org/203/Personnel',
'https://www.yonkersny.gov/work/jobs-civil-service-exams',
'https://www.yorktownny.org/jobs',
'https://www1.nyc.gov/jobs',
'https://www1.nyc.gov/jobs/index.page',
'https://www2.monroecounty.gov/careers',
'https://countyfranklin.digitaltowpath.org:10078/content/Departments/View/6:field=services;/content/DepartmentServices/View/48',
'https://countyherkimer.digitaltowpath.org:10069/content/Departments/View/9',
'https://mycivilservice.rocklandgov.com',
'https://mycivilservice.schenectadycounty.com',
'https://romenewyork.com/civil-service/',
'https://seneca-portal.mycivilservice.com',
'https://sites.google.com/a/columbiacountyny.com/civilservice/',
'https://www.albanyny.gov/government/departments/humanresources/employment',
'https://www.colonie.org/departments/civilservice/',
'https://www.lewiscounty.org/departments/human-resources/human-resources',
'https://www.madisoncounty.ny.gov/287/Personnel',
'https://www.monroeny.org/doc-center/town-of-monroe-job-opportunities.html',
'https://www.orangecountygov.com/1137/Human-Resources',
'https://www.orangetown.com/groups/department/personnel/',
'http://www.cayugacounty.us/QuickLinks.aspx?CID=103',
'https://hempsteadny.gov/employment-services',
'https://www.co.montgomery.ny.us/web/sites/departments/personnel/employment.asp',
'http://cmvny.com/departments/civil-service/job-postings',
'http://www.townofpoughkeepsie.com/human_resources/index.html?_sm_au_=ivv8z8lp1wffsnv6',
'https://www.watertown-ny.gov/index.asp?nid=791',
'https://www.townofislip-ny.gov/?Itemid=220'
)

    school_list2 = (
'http://academyofthecity.org/about_us/employment',
'http://albanycommunitycs.org/careers'
)

    # School URLs, initial crawl levels, and coordinates database
    school_list = (
'http://academyofthecity.org/about_us/employment',
'http://albanycommunitycs.org/careers',
'http://aldenschools.org/Page/25',
'http://bemusptcsd.org/district/employment_information',
'http://berlincentral.org/district/employment',
'http://bit.ly/2xbEAIJ',
'http://bphs.democracyprep.org',
'http://brillacollegeprep.org/careers',
'http://brooklyncompass.org/careers',
'http://brooklyneastcollegiate.uncommonschools.org/brooklyn-east/careers',
'http://brownsvillecollegiate.uncommonschools.org/bvc/careers',
'http://buffaloschools.applicantstack.com/x/openings',
'https://www.applitrack.com/buffaloschools/onlineapp/default.aspx?all=1',
'http://campacharter.org',
'http://classicalcharterschools.org/careers',
'http://community.waverlyschools.com/employment',
'http://comsewogue.k12.ny.us',
'http://comsewogue.k12.ny.us/departments/human_resources',
'http://coneyislandprep.org/careers/career-opportunities',
'http://csicharter.org/career',
'http://cvweb.wnyric.org/Page/998',
'http://democracyprep.org/careers',
'http://district.uniondaleschools.org/job_postings',
'http://dpems.democracyprep.org',
'http://ecs.schoolwires.com/contact_us/employment',
'http://ecsli.org/careers',
'http://egcsd.org/departments/personnel-and-professional-development/employment',
'http://elmcharterschool.org/work-at-elm',
'http://eufsd.org/domain/119',
'http://excellenceboys.uncommonschools.org',
'http://excellencegirls.uncommonschools.org/egcs/careers',
'http://explorenetwork.org/careers/careers',
'http://gc.schoolwires.net/Page/3855',
'http://gilboa-conesville.k12.ny.us/our_school/Job_Vacancies',
'http://greenville.k12.ny.us/district/Human%20Resources/Availablepositions.asp',
'http://gufsd.org/district/employment-opportunities',
'http://hammondcsd.schoolwires.net/Page/104',
'http://healthsciencescharterschool.org/apps/pages/index.jsp?uREC_ID=366249&type=d&pREC_ID=816495',
'http://hpes.democracyprep.org',
'http://imaginemeleadership.org/about-us/careers',
'http://inletcommonschool.wordpress.com',
'http://integrationcharterschools.org/jobs',
'http://integrationcharterschools.org/richmond-preparatory-charter-school',
'http://jerichoschools.org',
'http://jobs.successacademies.org/search',
'http://kingscollegiate.uncommonschools.org/kccs/careers',
'http://leadershipprepbedstuy.uncommonschools.org/lpbs/our-school/elementary-academy',
'http://leadershipprepbrownsville.uncommonschools.org/lpbv/our-school/elementary-academy',
'http://leadershipprepcanarsie.uncommonschools.org/lpcs/our-school/elementary-academy',
'http://legacycollegeprep.org',
'http://lisboncs.schoolwires.com/Page/1346',
'http://lmcs.k12.ny.us/domain/15',
'http://mesacharter.org',
'http://middlevillageprep.org/apps/jobs',
'http://motthallcharterschool.org',
'http://nanuet-union-free-school-district.echalksites.com/employment_opportunities',
'http://northport.k12.ny.us/district/human_resources',
'http://northshore.k12.ny.us/district/employment.htm',
'http://nycmcs.org/about-us/employment',
'http://obenschools.org/domain/33',
'http://oceanhillcollegiate.uncommonschools.org/ohc/careers',
'http://onteora.schoolwires.com/departments/human-resources',
'http://pvcsd.org/index.php/district/district-info/human-resources',
'http://ripleyelementary.weebly.com/employment-opportunities.html',
'http://rochesterprep.uncommonschools.org/rpcs/careers',
'http://romuluscsd.org/employment_opportunities',
'http://roslyn.schoolwires.net/domain/37',
'http://rsufsd.weebly.com/employment-opportunities.html',
'http://scotiaglenvilleschools.org',
'http://shermancsd.org/employment',
'https://classicalcharterschools.org/careers',
'http://southoldufsd.com',
'http://storefrontacademy.org/employment-opportunities',
'http://sweethomeschools.org/District/2200-Employment-Opportunities.html',
'http://troyprep.uncommonschools.org/careers-2',
'http://tullyschools.org/teacherpage.cfm?teacher=694',
'http://upchs.org/contact_school/prospective_employees/current_opportunities',
'http://uticaschools.schoolwires.net/Page/115',
'http://valleystream13.com/departments/human-resources',
'http://westbuffalocharter.org/job-opportunities',
'http://williamsburgcollegiate.uncommonschools.org/wccs/careers',
'http://wps.greenwichcsd.org/employment',
'http://www.1000islandsschools.org',
'http://www.3villagecsd.k12.ny.us',
'http://www.aacsapps.com/domain/55',
'http://www.academycharterschool.org/careers',
'http://www.achievementfirst.org/schools/new-york-schools/achievement-first-apollo-elementary-school/about',
'http://www.achievementfirst.org/schools/new-york-schools/achievement-first-aspire-elementary-school/about',
'http://www.achievementfirst.org/schools/new-york-schools/achievement-first-brownsville-elementary-school/about',
'http://www.achievementfirst.org/schools/new-york-schools/achievement-first-bushwick-elementary-school/about',
'http://www.achievementfirst.org/schools/new-york-schools/achievement-first-crown-heights-elementary-school/about',
'http://www.achievementfirst.org/schools/new-york-schools/achievement-first-endeavor-elementary-school/about',
'http://www.achievementfirst.org/schools/new-york-schools/achievement-first-linden-elementary-school/about',
'http://www.achievementfirst.org/schools/new-york-schools/achievement-first-north-brooklyn-prep-elementary-school/about',
'http://www.addisoncsd.org/domain/30',
'http://www.adjcharter.org./employment.html',
'http://www.akronschools.org/Page/5499',
'http://www.albanyleadershiphigh.org/community/careers',
'http://www.albionk12.org/district/district-office/employment/index',
'http://www.alcsbronx.org/apps/jobs',
'http://www.alcsny.org/Page/1695',
'http://www.alexandriacentral.org/Page/398',
'http://www.amanicharter.org/open-positions',
'http://www.amherstschools.org/Page/242',
'http://www.amityvilleschools.org/departments/human_resources',
'http://www.andescentralschool.org/district/employment',
'http://www.andovercsd.org/Page/131',
'http://www.ardsleyschools.org/Page/277',
'http://www.argylecsd.org/district/job_opportunities',
'http://www.ascendlearning.org',
'http://www.ascendlearning.org/careers',
'http://www.atticacsd.org/Page/23',
'http://www.avcs.org/district-offices/employment-opportunities',
'http://www.averillpark.k12.ny.us/district-information/job-vacancies',
'http://www.avocacsd.org',
'http://www.avoncsd.org/jobs.cfm',
'http://www.babylon.k12.ny.us/our_district/employment',
'http://www.bataviacsd.org/Page/574',
'http://www.bathcsd.org/jobs.cfm',
'http://www.bbpschools.org/district_information/human_resources_department',
'http://www.bbschools.org/Employment.aspx',
'http://www.bcsdk12.org',
'http://www.bcsdny.org/Page/134',
'http://www.beaconcityk12.org/Page/117',
'http://www.bedstuycollegiate.org/bsc/careers',
'http://www.belfast.wnyric.org/Page/36',
'http://www.bellmore-merrick.k12.ny.us/district/opportunities',
'http://www.bethpagecommunity.com/district/employment',
'http://www.bfcsd.org/apps/spotlightmessages/1776',
'http://www.bgligschool.org/apps/jobs',
'http://www.bhpanthers.org/Page/1054',
'http://www.binghamtonschools.org',
'http://www.blindbrook.org',
'http://www.bloomfieldcsd.org/apps/jobs',
'http://www.bmcsd.org/home/employment-opportunities',
'http://www.boltoncsd.org',
'http://www.bpcsd.org/community/employment',
'http://www.brcs.wnyric.org/Page/194',
'http://www.brcsd.org',
'http://www.briarcliffschools.org/district-information/human-resources',
'http://www.bridgehampton.k12.ny.us/district/employment_opportunities',
'http://www.brighterchoice.org/boys/resources/employment-information',
'http://www.brighterchoice.org/girls/resources/career-opportunities',
'http://www.brittonkill.k12.ny.us',
'http://www.brockport.k12.ny.us',
'http://www.broctoncsd.org/Page/1907',
'http://www.bronxbetterlearning.org',
'http://www.bronxcommunity.org',
'http://www.brookfieldcsd.org/Page/429',
'http://www.bscsd.org/Page/559',
'http://www.bufsd.org/HTMLpages/Employment/Employment.html',
'http://www.bville.org/teacherpage.cfm?teacher=99',
'http://www.bwccs2.org',
'http://www.cairodurham.org/jobs',
'http://www.cambridgecsd.org/domain/23',
'http://www.camdenschools.org/districtpage.cfm?pageid=1395',
'http://www.canastotacsd.org',
'http://www.candorcsd.org/index.php/departments/employment',
'http://www.carmelschools.org/groups/6223/personnelpayrollbenefits/employment_opportunities',
'http://www.carthagecsd.org',
'http://www.catomeridian.org/districtpage.cfm?pageid=1350',
'http://www.cc.cnyric.org/districtpage.cfm?pageid=65',
'http://www.ccs.edu/Page/228',
'http://www.ccsd.edu/domain/999',
'http://www.ccsdk12.org',
'http://www.ccsdli.org/staff_resources/employment',
'http://www.ccsdny.org/domain/8',
'http://www.ccsknights.org',
'http://www.centermoriches.k12.ny.us/district/employment',
'http://www.centralislip.k12.ny.us',
'http://www.centralqueensacademy.org/careers',
'http://www.centralsquareschools.org/departments.cfm?subpage=20471',
'http://www.cg.wnyric.org/Page/51',
'http://www.challengeprepcharter.org/careers',
'http://www.charlottevalleycs.org/district/employment_opportunities',
'http://www.charterschoolofeducationalexcellence.org/apps/pages/index.jsp?uREC_ID=386672&type=d&pREC_ID=879215',
'http://www.chateaugaycsd.org/employment',
'http://www.chathamcentralschools.com/district/employment',
'http://www.cheektowagacentral.org',
'http://www.chittenangoschools.org',
'http://www.chslsj.org/apps/pages/index.jsp?uREC_ID=482551&type=d&pREC_ID=1018626',
'http://www.cityschoolofthearts.org',
'http://www.clarenceschools.org/Page/3205',
'http://www.clevehill.wnyric.org/Page/357',
'http://www.cliftonfine.org/cliftonfine.org/district/employment',
'http://www.clydesavannah.org/district/employment_opportunities',
'http://www.clymercsd.org/site/Default.aspx?PageID=118',
'http://www.cmcs.org/news-events/stories/charter-school-countdown',
'http://www.commackschools.org/employment.aspx',
'http://www.copiague.k12.ny.us/our_district/employment',
'http://www.corningareaschools.com/content/vacai',
'http://www.cortlandschools.org/teacherpage.cfm?teacher=814',
'http://www.cpcsteam.org/district/employment',
'http://www.cps.k12.ny.us/departments/oip_employment',
'http://www.crcs.k12.ny.us',
'http://www.croton-harmonschools.org',
'http://www.csh.k12.ny.us/domain/49',
'http://www.cvcsd.stier.org',
'http://www.deerparkschools.org/staff/job_opportunities',
'http://www.delhischools.org',
'http://www.depewschools.org',
'http://www.depositcsd.org',
'http://www.deruyter.k12.ny.us/districtpage.cfm?pageid=518',
'http://www.dfsd.org/domain/239',
'http://www.dolgeville.org',
'http://www.doverschools.org/page.cfm?p=5039',
'http://www.dryden.k12.ny.us',
'http://www.dundeecs.org/staff/job_opportunities',
'http://www.dunkirkcsd.org',
'http://www.eastauroraschools.org/domain/56',
'http://www.eastchester.k12.ny.us',
'http://www.easthamptonschools.org/district/employment',
'http://www.eastmeadow.k12.ny.us/our_district/human_resources',
'http://www.eastquogue.k12.ny.us',
'http://www.eastrockawayschools.org/district/employment',
'http://www.ecs.k12.ny.us',
'http://www.edencsd.org/Page/10',
'http://www.edgemont.org/district/human-resources/employment',
'http://www.edinburgcs.org/employment-opportunities.html',
'http://www.edmestoncentralschool.net/job-of-the-week',
'http://www.eicsd.k12.ny.us',
'http://www.eischools.org/district/personnel_services',
'http://www.ekcsk12.org/domain/134',
'http://www.elbacsd.org/domain/47',
'http://www.ellicottvillecentral.com',
'http://www.elmiracityschools.com',
'http://www.elmontschools.org/Page/381',
'http://www.elwood.k12.ny.us/departments/human_resources',
'http://www.emblazeacademy.org',
'http://www.emhcharter.org/careers',
'http://www.emoschools.org/Employment.aspx',
'http://www.equalitycharterschool.org/careers',
'http://www.ercsd.org/Page/440',
'http://www.erschools.org/departments/employment/employment_opportunities',
'http://www.esmonline.org',
'http://www.esmschools.org/district.cfm?subpage=24415',
'http://www.evcsbuffalo.org/careers',
'http://www.ewsdonline.org',
'http://www.explorenetwork.org/empower-charter-schoo',
'http://www.explorenetwork.org/empower-charter-school',
'http://www.explorenetwork.org/exceed-charter-school',
'http://www.explorenetwork.org/explore-charter-school',
'http://www.fabiuspompey.org',
'http://www.fallsburgcsd.net',
'http://www.farmingdaleschools.org/domain/2290',
'http://www.fi.k12.ny.us/district/employment',
'http://www.fillmorecsd.org/domain/209',
'http://www.fischool.com',
'http://www.floralpark.k12.ny.us/Page/1164',
'http://www.floridaufsd.org',
'http://www.fmschools.org/departments-services/employment',
'http://www.fortannschool.org/district/job_opportunities',
'http://www.fortedward.org',
'http://www.forteprep.org',
'http://www.fortplain.org/contact-us/employment',
'http://www.frankfort-schuyler.org/Page/47',
'http://www.franklinsquare.k12.ny.us',
'http://www.fredonia.wnyric.org/Page/80',
'http://www.freeportschools.org/district/employment_opportunities',
'http://www.frewsburgcsd.org/domain/146',
'http://www.friendship.wnyric.org/Page/39',
'http://www.frontier.wnyric.org/Page/118',
'http://www.fultoncsd.org/districtpage.cfm?pageid=119',
'http://www.galwaycsd.org',
'http://www.gananda.org/apps/jobs',
'http://www.gblions.org/Page/67',
'http://www.gcacs.org/District/1765-Job-Opportunities.html',
'http://www.gccschool.org',
'http://www.gcsk12.org/about-us/employment',
'http://www.genevacsd.org/Page/285',
'http://www.germantowncsd.org/Page/71',
'http://www.gjrufsd.org',
'http://www.glencove.k12.ny.us/staff_resources/employment',
'http://www.globalccs.org',
'http://www.globalcommunitycs.org/careers',
'http://www.gowcsd.org/employment-opportunities',
'http://www.granvillecsd.org/Page/27',
'http://www.greatneck.k12.ny.us/Page/3453',
'https://www.applitrack.com/greececsd/onlineapp/default.aspx?all=1',
'http://www.greenburgh-graham.org',
'http://www.greenburgheleven.org/employment.html',
'http://www.greenburghnorthcastleschools.com',
'http://www.greenecsd.org',
'http://www.greentechhigh.org/career-opportunities',
'http://www.grotoncs.org/districtpage.cfm?pageid=1407',
'http://www.guilderlandschools.org',
'http://www.gwlufsd.org/domain/41',
'http://www.halfhollowhills.k12.ny.us/district/career-opportunities',
'http://www.hamburgschools.org/Page/251',
'http://www.hamiltoncentral.org/domain/66',
'http://www.hammondsportcsd.org/domain/65',
'http://www.hannibalcsd.org',
'http://www.harborcharter.org/apps/jobs',
'http://www.harborfieldscsd.net/employment/employment_opportunities',
'http://www.harlemlink.org/open-positions.html',
'http://www.harrisoncsd.org/index.php/current-job-vacancies/certificated-openings',
'http://www.hartfordcsd.org/Page/797',
'http://www.hauppauge.k12.ny.us/Page/2668',
'http://www.hbschools.us/district/employment',
'http://www.hccs-nys.org',
'http://www.hccs-nys.org',
'http://www.hcks.org/district/human-resources',
'http://www.hczpromise.org/careers/current-openings',
'http://www.heightsschools.com',
'http://www.heketi.org',
'http://www.hempsteadschools.org/Page/120',
'http://www.henhudschools.org/domain/1148',
'http://www.henryjohnsoncs.org',
'http://www.herricks.org/Page/167',
'http://www.hewlett-woodmere.net',
'http://www.hfcsd.org',
'http://www.hffmcsd.org/Page/66',
'http://www.hicksvillepublicschools.org',
'http://www.highland-k12.org/Page/23',
'http://www.hinsdalebobcats.org/Page/107',
'http://www.hirebridge.com/jobseeker2/Searchjobresults.asp?cid=5577',
'http://www.hlacharterschool.org',
'http://www.hlcs.org/?DivisionID=22236&ToggleSideNav=ShowAll',
'http://www.holland.wnyric.org/Page/32',
'http://www.holleycsd.org/JobOpportunities1.aspx',
'http://www.honeoye.org/apps/jobs',
'http://www.hoosickfallscsd.org',
'http://www.hoosicvalley.k12.ny.us/district/jobs',
'http://www.horseheadsdistrict.com',
'http://www.hpschools.org/Page/1693',
'http://www.hudsoncityschooldistrict.com/employment',
'http://www.hufsd.edu/leadership/hr.html',
'http://www.hydebronxny.org/careers',
'http://www.hydebrooklyn.org',
'http://www.icahncharterschool1.org',
'http://www.icahncharterschool2.org',
'http://www.icahncharterschool3.org',
'http://www.icahncharterschool4.org',
'http://www.icahncharterschool5.org',
'http://www.icahncharterschool6.org',
'http://www.icahncharterschool7.org',
'http://www.ichabodcrane.org/district/employment',
'http://www.icsnyc.org/careers',
'http://www.ilcsd.org',
'http://www.ips.k12.ny.us/employment_opportunities',
'http://www.ircsd.org/about_i_r_c_s_d/employment_opportunities',
'http://www.iroquoiscsd.org/domain/12',
'http://www.islandtrees.org/districtinformation/employment.htm',
'http://www.islipufsd.org/staff/professional_employment_opportunities',
'http://www.jamestownpublicschools.org',
'http://www.jamesvilledewitt.org/employment',
'http://www.jcschools.com/Departments/Personnel/personnel.html',
'http://www.jecsd.org/districtpage.cfm?pageid=1586',
'http://www.jeffersoncs.org/about_j_c_s/district_job_opportunities',
'http://www.johnsburgcsd.org',
'http://www.jtcsd.org/Page/51',
'http://www.jvlwildcat.org',
'http://www.k12.ginet.org/Page/932',
'http://www.kccs.org/employment.html',
'http://www.keenecentralschool.org/about-us/employment',
'http://www.kendallschools.org/district2.cfm?subpage=1169',
'http://www.kingstoncityschools.org',
'http://www.kippnyc.org/schools/kipp-amp-elementary',
'http://www.kippnyc.org/schools/kipp-infinity-elementary',
'http://www.kippnyc.org/schools/kipp-star-middle-school',
'http://www.kippnyc.org/schools/kipp-washington-heights-middle-school',
'http://www.kipptechvalley.org',
'http://www.klschools.org/groups/4498/human_resources/career_opportunities',
'http://www.lacimacharterschool.org',
'http://www.lackawannaschools.org',
'http://www.lafargevillecsd.org/Page/187',
'http://www.lafayetteschools.org/teacherpage.cfm?teacher=247',
'http://www.lakelandschools.org/departments/human_resources/employment.php',
'http://www.lakeshore.wnyric.org/Page/282',
'http://www.lancasterschools.org/Page/468',
'http://www.lansingburgh.org/Page/38',
'http://www.lansingschools.org/districtpage.cfm?pageid=1204',
'http://www.launchschool.org/careers-launch',
'http://www.laurenscs.org/Employment.aspx',
'http://www.lavelleprep.org',
'http://www.lawrence.org',
'http://www.lbeach.org/departments/opportunities',
'http://www.letchworth.k12.ny.us/domain/1056',
'http://www.levittownschools.com/departments/administrative/hr/employment',
'http://www.lfcsd.org',
'http://www.libertyk12.org/about-us/employment',
'http://www.lighthouse-academies.org/schools/metropolitan',
'http://www.lindenhurstschools.org/our_district/employment',
'http://www.littleflowerufsd.org',
'http://www.liverpool.k12.ny.us/departments/human-resources/job-opportunities',
'http://www.livoniacsd.org/Page/537',
'http://www.lkgeorge.org/Page/40',
'http://www.lockportschools.wnyric.org/Page/194',
'http://www.longlakecsd.org/employment',
'http://www.longwood.k12.ny.us',
'http://www.lpcsd.org/employment',
'http://www.lpschool.com',
'http://www.lvcsd.k12.ny.us',
'http://www.lymecsd.org/domain/31',
'http://www.lynbrookschools.org/departments/personnel_office',
'http://www.lyncourtschool.org/districtpage.cfm?pageid=259',
'http://www.lyndonvillecsd.org',
'http://www.lyonscsd.org/Page/1374',
'http://www.m-ecs.org/departments/business_office/human_resources/vacancy_postings',
'http://www.madisoncentralny.org/domain/176',
'http://www.mahopac.k12.ny.us/groups/11079/human_resources/home',
'http://www.malonecsd.org/employment.html',
'http://www.malverne.k12.ny.us/district/employment',
'http://www.mamkschools.org/district/personnel/employment-opportunities',
'http://www.manhattancharterschool.org',
'http://www.marathonschools.org/job-postings.html',
'http://www.marcellusschools.org/teacherpage.cfm?teacher=816',
'http://www.mayfieldk12.com',
'http://www.mcgrawschools.org/teacherpage.cfm?teacher=842',
'http://www.mechanicville.org/Page/189',
'http://www.medinacsd.org/Page/761',
'http://www.merrick.k12.ny.us/district/job_opportunities',
'http://www.merrickacademy.org',
'http://www.middleburgh.k12.ny.us',
'http://www.middletowncityschools.org',
'http://www.midlakes.org/Page/43',
'http://www.mineola.k12.ny.us/district/human_resources',
'http://www.minervasd.org',
'http://www.minisink.com/index.php?id=11',
'http://www.mmcsd.org/Page/19',
'http://www.montaukschool.org/domain/16',
'http://www.moraviaschool.org/teacherpage.cfm?teacher=1831',
'http://www.moriahk12.org/employment.html',
'http://www.morriscs.org',
'http://www.mpbschools.org',
'http://www.mpcsny.org',
'http://www.msd.k12.ny.us/domain/33',
'http://www.mtmorriscsd.org',
'http://www.mtplcsd.org',
'http://www.mtsinai.k12.ny.us/our_district/employment/employment.html',
'http://www.mtvernoncsd.org',
'http://www.mufsd.com/departments/human_resources/job_postings',
'http://www.mwcsk12.org',
'http://www.nacs1.org/cms/One.aspx?portalId=465963&pageId=1327562',
'http://www.naplescsd.org/districtpage.cfm?pageid=550',
'http://www.nccscougar.org/Page/29',
'http://www.ndchsbrooklyn.org/careers',
'http://www.newark.k12.ny.us/Page/455',
'http://www.newburghschools.org/page.php?page=7',
'http://www.newfane.wnyric.org/page/24',
'http://www.newfieldschools.org',
'http://www.newhartfordschools.org/Page/2553',
'http://www.newheightsacademy.org',
'http://www.newlebanoncsd.org/district/employment',
'http://www.newpaltz.k12.ny.us/domain/10',
'http://www.newsuffolkschool.com',
'http://www.newvisions.org/charter',
'http://www.newvisions.org/charter/humii',
'http://www.newvisions.org/pages/careers',
'http://www.newvisions.org/schools/entry/ams3',
'http://www.newvisions.org/schools/entry/amsii',
'http://www.newvisions.org/schools/entry/hum3',
'http://www.newvisions.org/schools/entry/humanities-iv',
'http://www.newworldprep.org',
'http://www.newyorkcharters.org/about/employment-opportunities',
'http://www.newyorkmills.org/Page/30',
'http://www.nhp-gcp.org/domain/63',
'http://www.niagaracharter.org',
'http://www.nncsk12.org/Page/36',
'http://www.northbabylonschools.net/our_district/employment_opportunities',
'http://www.northbellmoreschools.org/Page/1544',
'http://www.northgreenbushcommon.org',
'http://www.northsalemschools.org/Page/2807',
'http://www.northsidechs.org',
'http://www.northwarren.k12.ny.us/Employment.html',
'http://www.nrcsd.org/hr',
'http://www.nred.org/groups/17143/human_resources/human_resources',
'http://www.nrwcs.org/domain/38',
'http://www.nscsd.org',
'http://www.nvcs.stier.org',
'http://www.nyackschools.org/groups/6169/human_resources/home',
'http://www.nycacharterschool.org/careers',
'http://www.nycautismcharterschool.org/careers',
'http://www.ocs.cnyric.org/district.cfm?subpage=3520',
'http://www.odyoungcsd.org/Page/79',
'http://www.oesj.org',
'http://www.ogdensburgk12.org/domain/1035',
'http://www.omschools.org/employment.cfm',
'http://www.oneidacsd.org',
'http://www.opportunitycharter.org',
'http://www.opschools.org/Page/125',
'http://www.oriskanycsd.org/Page/663',
'http://www.oswego.org/personnel',
'http://www.ovcs.org',
'http://www.owncs.org/about/employment',
'http://www.oysterponds.org',
'http://www.palmaccsd.org/Content2/286',
'http://www.pancent.org/Page/27',
'http://www.pavilioncsd.org',
'http://www.pawlingschools.org',
'http://www.pbcschools.org/districtpage.cfm?pageid=1512',
'http://www.pearlriver.org/groups/55638/human_resources/employment_opportunities',
'http://www.pelhamschools.org',
'http://www.pembrokecsd.org',
'http://www.peninsulaprep.org',
'http://www.perry.k12.ny.us/Page/140',
'http://www.perucsd.org/Page/1822',
'http://www.phoenixcsd.org/Page/1053',
'http://www.pioneerschools.org/domain/48',
'http://www.pisecoschool.com',
'http://www.pittsfordschools.org/Page/928',
'http://www.plainedgeschools.org/administration/office_of_human_resources/employment_opportunities',
'http://www.plattscsd.org/district/human-resources/employment-opportunities',
'http://www.pleasantvilleschools.com',
'http://www.pocanticohills.org/human_resources',
'http://www.polandcs.org/domain/270',
'http://www.portchesterschools.org/employment__job_postings',
'http://www.portjeff.k12.ny.us',
'http://www.portjerviscsd.k12.ny.us/departments/employment-opportunities',
'http://www.portville.wnyric.org',
'http://www.potsdam.k12.ny.us/apps/pages/index.jsp?uREC_ID=747176&type=d&pREC_ID=1248094',
'http://www.ppcsd.org/Employment',
'http://www.publicprep.org/careers',
'http://www.pulaskicsd.org/districtpage.cfm?pageid=511',
'http://www.putnamcsd.org/employment.html',
'http://www.pval.org/Page/20',
'http://www.randolphacademy.org',
'http://www.randolphcsd.org/domain/24',
'http://www.rcacs.org',
'http://www.rccsd.org/apps/jobs',
'http://www.rcsd.k12.ny.us/district/employment',
'http://www.redhookcentralschools.org',
'http://www.remsencsd.org/Page/1050',
'http://www.renaissancecharter.org',
'http://www.rhinebeckcsd.org/pagecontent.php?id=69',
'http://www.richfieldcsd.org/Page/442',
'http://www.riverhead.net/district/employment',
'http://www.rocachieve.org',
'http://www.rockypointschools.org',
'http://www.romecsd.org',
'http://www.rondout.k12.ny.us',
'http://www.roscoe.k12.ny.us/Page/88',
'http://www.roxburycs.org',
'http://www.royhart.org/Page/269',
'http://www.rvcschools.org/departments_and_programs/personnel/employment_opportunities',
'http://www.ryeneck.k12.ny.us',
'http://www.sachem.k12.ny.us/district/employment_opportunities',
'http://www.sacketspatriots.org/our_district/employment_opportunities',
'http://www.sacsny.com/careers',
'http://www.sagaponackschool.com',
'http://www.sagharborschools.org',
'http://www.salamancany.org',
'http://www.salemcsd.org',
'http://www.sascs.org',
'http://www.schenectady.k12.ny.us',
'http://www.schenevuscsd.org/EmploymentOpportunities.aspx',
'http://www.schodack.k12.ny.us/district/employment',
'http://www.schoharie.k12.ny.us',
'http://www.schroonschool.org/?page_id=30',
'http://www.scio.wnyric.org/districtpage.cfm?pageid=334',
'http://www.seaford.k12.ny.us',
'http://www.sewanhaka.k12.ny.us',
'http://www.sfcs.k12.ny.us/Page/4406',
'http://www.shelterisland.k12.ny.us/domain/104',
'http://www.shufsd.org/district/employment',
'http://www.silvercreekschools.org',
'http://www.sisuluwalker.org/employment-listings',
'http://www.skanschools.org/districtpage.cfm?pageid=363',
'http://www.skcs.org/Employment.aspx',
'http://www.slcs.org/district-office/employment-applications',
'http://www.sloanschools.org/Page/639',
'http://www.smithtown.k12.ny.us/district/district_documents',
'http://www.solvayschools.org/districtpage.cfm?pageid=346',
'http://www.somersschools.org/Page/3984',
'http://www.southamptonschools.org/Page/56',
'http://www.southbronxcommunity.org/employment',
'http://www.southbuffalocs.org/domain/6',
'http://www.southcountry.org/departments/employment_opportunities',
'http://www.southerncayuga.org',
'https://www.southlewis.org/employment-opportunities--163',
'http://www.southseneca.com/districtpage.cfm?pageid=780',
'http://www.spackenkillschools.org/departments/human_resources',
'http://www.spartanpride.org/districtpage.cfm?pageid=1729',
'http://www.spencerportschools.org/departments_and_programs/human_resources/JobOpportunities',
'http://www.springsschool.org/district/employment',
'http://www.springvillegi.org/available-positions',
'https://www.applitrack.com/salmonriver/onlineapp/jobpostings/view.asp?internaltransferform.Url=&all=1',
'http://www.stamfordcs.org/Employment.aspx',
'http://www.starpointcsd.org/Page/42',
'http://www.sthopeleadershipacademy.org/apps/jobs',
'http://www.stockbridgevalley.org',
'http://www.successacademies.org/schools/bushwick',
'http://www.successacademies.org/schools/far-rockaway',
'http://www.successacademies.org/schools/flatbush',
'http://www.successacademies.org/schools/hudson-yards',
'http://www.successacademies.org/schools/south-jamaica',
'http://www.sufferncentral.org/human-resources',
'http://www.svcsd.org',
'http://www.svecsd.org',
'http://www.svsabers.org/EmploymentOpportunities.aspx',
'http://www.swcsd.org/Page/194',
'http://www.swrschools.org/our_district/employment',
'http://www.syosset.k12.ny.us/district/employment_information',
'http://www.taconichills.k12.ny.us/site/Default.aspx?PageID=193',
'http://www.tbafcs.org/Page/1444',
'http://www.tbcsc.org/english/join-the-bcsc-team',
'http://www.tburgschools.org/districtpage.cfm?pageid=433',
'http://www.tepcharter.org',
'http://www.tfoaprofessionalprep.org',
'http://www.theamericandreamschool.org',
'http://www.thewcs.org/employment.php',
'http://www.ticonderogak12.org/Employment',
'http://www.tiogacentral.org',
'http://www.tonawandacsd.org/Page/39',
'http://www.towschool.org/our_district/employment_opportunities',
'http://www.troycsd.org/district-services/human-resources',
'http://www.tuckahoeschools.org/employment_opportunities',
'http://www.tufsd.org/Page/49',
'http://www.tupperlakecsd.net',
'http://www.tuxedoufsd.org',
'http://www.uascs.org/index.php/careers',
'http://www.uek12.org/Employment.aspx',
'https://www.unatego.org/Employment.aspx',
'http://www.unionspringscsd.org/districtpage.cfm?pageid=193',
'http://www.unityprep.org/careers/teaching-at-unity',
'http://www.upreprochester.org',
'http://www.uvstorm.org/EmploymentOpportunities.aspx',
'http://www.valhallaschools.org',
'http://www.valleystream30.com/our_district/employmentcareers',
'http://www.valleystreamdistrict24.org/employment-opportunities-1.html',
'http://www.vcsd.k12.ny.us/Page/114',
'http://www.vertusschool.org/careers',
'http://www.vestal.stier.org/CurrentVacancies.aspx',
'http://www.voicecharterschool.org',
'http://www.voorheesville.org/domain/40',
'http://www.vschsd.org/district/employment',
'http://www.vvsschools.org/domain/16',
'http://www.wacs.wnyric.org/Page/1330',
'http://www.wainscottschool.org',
'http://www.wajcs.org/?PageName=bc&n=246209',
'http://www.wallkillcsd.k12.ny.us/domain/258',
'http://www.waltoncsd.org',
'http://www.wantaghschools.org/domain/956',
'http://www.wappingersschools.org',
'http://www.warsaw.k12.ny.us/Page/358',
'http://www.watervillecsd.org/site/default.aspx?pageid=1',
'http://www.wboro.org/Page/32',
'http://www.wbschools.org/District/employment_opportunities',
'http://www.wccsk12.org',
'http://www.wcsd.org/district/employment_opportunities',
'http://www.web.milfordcentral.org/district/job_opportunities',
'http://www.websterschools.org',
'http://www.weedsport.org',
'http://www.wellscsd.org/district-information/employment-opportunities',
'http://www.wellsville.wnyric.org/Page/279',
'http://www.westburyschools.org',
'http://www.westcanada.org/domain/93',
'http://www.westhamptonbeach.k12.ny.us/district/employment',
'http://www.westhillschools.org/teacherpage.cfm?teacher=448',
'http://www.westminsterccs.org/careers',
'http://www.westmorelandschool.org/Page/1867',
'http://www.westportcs.org/Page/55',
'http://www.wfsd.k12.ny.us/index.php/employment-opportunities',
'http://www.wgcsd.org/employment.cfm',
'http://www.whitesville.wnyric.org/domain/91',
'http://www.whufsd.com/district/human_resources',
'http://www.whufsd.org',
'http://www.wi.k12.ny.us/district/office_of_human_resources',
'http://www.williamsvillek12.org/departments/human_resources/career_opportunities.php',
'http://www.willsborocsd.org/district/employment',
'http://www.worcestercs.org/employment-opportunities.html',
'http://www.wufsk8.com',
'http://www.wvalley.wnyric.org/Page/159',
'http://www.wyandanch.k12.ny.us',
'http://www.wynantskillufsd.org/district/employment',
'http://www.yalowcharter.org/jobs',
'http://www.yonkerspublicschools.org/Page/1191',
'http://www.yorkcsd.org/Page/65',
'http://www1.homercentral.org/district/employment',
'https://ambercharter.tedk12.com/hire/index.aspx',
'https://ats1.searchsoft.net/ats/app_login.shtml?COMPANY_ID=00004834',
'https://auburn.tedk12.com/hire/index.aspx',
'https://boards.greenhouse.io/bsnbcscareers',
'https://boards.greenhouse.io/eastharlemtutorialprogram',
'https://boldschools.org/careers',
'https://broomestreetacademy.org/careers',
'https://buffsci.org/our-school',
'https://careers-ascendlearning.icims.com/jobs/search?ss=1&hashed=-435681916',
'https://careers.smartrecruiters.com/UncommonSchools',
'https://careers.wearedream.org/careers',
'https://catskillcsd.org/employment',
'https://cazenoviacsd.com/homes/staff-resources/employment-opportunities',
'https://ccrsk12.org/opportunities',
'https://delhi.interviewexchange.com/static/clients/409SDM1/index.jsp;jsessionid=617C89830CE8E53BF77CF8B7589D5895;jsessionid=0332E7A4D070E2A91EFCC6FF4283BD74',
'https://docs.google.com/document/d/1QZP04N1Yi1bssffXJhoEJn1gSsq7kw7-ib4YvGHHvuY',
'https://docs.google.com/document/d/1eLpsys_UJnYhr6pnwzJEBeBmbty9d4ztz0i3i5bGmP4/edit?usp=sharing',
'https://excellence-community-schools.workable.com',
'https://havenacademy.org/join-us/employment-opportunities',
'https://hebrewpublic.org/careers-at-hebrew-public',
'https://hlacharterschool.org',
'https://inwoodacademy.org/careers/openings',
'https://jobs.lever.co/drihscs',
'https://jobs.schoolsites.com/CCCSD/jobs.cfm',
'https://jobs.successacademies.org',
'https://ncschools.org/about-ncs/careers-at-ncs',
'https://newrootsschool.org/employment-opportunities',
'https://ossiningufsd.org/departments/human-resources',
'https://paveschools.org',
'https://platform.teachermatch.org/jobsboard.do?districtId=264888318',
'https://plus.google.com/s/%23Employment/posts',
'https://recruiting.paylocity.com/recruiting/jobs/List/2903/Harriet-Tubman-Charter-School',
'https://renacad.org/contact/employment',
'https://rew11.ultipro.com/BER1014/JobBoard/listjobs.aspx',
'https://riverheadcharterschool.org/join-us/careers-at-riverhead',
'https://sbecacs.org/careers',
'https://www.falconercsd.org/Page/4747',
'https://www.swcsk12.org/Page/19',
'https://sites.google.com/a/northvillecsd.org/ncsd/home/district/community/local-job-postings',
'https://sites.google.com/htcschools.org/htcemployment/home',
'https://stradfordprep.org',
'https://tapestryschool.org/about-tapestry/careers',
'https://tech.dcboces.org/recruitment/posting/browse_all.php',
'https://udteam.org/employment',
'https://uncommonschools.secure.force.com/careers',
'https://urbanassembly.org/career',
'https://urbanchoicecharter.org/employment',
'https://www.abewing.org/aws',
'https://www.achievementfirst.org/careers',
'https://www.achievementfirst.org/schools/new-york-schools',
'https://www.adirondackcsd.org/welcome/employment_opportunities',
'https://www.aftoncsd.org/Employment1.aspx',
'https://www.albanyschools.org/employment/index.html',
'https://www.alexandercsd.org/apps/pages/index.jsp?uREC_ID=887506&type=d&pREC_ID=1238008',
'https://www.applitrack.com/caboces/onlineapp/default.aspx?choosedistrict=true&applitrackclient=38921',
'https://www.applitrack.com/fairportcsd/onlineapp/default.aspx?all=1',
'https://www.applitrack.com/gateschili/onlineapp/default.aspx?all=1',
'https://www.applitrack.com/hohschools/onlineapp/default.aspx?all=1',
'https://www.applitrack.com/honeoye/onlineapp/default.aspx?all=1',
'https://www.applitrack.com/oacsd/onlineapp/default.aspx?all=1',
'https://www.applitrack.com/penfield/onlineapp/default.aspx?all=1',
'https://www.applitrack.com/rhcsd/onlineapp/default.aspx?all=1',
'https://www.applitrack.com/saugertiesk12/onlineapp/jobpostings/view.asp?all=1',
'https://www.applitrack.com/sidney/onlineapp/default.aspx?all=1',
'https://www.applitrack.com/watertowncsd/onlineapp/default.aspx?all=1',
'https://www.applitrack.com/wheatlandchili/onlineapp/default.aspx?all=1',
'https://www.applitrack.com/yorktown/onlineapp/default.aspx?all=1',
'https://www.apwschools.org/Page/1083',
'https://www.arkportcsd.org/Page/121',
'https://www.atmosphereacademy.org/contact-us/careers/current-openings',
'https://www.aufsd.org/Page/93',
'https://www.barkercsd.net/Page/3945',
'https://www.bayshoreschools.org/jobs.cfm',
'https://www.belahs.org',
'https://www.bethlehemschools.org/employment',
'https://www.bgcsd.org/Employment.aspx',
'https://www.bkwschools.org/employment',
'https://www.bradfordcsd.org/our-school/employment',
'https://www.brewsterschools.org/departments/humanresources/employment',
'https://www.bronxbetterlearning.org',
'https://www.bronxvilleschool.org',
'https://www.brooklyncharter.org/about/employment',
'https://www.brooklynlaboratoryschool.org/careers',
'https://www.buffalocollegiate.org/careers',
'https://www.byramhills.org/departments/human-resources/career-opportunities',
'https://www.cacsd.org/domain/188',
'https://www.canajoharieschools.org/employment',
'https://www.capitalregionboces.org/employment/job-openings',
'https://www.cattlv.wnyric.org/Page/20',
'https://www.applitrack.com/Chappaqua/onlineapp/default.aspx?all=1',
'https://www.cforks.org/Employment.aspx',
'https://www.clake.org/District/1748-Untitled.html',
'https://www.communityroots.org/apps/pages/index.jsp?uREC_ID=279770&type=d&pREC_ID=632492',
'https://www.cooperstowncs.org/o/cooperstown-csd/page/employment-information--13',
'https://www.corinthcsd.org/employment-opportunities',
'https://www.cornwallschools.com/apps/pages/index.jsp?uREC_ID=310699&type=d&termREC_ID=&pREC_ID=577553',
'https://www.cpcsschool.org/careers',
'https://www.creoprep.org/careers',
'https://www.csat-k12.org/Page/1829',
'https://www.cvalleycsd.org/human-resources',
'https://www.cvscs.org/EmploymentOpportunities.aspx',
'https://www.dansvillecsd.org/Page/2394',
'https://www.dcseagles.org/employment.aspx',
'https://www.duanesburg.org',
'https://www.elcsd.org/Page/30',
'https://www.explorationrochester.org',
'https://www.fondafultonvilleschools.org/about/employment',
'https://www.forestville.com/domain/10',
'https://www.franklincsd.org/Employment.aspx',
'https://www.futureleadersinstitute.org/about-us/careers',
'https://www.gasd.org/employment',
'https://www.gcsny.org/employment',
'https://www.genvalley.org/Page/49',
'https://www.gesdk12.org/employment',
'https://www.gmucsd.org/Employment.aspx',
'https://www.greenburghcsd.org/domain/45',
'https://www.gugcs.org/apps/jobs',
'https://www.haldaneschool.org/departments/employment-resources/employment-opportunities',
'https://www.hancock.stier.org/Employment.aspx',
'https://www.hcs.stier.org/employment.aspx',
'https://www.hcsk12.org/Page/194',
'https://www.hdcsk12.org/Page/29',
'https://www.herkimercsd.org/employment',
'https://www.heuvelton.k12.ny.us',
'https://www.hpcsd.org/Page/412',
'https://www.irvingtonschools.org/Page/2145',
'https://www.ivyhillprep.org/careers',
'https://www.johnstownschools.org/job-openings',
'https://www.keycollegiate.org/careers',
'https://www.kippnyc.org/careers/listings',
'https://www.kippnyc.org/schools/kipp-freedom',
'https://www.kpcsd.org/apps/pages/index.jsp?dir=Job%20Postings&type=d&uREC_ID=346753',
'https://www.ktufsd.org/Page/17387',
'https://www.lew-port.com/Page/77',
'https://www.manhassetschools.org/domain/64',
'https://www.margaretvillecs.org/Employment.aspx',
'https://www.maryvaleufsd.org',
'https://www.mccsd.net/Page/317',
'https://www.mcs.k12.ny.us/apps/pages/index.jsp?uREC_ID=776749&type=d&pREC_ID=1175998',
'https://www.me.stier.org/Personnel-Employment.aspx',
'https://www.menands.org/menands_union_free_school_employ.html',
'https://www.mexicocsd.org/Page/534',
'https://www.millerplace.k12.ny.us/Domain/39',
'https://www.mohonasen.org/employment',
'https://www.monticelloschools.net/business-hr/employment',
'https://www.mw.k12.ny.us/about/employment',
'https://www.newvisions.org/aim2',
'https://www.newvisions.org/careers',
'https://www.nfschools.net/Page/3559',
'https://www.niskayunaschools.org/employment',
'https://www.northcollins.com/cms/One.aspx?portalId=272706&pageId=626890',
'https://www.northcolonie.org/about-us/employment-opportunities',
'https://www.norwichcsd.org/Vacancies.aspx',
'https://www.ntschools.org//site/Default.aspx?PageID=5052',
'https://www.nwcsd.org/Page/64',
'https://www.oahornets.org/apps/jobs',
'https://www.oesj.org',
'https://www.oleanschools.org/Page/5715',
'https://www.oneontacsd.org/EmploymentOpportunities.aspx',
'https://www.oxac.org/Employment.aspx',
'https://www.peekskillcsd.org/Page/383',
'https://www.persistenceprep.org/mission',
'https://www.phcsd.org/apps/pages/index.jsp?uREC_ID=1161786&type=d&pREC_ID=1415161',
'https://www.pinebushschools.org/departments/hr-employment',
'https://www.pmschools.org/Page/160',
'http://www.ryeschools.org',
'http://www.gufs.org',
'https://www.poughkeepsieschools.org/Page/320',
'https://www.prattsburghcsd.org/Page/26',
'https://www.pycsd.org/apps/pages/index.jsp?uREC_ID=948562&type=d&pREC_ID=1275659',
'https://www.quogueschool.com',
'https://www.railroaders.net/EmploymentHAL.php',
'https://www.rcscsd.org/about-us/employment',
'https://www.rcsdk12.org/employment',
'https://www.reachacademycharter.org/employment',
'https://www.rooseveltufsd.org/Page/325',
'https://www.sandycreekcsd.org',
'https://www.saratogaschools.org/district.cfm?subpage=1383228',
'https://www.sayvilleschools.org/Page/3271',
'https://www.scarsdaleschools.k12.ny.us/Page/19564',
'https://www.schoolinthesquare.org/our-team/join-our-team',
'https://www.schuylervilleschools.org/employment',
'https://www.scsd.org/employment',
'https://www.secsd.org/Employment.aspx',
'https://www.sgfcsd.org/human-resources',
'https://www.sharonsprings.org/employment',
'https://www.shenet.org/employment',
'https://www.socsd.org',
'https://www.southcolonieschools.org/departments/human-resources-department/employment-opportunities',
'https://www.stregiscsd.org/faculty-staff',
'https://www.successacademies.org/schools',
'https://www.sunyacc.edu/careers',
'https://www.theuftcharterschool.org',
'https://www.trivalleycsd.org/domain/124',
'https://www.valencecollegeprep.org',
'https://www.warwickvalleyschools.com/employment',
'https://www.waterloocsd.org/Page/66',
'https://www.watervlietcityschools.org/employment',
'https://www.webutuckschools.org/Page/29',
'https://www.westgenesee.org/staff-resources/job-opportunities',
'https://www.whiteplainspublicschools.org/Page/546',
'https://www.wilsoncsd.org/site/Default.aspx?PageID=77',
'https://www.windsor-csd.org/Employment.aspx',
'https://www.wpcsd.org/EmploymentOpportunities.aspx',
'https://www.ws.k12.ny.us/JobPostings.aspx',
'https://www.wscschools.org/Page/291',
'https://www.wyomingcsd.org/Page/20',
'https://zetaschools.org/careers'
)


    uni_list2 = (
'http://careers.canisius.edu/cw/en-us/listing',
'http://careers.marist.edu/cw/en-us/listing'
)


    # University URLs, initial crawl levels, and coordinates database
    uni_list = (
'http://careers.canisius.edu/cw/en-us/listing',
'http://careers.marist.edu/cw/en-us/listing',
'http://cooper.edu/work/employment-opportunities',
'http://einstein.yu.edu/administration/human-resources/career-opportunities.html',
'http://gts.edu/job-postings',
'http://huc.edu/about/employment-opportunities',
'http://humanresources.vassar.edu/jobs',
'http://inside.manhattan.edu/offices/human-resources/jobs.php',
'http://jobs.medaille.edu',
'http://jobs.union.edu/cw/en-us/listing',
'http://liu.edu/brooklyn.aspx',
'http://newschool.edu/public-engagement',
'http://niagaracc.suny.edu/careers/nccc-jobs.php',
'http://sunysccc.edu/About-Us/Office-of-Human-Resources/Employment-Opportunities',
'http://utica.edu/hr/employment.cfm',
'http://www.bard.edu/employment/employment',
'http://www.berkeleycollege.edu/index.htm',
'http://www.canton.edu/human_resources/job_opportunities.html',
'http://www.cazenovia.edu/campus-resources/human-resources/employment-opportunities',
'http://www.colgate.edu/working-at-colgate',
'http://www.college.columbia.edu',
'http://www.columbia.edu/cu/ssw',
'http://www.dental.columbia.edu',
'http://www.dyc.edu/about/administrative-offices/human-resources/career-opportunities.aspx',
'http://www.gs.columbia.edu',
'http://www.houghton.edu/campus/human-resources/employment',
'http://www.hunter.cuny.edu/hr/Employment',
'http://www.jtsa.edu/jobs-at-jts',
'http://www.law.columbia.edu',
'http://www.liu.edu/post',
'http://www.mcny.edu/index.php',
'http://www.monroecc.edu/employment',
'http://www.nccc.edu/careers-2',
'http://www.nycc.edu/employment-opportunities',
'http://www.nyts.edu',
'http://www.nyu.edu/about/careers-at-nyu.html',
'http://www.paulsmiths.edu/humanresources/employment',
'http://www.potsdam.edu/crane',
'http://www.qcc.cuny.edu/employment/index.html',
'http://www.rit.edu/employment_rit.html',
'http://www.rochester.edu/working/hr/jobs',
'http://www.simon.rochester.edu/faculty-and-research/faculty-directory/faculty-recruitment/index.aspx',
'http://www.sunyacc.edu/job-listings',
'http://www.sunywcc.edu/about/jobshuman-resources',
'http://www.webb.edu/employment',
'http://www.youngwomenscollegeprep.org',
'http://www1.cuny.edu/sites/onboard/homepage/getting-started/campus/medgar-evers-college',
'http://www1.sunybroome.edu/about/employment',
'https://albany.interviewexchange.com/jobsrchresults.jsp',
'https://alfredstate.interviewexchange.com/static/clients/481ASM1/index.jsp',
'https://apply.interfolio.com/14414/positions',
'https://careers-nyit.icims.com/jobs/search?ss=1',
'https://careers.barnard.edu',
'https://careers.columbia.edu',
'https://careers.columbia.edu/content/how-apply',
'https://careers.mountsinai.org/jobs?page=1',
'https://careers.newschool.edu',
'https://careers.pace.edu/postings/search',
'https://careers.pageuppeople.com/876/cw/en-us/listing',
'https://careers.skidmore.edu/postings/search',
'https://clarkson.peopleadmin.com',
'https://clinton.interviewexchange.com/static/clients/552CCM1/index.jsp',
'https://cobleskill.interviewexchange.com/static/clients/474SCM1/index.jsp',
'https://cshl.peopleadmin.com/postings/search',
'https://cuny.jobs',
'https://daemen.applicantpro.com/jobs',
'https://employment.acphs.edu/postings/search',
'https://employment.potsdam.edu/postings/search',
'https://employment.stlawu.edu/postings/search',
'https://farmingdale.interviewexchange.com/static/clients/383FAM1/index.jsp',
'https://fitnyc.interviewexchange.com/static/clients/391FIM1/index.jsp',
'https://fredonia.interviewexchange.com/static/clients/471SFM1/index.jsp',
'https://genesee.interviewexchange.com/static/clients/374GCM1/index.jsp',
'https://herkimer.interviewexchange.com/static/clients/505HCM1/index.jsp',
'https://hr.adelphi.edu/position-openings',
'https://hr.cornell.edu/jobs',
'https://hvcc.edu/hr/employment-opportunities.html',
'https://iona-openhire.silkroad.com/epostings/index.cfm?fuseaction=app.jobsearch',
'https://ithaca.peopleadmin.com',
'https://jobs.buffalostate.edu',
'https://jobs.cortland.edu',
'https://jobs.excelsior.edu',
'https://jobs.geneseo.edu/postings/search',
'https://jobs.liu.edu/#/list',
'https://jobs.mercy.edu/postings/search',
'https://jobs.naz.edu/postings/search',
'https://jobs.niagara.edu/JobPostings.aspx',
'https://jobs.plattsburgh.edu/postings/search',
'https://jobs.purchase.edu/applicants/jsp/shared/frameset/Frameset.jsp',
'https://jobs.sjfc.edu',
'https://jobsatupstate.peopleadmin.com/applicants/jsp/shared/search/SearchResults_css.jsp',
'https://law-touro-csm.symplicity.com/students/index.php/pid170913',
'https://maritime.interviewexchange.com/static/clients/373SMM1/index.jsp',
'https://mountsaintvincent.edu/campus-life/campus-services/human-resources/employment-opportunities',
'https://mvcc.csod.com/ats/careersite/search.aspx',
'https://ncc.interviewexchange.com/static/clients/489NCM1/index.jsp',
'https://occc.interviewexchange.com/static/clients/437SOM1/index.jsp',
'https://oldwestbury.interviewexchange.com/static/clients/519OWM1/index.jsp',
'https://oswego.interviewexchange.com/static/clients/313OSM1/index.jsp',
'https://pa334.peopleadmin.com/postings/search',
'https://recruiting.ultipro.com/CUL1001CLNRY/JobBoard/5d1a692d-cf6b-4b4f-8652-c60b25898609/?q=&o=postedDateDesc',
'https://rpijobs.rpi.edu',
'https://strose.interviewexchange.com/jobsrchresults.jsp',
'https://suny.oneonta.edu/sponsored-programs/employment-opportunities',
'https://sunydutchess.interviewexchange.com/static/clients/539DCM1/index.jsp',
'https://sunyocc.peopleadmin.com/postings/search',
'https://sunyopt.peopleadmin.com/postings/search',
'https://sunypoly.interviewexchange.com/static/clients/511SPM1/hiring.jsp',
'https://sunysullivan.edu/offices/associate-vp-for-planning-human-resources-facilities/job-opportunities',
'https://touro.peopleadmin.com/postings/search',
'https://trocaire.applicantpro.com/jobs',
'https://utsnyc.edu/about/careers-at-union',
'https://wagner.edu/hr/hr_openings',
'https://workforcenow.adp.com/mdf/recruitment/recruitment.html?cid=b635a855-6cf7-4ee7-ba36-6da36d9f2eea&ccId=19000101_000001&type=MP',
'https://www.alfred.edu/jobs-at-alfred/index.cfm',
'https://www.bankstreet.edu/about-bank-street/job-opportunities',
'https://www.binghamton.edu/human-resources/employment-opportunities/index.html',
'https://www.brockport.edu/support/human_resources/empop/vacancies',
'https://www.brooklaw.edu/about-us/job-opportunities.aspx',
'https://www.cayuga-cc.edu/about/human-resources',
'https://www.cnr.edu/employment-opportunities',
'https://www.davisny.edu/jobs',
'https://www.dc.edu/human-resources',
'https://www.ecc.edu/work',
'https://www.elmira.edu/Student/Offices_Resources/Employment_Opportunities/index.html',
'https://www.esc.edu/human-resources/employment-opportunities',
'https://www.flcc.edu/jobs',
'https://www.fmcc.edu/about/employment-opportunities',
'https://www.fordham.edu/info/23411/job_opportunities',
'https://www.ftc.edu/employment',
'https://www.hamilton.edu/offices/human-resources/employment/job-opportunities',
'https://www.hartwick.edu/about-us/employment/human-resources/employment-opportunities',
'https://www.helenefuld.edu/employment',
'https://www.hilbert.edu/about/human-resources/hilbert-job-openings',
'https://www.hofstra.edu/about/jobs/index.html',
'https://www.hofstra.edu/academics/colleges/zarb',
'https://www.hws.edu/offices/hr/employment/index.aspx',
'https://www.juilliard.edu/jobs',
'https://www.keuka.edu/hr/employment-opportunities',
'https://www.laguardia.edu/employment',
'https://www.lemoyne.edu/Work-at-Le-Moyne',
'https://www.limcollege.edu/about-lim/careers',
'https://www.mmm.edu/offices/human-resources/Employment',
'https://www.molloy.edu/about-molloy-college/human-resources/careers-at-molloy',
'https://www.monroecollege.edu/About/Employment/u',
'https://www.morrisville.edu/contact/offices/human-resources/careers',
'https://www.msmc.edu/employment',
'https://www.msmnyc.edu/about/employment-at-msm',
'https://www.mville.edu/about-manhattanville/human-resources',
'https://www.newpaltz.edu/hr/jobs.html',
'https://www.newschool.edu/performing-arts',
'https://www.nyack.edu/site/employment-opportunities',
'https://www.paycomonline.net/v4/ats/web.php/jobs',
'https://www.qc.cuny.edu/HR/Pages/JobListings.aspx',
'https://www.roberts.edu/employment',
'https://www.rochester.edu/faculty-recruiting/positions',
'https://www.sage.edu/about/human-resources/employment-opportunities',
'https://www.sarahlawrence.edu/human-resources/job-openings.html',
'https://www.sbu.edu/jobs-at-sbu',
'https://www.sfc.edu/about/careers',
'https://www.sjcny.edu/employment',
'https://www.stac.edu/about-stac/jobs-stac',
'https://www.stjohns.edu/about/administrative-offices/human-resources/recruitment',
'https://www.stonybrookmedicine.edu/careers',
'https://www.sujobopps.com/postings/search',
'https://www.suny.edu/campuses/cornell-vet',
'https://www.suny.edu/careers/employment/index.cfm?s=y',
'https://www.sunycgcc.edu/about-cgcc/employment-cgcc',
'https://www.sunyjcc.edu/about/human-resources/jobs',
'https://www.sunyjefferson.edu/careers-jefferson/open-positions.php',
'https://www.sunyulster.edu/campus_and_culture/about_us/jobs.php',
'https://www.tkc.edu/careers-at-kings',
'https://www.tompkinscortland.edu/college-info/employment',
'https://www.ubjobs.buffalo.edu',
'https://www.usmma.edu/about/employment/career-opportunities',
'https://www.vaughn.edu/jobs',
'https://www.villa.edu/about-us/employment-opportunities',
'https://www.warner.rochester.edu/faculty/positions',
'https://www.wells.edu/jobs',
'https://www.york.cuny.edu/administrative/human-resources/jobs',
'https://www.yu.edu/hr/opportunities',
'https://www2.appone.com/Search/Search.aspx?ServerVar=ConcordiaCollege.appone.com&results=yes',
'https://www3.sunysuffolk.edu/About/Employment.asp'
)


    # Must run Docker with sudo and without VPN
    # Start Docker container
    print(os.getpid(), 'Starting Splash Docker container...')
    client = docker.from_env()
    client.containers.run("scrapinghub/splash", name='jj_con', ports={'8050/tcp': 8050}, command='--disable-private-mode --disable-browser-caches --slots 100', detach=True, remove=True)
    #client.containers.run("scrapinghub/splash", name='jj_con', ports={'8050/tcp': 8050}, detach=True, remove=True)

    # Wait for Splash to be ready
    while True:
        try:
            resp = requests.post('http://localhost:8050/_gc')
            print(os.getpid(), 'Splash is running')
            break

        except Exception as eee:
            if 'Connection reset by peer' in str(eee):
                print(os.getpid(), '...')
                time.sleep(1)
                continue


    # Get container name
    container = client.containers.get('jj_con')


    # Advanced options
    max_crawl_depth = 2
    num_procs = 32


    # URL queues
    all_urls_q = Queue() # Put all portal and working URLs in this (primary) queue

    # Create manager lists to be shared between processes
    manager = Manager()
    checkedurls_man_list = manager.list() # URLs that have been checked
    errorurls_man_dict = manager.dict() # URLs that have resulted in an error

    # Debugging
    jbw_tally_man_l = manager.list() # Used to determine the frequency that jbws are used

    # Put school URLs in queue
    for i in school_list:

        # Put civil service URLs, initial crawl level, portal url, and jbws type into queue
        all_urls_q.put([i, 0, i, 'sch'])

        # Put portal URL into checked pages
        dup_checker = dup_checker_f(i)
        checkedurls_man_list.append([dup_checker, None])

    # Clear list to free up memory
    school_list = None

    # Put university URLs in queue
    for i in uni_list:
        all_urls_q.put([i, 0, i, 'uni'])
        dup_checker = dup_checker_f(i)
        checkedurls_man_list.append([dup_checker, None])
    uni_list = None

    # Put civil service URLs in queue
    for i in civ_list:
        all_urls_q.put([i, 0, i, 'civ'])
        dup_checker = dup_checker_f(i)
        checkedurls_man_list.append([dup_checker, None])
    civ_list = None

    # Integers to be shared between processes
    qlength = all_urls_q.qsize() # Length of the primary queue
    skipped_pages = Value('i', 0) # Number of pages that have been skipped
    prog_count = Value('i', 0) # Number of pages checked
    total_count = Value('i', qlength) # Number of pages to be checked
    dock_pause = Value('i', 0) # Used to tell children to wait
    waiting_procs = Value('i', 0) # Used to tell manager that proc is waiting


    # Create child processes
    for arb_var in range(num_procs):
        worker = Process(target=scraper, args=(all_urls_q, max_crawl_depth, checkedurls_man_list, errorurls_man_dict, skipped_pages, prog_count, total_count, jbw_tally_man_l, dock_pause))
        worker.start()

    # Wait until all tasks are done
    current_prog_c = None
    while len(active_children()) > 1:
        if current_prog_c != prog_count.value:
            #if not verbose_arg: tmp = os.system('clear||cls')
            print(os.getpid(), ' Number of processes running =', len(active_children()), '\n Max crawl depth =', max_crawl_depth)
            print(os.getpid(), '\n\n\n\n Searching in:')
            print(os.getpid(), 'Civil Service')
            print(os.getpid(), 'School districts and charter schools')
            print(os.getpid(), 'Universities and colleges')

            print(os.getpid(), '\n\n Waiting for all processes to finish. Progress =', prog_count.value, 'of', total_count.value)
            current_prog_c = prog_count.value

            # Call garbage collecting periodically
            print(os.getpid(), 'mem use before:', print(os.getpid(), psutil.virtual_memory()[2]))
            resp = requests.post('http://localhost:8050/_gc')
            print(os.getpid(), 'mem use after:', print(os.getpid(), psutil.virtual_memory()[2]))

        time.sleep(6)


        # Reset container if memory usage gets too high
        if psutil.virtual_memory()[2] > 70:

            # Tell processes to wait
            dock_pause.value = 1
            print(os.getpid(), 'restarting cont...')

            # Wait for all processes to say they are waiting
            while waiting_procs.value < len(active_children()) - 1:
                print(os.getpid(), 'Procs waiting =', waiting_procs.value, len(active_children()))
                time.sleep(0.5)

            # Reset waiting_procs count
            waiting_procs.value = 0

            # Restart Splash
            container.restart()
            #container.stop()
            print(os.getpid(), 'Starting Splash Docker container...')

            #client.containers.run("scrapinghub/splash", name='jj_con', ports={'8050/tcp': 8050}, command='--disable-private-mode --disable-browser-caches', detach=True, remove=True)


            # Wait for Splash to be ready
            while True:
                try:
                    resp = requests.post('http://localhost:8050/_gc')
                    print(os.getpid(), 'Splash is running')

                    # Reset dock pause count
                    dock_pause.value = 0
                    container = client.containers.get('jj_con')
                    break

                except:
                    print(os.getpid(), '...')
                    time.sleep(3)
                    continue



    print(os.getpid(), '\n =======================  Search complete  =======================')

    # Stop container
    if client.containers.list():
        container.stop()

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
    checked_path = os.path.join(jorb_home, 'checked_pages.txt')
    with open(checked_path, "w") as checked_file:
        checked_file.write('')

    # Write checked pages to file
    with open(checked_path, "a") as checked_file:
        for kk in checkedurls_man_list:
            checked_file.write(str(kk) + ',\n')


    # Clear errorlog
    error_path = os.path.join(jorb_home, 'errorlog.txt')
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
        print(os.getpid(), '      Error 6:     HTML decode |', error6_tally)
        print(os.getpid(), '      Error 7:  Selenium error |', error7_tally)






    # Open portal URL errors in browser
    #print(os.getpid(), '\n\n Portal error URLs:')
    #for i in portal_error_list:
    #    print(os.getpid(), i)







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













