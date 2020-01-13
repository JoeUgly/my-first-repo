
# Desc: Finds all lists that are not changed and therefore should be tuples

# program cannot contain triple double quotes


# Place progam here
orig = """


# Description: Search NYS civil service and school webpages for keywords using a CLI.

# To do:
# switch to tuple where possible
# freezing
# webbrowser losing pages
# jbws back to count but limit to x occurrences?
# make jbw type mandatory?
# clear objects when done
# dub check dup checker with redirects +
# use redirects as portal url
# prevent dups from retry loop in error log -
# blacklist must be ran through dup checker

# Later versions:
# comprehensive db = org name, home url, employ url or centralized service, address, geopy location, coords
# Selenium
# false positives: search visible text only https://www.friendship.wnyric.org/domain/9
# true negatives: dynamic pages https://www.applitrack.com/penfield/onlineapp/default.aspx?all=1
# test other BS parsers
# weighted jbws
# pass interviewexchange captcha
# find postings on multiple pages

# Technical concerns:
# removing fragments and trailing slash
# case sensitivity for dup checker
# high conf true or false postive excludes potentionally good links




import datetime, gzip, os, queue, re, socket, time, urllib.parse, urllib.request, webbrowser
from multiprocessing import active_children, Lock, Manager, Process, Queue, Value
from math import sin, cos, sqrt, atan2, radians
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup




# Global variables
user_agent_str = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'

blacklist = ('herkimercounty.org/content/departments/view/9:field=services;/content/departmentservices/view/190', 'herkimercounty.org/content/departments/view/9:field=services;/content/departmentservices/view/35', 'cs.monroecounty.gov/mccs/lists', 'countyherkimer.digitaltowpath.org:10069/content/departments/view/9:field=services;/content/departmentservices/view/190', 'countyherkimer.digitaltowpath.org:10069/content/departments/view/9:field=services;/content/departmentservices/view/35', 'monroecounty.gov/mccs/lists', 'tompkinscivilservice.org/civilservice/jobs', 'co.essex.ny.us/personnel', 'monroecounty.gov/hr/lists', 'niagaracounty.com/employment/eligible-lists', 'ogdensburg.org/index.aspx?nid=345', 'tompkinscivilservice.org/civilservice/jobs', 'penfield.org/multirss.php', 'jobs.albanyny.gov/default/jobs', 'mycivilservice.rocklandgov.com/default/jobs', 'co.ontario.ny.us/94/Human-Resources', 'cc.cnyric.org/districtpage.cfm?pageid=112')

# Include links that include any of these
# High confidence
jobwords_certainty = ('continuous recruitment', 'employment', 'job listing', 'job opening', 'job posting', 'job announcement', 'job opportunities', 'jobs available', 'available positions', 'open positions', 'available employment', 'career opportunities', 'employment opportunities', 'current vacancies', 'current job', 'current employment', 'current opening', 'current posting', 'current opportunities', 'careers at', 'jobs at', 'jobs @', 'work at', 'employment at', 'find your career', 'browse jobs', 'search jobs', 'continuous recruitment', 'vacancy postings', 'prospective employees')

# opportunities
# Low confidence
jobwords_civ = ('open competitive', 'open-competitive', 'open to', 'job', 'job seeker', 'job title', 'civil service', 'civil service opportunities', 'civil service exam', 'civil service test', 'civil service exam announcements', 'exam', 'examination', 'exam announcement', 'examination announcement', 'test', 'positions', 'careers', 'human resource', 'personnel', 'vacancies', 'current exam', 'current civil service', 'posting', 'opening', 'vacancy')

jobwords_s = ('join', 'job seeker', 'job', 'job title', 'positions', 'careers', 'human resource', 'personnel', 'vacancies', 'posting', 'opening', 'recruitment', '>faculty<', '>staff<', '>adjunct<', '>academic<', '>support<', '>instructional<', '>administrative<', '>professional<', '>classified<', '>coaching<', 'vacancy')

# Worst offenders
#offenders = ['faculty', 'staff', 'professional', 'management', 'administrat', 'academic', 'support', 'instructional', 'adjunct', 'classified', 'teach', 'coaching']

## switching to careers solves all these
# career services, career peers, career prep, career fair, volunteer
##
# Exclude links that contain any of these
bunkwords = ('academics', 'pnwboces.org', 'recruitfront.com', 'schoolapp.wnyric.org', 'professional development', 'career development', 'javascript:', '.pdf', '.jpg', '.ico', '.rtf', '.doc', 'mailto:', 'tel:', 'icon', 'description', 'specs', 'specification', 'guide', 'faq', 'images', 'exam scores', 'resume-sample', 'resume sample', 'directory', 'pupil personnel')

# olas
# https://schoolapp.wnyric.org/ats/job_board
# recruitfront

# Multiprocessing lock for shared objects
lock = Lock()




# Define duplicate URL checking function
def dup_checker_f(dup_checker):

    # Remove scheme and unneccessary characters to prevent dups
    if '://' in dup_checker:
        dup_checker = dup_checker.split('://')[1]

    # Catch no scheme error
    else:
        with lock:
            errorurls_man_dict[dup_checker] = ['error 2: No scheme']
        return dup_checker

    # Remove www. and variants
    if dup_checker.startswith('www.'):
        dup_checker = dup_checker.split('www.')[1]
    elif dup_checker.startswith('www2.'):
        dup_checker = dup_checker.split('www2.')[1]
    elif dup_checker.startswith('www3.'):
        dup_checker = dup_checker.split('www3.')[1]

    # Remove fragments
    dup_checker = dup_checker.split('#')[0]

    ## lower?
    # Remove trailing whitespace and slash and then lowercase it
    dup_checker = dup_checker.strip().strip('/').lower()

    return dup_checker



# Define HTML request function
def html_requester(workingurl, current_crawl_level, errorurls_man_dict, all_urls_q, total_count, domain, verbose_arg, working_list):

# Request html using a spoofed user agent, cookiejar, and timeout
    try:
        cj = CookieJar()
        req = urllib.request.Request(workingurl, headers={'User-Agent': user_agent_str})
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        html = opener.open(req, timeout=10)
        return html

    ## Catch and log HTTP request errors
    except Exception as errex:

        # Retry on timeout error
        if 'timed out' in str(errex):
            if verbose_arg: print(os.getpid(), 'error 3: request timeout at', workingurl)
            with lock:
                errorurls_man_dict[workingurl] = ['error 3: ', str(errex), current_crawl_level]

            # If portal has error then use domain as fallback
            if current_crawl_level < 1:

                # Skip if url is same as the domain
                if workingurl != domain:

                    # Put fallback url into queue
                    with lock:
                        all_urls_q.put([domain, -1,  working_list[2]])

                        # Incrament queue length to use as progress report
                        total_count.value += 1

            #print('loopretry1 at:', workingurl)
            return True

        # Don't retry on 404 or 403 error
        elif 'HTTP Error 404:' in str(errex) or 'HTTP Error 403:' in str(errex):
            if verbose_arg: print(os.getpid(), 'error 4: HTTP 404/403 request at', workingurl)
            with lock:
                errorurls_man_dict[workingurl] = ['error 4: ', str(errex), current_crawl_level]
            if current_crawl_level < 1:
                if workingurl != domain:
                    with lock:
                        all_urls_q.put([domain, -1,  working_list[2]])
                        total_count.value += 1
            #print('loopfail1 at:', workingurl)
            return False

        # Retry on other error
        else:
            if verbose_arg: print(os.getpid(), 'error 5:', workingurl)
            with lock:
                errorurls_man_dict[workingurl] = ['error 5: ', str(errex), current_crawl_level]
            if current_crawl_level < 1:
                if workingurl != domain:
                    with lock:
                        all_urls_q.put([domain, -1,  working_list[2]])
                        total_count.value += 1
            #print('loopretry2 at:', workingurl)
            return True



# Define the crawling function
def scraper(keyword_list, all_urls_q, max_crawl_depth, keywordurl_man_list, checkedurls_man_list, errorurls_man_dict, skipped_pages, prog_count, total_count, all_links_arg, verbose_arg, jobwords, disagree_list, woww):
    if verbose_arg: print(os.getpid(), '\n\n =================== Start function ===================')
    while True:

        # Get a url list from the queue
        try:
            with lock:
                working_list = all_urls_q.get_nowait()

        # If queue is empty wait and try again
        except queue.Empty:
            time.sleep(2)
            try:
                with lock:
                    working_list = all_urls_q.get_nowait()

            # Exit function if queue is empty
            except queue.Empty:
                if verbose_arg: print(os.getpid(), 'Queue empty. Closing process...')
                break

        # Begin fetching
        else:
            try:

                ## fourth item somtimes jbw type
                # working_list contents: [workingurl, current_crawl_level, portal URL]
                # Seperate working list
                workingurl = working_list[0]
                current_crawl_level = working_list[1]

                # Call dup checker function
                dup_checker = dup_checker_f(workingurl)

                # Skip checked pages
                if dup_checker in checkedurls_man_list:
                    #if verbose_arg: print(os.getpid(), 'Skipping(1)', dup_checker)
                    with lock:
                        skipped_pages.value += 1
                    continue

                ## keep this part if running retry loop?
                # Add to checked pages list
                with lock:
                    checkedurls_man_list.append(dup_checker)


                ## Form domain by splitting after 3rd slash
                try:
                    domain = '/'.join(workingurl.split('/')[:3])
                except:
                    print('domain error at:', working_list)
                    continue


                ## Create domain by finding a slash after the 9th character
                domain_delim = workingurl.find('/', 9)
                if domain_delim > -1: odomain = workingurl[:domain_delim].strip()
                else: odomain = workingurl.strip()

                if odomain != domain:
                    stuff = workingurl, odomain, domain
                    disagree_list.append(stuff)


                # Retry loop for request and decode errors
                loop_success = False
                for loop_count in range(3):

                    # Get html from function
                    html = html_requester(workingurl, current_crawl_level, errorurls_man_dict, all_urls_q, total_count, domain, verbose_arg, working_list)

                    if html == True:
                        #print('cont')
                        continue
                    elif html == False:
                        #print('brea')
                        break

                    ## exclude from loop?
                    ## keep, but only add to checkedpages after loop
                    # Follow redirects
                    if html.geturl() != workingurl:
                        #print('redirect from/to', workingurl, html.geturl())

                        workingurl = html.geturl()

                        # Call dup checker function with redirected workingurl
                        dup_checker = dup_checker_f(workingurl)

                        # Skip checked pages
                        if dup_checker in checkedurls_man_list:
                            #if verbose_arg: print(os.getpid(), 'Skipping(1)', dup_checker)
                            with lock:
                                skipped_pages.value += 1
                            break

                    ## errors = ignore?
                    # Decode html using char set
                    charset_encoding = html.info().get_content_charset()
                    try:
                        if charset_encoding == None:
                            up_dec_html = html.read()
                        else:
                            up_dec_html = html.read().decode(charset_encoding)

                        # Declare successful and exit loop
                        loop_success = True
                        #print('loopsuc1 at:', workingurl)
                        break

                    ## disgusto barfo
                    # Attempt explicit gzip decompression on decode error
                    except Exception as errex:

                        if "codec can't decode byte" in str(errex):
                            #print(errex, '\nFailed to decode. Retrying with gzip at:', workingurl)

                            # Must make another request
                            html = html_requester(workingurl, current_crawl_level, errorurls_man_dict, all_urls_q, total_count, domain, verbose_arg, working_list)
                            #print('got it2', html)

                            # Retry loop on request error
                            if html == True:
                                #print('cont2')
                                continue

                            # Exit loop on fatal error
                            elif html == False:
                                #print('brea2')
                                break

                            # Retry decode with gzip
                            try:
                                html = gzip.open(html)

                                # Exit loop if decode successful
                                if charset_encoding == None:
                                    up_dec_html = html.read()
                                else:
                                    up_dec_html = html.read().decode(charset_encoding)

                                loop_success = True
                                #print('loopsuc2 at:', workingurl)
                                break

                            ## Catch other errors
                            except Exception as errex:
                                print('\nerror 6: gzip failure at:', workingurl, errex)
                                with lock:
                                    errorurls_man_dict[workingurl] = ['error 6: ', str(errex), current_crawl_level]
                                continue

                        # Retry on other decode error
                        else:
                            charset_encoding = 'FAILED'
                            print('\nerror 6: ', charset_encoding, 'decode at', workingurl, errex)
                            with lock:
                                errorurls_man_dict[workingurl] = ['error 6: ', str(errex), current_crawl_level]
                            #print('loopretry3 at:', workingurl)
                            continue


                # End of retry attempts
                else:
                    print('\nIssue: loop exhausted', workingurl)

                # Add redirected workingurl to checked pages
                if not workingurl in checkedurls_man_list:
                    with lock:
                        checkedurls_man_list.append(workingurl)


                # Skip to next URL if loop is exhausted or on fatal error
                if loop_success == False:
                    #print('loopfail2 at:', workingurl, '\n')
                    continue



                # Parse HTML with BeautifulSoup to remove hidden elements
                soup = BeautifulSoup(up_dec_html, 'html.parser')

                soup = soup.find('body')
                if soup is None:
                    print('empty soup at:', workingurl)
                    continue

                # Clear old html to free up memory
                #html = None
                #up_dec_html = None

                ## make global
                # Compile regex paterns for finding hidden HTML elements
                style_reg = re.compile("(display\s*:\s*(none|block);?|visibility\s*:\s*hidden;?)")
                class_reg = re.compile('(hidden-sections?|sw-channel-dropdown)')

                # Iterate through and remove all of the hidden style attributes
                r = soup.find_all('', {"style" : style_reg})
                for x in r:
                    #results.append(str(x)+'===================================\n\n')
                    x.decompose()

                # Type="hidden" attribute
                r = soup.find_all('', {"type" : 'hidden'})
                for x in r:
                    #results.append(str(x)+'===================================\n\n')
                    x.decompose()

                # Hidden section(s) and dropdown classes
                for i in soup(class_=class_reg):
                    #results.append(str(i)+'===================================\n\n')
                    i.decompose()

                # Use lowercase for comparisons
                lower_soup = str(soup).lower()


                # Don't search the fallback domain
                if current_crawl_level != -1:

                    # Search for keyword on page
                    if any(zzzz in lower_soup for zzzz in keyword_list):
                        if verbose_arg: print(os.getpid(), '\n~~~~~~ Keyword match at ~~~~~~', workingurl)

                        # Count jobwords on the page and attach to the match
                        jbw_count = 0
                        for i in jobwords:
                            if i in lower_soup: jbw_count += 1
                        for i in jobwords_certainty:
                            if i in lower_soup: jbw_count += 2

                        # Append URL, jobword confidence, and portal URL to result list
                        with lock:
                            keywordurl_man_list.append([workingurl, jbw_count, working_list[2]])




                # Start relavent crawler
                if current_crawl_level < max_crawl_depth:

                    # Increment crawl level
                    #if verbose_arg: print(os.getpid(), 'Starting crawler at', working_list)
                    current_crawl_level += 1

                    # Seperate html into a set of tags
                    alltags_set = set(soup.find_all('a'))
                    #alltags_set = set(alltags)

                    ## make this consideration for contents not tag
                    # Set jbws confidence based on tags
                    high_confidence = False
                    for tag in alltags_set:
                        bs_contents = str(tag.text).lower()
                        #print('bs_contents =', bs_contents, type(bs_contents))

                        if any(www in bs_contents for www in jobwords_certainty):
                            #print('found at:', bs_contents)
                            high_confidence = True
                            break


                    ## debug
                    good_tags = 0


                    # Parse tags
                    for tag in alltags_set:

                        ## Skip long tags because they are probably unusable
                        if len(tag) > 500:
                            continue

                        # Get the URL
                        bs_url = tag.get('href')

                        # Use lower tag for jbws and bunkwords only
                        lower_tag = str(tag).lower()

                        # Get the tag contents
                        bs_contents = lower_tag.text.strip()

                        # Skip if empty
                        if not bs_contents:
                            continue

                        # Add >< to help worst offenders
                        bs_contents = '>' + bs_contents
                        bs_contents = bs_contents + '<'



                        #print('\n\nbs_url =', type(bs_url), '\nbs_contents =', type(bs_contents), '\nlower_tag =', lower_tag, type(lower_tag))


                        if not all_links_arg:

                            # Proceed if the tag contents contain a high confidence jobword
                            if high_confidence:
                                if not any(xxx in bs_contents for xxx in jobwords_certainty):
                                    if verbose_arg: print(os.getpid(), 'No high job words detected at:', bs_contents[:99])
                                    continue
                                #else: print('good high at:', bs_contents)

                            # Set jbws type based on original queue put
                            else:
                                if len(working_list) == 4:
                                    if working_list[3] == 'civ': jobwords = jobwords_civ
                                    if working_list[3] == 'sch': jobwords = jobwords_s
                                    if working_list[3] == 'uni': jobwords = jobwords_s

                                # Proceed if the tag contents contain a low confidence jobword
                                if not any(yyy in bs_contents for yyy in jobwords):
                                    if verbose_arg: print(os.getpid(), 'No low job words detected at:', bs_contents[:99])
                                    continue
                                #else: print('good low at:', bs_contents)

                            ## tag or contents?
                            # Exclude if the tag contains a bunkword
                            if any(zzz in lower_tag for zzz in bunkwords):
                                if verbose_arg: print(os.getpid(), 'Bunk word detected at:', lower_tag[:99])
                                continue

                            # Check tag contents for debugging
                            #print(bs_contents)

                        # Jbw tally
                        good_tags += 1

                        for i in jobwords:
                            if i in lower_tag:
                                with lock:
                                    woww.append(i)

                        for i in jobwords_certainty:
                            if i in lower_tag:
                                with lock:
                                    woww.append(i)


                        abspath = urllib.parse.urljoin(domain, bs_url)

                        dup_checker = dup_checker_f(abspath)

                        ## test BL first
                        ##if dup_checker in checkedurls_man_list or dup_checker in blacklist:  ??
                        # Exclude checked pages
                        if dup_checker in checkedurls_man_list:
                            #if verbose_arg: print(os.getpid(), 'Skipping(2)', dup_checker)
                            with lock:
                                skipped_pages.value += 1
                            continue

                        # Exclude if the abspath is on the Blacklist
                        if dup_checker in blacklist:
                            if verbose_arg: print(os.getpid(), 'Blacklist invoked at:', dup_checker)
                            continue

                        # Create new working list and put in queue
                        new_working_list = [abspath, current_crawl_level, working_list[2]]
                        if len(working_list) == 4: new_working_list.append(working_list[3])
                        #if verbose_arg: print(os.getpid(), 'new list =', new_working_list)
                        with lock:
                            all_urls_q.put(new_working_list)
                            total_count.value += 1


            ## Catch all other errors
            except Exception as errex:
                print(os.getpid(), 'Fatal error detected. Killing process ...', str(errex)[:999], workingurl)
                with lock:
                    errorurls_man_dict[workingurl] = str(os.getpid()) + 'error 1: ', str(errex)
                break


            # Declare the task has finished
            finally:
                prog_count.value += 1





# Multiprocessing
if __name__ == '__main__':
    tmp = os.system('clear||cls')
    print('\n     ~~~  Joe\'s Jorbs  ~~~ \n  Find jobs in New York State \n')


    # ZIP codes and coordinates database
    zip_dict = {
501: (40.8153762, -73.0451085),
544: (40.8153762, -73.0451085),
6390: (41.27095945, -71.9839111362531),
10001: (40.7308619, -73.9871558),
10002: (40.7308619, -73.9871558),
10003: (40.7308619, -73.9871558),
10004: (40.7308619, -73.9871558),
10005: (40.7308619, -73.9871558),
10006: (40.7308619, -73.9871558),
10007: (40.7308619, -73.9871558),
10008: (40.7308619, -73.9871558),
10009: (40.7308619, -73.9871558),
10010: (40.7308619, -73.9871558),
10011: (40.7308619, -73.9871558),
10012: (40.7308619, -73.9871558),
10013: (40.7308619, -73.9871558),
10014: (40.7308619, -73.9871558),
10016: (40.7308619, -73.9871558),
10017: (40.7308619, -73.9871558),
10018: (40.7308619, -73.9871558),
10019: (40.7642499, -73.954525),
10020: (40.7642499, -73.954525),
10021: (40.7642499, -73.954525),
10022: (40.7642499, -73.954525),
10023: (40.7642499, -73.954525),
10024: (40.7642499, -73.954525),
10025: (40.7642499, -73.954525),
10026: (40.7642499, -73.954525),
10027: (40.7642499, -73.954525),
10028: (40.7642499, -73.954525),
10029: (40.7642499, -73.954525),
10030: (40.7642499, -73.954525),
10031: (40.7642499, -73.954525),
10032: (40.7642499, -73.954525),
10033: (40.7642499, -73.954525),
10034: (40.7642499, -73.954525),
10035: (40.7642499, -73.954525),
10036: (40.7308619, -73.9871558),
10037: (40.7642499, -73.954525),
10038: (40.7308619, -73.9871558),
10039: (40.7642499, -73.954525),
10040: (40.7642499, -73.954525),
10041: (40.7308619, -73.9871558),
10043: (40.7642499, -73.954525),
10044: (40.7642499, -73.954525),
10045: (40.7308619, -73.9871558),
10055: (40.7642499, -73.954525),
10060: (40.7642499, -73.954525),
10065: (40.7642499, -73.954525),
10069: (40.7642499, -73.954525),
10075: (40.7642499, -73.954525),
10080: (40.7642499, -73.954525),
10081: (40.7642499, -73.954525),
10087: (40.7642499, -73.954525),
10090: (40.7642499, -73.954525),
10101: (40.7308619, -73.9871558),
10102: (40.7308619, -73.9871558),
10103: (40.7642499, -73.954525),
10104: (40.7642499, -73.954525),
10105: (40.7642499, -73.954525),
10106: (40.7642499, -73.954525),
10107: (40.7642499, -73.954525),
10108: (40.7308619, -73.9871558),
10109: (40.7308619, -73.9871558),
10110: (40.7308619, -73.9871558),
10111: (40.7642499, -73.954525),
10112: (40.7642499, -73.954525),
10113: (40.7308619, -73.9871558),
10114: (40.7308619, -73.9871558),
10115: (40.7642499, -73.954525),
10116: (40.7642499, -73.954525),
10117: (40.7308619, -73.9871558),
10118: (40.7308619, -73.9871558),
10119: (40.7308619, -73.9871558),
10120: (40.7308619, -73.9871558),
10121: (40.7308619, -73.9871558),
10122: (40.7308619, -73.9871558),
10123: (40.7308619, -73.9871558),
10124: (40.7308619, -73.9871558),
10125: (40.7308619, -73.9871558),
10126: (40.7308619, -73.9871558),
10128: (40.7642499, -73.954525),
10129: (40.7642499, -73.954525),
10130: (40.7642499, -73.954525),
10131: (40.7642499, -73.954525),
10132: (40.7308619, -73.9871558),
10133: (40.7642499, -73.954525),
10138: (40.7642499, -73.954525),
10150: (40.7642499, -73.954525),
10151: (40.7642499, -73.954525),
10152: (40.7642499, -73.954525),
10153: (40.7642499, -73.954525),
10154: (40.7642499, -73.954525),
10155: (40.7587979, -73.9623427),
10156: (40.7642499, -73.954525),
10157: (40.7642499, -73.954525),
10158: (40.7308619, -73.9871558),
10159: (40.7642499, -73.954525),
10160: (40.7642499, -73.954525),
10162: (40.7642499, -73.954525),
10163: (40.7642499, -73.954525),
10164: (40.7642499, -73.954525),
10165: (40.7308619, -73.9871558),
10166: (40.7642499, -73.954525),
10167: (40.7642499, -73.954525),
10168: (40.7308619, -73.9871558),
10169: (40.7642499, -73.954525),
10170: (40.7642499, -73.954525),
10171: (40.7642499, -73.954525),
10172: (40.7642499, -73.954525),
10173: (40.7308619, -73.9871558),
10174: (40.7308619, -73.9871558),
10175: (40.7642499, -73.954525),
10176: (40.7642499, -73.954525),
10177: (40.7642499, -73.954525),
10178: (40.7308619, -73.9871558),
10179: (40.7642499, -73.954525),
10185: (40.7642499, -73.954525),
10199: (40.7308619, -73.9871558),
10203: (40.7308619, -73.9871558),
10211: (40.7308619, -73.9871558),
10212: (40.7308619, -73.9871558),
10213: (40.7308619, -73.9871558),
10242: (40.7642499, -73.954525),
10249: (40.7308619, -73.9871558),
10256: (40.7642499, -73.954525),
10258: (40.7642499, -73.954525),
10259: (40.7642499, -73.954525),
10260: (40.7308619, -73.9871558),
10261: (40.7642499, -73.954525),
10265: (40.7642499, -73.954525),
10268: (40.7642499, -73.954525),
10269: (40.7642499, -73.954525),
10270: (40.7642499, -73.954525),
10271: (40.7308619, -73.9871558),
10272: (40.7642499, -73.954525),
10273: (40.7642499, -73.954525),
10274: (40.7642499, -73.954525),
10275: (40.7308619, -73.9871558),
10276: (40.7642499, -73.954525),
10277: (40.7642499, -73.954525),
10278: (40.7308619, -73.9871558),
10279: (40.7308619, -73.9871558),
10280: (40.7308619, -73.9871558),
10281: (40.7308619, -73.9871558),
10282: (40.7308619, -73.9871558),
10285: (40.7308619, -73.9871558),
10286: (40.7642499, -73.954525),
10301: (40.5834379, -74.1495875),
10302: (40.645349, -74.0929616),
10303: (40.5834557, -74.1496048),
10304: (40.564209, -74.1253046199539),
10305: (40.564209, -74.1253046199539),
10306: (40.564209, -74.1253046199539),
10307: (40.5834557, -74.1496048),
10308: (40.564209, -74.1253046199539),
10309: (40.5834557, -74.1496048),
10310: (40.5834557, -74.1496048),
10311: (40.5834557, -74.1496048),
10312: (40.5834557, -74.1496048),
10313: (40.564209, -74.1253046199539),
10314: (40.5834557, -74.1496048),
10451: (40.85048545, -73.8404035580209),
10452: (40.85048545, -73.8404035580209),
10453: (40.85048545, -73.8404035580209),
10454: (40.85048545, -73.8404035580209),
10455: (40.85048545, -73.8404035580209),
10456: (40.85048545, -73.8404035580209),
10457: (40.85048545, -73.8404035580209),
10458: (40.85048545, -73.8404035580209),
10459: (40.85048545, -73.8404035580209),
10460: (40.85048545, -73.8404035580209),
10461: (40.85048545, -73.8404035580209),
10462: (40.85048545, -73.8404035580209),
10463: (40.85048545, -73.8404035580209),
10464: (40.85048545, -73.8404035580209),
10465: (40.85048545, -73.8404035580209),
10466: (40.85048545, -73.8404035580209),
10467: (40.85048545, -73.8404035580209),
10468: (40.85048545, -73.8404035580209),
10469: (40.85048545, -73.8404035580209),
10470: (40.85048545, -73.8404035580209),
10471: (40.85048545, -73.8404035580209),
10472: (40.85048545, -73.8404035580209),
10473: (40.85048545, -73.8404035580209),
10474: (40.85048545, -73.8404035580209),
10475: (40.85048545, -73.8404035580209),
10501: (41.2884273, -73.7662443),
10502: (41.0106531, -73.8437452),
10503: (41.0250973, -73.8704127),
10504: (41.1264849, -73.7140195),
10505: (41.3475938, -73.7620772),
10506: (41.2042741, -73.6426507),
10507: (41.1763139, -73.7907554),
10509: (41.426996, -73.760156),
10510: (41.1456512, -73.8237456),
10511: (41.2620383, -73.9381943),
10512: (41.4266361, -73.6788272),
10514: (41.1595399, -73.764855),
10516: (41.4200938, -73.9545831),
10517: (41.2950939, -73.8654141),
10518: (41.2614778, -73.5932622),
10519: (41.3482011, -73.6628544),
10520: (41.2084303, -73.8912383),
10521: (41.2084303, -73.8912383),
10522: (41.0145418, -73.872635),
10523: (41.0550969, -73.8201338),
10524: (41.3809926, -73.9473575),
10526: (41.2938384, -73.6765309),
10527: (41.3103717, -73.757355),
10528: (40.9689871, -73.71263),
10530: (41.0189863, -73.7981884),
10532: (41.1073184, -73.7959667),
10533: (41.0350625, -73.864852135741),
10535: (41.3381494, -73.7906892),
10536: (41.25877, -73.6853852),
10537: (41.3348161, -73.88097),
10538: (40.9341578, -73.7586903),
10540: (41.3228718, -73.7181869),
10541: (41.372316, -73.733465),
10542: (41.3720381, -73.7617993),
10543: (40.9539227, -73.7362872),
10545: (41.1798173, -73.8301349),
10546: (41.1923171, -73.7973562),
10547: (41.3184272, -73.8590248),
10548: (41.2523162, -73.9315275),
10549: (41.2042616, -73.7270761),
10550: (40.9125992, -73.8370786),
10551: (40.9125992, -73.8370786),
10552: (40.9125992, -73.8370786),
10553: (40.9125992, -73.8370786),
10560: (41.3348169, -73.5712374),
10562: (41.1613168, -73.8620367),
10566: (41.289811, -73.9204922),
10567: (41.282198, -73.71417),
10570: (41.1328736, -73.7926335),
10573: (41.0017643, -73.6656834),
10576: (41.2087066, -73.5748483),
10577: (41.0409305, -73.7145746),
10578: (41.3259276, -73.6551292),
10579: (41.3359272, -73.8740252),
10580: (40.9808209, -73.684294),
10583: (40.990605, -73.8082739),
10587: (41.3317606, -73.7381876),
10588: (41.321675, -73.8296366962619),
10589: (41.3281498, -73.6856857),
10590: (41.2723173, -73.5529034),
10591: (41.0762077, -73.8587461),
10594: (41.1234293, -73.7790218),
10595: (41.0748189, -73.7751326),
10596: (41.2528717, -73.9598618),
10597: (41.300315, -73.5761584),
10598: (41.2709274, -73.7776336),
10601: (41.0339862, -73.7629097),
10602: (41.0339862, -73.7629097),
10603: (41.0339862, -73.7629097),
10604: (40.9689871, -73.71263),
10605: (41.0339862, -73.7629097),
10606: (41.0339862, -73.7629097),
10607: (41.0339862, -73.7629097),
10610: (41.0339862, -73.7629097),
10701: (40.9312099, -73.8987469),
10702: (40.9312099, -73.8987469),
10703: (40.9312099, -73.8987469),
10704: (40.9312099, -73.8987469),
10705: (40.9312099, -73.8987469),
10706: (40.9946622, -73.8785922),
10707: (40.9503764, -73.827356),
10708: (40.9381544, -73.8320784),
10709: (40.9610563, -73.8064739),
10710: (40.9312099, -73.8987469),
10801: (40.9114459, -73.7841684271834),
10802: (40.9115386, -73.7826363),
10803: (40.9098215, -73.8079111),
10804: (40.9115386, -73.7826363),
10805: (40.9115386, -73.7826363),
10901: (41.1151372, -74.1493948),
10910: (41.2745381, -74.1529235),
10911: (41.3128717, -74.0062519),
10912: (41.2503717, -74.3107068),
10913: (41.0634299, -73.9576378),
10914: (41.4092605, -74.1951475),
10915: (41.5428194, -74.3608495),
10916: (41.4506509, -74.2658934),
10917: (41.3317605, -74.120978),
10918: (41.3625937, -74.2712613),
10919: (41.5142604, -74.3834883),
10920: (41.150651, -73.9454159),
10921: (41.3317607, -74.35682),
10922: (41.34108425, -73.9954204997347),
10923: (41.2017613, -73.9943068),
10924: (41.4020382, -74.3243191),
10925: (41.2225932, -74.2943178),
10926: (41.308427, -74.1445899),
10927: (41.1976502, -73.9640541),
10928: (41.3692605, -73.9662504),
10930: (41.3470382, -74.126256),
10931: (41.1239845, -74.1693119),
10932: (41.4795381, -74.4651581),
10933: (41.3662053, -74.5065481),
10940: (41.44591415, -74.4224417389405),
10941: (41.44591415, -74.4224417389405),
10949: (40.71134085, -73.6228066),
10950: (41.3304767, -74.1866348),
10952: (41.1112069, -74.0684751),
10953: (41.4009271, -74.0784765),
10954: (41.0887073, -74.013473),
10956: (41.1469917, -73.9902998),
10958: (41.4109272, -74.4071001),
10959: (41.234539, -74.4137664),
10960: (41.444492, -74.00562),
10960: (41.0906519, -73.9179146),
10962: (41.0465776, -73.9496707),
10963: (41.4734268, -74.5384933),
10964: (41.0111793, -73.91346),
10965: (41.0586333, -74.0218967),
10968: (41.04152295, -73.9183875),
10969: (41.2978079, -74.461481),
10970: (41.1670394, -74.043197),
10973: (41.3909274, -74.4765471),
10974: (41.1545395, -74.192924),
10975: (41.2448159, -74.1754241),
10976: (41.0289025, -73.9326580670926),
10977: (41.1130231, -74.0437839),
10979: (41.1825949, -74.3187622),
10980: (41.2295386, -73.9870847),
10981: (41.3209271, -74.2854283),
10982: (41.1112069, -74.099865),
10983: (41.0225273, -73.9486643),
10984: (41.2108695, -74.0182453),
10985: (41.5681493, -74.329875),
10986: (41.2570383, -73.9834736),
10987: (41.1934278, -74.1843129),
10988: (41.302039, -74.5615492),
10989: (41.1181514, -73.9554159),
10990: (41.256483, -74.3598755),
10992: (41.4278716, -74.1659798),
10993: (41.2095941, -73.9852994),
10994: (41.096485, -73.9729162),
10996: (43.806032, -73.437876),
10997: (43.806032, -73.437876),
10998: (41.3367611, -74.5398821),
11001: (40.724269, -73.7151313),
11001: (40.714269, -73.7001309),
11001: (40.72473015, -73.706479773572),
11002: (40.7246999, -73.7048024),
11003: (40.700936, -73.712909),
11004: (40.7470463, -73.7115199),
11005: (40.7246999, -73.7048024),
11010: (40.7073244, -73.6759635),
11020: (40.8006567, -73.7284647),
11021: (40.8006567, -73.7284647),
11022: (40.8006567, -73.7284647),
11023: (40.8006567, -73.7284647),
11024: (40.7870327, -73.7267563),
11026: (40.8006567, -73.7284647),
11027: (40.8006567, -73.7284647),
11030: (40.7978787, -73.6995749),
11040: (40.73071865, -73.6812564655372),
11042: (40.7352157, -73.6883239),
11050: (40.8256561, -73.6981858),
11051: (40.8256561, -73.6981858),
11052: (40.8256561, -73.6981858),
11053: (40.8256561, -73.6981858),
11054: (40.8256561, -73.6981858),
11055: (40.8256561, -73.6981858),
11096: (40.61215055, -73.7443639351021),
11101: (40.7415369, -73.9571249),
11102: (40.7720145, -73.9302673),
11103: (40.7720145, -73.9302673),
11104: (40.7398242, -73.9354153),
11105: (40.7720145, -73.9302673),
11106: (40.7720145, -73.9302673),
11109: (40.7415369, -73.9571249),
11120: (40.7455316, -73.9484995),
11201: (40.64530975, -73.9550230275334),
11202: (40.64530975, -73.9550230275334),
11203: (40.64530975, -73.9550230275334),
11204: (40.64530975, -73.9550230275334),
11205: (40.64530975, -73.9550230275334),
11206: (40.64530975, -73.9550230275334),
11207: (40.64530975, -73.9550230275334),
11208: (40.64530975, -73.9550230275334),
11209: (40.64530975, -73.9550230275334),
11210: (40.64530975, -73.9550230275334),
11211: (40.64530975, -73.9550230275334),
11212: (40.64530975, -73.9550230275334),
11213: (40.64530975, -73.9550230275334),
11214: (40.64530975, -73.9550230275334),
11215: (40.64530975, -73.9550230275334),
11216: (40.64530975, -73.9550230275334),
11217: (40.64530975, -73.9550230275334),
11218: (40.64530975, -73.9550230275334),
11219: (40.64530975, -73.9550230275334),
11220: (40.64530975, -73.9550230275334),
11221: (40.64530975, -73.9550230275334),
11222: (40.64530975, -73.9550230275334),
11223: (40.64530975, -73.9550230275334),
11224: (40.64530975, -73.9550230275334),
11225: (40.64530975, -73.9550230275334),
11226: (40.6501038, -73.9495823),
11228: (40.64530975, -73.9550230275334),
11229: (40.64530975, -73.9550230275334),
11230: (40.64530975, -73.9550230275334),
11231: (40.64530975, -73.9550230275334),
11232: (40.64530975, -73.9550230275334),
11233: (40.64530975, -73.9550230275334),
11234: (40.64530975, -73.9550230275334),
11235: (40.64530975, -73.9550230275334),
11236: (40.64530975, -73.9550230275334),
11237: (40.64530975, -73.9550230275334),
11238: (40.64530975, -73.9550230275334),
11239: (40.64530975, -73.9550230275334),
11241: (40.64530975, -73.9550230275334),
11242: (40.64530975, -73.9550230275334),
11243: (40.64530975, -73.9550230275334),
11245: (40.64530975, -73.9550230275334),
11247: (40.64530975, -73.9550230275334),
11249: (40.64530975, -73.9550230275334),
11251: (40.64530975, -73.9550230275334),
11252: (40.64530975, -73.9550230275334),
11256: (40.64530975, -73.9550230275334),
11351: (40.958754, -72.964712),
11352: (40.698188, -73.961899),
11354: (40.76494565, -73.8265816714178),
11355: (40.7532086, -73.8216745),
11356: (40.7876014, -73.8459682),
11357: (40.7945457, -73.8184674),
11358: (40.7546933, -73.8024122656064),
11359: (40.7684351, -73.7770774),
11360: (40.7684351, -73.7770774),
11361: (40.7684351, -73.7770774),
11362: (40.7620463, -73.7381874),
11363: (40.7745338, -73.7412564),
11364: (40.753991, -73.765966),
11365: (40.7348246, -73.7934668),
11366: (40.73613835, -73.7800816557486),
11367: (40.7372221, -73.8136111),
11368: (40.7469593, -73.8601456),
11369: (40.7612123, -73.8651358),
11370: (40.7612123, -73.8651358),
11371: (40.7658119, -73.8639854),
11372: (40.7556561, -73.8857755),
11373: (40.7365804, -73.8783932),
11374: (40.72293705, -73.8622065151304),
11375: (43.1037625, -77.4841397804973),
11377: (40.7461604, -73.9032853),
11378: (40.723158, -73.912637),
11379: (40.7182153, -73.8786698186696),
11380: (40.7365804, -73.8783932),
11381: (40.958754, -72.964712),
11385: (40.7080556, -73.9141667),
11386: (43.2503348, -78.6472536),
11405: (40.6914852, -73.8056771),
11411: (40.6945474, -73.7384653),
11412: (40.6984364, -73.7606881),
11413: (40.678159, -73.746521),
11414: (40.6578815, -73.8362459),
11415: (40.7139415, -73.830742),
11416: (40.67677, -73.8437461),
11417: (40.67677, -73.8437461),
11418: (40.6994253, -73.8309672),
11419: (40.6994253, -73.8309672),
11420: (40.6701035, -73.8190231),
11421: (40.6892698, -73.8579131),
11422: (40.6620479, -73.7354097),
11423: (40.7134361, -73.7670772),
11424: (40.6914852, -73.8056771),
11425: (40.6914852, -73.8056771),
11426: (40.724269, -73.7151313),
11427: (40.7267692, -73.7415208),
11428: (40.7267692, -73.7415208),
11429: (40.7170975, -73.7375862),
11430: (40.6914852, -73.8056771),
11431: (40.6914852, -73.8056771),
11432: (40.69983135, -73.8077028537026),
11433: (40.6914852, -73.8056771),
11434: (40.6914852, -73.8056771),
11435: (40.6914852, -73.8056771),
11436: (40.6914852, -73.8056771),
11439: (40.69983135, -73.8077028537026),
11451: (40.69983135, -73.8077028537026),
11499: (40.6914852, -73.8056771),
11501: (40.7492678, -73.6406845),
11507: (40.7734341, -73.6431844),
11509: (40.5889936, -73.7290207),
11510: (40.6564913, -73.6092953),
11514: (40.7526008, -73.6104058),
11516: (40.6226058, -73.7256873),
11518: (40.6420477, -73.6695747),
11520: (40.6576022, -73.5831835),
11530: (40.72319685, -73.6403872966069),
11531: (40.7266477, -73.6343052),
11542: (40.862755, -73.6336094),
11545: (40.8353776, -73.6237388),
11547: (40.8306556, -73.6387393),
11548: (40.8106558, -73.6284614),
11549: (40.7063185, -73.618684),
11550: (40.7063185, -73.618684),
11551: (40.7063185, -73.618684),
11552: (40.7048242, -73.6501295),
11553: (40.7003793, -73.5929056),
11554: (40.7139898, -73.5590157),
11555: (40.7003793, -73.5929056),
11556: (40.7003793, -73.5929056),
11557: (40.6431591, -73.6956865),
11558: (40.6042705, -73.6554078),
11559: (40.6156599, -73.7295763),
11560: (40.8745314, -73.5981168),
11561: (40.58888905, -73.6648751135986),
11563: (40.6559054, -73.6752222),
11565: (40.67555035, -73.6686786894678),
11566: (40.6628796, -73.551516),
11568: (40.7887113, -73.5995717),
11569: (40.5923255, -73.580684),
11570: (40.6574186, -73.6450664),
11571: (40.6574186, -73.6450664),
11572: (40.6387141, -73.6401296),
11575: (40.678713, -73.5890168),
11576: (40.7998227, -73.6509621),
11577: (40.7887117, -73.6473511),
11579: (40.8489887, -73.6448505),
11580: (40.6631362, -73.7056955),
11581: (40.6614765, -73.7045922),
11582: (40.6631362, -73.7056955),
11590: (40.7534275, -73.5858684),
11596: (40.75649, -73.6448513),
11598: (40.63155395, -73.7132226),
11599: (40.7266477, -73.6343052),
11690: (40.609039, -73.7506461),
11691: (40.6053825, -73.7551326),
11692: (40.5934173, -73.7895462),
11693: (40.6053825, -73.7551326),
11694: (40.5805104, -73.8361535),
11695: (40.609039, -73.7506461),
11697: (40.5562395, -73.9267179035117),
11701: (40.6789893, -73.4170673),
11702: (40.6956552, -73.3256753),
11703: (40.7164881, -73.3217861),
11704: (40.718155, -73.3542871),
11705: (40.7384317, -73.0506656),
11706: (40.72508825, -73.253032759713),
11707: (40.718155, -73.3542871),
11709: (40.9106541, -73.5620689),
11710: (40.6540805, -73.5285878127105),
11713: (40.77370975, -72.94376015),
11714: (40.74336, -73.4838031),
11715: (40.7439872, -73.0345539),
11716: (40.7694091, -73.1148664),
11717: (40.78115805, -73.2425282958642),
11718: (40.7209321, -73.2673399),
11719: (40.7792653, -72.9153827),
11720: (40.8584316, -73.0995539),
11721: (40.89782185, -73.3717214029655),
11722: (40.7906538, -73.2017811),
11724: (40.8714873, -73.456788),
11725: (40.8428759, -73.2928943),
11726: (40.6731835, -73.394809575505),
11727: (40.8687097, -73.0014946),
11729: (40.7617653, -73.3292858),
11730: (40.7320429, -73.1856703),
11731: (40.8767648, -73.3245614),
11732: (40.8467657, -73.5351245),
11733: (40.9418427, -73.1058559),
11735: (40.73567545, -73.441758295828),
11737: (40.73567545, -73.441758295828),
11738: (40.8312096, -73.029552),
11739: (40.7212097, -73.1576139),
11740: (40.8686822, -73.362712),
11741: (40.8123205, -73.078443),
11742: (40.8153762, -73.0451085),
11743: (40.868154, -73.425676),
11746: (40.8534318, -73.4115091),
11747: (40.7934322, -73.4151214),
11749: (40.8042649, -73.1690019),
11751: (40.7359239, -73.2091231),
11752: (40.7504303, -73.1857520086702),
11753: (40.7920441, -73.5398476),
11754: (40.88373, -73.2544898),
11755: (40.8528761, -73.1151102),
11756: (40.7259336, -73.5142921),
11757: (40.6867667, -73.3734547),
11758: (40.6806564, -73.4742914),
11760: (40.7934322, -73.4151214),
11762: (40.6803785, -73.4551241),
11763: (40.81730195, -72.9993051867247),
11764: (40.9598212, -72.9962148),
11765: (40.8870431, -73.5551246),
11766: (40.9470432, -73.0295495),
11767: (40.8520426, -73.1540004),
11768: (40.9038855, -73.3419913726415),
11769: (40.7439872, -73.1387242),
11770: (40.6467664, -73.1570589),
11771: (40.865819, -73.5320304),
11772: (40.7656539, -73.0151084),
11773: (40.7934322, -73.4151214),
11775: (40.7934322, -73.4151214),
11776: (40.9253764, -73.0473284),
11777: (40.9464875, -73.0692732),
11778: (40.9525987, -72.9253805),
11779: (40.8153761, -73.112333),
11780: (40.8824834, -73.1590454),
11782: (40.7403343, -73.0858595),
11783: (40.6659344, -73.4881809),
11784: (40.8664874, -73.0356625),
11786: (40.9573208, -72.9076025),
11787: (40.8559314, -73.2006687),
11788: (40.8256537, -73.2026138),
11789: (40.9562099, -72.9678811),
11790: (40.9256538, -73.140943),
11791: (40.8262101, -73.502068),
11792: (40.9503762, -72.8426016),
11793: (40.6837121, -73.5101258),
11794: (40.9256538, -73.140943),
11795: (40.7058564, -73.3077301),
11796: (40.7278763, -73.0976118),
11797: (40.8256545, -73.4676225),
11798: (40.7539878, -73.360398),
11801: (40.7668163, -73.5297439785641),
11802: (40.7668163, -73.5297439785641),
11803: (40.7764882, -73.4673455),
11804: (40.7647119, -73.4622586515897),
11815: (40.7684331, -73.5251253),
11853: (40.7920441, -73.5398476),
11901: (40.9170435, -72.6620402),
11930: (40.9844862, -72.1322676993658),
11931: (40.9445438, -72.6270382),
11932: (40.9378777, -72.3009158),
11933: (40.9064873, -72.7434331),
11934: (40.8002427, -72.7901318),
11935: (41.0106563, -72.4850859),
11937: (40.9649335, -72.1935296987861),
11939: (41.1275989, -72.3400829),
11940: (40.8050989, -72.7609336),
11941: (40.8441033, -72.7200324802622),
11942: (40.8406554, -72.5814814),
11944: (41.09971395, -72.3631363923228),
11946: (40.8689892, -72.5175893),
11947: (40.9495443, -72.5814801),
11948: (40.9695445, -72.5620344),
11949: (40.8737096, -72.8078791),
11950: (40.8020431, -72.8409359),
11951: (40.7667655, -72.8520476),
11952: (40.9916223, -72.5361533),
11953: (40.8842653, -72.9373262),
11954: (41.0482141, -71.9532344633105),
11955: (40.807321, -72.8212131),
11956: (40.9914896, -72.475919),
11957: (41.1389875, -72.303415),
11958: (41.0478783, -72.4631412),
11959: (40.823177, -72.6096451),
11960: (40.8076955, -72.7088261),
11961: (40.8939875, -72.8959364),
11962: (40.9253776, -72.2781375),
11963: (40.9978727, -72.2922292),
11964: (41.0645437, -72.3328604),
11965: (41.074356, -72.3605399027343),
11967: (40.8014876, -72.8676033),
11968: (40.884267, -72.3895296),
11969: (40.884267, -72.3895296),
11970: (40.9364888, -72.5773135),
11971: (41.0652287, -72.4263169),
11972: (40.8193623, -72.7052544),
11973: (40.869543, -72.8867697),
11975: (40.9367664, -72.2428587),
11976: (40.9059335, -72.3620287),
11977: (40.83031155, -72.6625742249036),
11978: (40.8102203, -72.6430174),
11980: (40.8367653, -72.9170487),
12007: (42.4686918, -73.9256839),
12008: (42.8553542, -73.8990122),
12009: (42.7006324, -74.0337382),
12010: (42.943367, -74.1850436),
12015: (42.2603648, -73.8095707),
12016: (42.9295183, -74.3165222),
12017: (42.3117536, -73.4731684),
12018: (42.6343578, -73.5537673),
12019: (42.9117428, -73.8681782),
12020: (43.0009087, -73.8490111),
12022: (42.6931351, -73.3720549),
12023: (42.6253546, -74.1334647),
12024: (42.4959149, -73.5120564),
12025: (43.0586846, -74.1965206),
12027: (42.9097982, -73.8951234),
12028: (42.9536888, -73.4342797),
12029: (42.4118426, -73.4496088),
12031: (42.7570191, -74.4456909),
12032: (43.137849, -74.4812516),
12033: (42.5308134, -73.7553018),
12035: (42.7111862, -74.3387443),
12036: (42.5453541, -74.664594),
12037: (42.3642517, -73.5948391),
12040: (42.625928, -73.361092),
12041: (42.5759119, -73.9640169),
12042: (42.3659174, -73.85096),
12043: (42.677853, -74.4854172),
12045: (42.4739705, -73.7923456),
12046: (42.4717475, -73.8945716),
12047: (42.7742446, -73.7001187),
12050: (42.3184188, -73.7531791),
12051: (42.3509179, -73.8029028),
12052: (42.7489669, -73.5573377),
12053: (42.7453532, -74.1881834),
12054: (42.6220235, -73.8326232),
12055: (42.4995235, -73.9945751),
12056: (42.76202, -74.1337383),
12057: (42.9500778, -73.3962234),
12058: (42.3556399, -73.9006841),
12059: (42.6164662, -74.0745747),
12060: (42.4106396, -73.5245579),
12061: (42.5909135, -73.7017858),
12062: (42.5078592, -73.5065006),
12063: (42.562025, -73.6334502),
12064: (42.6234089, -74.6715361),
12065: (42.8656325, -73.7709535),
12066: (42.761186, -74.2565176),
12067: (42.5778571, -73.8787363),
12068: (42.9545179, -74.3765241),
12069: (42.9422962, -74.2851327),
12070: (42.9572054, -74.2406014954484),
12071: (42.5684093, -74.3954187),
12072: (42.9478514, -74.3704128),
12073: (42.6625757, -74.2326321),
12074: (43.0186858, -74.0315162),
12075: (42.3292525, -73.6156736),
12076: (42.3973028, -74.4459805),
12077: (42.604802, -73.7695658),
12078: (43.0528133, -74.34369),
12082: (42.768967, -73.4509464),
12083: (42.4153596, -74.0220769),
12084: (42.704522, -73.911513),
12085: (42.7020217, -73.9662368),
12086: (42.9745189, -74.1509633),
12087: (42.4289715, -73.8092911),
12089: (42.8625783, -73.3281661),
12090: (42.9011892, -73.3515001),
12092: (42.6900752, -74.3829133),
12093: (42.4811884, -74.6104276),
12094: (42.9145219, -73.5137258),
12095: (43.0068689, -74.3676437),
12106: (42.3953617, -73.6978983),
12107: (42.6711876, -74.115685),
12108: (43.47111, -74.412804),
12110: (42.7442986, -73.7614799),
12115: (42.4706378, -73.5828928),
12116: (42.5364661, -74.8865453),
12117: (43.104743, -74.265175),
12118: (42.9028547, -73.6873405),
12120: (42.4367469, -74.1301365),
12121: (42.8420219, -73.622617),
12122: (42.598687, -74.3329156),
12123: (42.5159145, -73.6101159),
12124: (42.4461934, -73.7884568),
12125: (42.4639722, -73.3964977),
12128: (42.7245228, -73.7584535),
12130: (42.4409161, -73.6609519),
12131: (42.4709109, -74.4454234),
12132: (42.4720265, -73.6317837),
12133: (42.9281336, -73.3428888),
12134: (43.226193, -74.172478),
12136: (42.4406387, -73.5617812),
12137: (42.8900753, -74.0815164),
12138: (42.7495232, -73.3401106),
12139: (43.4484024, -74.518484),
12140: (42.6903566, -73.5645597),
12141: (43.3950404, -73.2643558),
12143: (42.4684148, -73.8162354),
12144: (42.7091389, -73.5107732),
12147: (42.5161888, -74.1379131),
12148: (42.8531321, -73.8879008),
12149: (42.6342422, -74.5640324),
12150: (42.8743319, -74.0465958),
12151: (42.9386872, -73.7898429),
12153: (43.3434899, -74.0697626711536),
12154: (42.9000773, -73.5853939),
12155: (42.5489657, -74.8209875),
12156: (42.479526, -73.7695669),
12157: (42.5757217, -74.4390277),
12158: (42.5323027, -73.7984563),
12159: (42.6292455, -73.8645685),
12160: (42.7570192, -74.330409),
12161: (42.5317467, -73.847347),
12164: (43.497515, -74.361992),
12165: (42.3234196, -73.5459487),
12166: (42.8914624, -74.5134719),
12167: (42.4073024, -74.614318),
12168: (42.5486929, -73.3739973),
12169: (42.5486929, -73.3739973),
12170: (42.9384101, -73.6531731),
12172: (42.2861974, -73.7387345),
12173: (42.3903615, -73.7815127),
12174: (42.3553625, -73.7309556),
12175: (42.5795203, -74.5882017),
12176: (42.392583, -73.9498522),
12177: (42.9553517, -74.2851329),
12180: (42.7284117, -73.6917878),
12181: (42.7284117, -73.6917878),
12182: (42.7284117, -73.6917878),
12183: (42.7284117, -73.6917878),
12184: (42.4134168, -73.6731749),
12185: (42.9034107, -73.5626157),
12186: (42.653967, -73.9287366),
12187: (42.6603531, -74.507363),
12188: (42.7925778, -73.6812293),
12189: (42.7282483, -73.7014649039252),
12190: (43.396067, -74.289894),
12192: (42.3606399, -73.8167921),
12193: (42.5150785, -74.0454099),
12194: (42.5645204, -74.4637542),
12195: (42.4861933, -73.4662217),
12196: (42.640464, -73.6052888476406),
12197: (42.5914958, -74.7503896),
12198: (42.6967455, -73.644284),
12201: (42.6511674, -73.754968),
12202: (42.6511674, -73.754968),
12203: (42.6511674, -73.754968),
12204: (42.6511674, -73.754968),
12205: (42.6511674, -73.754968),
12206: (42.6511674, -73.754968),
12207: (42.6511674, -73.754968),
12208: (42.6511674, -73.754968),
12209: (42.6511674, -73.754968),
12210: (42.6511674, -73.754968),
12211: (42.6511674, -73.754968),
12212: (42.5986896, -73.9843997),
12214: (42.6511674, -73.754968),
12220: (42.6511674, -73.754968),
12222: (42.6511674, -73.754968),
12223: (42.6511674, -73.754968),
12224: (42.6511674, -73.754968),
12225: (42.6511674, -73.754968),
12226: (42.6511674, -73.754968),
12227: (42.6511674, -73.754968),
12228: (42.6511674, -73.754968),
12229: (42.6511674, -73.754968),
12230: (42.6511674, -73.754968),
12231: (42.6511674, -73.754968),
12232: (42.6511674, -73.754968),
12233: (42.6511674, -73.754968),
12234: (42.6511674, -73.754968),
12235: (42.5986896, -73.9843997),
12236: (42.6511674, -73.754968),
12237: (42.6511674, -73.754968),
12238: (42.6511674, -73.754968),
12239: (42.6511674, -73.754968),
12240: (42.6511674, -73.754968),
12241: (42.6511674, -73.754968),
12242: (42.6511674, -73.754968),
12243: (42.6511674, -73.754968),
12244: (42.6511674, -73.754968),
12245: (42.6511674, -73.754968),
12246: (42.6511674, -73.754968),
12247: (42.5986896, -73.9843997),
12248: (42.6511674, -73.754968),
12249: (42.6511674, -73.754968),
12250: (42.5986896, -73.9843997),
12255: (42.6511674, -73.754968),
12257: (42.6511674, -73.754968),
12260: (42.6511674, -73.754968),
12261: (42.6511674, -73.754968),
12288: (42.6511674, -73.754968),
12301: (42.8142432, -73.9395687),
12302: (42.8142432, -73.9395687),
12303: (42.8142432, -73.9395687),
12304: (42.8142432, -73.9395687),
12305: (42.8142432, -73.9395687),
12306: (42.8142432, -73.9395687),
12307: (42.8142432, -73.9395687),
12308: (42.8142432, -73.9395687),
12309: (42.8142432, -73.9395687),
12325: (42.8142432, -73.9395687),
12345: (42.8142432, -73.9395687),
12401: (41.9287812, -74.0023702),
12402: (41.9287812, -74.0023702),
12404: (41.7856489, -74.2290366),
12405: (42.3109186, -74.0554126),
12406: (42.1478659, -74.6198771),
12407: (42.3036956, -74.3334789),
12409: (42.040647, -74.1551429),
12410: (42.10259, -74.4437624),
12411: (41.8789815, -74.0440293),
12412: (42.0050923, -74.2659804),
12413: (42.2989749, -73.9984659),
12414: (42.2173102, -73.8645734),
12416: (42.1017567, -74.3093139),
12417: (41.9100924, -73.9912495),
12418: (42.3681382, -74.1581939),
12419: (41.853392, -74.106082),
12420: (41.6734269, -74.3854321),
12421: (42.2125871, -74.5693201),
12422: (42.3995257, -74.1723608),
12423: (42.3725828, -74.0956914),
12424: (42.2350874, -74.1454173),
12427: (42.1592556, -74.1573634),
12428: (41.7170379, -74.39571),
12429: (41.8278707, -73.9651379),
12430: (42.1553663, -74.5323753),
12431: (42.3592503, -74.0498564),
12432: (42.0437023, -73.9473576),
12433: (42.0025921, -74.1262536),
12434: (42.3578599, -74.508483),
12435: (41.7259269, -74.4857134),
12436: (42.1959216, -74.0970826),
12438: (42.2084203, -74.6009875),
12439: (42.2898074, -74.2165307),
12440: (41.8267597, -74.1262549),
12441: (42.1442557, -74.4898745),
12442: (42.2136987, -74.2187541),
12443: (41.9274787, -74.0679984),
12444: (42.2703636, -74.3029229),
12446: (41.7748155, -74.2982059),
12448: (42.0673131, -74.1870881),
12449: (41.9856476, -73.9881934),
12450: (42.1278673, -74.2629234),
12451: (42.2553651, -73.9023518),
12452: (42.2403646, -74.3654253),
12453: (42.095368, -73.9340227),
12454: (42.2759192, -74.1868074),
12455: (42.148699, -74.648211),
12456: (42.0614798, -73.9937478),
12457: (42.0448136, -74.2754247),
12458: (41.7439824, -74.3715423),
12459: (42.2136977, -74.6821003),
12460: (42.4098033, -74.1523599),
12461: (41.9278705, -74.2154239),
12463: (42.1745334, -74.0201355),
12464: (42.0848126, -74.3154254),
12465: (42.1334121, -74.479341),
12466: (41.9053703, -73.976249),
12468: (42.3148062, -74.4329261),
12469: (42.4445237, -74.207917),
12470: (42.2842532, -74.0054108),
12471: (41.8375928, -74.0373627),
12472: (41.8439818, -74.0820865),
12473: (42.2689759, -74.0273563),
12474: (42.2839739, -74.5648747),
12475: (42.0181472, -74.0148606),
12477: (42.0775906, -73.9529126),
12480: (42.1200896, -74.3954274),
12481: (41.9734258, -74.2120901),
12482: (42.2770311, -73.9567979),
12483: (41.6656492, -74.4298783),
12484: (41.8531485, -74.1390329),
12485: (42.1956438, -74.1337508),
12486: (41.8289818, -74.068475),
12487: (41.855926, -73.9770826),
12489: (41.7589823, -74.357375),
12490: (42.1231454, -73.9348556),
12491: (41.9973144, -74.104864),
12492: (42.1977908, -74.3479506),
12493: (41.7945375, -73.9595823),
12494: (41.9673148, -74.2870925),
12495: (42.0764796, -74.2279228),
12496: (42.3073066, -74.2520875),
12498: (42.041003, -74.118329),
12501: (41.8492599, -73.5567919),
12502: (42.0506467, -73.6362361),
12503: (42.0181473, -73.5912358),
12504: (42.0128695, -73.9081901),
12506: (41.8756486, -73.6912393),
12507: (41.9984252, -73.9240242),
12508: (41.504879, -73.9696822),
12510: (41.6712049, -73.7631865),
12511: (41.7027228, -74.2736319),
12512: (40.7464906, -74.0015283),
12513: (42.2250876, -73.7345686),
12514: (41.8300933, -73.7623524),
12515: (41.6948156, -74.0512528),
12516: (42.1035545, -73.5496591),
12517: (42.1203043, -73.5239582),
12518: (40.7910799, -73.9748635),
12520: (41.444816, -74.0156961),
12521: (42.1748115, -73.5828976),
12522: (41.7412051, -73.5765151),
12523: (42.0509242, -73.7937408),
12524: (41.5355745, -73.898702),
12525: (41.6798157, -74.1504231),
12526: (42.1345339, -73.8917982),
12527: (41.5217603, -73.9265262),
12528: (41.7209267, -73.9601382),
12529: (42.1789784, -73.5259511),
12530: (42.205366, -73.6912341),
12531: (41.5234269, -73.646795),
12533: (41.5839824, -73.8087442),
12534: (42.2528649, -73.790959),
12537: (41.5809269, -73.9270817),
12538: (41.7847232, -73.9332461),
12540: (41.6541106, -73.6667779),
12541: (42.1420336, -73.777905),
12542: (41.6056492, -73.9715276),
12543: (41.4839827, -74.2176487),
12544: (42.2531431, -73.667621),
12545: (41.7865038, -73.6921867),
12546: (41.9537035, -73.5106791),
12547: (41.6598157, -73.9570826),
12548: (41.6684268, -74.1026437),
12549: (41.5275938, -74.236816),
12550: (41.5034271, -74.0104179),
12551: (41.5034271, -74.0104179),
12552: (41.5034271, -74.0104179),
12553: (41.4767605, -74.0237519),
12555: (41.5034271, -74.0104179),
12561: (41.7464972, -74.0844894),
12563: (41.5117316, -73.604253),
12564: (41.5620381, -73.6026271),
12565: (42.248421, -73.653176),
12566: (41.6081492, -74.2990402),
12567: (41.9798143, -73.6559602),
12568: (41.6173567, -74.0761622),
12569: (41.7445382, -73.8212439),
12570: (41.6089826, -73.6817957),
12571: (41.9950819, -73.8755918),
12572: (41.9268754, -73.9126639),
12574: (41.9195124, -73.9512441),
12575: (41.4662049, -74.1912587),
12577: (41.4306494, -74.1190335),
12578: (41.8067601, -73.7931869),
12580: (41.8498151, -73.9301365),
12581: (41.8673152, -73.7142954),
12582: (41.5703713, -73.7454088),
12583: (42.058528, -73.908913),
12584: (41.4542605, -74.0576423),
12585: (41.7287051, -73.710407),
12586: (41.5612048, -74.1884806),
12588: (41.6337047, -74.377932),
12589: (41.6056492, -74.1840358),
12590: (41.5965635, -73.9112103),
12592: (41.8039825, -73.5587368),
12594: (41.6470383, -73.5681816),
12601: (41.7065779, -73.9284101),
12602: (41.7065779, -73.9284101),
12603: (41.7065779, -73.9284101),
12604: (41.7065779, -73.9284101),
12701: (41.6556465, -74.6893282),
12719: (41.4775904, -74.911),
12720: (41.6834224, -74.8712753),
12721: (41.5542603, -74.4396014),
12722: (41.5900936, -74.382099),
12723: (41.7673105, -75.0562785),
12724: (41.8367551, -74.946553),
12725: (41.918425, -74.5723786),
12726: (41.7059217, -75.0604458),
12727: (41.7059217, -75.0604458),
12729: (41.4673154, -74.5937719),
12732: (41.5270346, -74.8840544),
12733: (41.7320362, -74.6012711),
12734: (41.7739781, -74.7384949),
12736: (41.8423103, -75.0429442),
12737: (41.4787025, -74.8134978),
12738: (41.6539812, -74.5868267),
12740: (41.8478701, -74.547935),
12741: (41.8142548, -75.0868347),
12742: (41.7142564, -74.726273),
12743: (41.5234238, -74.8512761),
12745: (41.764255, -75.0301665),
12746: (41.4178712, -74.6309949),
12747: (41.735646, -74.6743277),
12748: (41.7809217, -74.9337755),
12749: (41.6912003, -74.8357192),
12750: (41.7334218, -74.9496094),
12751: (41.6831467, -74.6607165),
12752: (41.6842552, -74.9926661),
12754: (41.8012002, -74.7465527),
12758: (41.9003667, -74.8282167),
12759: (41.77415415, -74.6566052645852),
12760: (41.8509212, -75.1335027),
12762: (41.6687008, -74.7846074),
12763: (41.6895375, -74.5312702),
12764: (41.6084397, -75.0604273),
12765: (41.8473134, -74.6190472),
12766: (41.8067549, -74.9915539),
12767: (41.8448104, -75.0071097),
12768: (41.8554576, -74.7595057),
12769: (41.6392603, -74.4457123),
12770: (41.4403697, -74.8232207),
12771: (41.3750937, -74.692663),
12775: (41.6259256, -74.5976603),
12776: (41.92625995, -74.8643013730444),
12777: (41.5490925, -74.6932298009079),
12778: (41.658816, -74.8236614055944),
12779: (41.7206468, -74.6343271),
12780: (41.4000933, -74.7232189),
12781: (41.6214825, -74.4507126),
12783: (41.7506445, -74.7779402),
12784: (41.6681473, -74.6251606),
12785: (41.4987043, -74.5584936),
12786: (41.6770338, -74.8279413),
12787: (41.7975888, -74.8268291),
12788: (41.759814, -74.5940484),
12789: (41.7106479, -74.5743262),
12790: (41.5767603, -74.4871031),
12791: (41.8084219, -74.8862745),
12792: (41.5225898, -74.9329444),
12801: (43.309941, -73.644447),
12803: (43.299447, -73.635178),
12804: (43.3772932, -73.6131714),
12808: (43.7639539, -73.7584623),
12809: (43.23795, -73.491669),
12810: (43.4925679, -73.8429001),
12811: (43.6147877, -74.0248539),
12812: (43.8553412, -74.4434931),
12814: (43.5572898, -73.6548408),
12815: (43.6764553, -73.7495703),
12816: (43.0281329, -73.3812231),
12817: (43.6525664, -73.8009597),
12819: (43.6364539, -73.4453928),
12820: (43.4782055, -73.6426284),
12821: (43.4572922, -73.4415004),
12822: (43.244703, -73.832588),
12823: (43.1836864, -73.4267786),
12824: (43.4792357, -73.6870621),
12827: (43.414276, -73.487892),
12828: (43.267206, -73.584709),
12831: (43.1961848, -73.651784),
12832: (43.408041, -73.259583),
12833: (43.1284071, -73.8465114),
12834: (43.0906318, -73.4987251),
12835: (43.3177008, -73.8474816),
12836: (43.745553, -73.498535),
12837: (43.5259, -73.250656),
12838: (43.363967, -73.4052888),
12839: (43.300697, -73.586082),
12841: (43.6392315, -73.5070609),
12842: (43.782497, -74.272041),
12843: (43.618431, -73.961334),
12844: (43.4829549, -73.6365404),
12845: (43.425996, -73.712425),
12846: (43.3126329, -73.8345646),
12847: (43.973052, -74.421043),
12848: (43.0990003, -73.5252954),
12849: (43.4334042, -73.2834424),
12850: (43.0897964, -73.9179022),
12851: (43.791667, -73.984337),
12852: (43.969592, -74.164925),
12853: (43.699899, -73.98571),
12854: (43.4503482, -73.3414988),
12855: (43.952788, -73.728561),
12856: (43.7433297, -74.0556049),
12857: (43.7714532, -73.9312445),
12858: (43.8914481, -73.6456827),
12859: (43.1484068, -73.8865126),
12860: (43.7311765, -73.8192961),
12861: (43.7342291, -73.3748383),
12862: (43.6624129, -73.8959857),
12863: (43.0620189, -73.9170688),
12864: (43.7283982, -74.305705),
12865: (43.1722983, -73.3276101),
12866: (43.0821793, -73.7853915),
12870: (43.8386732, -73.7609635),
12871: (43.100231, -73.581963),
12872: (43.8758937, -73.7304075),
12873: (43.0903546, -73.3428885),
12874: (43.6964519, -73.5056735),
12878: (43.4178278, -73.9185642),
12879: (43.969592, -74.164925),
12883: (43.848889, -73.423347),
12884: (43.0878534, -73.594005),
12885: (43.496768, -73.776283),
12886: (43.6337444, -73.940032),
12887: (43.555764, -73.403778),
12901: (44.69282, -73.45562),
12903: (44.6967981, -73.4463115),
12910: (44.888472, -73.655777),
12911: (44.5050479, -73.4801348),
12912: (44.441714, -73.6745834),
12913: (44.4078279, -74.0870965),
12914: (44.939043, -74.567986),
12915: (44.8578221, -74.0334864),
12916: (44.830552, -74.513741),
12917: (44.9047681, -74.1693397),
12918: (44.6980977, -73.631528),
12919: (44.986656, -73.446693),
12920: (44.926648, -74.079781),
12921: (44.889931, -73.43605),
12922: (44.2864502, -74.6632351),
12923: (44.9539315, -73.9315417),
12924: (44.5050479, -73.4801348),
12926: (44.929321, -74.297447),
12927: (44.2225615, -74.8362986),
12928: (43.950563, -73.43708),
12929: (44.721613, -73.723755),
12930: (44.7175567, -74.5526752),
12932: (44.216171, -73.591232),
12933: (44.894066, -73.836708),
12934: (44.864764, -73.8970926),
12935: (44.9058729, -73.8009813),
12936: (44.0638879, -73.7542043),
12937: (44.989033, -74.494262),
12939: (44.4319972, -74.1809887),
12941: (44.375159, -73.728218),
12942: (44.256265, -73.792419),
12943: (44.1899781, -73.7862601),
12944: (44.5050479, -73.4801348),
12945: (44.3675548, -74.2326587),
12946: (44.279621, -73.979874),
12949: (41.8406485, -74.1029206),
12950: (43.7344277, -75.440289),
12952: (44.73028695, -73.9084092853456),
12953: (44.84881, -74.295044),
12955: (44.73028695, -73.9084092853456),
12956: (44.0886055, -73.5157456),
12957: (44.818133, -74.555969),
12958: (44.963583, -73.587456),
12959: (44.9580936, -73.6406994),
12960: (44.0461764, -73.5053263),
12961: (44.0611114, -73.5097094),
12962: (44.6930981, -73.5620818),
12964: (44.1633846, -73.611521),
12965: (44.6972791, -74.6593512),
12966: (44.8419939, -74.4010108),
12967: (44.8050533, -74.6749087),
12969: (44.7436591, -74.159044),
12970: (44.4386659, -74.2526581),
12972: (44.578486, -73.527031),
12973: (44.232163, -74.569702),
12974: (44.048609, -73.45974),
12975: (44.5281031, -73.4070773),
12976: (44.4669968, -74.1729322),
12977: (44.2916917, -74.0789035),
12978: (44.6083776, -73.8043096),
12979: (44.995033, -73.3713021),
12980: (44.6733509, -74.5503169),
12981: (44.651559, -73.743668),
12983: (44.329497, -74.131279),
12985: (44.62884, -73.55793),
12986: (44.224044, -74.464302),
12987: (44.3364359, -73.7756963),
12989: (44.4517163, -74.0657061),
12992: (44.8205957, -73.5070812),
12993: (44.1871187, -73.4518977971491),
12995: (44.8097716, -74.261837),
12996: (44.357488, -73.392105),
12997: (44.388409, -73.815422),
12998: (44.0875852, -73.5334041),
13020: (42.8186783, -76.072424),
13021: (42.9320202, -76.5672029),
13022: (42.9320202, -76.5672029),
13024: (42.9320202, -76.5672029),
13026: (42.7539591, -76.7024485),
13027: (43.158679, -76.33271),
13028: (43.2445133, -75.933527),
13029: (43.2381242, -76.1407575),
13030: (43.1553457, -75.9693622),
13031: (43.039233, -76.3040965),
13032: (43.079672, -75.751076),
13033: (43.168123, -76.572999),
13034: (42.8093409, -76.5700777),
13035: (42.9300668, -75.8526915),
13036: (43.286736, -76.146036),
13037: (43.0450671, -75.86658),
13039: (43.1756235, -76.1193678),
13040: (42.5422923, -75.8957534),
13041: (43.1859013, -76.1724254),
13042: (43.240451, -75.883942),
13043: (43.0417341, -75.7446299),
13044: (43.247847, -76.000197),
13045: (42.6011813, -76.1804843),
13051: (42.8764558, -75.9135283),
13052: (42.875882, -75.6802581),
13053: (42.4909053, -76.2971553),
13054: (43.1206241, -75.6710161),
13056: (42.6661801, -76.1015927),
13057: (43.0653446, -76.0785332),
13060: (43.0345105, -76.4479914),
13061: (42.8517337, -75.7554654),
13062: (42.4850722, -76.3835475),
13063: (42.835067, -75.9860322),
13064: (42.7692348, -76.2682633),
13065: (42.8142352, -76.8091216),
13066: (43.0297887, -76.0043643),
13068: (42.512807, -76.3464675),
13069: (43.322846, -76.417159),
13071: (42.6678489, -76.5357741),
13072: (42.7684005, -75.7365767),
13073: (42.5866943, -76.3666213),
13074: (43.321179, -76.578834),
13076: (43.373958, -76.152425),
13077: (42.6370141, -76.1788174),
13078: (42.9920106, -76.0715887),
13080: (43.0653441, -76.4729927),
13081: (42.6653488, -76.6166113),
13082: (43.0750671, -75.9518617),
13083: (43.643402, -76.068534),
13084: (42.8142352, -76.8091216),
13087: (42.695902, -76.164372),
13088: (43.106456, -76.217705),
13089: (43.106456, -76.217705),
13090: (43.106456, -76.217705),
13092: (42.6606263, -76.4307699),
13093: (43.4986801, -76.3857694),
13101: (42.5842136, -76.0704906),
13102: (42.443114, -76.4725920912081),
13103: (43.3236802, -76.1165902),
13104: (43.0020107, -75.9768632),
13107: (43.4572919, -76.1452031),
13108: (42.9556549, -76.3249424),
13110: (42.9090587, -76.3232396),
13111: (43.2800674, -76.6271695),
13112: (43.0828444, -76.3771554),
13113: (43.165623, -76.536886),
13114: (43.459514, -76.228818),
13115: (43.398124, -76.47744),
13116: (43.076178, -76.000753),
13117: (43.010065, -76.7032833),
13118: (42.7125702, -76.4216025),
13119: (42.9736773, -76.4424356),
13120: (42.9750662, -76.1413133),
13121: (43.479791, -76.315211),
13122: (42.8484003, -75.8543591),
13123: (43.2300689, -75.7482415),
13124: (42.6225686, -75.8196382),
13126: (43.4547284, -76.5095967),
13131: (43.406181, -76.125758),
13132: (43.2825686, -76.2704851),
13134: (42.9672898, -75.6879613),
13135: (43.231179, -76.300764),
13136: (42.5809027, -75.8649184),
13137: (43.159234, -76.4471588),
13138: (42.8989556, -76.0160326),
13139: (42.7384038, -76.6179999),
13140: (43.0345099, -76.6238343),
13141: (42.7157449, -76.145739705359),
13142: (43.567014, -76.127703),
13143: (43.247289, -76.723564),
13144: (43.569514, -76.0477),
13145: (43.644235, -76.086035),
13146: (43.0672874, -76.7596759),
13147: (42.7836809, -76.5591079),
13148: (42.910622, -76.7966215),
13152: (42.947011, -76.4291017),
13153: (42.9931214, -76.4560472),
13154: (43.1314546, -76.7657877),
13155: (42.6467349, -75.7813028),
13156: (43.325901, -76.644949),
13157: (43.196667, -75.730476),
13158: (42.7120125, -76.0285349),
13159: (42.798123, -76.1093696),
13160: (42.8397906, -76.6932818),
13162: (43.1909019, -75.729074),
13163: (43.075408, -75.70713),
13164: (43.0853445, -76.3290977),
13165: (42.9047884, -76.8627368),
13166: (43.048677, -76.5627197),
13167: (43.280902, -76.066588),
13201: (43.0481221, -76.1474244),
13202: (43.0481221, -76.1474244),
13203: (43.0481221, -76.1474244),
13204: (43.0481221, -76.1474244),
13205: (43.0481221, -76.1474244),
13206: (43.0481221, -76.1474244),
13207: (43.0481221, -76.1474244),
13208: (43.0481221, -76.1474244),
13209: (43.0481221, -76.1474244),
13210: (43.0481221, -76.1474244),
13211: (43.0481221, -76.1474244),
13212: (43.0481221, -76.1474244),
13214: (43.0481221, -76.1474244),
13215: (43.0481221, -76.1474244),
13217: (43.0481221, -76.1474244),
13218: (43.0481221, -76.1474244),
13219: (43.0481221, -76.1474244),
13220: (43.0481221, -76.1474244),
13221: (43.0481221, -76.1474244),
13224: (43.0481221, -76.1474244),
13225: (43.0481221, -76.1474244),
13235: (43.0481221, -76.1474244),
13244: (43.0481221, -76.1474244),
13250: (43.0481221, -76.1474244),
13251: (43.0481221, -76.1474244),
13252: (43.0481221, -76.1474244),
13261: (43.0481221, -76.1474244),
13290: (43.0481221, -76.1474244),
13301: (43.5344353, -75.5476355),
13302: (43.51007, -76.002142),
13303: (43.419014, -75.479507),
13304: (43.272456, -75.190086),
13305: (43.8870133, -75.4274083),
13308: (43.2797915, -75.6435156),
13309: (43.4843153, -75.3357941),
13310: (42.8892358, -75.5512901),
13312: (43.6886801, -75.2921223),
13313: (42.8792376, -75.2509971),
13314: (42.8128488, -75.3176677),
13315: (42.7453504, -75.1829401),
13316: (43.334668, -75.747986),
13317: (42.9056288, -74.5718073),
13318: (42.9459036, -75.2543302),
13319: (43.0278475, -75.2715534),
13320: (42.7956295, -74.7532018),
13321: (43.0922918, -75.379615),
13322: (42.98007, -75.2509966),
13323: (44.7278943, -73.6686982),
13324: (43.241952, -75.039024),
13325: (43.566959, -75.428696),
13326: (42.7006303, -74.924321),
13327: (43.895913, -75.392647),
13328: (42.9950695, -75.4285054),
13329: (43.100983, -74.772949),
13331: (43.7695099, -74.816839),
13332: (42.7397917, -75.5451804),
13333: (42.8309065, -74.8151489),
13334: (42.8499105, -75.612325),
13335: (42.6978509, -75.2437763),
13337: (42.7184076, -74.983212),
13338: (43.442201, -75.207253),
13339: (42.9314616, -74.6226425),
13340: (43.038959, -75.070436),
13341: (43.0367363, -75.392115),
13342: (42.6472968, -75.1718306),
13343: (43.710347, -75.4021251),
13345: (43.681529, -75.354881),
13346: (42.8268798, -75.5444159),
13348: (42.6597973, -75.0487708),
13350: (43.0256259, -74.9859889),
13352: (43.3122913, -75.1218294),
13353: (43.3909018, -74.7168209),
13354: (43.241952, -75.257034),
13355: (42.8178478, -75.4632312),
13357: (43.0150703, -75.0354347),
13360: (43.754729, -74.793205),
13361: (42.9147939, -74.9515431),
13362: (42.9864581, -75.5171209),
13363: (43.3034028, -75.5179556),
13364: (42.8086826, -75.2526642),
13365: (43.0434039, -74.8595958),
13367: (43.786711, -75.49221),
13368: (43.62539, -75.367241),
13401: (43.2144051, -75.4039155),
13402: (42.875882, -75.6802581),
13403: (43.170632, -75.29171),
13404: (43.737616, -75.469894),
13406: (43.138823, -74.9683),
13407: (43.0114592, -75.0040449),
13408: (42.8986566, -75.6402204),
13409: (42.977013, -75.586846),
13410: (42.9347949, -74.6134755),
13411: (42.6239023, -75.3321363),
13413: (43.073653, -75.287933),
13415: (42.5878535, -75.1840544),
13416: (43.185904, -75.014648),
13417: (43.105495, -75.291367),
13418: (42.8503481, -75.3907269),
13420: (43.7100676, -74.9743407),
13421: (43.2144051, -75.4039155),
13424: (43.157359, -75.332909),
13425: (42.9392363, -75.4610076),
13426: (43.574792, -75.996309),
13428: (42.9109064, -74.5740296),
13431: (43.225693, -75.06134),
13433: (43.583127, -75.345268),
13435: (43.304444, -75.152321),
13436: (43.8131196, -74.6573899),
13437: (43.533367, -75.8218),
13438: (43.327176, -75.186996),
13439: (42.8534057, -74.9854335),
13440: (43.2128473, -75.4557304),
13441: (43.2128473, -75.4557304),
13442: (44.4406028, -73.6881949),
13449: (43.2128473, -75.4557304),
13450: (42.7417411, -74.7765361),
13452: (42.9981274, -74.6829225),
13454: (43.14257, -74.7865391),
13455: (42.9139589, -75.3790591),
13456: (43.0042365, -75.2598859),
13457: (42.7803509, -75.0279352),
13459: (42.7959074, -74.617086),
13460: (42.6781266, -75.4985123),
13461: (43.073904, -75.598297),
13464: (42.6872921, -75.5707376),
13465: (42.910625, -75.5176773),
13468: (42.8289619, -74.8765402),
13469: (43.2231253, -75.2882236),
13470: (43.179895, -74.697075),
13471: (43.3036805, -75.616848),
13472: (43.7000679, -75.0018408),
13473: (43.627378, -75.41153),
13475: (42.8950724, -74.8276495),
13476: (43.079672, -75.539589),
13477: (43.0522916, -75.5015648),
13478: (43.138322, -75.570831),
13479: (43.0503059, -75.2728117),
13480: (42.931181, -75.3798924),
13482: (42.7075733, -75.1876633),
13483: (43.3878475, -75.8151893),
13484: (42.8545124, -75.6560169),
13485: (42.763405, -75.2782213),
13486: (43.3056251, -75.3829503),
13488: (42.6500755, -74.7976507),
13489: (43.4595139, -75.4637878),
13490: (43.116272, -75.403976),
13491: (42.8853489, -75.1932175),
13492: (43.122036, -75.29171),
13493: (43.424001, -75.890121),
13494: (43.5203464, -75.1548888),
13495: (43.113014, -75.271111),
13501: (43.104752, -75.2229497),
13502: (43.1009031, -75.2326641),
13503: (43.1009031, -75.2326641),
13504: (43.1009031, -75.2326641),
13505: (43.1009031, -75.2326641),
13599: (43.1009031, -75.2326641),
13601: (43.9747838, -75.9107565),
13602: (44.058053, -75.74324),
13603: (43.9747838, -75.9107565),
13605: (43.809232, -76.024089),
13606: (43.8600635, -76.0054785),
13607: (44.336127, -75.917931),
13608: (44.199436, -75.60688),
13611: (43.7833992, -76.1193694),
13612: (44.0070824, -75.7925008),
13613: (44.8075536, -74.773803),
13614: (44.5314487, -75.6627354),
13615: (44.007003, -75.984092),
13616: (44.040826, -75.8509740348575),
13617: (44.5956163, -75.1690942),
13618: (44.125494, -76.3304640631677),
13619: (43.97824, -75.609627),
13620: (43.888491, -75.511436),
13621: (44.8489423, -75.0807625),
13622: (44.066999, -76.130209),
13623: (44.4420021, -75.7569034),
13624: (44.239491, -76.085776),
13625: (44.553292, -74.939804),
13626: (43.893439, -75.673828),
13627: (44.7132825, -74.4160078),
13628: (44.035776, -75.684128),
13630: (44.5050607, -75.273822),
13631: (43.899871, -75.582504),
13632: (44.1383847, -76.0654913),
13633: (44.552803, -75.435562),
13634: (44.007835, -76.044371),
13635: (44.324585, -75.251198),
13636: (43.732845, -76.136036),
13637: (44.088325, -75.807381),
13638: (44.0222866, -75.7632565),
13639: (44.247904, -75.137901),
13640: (44.32608405, -76.0273267589538),
13641: (44.2764357, -76.0080027),
13642: (44.336864, -75.463028),
13643: (44.0342315, -75.7188119),
13645: (44.3100614, -75.4463246),
13646: (44.448977, -75.694427),
13647: (44.612282, -74.9710304),
13648: (44.152159, -75.321236),
13649: (44.9217176, -74.7262966),
13650: (43.847008, -76.181871),
13651: (43.8647846, -76.2018719),
13652: (44.467356, -75.230598),
13654: (44.618333, -75.40741),
13655: (44.9739364, -74.6632416),
13656: (44.1947726, -75.9660514),
13657: (44.0292232, -76.0429835),
13658: (44.727467, -75.321236),
13659: (43.766457, -75.959364),
13660: (44.750391, -75.131378),
13661: (43.712846, -76.062701),
13662: (44.928106, -74.892082),
13664: (44.586555, -75.648422),
13665: (44.069087, -75.493927),
13666: (44.2106178, -74.9890831),
13667: (44.801083, -74.991302),
13668: (44.75161, -74.994392),
13669: (44.694285, -75.486374),
13670: (44.182943, -75.070267),
13671: (44.199436, -75.60688),
13672: (44.6279506, -74.8153687),
13673: (44.154622, -75.708847),
13674: (43.7350677, -76.0588116),
13675: (44.2703297, -75.8543918),
13676: (44.6697996, -74.9813349),
13677: (44.5147832, -75.185762),
13678: (44.8381078, -74.9779795),
13679: (44.3008875, -75.8013388),
13680: (44.592179, -75.319176),
13681: (44.417352, -75.39196),
13682: (43.851176, -75.940755),
13683: (44.9728277, -74.7310168),
13684: (44.429612, -75.150261),
13685: (43.946171, -76.119093),
13687: (44.5106186, -74.887694),
13690: (44.159785, -75.0315826),
13691: (44.215432, -75.797424),
13692: (44.2869911, -76.0277259),
13693: (44.081442, -76.198266),
13694: (44.86463, -75.204163),
13695: (44.1339512, -74.9210219),
13696: (44.7136679, -74.9007513),
13697: (44.7947761, -74.7868595),
13699: (44.6697996, -74.9813349),
13730: (42.228136, -75.5265715),
13731: (42.1886976, -74.7857138),
13732: (42.0695189, -76.1546504),
13733: (42.2935152, -75.4792592),
13734: (42.042852, -76.4485515),
13736: (42.3042403, -76.1865965),
13737: (42.1455623, -75.8404114),
13738: (42.5684039, -76.1257608),
13739: (42.3334161, -74.8076575),
13740: (42.2620297, -74.7846024),
13743: (42.232902, -76.3424188),
13744: (42.2275753, -75.918253),
13745: (42.1667426, -75.8624167),
13746: (42.2356313, -75.8482503),
13747: (42.4909119, -74.9821045),
13748: (42.0342437, -75.803801),
13749: (42.0156328, -75.7904667),
13750: (42.4717451, -74.8446009),
13751: (42.4481351, -74.9190477),
13752: (40.7179671, -73.9852989),
13753: (42.2781401, -74.9159946),
13754: (42.0600834, -75.4276769),
13755: (42.0809204, -74.9957197),
13756: (41.9884206, -75.1337792),
13757: (42.4214691, -74.886825),
13758: (42.558125, -75.7171347),
13760: (42.098408, -76.0493684),
13761: (42.098408, -76.0493684),
13762: (42.1128526, -76.021034),
13763: (42.098408, -76.0493684),
13774: (41.9636984, -75.1748916),
13775: (42.3406373, -75.1651689),
13776: (42.4714657, -75.325729),
13777: (42.2586856, -76.0093678),
13778: (42.2628769, -74.0878112),
13780: (42.4042433, -75.4896253),
13782: (42.1911969, -74.9946083),
13783: (41.9539754, -75.2804502),
13784: (42.4261836, -76.2265976),
13786: (42.4384124, -74.6873749),
13787: (42.1784124, -75.6246298),
13788: (42.3714704, -74.6704311),
13790: (42.1156308, -75.9588092),
13794: (42.4006284, -76.020758),
13795: (42.0397993, -75.7971341),
13796: (42.530633, -75.0896077),
13797: (42.3511727, -76.0032134),
13801: (42.4784565, -75.6130279),
13802: (42.1925746, -76.0610361),
13803: (42.4417391, -76.0321474),
13804: (42.2420265, -75.3773999),
13806: (42.3670263, -74.9537721),
13807: (42.5906322, -74.9451573),
13808: (42.5486871, -75.2451685),
13809: (42.4264662, -75.3832319),
13810: (42.5784099, -75.057939),
13811: (42.2236853, -76.183263),
13812: (42.021741, -76.3668815),
13813: (42.1942461, -75.6024071),
13814: (42.617016, -75.5268475),
13815: (42.531184, -75.5235149),
13820: (42.453492, -75.0629531),
13825: (42.3973023, -75.1735017),
13826: (42.1261367, -75.6470363),
13827: (42.1034075, -76.2621549),
13830: (42.4420181, -75.5976855),
13832: (42.6170149, -75.6024065),
13833: (42.1642428, -75.8335265),
13834: (42.5303555, -74.9671035),
13835: (42.3556287, -76.2007636),
13838: (42.3157824, -75.392776),
13839: (42.2906379, -75.2557286),
13840: (42.0339631, -76.4002163),
13841: (43.8761735, -76.0999253),
13842: (42.3423047, -74.7170994),
13843: (42.5295192, -75.3851753),
13844: (42.5814604, -75.5643496),
13845: (42.0561854, -76.3479918),
13846: (42.3423045, -75.0512757),
13847: (42.2036948, -75.2793406),
13848: (42.2161881, -75.7265786),
13849: (42.3253586, -75.3123969),
13850: (42.0850747, -76.053813),
13851: (42.0850747, -76.053813),
13856: (42.1695296, -75.1293351),
13859: (42.3675804, -75.2454493),
13860: (42.4459131, -74.9632157),
13861: (42.4723007, -75.1171096),
13862: (42.3289626, -75.9677001),
13863: (42.4692381, -75.9115876),
13864: (42.2900737, -76.3782702),
13865: (42.0759128, -75.640462),
13901: (42.096968, -75.914341),
13902: (42.096968, -75.914341),
13903: (42.096968, -75.914341),
13904: (42.096968, -75.914341),
13905: (42.096968, -75.914341),
14001: (43.0150996, -78.4945500453653),
14004: (42.9000596, -78.4919671),
14005: (42.9011711, -78.2566834),
14006: (42.638393, -79.027816),
14008: (43.3271814, -78.6487085),
14009: (42.5339513, -78.4230737),
14010: (42.769781, -78.8664229),
14011: (42.8642267, -78.2802946),
14012: (43.330334, -78.554531),
14013: (43.0672812, -78.3914111),
14020: (42.9980144, -78.1875515),
14021: (42.9980144, -78.1875515),
14024: (42.5770065, -78.2527907),
14025: (42.6289495, -78.7375289),
14026: (42.9383918, -78.6847515),
14027: (42.588393, -79.017815),
14028: (43.3164256, -78.7135965),
14029: (42.4797854, -78.2497346),
14030: (42.5681176, -78.4789091),
14031: (42.9768372, -78.5930999),
14032: (43.0106139, -78.6375283),
14033: (42.6442273, -78.6847495),
14034: (42.49645, -78.920589),
14035: (42.4936725, -78.8514207),
14036: (42.9600595, -78.4055767),
14037: (42.8433932, -78.4689105),
14038: (42.9461705, -78.4847451),
14039: (42.8192273, -78.1727908),
14040: (42.9011709, -78.3886312),
14041: (42.417006, -78.976981),
14042: (42.4892295, -78.4808534),
14043: (42.9022047, -78.6956723),
14047: (42.6814481, -78.9753145),
14048: (42.479502, -79.333932),
14051: (43.0183913, -78.696697),
14052: (42.7689141, -78.6177611),
14054: (42.9314495, -78.101402),
14055: (42.552006, -78.6403032),
14056: (42.9956152, -78.3100195),
14057: (42.652282, -78.896979),
14058: (43.077282, -78.186962),
14059: (42.8510195, -78.640311),
14060: (42.4275638, -78.3608499),
14061: (42.594503, -79.09115),
14062: (42.468392, -79.176985),
14063: (42.440058, -79.331711),
14065: (42.4847852, -78.3311262),
14066: (42.6408954, -78.1338985),
14067: (43.197577, -78.5767928),
14068: (43.0243244, -78.7678332),
14069: (42.6192276, -78.6578041),
14070: (42.463117, -78.935868),
14072: (43.0097402, -78.9706093624524),
14075: (42.716293, -78.828717),
14080: (42.6411908, -78.5417311),
14081: (42.5675589, -79.1128169),
14082: (42.6500613, -78.3858509),
14083: (42.672561, -78.4361304),
14085: (42.7111701, -78.9361468),
14086: (42.9005956, -78.669997),
14091: (42.5381163, -78.9308676),
14092: (43.172555, -79.035878),
14094: (43.168863, -78.6929557832681),
14095: (43.168863, -78.6929557832681),
14098: (43.326724, -78.388914),
14101: (42.419508, -78.4944656),
14102: (42.8400596, -78.5550242),
14103: (43.220058, -78.386969),
14105: (43.212301, -78.476563),
14107: (43.1849235, -78.9831263),
14108: (43.286723, -78.710312),
14109: (43.13755555, -79.0375125585894),
14110: (42.6856155, -78.7766971),
14111: (42.595338, -78.941146),
14112: (42.6970036, -78.9414247),
14113: (42.6836721, -78.3377941),
14120: (43.038668, -78.8642034),
14125: (43.0658926, -78.269742),
14126: (43.3378336, -78.7147571),
14127: (42.7670376, -78.7435517),
14129: (42.45645, -79.001981),
14130: (42.5564517, -78.1527873),
14131: (43.2386666, -78.9097634),
14132: (43.136723, -78.8847611),
14133: (42.4958961, -78.3844612),
14134: (42.5411733, -78.5080766),
14135: (42.488391, -79.237263),
14136: (42.5160058, -79.1461454),
14138: (42.364227, -79.055595),
14139: (42.7089493, -78.5780796),
14140: (42.8181149, -78.6755836),
14141: (42.5083952, -78.6672482),
14143: (42.9817273, -78.0739023),
14144: (43.2019994, -79.0422678),
14145: (42.7050607, -78.4483532),
14150: (42.991733, -78.8824886119079),
14151: (42.991733, -78.8824886119079),
14166: (42.4489464, -79.4183789),
14167: (42.7633936, -78.3097382),
14168: (42.5189496, -78.9958695),
14169: (42.7683934, -78.5300228),
14170: (42.701449, -78.6822497),
14171: (42.402841, -78.6100253),
14172: (43.309778, -78.82615),
14173: (42.5300624, -78.4727976),
14174: (43.247453, -79.050064),
14201: (42.8867166, -78.8783922),
14202: (42.8867166, -78.8783922),
14203: (42.8867166, -78.8783922),
14204: (42.8867166, -78.8783922),
14205: (42.8867166, -78.8783922),
14206: (42.8867166, -78.8783922),
14207: (42.8867166, -78.8783922),
14208: (42.8867166, -78.8783922),
14209: (42.8867166, -78.8783922),
14210: (42.8867166, -78.8783922),
14211: (42.8867166, -78.8783922),
14212: (42.8867166, -78.8783922),
14213: (42.8867166, -78.8783922),
14214: (42.8867166, -78.8783922),
14215: (42.8867166, -78.8783922),
14216: (42.8867166, -78.8783922),
14217: (42.8867166, -78.8783922),
14218: (42.8867166, -78.8783922),
14219: (42.8867166, -78.8783922),
14220: (42.8867166, -78.8783922),
14221: (42.8867166, -78.8783922),
14222: (42.8867166, -78.8783922),
14223: (42.8867166, -78.8783922),
14224: (42.8867166, -78.8783922),
14225: (42.8867166, -78.8783922),
14226: (42.8867166, -78.8783922),
14227: (42.8867166, -78.8783922),
14228: (42.8867166, -78.8783922),
14231: (42.8867166, -78.8783922),
14233: (42.8867166, -78.8783922),
14240: (42.8867166, -78.8783922),
14241: (42.8867166, -78.8783922),
14260: (42.8867166, -78.8783922),
14261: (42.8867166, -78.8783922),
14263: (42.8867166, -78.8783922),
14264: (42.8867166, -78.8783922),
14265: (42.8867166, -78.8783922),
14267: (42.8867166, -78.8783922),
14269: (42.8867166, -78.8783922),
14270: (42.8867166, -78.8783922),
14272: (42.8867166, -78.8783922),
14273: (42.8867166, -78.8783922),
14276: (42.8867166, -78.8783922),
14280: (42.8867166, -78.8783922),
14301: (43.1030928, -79.0302618),
14302: (43.1030928, -79.0302618),
14303: (43.0784134, -79.074326602),
14304: (43.1030928, -79.0302618),
14305: (43.1030928, -79.0302618),
14410: (43.1961806, -77.8571354),
14411: (43.246488, -78.193516),
14413: (43.2111765, -76.9805232),
14414: (42.9119925, -77.7454567),
14415: (42.757013, -77.0146893),
14416: (43.085391, -77.941714),
14418: (42.5986805, -77.1538624),
14420: (43.213671, -77.93918),
14422: (43.079782, -78.063904),
14423: (42.9731175, -77.852785),
14424: (42.8844625, -77.278399),
14425: (42.9832214, -77.3089608),
14427: (42.6289515, -78.0544514),
14428: (43.104228, -77.884454),
14429: (43.193393, -78.064739),
14430: (43.233116, -77.927513),
14432: (42.9617304, -77.1399757),
14433: (43.084231, -76.869405),
14435: (42.7189532, -77.6763859),
14437: (42.5611258, -77.6961817),
14441: (42.6839586, -76.9557968),
14443: (42.8950641, -77.4347128),
14445: (43.112157, -77.483559),
14449: (43.23062, -77.1452561),
14450: (43.0993, -77.443014),
14452: (43.2447815, -78.0911291),
14453: (43.0086744, -77.464716),
14454: (42.795896, -77.816947),
14456: (42.8689552, -76.9777436),
14461: (42.7989556, -77.1316402),
14462: (42.6647868, -77.7697212),
14463: (42.7939562, -77.066359),
14464: (43.303115, -77.921124),
14466: (42.7942307, -77.6063849),
14467: (43.0611781, -77.6338983),
14468: (43.2881104, -77.7928574),
14469: (42.8950641, -77.4347128),
14470: (43.226806, -78.027155),
14471: (42.7908335, -77.5170721),
14472: (42.9519038, -77.5914322),
14475: (42.9314527, -77.4919385),
14476: (43.327281, -78.03585),
14477: (43.3276028, -78.1351835),
14478: (42.6153474, -77.0921927),
14479: (43.2412042, -78.3112756),
14480: (42.8364522, -77.7050001),
14481: (42.7720066, -77.8966709),
14482: (42.9783944, -77.9841776),
14485: (42.9047857, -77.611387),
14486: (42.8947837, -77.9491748),
14487: (42.8214525, -77.6686097),
14488: (42.8214526, -77.6386087),
14489: (43.0642305, -76.9902456),
14502: (43.06923, -77.298875),
14504: (42.9694241, -77.2296711),
14505: (43.143397, -77.189147),
14506: (42.9978411, -77.5044401),
14507: (42.7050087, -77.2716597),
14508: (43.3284457, -77.9955584),
14510: (44.1595046, -74.475168),
14511: (42.9928396, -77.8602856),
14512: (42.6160647, -77.4030253),
14513: (43.0467301, -77.0952516),
14514: (43.1197837, -77.8055632),
14515: (43.2536723, -77.7325066),
14516: (43.1856211, -76.8924623),
14517: (42.5795085, -77.942503),
14518: (42.9322868, -77.0124683),
14519: (42.8580624, -77.295025),
14520: (43.2258967, -77.3058211),
14521: (42.6764593, -76.8230111),
14522: (43.0623754, -77.2347245),
14525: (42.8761722, -78.0227877),
14526: (43.1301133, -77.4759588),
14527: (42.6603037, -77.0540989),
14529: (42.5397896, -77.6283257),
14530: (42.7156175, -78.0055618),
14532: (42.957564, -77.057471),
14533: (42.8283957, -77.8508375),
14534: (43.090959, -77.515298),
14536: (42.5697856, -78.040006),
14537: (43.0345076, -77.1574773),
14538: (43.2797862, -77.1860929),
14539: (42.83534, -77.878894),
14541: (42.752292, -76.8335672),
14542: (43.153676, -76.878572),
14543: (42.9958962, -77.6455564),
14544: (42.7600665, -77.226367),
14545: (42.6642317, -77.7141639),
14546: (43.0258957, -77.7452826),
14547: (42.8870097, -77.0960836),
14548: (42.9559145, -77.2206913),
14549: (42.7017287, -78.0219511),
14550: (42.6606177, -78.0855638),
14551: (43.237843, -77.061362),
14555: (43.27245, -76.987993),
14556: (42.6789527, -77.8272231),
14557: (43.0482873, -78.0657989),
14558: (42.8553412, -77.6752772),
14559: (43.18645, -77.803897),
14560: (42.6372883, -77.5958264),
14561: (42.8250665, -77.0958052),
14563: (43.2228409, -77.3716577),
14564: (42.9825634, -77.4088794),
14568: (43.13923, -77.272207),
14569: (42.7401871, -78.1325548),
14571: (43.3167135, -78.2520383),
14572: (42.5678449, -77.5897139),
14580: (43.212285, -77.429994),
14585: (42.9058971, -77.5391622),
14586: (43.0400626, -77.6616685),
14588: (42.6822923, -76.8685694),
14589: (43.2241225, -77.1863529),
14590: (43.220622, -76.814958),
14591: (42.7039813, -78.2415228),
14592: (42.8711324, -77.885552),
14602: (43.157285, -77.615214),
14603: (43.1854754, -77.6106861508176),
14604: (43.1854754, -77.6106861508176),
14605: (43.1635257, -77.6083784825996),
14606: (43.1854754, -77.6106861508176),
14607: (43.1854754, -77.6106861508176),
14608: (43.157285, -77.615214),
14609: (43.1854754, -77.6106861508176),
14610: (43.1854754, -77.6106861508176),
14611: (43.157285, -77.615214),
14612: (43.1854754, -77.6106861508176),
14613: (43.1854754, -77.6106861508176),
14614: (43.157285, -77.615214),
14615: (43.1854754, -77.6106861508176),
14616: (43.1854754, -77.6106861508176),
14617: (43.1854754, -77.6106861508176),
14618: (43.1854754, -77.6106861508176),
14619: (43.157285, -77.615214),
14620: (43.157285, -77.615214),
14621: (43.1854754, -77.6106861508176),
14622: (43.1854754, -77.6106861508176),
14623: (43.157285, -77.615214),
14624: (43.157285, -77.615214),
14625: (43.1854754, -77.6106861508176),
14626: (43.1854754, -77.6106861508176),
14627: (43.157285, -77.615214),
14638: (43.157285, -77.615214),
14639: (43.157285, -77.615214),
14642: (43.157285, -77.615214),
14643: (43.157285, -77.615214),
14644: (43.157285, -77.615214),
14646: (43.157285, -77.615214),
14647: (43.157285, -77.615214),
14649: (43.157285, -77.615214),
14650: (43.157285, -77.615214),
14651: (43.157285, -77.615214),
14652: (43.157285, -77.615214),
14653: (43.157285, -77.615214),
14692: (43.157285, -77.615214),
14694: (43.157285, -77.615214),
14701: (42.0970023, -79.2353259),
14702: (42.0970023, -79.2353259),
14706: (42.0900647, -78.4941887),
14707: (42.0836783, -78.0644508),
14708: (42.0125667, -78.0577834),
14709: (42.3067345, -78.0158388),
14710: (42.096446, -79.3756044),
14711: (42.3428443, -78.1113975),
14712: (42.161724, -79.391714),
14714: (42.2756225, -78.2264021),
14715: (42.0670399, -78.1669081),
14716: (42.388669, -79.441157),
14717: (42.3864543, -78.1536209),
14718: (42.344225, -79.309489),
14719: (42.2234823, -78.6477096),
14720: (42.109502, -79.283104),
14721: (41.9995099, -78.2689024),
14722: (42.2894671, -79.421728),
14723: (42.294504, -79.099764),
14724: (42.020888, -79.63005),
14726: (42.2408935, -79.0608745),
14727: (42.2175668, -78.2752927),
14728: (42.2392247, -79.4453246),
14729: (42.389785, -78.754753),
14730: (42.172839, -78.947817),
14731: (42.2750639, -78.6728071),
14732: (42.2167411, -79.1085802),
14733: (42.11867, -79.19838),
14735: (42.4661754, -78.115008),
14736: (42.1192226, -79.7325485),
14737: (42.3370091, -78.4580762),
14738: (42.0545029, -79.1581019),
14739: (42.2064566, -78.1375099),
14740: (42.193392, -79.248658),
14741: (42.2145087, -78.636417),
14742: (42.119502, -79.3103261),
14743: (42.1678436, -78.3872408),
14744: (42.4233981, -78.1572319),
14745: (42.4728418, -78.1363976),
14747: (42.1572816, -79.1019877),
14748: (42.1582201, -78.6806365),
14750: (42.104224, -79.333104),
14751: (42.293116, -79.016428),
14752: (42.3517246, -79.3242113),
14753: (42.0272856, -78.6294717),
14754: (42.0270104, -78.2061224),
14755: (42.252563, -78.80559),
14756: (42.1967243, -79.4239362),
14757: (42.253947, -79.504491),
14758: (42.0125559, -79.4494948),
14760: (42.077565, -78.4297419),
14766: (42.356173, -78.8317),
14767: (42.075056, -79.483105),
14769: (42.37978, -79.467547),
14770: (42.0386764, -78.3408496),
14772: (42.162005, -78.975317),
14774: (42.0884, -78.153343),
14775: (42.267002, -79.710602),
14777: (42.3922869, -78.2536243),
14778: (42.0803426, -78.4750213),
14779: (42.1578412, -78.7150311),
14781: (42.159224, -79.595326),
14782: (42.263947, -79.258656),
14783: (42.1081167, -78.9042042),
14784: (42.317558, -79.355879),
14785: (42.1567241, -79.4014368),
14786: (42.1281221, -78.2430688),
14787: (42.32228, -79.578103),
14788: (42.0622874, -78.3772399),
14801: (42.1051571, -77.2340584),
14802: (42.2542366, -77.7905509),
14803: (42.2697921, -77.7591607),
14804: (42.3222916, -77.738327),
14805: (42.3131298, -76.7241178),
14806: (42.1564581, -77.7955509),
14807: (42.3945133, -77.6966596),
14808: (42.5542347, -77.4724875),
14809: (42.4091649, -77.4206245),
14810: (42.3370164, -77.3177577),
14812: (42.2911853, -76.9596855),
14813: (42.2231241, -78.0344506),
14814: (42.1372967, -76.9369067),
14815: (42.3711837, -77.1088596),
14816: (42.173408, -76.733841),
14817: (42.3806287, -76.3946593),
14818: (42.4200726, -76.8488463),
14819: (42.199239, -77.4063715),
14820: (42.1803504, -77.3635923),
14821: (42.2331295, -77.1974748),
14822: (42.4614564, -77.7769405),
14823: (42.2703487, -77.6058225),
14824: (42.2817412, -76.6968945),
14825: (42.1384667, -76.7725493),
14826: (42.5022907, -77.5072102),
14827: (42.1822963, -77.1416388),
14830: (42.1435257, -77.0543408),
14831: (42.1435257, -77.0543408),
14836: (42.5408977, -77.9525029),
14837: (42.5234044, -76.976631),
14838: (42.1859079, -76.6699493),
14839: (42.13507, -77.6483236),
14840: (42.4078495, -77.2235873),
14841: (42.5006271, -76.8724586),
14842: (42.5895869, -76.9551334),
14843: (42.3278477, -77.6611025),
14845: (42.167019, -76.8205119),
14846: (42.5470083, -77.9941709),
14847: (42.6170155, -76.7249502),
14850: (42.4396039, -76.4968019),
14851: (42.4396039, -76.4968019),
14852: (42.4396039, -76.4968019),
14853: (42.4396039, -76.4968019),
14854: (42.5084053, -76.6149456),
14855: (42.122571, -77.5030413),
14856: (42.3722934, -77.3658151),
14857: (42.5161824, -76.9280172),
14858: (42.0284072, -77.1396946),
14859: (42.0911853, -76.5499445),
14860: (42.6139597, -76.8224557),
14861: (42.0297962, -76.7205076),
14863: (42.4575724, -76.710228),
14864: (42.2653526, -76.8346791),
14865: (42.3472958, -76.8452351),
14867: (42.3621811, -76.5905632),
14869: (42.3367406, -76.7885655),
14870: (42.16396, -77.0937953488168),
14871: (42.0367409, -76.8694036),
14872: (42.2253526, -76.845513),
14873: (42.2359045, -77.3750862),
14874: (42.5250703, -77.167196),
14876: (42.4303502, -76.9327397),
14877: (42.0842363, -77.6622129),
14878: (42.4711829, -76.9274616),
14879: (42.2886844, -77.2183091),
14880: (42.1714573, -77.9786147),
14881: (42.3956285, -76.3504909),
14882: (42.4840418, -76.4779117),
14883: (42.2097963, -76.4932748),
14884: (42.4778443, -77.8533322),
14885: (42.0436813, -77.5460982),
14886: (42.5422939, -76.6660589),
14887: (42.4081279, -77.0583016),
14889: (42.1986854, -76.5524441),
14891: (42.3810555, -76.8705777),
14892: (42.0103519, -76.527166),
14893: (43.1500557, -77.0377603),
14894: (42.0161851, -76.7268968),
14895: (42.1220125, -77.9480575),
14897: (42.0378463, -77.7624938),
14898: (42.0803496, -77.4085938),
14901: (42.0897965, -76.8077338),
14902: (42.0897965, -76.8077338),
14903: (42.0897965, -76.8077338),
14904: (42.0897965, -76.8077338),
14905: (42.0897965, -76.8077338)
}

    civ_list2 = [
#['https://www.ellicottvillecentral.com/', 0, (41.7065779, -73.9284101)],
#['https://www.broctoncsd.org/Page/1907', 0, (41.7065779, -73.9284101)],
['http://www.liverpool.k12.ny.us/departments/human-resources/job-opportunities', 0, (41.7065779, -73.9284101)]
#['http://www.hicksvillepublicschools.org', 0, (41.7065779, -73.9284101)]
]
    # Civil Service URLs, initial crawl levels, and coordinates database
    civ_list = (
['http://cityofpoughkeepsie.com/personnel', 0, (41.7065779, -73.9284101)],
['http://cmvny.com/departments/civil-service/job-postings', 0, (40.9125992, -73.8370786)],
['http://greenegovernment.com/departments/human-resources-and-civil-service', 0, (42.1956438, -74.1337508)],
['http://humanresources.westchestergov.com/job-seekers/civil-service-exams', 0, (41.0339862, -73.7629097)],
['http://kingston-ny.gov/employment', 0, (41.9287812, -74.0023702)],
['http://niagarafallsusa.org/government/city-departments/human-resources-department', 0, (43.1030928, -79.0302618)],
['http://ny-whiteplains.civicplus.com/index.aspx?nid=98', 0, (41.0335885, -73.7639768)],
['http://ocgov.net/personnel', 0, (43.104752, -75.2229497)],
['http://oneidacity.com/civil-servic', 0, (43.2144051, -75.4039155)],
['http://oswegocounty.com/humanresources/openings.php', 0, (43.4547284, -76.5095967)],
['http://oysterbaytown.com/departments/human-resources', 0, (40.6806564, -73.4742914)],
['http://rocklandgov.com/departments/personnel/civil-service-examinations', 0, (41.1469917, -73.9902998)],
['http://sullivanny.us/index.php/Departments/Personnel', 0, (41.6556465, -74.6893282)],
['http://tompkinscountyny.gov/personnel', 0, (42.4396039, -76.4968019)],
['http://villageofhempstead.org/197/employment-opportunities', 0, (40.7063185, -73.618684)],
['http://watervliet.com/city/civil-service.htm', 0, (42.7282483, -73.7014649039252)],
['http://web.co.wayne.ny.us', 0, (43.0642305, -76.9902456)],
['http://www.albanycounty.com/civilservice', 0, (42.6511674, -73.754968)],
['http://www.alleganyco.com/departments/human-resources-civil-service', 0, (42.2231241, -78.0344506)],
['http://www.amherst.ny.us', 0, (42.9637836, -78.7377258)],
['http://www.auburnny.gov/public_documents/auburnny_civilservice/index', 0, (42.9320202, -76.5672029)],
['http://www.batavianewyork.com/fire-department/pages/employment', 0, (42.9980144, -78.1875515)],
['http://www.binghamton-ny.gov/departments/personnel/employment/employment', 0, (42.096968, -75.914341)],
['http://www.brookhaven.org', 0, (40.8312096, -73.029552)],
['http://www.cattco.org/jobs', 0, (42.252563, -78.80559)],
['http://www.cayugacounty.us/community/civilservicecommission/examannouncementsvacancies.aspx', 0, (42.932628, -76.5643831)],
['http://www.chemungcountyny.gov/departments/a_-_f_departments/civil_service_personnel/index.php', 0, (42.0897965, -76.8077338)],
['http://www.ci.buffalo.ny.us/home/city_departments/civil_service', 0, (42.8867166, -78.8783922)],
['http://www.ci.webster.ny.us/index.aspx?nid=85&amp;_sm_au_=ivv8z8lp1wffsnv6', 0, (43.263428, -77.4334757)],
['http://www.cityofelmira.net/personnel', 0, (42.0897965, -76.8077338)],
['http://www.cityofglencoveny.org/index.htm', 0, (40.862755, -73.6336094)],
['http://www.cityofglensfalls.com/index.aspx?nid=55', 0, (43.3772932, -73.6131714)],
['http://www.cityofithaca.org/299/civil-service-examinations', 0, (42.4396039, -76.4968019)],
['http://www.cityofnewburgh-ny.gov/civil-service', 0, (41.5034271, -74.0104179)],
['http://www.cityofpeekskill.com/human-resources/pages/about-human-resources', 0, (41.289811, -73.9204922)],
['http://www.cityofrochester.gov/article.aspx?id=8589936759', 0, (43.157285, -77.615214)],
['http://www.cityofschenectady.com/208/human-resources', 0, (42.8143922952735, -73.9420906329747)],
['http://www.cityofutica.com/departments/civil-service/index', 0, (43.1009031, -75.2326641)],
['http://www.cliftonpark.org/services/employment-applications.html', 0, (42.8656325, -73.7709535)],
['http://www.clintoncountygov.com/departments/personnel/personnelhomepage.htm', 0, (44.69282, -73.45562)],
['http://www.co.chautauqua.ny.us/314/human-resources', 0, (42.253947, -79.504491)],
['http://www.co.chenango.ny.us/personnel/examinations', 0, (42.531184, -75.5235149)],
['http://www.co.delaware.ny.us/departments/pers/jobs.htm', 0, (42.2781401, -74.9159946)],
['http://www.co.dutchess.ny.us/civilserviceinformationsystem/applicantweb/frmannouncementlist.aspx?aspxerrorpath=/civilserviceinformationsystem/applicantweb/frmuserlogin', 0, (41.7065779, -73.9284101)],
['http://www.co.dutchess.ny.us/countygov/departments/personnel/psexamannouncements.htm', 0, (41.7065779, -73.9284101)],
['http://www.co.essex.ny.us/jobs.asp', 0, (44.216171, -73.591232)],
['http://www.co.genesee.ny.us/departments/humanresources/index.html', 0, (42.9980144, -78.1875515)],
['http://www.co.jefferson.ny.us', 0, (43.9747838, -75.9107565)],
['http://www.co.livingston.state.ny.us/index.aspx?nid=207', 0, (42.795896, -77.816947)],
['http://www.co.ontario.ny.us/jobs.aspx', 0, (42.8844625, -77.278399)],
['http://www.co.st-lawrence.ny.us/departments/humanresources/examinationschedule', 0, (44.5956163, -75.1690942)],
['http://www.co.ulster.ny.us/personnel', 0, (41.9287812, -74.0023702)],
['http://www.cohoes.com', 0, (42.7742446, -73.7001187)],
['http://www.cortland-co.org/263/personnel-civil%20service', 0, (42.6000833, -76.1804347)],
['http://www.cs.ny.gov', 0, (42.6511674, -73.754968)],
['http://www.cuny.edu/employment/civil-service.html', 0, (40.7308619, -73.9871558)],
['http://www.eastchester.org/departments/comptoller.php', 0, (40.9562415, -73.8129474)],
['http://www.eastfishkillny.org/government/employment.htm', 0, (41.5839824, -73.8087442)],
['http://www.erie.gov/employment', 0, (42.8867166, -78.8783922)],
['http://www.fultoncountyny.gov/node/5', 0, (43.0068689, -74.3676437)],
['http://www.gobroomecounty.com/personnel/cs', 0, (42.1156308, -75.9588092)],
['http://www.greenburghny.com', 0, (41.0447887, -73.803487)],
['http://www.hamiltoncounty.com/government/departments-services', 0, (43.47111, -74.412804)],
['http://www.huntingtonny.gov/content/13753/13757/17478/17508/default.aspx?_sm_au_=ivvt78qz5w7p2qhf', 0, (40.868154, -73.425676)],
['http://www.irondequoit.org/town-departments/human-resources/town-employment-opportunities?_sm_au_=ivv8z8lp1wffsnv6', 0, (43.1854754, -77.6106861508176)],
['http://www.lackawannany.gov/departments/civil-service', 0, (42.8262, -78.820732)],
['https://www.lockportny.gov/current-exams-and-openings/', 0, (43.168863, -78.6929557832681)],
['http://www.longbeachny.org/index.asp?type=b_basic&amp;sec={9c88689c-135f-4293-a9ce-7a50346bea23}', 0, (40.58888905, -73.6648751135986)],
['http://www.mechanicville.com/index.aspx?nid=563', 0, (42.903367, -73.686416)],
['http://www.middletown-ny.com/departments/civil-service.html?_sm_au_=ivvrlpv4fvqpnjqj', 0, (41.44591415, -74.4224417389405)],
['http://www.nassaucivilservice.com/nccsweb/homepage.nsf/homepage?readform', 0, (40.7063185, -73.618684)],
['http://www.newrochelleny.com/index.aspx?nid=362', 0, (40.9114459, -73.7841684271834)],
['http://www.niagaracounty.com/departments/civilservice.aspx', 0, (43.168863, -78.6929557832681)],
['http://www.northhempstead.com/employment-opportunities', 0, (40.7978787, -73.6995749)],
['http://www.norwichnewyork.net/human_resources.html', 0, (42.531184, -75.5235149)],
['http://www.ogdensburg.org/index.aspx?nid=97', 0, (44.694285, -75.486374)],
['http://www.oneonta.ny.us/departments/personnel', 0, (42.453492, -75.0629531)],
['http://www.ongov.net/employment/civilservice.html', 0, (43.0481221, -76.1474244)],
['http://www.ongov.net/employment/jurisdiction.html', 0, (43.158679, -76.33271)],
['http://www.ongov.net/employment/jurisdiction.html?_sm_au_=ivvrlpv4fvqpnjqj', 0, (43.0481221, -76.1474244)],
['http://www.orleansny.com/departments/operations/personnel.aspx', 0, (43.246488, -78.193516)],
['http://www.oswegony.org/government/personnel', 0, (43.4547284, -76.5095967)],
['http://www.otsegocounty.com/depts/per', 0, (42.7006303, -74.924321)],
['http://www.penfield.org', 0, (43.1301133, -77.4759588)],
['http://www.perinton.org/departments/finpers', 0, (43.0993, -77.443014)],
['http://www.putnamcountyny.com/personneldept', 0, (41.4266361, -73.6788272)],
['http://www.putnamcountyny.com/personneldept/exam-postings', 0, (41.4266361, -73.6788272)],
['http://www.ramapo.org/page/personnel-30.html?_sm_au_=ivvt78qz5w7p2qhf', 0, (41.1151372, -74.1493948)],
['http://www.rensco.com/county-job-assistance', 0, (42.7284117, -73.6917878)],
['http://www.rvcny.us/jobs.html?_sm_au_=ivv8z8lp1wffsnv6', 0, (40.6574186, -73.6450664)],
['http://www.ryeny.gov', 0, (40.9808209, -73.684294)],
['http://www.saratoga-springs.org/jobs.aspx', 0, (43.0821793, -73.7853915)],
['http://www.saratogacountyny.gov/departments/personnel', 0, (43.0009087, -73.8490111)],
['http://www.schenectadycounty.com', 0, (42.8143922952735, -73.9420906329747)],
['http://www.schohariecounty-ny.gov', 0, (42.5757217, -74.4390277)],
['http://www.schuylercounty.us/index.aspx?nid=119', 0, (42.3810555, -76.8705777)],
['http://www.smithtownny.gov/jobs.aspx?_sm_au_=ivvt78qz5w7p2qhf', 0, (40.8559314, -73.2006687)],
['http://www.southamptontownny.gov/jobs.aspx', 0, (40.884267, -72.3895296)],
['http://www.steubencony.org/pages.asp?pgid=32', 0, (42.3370164, -77.3177577)],
['http://www.suffolkcountyny.gov/departments/civilservice.aspx', 0, (40.8256537, -73.2026138)],
['http://www.tiogacountyny.com/departments/personnel-civil-service', 0, (42.1034075, -76.2621549)],
['http://www.tonawandacity.com/residents/civil_service.php', 0, (42.991733, -78.8824886119079)],
['http://www.townofbethlehem.org/137/human-resources?_sm_au_=ivv8z8lp1wffsnv6', 0, (42.6220235, -73.8326232)],
['http://www.townofbrighton.org/index.aspx?nid=219&amp;_sm_au_=ivv8z8lp1wffsnv6', 0, (43.1635257, -77.6083784825996)],
['http://www.townofchili.org/notice-category/job-postings', 0, (43.157285, -77.615214)],
['http://www.townofcortlandt.com', 0, (41.248774, -73.9086846461571)],
['http://www.townofguilderland.org/pages/guilderlandny_hr/index?_sm_au_=ivv8z8lp1wffsnv6', 0, (42.704522, -73.911513)],
['http://www.townofhempstead.org/civil-service-commission?_sm_au_=ivv8z8lp1wffsnv6', 0, (40.7063185, -73.618684)],
['http://www.townofossining.com/cms/resources/human-resources', 0, (41.1613168, -73.8620367)],
['http://www.townofpittsford.org/home-hr?_sm_au_=ivv8z8lp1wffsnv6', 0, (43.090959, -77.515298)],
['http://www.townofpoughkeepsie.com/human_resources/index.html?_sm_au_=ivv8z8lp1wffsnv6', 0, (41.7065779, -73.9284101)],
['http://www.townofriverheadny.gov/pview.aspx?id=2481&amp;catid=118&amp;_sm_au_=ivvt78qz5w7p2qhf', 0, (40.9170435, -72.6620402)],
['http://www.townofunion.com', 0, (42.1128526, -76.021034)],
['http://www.townofwallkill.com/index.php/departments/human-resources', 0, (41.44591415, -74.4224417389405)],
['http://www.troyny.gov/departments/personnel-department', 0, (42.7284117, -73.6917878)],
['http://www.usajobs.gov', 0, (44.933143, 7.540121)],
['http://www.vestalny.com/departments/human_resources/job_opportunities.php', 0, (42.0850747, -76.053813)],
['http://www.villageofossining.org/personnel-department', 0, (41.1613168, -73.8620367)],
['http://www.vsvny.org/index.asp?type=b_job&amp;sec=%7b05c716c7-40ee-49ee-b5ee-14efa9074ab9%7d&amp;_sm_au_=ivv8z8lp1wffsnv6', 0, (40.6715969, -73.6982991)],
['http://www.warrencountyny.gov/civilservice/exams.php', 0, (43.425996, -73.712425)],
['http://www.washingtoncountyny.gov/jobs.aspx', 0, (43.267206, -73.584709)],
['http://www.wyomingco.net/164/civil-service', 0, (42.74271215, -78.1326011420972)],
['http://www.yatescounty.org/203/personnel', 0, (42.6609248, -77.0563316)],
['http://www.yonkersny.gov/work/jobs-civil-service-exams', 0, (40.9312099, -73.8987469)],
['http://www.yorktownny.org/jobs', 0, (41.2709274, -73.7776336)],
['http://www1.nyc.gov/jobs', 0, (40.7308619, -73.9871558)],
['http://www1.nyc.gov/jobs/index.page', 0, (40.7308619, -73.9871558)],
['http://www2.monroecounty.gov/employment-index.php', 0, (43.157285, -77.615214)],
['https://countyfranklin.digitaltowpath.org:10078/content/Departments/View/6:field=services;/content/DepartmentServices/View/48', 0, (44.831732274226, -74.5184874695369)],
['https://countyherkimer.digitaltowpath.org:10069/content/Departments/View/9', 0, (43.0256259, -74.9859889)],
['https://mycivilservice.rocklandgov.com', 0, (41.1670394, -74.043197)],
['https://mycivilservice.schenectadycounty.com', 0, (42.8143922952735, -73.9420906329747)],
['https://romenewyork.com/civil-service', 0, (43.2128473, -75.4557304)],
['https://seneca-portal.mycivilservice.com', 0, (42.9047884, -76.8627368)],
['https://sites.google.com/a/columbiacountyny.com/civilservice', 0, (42.2528649, -73.790959)],
['https://www.albanyny.gov/government/departments/humanresources/employment', 0, (42.6511674, -73.754968)],
['https://www.co.montgomery.ny.us/web/sites/departments/personnel/default.asp', 0, (42.9545179, -74.3765241)],
['https://www.colonie.org/departments/civilservice', 0, (42.7442986, -73.7614799)],
['https://www.lewiscounty.org/departments/human-resources/human-resources', 0, (43.7884182, -75.4935757)],
['https://www.madisoncounty.ny.gov/287/personnel', 0, (43.075408, -75.70713)],
['https://www.monroeny.org/doc-center/town-of-monroe-job-opportunities.html', 0, (41.3304767, -74.1866348)],
['https://www.orangecountygov.com/1137/human-resources', 0, (41.4020382, -74.3243191)],
['https://www.orangetown.com/groups/department/personnel', 0, (41.0465776, -73.9496707)],
['https://www.townofislip-ny.gov/?Itemid=220', 0, (40.7360109, -73.2089705862445)],
['https://www.watertown-ny.gov/index.asp?nid=791', 0, (43.9747838, -75.9107565)]
)




    # School URLs, initial crawl levels, and coordinates database
    school_list = (
['http://academyofthecity.org/about_us/employment', 0, (40.7461604, -73.9032853)],
['http://albanycommunitycs.org/careers', 0, (42.6511674, -73.754968)],
['http://aldenschools.org/Page/25', 0, (42.9029263, -78.4934704)],
['http://bemusptcsd.org/district/employment_information', 0, (42.161724, -79.391714)],
['http://berlincentral.org/district/employment', 0, (42.625928, -73.361092)],
['http://bit.ly/2xbEAIJ', 0, (41.6598157, -73.9570826)],
['http://bphs.democracyprep.org', 0, (40.85048545, -73.8404035580209)],
['http://brillacollegeprep.org/careers', 0, (40.85048545, -73.8404035580209)],
['http://brooklyncompass.org/careers', 0, (40.64530975, -73.9550230275334)],
['http://brooklyneastcollegiate.uncommonschools.org/brooklyn-east/careers', 0, (40.64530975, -73.9550230275334)],
['http://brownsvillecollegiate.uncommonschools.org/bvc/careers', 0, (40.64530975, -73.9550230275334)],
['http://buffaloschools.applicantstack.com/x/openings', 0, (42.8867166, -78.8783922)],
['https://www.applitrack.com/buffaloschools/onlineapp/default.aspx?all=1', 0, (42.8867166, -78.8783922)],
['http://campacharter.org', 0, (40.64530975, -73.9550230275334)],
['http://classicalcharterschools.org/careers', 0, (40.85048545, -73.8404035580209)],
['http://community.waverlyschools.com/employment', 0, (42.0103519, -76.527166)],
['http://comsewogue.k12.ny.us', 0, (40.9253764, -73.0473284)],
['http://comsewogue.k12.ny.us/departments/human_resources', 0, (40.9253764, -73.0473284)],
['http://coneyislandprep.org/careers/career-opportunities', 0, (40.64530975, -73.9550230275334)],
['http://csicharter.org/career', 0, (42.8867166, -78.8783922)],
['http://cvweb.wnyric.org/Page/998', 0, (42.263947, -79.258656)],
['http://democracyprep.org/careers', 0, (40.85048545, -73.8404035580209)],
['http://district.uniondaleschools.org/job_postings', 0, (40.7308619, -73.9871558)],
['http://dpems.democracyprep.org', 0, (40.8088437, -73.9658566)],
['http://ecs.schoolwires.com/contact_us/employment', 0, (41.5270346, -74.8840544)],
['http://ecsli.org/careers', 0, (40.6914852, -73.8056771)],
['http://egcsd.org/departments/personnel-and-professional-development/employment', 0, (42.5909135, -73.7017858)],
['http://elmcharterschool.org/work-at-elm', 0, (40.6524927, -73.7914214158161)],
['http://eufsd.org/domain/119', 0, (41.0550969, -73.8201338)],
['http://excellenceboys.uncommonschools.org', 0, (40.64530975, -73.9550230275334)],
['http://excellencegirls.uncommonschools.org/egcs/careers', 0, (40.64530975, -73.9550230275334)],
['http://explorenetwork.org/careers/careers', 0, (40.64530975, -73.9550230275334)],
['http://gc.schoolwires.net/Page/3855', 0, (40.72319685, -73.6403872966069)],
['http://gilboa-conesville.k12.ny.us/our_school/Job_Vacancies', 0, (42.3073066, -74.2520875)],
['http://greenville.k12.ny.us/district/Human%20Resources/Availablepositions.asp', 0, (42.4153596, -74.0220769)],
['http://gufsd.org/district/employment-opportunities', 0, (41.1002404, -72.3699098)],
['http://hammondcsd.schoolwires.net/Page/104', 0, (44.448977, -75.694427)],
['http://healthsciencescharterschool.org/apps/pages/index.jsp?uREC_ID=366249&type=d&pREC_ID=816495', 0, (42.8867166, -78.8783922)],
['http://hpes.democracyprep.org', 0, (42.655843, -73.756471)],
['http://imaginemeleadership.org/about-us/careers', 0, (40.64530975, -73.9550230275334)],
['http://inletcommonschool.wordpress.com', 0, (43.754729, -74.793205)],
['http://integrationcharterschools.org/jobs', 0, (40.5834557, -74.1496048)],
['http://integrationcharterschools.org/richmond-preparatory-charter-school', 0, (40.5834557, -74.1496048)],
['http://jerichoschools.org', 0, (40.7920441, -73.5398476)],
['http://jobs.successacademies.org/search', 0, (40.8088437, -73.9658566)],
['http://kingscollegiate.uncommonschools.org/kccs/careers', 0, (40.64530975, -73.9550230275334)],
['http://leadershipprepbedstuy.uncommonschools.org/lpbs/our-school/elementary-academy', 0, (40.64530975, -73.9550230275334)],
['http://leadershipprepbrownsville.uncommonschools.org/lpbv/our-school/elementary-academy', 0, (40.64530975, -73.9550230275334)],
['http://leadershipprepcanarsie.uncommonschools.org/lpcs/our-school/elementary-academy', 0, (40.64530975, -73.9550230275334)],
['http://legacycollegeprep.org', 0, (40.85048545, -73.8404035580209)],
['http://lisboncs.schoolwires.com/Page/1346', 0, (44.727467, -75.321236)],
['http://lmcs.k12.ny.us/domain/15', 0, (41.9003667, -74.8282167)],
['http://mesacharter.org', 0, (40.64530975, -73.9550230275334)],
['http://middlevillageprep.org/apps/jobs', 0, (40.7189809300189, -73.8795457411145)],
['http://motthallcharterschool.org', 0, (40.85048545, -73.8404035580209)],
['http://nanuet-union-free-school-district.echalksites.com/employment_opportunities', 0, (41.0895016, -74.0070235)],
['http://northport.k12.ny.us/district/human_resources', 0, (40.9038855, -73.3419913726415)],
['http://northshore.k12.ny.us/district/employment.htm', 0, (40.845604, -73.646664)],
['http://nycmcs.org/about-us/employment', 0, (40.85048545, -73.8404035580209)],
['http://obenschools.org/domain/33', 0, (40.865819, -73.5320304)],
['http://oceanhillcollegiate.uncommonschools.org/ohc/careers', 0, (40.64530975, -73.9550230275334)],
['http://onteora.schoolwires.com/departments/human-resources', 0, (42.0050923, -74.2659804)],
['http://pvcsd.org/index.php/district/district-info/human-resources', 0, (41.3359272, -73.8740252)],
['http://ripleyelementary.weebly.com/employment-opportunities.html', 0, (42.267002, -79.710602)],
['http://rochesterprep.uncommonschools.org/rpcs/careers', 0, (43.157285, -77.615214)],
['http://romuluscsd.org/employment_opportunities', 0, (42.752292, -76.8335672)],
['http://roslyn.schoolwires.net/domain/37', 0, (40.7998227, -73.6509621)],
['http://rsufsd.weebly.com/employment-opportunities.html', 0, (40.8076955, -72.7088261)],
['http://scotiaglenvilleschools.org', 0, (42.8264652, -73.9642915)],
['http://shermancsd.org/employment', 0, (42.159224, -79.595326)],
['https://classicalcharterschools.org/careers', 0, (40.85048545, -73.8404035580209)],
['http://southoldufsd.com', 0, (41.06621895, -72.42794565)],
['http://storefrontacademy.org/employment-opportunities', 0, (40.7238838, -73.9911486)],
['http://sweethomeschools.org/District/2200-Employment-Opportunities.html', 0, (43.0186816387441, -78.8018505655704)],
['http://troyprep.uncommonschools.org/careers-2', 0, (42.7284117, -73.6917878)],
['http://tullyschools.org/teacherpage.cfm?teacher=694', 0, (42.798123, -76.1093696)],
['http://upchs.org/contact_school/prospective_employees/current_opportunities', 0, (40.85048545, -73.8404035580209)],
['http://uticaschools.schoolwires.net/Page/115', 0, (43.104752, -75.2229497)],
['http://valleystream13.com/departments/human-resources', 0, (40.6631362, -73.7056955)],
['http://westbuffalocharter.org/job-opportunities', 0, (42.8867166, -78.8783922)],
['http://williamsburgcollegiate.uncommonschools.org/wccs/careers', 0, (40.64530975, -73.9550230275334)],
['http://wps.greenwichcsd.org/employment', 0, (43.0906318, -73.4987251)],
['http://www.1000islandsschools.org', 0, (44.239491, -76.085776)],
['http://www.3villagecsd.k12.ny.us', 0, (40.928767, -73.142239)],
['http://www.aacsapps.com/domain/55', 0, (42.3222916, -77.738327)],
['http://www.academycharterschool.org/careers', 0, (40.7063185, -73.618684)],
['http://www.achievementfirst.org/schools/new-york-schools/achievement-first-apollo-elementary-school/about', 0, (40.64530975, -73.9550230275334)],
['http://www.achievementfirst.org/schools/new-york-schools/achievement-first-aspire-elementary-school/about', 0, (40.64530975, -73.9550230275334)],
['http://www.achievementfirst.org/schools/new-york-schools/achievement-first-brownsville-elementary-school/about', 0, (40.64530975, -73.9550230275334)],
['http://www.achievementfirst.org/schools/new-york-schools/achievement-first-bushwick-elementary-school/about', 0, (40.64530975, -73.9550230275334)],
['http://www.achievementfirst.org/schools/new-york-schools/achievement-first-crown-heights-elementary-school/about', 0, (40.64530975, -73.9550230275334)],
['http://www.achievementfirst.org/schools/new-york-schools/achievement-first-endeavor-elementary-school/about', 0, (40.64530975, -73.9550230275334)],
['http://www.achievementfirst.org/schools/new-york-schools/achievement-first-linden-elementary-school/about', 0, (40.64530975, -73.9550230275334)],
['http://www.achievementfirst.org/schools/new-york-schools/achievement-first-north-brooklyn-prep-elementary-school/about', 0, (40.64530975, -73.9550230275334)],
['http://www.addisoncsd.org/domain/30', 0, (42.1051571, -77.2340584)],
['http://www.adjcharter.org./employment.html', 0, (42.8867166, -78.8783922)],
['http://www.akronschools.org/Page/5499', 0, (43.0150996, -78.4945500453653)],
['http://www.albanyleadershiphigh.org/community/careers', 0, (42.6511674, -73.754968)],
['http://www.albionk12.org/district/district-office/employment/index', 0, (43.246488, -78.193516)],
['http://www.alcsbronx.org/apps/jobs', 0, (40.9006438, -73.8969749)],
['http://www.alcsny.org/Page/1695', 0, (42.0900647, -78.4941887)],
['http://www.alexandriacentral.org/Page/398', 0, (44.336127, -75.917931)],
['http://www.amanicharter.org/open-positions', 0, (40.9125992, -73.8370786)],
['http://www.amherstschools.org/Page/242', 0, (42.956441, -78.78162)],
['http://www.amityvilleschools.org/departments/human_resources', 0, (40.6789893, -73.4170673)],
['http://www.andescentralschool.org/district/employment', 0, (42.1886976, -74.7857138)],
['http://www.andovercsd.org/Page/131', 0, (42.1564581, -77.7955509)],
['http://www.ardsleyschools.org/Page/277', 0, (41.018219, -73.834564)],
['http://www.argylecsd.org/district/job_opportunities', 0, (43.23795, -73.491669)],
['http://www.ascendlearning.org', 0, (40.64530975, -73.9550230275334)],
['http://www.ascendlearning.org/careers', 0, (40.64530975, -73.9550230275334)],
['http://www.atticacsd.org/Page/23', 0, (42.8642267, -78.2802946)],
['http://www.avcs.org/district-offices/employment-opportunities', 0, (42.748876, -73.8548382490204)],
['http://www.averillpark.k12.ny.us/district-information/job-vacancies', 0, (42.6343578, -73.5537673)],
['http://www.avocacsd.org', 0, (42.4091649, -77.4206245)],
['http://www.avoncsd.org/jobs.cfm', 0, (42.9119925, -77.7454567)],
['http://www.babylon.k12.ny.us/our_district/employment', 0, (40.700182, -73.322722)],
['http://www.bataviacsd.org/Page/574', 0, (42.9980144, -78.1875515)],
['http://www.bathcsd.org/jobs.cfm', 0, (42.3370164, -77.3177577)],
['http://www.bbpschools.org/district_information/human_resources_department', 0, (40.7384317, -73.0506656)],
['http://www.bbschools.org/Employment.aspx', 0, (43.085391, -77.941714)],
['http://www.bcsdk12.org', 0, (44.8205957, -73.5070812)],
['http://www.bcsdny.org/Page/134', 0, (41.1941871, -73.6748116)],
['http://www.beaconcityk12.org/Page/117', 0, (41.4961211, -73.9719299)],
['http://www.bedstuycollegiate.org/bsc/careers', 0, (40.64530975, -73.9550230275334)],
['http://www.belfast.wnyric.org/Page/36', 0, (42.3428443, -78.1113975)],
['http://www.bellmore-merrick.k12.ny.us/district/opportunities', 0, (40.6916154, -73.5635456)],
['http://www.bethpagecommunity.com/district/employment', 0, (40.74336, -73.4838031)],
['http://www.bfcsd.org/apps/spotlightmessages/1776', 0, (44.8075536, -74.773803)],
['http://www.bgligschool.org/apps/jobs', 0, (40.85048545, -73.8404035580209)],
['http://www.bhpanthers.org/Page/1054', 0, (43.809232, -76.024089)],
['http://www.binghamtonschools.org', 0, (42.096968, -75.914341)],
['http://www.blindbrook.org', 0, (41.0192641, -73.6834621)],
['http://www.bloomfieldcsd.org/apps/jobs', 0, (42.8950641, -77.4347128)],
['http://www.bmcsd.org/home/employment-opportunities', 0, (44.830552, -74.513741)],
['http://www.boltoncsd.org', 0, (43.5642373545003, -73.6592186486086)],
['http://www.bpcsd.org/community/employment', 0, (43.0068689, -74.3676437)],
['http://www.brcs.wnyric.org/Page/194', 0, (42.06612, -78.160843)],
['http://www.brcsd.org', 0, (43.8870133, -75.4274083)],
['http://www.briarcliffschools.org/district-information/human-resources', 0, (41.147144, -73.819)],
['http://www.bridgehampton.k12.ny.us/district/employment_opportunities', 0, (40.9378777, -72.3009158)],
['http://www.brighterchoice.org/boys/resources/employment-information', 0, (42.6511674, -73.754968)],
['http://www.brighterchoice.org/girls/resources/career-opportunities', 0, (42.6511674, -73.754968)],
['http://www.brittonkill.k12.ny.us', 0, (42.7284117, -73.6917878)],
['http://www.brockport.k12.ny.us', 0, (43.213671, -77.93918)],
['http://www.broctoncsd.org/Page/1907', 0, (42.379264, -79.468798)],
['http://www.bronxbetterlearning.org', 0, (40.85048545, -73.8404035580209)],
['http://www.bronxcommunity.org', 0, (40.85048545, -73.8404035580209)],
['http://www.brookfieldcsd.org/Page/429', 0, (42.8128488, -75.3176677)],
['http://www.bscsd.org/Page/559', 0, (43.0009087, -73.8490111)],
['http://www.bufsd.org/HTMLpages/Employment/Employment.html', 0, (40.7812093, -73.2462273)],
['http://www.bville.org/teacherpage.cfm?teacher=99', 0, (43.158679, -76.33271)],
['http://www.bwccs2.org', 0, (40.64530975, -73.9550230275334)],
['http://www.cairodurham.org/jobs', 0, (42.2989749, -73.9984659)],
['http://www.cambridgecsd.org/domain/23', 0, (43.0281329, -73.3812231)],
['http://www.camdenschools.org/districtpage.cfm?pageid=1395', 0, (43.334668, -75.747986)],
['http://www.canastotacsd.org', 0, (43.079672, -75.751076)],
['http://www.candorcsd.org/index.php/departments/employment', 0, (42.232902, -76.3424188)],
['http://www.carmelschools.org/groups/6223/personnelpayrollbenefits/employment_opportunities', 0, (41.5117316, -73.604253)],
['http://www.carthagecsd.org', 0, (43.97824, -75.609627)],
['http://www.catomeridian.org/districtpage.cfm?pageid=1350', 0, (43.168123, -76.572999)],
['http://www.cc.cnyric.org/districtpage.cfm?pageid=65', 0, (42.5422923, -75.8957534)],
['http://www.ccs.edu/Page/228', 0, (44.7278943, -73.6686982)],
['http://www.ccsd.edu/domain/999', 0, (41.1469917, -73.9902998)],
['http://www.ccsdk12.org', 0, (44.5956163, -75.1690942)],
['http://www.ccsdli.org/staff_resources/employment', 0, (40.7694091, -73.1148664)],
['http://www.ccsdny.org/domain/8', 0, (42.4614564, -77.7769405)],
['http://www.ccsknights.org', 0, (43.893439, -75.673828)],
['http://www.centermoriches.k12.ny.us/district/employment', 0, (40.8002427, -72.7901318)],
['http://www.centralislip.k12.ny.us', 0, (40.7906538, -73.2017811)],
['http://www.centralqueensacademy.org/careers', 0, (40.7365804, -73.8783932)],
['http://www.centralsquareschools.org/departments.cfm?subpage=20471', 0, (43.286736, -76.146036)],
['http://www.cg.wnyric.org/Page/51', 0, (42.265122, -77.60886)],
['http://www.challengeprepcharter.org/careers', 0, (40.6053825, -73.7551326)],
['http://www.charlottevalleycs.org/district/employment_opportunities', 0, (42.4717451, -74.8446009)],
['http://www.charterschoolofeducationalexcellence.org/apps/pages/index.jsp?uREC_ID=386672&type=d&pREC_ID=879215', 0, (40.9312099, -73.8987469)],
['http://www.chateaugaycsd.org/employment', 0, (44.926648, -74.079781)],
['http://www.chathamcentralschools.com/district/employment', 0, (42.3642517, -73.5948391)],
['http://www.cheektowagacentral.org', 0, (42.9033917, -78.7547536)],
['http://www.chittenangoschools.org', 0, (43.0450671, -75.86658)],
['http://www.chslsj.org/apps/pages/index.jsp?uREC_ID=482551&type=d&pREC_ID=1018626', 0, (40.85048545, -73.8404035580209)],
['http://www.cityschoolofthearts.org', 0, (40.7308619, -73.9871558)],
['http://www.clarenceschools.org/Page/3205', 0, (42.9768372, -78.5930999)],
['http://www.clevehill.wnyric.org/Page/357', 0, (42.9033917, -78.7547536)],
['http://www.cliftonfine.org/cliftonfine.org/district/employment', 0, (44.5906039628011, -75.1542841542162)],
['http://www.clydesavannah.org/district/employment_opportunities', 0, (43.084231, -76.869405)],
['http://www.clymercsd.org/site/Default.aspx?PageID=118', 0, (42.020888, -79.63005)],
['http://www.cmcs.org/news-events/stories/charter-school-countdown', 0, (41.0748189, -73.7751326)],
['http://www.commackschools.org/employment.aspx', 0, (40.8428759, -73.2928943)],
['http://www.copiague.k12.ny.us/our_district/employment', 0, (40.6731835, -73.394809575505)],
['http://www.corningareaschools.com/content/vacai', 0, (42.16396, -77.0937953488168)],
['http://www.cortlandschools.org/teacherpage.cfm?teacher=814', 0, (42.6011813, -76.1804843)],
['http://www.cpcsteam.org/district/employment', 0, (43.950563, -73.43708)],
['http://www.cps.k12.ny.us/departments/oip_employment', 0, (40.7526008, -73.6104058)],
['http://www.crcs.k12.ny.us', 0, (42.677853, -74.4854172)],
['http://www.croton-harmonschools.org', 0, (41.2171115011634, -73.8875568329002)],
['http://www.csh.k12.ny.us/domain/49', 0, (40.8714873, -73.456788)],
['http://www.cvcsd.stier.org', 0, (42.096968, -75.914341)],
['http://www.deerparkschools.org/staff/job_opportunities', 0, (40.7617653, -73.3292858)],
['http://www.delhischools.org', 0, (42.2781401, -74.9159946)],
['http://www.depewschools.org', 0, (42.9022047, -78.6956723)],
['http://www.depositcsd.org', 0, (40.64530975, -73.9550230275334)],
['http://www.deruyter.k12.ny.us/districtpage.cfm?pageid=518', 0, (42.7584005, -75.8843616)],
['http://www.dfsd.org/domain/239', 0, (41.0145418, -73.872635)],
['http://www.dolgeville.org', 0, (43.100983, -74.772949)],
['http://www.doverschools.org/page.cfm?p=5039', 0, (41.7412051, -73.5765151)],
['http://www.dryden.k12.ny.us', 0, (42.4909053, -76.2971553)],
['http://www.dundeecs.org/staff/job_opportunities', 0, (42.5234044, -76.976631)],
['http://www.dunkirkcsd.org', 0, (42.479502, -79.333932)],
['http://www.eastauroraschools.org/domain/56', 0, (42.7689141, -78.6177611)],
['http://www.eastchester.k12.ny.us', 0, (40.9610563, -73.8064739)],
['http://www.easthamptonschools.org/district/employment', 0, (40.7466023, -72.9717159)],
['http://www.eastmeadow.k12.ny.us/our_district/human_resources', 0, (40.7534275, -73.5858684)],
['http://www.eastquogue.k12.ny.us', 0, (40.8406554, -72.5814814)],
['http://www.eastrockawayschools.org/district/employment', 0, (40.6420477, -73.6695747)],
['http://www.ecs.k12.ny.us', 0, (41.7170379, -74.39571)],
['http://www.edencsd.org/Page/10', 0, (42.652282, -78.896979)],
['http://www.edgemont.org/district/human-resources/employment', 0, (40.990605, -73.8082739)],
['http://www.edinburgcs.org/employment-opportunities.html', 0, (43.2217388, -74.1040191)],
['http://www.edmestoncentralschool.net/job-of-the-week', 0, (42.6978509, -75.2437763)],
['http://www.eicsd.k12.ny.us', 0, (43.182942, -77.55297)],
['http://www.eischools.org/district/personnel_services', 0, (40.7504303, -73.1857520086702)],
['http://www.ekcsk12.org/domain/134', 0, (44.467356, -75.230598)],
['http://www.elbacsd.org/domain/47', 0, (43.077282, -78.186962)],
['http://www.ellicottvillecentral.com', 0, (42.2750639, -78.6728071)],
['http://www.elmiracityschools.com', 0, (40.7308619, -73.9871558)],
['http://www.elmontschools.org/Page/381', 0, (40.700936, -73.712909)],
['http://www.elwood.k12.ny.us/departments/human_resources', 0, (40.8686822, -73.362712)],
['http://www.emblazeacademy.org', 0, (40.85048545, -73.8404035580209)],
['http://www.emhcharter.org/careers', 0, (43.1854754, -77.6106861508176)],
['http://www.emoschools.org/Employment.aspx', 0, (40.8050989, -72.7609336)],
['http://www.equalitycharterschool.org/careers', 0, (40.85048545, -73.8404035580209)],
['http://www.ercsd.org/Page/440', 0, (42.3803198, -76.8742707)],
['http://www.erschools.org/departments/employment/employment_opportunities', 0, (43.112157, -77.483559)],
['http://www.esmonline.org', 0, (40.8737096, -72.8078791)],
['http://www.esmschools.org/district.cfm?subpage=24415', 0, (43.0653446, -76.0785332)],
['http://www.evcsbuffalo.org/careers', 0, (42.8867166, -78.8783922)],
['http://www.ewsdonline.org', 0, (40.7561231, -73.6394351)],
['http://www.explorenetwork.org/empower-charter-schoo', 0, (40.64530975, -73.9550230275334)],
['http://www.explorenetwork.org/empower-charter-school', 0, (40.64530975, -73.9550230275334)],
['http://www.explorenetwork.org/exceed-charter-school', 0, (40.7607161, -73.9669623)],
['http://www.explorenetwork.org/explore-charter-school', 0, (40.702197, -73.9964806)],
['http://www.fabiuspompey.org', 0, (42.835067, -75.9860322)],
['http://www.fallsburgcsd.net', 0, (41.7320362, -74.6012711)],
['http://www.farmingdaleschools.org/domain/2290', 0, (40.7328811, -73.4458564)],
['http://www.fi.k12.ny.us/district/employment', 0, (40.6467664, -73.1570589)],
['http://www.fillmorecsd.org/domain/209', 0, (42.466314, -78.116995)],
['http://www.fischool.com', 0, (41.27095945, -71.9839111362531)],
['http://www.floralpark.k12.ny.us/Page/1164', 0, (40.72473015, -73.706479773572)],
['http://www.floridaufsd.org', 0, (41.3317607, -74.35682)],
['http://www.fmschools.org/departments-services/employment', 0, (43.0020107, -75.9768632)],
['http://www.fortannschool.org/district/job_opportunities', 0, (43.414276, -73.487892)],
['http://www.fortedward.org', 0, (43.267206, -73.584709)],
['http://www.forteprep.org', 0, (40.7612123, -73.8651358)],
['http://www.fortplain.org/contact-us/employment', 0, (42.9314616, -74.6226425)],
['http://www.frankfort-schuyler.org/Page/47', 0, (43.032595, -75.070478)],
['http://www.franklinsquare.k12.ny.us', 0, (40.7073244, -73.6759635)],
['http://www.fredonia.wnyric.org/Page/80', 0, (42.440058, -79.331711)],
['http://www.freeportschools.org/district/employment_opportunities', 0, (40.6576022, -73.5831835)],
['http://www.frewsburgcsd.org/domain/146', 0, (42.0545029, -79.1581019)],
['http://www.friendship.wnyric.org/Page/39', 0, (42.2064566, -78.1375099)],
['http://www.frontier.wnyric.org/Page/118', 0, (42.716293, -78.828717)],
['http://www.fultoncsd.org/districtpage.cfm?pageid=119', 0, (43.322846, -76.417159)],
['http://www.galwaycsd.org', 0, (43.0186858, -74.0315162)],
['http://www.gananda.org/apps/jobs', 0, (43.13923, -77.272207)],
['http://www.gblions.org/Page/67', 0, (44.007835, -76.044371)],
['http://www.gcacs.org/District/1765-Job-Opportunities.html', 0, (40.85048545, -73.8404035580209)],
['http://www.gccschool.org', 0, (43.1551169, -77.597215)],
['http://www.gcsk12.org/about-us/employment', 0, (44.336864, -75.463028)],
['http://www.genevacsd.org/Page/285', 0, (42.8773451, -77.0093019)],
['http://www.germantowncsd.org/Page/71', 0, (42.1345339, -73.8917982)],
['http://www.gjrufsd.org', 0, (42.512807, -76.3464675)],
['http://www.glencove.k12.ny.us/staff_resources/employment', 0, (40.862755, -73.6336094)],
['http://www.globalccs.org', 0, (42.81909025, -78.833717479075)],
['http://www.globalcommunitycs.org/careers', 0, (40.8115226, -73.9348399)],
['http://www.gowcsd.org/employment-opportunities', 0, (42.463117, -78.935868)],
['http://www.granvillecsd.org/Page/27', 0, (43.408041, -73.259583)],
['http://www.greatneck.k12.ny.us/Page/3453', 0, (40.8006567, -73.7284647)],
['https://www.applitrack.com/greececsd/onlineapp/default.aspx?all=1', 0, (43.1854754, -77.6106861508176)],
['http://www.greenburgh-graham.org', 0, (40.9915512338856, -73.8759938526594)],
['http://www.greenburgheleven.org/employment.html', 0, (41.0145418, -73.872635)],
['http://www.greenburghnorthcastleschools.com', 0, (41.0156747, -73.8691324)],
['http://www.greenecsd.org', 0, (42.2628769, -74.0878112)],
['http://www.greentechhigh.org/career-opportunities', 0, (42.6511674, -73.754968)],
['http://www.grotoncs.org/districtpage.cfm?pageid=1407', 0, (42.5866943, -76.3666213)],
['http://www.guilderlandschools.org', 0, (42.7020217, -73.9662368)],
['http://www.gwlufsd.org/domain/41', 0, (41.2225932, -74.2943178)],
['http://www.halfhollowhills.k12.ny.us/district/career-opportunities', 0, (40.8175985, -73.3540078)],
['http://www.hamburgschools.org/Page/251', 0, (42.716293, -78.828717)],
['http://www.hamiltoncentral.org/domain/66', 0, (42.8268798, -75.5444159)],
['http://www.hammondsportcsd.org/domain/65', 0, (42.4078495, -77.2235873)],
['http://www.hannibalcsd.org', 0, (43.321179, -76.578834)],
['http://www.harborcharter.org/apps/jobs', 0, (40.7796637, -73.9438435)],
['http://www.harborfieldscsd.net/employment/employment_opportunities', 0, (40.872447, -73.380277)],
['http://www.harlemlink.org/open-positions.html', 0, (40.7308619, -73.9871558)],
['http://www.harrisoncsd.org/index.php/current-job-vacancies/certificated-openings', 0, (40.9689871, -73.71263)],
['http://www.hartfordcsd.org/Page/797', 0, (43.363967, -73.4052888)],
['http://www.hauppauge.k12.ny.us/Page/2668', 0, (40.8256537, -73.2026138)],
['http://www.hbschools.us/district/employment', 0, (40.8689892, -72.5175893)],
['http://www.hccs-nys.org', 0, (40.64530975, -73.9550230275334)],
['http://www.hccs-nys.org', 0, (40.7415369, -73.9571249)],
['http://www.hcks.org/district/human-resources', 0, (41.107636, -73.788188)],
['http://www.hczpromise.org/careers/current-openings', 0, (40.8088437, -73.9658566)],
['http://www.heightsschools.com', 0, (42.1297967, -76.8207898)],
['http://www.heketi.org', 0, (40.85048545, -73.8404035580209)],
['http://www.hempsteadschools.org/Page/120', 0, (40.7063185, -73.618684)],
['http://www.henhudschools.org/domain/1148', 0, (41.252586, -73.93643)],
['http://www.henryjohnsoncs.org', 0, (42.6772173, -73.7818731)],
['http://www.herricks.org/Page/167', 0, (43.483661, -73.6550357117009)],
['http://www.hewlett-woodmere.net', 0, (40.632819, -73.704038)],
['http://www.hfcsd.org', 0, (43.300697, -73.586082)],
['http://www.hffmcsd.org/Page/66', 0, (41.3692605, -73.9662504)],
['http://www.hicksvillepublicschools.org', 0, (40.7668163, -73.5297439785641)],
['http://www.highland-k12.org/Page/23', 0, (41.7209267, -73.9601382)],
['http://www.hinsdalebobcats.org/Page/107', 0, (42.1678436, -78.3872408)],
['http://www.hirebridge.com/jobseeker2/Searchjobresults.asp?cid=5577', 0, (40.85048545, -73.8404035580209)],
['http://www.hlacharterschool.org', 0, (40.64530975, -73.9550230275334)],
['http://www.hlcs.org/?DivisionID=22236&ToggleSideNav=ShowAll', 0, (42.1199356353159, -75.9311278841423)],
['http://www.holland.wnyric.org/Page/32', 0, (42.6411908, -78.5417311)],
['http://www.holleycsd.org/JobOpportunities1.aspx', 0, (43.226806, -78.027155)],
['http://www.honeoye.org/apps/jobs', 0, (42.7908335, -77.5170721)],
['http://www.hoosickfallscsd.org', 0, (42.9011892, -73.3515001)],
['http://www.hoosicvalley.k12.ny.us/district/jobs', 0, (42.9000773, -73.5853939)],
['http://www.horseheadsdistrict.com', 0, (42.167019, -76.8205119)],
['http://www.hpschools.org/Page/1693', 0, (43.241952, -75.257034)],
['http://www.hudsoncityschooldistrict.com/employment', 0, (42.2528649, -73.790959)],
['http://www.hufsd.edu/leadership/hr.html', 0, (40.868154, -73.425676)],
['http://www.hydebronxny.org/careers', 0, (40.85048545, -73.8404035580209)],
['http://www.hydebrooklyn.org', 0, (40.64530975, -73.9550230275334)],
['http://www.icahncharterschool1.org', 0, (40.85048545, -73.8404035580209)],
['http://www.icahncharterschool2.org', 0, (42.6511674, -73.754968)],
['http://www.icahncharterschool3.org', 0, (42.6511674, -73.754968)],
['http://www.icahncharterschool4.org', 0, (42.6511674, -73.754968)],
['http://www.icahncharterschool5.org', 0, (40.85048545, -73.8404035580209)],
['http://www.icahncharterschool6.org', 0, (40.85048545, -73.8404035580209)],
['http://www.icahncharterschool7.org', 0, (40.85048545, -73.8404035580209)],
['http://www.ichabodcrane.org/district/employment', 0, (42.4134168, -73.6731749)],
['http://www.icsnyc.org/careers', 0, (40.6922462, -73.987678)],
['http://www.ilcsd.org', 0, (43.782497, -74.272041)],
['http://www.ips.k12.ny.us/employment_opportunities', 0, (40.6042705, -73.6554078)],
['http://www.ircsd.org/about_i_r_c_s_d/employment_opportunities', 0, (44.154622, -75.708847)],
['http://www.iroquoiscsd.org/domain/12', 0, (42.8510195, -78.640311)],
['http://www.islandtrees.org/districtinformation/employment.htm', 0, (42.6511674, -73.754968)],
['http://www.islipufsd.org/staff/professional_employment_opportunities', 0, (40.7359239, -73.2091231)],
['http://www.jamestownpublicschools.org', 0, (42.0970023, -79.2353259)],
['http://www.jamesvilledewitt.org/employment', 0, (42.9920106, -76.0715887)],
['http://www.jcschools.com/Departments/Personnel/personnel.html', 0, (42.1156308, -75.9588092)],
['http://www.jecsd.org/districtpage.cfm?pageid=1586', 0, (43.0653441, -76.4729927)],
['http://www.jeffersoncs.org/about_j_c_s/district_job_opportunities', 0, (42.4811884, -74.6104276)],
['http://www.johnsburgcsd.org', 0, (43.699899, -73.98571)],
['http://www.jtcsd.org/Page/51', 0, (42.122571, -77.5030413)],
['http://www.jvlwildcat.org', 0, (40.85048545, -73.8404035580209)],
['http://www.k12.ginet.org/Page/932', 0, (43.038715, -78.923017)],
['http://www.kccs.org/employment.html', 0, (42.8867166, -78.8783922)],
['http://www.keenecentralschool.org/about-us/employment', 0, (44.1899781, -73.7862601)],
['http://www.kendallschools.org/district2.cfm?subpage=1169', 0, (43.327281, -78.03585)],
['http://www.kingstoncityschools.org', 0, (41.933663, -74.021045)],
['http://www.kippnyc.org/schools/kipp-amp-elementary', 0, (40.64530975, -73.9550230275334)],
['http://www.kippnyc.org/schools/kipp-infinity-elementary', 0, (40.8088437, -73.9658566)],
['http://www.kippnyc.org/schools/kipp-star-middle-school', 0, (40.8088437, -73.9658566)],
['http://www.kippnyc.org/schools/kipp-washington-heights-middle-school', 0, (40.837405758702, -73.9410333110889)],
['http://www.kipptechvalley.org', 0, (42.6511674, -73.754968)],
['http://www.klschools.org/groups/4498/human_resources/career_opportunities', 0, (41.2614778, -73.5932622)],
['http://www.lacimacharterschool.org', 0, (40.64530975, -73.9550230275334)],
['http://www.lackawannaschools.org', 0, (42.81909025, -78.833717479075)],
['http://www.lafargevillecsd.org/Page/187', 0, (44.197348441484, -75.9510321118575)],
['http://www.lafayetteschools.org/teacherpage.cfm?teacher=247', 0, (42.892289, -76.1052019)],
['http://www.lakelandschools.org/departments/human_resources/employment.php', 0, (41.321675, -73.8296366962619)],
['http://www.lakeshore.wnyric.org/Page/282', 0, (42.650611, -79.061085)],
['http://www.lancasterschools.org/Page/468', 0, (42.9005956, -78.669997)],
['http://www.lansingburgh.org/Page/38', 0, (42.7284117, -73.6917878)],
['http://www.lansingschools.org/districtpage.cfm?pageid=1204', 0, (42.4840418, -76.4779117)],
['http://www.launchschool.org/careers-launch', 0, (40.64530975, -73.9550230275334)],
['http://www.laurenscs.org/Employment.aspx', 0, (42.530633, -75.0896077)],
['http://www.lavelleprep.org', 0, (40.5834557, -74.1496048)],
['http://www.lawrence.org', 0, (40.6156599, -73.7295763)],
['http://www.lbeach.org/departments/opportunities', 0, (40.5867704, -73.616796)],
['http://www.letchworth.k12.ny.us/domain/1056', 0, (42.6408954, -78.1338985)],
['http://www.levittownschools.com/departments/administrative/hr/employment', 0, (40.7241905, -73.5152739674997)],
['http://www.lfcsd.org', 0, (43.0434039, -74.8595958)],
['http://www.libertyk12.org/about-us/employment', 0, (41.8012002, -74.7465527)],
['http://www.lighthouse-academies.org/schools/metropolitan', 0, (40.85048545, -73.8404035580209)],
['http://www.lindenhurstschools.org/our_district/employment', 0, (40.6867667, -73.3734547)],
['http://www.littleflowerufsd.org', 0, (40.9503762, -72.8426016)],
['http://www.liverpool.k12.ny.us/departments/human-resources/job-opportunities', 0, (43.106456, -76.217705)],
['http://www.livoniacsd.org/Page/537', 0, (42.8214525, -77.6686097)],
['http://www.lkgeorge.org/Page/40', 0, (43.404414, -73.7083858)],
['http://www.lockportschools.wnyric.org/Page/194', 0, (43.1490502, -78.6799306)],
['http://www.longlakecsd.org/employment', 0, (43.973052, -74.421043)],
['http://www.longwood.k12.ny.us', 0, (40.8842653, -72.9373262)],
['http://www.lpcsd.org/employment', 0, (44.2817732, -73.9866898)],
['http://www.lpschool.com', 0, (43.497515, -74.361992)],
['http://www.lvcsd.k12.ny.us', 0, (40.8745314, -73.5981168)],
['http://www.lymecsd.org/domain/31', 0, (44.066999, -76.130209)],
['http://www.lynbrookschools.org/departments/personnel_office', 0, (40.6559054, -73.6752222)],
['http://www.lyncourtschool.org/districtpage.cfm?pageid=259', 0, (43.0481221, -76.1474244)],
['http://www.lyndonvillecsd.org', 0, (43.326724, -78.388914)],
['http://www.lyonscsd.org/Page/1374', 0, (43.063803, -76.9839337)],
['http://www.m-ecs.org/departments/business_office/human_resources/vacancy_postings', 0, (42.8986566, -75.6402204)],
['http://www.madisoncentralny.org/domain/176', 0, (42.875882, -75.6802581)],
['http://www.mahopac.k12.ny.us/groups/11079/human_resources/home', 0, (41.372316, -73.733465)],
['http://www.malonecsd.org/employment.html', 0, (44.84881, -74.295044)],
['http://www.malverne.k12.ny.us/district/employment', 0, (40.67555035, -73.6686786894678)],
['http://www.mamkschools.org/district/personnel/employment-opportunities', 0, (40.9539227, -73.7362872)],
['http://www.manhattancharterschool.org', 0, (40.7308619, -73.9871558)],
['http://www.marathonschools.org/job-postings.html', 0, (42.4417391, -76.0321474)],
['http://www.marcellusschools.org/teacherpage.cfm?teacher=816', 0, (42.9556549, -76.3249424)],
['http://www.mayfieldk12.com', 0, (43.104743, -74.265175)],
['http://www.mcgrawschools.org/teacherpage.cfm?teacher=842', 0, (42.5961812, -76.0932597)],
['http://www.mechanicville.org/Page/189', 0, (42.9028547, -73.6873405)],
['http://www.medinacsd.org/Page/761', 0, (43.2160155, -75.4275003344088)],
['http://www.merrick.k12.ny.us/district/job_opportunities', 0, (40.6628796, -73.551516)],
['http://www.merrickacademy.org', 0, (40.678159, -73.746521)],
['http://www.middleburgh.k12.ny.us', 0, (42.598687, -74.3329156)],
['http://www.middletowncityschools.org', 0, (41.4529621, -74.4052974)],
['http://www.midlakes.org/Page/43', 0, (42.9617304, -77.1399757)],
['http://www.mineola.k12.ny.us/district/human_resources', 0, (40.7492678, -73.6406845)],
['http://www.minervasd.org', 0, (43.7714532, -73.9312445)],
['http://www.minisink.com/index.php?id=11', 0, (41.3909274, -74.4765471)],
['http://www.mmcsd.org/Page/19', 0, (42.8853489, -75.1932175)],
['http://www.montaukschool.org/domain/16', 0, (41.0482141, -71.9532344633105)],
['http://www.moraviaschool.org/teacherpage.cfm?teacher=1831', 0, (42.7125702, -76.4216025)],
['http://www.moriahk12.org/employment.html', 0, (44.048609, -73.45974)],
['http://www.morriscs.org', 0, (42.5486871, -75.2451685)],
['http://www.mpbschools.org', 0, (41.0748189, -73.7751326)],
['http://www.mpcsny.org', 0, (41.1328736, -73.7926335)],
['http://www.msd.k12.ny.us/domain/33', 0, (40.6806564, -73.4742914)],
['http://www.mtmorriscsd.org', 0, (42.5486871, -75.2451685)],
['http://www.mtplcsd.org', 0, (41.1234293, -73.7790218)],
['http://www.mtsinai.k12.ny.us/our_district/employment/employment.html', 0, (40.9470432, -73.0295495)],
['http://www.mtvernoncsd.org', 0, (40.9125992, -73.8370786)],
['http://www.mufsd.com/departments/human_resources/job_postings', 0, (41.0106563, -72.4850859)],
['http://www.mwcsk12.org', 0, (44.750391, -75.131378)],
['http://www.nacs1.org/cms/One.aspx?portalId=465963&pageId=1327562', 0, (44.9058729, -73.8009813)],
['http://www.naplescsd.org/districtpage.cfm?pageid=550', 0, (42.6160647, -77.4030253)],
['http://www.nccscougar.org/Page/29', 0, (44.986656, -73.446693)],
['http://www.ndchsbrooklyn.org/careers', 0, (40.689631, -73.985739)],
['http://www.newark.k12.ny.us/Page/455', 0, (43.0467301, -77.0952516)],
['http://www.newburghschools.org/page.php?page=7', 0, (41.5034271, -74.0104179)],
['http://www.newfane.wnyric.org/page/24', 0, (43.286723, -78.710312)],
['http://www.newfieldschools.org', 0, (42.3621811, -76.5905632)],
['http://www.newhartfordschools.org/Page/2553', 0, (43.073653, -75.287933)],
['http://www.newheightsacademy.org', 0, (40.8253151597687, -73.9483580840834)],
['http://www.newlebanoncsd.org/district/employment', 0, (42.4639722, -73.3964977)],
['http://www.newpaltz.k12.ny.us/domain/10', 0, (41.7464972, -74.0844894)],
['http://www.newsuffolkschool.com', 0, (40.9914896, -72.475919)],
['http://www.newvisions.org/charter', 0, (40.7308619, -73.9871558)],
['http://www.newvisions.org/charter/humii', 0, (40.85048545, -73.8404035580209)],
['http://www.newvisions.org/pages/careers', 0, (40.6914852, -73.8056771)],
['http://www.newvisions.org/schools/entry/ams3', 0, (40.64530975, -73.9550230275334)],
['http://www.newvisions.org/schools/entry/amsii', 0, (40.85048545, -73.8404035580209)],
['http://www.newvisions.org/schools/entry/hum3', 0, (40.64530975, -73.9550230275334)],
['http://www.newvisions.org/schools/entry/humanities-iv', 0, (40.5805104, -73.8361535)],
['http://www.newworldprep.org', 0, (40.645349, -74.0929616)],
['http://www.newyorkcharters.org/about/employment-opportunities', 0, (42.6511674, -73.754968)],
['http://www.newyorkmills.org/Page/30', 0, (43.105495, -75.291367)],
['http://www.nhp-gcp.org/domain/63', 0, (40.73071865, -73.6812564655372)],
['http://www.niagaracharter.org', 0, (43.1030928, -79.0302618)],
['http://www.nncsk12.org/Page/36', 0, (44.75161, -74.994392)],
['http://www.northbabylonschools.net/our_district/employment_opportunities', 0, (40.7164881, -73.3217861)],
['http://www.northbellmoreschools.org/Page/1544', 0, (40.6540805, -73.5285878127105)],
['http://www.northgreenbushcommon.org', 0, (42.7284117, -73.6917878)],
['http://www.northsalemschools.org/Page/2807', 0, (41.3348169, -73.5712374)],
['http://www.northsidechs.org', 0, (40.64530975, -73.9550230275334)],
['http://www.northwarren.k12.ny.us/Employment.html', 0, (43.6764553, -73.7495703)],
['http://www.nrcsd.org/hr', 0, (41.2017613, -73.9943068)],
['http://www.nred.org/groups/17143/human_resources/human_resources', 0, (40.9114459, -73.7841684271834)],
['http://www.nrwcs.org/domain/38', 0, (43.2317547, -76.820325)],
['http://www.nscsd.org', 0, (43.1756235, -76.1193678)],
['http://www.nvcs.stier.org', 0, (42.2236853, -76.183263)],
['http://www.nyackschools.org/groups/6169/human_resources/home', 0, (41.0906519, -73.9179146)],
['http://www.nycacharterschool.org/careers', 0, (40.7796637, -73.9438435)],
['http://www.nycautismcharterschool.org/careers', 0, (40.7796637, -73.9438435)],
['http://www.ocs.cnyric.org/district.cfm?subpage=3520', 0, (42.9750662, -76.1413133)],
['http://www.odyoungcsd.org/Page/79', 0, (42.8950724, -74.8276495)],
['http://www.oesj.org', 0, (42.9981274, -74.6829225)],
['http://www.ogdensburgk12.org/domain/1035', 0, (44.694285, -75.486374)],
['http://www.omschools.org/employment.cfm', 0, (42.3367406, -76.7885655)],
['http://www.oneidacsd.org', 0, (43.2144051, -75.4039155)],
['http://www.opportunitycharter.org', 0, (40.7308619, -73.9871558)],
['http://www.opschools.org/Page/125', 0, (42.811242, -78.713679)],
['http://www.oriskanycsd.org/Page/663', 0, (43.156049, -75.330749)],
['http://www.oswego.org/personnel', 0, (43.4547284, -76.5095967)],
['http://www.ovcs.org', 0, (42.6358870995644, -75.7757315906073)],
['http://www.owncs.org/about/employment', 0, (40.7720145, -73.9302673)],
['http://www.oysterponds.org', 0, (41.1389875, -72.303415)],
['http://www.palmaccsd.org/Content2/286', 0, (43.0623754, -77.2347245)],
['http://www.pancent.org/Page/27', 0, (42.075056, -79.483105)],
['http://www.pavilioncsd.org', 0, (42.8761722, -78.0227877)],
['http://www.pawlingschools.org', 0, (41.5620381, -73.6026271)],
['http://www.pbcschools.org/districtpage.cfm?pageid=1512', 0, (43.0345099, -76.6238343)],
['http://www.pearlriver.org/groups/55638/human_resources/employment_opportunities', 0, (41.0586333, -74.0218967)],
['http://www.pelhamschools.org', 0, (40.9098215, -73.8079111)],
['http://www.pembrokecsd.org', 0, (42.9600595, -78.4055767)],
['http://www.peninsulaprep.org', 0, (40.6053825, -73.7551326)],
['http://www.perry.k12.ny.us/Page/140', 0, (42.7156175, -78.0055618)],
['http://www.perucsd.org/Page/1822', 0, (44.578486, -73.527031)],
['http://www.phoenixcsd.org/Page/1053', 0, (43.231179, -76.300764)],
['http://www.pioneerschools.org/domain/48', 0, (42.524986, -78.464228)],
['http://www.pisecoschool.com', 0, (43.4484024, -74.518484)],
['http://www.pittsfordschools.org/Page/928', 0, (43.090959, -77.515298)],
['http://www.plainedgeschools.org/administration/office_of_human_resources/employment_opportunities', 0, (40.6806564, -73.4742914)],
['http://www.plattscsd.org/district/human-resources/employment-opportunities', 0, (44.69282, -73.45562)],
['http://www.pleasantvilleschools.com', 0, (41.1328736, -73.7926335)],
['http://www.pocanticohills.org/human_resources', 0, (41.0762077, -73.8587461)],
['http://www.polandcs.org/domain/270', 0, (43.225693, -75.06134)],
['http://www.portchesterschools.org/employment__job_postings', 0, (41.0192641, -73.6834621)],
['http://www.portjeff.k12.ny.us', 0, (40.9464875, -73.0692732)],
['http://www.portjerviscsd.k12.ny.us/departments/employment-opportunities', 0, (41.3750937, -74.692663)],
['http://www.portville.wnyric.org', 0, (42.0386764, -78.3408496)],
['http://www.potsdam.k12.ny.us/apps/pages/index.jsp?uREC_ID=747176&type=d&pREC_ID=1248094', 0, (44.6752342, -74.9860333)],
['http://www.ppcsd.org/Employment', 0, (41.9798143, -73.6559602)],
['http://www.publicprep.org/careers', 0, (40.8283807, -73.9270844)],
['http://www.pulaskicsd.org/districtpage.cfm?pageid=511', 0, (43.567014, -76.127703)],
['http://www.putnamcsd.org/employment.html', 0, (43.7342291, -73.3748383)],
['http://www.pval.org/Page/20', 0, (42.364227, -79.055595)],
['http://www.randolphacademy.org', 0, (42.162005, -78.975317)],
['http://www.randolphcsd.org/domain/24', 0, (42.163729, -78.969094)],
['http://www.rcacs.org', 0, (40.678713, -73.5890168)],
['http://www.rccsd.org/apps/jobs', 0, (43.247289, -76.723564)],
['http://www.rcsd.k12.ny.us/district/employment', 0, (42.7091389, -73.5107732)],
['http://www.redhookcentralschools.org', 0, (41.9950819, -73.8755918)],
['http://www.remsencsd.org/Page/1050', 0, (43.327176, -75.186996)],
['http://www.renaissancecharter.org', 0, (40.7556561, -73.8857755)],
['http://www.rhinebeckcsd.org/pagecontent.php?id=69', 0, (41.9268754, -73.9126639)],
['http://www.richfieldcsd.org/Page/442', 0, (42.8534057, -74.9854335)],
['http://www.riverhead.net/district/employment', 0, (40.8256537, -73.2026138)],
['http://www.rocachieve.org', 0, (43.1635257, -77.6083784825996)],
['http://www.rockypointschools.org', 0, (40.9525987, -72.9253805)],
['http://www.romecsd.org', 0, (43.2128473, -75.4557304)],
['http://www.rondout.k12.ny.us', 0, (41.7856489, -74.2290366)],
['http://www.roscoe.k12.ny.us/Page/88', 0, (41.92625995, -74.8643013730444)],
['http://www.roxburycs.org', 0, (42.2839739, -74.5648747)],
['http://www.royhart.org/Page/269', 0, (43.212301, -78.476563)],
['http://www.rvcschools.org/departments_and_programs/personnel/employment_opportunities', 0, (40.6574186, -73.6450664)],
['http://www.ryeneck.k12.ny.us', 0, (40.9539227, -73.7362872)],
['http://www.sachem.k12.ny.us/district/employment_opportunities', 0, (40.8237106, -73.1075598)],
['http://www.sacketspatriots.org/our_district/employment_opportunities', 0, (43.946171, -76.119093)],
['http://www.sacsny.com/careers', 0, (40.64530975, -73.9550230275334)],
['http://www.sagaponackschool.com', 0, (40.9253776, -72.2781375)],
['http://www.sagharborschools.org', 0, (40.9978727, -72.2922292)],
['http://www.salamancany.org', 0, (42.158583, -78.736381)],
['http://www.salemcsd.org', 0, (43.1722983, -73.3276101)],
['http://www.sascs.org', 0, (43.0481221, -76.1474244)],
['http://www.schenectady.k12.ny.us', 0, (42.8142432, -73.9395687)],
['http://www.schenevuscsd.org/EmploymentOpportunities.aspx', 0, (42.5489657, -74.8209875)],
['http://www.schodack.k12.ny.us/district/employment', 0, (42.2528649, -73.790959)],
['http://www.schoharie.k12.ny.us', 0, (42.5757217, -74.4390277)],
['http://www.schroonschool.org/?page_id=30', 0, (43.8386732, -73.7609635)],
['http://www.scio.wnyric.org/districtpage.cfm?pageid=334', 0, (42.1714573, -77.9786147)],
['http://www.seaford.k12.ny.us', 0, (40.6659344, -73.4881809)],
['http://www.sewanhaka.k12.ny.us', 0, (40.72473015, -73.706479773572)],
['http://www.sfcs.k12.ny.us/Page/4406', 0, (42.910622, -76.7966215)],
['http://www.shelterisland.k12.ny.us/domain/104', 0, (41.0645437, -72.3328604)],
['http://www.shufsd.org/district/employment', 0, (40.8534318, -73.4115091)],
['http://www.silvercreekschools.org', 0, (42.5160058, -79.1461454)],
['http://www.sisuluwalker.org/employment-listings', 0, (40.7308619, -73.9871558)],
['http://www.skanschools.org/districtpage.cfm?pageid=363', 0, (42.947011, -76.4291017)],
['http://www.skcs.org/Employment.aspx', 0, (42.3423047, -74.7170994)],
['http://www.slcs.org/district-office/employment-applications', 0, (44.329497, -74.131279)],
['http://www.sloanschools.org/Page/639', 0, (42.895461, -78.794062)],
['http://www.smithtown.k12.ny.us/district/district_documents', 0, (40.8559314, -73.2006687)],
['http://www.solvayschools.org/districtpage.cfm?pageid=346', 0, (43.0581222, -76.2074263)],
['http://www.somersschools.org/Page/3984', 0, (41.3281498, -73.6856857)],
['http://www.southamptonschools.org/Page/56', 0, (40.884267, -72.3895296)],
['http://www.southbronxcommunity.org/employment', 0, (40.85048545, -73.8404035580209)],
['http://www.southbuffalocs.org/domain/6', 0, (42.8867166, -78.8783922)],
['http://www.southcountry.org/departments/employment_opportunities', 0, (40.7670427, -72.9962189)],
['http://www.southerncayuga.org', 0, (42.7539591, -76.7024485)],
['https://www.southlewis.org/employment-opportunities--163', 0, (43.627378, -75.41153)],
['http://www.southseneca.com/districtpage.cfm?pageid=780', 0, (42.6764593, -76.8230111)],
['http://www.spackenkillschools.org/departments/human_resources', 0, (41.7065779, -73.9284101)],
['http://www.spartanpride.org/districtpage.cfm?pageid=1729', 0, (43.809232, -76.024089)],
['http://www.spencerportschools.org/departments_and_programs/human_resources/JobOpportunities', 0, (43.18645, -77.803897)],
['http://www.springsschool.org/district/employment', 0, (40.9649335, -72.1935296987861)],
['http://www.springvillegi.org/available-positions', 0, (42.5083952, -78.6672482)],
['http://www.srk12.org', 0, (44.989033, -74.494262)],
['http://www.stamfordcs.org/Employment.aspx', 0, (42.4073024, -74.614318)],
['http://www.starpointcsd.org/Page/42', 0, (43.168863, -78.6929557832681)],
['http://www.sthopeleadershipacademy.org/apps/jobs', 0, (40.8180784688337, -73.9431029124958)],
['http://www.stockbridgevalley.org', 0, (42.977013, -75.586846)],
['http://www.successacademies.org/schools/bushwick', 0, (40.64530975, -73.9550230275334)],
['http://www.successacademies.org/schools/far-rockaway', 0, (40.6524927, -73.7914214158161)],
['http://www.successacademies.org/schools/flatbush', 0, (40.6501038, -73.9495823)],
['http://www.successacademies.org/schools/hudson-yards', 0, (40.7308619, -73.9871558)],
['http://www.successacademies.org/schools/south-jamaica', 0, (40.6914852, -73.8056771)],
['http://www.sufferncentral.org/human-resources', 0, (42.6511674, -73.754968)],
['http://www.svcsd.org', 0, (43.0042365, -75.2598859)],
['http://www.svecsd.org', 0, (42.2097963, -76.4932748)],
['http://www.svsabers.org/EmploymentOpportunities.aspx', 0, (42.0342437, -75.803801)],
['http://www.swcsd.org/Page/194', 0, (41.7809217, -74.9337755)],
['http://www.swrschools.org/our_district/employment', 0, (40.9573208, -72.9076025)],
['http://www.syosset.k12.ny.us/district/employment_information', 0, (40.8262101, -73.502068)],
['http://www.taconichills.k12.ny.us/site/Default.aspx?PageID=193', 0, (42.1748115, -73.5828976)],
['http://www.tbafcs.org/Page/1444', 0, (42.3370091, -78.4580762)],
['http://www.tbcsc.org/english/join-the-bcsc-team', 0, (40.85048545, -73.8404035580209)],
['http://www.tburgschools.org/districtpage.cfm?pageid=433', 0, (42.5422939, -76.6660589)],
['http://www.tepcharter.org', 0, (40.8539389847281, -73.9318135025059)],
['http://www.tfoaprofessionalprep.org', 0, (40.64530975, -73.9550230275334)],
['http://www.theamericandreamschool.org', 0, (40.85048545, -73.8404035580209)],
['http://www.thewcs.org/employment.php', 0, (40.64530975, -73.9550230275334)],
['http://www.ticonderogak12.org/Employment', 0, (43.848889, -73.423347)],
['http://www.tiogacentral.org', 0, (42.0561854, -76.3479918)],
['http://www.tonawandacsd.org/Page/39', 0, (42.991733, -78.8824886119079)],
['http://www.towschool.org/our_district/employment_opportunities', 0, (43.7100676, -74.9743407)],
['http://www.troycsd.org/district-services/human-resources', 0, (42.7284117, -73.6917878)],
['http://www.tuckahoeschools.org/employment_opportunities', 0, (40.9610563, -73.8064739)],
['http://www.tufsd.org/Page/49', 0, (40.905093, -73.896435)],
['http://www.tupperlakecsd.net', 0, (44.224044, -74.464302)],
['http://www.tuxedoufsd.org', 0, (41.1982440035408, -74.21294327586)],
['http://www.uascs.org/index.php/careers', 0, (43.038959, -75.070436)],
['http://www.uek12.org/Employment.aspx', 0, (42.098408, -76.0493684)],
['https://www.unatego.org/Employment.aspx', 0, (42.3973023, -75.1735017)],
['http://www.unionspringscsd.org/districtpage.cfm?pageid=193', 0, (42.8397906, -76.6932818)],
['http://www.unityprep.org/careers/teaching-at-unity', 0, (40.64530975, -73.9550230275334)],
['http://www.upreprochester.org', 0, (43.1854754, -77.6106861508176)],
['http://www.uvstorm.org/EmploymentOpportunities.aspx', 0, (42.6239023, -75.3321363)],
['http://www.valhallaschools.org', 0, (41.0339862, -73.7629097)],
['http://www.valleystream30.com/our_district/employmentcareers', 0, (40.6715969, -73.6982991)],
['http://www.valleystreamdistrict24.org/employment-opportunities-1.html', 0, (40.657709, -73.6896071)],
['http://www.vcsd.k12.ny.us/Page/114', 0, (42.8941269, -74.4099745)],
['http://www.vertusschool.org/careers', 0, (43.1742152222803, -77.5608675908798)],
['http://www.vestal.stier.org/CurrentVacancies.aspx', 0, (42.0850747, -76.053813)],
['http://www.voicecharterschool.org', 0, (40.7415369, -73.9571249)],
['http://www.voorheesville.org/domain/40', 0, (42.653967, -73.9287366)],
['http://www.vschsd.org/district/employment', 0, (40.6631362, -73.7056955)],
['http://www.vvsschools.org/domain/16', 0, (43.138322, -75.570831)],
['http://www.wacs.wnyric.org/Page/1330', 0, (42.32228, -79.578103)],
['http://www.wainscottschool.org', 0, (40.9367664, -72.2428587)],
['http://www.wajcs.org/?PageName=bc&n=246209', 0, (42.3073066, -74.2520875)],
['http://www.wallkillcsd.k12.ny.us/domain/258', 0, (41.6056492, -74.1840358)],
['http://www.waltoncsd.org', 0, (42.1695296, -75.1293351)],
['http://www.wantaghschools.org/domain/956', 0, (40.6837121, -73.5101258)],
['http://www.wappingersschools.org', 0, (41.5839824, -73.8087442)],
['http://www.warsaw.k12.ny.us/Page/358', 0, (42.7401871, -78.1325548)],
['http://www.watervillecsd.org/site/default.aspx?pageid=1', 0, (42.931181, -75.3798924)],
['http://www.wboro.org/Page/32', 0, (43.122036, -75.29171)],
['http://www.wbschools.org/District/employment_opportunities', 0, (40.718155, -73.3542871)],
['http://www.wccsk12.org', 0, (42.5678449, -77.5897139)],
['http://www.wcsd.org/district/employment_opportunities', 0, (43.496768, -73.776283)],
['http://www.web.milfordcentral.org/district/job_opportunities', 0, (42.5906322, -74.9451573)],
['http://www.websterschools.org', 0, (43.263428, -77.4334757)],
['http://www.weedsport.org', 0, (43.048677, -76.5627197)],
['http://www.wellscsd.org/district-information/employment-opportunities', 0, (43.396067, -74.289894)],
['http://www.wellsville.wnyric.org/Page/279', 0, (42.1194172, -77.9452697)],
['http://www.westburyschools.org', 0, (40.7887113, -73.5995717)],
['http://www.westcanada.org/domain/93', 0, (43.185904, -75.014648)],
['http://www.westhamptonbeach.k12.ny.us/district/employment', 0, (40.8102203, -72.6430174)],
['http://www.westhillschools.org/teacherpage.cfm?teacher=448', 0, (43.0481221, -76.1474244)],
['http://www.westminsterccs.org/careers', 0, (42.8867166, -78.8783922)],
['http://www.westmorelandschool.org/Page/1867', 0, (43.1070992876963, -75.4351414037091)],
['http://www.westportcs.org/Page/55', 0, (44.1871187, -73.4518977971491)],
['http://www.wfsd.k12.ny.us/index.php/employment-opportunities', 0, (40.7667655, -72.8520476)],
['http://www.wgcsd.org/employment.cfm', 0, (42.0897965, -76.8077338)],
['http://www.whitesville.wnyric.org/domain/91', 0, (42.0378463, -77.7624938)],
['http://www.whufsd.com/district/human_resources', 0, (40.7048242, -73.6501295)],
['http://www.whufsd.org', 0, (42.7925778, -73.6812293)],
['http://www.wi.k12.ny.us/district/office_of_human_resources', 0, (40.7058564, -73.3077301)],
['http://www.williamsvillek12.org/departments/human_resources/career_opportunities.php', 0, (43.0183913, -78.696697)],
['http://www.willsborocsd.org/district/employment', 0, (44.357488, -73.392105)],
['http://www.worcestercs.org/employment-opportunities.html', 0, (42.5914958, -74.7503896)],
['http://www.wufsk8.com', 0, (43.137849, -74.4812516)],
['http://www.wvalley.wnyric.org/Page/159', 0, (42.402841, -78.6100253)],
['http://www.wyandanch.k12.ny.us', 0, (40.7539878, -73.360398)],
['http://www.wynantskillufsd.org/district/employment', 0, (42.7284117, -73.6917878)],
['http://www.yalowcharter.org/jobs', 0, (40.8458811912444, -73.8409497112859)],
['http://www.yonkerspublicschools.org/Page/1191', 0, (40.9312099, -73.8987469)],
['http://www.yorkcsd.org/Page/65', 0, (42.83534, -77.878894)],
['http://www1.homercentral.org/district/employment', 0, (42.6370141, -76.1788174)],
['https://ambercharter.tedk12.com/hire/index.aspx', 0, (40.7796637, -73.9438435)],
['https://ats1.searchsoft.net/ats/app_login.shtml?COMPANY_ID=00004834', 0, (40.778762, -73.466634)],
['https://auburn.tedk12.com/hire/index.aspx', 0, (47.3075369, -122.2301808)],
['https://boards.greenhouse.io/bsnbcscareers', 0, (40.64530975, -73.9550230275334)],
['https://boards.greenhouse.io/eastharlemtutorialprogram', 0, (40.7796637, -73.9438435)],
['https://boldschools.org/careers', 0, (40.85048545, -73.8404035580209)],
['https://broomestreetacademy.org/careers', 0, (40.7308619, -73.9871558)],
['https://buffsci.org/our-school', 0, (42.6511674, -73.754968)],
['https://careers-ascendlearning.icims.com/jobs/search?ss=1&hashed=-435681916', 0, (40.64530975, -73.9550230275334)],
['https://careers.smartrecruiters.com/UncommonSchools', 0, (40.64530975, -73.9550230275334)],
['https://careers.wearedream.org/careers', 0, (40.7796637, -73.9438435)],
['https://catskillcsd.org/employment', 0, (42.2173102, -73.8645734)],
['https://cazenoviacsd.com/homes/staff-resources/employment-opportunities', 0, (42.9300668, -75.8526915)],
['https://ccrsk12.org/opportunities', 0, (44.889931, -73.43605)],
['https://delhi.interviewexchange.com/static/clients/409SDM1/index.jsp;jsessionid=617C89830CE8E53BF77CF8B7589D5895;jsessionid=0332E7A4D070E2A91EFCC6FF4283BD74', 0, (42.2781401, -74.9159946)],
['https://docs.google.com/document/d/1QZP04N1Yi1bssffXJhoEJn1gSsq7kw7-ib4YvGHHvuY', 0, (40.6387141, -73.6401296)],
['https://docs.google.com/document/d/1eLpsys_UJnYhr6pnwzJEBeBmbty9d4ztz0i3i5bGmP4/edit?usp=sharing', 0, (44.553292, -74.939804)],
['https://excellence-community-schools.workable.com', 0, (40.85048545, -73.8404035580209)],
['https://havenacademy.org/join-us/employment-opportunities', 0, (40.804696, -73.922387)],
['https://hebrewpublic.org/careers-at-hebrew-public', 0, (40.7308619, -73.9871558)],
['https://hlacharterschool.org', 0, (40.64530975, -73.9550230275334)],
['https://inwoodacademy.org/careers/openings', 0, (40.8728056, -73.9116935)],
['https://jobs.lever.co/drihscs', 0, (40.85048545, -73.8404035580209)],
['https://jobs.schoolsites.com/CCCSD/jobs.cfm', 0, (43.090959, -77.515298)],
['https://jobs.successacademies.org', 0, (40.64530975, -73.9550230275334)],
['https://ncschools.org/about-ncs/careers-at-ncs', 0, (40.8253151597687, -73.9483580840834)],
['https://newrootsschool.org/employment-opportunities', 0, (42.4396039, -76.4968019)],
['https://ossiningufsd.org/departments/human-resources', 0, (41.1613168, -73.8620367)],
['https://paveschools.org', 0, (40.64530975, -73.9550230275334)],
['https://platform.teachermatch.org/jobsboard.do?districtId=264888318', 0, (43.0481221, -76.1474244)],
['https://plus.google.com/s/%23Employment/posts', 0, (43.969592, -74.164925)],
['https://recruiting.paylocity.com/recruiting/jobs/List/2903/Harriet-Tubman-Charter-School', 0, (40.85048545, -73.8404035580209)],
['https://renacad.org/contact/employment', 0, (43.1854754, -77.6106861508176)],
['https://rew11.ultipro.com/BER1014/JobBoard/listjobs.aspx', 0, (42.4118426, -73.4496088)],
['https://riverheadcharterschool.org/join-us/careers-at-riverhead', 0, (40.9064873, -72.7434331)],
['https://sbecacs.org/careers', 0, (40.85048545, -73.8404035580209)],
['https://www.falconercsd.org/Page/4747', 0, (42.11867, -79.19838)],
['https://www.swcsk12.org/Page/19', 0, (42.0970023, -79.2353259)],
['https://sites.google.com/a/northvillecsd.org/ncsd/home/district/community/local-job-postings', 0, (43.226193, -74.172478)],
['https://sites.google.com/htcschools.org/htcemployment/home', 0, (42.1956438, -74.1337508)],
['https://stradfordprep.org', 0, (40.7308619, -73.9871558)],
['https://tapestryschool.org/about-tapestry/careers', 0, (42.8867166, -78.8783922)],
['https://tech.dcboces.org/recruitment/posting/browse_all.php', 0, (41.7865038, -73.6921867)],
['https://udteam.org/employment', 0, (40.64530975, -73.9550230275334)],
['https://uncommonschools.secure.force.com/careers', 0, (40.64530975, -73.9550230275334)],
['https://urbanassembly.org/career', 0, (40.7308619, -73.9871558)],
['https://urbanchoicecharter.org/employment', 0, (43.1399713, -77.5524612)],
['https://www.abewing.org/aws', 0, (43.309941, -73.644447)],
['https://www.achievementfirst.org/careers', 0, (40.64530975, -73.9550230275334)],
['https://www.achievementfirst.org/schools/new-york-schools', 0, (40.64530975, -73.9550230275334)],
['https://www.adirondackcsd.org/welcome/employment_opportunities', 0, (43.4843153, -75.3357941)],
['https://www.aftoncsd.org/Employment1.aspx', 0, (42.2346546272836, -75.5425340462906)],
['https://www.albanyschools.org/employment/index.html', 0, (42.6511674, -73.754968)],
['https://www.alexandercsd.org/apps/pages/index.jsp?uREC_ID=887506&type=d&pREC_ID=1238008', 0, (42.9011711, -78.2566834)],
['https://www.applitrack.com/caboces/onlineapp/default.aspx?choosedistrict=true&applitrackclient=38921', 0, (42.2175668, -78.2752927)],
['https://www.applitrack.com/fairportcsd/onlineapp/default.aspx?all=1', 0, (43.0993, -77.443014)],
['https://www.applitrack.com/gateschili/onlineapp/default.aspx?all=1', 0, (43.157285, -77.615214)],
['https://www.applitrack.com/hohschools/onlineapp/default.aspx?all=1', 0, (40.9915512338856, -73.8759938526594)],
['https://www.applitrack.com/honeoye/onlineapp/default.aspx?all=1', 0, (42.9519038, -77.5914322)],
['https://www.applitrack.com/oacsd/onlineapp/default.aspx?all=1', 0, (42.1034075, -76.2621549)],
['https://www.applitrack.com/penfield/onlineapp/default.aspx?all=1', 0, (43.1301133, -77.4759588)],
['https://www.applitrack.com/rhcsd/onlineapp/default.aspx?all=1', 0, (43.059192, -77.625922)],
['https://www.applitrack.com/saugertiesk12/onlineapp/jobpostings/view.asp?all=1', 0, (42.0775906, -73.9529126)],
['https://www.applitrack.com/sidney/onlineapp/default.aspx?all=1', 0, (42.3157824, -75.392776)],
['https://www.applitrack.com/watertowncsd/onlineapp/default.aspx?all=1', 0, (43.9747838, -75.9107565)],
['https://www.applitrack.com/wheatlandchili/onlineapp/default.aspx?all=1', 0, (43.0258957, -77.7452826)],
['https://www.applitrack.com/yorktown/onlineapp/default.aspx?all=1', 0, (41.2709274, -73.7776336)],
['https://www.apwschools.org/Page/1083', 0, (43.406181, -76.125758)],
['https://www.arkportcsd.org/Page/121', 0, (42.6511674, -73.754968)],
['https://www.atmosphereacademy.org/contact-us/careers/current-openings', 0, (40.85048545, -73.8404035580209)],
['https://www.aufsd.org/Page/93', 0, (40.9844862, -72.1322676993658)],
['https://www.barkercsd.net/Page/3945', 0, (43.330334, -78.554531)],
['https://www.bayshoreschools.org/jobs.cfm', 0, (40.72508825, -73.253032759713)],
['https://www.belahs.org', 0, (40.64530975, -73.9550230275334)],
['https://www.bethlehemschools.org/employment', 0, (42.6220235, -73.8326232)],
['https://www.bgcsd.org/Employment.aspx', 0, (42.2935152, -75.4792592)],
['https://www.bkwschools.org/employment', 0, (42.6253546, -74.1334647)],
['https://www.bradfordcsd.org/our-school/employment', 0, (42.3711837, -77.1088596)],
['https://www.brewsterschools.org/departments/humanresources/employment', 0, (41.3973335, -73.6171915)],
['https://www.bronxbetterlearning.org', 0, (40.85048545, -73.8404035580209)],
['https://www.bronxvilleschool.org', 0, (40.9366426, -73.8314989)],
['https://www.brooklyncharter.org/about/employment', 0, (40.64530975, -73.9550230275334)],
['https://www.brooklynlaboratoryschool.org/careers', 0, (40.64530975, -73.9550230275334)],
['https://www.buffalocollegiate.org/careers', 0, (42.8867166, -78.8783922)],
['https://www.byramhills.org/departments/human-resources/career-opportunities', 0, (41.1264849, -73.7140195)],
['https://www.cacsd.org/domain/188', 0, (42.3509179, -73.8029028)],
['https://www.canajoharieschools.org/employment', 0, (42.9056288, -74.5718073)],
['https://www.capitalregionboces.org/employment/job-openings', 0, (42.7742446, -73.7001187)],
['https://www.cattlv.wnyric.org/Page/20', 0, (42.2234823, -78.6477096)],
['https://www.ccsd.ws', 0, (41.1595399, -73.764855)],
['https://www.cforks.org/Employment.aspx', 0, (42.096968, -75.914341)],
['https://www.clake.org/District/1748-Untitled.html', 0, (42.253947, -79.504491)],
['https://www.communityroots.org/apps/pages/index.jsp?uREC_ID=279770&type=d&pREC_ID=632492', 0, (40.64530975, -73.9550230275334)],
['https://www.cooperstowncs.org/o/cooperstown-csd/page/employment-information--13', 0, (42.7006303, -74.924321)],
['https://www.corinthcsd.org/employment-opportunities', 0, (43.241933, -73.831796)],
['https://www.cornwallschools.com/apps/pages/index.jsp?uREC_ID=310699&type=d&termREC_ID=&pREC_ID=577553', 0, (41.445791, -74.028788)],
['https://www.cpcsschool.org/careers', 0, (40.64530975, -73.9550230275334)],
['https://www.creoprep.org/careers', 0, (40.7308619, -73.9871558)],
['https://www.csat-k12.org/Page/1829', 0, (42.9612808, -78.8933608)],
['https://www.cvalleycsd.org/human-resources', 0, (43.0150703, -75.0354347)],
['https://www.cvscs.org/EmploymentOpportunities.aspx', 0, (42.7956295, -74.7532018)],
['https://www.dansvillecsd.org/Page/2394', 0, (42.5610571, -77.6960138)],
['https://www.dcseagles.org/employment.aspx', 0, (42.0809204, -74.9957197)],
['https://www.duanesburg.org', 0, (42.7453532, -74.1881834)],
['https://www.elcsd.org/Page/30', 0, (44.216171, -73.591232)],
['https://www.explorationrochester.org', 0, (43.1854754, -77.6106861508176)],
['https://www.fondafultonvilleschools.org/about/employment', 0, (42.9545179, -74.3765241)],
['https://www.forestville.com/domain/10', 0, (42.468392, -79.176985)],
['https://www.franklincsd.org/Employment.aspx', 0, (42.3406373, -75.1651689)],
['https://www.futureleadersinstitute.org/about-us/careers', 0, (40.8088437, -73.9658566)],
['https://www.gasd.org/employment', 0, (42.943367, -74.1850436)],
['https://www.gcsny.org/employment', 0, (41.4020382, -74.3243191)],
['https://www.genvalley.org/Page/49', 0, (42.2231241, -78.0344506)],
['https://www.gesdk12.org/employment', 0, (43.0528133, -74.34369)],
['https://www.gmucsd.org/Employment.aspx', 0, (42.4714657, -75.325729)],
['https://www.greenburghcsd.org/domain/45', 0, (41.02473, -73.804168)],
['https://www.gugcs.org/apps/jobs', 0, (40.6524927, -73.7914214158161)],
['https://www.haldaneschool.org/departments/employment-resources/employment-opportunities', 0, (41.4200938, -73.9545831)],
['https://www.hancock.stier.org/Employment.aspx', 0, (41.9539754, -75.2804502)],
['https://www.hcs.stier.org/employment.aspx', 0, (42.1784124, -75.6246298)],
['https://www.hcsk12.org/Page/194', 0, (44.152159, -75.321236)],
['https://www.hdcsk12.org/Page/29', 0, (44.5050607, -75.273822)],
['https://www.herkimercsd.org/employment', 0, (43.0256259, -74.9859889)],
['https://www.heuvelton.k12.ny.us', 0, (44.618333, -75.40741)],
['https://www.hpcsd.org/Page/412', 0, (41.7847232, -73.9332461)],
['https://www.irvingtonschools.org/Page/2145', 0, (41.0331138, -73.8683368)],
['https://www.ivyhillprep.org/careers', 0, (40.7308619, -73.9871558)],
['https://www.johnstownschools.org/job-openings', 0, (43.0068689, -74.3676437)],
['https://www.keycollegiate.org/careers', 0, (40.64530975, -73.9550230275334)],
['https://www.kippnyc.org/careers/listings', 0, (40.85048545, -73.8404035580209)],
['https://www.kippnyc.org/schools/kipp-freedom', 0, (40.74123595, -73.356691165361)],
['https://www.kpcsd.org/apps/pages/index.jsp?dir=Job%20Postings&type=d&uREC_ID=346753', 0, (40.9125979, -73.3009489)],
['https://www.ktufsd.org/Page/17387', 0, (42.8867166, -78.8783922)],
['https://www.lew-port.com/Page/77', 0, (43.247453, -79.050064)],
['https://www.manhassetschools.org/domain/64', 0, (40.7978787, -73.6995749)],
['https://www.margaretvillecs.org/Employment.aspx', 0, (42.148699, -74.648211)],
['https://www.maryvaleufsd.org', 0, (42.9033917, -78.7547536)],
['https://www.mccsd.net/Page/317', 0, (40.8584316, -73.0995539)],
['https://www.mcs.k12.ny.us/apps/pages/index.jsp?uREC_ID=776749&type=d&pREC_ID=1175998', 0, (44.928106, -74.892082)],
['https://www.me.stier.org/Personnel-Employment.aspx', 0, (42.1128526, -76.021034)],
['https://www.menands.org/menands_union_free_school_employ.html', 0, (42.6920233, -73.7245639)],
['https://www.mexicocsd.org/Page/534', 0, (43.459514, -76.228818)],
['https://www.millerplace.k12.ny.us/Domain/39', 0, (40.9598212, -72.9962148)],
['https://www.mohonasen.org/employment', 0, (42.8142432, -73.9395687)],
['https://www.monticelloschools.net/business-hr/employment', 0, (41.6556465, -74.6893282)],
['https://www.mw.k12.ny.us/about/employment', 0, (41.3317605, -74.120978)],
['https://www.newvisions.org/aim2', 0, (40.85048545, -73.8404035580209)],
['https://www.newvisions.org/careers', 0, (40.64530975, -73.9550230275334)],
['https://www.nfschools.net/Page/3559', 0, (43.1098695, -79.055139)],
['https://www.niskayunaschools.org/employment', 0, (42.8076585, -73.8750206265193)],
['https://www.northcollins.com/cms/One.aspx?portalId=272706&pageId=626890', 0, (42.595338, -78.941146)],
['https://www.northcolonie.org/about-us/employment-opportunities', 0, (42.7442986, -73.7614799)],
['https://www.norwichcsd.org/Vacancies.aspx', 0, (42.531184, -75.5235149)],
['https://www.ntschools.org//site/Default.aspx?PageID=5052', 0, (43.038668, -78.8642034)],
['https://www.nwcsd.org/Page/64', 0, (43.136723, -78.8847611)],
['https://www.oahornets.org/apps/jobs', 0, (43.0658926, -78.269742)],
['https://www.oesj.org', 0, (42.9981274, -74.6829225)],
['https://www.oleanschools.org/Page/5715', 0, (42.081489, -78.4302926)],
['https://www.oneontacsd.org/EmploymentOpportunities.aspx', 0, (42.453492, -75.0629531)],
['https://www.oxac.org/Employment.aspx', 0, (42.4420181, -75.5976855)],
['https://www.peekskillcsd.org/Page/383', 0, (41.28636, -73.915066)],
['https://www.persistenceprep.org/mission', 0, (42.8867166, -78.8783922)],
['https://www.phcsd.org/apps/pages/index.jsp?uREC_ID=1161786&type=d&pREC_ID=1415161', 0, (44.6279506, -74.8153687)],
['https://www.pinebushschools.org/departments/hr-employment', 0, (41.4278716, -74.1659798)],
['https://www.pmschools.org/Page/160', 0, (40.7656539, -73.0151084)],
['http://www.ryeschools.org', 0, (40.9808209, -73.684294)],
['http://www.gufs.org', 0, (41.3809926, -73.9473575)],
['https://www.poughkeepsieschools.org/Page/320', 0, (41.7065779, -73.9284101)],
['https://www.prattsburghcsd.org/Page/26', 0, (42.5219092665856, -77.2910005561379)],
['https://www.pycsd.org/apps/pages/index.jsp?uREC_ID=948562&type=d&pREC_ID=1275659', 0, (42.6603037, -77.0540989)],
['https://www.quogueschool.com', 0, (40.820974, -72.605024)],
['https://www.railroaders.net/EmploymentHAL.php', 0, (43.555764, -73.403778)],
['https://www.rcscsd.org/about-us/employment', 0, (42.4684148, -73.8162354)],
['https://www.rcsdk12.org/employment', 0, (43.157285, -77.615214)],
['https://www.reachacademycharter.org/employment', 0, (42.8867166, -78.8783922)],
['https://www.rooseveltufsd.org/Page/325', 0, (40.678713, -73.5890168)],
['https://www.sandycreekcsd.org', 0, (40.7308619, -73.9871558)],
['https://www.saratogaschools.org/district.cfm?subpage=1383228', 0, (43.0821793, -73.7853915)],
['https://www.sayvilleschools.org/Page/3271', 0, (40.740111, -73.08806)],
['https://www.scarsdaleschools.k12.ny.us/Page/19564', 0, (40.990605, -73.8082739)],
['https://www.schoolinthesquare.org/our-team/join-our-team', 0, (40.8493254985483, -73.9351991867384)],
['https://www.schuylervilleschools.org/employment', 0, (43.100231, -73.581963)],
['https://www.scsd.org/employment', 0, (42.9384101, -73.6531731)],
['https://www.secsd.org/Employment.aspx', 0, (42.6781266, -75.4985123)],
['https://www.sgfcsd.org/human-resources', 0, (43.299447, -73.635178)],
['https://www.sharonsprings.org/employment', 0, (42.7959074, -74.617086)],
['https://www.shenet.org/employment', 0, (42.8656325, -73.7709535)],
['https://www.socsd.org', 0, (41.0634299, -73.9576378)],
['https://www.southcolonieschools.org/departments/human-resources-department/employment-opportunities', 0, (42.6511674, -73.754968)],
['https://www.stregiscsd.org/faculty-staff', 0, (44.6733509, -74.5503169)],
['https://www.successacademies.org/schools', 0, (40.7308619, -73.9871558)],
['https://www.sunyacc.edu/careers', 0, (43.3772932, -73.6131714)],
['https://www.theuftcharterschool.org', 0, (40.64530975, -73.9550230275334)],
['https://www.trivalleycsd.org/domain/124', 0, (41.8478701, -74.547935)],
['https://www.valencecollegeprep.org', 0, (40.7308619, -73.9871558)],
['https://www.warwickvalleyschools.com/employment', 0, (41.2636177599633, -74.3687918430554)],
['https://www.waterloocsd.org/Page/66', 0, (42.9047884, -76.8627368)],
['https://www.watervlietcityschools.org/employment', 0, (42.7282483, -73.7014649039252)],
['https://www.webutuckschools.org/Page/29', 0, (41.8492599, -73.5567919)],
['https://www.westgenesee.org/staff-resources/job-opportunities', 0, (43.0481221, -76.1474244)],
['https://www.whiteplainspublicschools.org/Page/546', 0, (41.007046, -73.734376)],
['https://www.wilsoncsd.org/site/Default.aspx?PageID=77', 0, (43.309778, -78.82615)],
['https://www.windsor-csd.org/Employment.aspx', 0, (42.0759128, -75.640462)],
['https://www.wpcsd.org/EmploymentOpportunities.aspx', 0, (42.3289626, -75.9677001)],
['https://www.ws.k12.ny.us/JobPostings.aspx', 0, (41.4245962, -74.1714163)],
['https://www.wscschools.org/Page/291', 0, (42.83943505, -78.7465029066232)],
['https://www.wyomingcsd.org/Page/20', 0, (42.7039813, -78.2415228)],
['https://zetaschools.org/careers', 0, (40.8493254985483, -73.9351991867384)]
)





    # University URLs, initial crawl levels, and coordinates database
    uni_list = (
['http://careers.canisius.edu/cw/en-us/listing', 0, (42.8867166, -78.8783922)],
['http://careers.marist.edu/cw/en-us/listing', 0, (41.7065779, -73.9284101)],
['http://cooper.edu/work/employment-opportunities', 0, (40.7308619, -73.9871558)],
['http://einstein.yu.edu/administration/human-resources/career-opportunities.html', 0, (40.8511468, -73.8444737)],
['http://gts.edu/job-postings', 0, (40.7308619, -73.9871558)],
['http://huc.edu/about/employment-opportunities', 0, (40.7308619, -73.9871558)],
['http://humanresources.vassar.edu/jobs', 0, (41.7065779, -73.9284101)],
['http://inside.manhattan.edu/offices/human-resources/jobs.php', 0, (40.90056, -73.90639)],
['http://jobs.medaille.edu', 0, (42.8867166, -78.8783922)],
['http://jobs.union.edu/cw/en-us/listing', 0, (42.8142432, -73.9395687)],
['http://liu.edu/brooklyn.aspx', 0, (40.64530975, -73.9550230275334)],
['http://newschool.edu/public-engagement', 0, (40.7308619, -73.9871558)],
['http://niagaracc.suny.edu/careers/nccc-jobs.php', 0, (43.136723, -78.8847611)],
['http://sunysccc.edu/About-Us/Office-of-Human-Resources/Employment-Opportunities', 0, (42.8143922952735, -73.9420906329747)],
['http://utica.edu/hr/employment.cfm', 0, (43.1009031, -75.2326641)],
['http://www.bard.edu/employment/employment', 0, (42.2528649, -73.790959)],
['http://www.berkeleycollege.edu/index.htm', 0, (40.7308619, -73.9871558)],
['http://www.canton.edu/human_resources/job_opportunities.html', 0, (44.5956163, -75.1690942)],
['http://www.cazenovia.edu/campus-resources/human-resources/employment-opportunities', 0, (42.9300668, -75.8526915)],
['http://www.colgate.edu/working-at-colgate', 0, (42.8268798, -75.5444159)],
['http://www.college.columbia.edu', 0, (40.8088437, -73.9658566)],
['http://www.columbia.edu/cu/ssw', 0, (40.8088437, -73.9658566)],
['http://www.dental.columbia.edu', 0, (40.8088437, -73.9658566)],
['http://www.dyc.edu/about/administrative-offices/human-resources/career-opportunities.aspx', 0, (42.8867166, -78.8783922)],
['http://www.gs.columbia.edu', 0, (40.8088437, -73.9658566)],
['http://www.houghton.edu/campus/human-resources/employment', 0, (42.4233981, -78.1572319)],
['http://www.hunter.cuny.edu/hr/Employment', 0, (40.7308619, -73.9871558)],
['http://www.jtsa.edu/jobs-at-jts', 0, (40.8088437, -73.9658566)],
['http://www.law.columbia.edu', 0, (40.8088437, -73.9658566)],
['http://www.liu.edu/post', 0, (40.64530975, -73.9550230275334)],
['http://www.mcny.edu/index.php', 0, (40.7093848, -74.0147256)],
['http://www.monroecc.edu/employment', 0, (43.157285, -77.615214)],
['http://www.nccc.edu/careers-2', 0, (44.329497, -74.131279)],
['http://www.nycc.edu/employment-opportunities', 0, (42.910622, -76.7966215)],
['http://www.nyts.edu', 0, (40.8108175295545, -73.9637256464405)],
['http://www.nyu.edu/about/careers-at-nyu.html', 0, (40.7308619, -73.9871558)],
['http://www.paulsmiths.edu/humanresources/employment', 0, (44.4386659, -74.2526581)],
['http://www.potsdam.edu/crane', 0, (44.6752342, -74.9860333)],
['http://www.qcc.cuny.edu/employment/index.html', 0, (40.7684351, -73.7770774)],
['http://www.rit.edu/employment_rit.html', 0, (43.157285, -77.615214)],
['http://www.rochester.edu/working/hr/jobs', 0, (43.1551894, -77.6077078)],
['http://www.simon.rochester.edu/faculty-and-research/faculty-directory/faculty-recruitment/index.aspx', 0, (43.157285, -77.615214)],
['http://www.sunyacc.edu/job-listings', 0, (43.3772932, -73.6131714)],
['http://www.sunywcc.edu/about/jobshuman-resources', 0, (41.0748189, -73.7751326)],
['http://www.webb.edu/employment', 0, (40.882699, -73.644578)],
['http://www.youngwomenscollegeprep.org', 0, (43.1854754, -77.6106861508176)],
['http://www1.cuny.edu/sites/onboard/homepage/getting-started/campus/medgar-evers-college', 0, (40.7684351, -73.7770774)],
['http://www1.sunybroome.edu/about/employment', 0, (42.096968, -75.914341)],
['https://albany.interviewexchange.com/jobsrchresults.jsp', 0, (42.6511674, -73.754968)],
['https://alfredstate.interviewexchange.com/static/clients/481ASM1/index.jsp', 0, (42.2542366, -77.7905509)],
['https://apply.interfolio.com/14414/positions', 0, (40.64530975, -73.9550230275334)],
['https://careers-nyit.icims.com/jobs/search?ss=1', 0, (40.7887113, -73.5995717)],
['https://careers.barnard.edu', 0, (40.8088437, -73.9658566)],
['https://careers.columbia.edu', 0, (40.8088437, -73.9658566)],
['https://careers.columbia.edu/content/how-apply', 0, (40.8088437, -73.9658566)],
['https://careers.mountsinai.org/jobs?page=1', 0, (40.7796637, -73.9438435)],
['https://careers.newschool.edu', 0, (42.6511674, -73.754968)],
['https://careers.pace.edu/postings/search', 0, (40.7308619, -73.9871558)],
['https://careers.pageuppeople.com/876/cw/en-us/listing', 0, (40.7308619, -73.9871558)],
['https://careers.skidmore.edu/postings/search', 0, (43.0821793, -73.7853915)],
['https://clarkson.peopleadmin.com', 0, (44.6697996, -74.9813349)],
['https://clinton.interviewexchange.com/static/clients/552CCM1/index.jsp', 0, (44.69282, -73.45562)],
['https://cobleskill.interviewexchange.com/static/clients/474SCM1/index.jsp', 0, (42.677853, -74.4854172)],
['https://cshl.peopleadmin.com/postings/search', 0, (40.8714873, -73.456788)],
['https://cuny.jobs', 0, (40.7308619, -73.9871558)],
['https://daemen.applicantpro.com/jobs', 0, (42.9783924, -78.7997616)],
['https://employment.acphs.edu/postings/search', 0, (42.6511674, -73.754968)],
['https://employment.potsdam.edu/postings/search', 0, (44.6752342, -74.9860333)],
['https://employment.stlawu.edu/postings/search', 0, (44.5956163, -75.1690942)],
['https://farmingdale.interviewexchange.com/static/clients/383FAM1/index.jsp', 0, (40.7328811, -73.4458564)],
['https://fitnyc.interviewexchange.com/static/clients/391FIM1/index.jsp', 0, (40.7308619, -73.9871558)],
['https://fredonia.interviewexchange.com/static/clients/471SFM1/index.jsp', 0, (42.440058, -79.331711)],
['https://genesee.interviewexchange.com/static/clients/374GCM1/index.jsp', 0, (42.9980144, -78.1875515)],
['https://herkimer.interviewexchange.com/static/clients/505HCM1/index.jsp', 0, (43.0256259, -74.9859889)],
['https://hr.adelphi.edu/position-openings', 0, (40.72319685, -73.6403872966069)],
['https://hr.cornell.edu/jobs', 0, (42.4396039, -76.4968019)],
['https://hvcc.edu/hr/employment-opportunities.html', 0, (42.7284117, -73.6917878)],
['https://iona-openhire.silkroad.com/epostings/index.cfm?fuseaction=app.jobsearch', 0, (40.9665587, -73.7878852)],
['https://ithaca.peopleadmin.com', 0, (42.4396039, -76.4968019)],
['https://jobs.buffalostate.edu', 0, (42.9203639, -78.8770557)],
['https://jobs.cortland.edu', 0, (42.6011813, -76.1804843)],
['https://jobs.excelsior.edu', 0, (42.6511674, -73.754968)],
['https://jobs.geneseo.edu/postings/search', 0, (42.795896, -77.816947)],
['https://jobs.liu.edu/#/list', 0, (40.64530975, -73.9550230275334)],
['https://jobs.mercy.edu/postings/search', 0, (41.013115, -73.849734)],
['https://jobs.naz.edu/postings/search', 0, (43.1635257, -77.6083784825996)],
['https://jobs.niagara.edu/JobPostings.aspx', 0, (43.13755555, -79.0375125585894)],
['https://jobs.plattsburgh.edu/postings/search', 0, (44.69282, -73.45562)],
['https://jobs.purchase.edu/applicants/jsp/shared/frameset/Frameset.jsp', 0, (41.0409305, -73.7145746)],
['https://jobs.sjfc.edu', 0, (43.1635257, -77.6083784825996)],
['https://jobsatupstate.peopleadmin.com/applicants/jsp/shared/search/SearchResults_css.jsp', 0, (43.0481221, -76.1474244)],
['https://law-touro-csm.symplicity.com/students/index.php/pid170913', 0, (41.1073184, -73.7959667)],
['https://maritime.interviewexchange.com/static/clients/373SMM1/index.jsp', 0, (40.8214533, -73.8241910783815)],
['https://mountsaintvincent.edu/campus-life/campus-services/human-resources/employment-opportunities', 0, (40.90056, -73.90639)],
['https://mvcc.csod.com/ats/careersite/search.aspx', 0, (43.079254, -75.221178)],
['https://ncc.interviewexchange.com/static/clients/489NCM1/index.jsp', 0, (40.72319685, -73.6403872966069)],
['https://occc.interviewexchange.com/static/clients/437SOM1/index.jsp', 0, (41.44591415, -74.4224417389405)],
['https://oldwestbury.interviewexchange.com/static/clients/519OWM1/index.jsp', 0, (40.7887113, -73.5995717)],
['https://oswego.interviewexchange.com/static/clients/313OSM1/index.jsp', 0, (43.4547284, -76.5095967)],
['https://pa334.peopleadmin.com/postings/search', 0, (40.8088437, -73.9658566)],
['https://recruiting.ultipro.com/CUL1001CLNRY/JobBoard/5d1a692d-cf6b-4b4f-8652-c60b25898609/?q=&o=postedDateDesc', 0, (41.7847232, -73.9332461)],
['https://rpijobs.rpi.edu', 0, (42.7284117, -73.6917878)],
['https://strose.interviewexchange.com/jobsrchresults.jsp', 0, (42.6511674, -73.754968)],
['https://suny.oneonta.edu/sponsored-programs/employment-opportunities', 0, (42.453492, -75.0629531)],
['https://sunydutchess.interviewexchange.com/static/clients/539DCM1/index.jsp', 0, (41.5965635, -73.9112103)],
['https://sunyocc.peopleadmin.com/postings/search', 0, (43.0481221, -76.1474244)],
['https://sunyopt.peopleadmin.com/postings/search', 0, (40.7308619, -73.9871558)],
['https://sunypoly.interviewexchange.com/static/clients/511SPM1/hiring.jsp', 0, (42.6511674, -73.754968)],
['https://sunysullivan.edu/offices/associate-vp-for-planning-human-resources-facilities/job-opportunities', 0, (41.77415415, -74.6566052645852)],
['https://touro.peopleadmin.com/postings/search', 0, (40.7287818856407, -73.8210681595253)],
['https://trocaire.applicantpro.com/jobs', 0, (42.8867166, -78.8783922)],
['https://utsnyc.edu/about/careers-at-union', 0, (40.8088437, -73.9658566)],
['https://wagner.edu/hr/hr_openings', 0, (40.5834379, -74.1495875)],
['https://workforcenow.adp.com/mdf/recruitment/recruitment.html?cid=b635a855-6cf7-4ee7-ba36-6da36d9f2eea&ccId=19000101_000001&type=MP', 0, (41.1151372, -74.1493948)],
['https://www.alfred.edu/jobs-at-alfred/index.cfm', 0, (42.2542366, -77.7905509)],
['https://www.bankstreet.edu/about-bank-street/job-opportunities', 0, (40.7967148, -73.9647223)],
['https://www.binghamton.edu/human-resources/employment-opportunities/index.html', 0, (42.096968, -75.914341)],
['https://www.brockport.edu/support/human_resources/empop/vacancies', 0, (43.213671, -77.93918)],
['https://www.brooklaw.edu/about-us/job-opportunities.aspx', 0, (40.64530975, -73.9550230275334)],
['https://www.cayuga-cc.edu/about/human-resources', 0, (42.9320202, -76.5672029)],
['https://www.cnr.edu/employment-opportunities', 0, (40.9115386, -73.7826363)],
['https://www.davisny.edu/jobs', 0, (42.1156308, -75.9588092)],
['https://www.dc.edu/human-resources', 0, (41.0465776, -73.9496707)],
['https://www.ecc.edu/work', 0, (42.8867166, -78.8783922)],
['https://www.elmira.edu/Student/Offices_Resources/Employment_Opportunities/index.html', 0, (42.0897965, -76.8077338)],
['https://www.esc.edu/human-resources/employment-opportunities', 0, (43.0821793, -73.7853915)],
['https://www.flcc.edu/jobs', 0, (42.8844625, -77.278399)],
['https://www.fmcc.edu/about/employment-opportunities', 0, (43.0068689, -74.3676437)],
['https://www.fordham.edu/info/23411/job_opportunities', 0, (40.85048545, -73.8404035580209)],
['https://www.ftc.edu/employment', 0, (40.8175985, -73.3540078)],
['https://www.hamilton.edu/offices/human-resources/employment/job-opportunities', 0, (44.7278943, -73.6686982)],
['https://www.hartwick.edu/about-us/employment/human-resources/employment-opportunities', 0, (42.453492, -75.0629531)],
['https://www.helenefuld.edu/employment', 0, (40.7238838, -73.9911486)],
['https://www.hilbert.edu/about/human-resources/hilbert-job-openings', 0, (42.716293, -78.828717)],
['https://www.hofstra.edu/about/jobs/index.html', 0, (40.7063185, -73.618684)],
['https://www.hofstra.edu/academics/colleges/zarb', 0, (40.7063185, -73.618684)],
['https://www.hws.edu/offices/hr/employment/index.aspx', 0, (42.8689552, -76.9777436)],
['https://www.juilliard.edu/jobs', 0, (40.7771311410301, -73.9808786732298)],
['https://www.keuka.edu/hr/employment-opportunities', 0, (42.8689552, -76.9777436)],
['https://www.laguardia.edu/employment', 0, (40.7308619, -73.9871558)],
['https://www.lemoyne.edu/Work-at-Le-Moyne', 0, (43.0481221, -76.1474244)],
['https://www.limcollege.edu/about-lim/careers', 0, (40.7607161, -73.9669623)],
['https://www.mmm.edu/offices/human-resources/Employment', 0, (40.7666562, -73.9508886)],
['https://www.molloy.edu/about-molloy-college/human-resources/careers-at-molloy', 0, (40.6574186, -73.6450664)],
['https://www.monroecollege.edu/About/Employment/u', 0, (42.6511674, -73.754968)],
['https://www.morrisville.edu/contact/offices/human-resources/careers', 0, (42.8986566, -75.6402204)],
['https://www.msmc.edu/employment', 0, (41.5034271, -74.0104179)],
['https://www.msmnyc.edu/about/employment-at-msm', 0, (40.8088437, -73.9658566)],
['https://www.mville.edu/about-manhattanville/human-resources', 0, (41.0409305, -73.7145746)],
['https://www.newpaltz.edu/hr/jobs.html', 0, (41.7464972, -74.0844894)],
['https://www.newschool.edu/performing-arts', 0, (40.7308619, -73.9871558)],
['https://www.nyack.edu/site/employment-opportunities', 0, (40.7308619, -73.9871558)],
['https://www.paycomonline.net/v4/ats/web.php/jobs', 0, (40.7308619, -73.9871558)],
['https://www.qc.cuny.edu/HR/Pages/JobListings.aspx', 0, (40.6524927, -73.7914214158161)],
['https://www.roberts.edu/employment', 0, (43.157285, -77.615214)],
['https://www.rochester.edu/faculty-recruiting/positions', 0, (43.157285, -77.615214)],
['https://www.sage.edu/about/human-resources/employment-opportunities', 0, (42.7284117, -73.6917878)],
['https://www.sarahlawrence.edu/human-resources/job-openings.html', 0, (40.9381544, -73.8320784)],
['https://www.sbu.edu/jobs-at-sbu', 0, (42.0761398888889, -78.475734)],
['https://www.sfc.edu/about/careers', 0, (40.64530975, -73.9550230275334)],
['https://www.sjcny.edu/employment', 0, (40.64530975, -73.9550230275334)],
['https://www.stac.edu/about-stac/jobs-stac', 0, (41.0289025, -73.9326580670926)],
['https://www.stjohns.edu/about/administrative-offices/human-resources/recruitment', 0, (40.6524927, -73.7914214158161)],
['https://www.stonybrookmedicine.edu/careers', 0, (40.9215391, -73.1279744)],
['https://www.sujobopps.com/postings/search', 0, (43.0481221, -76.1474244)],
['https://www.suny.edu/campuses/cornell-vet', 0, (42.4396039, -76.4968019)],
['https://www.suny.edu/careers/employment/index.cfm?s=y', 0, (42.6511674, -73.754968)],
['https://www.sunycgcc.edu/about-cgcc/employment-cgcc', 0, (42.2528649, -73.790959)],
['https://www.sunyjcc.edu/about/human-resources/jobs', 0, (42.0970023, -79.2353259)],
['https://www.sunyjefferson.edu/careers-jefferson/open-positions.php', 0, (44.058053, -75.74324)],
['https://www.sunyulster.edu/campus_and_culture/about_us/jobs.php', 0, (41.8531485, -74.1390329)],
['https://www.tkc.edu/careers-at-kings', 0, (40.7308619, -73.9871558)],
['https://www.tompkinscortland.edu/college-info/employment', 0, (42.4909053, -76.2971553)],
['https://www.ubjobs.buffalo.edu', 0, (42.8867166, -78.8783922)],
['https://www.usmma.edu/about/employment/career-opportunities', 0, (40.8198231, -73.7351316)],
['https://www.vaughn.edu/jobs', 0, (40.7660002, -73.8636574)],
['https://www.villa.edu/about-us/employment-opportunities', 0, (42.8867166, -78.8783922)],
['https://www.warner.rochester.edu/faculty/positions', 0, (43.157285, -77.615214)],
['https://www.wells.edu/jobs', 0, (42.7539591, -76.7024485)],
['https://www.york.cuny.edu/administrative/human-resources/jobs', 0, (40.69983135, -73.8077028537026)],
['https://www.yu.edu/hr/opportunities', 0, (40.8493254985483, -73.9351991867384)],
['https://www2.appone.com/Search/Search.aspx?ServerVar=ConcordiaCollege.appone.com&results=yes', 0, (40.9381544, -73.8320784)],
['https://www3.sunysuffolk.edu/About/Employment.asp', 0, (40.8664874, -73.0356625)]
)





    # Set search arguments
    all_args = ('c', 's', 'u', 'help')
    while True:
        print('\n\n\n Enter "c" to search Civil Service websites, \n Enter "s" to search school district and charter school websites, \n Enter "u" to search university and college websites, \n or enter any combination thereof. \n Example: scu')
        arg_resp = input().lower()
        if any(aaa in arg_resp for aaa in all_args):
            tmp = os.system('clear||cls')
            break
        else:
            tmp = os.system('clear||cls')
            print('\n\n\n____ Error. You must enter at least one valid option. ____  \n Example: c')

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

    opt_arg = False
    if 'o' in arg_resp:
        opt_arg = True
        print('Advanced option invoked.')

    school_arg = False
    if 's' in arg_resp:
        school_arg = True
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
    while True:
        keyword_resp = input('\n\n\n Enter a job title to search for. \n Example: library media specialist \n').lower()
        if keyword_resp == '':
            tmp = os.system('clear||cls')
            print('\n\n\n____ Error. You must enter a job title. ____ \n Example: electrician')
            continue
        keyword_list.append(keyword_resp)
        break
    while True:
        keyword_resp = input('\n\n Enter another job title \n or leave blank to finish. \n Example: library clerk \n').lower()
        if keyword_resp == '':
            tmp = os.system('clear||cls')
            break
        else: keyword_list.append(keyword_resp)

    # Set the coordinates
    while True:
        try:
            home_resp = input('\n\n\n Enter your ZIP code. \n This will be used to search only the job postings near you. \n Leave blank to search all of NYS. \n Example: 14020 \n')
            if home_resp == '':
                tmp = os.system('clear||cls')
                break
            if home_resp == 'b': home_resp = '14020'
            hc = zip_dict[int(home_resp)]
            tmp = os.system('clear||cls')
            break
        except:
            tmp = os.system('clear||cls')
            print('\n\n\n____ Error. Your input cannot be converted into a known location. Try again. ____ \n Example: 14220')

    # Set the geographic limiter
    if home_resp:
        print('\n Using the following coordinates for your location:\n', hc)
        while True:
            try:
                max_dist = input('\n\n\n Enter the maximum distance (in miles) to search. \n Example: 100 \n')
                if max_dist == '': max_dist = 99999
                max_dist = int(max_dist)
                if max_dist > -1:
                    tmp = os.system('clear||cls')
                    break
                else: print('\n\n\n____ Error. Your input was a negative number. ____')
            except:
                tmp = os.system('clear||cls')
                print('\n\n\n____ Error. Your input was not an integer. ____')

    # Set optional advanced parameters
    if opt_arg:

        # Set the number of processes to run
        while True:
            try:
                num_procs = input('\n\n\n Enter the number of processes to run in parallel \n or leave blank to use the recommended value.\n Example: 32 \n')
                if num_procs == '':
                    num_procs = 32
                num_procs = int(num_procs)
                if num_procs > 0:
                    tmp = os.system('clear||cls')
                    break
                else: print('\n\n\n____ Error. Your input was not greater than zero. ____')
            except:
                tmp = os.system('clear||cls')
                print('\n\n\n____ Error. Your input was not an integer. ____')

        # Set the max crawl depth
        while True:
            try:
                max_crawl_depth = input('\n\n\n Enter the number of levels to crawl \n or leave blank to use the recommended value. \n Example: 2 \n')
                if max_crawl_depth == '':
                    max_crawl_depth = 2
                max_crawl_depth = int(max_crawl_depth)
                if max_crawl_depth >= 0:
                    tmp = os.system('clear||cls')
                    break
                else: print('\n\n\n____ Error. Your input was a negative number. ____')
            except:
                tmp = os.system('clear||cls')
                print('\n\n\n____ Error. Your input was not an integer. ____')
    else:
        num_procs = 32
        max_crawl_depth = 2


    # Start timer
    startTime = datetime.datetime.now()
    all_urls_q = Queue()

    # Geodesic function to calculate distance
    def geodesic(hc, url_coords):

        # Approximate radius of earth at 43 lat in miles
        R = 3962

        # Magic
        lat1 = radians(hc[0])
        lon1 = radians(hc[1])
        lat2 = radians(url_coords[0])
        lon2 = radians(url_coords[1])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        dist = R * c
        return(dist)

    # Put school URLs in queue
    if school_arg:
        for the_list in school_list:

            # Calculate distances if geo limiter invoked
            if home_resp:
                dist = geodesic(hc, the_list[2])

                # Omit if distance is too far
                if dist > max_dist:
                    continue

            # Replace coords with portal
            the_list[2] = the_list[0]

            # Append jbws type
            if civ_arg: the_list.append('sch')

            # Put civil service URls, initial crawl level, portal and optional jbws type into queue
            all_urls_q.put(the_list)

        # Declare civ jobwords
        jobwords = jobwords_s

    # Put university URLs in queue
    if uni_arg:
        for the_list in uni_list:
            if home_resp:
                dist = geodesic(hc, the_list[2])
                if dist > max_dist: continue
            the_list[2] = the_list[0]
            if civ_arg: the_list.append('uni')
            all_urls_q.put(the_list)
        jobwords = jobwords_s

    # Put civil service URLs in queue
    if civ_arg:
        for the_list in civ_list:
            if home_resp:
                dist = geodesic(hc, the_list[2])
                if dist > max_dist: continue
            the_list[2] = the_list[0]
            if school_arg or uni_arg: the_list.append('civ')
            all_urls_q.put(the_list)
        jobwords = jobwords_civ

    # Misc objects
    qlength = all_urls_q.qsize()
    skipped_pages = Value('i', 0)
    prog_count = Value('i', 0)
    total_count = Value('i', qlength)

    # Create manager lists
    manager = Manager()
    keywordurl_man_list = manager.list()
    checkedurls_man_list = manager.list()
    errorurls_man_dict = manager.dict()
    disagree_list = manager.list()
    woww = manager.list()

    # Create child processes
    for ii in range(num_procs):
        worker = Process(target=scraper, args=(keyword_list, all_urls_q, max_crawl_depth, keywordurl_man_list, checkedurls_man_list, errorurls_man_dict, skipped_pages, prog_count, total_count, all_links_arg, verbose_arg, jobwords, disagree_list, woww))
        worker.start()

    # Wait until all tasks are done
    current_prog_c = None
    while len(active_children()) > 1:
        if current_prog_c != prog_count.value:
            #if not verbose_arg: tmp = os.system('clear||cls')
            print(' Number of processes running =', len(active_children()), '\n Max crawl depth =', max_crawl_depth)
            print('\n\n\n\n Now searching for keyword(s):', keyword_list, '\n\n Searching in:')

            if civ_arg: print('Civil Service')
            if school_arg: print('School districts and charter schools')
            if uni_arg: print('Universities and colleges')

            print('\n\n Waiting for all processes to finish. Progress =', prog_count.value, 'of', total_count.value)
            current_prog_c = prog_count.value
        time.sleep(3)

    print('\n =======================  Search complete  =======================')

    for i in jobwords:
        r_count = woww.count(i)
        print(i, '=', r_count)

    print('\n')
    for i in jobwords_certainty:
        r_count = woww.count(i)
        print(i, '=', r_count)

    #print(sorted(woww))


    domain_limit_num = 6
    domain_excess_list = []
    portal_results_dict = {}
    keywordurl_man_list.sort()
    finalkeywordurl_list = []
    dup_list = []

    # keywordurl_man_list contents: [result URL, jobword confidence, portal URL]
    # Take results and group them by their portal in a dict
    for entry in keywordurl_man_list:

        # Remove '], scheme, www., and fragments to prevent dups
        result = entry[0][:-2].split('://')[1]
        if result.startswith('www.'):
            result = result.split('www.')[1]
        if result.startswith('www2.'):
            result = result.split('www2.')[1]
        if result.startswith('www3.'):
            result = result.split('www3.')[1]
        result = result.split('#')[0]

        # Remove trailing whitespace and slash and then lowercase it
        result = result.strip().strip('/').lower()

        # Discard dup-optimised URL dups. Keep first seen because they both yielded a match without error
        if result in dup_list: continue
        dup_list.append(result)


        '''
        ## dupdict consist of optimised URLs as key and origs as values?
        ## only if orig has upppercase
        # Compare dups using lowercase
        for i in duplist:

            # If dup is found add the one with uppercase letters to good list
            if result.lower() in i.lower():
                if any(x.isupper() for x in result):
                    goodlist.append(result)
                    print('upper in new')
                    break
                elif any(x.isupper() for x in i):
                    goodlist.append(i)
                    print('upper in duplist')
                    break
                else:
                    goodlist.append(result)
                    print('no upper found')
                    break

            # If no match then add to good and dup lists
            else:
                goodlist.append(result)
                duplist.append(result)
        '''


        ## maybe use this in addition to portal as domain?
        ## will limit many results at one domain but originating from multiple portals
        '''
        # Derive domain from result URL and catch domains that use periods
        domain_bare = result.split('/')[0]
        if domain_bare.count('.') > 1:
            domain_bare = domain_bare.split('.', 1)[1]
        '''

        # Use portal as domain
        domain_bare = entry[2]
        db_entry = [entry[0], entry[1]]

        # Build dict with domain as keys and urls and confidence as values
        if domain_bare in portal_results_dict.keys():
            portal_results_dict[domain_bare].append(db_entry)
        else:
            portal_results_dict[domain_bare] = [db_entry]

    # Intra-site exclusions by sorting by jobword confidence
    for each_portal in portal_results_dict.keys():
        domain_count = 0
        each_domain_list = []

        '''
        ## switch back to fixed num only?
        ## lengths of what? number of results per portal? using percent can still give a crapload of results per portal.
        ## each domain list is empty
        # Make domain_limit_num dynamic based on fixed num for low lengths and percent for high lengths
        if len(each_domain_list) < 10:
            domain_limit_num = 5
        else:
            domain_limit_num = int((len(each_domain_list) / 2) + 1)
        '''


        # Sort the domain list by confidence if there is a domain exceedance
        if len(portal_results_dict[each_portal]) > domain_limit_num:
            each_domain_list = portal_results_dict[each_portal]
            each_domain_list = sorted(each_domain_list, key = lambda x: int(x[1]), reverse=True)

            # Append results to either good list or domain exceedance list based on confidence and domain limit
            for i in each_domain_list:
                if domain_count < domain_limit_num:
                    finalkeywordurl_list.append(i)
                    domain_count += 1
                else:
                    domain_excess_list.append(i)

        # If the number of URLs is below the threshold then append all results to final good list
        else:
            for i in portal_results_dict[each_portal]:
                finalkeywordurl_list.append(i)

    # Inter-site ranking by sorting final result list by jobword confidence
    finalkeywordurl_list = sorted(finalkeywordurl_list, key = lambda x: int(x[1]), reverse=True)

    # Write results and errorlog
    if write_arg:
        from os.path import expanduser

        # Make jorbs directory in user's home directory
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

        # Write results using original manager list
        with open(results_path, "a", encoding='utf8') as writeresults:
            for kk in keywordurl_man_list:
                writeresults.write(str(kk) + "\n")
            '''
            for kk in checkedurls_man_list:
                writeresults.write(kk)
                print(kk)
            '''

        # errorurls_man_dict contents: {workingurl =
        # Write errorlog
        with open(error_path, "a", encoding='utf8') as writeerrors:
            for k, v in errorurls_man_dict.items():
                vk = str((v, '::', k))
                #writeerrors.write(v + ' :: ' + k + '\n\n')
                writeerrors.write(vk + '\n\n')

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

            ## Must have current crawl level in every errorurls_man_dict entry or you'll get error here
            # List based on crawl level and if URL in a portal list
            if k[2] < 1:
                if k[2] in civ_list[0] or k[2] in school_list[0] or k[2] in uni_list[0]:
                    portal_error_list.append(v)

    # Stop timer and display stats
    duration = datetime.datetime.now() - startTime
    print('\n\nPages checked =', len(checkedurls_man_list))
    if verbose_arg:
        for i in checkedurls_man_list: print(i)
    print('Pages skipped =', skipped_pages.value, '\nDuration =', duration.seconds, 'seconds\nPage/sec/proc =', str((len(checkedurls_man_list) / duration.seconds) / num_procs)[:4], '\nErrors detected =', len(errorurls_man_dict), error_rate_desc, '\nPortal errors =', len(portal_error_list), '\n')

    # Display errors
    if len(errorurls_man_dict.values()) > 0:
        error1_tally, error2_tally, error3_tally, error4_tally, error5_tally, error6_tally = (0,)*6

        for i in errorurls_man_dict.values():
            if 'error 1: ' in i: error1_tally += 1
            if 'error 2: ' in i: error2_tally += 1
            if 'error 3: ' in i: error3_tally += 1
            if 'error 4: ' in i: error4_tally += 1
            if 'error 5: ' in i: error5_tally += 1
            if 'error 6: ' in i: error6_tally += 1


        print('   Error code:     Description | Frequency')
        print('  -----------------------------|-------------')
        print('      Error 1:     fatal error |', error1_tally)
        print('      Error 2:       no scheme |', error2_tally)
        print('      Error 3: request timeout |', error3_tally)
        print('      Error 4:  HTTP 404 / 403 |', error4_tally)
        print('      Error 5:   other request |', error5_tally)
        print('      Error 6:     HTML decode |', error6_tally)



    # Display results
    print('\n\n\n   +++++++++++++++++   ', len(finalkeywordurl_list), ' matches found ', '   +++++++++++++++++\n')
    for i in finalkeywordurl_list:
        print(i[0].strip(), i[1])

    # Open results in browser
    if len(finalkeywordurl_list) > 0:
        print('\n\n Open all', len(finalkeywordurl_list), 'matches in browser?\ny/n\n')
        browserresp = input()
        if browserresp.lower() == 'y' or browserresp.lower() == 'yes':
            for eachbrowserresult in finalkeywordurl_list:
                webbrowser.open(eachbrowserresult[0], new=2)
                time.sleep(.4)

    # Display domain_excess_list
    if len(domain_excess_list) > 0:
        print('\n\n Domain limit exceedances:')
        for i in domain_excess_list:
            print(i)
        print('\n\n', len(domain_excess_list), 'Domain limit exceedances.\n These matches have been seperated because they are probably duplicates.\n\n\n')

    # Open portal URL errors in browser
    if len(portal_error_list) > 0:
        print('\n\n Portal error URLs:')
        for i in portal_error_list:
            print(i)
        print('\n\n Unable to search these', len(portal_error_list), 'portal URLs. \n Open them in browser?\ny/n\n')
        browserresp_e = input()
        if browserresp_e.lower() == 'y' or browserresp_e.lower() == 'yes':
            for i in portal_error_list:
                webbrowser.open(i, new=2)
                time.sleep(.4)

    ##
    print('disagree_list =', disagree_list)



"""






import re


listlist = []
keep = []
conv = []

# Find lists initialized by brackets
listlist = re.findall('\w+(?= ?= ?\[.*?\])', orig, flags=re.DOTALL)

# Find lists initialized by list()
listlist2 = re.findall('\w+(?= ?= ?list\()', orig, flags=re.DOTALL)
if listlist2:
    for i in listlist2:
        listlist.append(i)

print('\nFound', len(listlist), 'lists.')

# Mutators
mut_l = ['.append(', '.clear(', '.extend(', '.insert(', '.pop(', '.remove(', '.reverse(', '.sort(']


# Excluded lists that use a mutator
for i in listlist:
    for x in mut_l:
        mut = str(i) + x
        #print(mut)
        if mut in orig:
            #listlist.remove(i)
            keep.append(i)
            break
    else:
        conv.append(i)


print('\n\n  Keep as lists:')
for i in keep:
    print(i)


print('\n\n  Convert to tuples:')
for i in conv:
    print(i)



























