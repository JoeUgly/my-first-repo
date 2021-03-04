
# Description: Crawl and scrape the visible text from NYS civil service and school webpages
# Version: 2.2





# check recurring fallback successes
# broken pipe still
# clean up dbs
# add timeout to garbage collect +
# save objs to file when scraper finishes. as function +-
# use splash on jj.com instead of ping?
# fix cml save so it is recoverable after scraper completes +
# digitaltowpath urls fail +
# combine uni dbs +
# merge with work dbs +
# toggle http/https on recurring failing urls +

# fallback to non dynamic html reqs after exhausting sel +
# new requests_html lib. does not render JS properly
#   new cookiejar
# fix requests ssl
# catch specific errors for sel and reqs
# does sel ever solve a fatal splash error? yeah. get more specific errors from splash:
#   https://docs.scrapy.org/en/latest/topics/request-response.html#using-errbacks-to-catch-exceptions-in-request-processing
#   https://stackoverflow.com/questions/41594401/scrapyslash-masks-404
#   sometimes sel recovers from even its own empty vis text error after a retry


# winter update project:
#   which scraper to use?
#   use double quotes. watch out for replacing possesive apostrophes
#   update em urls and home urls
#   search for new em urls and home urls
#   verify coords?
#   use grudbs for scraper
# find out which home urls should be https. use redirect script
# check which em urls fail consistently. run redirect or google search script (auto?)
# document which orgs use a centralized service and exclude or include them from jj search. ie: applitrack/caboces, applitrack/penfield, etc
# dups in db. probably causes the dups found in cml




# scraper to do:
# put term out into dir if many files will continue
# many jj_error 7s. are mostly soft 404s and must enable javascript errors. cannot reproduce with manual reqs
# sort results to either regular dir or empty vis text dir (for debugging)
# fix sel iframes. how handle nested iframes? only first level iframes? limit num? + change to two levels?
# portal fallback to domain or homeurl? currently domain. home then domain?
# multiple fallback_success per entry in errorlog - not anymore
# mark all nonlogged errors with underscore or remove try block
# should global vars and import statements be in top level or under __name__ == main? move as much as possible to under main?
# use both a domain limiter and a limiter based on full url (except query)?
# splash returns code 200 on soft 404. https://www.tompkinscortland.edu/%20https:/forms.tc3.edu/forms/employment
# do not count jj_error 2 (forbidden content type) as error. mark as skip -
# create unique codes for all skips. print and mark in cml
# jj error 7 might be reduced by falling back to https -
# improve bunkwords: mark all skips in outcome. dont use list comprehension? print offending bunkword and context


# results.py to do:
# display url only once. multiple orgs can share a url +
# combine uni zip dicts +
# remove zip_form? display purposes only. keep
# show jj_error num in tooltip on error tabs?
# improve code comments
# optimise: two separate sections. one with geolimter function
# reword error pages to discourage refreshing?
# sort errors by alpha?
# sort results by jbw conf or fuzzy match percent? user specified -
# percent decode urls
# wraparound text for mobile?


# index.html to do:
# dup zip codes
# fix indents
# obfuscate
# improve code comments
# zip_dict one entry per line?
# hide modal after back button without refresh - difficult
# show progress on modal - difficult
# create favicon


# to do later:
# allow multiple em urls for each org name in db?
# wait for splash as function
# investigate multi thread vs multi proc. active_children > active_count, all others > good luck
# replace repr and eval with json loads and dumps
# run scraper as cron job
# what is portal url used for?? starts as homepage from db entry.
# malformed url in results: ttps:/www.cs.ny.gov
# excess errors per entry. https://www.cnr.edu/employment-opportunities, jj_error 3, HTTP timeout, 0, uni, Coll New Rochelle Dist Coun 31 Cmps, jj_error 3, HTTP timeout, 0, jj_error 3, HTTP timeout, 0, jj_error 3, HTTP timeout, 0, jj_error 3, HTTP timeout, 0, jj_error 3, HTTP timeout, 0. might be caused by a fatal splash error then resuming?
# put all errors in add_errorurls_f. eg: __error ...
# "None" in cml. prob from redirects, skipping, or fatal error
# dups in checked pages
# urls not found in cml
# reduce redundant dup checker calls
# jbws back to count but limit to x occurrences?
# combine high conf scan and jbw search into one for loop
# save all redirects to cml using resp.history
# decompose nav tags?
# content of script tags not decomposing because Splash evaluates scripts. So there is no script tag header or footer for BS to read: https://recruiting.ultipro.com/BRY1002BSC/JobBoard/6b838b9a-cd2b-436a-903b-0de7b6e17b4f/?q=&o=postedDateDesc
# max crawl depth 3? -
# remove non printable characters from result text? -
# phase out blacklist
# weighted jbws
# upgrade server to 20.04



# false positives: include keyword and date
# https://www.herkimer.edu/about/employment/
# https://hr.cornell.edu/jobs       librarian 1/20
# https://www.newvisions.org/pages/media-centers-for-the-21st-century
# https://www.tbafcs.org/Page/1444  nurse 2/20 dropdown


# All fallback types: sel fb, static fb, portal to domain fb, include_old fb


# Concerns:
# allow multiple orgs to share a url + Will give duplicate results. Better than missing results due to geo limiter or arbitrarily choosing only one org to use that url

# Only scrape if em URL is present?

# Dup checker: 
# remove after ampersand in query?
# remove fragments and trailing slash. yes
# case sensitivity. yes

# High conf: exclude good low conf links
# https://www.cityofnewburgh-ny.gov/civil-service = upcoming exams
# http://www.albanycounty.com/Government/Departments/DepartmentofCivilService.aspx = exam announcement
# have separate high conf jbw lists?

# Bunkwords: search entire element or just contents?
# must search url to exclude .pdf, etc

# Decompose: drop down menus?
# dont decompose menus for anchor tag search +

# No space between elements' content in results
# caused by converting from soup to soup.text
# eg: Corporation Counsel</option><option>Downtown Parking Improvement
# produces this: developmentcorporation counseldowntown parking improvement planengineeringethics
# this shouldn't matter because a keyword probably won't span accross multiple elements

# use urllib or manual replace to percent encode urls?
# url_path = workingurl.replace('/', '%2F')  # or
# url_path = urllib.parse.quote(workingurl, safe=':')








import datetime, requests, psutil, json, os, queue, re, time, traceback, urllib.parse, glob, shutil, sys
from multiprocessing import active_children, Lock, Manager, Process, Queue, Value
from math import sin, cos, sqrt, atan2, radians
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options




# Start timer
startTime = datetime.datetime.now()

# User agent
user_agent_str = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'

# Compile regex paterns for reducing whitespace in written files
white_reg = re.compile("\s{2,}")

# Compile regex paterns for finding hidden HTML elements
style_reg = re.compile("(display\s*:\s*(none|block);?|visibility\s*:\s*hidden;?)")
class_reg = re.compile('(hidden-sections?|dropdown|has-dropdown|sw-channel-dropdown|dropdown-toggle)')

## unn?
# Omit these pages
blacklist = ('cc.cnyric.org/districtpage.cfm?pageid=112', 'co.essex.ny.us/personnel', 'co.ontario.ny.us/94/human-resources', 'countyherkimer.digitaltowpath.org:10069/content/departments/view/9:field=services;/content/departmentservices/view/190', 'countyherkimer.digitaltowpath.org:10069/content/departments/view/9:field=services;/content/departmentservices/view/35', 'cs.monroecounty.gov/mccs/lists', 'herkimercounty.org/content/departments/view/9:field=services;/content/departmentservices/view/190', 'herkimercounty.org/content/departments/view/9:field=services;/content/departmentservices/view/35', 'jobs.albanyny.gov/default/jobs', 'monroecounty.gov/hr/lists', 'monroecounty.gov/mccs/lists', 'mycivilservice.rocklandgov.com/default/jobs', 'niagaracounty.com/employment/eligible-lists', 'ogdensburg.org/index.aspx?nid=345', 'penfield.org/multirss.php', 'tompkinscivilservice.org/civilservice/jobs', 'tompkinscivilservice.org/civilservice/jobs', 'swedishinstitute.edu/employment-at-swedish-institute', 'sunyacc.edu/job-listings')


# Include links that include any of these
# High confidence civ jbws
jobwords_civ_high = ('continuous recruitment', 'employment', 'job listing', 'job opening', 'job posting', 'job announcement', 'job opportunities', 'job vacancies', 'jobs available', 'available positions', 'open positions', 'available employment', 'career opportunities', 'employment opportunities', 'current vacancies', 'current job', 'current employment', 'current opening', 'current posting', 'current opportunities', 'careers at', 'jobs at', 'jobs @', 'work at', 'employment at', 'find your career', 'browse jobs', 'search jobs', 'vacancy postings', 'vacancy list', 'prospective employees', 'help wanted', 'work with', 'immediate opportunities', 'promotional announcements', 'upcoming exam', 'exam announcement', 'examination announcement', 'examinations list', 'civil service opportunities', 'civil service exam', 'civil service test', 'current civil service','open competitive', 'open-competitive')

# Low confidence civ jbws
jobwords_civ_low = ('open to', 'join', 'job', 'job seeker', 'job title', 'positions', 'careers', 'human resource', 'personnel', 'vacancies', 'vacancy', 'posting', 'opening', 'recruitment', 'civil service', 'exam', 'examination', 'test', 'current exam')


# High confidence sch and uni jbws
jobwords_su_high = ('continuous recruitment', 'employment', 'job listing', 'job opening', 'job posting', 'job announcement', 'job opportunities', 'job vacancies', 'jobs available', 'available positions', 'open positions', 'available employment', 'career opportunities', 'employment opportunities', 'current vacancies', 'current job', 'current employment', 'current opening', 'current posting', 'current opportunities', 'careers at', 'jobs at', 'jobs @', 'work at', 'employment at', 'find your career', 'browse jobs', 'search jobs', 'vacancy postings', 'vacancy list', 'prospective employees', 'help wanted', 'work with', 'immediate opportunities', 'promotional announcements')

# Low confidence sch and uni jbws
jobwords_su_low = ('join', 'job', 'job seeker', 'job title', 'positions', 'careers', 'human resource', 'personnel', 'vacancies', 'vacancy', 'posting', 'opening', 'recruitment', '>faculty<', '>staff<', '>adjunct<', '>academic<', '>support<', '>instructional<', '>administrative<', '>professional<', '>classified<', '>coaching<')


## application
# Exclude links that contain any of these
bunkwords = ('academics', 'pnwboces.org', 'recruitfront.com', 'schoolapp.wnyric.org', 'professional development', 'career development', 'javascript:', '.pdf', '.jpg', '.ico', '.rtf', '.doc', '.mp4', 'mailto:', 'tel:', 'icon', 'description', 'specs', 'specification', 'guide', 'faq', 'images', 'exam scores', 'resume-sample', 'resume sample', 'directory', 'pupil personnel')



# Multiprocessing lock for shared objects
lock = Lock()





# Removes extra info from urls to prevent duplicate pages from being checked more than once
def dup_checker_f(dup_checker):
    print(os.getpid(), 'start dup check:', dup_checker)

    ## just split without if dup_checker.startswith?
    # Remove scheme
    if dup_checker.startswith('http://') or dup_checker.startswith('https://'):
        dup_checker = dup_checker.split('://')[1]
    else:
        print('__Error__ No scheme at:', dup_checker)

    # Remove www. and variants. This also works with www3. and similar
    if dup_checker.startswith('www'):
        dup_checker = '.'.join(dup_checker.split('.')[1:])


    # Remove fragments
    dup_checker = dup_checker.split('#')[0]

    # Remove double forward slashes outside of scheme
    dup_checker = dup_checker.replace('//', '/')

    # Remove trailing whitespace and slash and then lowercase it
    dup_checker = dup_checker.strip(' \t\n\r/').lower()

    return dup_checker


# Determine if url has been checked already and optionally add to queue
def proceed_f(abspath, working_list, current_crawl_level, add_to_queue_b, workingurl, dup_checker):

    # Exclude checked pages
    for i in checkedurls_man_l:
        if dup_checker == i[0]:
            print(os.getpid(), 'Skipping:', dup_checker)
            with lock: skipped_pages.value += 1

            # Declare not to proceed
            return False


    # Count occurances of domain in cml if URL contains a query
    if '?' in workingurl:
        domain_count = 0

        ## switch to dup checker?
        # Strip off scheme and www to form domain
        domain = workingurl.split('/')[2]
        if domain.startswith('www'):
            domain = '.'.join(domain.split('.')[1:])

        for cml_entry in checkedurls_man_l:
            if domain in cml_entry[0]:
                domain_count += 1
        print(os.getpid(), 'Domain count:', domain_count, dup_checker)

        # Exclude if domain occurance limit is exceeded
        if domain_count > 49:
            print(os.getpid(), 'Domain limit exceeded:', dup_checker)
            with lock: skipped_pages.value += 1

            return False


    # Exclude if the abspath is on the blacklist
    if dup_checker in blacklist:
        print(os.getpid(), 'Blacklist invoked:', dup_checker)
        with lock: skipped_pages.value += 1

        return False



    # Add abspath to queue if add_to_queue_b is True
    if add_to_queue_b:

        # Create new working list: [org name, URL, crawl level, parent URL, jbw type]
        new_working_list = [working_list[0], abspath, current_crawl_level, workingurl, working_list[4]]
        print(os.getpid(), 'Putting list into queue:', new_working_list)
        print(os.getpid(), 'From:', workingurl)

        # Put new working list in queue
        try:
            with lock:
                all_urls_q.put(new_working_list)
                total_count.value += 1
        except Exception as errex:
            print('__Error trying to put into all_urls_q:', errex)

    # Add dup_checker and jbw confidence placeholder to checked pages list
    print(os.getpid(), 'Adding to cml with None:', dup_checker)
    with lock: checkedurls_man_l.append([dup_checker, None])

    # Declare to proceed
    return True



# Update outcome of each URL (dup checker) with jbw conf, error code, or redirected
def outcome_f(url_dup, conf_val, *args):

    # Convert URL to dup checker
    #url = dup_checker_f(url)

    ## Catch multiple matches?
    # Attach jbw conf to URL in checkedurls_man_l
    for each_url in checkedurls_man_l:
        if not each_url:
            print('__Error. (2) None in cml:', checkedurls_man_l)
            continue

        if each_url[0] == url_dup:
            
            remover = each_url
            break

            # Manager will not be aware of updates to items. Must append new item.

    # Catch no match
    else:
        print(os.getpid(), '__Error__ (1) not found in checkedurls_man_l:', repr(url_dup), url_dup.isprintable())
        return

    ## combine next two sections
    ## Remove old entry
    with lock:
        try:
            checkedurls_man_l.remove(remover)
        except Exception as errex:
            print(os.getpid(), '__Error__ (2) not found in checkedurls_man_l:', url_dup)
            print(errex)
            return
            
    ## Append new entry
    new_i = [url_dup, conf_val]

    if args: new_i.append(args[0])

    with lock:
        try:
            checkedurls_man_l.append(new_i)
            print(os.getpid(), 'Updated outcome for/with:', url_dup, conf_val)
        except Exception as errex:
            print(os.getpid(), '__Error__ (3) not found in checkedurls_man_l:', url_dup)
            print(errex)




## loop_type is wacky AF
# Retry loop on request
def looper_f(loop_type, workingurl, current_crawl_level, jbw_type, org_name, workingurl_dup):

    print(os.getpid(), 'Begin request loop:', loop_type.__name__, workingurl)
    
    for loop_count in range(3):

        # Rate limiter
        time.sleep(1)

        # Check internet
        while True:
            if all_pause.value != 0:
                print(os.getpid(), 'all_pause detected. Waiting ...')
                time.sleep(4)
            else: break


        # Get html and redirected url as tuple from the requester function stored in loop_type
        looper_return_l = loop_type(workingurl, current_crawl_level, jbw_type, org_name, workingurl_dup)


        # Requester returns True to indicate a needed retry
        if looper_return_l[0] == True:
            print(os.getpid(), loop_count, 'Retry request loop:', loop_type.__name__, workingurl)
            continue

        # Requester returns False to indicate don't retry
        elif looper_return_l[0] == False:
            print(os.getpid(), loop_count, 'Break request loop:', loop_type.__name__, workingurl)
            break

        # Requester returns 'empty_vis' to indicate retry with Sel
        elif looper_return_l[0] == 'empty_vis':
            print(os.getpid(), loop_count, 'Break request loop:', loop_type.__name__, workingurl)
            looper_return_l[0] = True
            break

        # Declare successful
        else:
            print(os.getpid(), loop_count, 'Success: HTML request:', loop_type.__name__, workingurl)
            break


    # Loop is exhausted
    else:
        print(os.getpid(), 'Loop exhausted:', loop_type.__name__, workingurl)
        #looper_return_l[0] = False # Mark it as a failure


    # looper_return_l will be: [True/False/'empty_vis', loop_type] or [soup, vis_soup, red_url, loop_type]
    looper_return_l.append(loop_type.__name__)
    return looper_return_l



            

## returns html and red url OR True/False and workingurl??
# Splash HTML request function
def splash_requester_f(workingurl, current_crawl_level, jbw_type, org_name, workingurl_dup):


    # Check if Splash is restarting
    while dock_pause.value > 0: time.sleep(2)

    # Begin HTML request
    try:

        # Tell the manager that this process is not ready for Splash to restart
        with lock: using_splash.value += 1

        # Make request on port 8050 so Splash handles it
        with requests.post('http://localhost:8050/render.json', json={
            'url': workingurl,
            'headers': {'User-Agent': user_agent_str}, # Spoof user agent
            'plugins_enabled': 'true', # May help with rendering
            'indexeddb_enabled': 'true', # May help with rendering
            'wait': 1, # Wait for dyanamic content to render
            'viewport': 'full', # Render the entire page ## replacement for 'render_all': 1
            'html': 1, # Static HTML
            'iframes': 1, # Dynamic content. JSON element is called 'childFrames'
            'images': 0, # Disable images for speed
            'geometry': 0, # Exclude unnecessary items
            'timeout': 10, # Timeout for the render
            'resource_timeout': 15 # Timeout for individual network requests
            }) as resp:


            # Get status code
            stat_code = resp.status_code

            # Catch errors
            if stat_code != 200:
                print(os.getpid(), 'stat_code=', stat_code, workingurl)

                # Get relevant error info
                ## stat_info for timeout errors will be a dict, not a string. Also it will not have ['info']['text']
                try:
                    stat_info = json.loads(resp.text)['info']['text']
                except:
                    stat_info = str(json.loads(resp.text)['info'])
                print(os.getpid(), 'status=', stat_info, workingurl)

                ## splash groups 4xx and 5xx errors into 'host not found'
                # Don't retry on 404 or 403 error
                if stat_info.endswith('not found'):
                    print(os.getpid(), 'jj_error 4: HTTP 404/403 request:', workingurl)
                    add_errorurls_f(workingurl, 'jj_error 4', 'Host not found', current_crawl_level, jbw_type, org_name, workingurl_dup)
                    return [False] # Declare not to retry

                # Retry on timeout errors
                elif stat_info.startswith("{'remaining': -"):
                    print(os.getpid(), 'jj_error 3: HTTP timeout:', workingurl)
                    add_errorurls_f(workingurl, 'jj_error 3', 'HTTP timeout', current_crawl_level, jbw_type, org_name, workingurl_dup)
                    return [True] # Declare to retry

                # Don't retry on non HTML errors (eg: pdf)
                elif stat_info == 'Frame load interrupted by policy change':
                    print(os.getpid(), 'jj_error 2: non-HTML detected:', workingurl)
                    add_errorurls_f(workingurl, 'jj_error 2', 'Forbidden content type', current_crawl_level, jbw_type, org_name, workingurl_dup)
                    return [False] # Declare not to retry


                # Retry on other error
                else:
                    print(os.getpid(), 'jj_error 5: Other request', workingurl)
                    stat_info = str(stat_code) + ' ' + stat_info ## yeah, just leave it
                    add_errorurls_f(workingurl, 'jj_error 5', stat_info, current_crawl_level, jbw_type, org_name, workingurl_dup)
                    return [True] # Declare to retry
            

            # Status code 200
            else:

                # Redirected URL
                red_url = json.loads(resp.text)['url']

                # Get HTML and dynamic content
                html_text = json.loads(resp.text)['html']
                dy_text = json.loads(resp.text)['childFrames']

                # Combine HTML and dynamic content
                rendered_html = html_text + str(dy_text)


                # Check vis soup
                vis_soup_t = vis_soup_f(workingurl, rendered_html)
                soup = vis_soup_t[0]
                vis_soup = vis_soup_t[1]


                # Skip if there is no useable visible text
                if len(vis_soup) < empty_cutoff:

                    # Mark error
                    print(os.getpid(), 'jj_error 7a: Empty vis text:', workingurl, len(vis_soup))
                    add_errorurls_f(workingurl, 'jj_error 7a', 'Empty vis text', current_crawl_level, jbw_type, org_name, workingurl_dup)


                    err7_dir = '/home/joepers/Desktop/jj_error7'


                    # Replace forward slashes so they aren't read as directory boundaries
                    ## alternative: url_path = workingurl.replace('/', '%2F')
                    url_path = urllib.parse.quote(workingurl, safe=':')
                    html_path = os.path.join(err7_dir, url_path)


                    # Write HTML to text file using url name (max length is 255)
                    with open(html_path[:254], "w", encoding='ascii', errors='ignore') as write_html:
                        write_html.write(vis_soup)

                    print(os.getpid(), 'Success: Write:', url_path)


                    
                    # Retry with next requester
                    return ['empty_vis']


                # Return [soup, vis_soup, red_url]
                return [soup, vis_soup, red_url]


    # Catch and log HTTP request errors
    except Exception as errex:

        # Try to halt the plague
        #if 'Remote end closed connection without response' in str(errex):
        with lock: dock_pause.value = 1
        print('__Forcing dock pause now!!!')
        
        # Retry on other error
        print(os.getpid(), 'jj_error 6: Other request', workingurl, errex, '__Problem line no:', sys.exc_info()[2].tb_lineno)
        add_errorurls_f(workingurl, 'jj_error 6', str(errex), current_crawl_level, jbw_type, org_name, workingurl_dup)

        return [True]


    # Tell the manager that this process is ready for Splash to restart
    finally:
        with lock: using_splash.value -= 1



# Selenium HTML request function
def sel_requester_f(workingurl, current_crawl_level, jbw_type, org_name, workingurl_dup):

    # Prevent too many procs running Sel concurrently
    while sel_count.value >= round(num_procs / 4):
        print(os.getpid(), 'Max number of Sel instances reached. Waiting ...')
        time.sleep(3)

    with lock: sel_count.value += 1


    try:
        options = Options()
        options.add_argument('--headless')

        driver = webdriver.Firefox(options=options, executable_path=r'/home/joepers/Downloads/geckodriver')

        driver.set_page_load_timeout(12)
        driver.get(workingurl) # Request

        rendered_html = driver.page_source
        red_url = driver.current_url

        # Include iframes
        ## this does not include nested iframes
        sel_c = 0
        while True:
            try:
                driver.switch_to.frame(sel_c)
                rendered_html += driver.page_source
                sel_c += 1
            
            except: break # Exit loop if no more iframes
            driver.switch_to.default_content() # Return to main frame after each recursion


        # Check vis soup
        vis_soup_t = vis_soup_f(workingurl, rendered_html)
        soup = vis_soup_t[0]
        vis_soup = vis_soup_t[1]

        # Skip if there is no useable visible text
        if len(vis_soup) < empty_cutoff:

            # Mark error
            print(os.getpid(), 'jj_error 7b: Empty vis text:', workingurl, len(vis_soup))
            add_errorurls_f(workingurl, 'jj_error 7b', 'Empty vis text', current_crawl_level, jbw_type, org_name, workingurl_dup)
            
            # Retry with next requester
            return ['empty_vis']


        # Return HTML and redirected URL
        return [soup, vis_soup, red_url]


    # Catch and log HTTP request errors
    except Exception as errex:
        ## check this
        # Retry on all errors
        print(os.getpid(), 'jj_error 8: Sel request', workingurl, errex, sys.exc_info()[2].tb_lineno)
        add_errorurls_f(workingurl, 'jj_error 8', str(errex), current_crawl_level, jbw_type, org_name, workingurl_dup)

        return [True]

    # Close Sel
    finally:
        if 'driver' in locals():
            driver.close()
            driver.quit()
        else: print(os.getpid(), 'Var named "driver" does not exist')
        with lock: sel_count.value -= 1



# Static HTML requester
def static_requester_f(workingurl, current_crawl_level, jbw_type, org_name, workingurl_dup):
    try:
        resp = requests.get(workingurl, timeout=15, headers={'User-Agent': user_agent_str}, verify=False)
        red_url = resp.url
 
        # Check vis soup
        vis_soup_t = vis_soup_f(workingurl, resp.text)
        soup = vis_soup_t[0]
        vis_soup = vis_soup_t[1]

        # Skip if there is no useable visible text
        if len(vis_soup) < empty_cutoff:

            # Mark error
            print(os.getpid(), 'jj_error 7c: Empty vis text:', workingurl, len(vis_soup))
            add_errorurls_f(workingurl, 'jj_error 7c', 'Empty vis text', current_crawl_level, jbw_type, org_name, workingurl_dup)
            
            return [False]

        # Success
        return [soup, vis_soup, red_url]


    # Catch and log request errors
    except Exception as errex:
        print(os.getpid(), 'jj_error 9: Static request', workingurl, errex, sys.exc_info()[2].tb_lineno)
        add_errorurls_f(workingurl, 'jj_error 9', str(errex), current_crawl_level, jbw_type, org_name, workingurl_dup)

        return [True]



# url: [[org name, db type, crawl level], [[error number, error desc], [error number, error desc]], [final error flag, fallback flags]]
# Append URLs and info to the errorlog. Allows multiple errors (values) to each URL (key)
def add_errorurls_f(workingurl, err_code, err_desc, current_crawl_level, jbw_type, org_name, workingurl_dup):

    # Remove commas from text to prevent splitting errors when reading errorlog
    err_desc = err_desc.replace(',', '').strip()

    # First error for this url
    if not workingurl in errorurls_man_d:
        with lock: errorurls_man_d[workingurl] = [[org_name, jbw_type, current_crawl_level], [[err_desc, err_code]]]

    # Not the first error for this url
    else:

        # Manager will not be aware of update (append) to dict value. Must overwrite key/value
        prev_item = errorurls_man_d[workingurl]
        prev_item[1].append([err_desc, err_code])

        try:
            with lock: errorurls_man_d[workingurl] = prev_item
        except Exception as errex: print(errex)


    # Update checked pages conf value to error code
    outcome_f(workingurl_dup, err_code)


# Mark final errors in errorlog
def final_error_f(workingurl):

        # Manager will not be aware of update to dict item unless you do this
        prev_item = errorurls_man_d[workingurl]
        prev_item.append(['jj_final_error'])

        with lock:
            try:
                errorurls_man_d[workingurl] = prev_item
            except Exception as errex:
                print(errex)


# Separate the visible text from HTML
def vis_soup_f(workingurl, html):

    # Select body
    soup = BeautifulSoup(html, 'html5lib')
    soup = soup.find('body')

    ## unn
    if soup is None:
        print(os.getpid(), '__Empty soup0:', workingurl)
        return False

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
    # Remove unnecessary whitespace. eg: multiple newlines, spaces, and tabs
    vis_soup = str(vis_soup.text)
    vis_soup = re.sub(white_reg, " ", vis_soup)


    return soup, vis_soup





# Define the crawling function
def scraper():
    print(os.getpid(), '====== Start scraper function ======')


    while True:

        # Get a url list from the queue
        try:
            with lock:
                working_list = all_urls_q.get(False)

        # If queue is empty wait and try again
        except queue.Empty:
            print(os.getpid(), 'Queue empty on first attempt. Trying again...')
            time.sleep(10)
            try:
                with lock:
                    working_list = all_urls_q.get(False)

            # Exit function if queue is empty again
            except queue.Empty:
                print(os.getpid(), 'Queue empty. Closing process...')
                break


        # Begin fetching
        try:
            print(os.getpid(), 'New working_list =', working_list)

            # working_list contents: [org name, workingurl, crawl level, parent URL, jbw type]
            org_name = working_list[0]
            workingurl = working_list[1]
            current_crawl_level = working_list[2]
            parent_url = working_list[3]
            jbw_type = working_list[4]

            workingurl_dup = dup_checker_f(workingurl)

            # Form domain by splitting after 3rd slash
            domain = '/'.join(workingurl.split('/')[:3])


            # Begin Splash request attempts
            # [True/False, loop_type] or [soup, vis_soup, red_url, loop_type]
            looper_return_l = looper_f(splash_requester_f, workingurl, current_crawl_level, jbw_type, org_name, workingurl_dup)

            # Fallback to Selenium requests on non fatal Splash failures
            if looper_return_l[0] == True:
                looper_return_l = looper_f(sel_requester_f, workingurl, current_crawl_level, jbw_type, org_name, workingurl_dup)

                # Fallback to static requests on non fatal Selenium failures
                if looper_return_l[0] == True:
                    looper_return_l = looper_f(static_requester_f, workingurl, current_crawl_level, jbw_type, org_name, workingurl_dup)



            # Request failure
            # Splash fatal error or Sel fail
            if type(looper_return_l[0]) == bool:

                # Mark error as final error
                final_error_f(workingurl)

                # If portal request failed, use domain as fallback one time
                if current_crawl_level == 0:

                    ## compare dups?
                    # Skip if url is same as the domain
                    if workingurl != domain:

                        domain_dup = dup_checker_f(domain)

                        # Put fallback url into queue with -1 current crawl level
                        print(os.getpid(), 'Using URL fallback:', domain)
                        add_to_queue_b = True
                        proceed_f(domain, working_list, -1, add_to_queue_b, workingurl, domain_dup)


                # Skip to next URL on fatal error
                continue


            # Request success
            # Check if this is a domain fallback attempt. ie: portal failed so now using domain instead. don't count as portal error
            if current_crawl_level < 0:
                print(os.getpid(), 'Success: Domain fallback: Overwriting parent_url error:', parent_url)
            
                # Manager will not be aware of update to dict item unless you do this
                prev_item = errorurls_man_d[parent_url]
                prev_item[-1].append('fallback_success')
                print(os.getpid(), prev_item)

                # Mark errorlog portal url entry as successful fallback
                with lock:
                    try:
                        errorurls_man_d[parent_url] = prev_item
                    except Exception as errex:
                        print(errex)


            # [soup, vis_soup, red_url, loop_type]
            soup = looper_return_l[0]
            vis_soup = looper_return_l[1]
            red_url = looper_return_l[2]
            browser = looper_return_l[3]


            # Remove non ascii characters, strip, percent encode
            #red_url = red_url.encode('ascii', 'ignore').decode().strip()
            #red_url = urllib.parse.quote(red_url, safe='/:')

            # Prevent trivial changes (eg: https upgrade) from being viewed as different urls
            if workingurl != red_url:
                red_url_dup = dup_checker_f(red_url)

                # Follow redirects
                if workingurl_dup != red_url_dup:
                    print(os.getpid(), 'Redirect from/to:', workingurl, red_url)

                    # Update checked pages conf value to redirected
                    conf_val = 'redirected'
                    outcome_f(workingurl_dup, conf_val, browser)

                    # Assign new redirected url
                    workingurl = red_url
                    workingurl_dup = red_url_dup

                    # Skip checked pages using redirected URL
                    add_to_queue_b = False
                    proceed_pass = proceed_f(red_url, working_list, current_crawl_level, add_to_queue_b, workingurl, red_url_dup)

                    # Break request loop if redirected URL has been checked already
                    if not proceed_pass: continue



            # Use lowercase visible text for comparisons
            vis_soup = vis_soup.lower()

            # Set jbw type based on jbw type
            if jbw_type == 'civ':
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

            # Update outcome in checkedurls_man_l
            outcome_f(workingurl_dup, jbw_count, browser)


            # Don't save the fallback domain
            if current_crawl_level > -1:

                # Make jbw type dirs inside date dir
                dated_results_path = os.path.join(dater_path, 'results', jbw_type)
                if not os.path.exists(dated_results_path):
                    os.makedirs(dated_results_path)


                # Make directory using org name
                org_path = os.path.join(dated_results_path, org_name)
                if not os.path.exists(org_path):
                    os.makedirs(org_path)

                # Replace forward slashes so they aren't read as directory boundaries
                ## alternative: url_path = workingurl.replace('/', '%2F')
                url_path = urllib.parse.quote(workingurl, safe=':')
                html_path = os.path.join(org_path, url_path)

                # Combine jbw conf, browser, and vis soup into a str. Separate by ascii delim char
                file_contents_s = str(jbw_count) + '\x1f' + browser + '\x1f' + vis_soup

                # Write HTML to text file using url name (max length is 255)
                with open(html_path[:254], "w", encoding='ascii', errors='ignore') as write_html:
                    write_html.write(file_contents_s)

                print(os.getpid(), 'Success: Write:', url_path)


            # Search for pagination class before checking crawl level
            for i in soup.find_all(class_='pagination'):

                # Find anchor tags
                for ii in i.find_all('a'):

                    # Find "next" page url
                    if ii.text.lower() == 'next':

                        # Get absolute url
                        abspath = urllib.parse.urljoin(domain, ii.get('href'))

                        # Dup checker must be called prior to proceed_f
                        dup_checker = dup_checker_f(abspath)

                        # Add to queue
                        print(os.getpid(), workingurl, 'Adding pagination url:', abspath)
                        add_to_queue_b = True
                        proceed_f(abspath, working_list, current_crawl_level, add_to_queue_b, workingurl, dup_checker)



            # Start relavent crawler
            if current_crawl_level >= max_crawl_depth:
                continue

            # Increment crawl level
            print(os.getpid(), 'Starting crawler:', workingurl)
            current_crawl_level += 1

            # separate soup into anchor tags
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
                if any(ttt in bs_contents for ttt in jobwords_high_conf):
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

                ## wut?
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

            # Print all links found
            print(os.getpid(), 'links from', workingurl, fin_l)
                
            # Prepare the URL for entry into the queue
            for fin_tag in fin_l:

                '''
                # Jbw tally
                lower_tag = str(fin_tag).lower()
                for i in jobwords_low_conf:
                    if i in lower_tag:
                        with lock: jbw_tally_man_l.append(i)

                for i in jobwords_high_conf:
                    if i in lower_tag:
                        with lock: jbw_tally_man_l.append(i)
                '''

                # Get url from anchor tag
                if fin_tag.name == 'a':
                    bs_url = fin_tag.get('href')

                # Get url from child anchor tag
                else:
                    bs_url = fin_tag.find('a').get('href')

                # Convert relative paths to absolute
                abspath = urllib.parse.urljoin(domain, bs_url)

                # Remove non printed characters, strip, and replace spaces
                #abspath = abspath.encode('ascii', 'ignore').decode().strip()
                #abspath = urllib.parse.quote(abspath)

                # Dup checker must be called prior to proceed_f
                dup_checker = dup_checker_f(abspath)

                # Add to new link queue
                add_to_queue_b = True
                proceed_f(abspath, working_list, current_crawl_level, add_to_queue_b, workingurl, dup_checker)



        # Catch all other errors
        except Exception as errex:
            print(os.getpid(), 'jj_error 1: Unknown error detected. Skipping...', str(traceback.format_exc()), workingurl)
            add_errorurls_f(workingurl, 'jj_error 1', str(errex), current_crawl_level, jbw_type, org_name, workingurl_dup)

            # Mark error as final error
            final_error_f(workingurl)

            # Update outcome
            conf_val = 'jj_error 1'
            outcome_f(workingurl_dup, conf_val)
            continue


        # Declare the task has finished
        finally: 
            with lock: prog_count.value += 1





# Multiprocessing
if __name__ == '__main__':

    import docker, subprocess


    # Write shared objects to file to save progress and restart Docker
    def save_objs_f():
        
        # Get items from queue
        queue_list = []
        while all_urls_q.qsize() > 0:
            queue_item = all_urls_q.get()
            queue_list.append(queue_item)

        # Return items to queue
        for queue_item in queue_list: 
            all_urls_q.put(queue_item)

        # Queue list
        with open(queue_path, "w") as queue_file:
            queue_file.write(repr(queue_list))

        # CML
        with open(checked_path, "w") as cml_file:
            cml_file.write(repr(list(checkedurls_man_l)))

        # Errorlog
        with open(error_path, "w") as error_file:
            error_file.write(repr(dict(errorurls_man_d)))

        # Multi org dict
        with open(multi_d_path, "w") as multi_d_file:
            multi_d_file.write(repr(dict(multi_d)))



    with open('/home/joepers/code/jj_v22/dbs/civ_db', 'r') as f:
        civ_tup = json.loads(f.read())

    with open('/home/joepers/code/jj_v22/dbs/sch_db', 'r') as f:
        sch_tup = json.loads(f.read())

    with open('/home/joepers/code/jj_v22/dbs/uni_db', 'r') as f:
        uni_tup = json.loads(f.read())



    '''
    # Testing purposes
    civ_tup = [
["City of Albany", "https://jobs.albanyny.gov/jobopps", "http://www.albanyny.org"],
["City of Amsterdam", "https://www.amsterdamny.gov/government/employment-opportunities", "http://www.amsterdamny.gov/"],
    ]
    sch_tup = []
    uni_tup = []
    '''




    # Make date dir to put results into
    jorb_home = '/home/joepers/joes_jorbs'
    dater = datetime.datetime.now().strftime("%x").replace('/', '_')
    dater_path = os.path.join(jorb_home, dater)



    # Scraper options
    max_crawl_depth = 1
    num_procs = 12
    max_mem_usage = 75
    empty_cutoff = 200 # Num of characters in webpage text file to be considered empty



    # Set Docker python client
    client = docker.from_env()


    # Wait for Splash to be ready
    while True:
        try:
            resp = requests.post('http://localhost:8050/_gc', timeout=10)
            print(os.getpid(), 'Splash is running')
            break

        except Exception as temp_e:
            if 'Connection reset by peer' in str(temp_e):
                print(os.getpid(), '...')
                time.sleep(1)
                continue


    # Get container name
    container = client.containers.get('jj_con')


    # Put all working URLs and relevant data (working_list) in this queue
    all_urls_q = Queue()

    # Create manager to share objects between processes
    manager = Manager()

    # Debugging
    #jbw_tally_man_l = manager.list() # Used to determine the frequency that jbws are used

    # Set paths to files
    queue_path = os.path.join(dater_path, 'queue')
    checked_path = os.path.join(dater_path, 'checked_pages')
    error_path = os.path.join(dater_path, 'errorlog')
    multi_d_path = os.path.join(dater_path, 'multi_d')

    # Resume scraping using leftover results from the previously failed scraping attempt
    try:

        # Read queue file as list
        with open(queue_path) as f:
            temp_obj = eval(f.read())

        # Put URLs into queue
        print('Attempting file queue')
        for i in temp_obj:
            all_urls_q.put(i)
        print('queue recovery complete')

        # Read errorlog file as dict
        with open(error_path) as f:
            temp_obj = eval(f.read())
            errorurls_man_d = manager.dict(temp_obj)
        print('errorlog recovery complete')

        # Read CML file as list
        with open(checked_path) as f:
            temp_obj = eval(f.read())
            checkedurls_man_l = manager.list(temp_obj)
        print('CML recovery complete')

        # Read multi_d file as dict
        with open(multi_d_path) as f:
            temp_obj = eval(f.read())
            multi_d = dict(temp_obj)
        print('multi_d recovery complete')

        print('File queue success')


    # Use original queue
    except Exception as errex:
        print(errex, '\nUsing original queue')

        # Start with empty manager objects
        all_urls_q = Queue() # Put all working URLs and relevant data (working_list) in this queue
        checkedurls_man_l = manager.list() # URLs that have been checked with their outcome: jbw conf or error
        errorurls_man_d = manager.dict() # URLs that have resulted in an error

        # Nested dicts for multiple orgs covered by a URL 
        multi_d = {}
        multi_d['civ'] = {}
        multi_d['sch'] = {}
        multi_d['uni'] = {}



        # Put civil service URLs into queue
        for i in civ_tup:
            org_name = i[0]
            em_url = i[1]

		    # Skip if em URL is missing or marked
            if not em_url: continue
            if em_url.startswith('_'): continue

            # URL as key, all org names using that URL as values
            try: multi_d['civ'][em_url].append(org_name) # Not first org using this URL
            except: 
                multi_d['civ'][em_url] = [org_name] # First org using this URL

                # Put org name, em URL, initial crawl level, homepage, and jbws type into queue
                all_urls_q.put([org_name, em_url, 0, i[2], 'civ'])

                # Put em URL into checked pages
                dup_checker = dup_checker_f(em_url)
                checkedurls_man_l.append([dup_checker, None])
        civ_tup = None

        
        # Put school URLs into queue
        for i in sch_tup:
            org_name = i[0]
            em_url = i[1]
            if not em_url: continue
            if em_url.startswith('_'): continue
            try: multi_d['sch'][em_url].append(org_name)
            except: 
                multi_d['sch'][em_url] = [org_name]
                all_urls_q.put([org_name, em_url, 0, i[2], 'sch'])
                dup_checker = dup_checker_f(em_url)
                checkedurls_man_l.append([dup_checker, None])
        sch_tup = None


        # Put uni URLs into queue
        for i in uni_tup:
            org_name = i[0]
            em_url = i[1]
            if not em_url: continue
            if em_url.startswith('_'): continue
            try: multi_d['uni'][em_url].append(org_name)
            except: 
                multi_d['uni'][em_url] = [org_name]
                all_urls_q.put([org_name, em_url, 0, i[2], 'uni'])
                dup_checker = dup_checker_f(em_url)
                checkedurls_man_l.append([dup_checker, None])
        uni_tup = None
        


    # Integers to be shared between processes
    skipped_pages = Value('i', 0) # Number of pages that have been skipped
    prog_count = Value('i', 0) # Number of pages checked
    total_count = Value('i', all_urls_q.qsize()) # Number of pages to be checked
    dock_pause = Value('i', 0) # Used to tell children to wait
    using_splash = Value('i', 0) # Used to tell manager that proc is waiting
    all_pause = Value('i', 0) # Used to tell all procs to wait if there is no internet connectivity
    sel_count = Value('i', 0) # Used to prevent too many procs running Sel concurrently




    # Create child processes
    for arb_var in range(num_procs):
        worker = Process(target=scraper, args=())
        worker.start()




    # Wait until all child procs are done scraping
    gc_count = 0
    while len(active_children()) > 1:

        print('\nProgress:', prog_count.value, 'of', total_count.value)
        print('Number of procs:', len(active_children()))
        print('Number of Sel procs:', sel_count.value, 'of', round(num_procs / 4))
        print('mem use:', psutil.virtual_memory()[2], '\n')

        time.sleep(2)

        # Call garbage collecting periodically
        if gc_count > 99:
            print('garbage collect begin')
            gc_count = 0
            resp = requests.post('http://localhost:8050/_gc', timeout=10)
            print('garbage collect end')
        else: gc_count += 1


        # Check internet connectivity
        while True:
            print('ping begin')
            ping_resp = subprocess.run('timeout 2 ping -c 1 joesjorbs.com', stdout=subprocess.PIPE, shell=True)
            if ping_resp.returncode != 0:
                with lock: all_pause.value = 1
                print(os.getpid(), '\n__Pausing all procs. Error code:', ping_resp.returncode)
                time.sleep(3)
            else:
                with lock: all_pause.value = 0
                print('ping end')
                break


        # Reset container if memory usage gets too high
        if psutil.virtual_memory()[2] > max_mem_usage or dock_pause.value == 1:

            # Tell processes to wait
            with lock: dock_pause.value = 1
            print(os.getpid(), 'Docker pause declared')


            save_objs_f() # Save progress


            # Wait for all processes to say they are waiting
            while using_splash.value > 0:
                print(os.getpid(), 'Procs using Splash =', using_splash.value, len(active_children()))
                time.sleep(0.5)

            # Restart Docker
            t = subprocess.call(["/home/joepers/code/jj_v22/start_docker.sh", "--nostart"])


            # Wait for Splash to be ready
            while True:
                try:
                    resp = requests.post('http://localhost:8050/_gc', timeout=10)
                    print(os.getpid(), 'Splash is running')

                    # Reset dock pause count
                    with lock: dock_pause.value = 0
                    container = client.containers.get('jj_con')
                    break

                except:
                    print(os.getpid(), '...')
                    time.sleep(2)



    print(os.getpid(), '\n =======================  Scrape complete  =======================')


    # Stop container
    if client.containers.list():
        container.stop()
        container.remove()

    '''
    # jbw tally
    for i in jobwords_civ_low:
        r_count = jbw_tally_man_l.count(i)
        print(os.getpid(), i, '=', r_count)

    for i in jobwords_su_low:
        r_count = jbw_tally_man_l.count(i)
        print(os.getpid(), i, '=', r_count)

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

    ## check this
    # Write checked pages to file
    with open(checked_path, "a") as checked_file:
        checked_file.write('[\n')
        for kk in checkedurls_man_l:
            checked_file.write(str(kk) + ',\n')
        checked_file.write('\n]')


    # url: [[org name, db type, crawl level], [[error number, error desc], [error number, error desc]], [final error flag, fallback flags]]
    # Convert errorlog to nice format that can be read by humans and json
    e_text = '{\n'
    for k,v in errorurls_man_d.items(): e_text += json.dumps(k) + ': ' + json.dumps(v) + ',\n\n' # json uses double quotes
    e_text = e_text[:-3] # Delete trailing newlines and comma
    e_text += '\n}'

    # Write errorlog
    with open(error_path, 'w', encoding='utf8') as error_file:
        error_file.write(e_text)


    # Calculate error rate
    try:
        error_rate = len(errorurls_man_d) / len(checkedurls_man_l)
        if error_rate < 0.05: error_rate_desc = '(low error rate)'
        elif error_rate < 0.15: error_rate_desc = '(medium error rate)'
        else: error_rate_desc = '(high error rate)'
    except: error_rate_desc = '(error rate unavailable)'

    # Build portal errors list based on crawl level
    portal_error_list = []
    for k,v in errorurls_man_d.items():
        if v[0][2] < 1: portal_error_list.append(k)

    # Stop timer and display stats
    duration = datetime.datetime.now() - startTime
    print('\n\nPages checked =', len(checkedurls_man_l))
    #for x in checkedurls_man_l: print(os.getpid(), x)
    print('Pages skipped =', skipped_pages.value, '\nDuration =', round(duration.seconds / 60), 'minutes\nPage/sec/proc =', str((len(checkedurls_man_l) / duration.seconds) / num_procs)[:4], '\nErrors detected =', len(errorurls_man_d), error_rate_desc, '\nPortal errors =', len(portal_error_list), '\n')



    '''
    ##
    # Delete queue.txt to indicate program completed successfully
    try:
        os.remove(queue_path)
        print('\nDeleted queue_path file\n')
    except:
        print('\nFailed to delete queue_path file\n')
    '''





    dater = glob.glob(jorb_home + "/*") # List all date dirs
    dater.sort(reverse=True)

    # Select old and current results dirs
    cur_dater_results_dir = os.path.join(dater[0], 'results')
    old_dater_results_dir = os.path.join(dater[1], 'results')
    count = 0

    # Allow one URL to cover multiple orgs
    for db_type, url_d in multi_d.items():

        for url, org_names_l in url_d.items():

            # URL is used by more than one org
            if len(org_names_l) > 1:

                # First org path
                src_path = os.path.join(cur_dater_results_dir, db_type, org_names_l[0])

                # Check if results exists for first org
                if os.path.isdir(src_path):
                    print('\nCopying:', src_path)
                    
                    # Copy results from first org to all remaining orgs
                    for dst_path in org_names_l[1:]:
                        dst_path = os.path.join(cur_dater_results_dir, db_type, dst_path)
                        print('to:', dst_path)
                        try: shutil.copytree(src_path, dst_path)
                        except Exception as errex: print(errex)
                        count += 1
    print('Multi orgs:', count)


    # Fallback to older results if newer results are missing
    # Skip this part if there are no old results
    if len(dater) > 1:
        print('Falling back to old results ...')
        count = 0

        # Loop through each results dir
        for each_db in ['/civ', '/sch', '/uni']:

            # Select old and current db dirs
            cur_db_dir = cur_dater_results_dir + each_db + '/*'
            old_db_dir = old_dater_results_dir + each_db + '/*'
            inc_old_dir = cur_dater_results_dir + '/include_old' + each_db


            # Loop through each org name dir in the old db type dir
            for old_org_name_path in glob.glob(old_db_dir):

                # Remove path from org name
                old_org_name = str(old_org_name_path.split('/')[7:])[2:-2]

                # Check current db dir
                for cur_org_name_path in glob.glob(cur_db_dir):

                    # Remove path from org name
                    cur_org_name = str(cur_org_name_path.split('/')[7:])[2:-2]

                    # Skip if the new dir has the result
                    if old_org_name == cur_org_name:
                        break

                # If old org name dir is missing
                else:

                    # Make old_include/old_org_name dir
                    inc_org_name_path = inc_old_dir + '/' + old_org_name

                    # Copy old org name dir to db type include_dir
                    if not os.path.exists(inc_org_name_path):
                        shutil.copytree(old_org_name_path, inc_org_name_path)
                        count += 1
                        #print(os.getpid(), 'Copied fallback result:', old_org_name)

                    # Catch errors
                    else:
                        print('Already exists:', inc_org_name_path)

    print('Files in /include_old:', count)



    # Copy results to remote server using bash
    t = subprocess.call("/home/joepers/code/jj_v22/push_res.sh")







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













