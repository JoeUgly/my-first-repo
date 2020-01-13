#!/usr/bin/python3.7

# Description: Search NYS civil service and school webpages for street address and attempt relavent crawling.

# To do:
# get remaining locs



import datetime, os, queue, re, socket, time, urllib.parse, urllib.request, webbrowser
from multiprocessing import active_children, Lock, Manager, Process, Queue, Value
from urllib.error import URLError


# Global variables
keyword_reg = "(?:[a-z]+\s+){0,4}[a-z]+,?\s+(?:ny|new\s+york)\s+\d{5}"                
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
                if workingurl_tup[1] != -1:
                    
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

    write_arg = False
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
    civ_list = ['http://www.usajobs.gov', 'http://www.cs.ny.gov', 'http://www.albanycounty.com/civilservice', 'http://www.albanyny.org/government/departments/humanresources/employment/examschedule.aspx', 'http://www.townofbethlehem.org/137/human-resources?_sm_au_=ivv8z8lp1wffsnv6', 'http://www.cohoes.com/cit-e-access/webpage.cfm?tid=34&amp;tpid=6383', 'https://www.colonie.org/departments/civilservice', 'http://www.townofguilderland.org/pages/guilderlandny_hr/index?_sm_au_=ivv8z8lp1wffsnv6', 'http://watervliet.com/city/civil-service.htm', 'http://www.alleganyco.com/departments/human-resources-civil-service', 'http://www1.nyc.gov/jobs/index.page', 'http://www.gobroomecounty.com/personnel/cs', 'http://www.binghamton-ny.gov/departments/personnel/employment/employment', 'http://www.townofunion.com/depts_services_human_full.html', 'http://www.vestalny.com/departments/human_resources/job_opportunities.php', 'http://www.cattco.org/jobs', 'http://www.cayugacounty.us/community/civilservicecommission/examannouncementsvacancies.aspx', 'http://www.auburnny.gov/public_documents/auburnny_civilservice/index', 'http://www.co.chautauqua.ny.us/314/human-resources', 'http://www.chemungcountyny.gov/departments/a_-_f_departments/civil_service_personnel/index.php', 'http://www.cityofelmira.net/personnel', 'http://www.co.chenango.ny.us/personnel/examinations', 'http://www.norwichnewyork.net/human_resources.html', 'http://www.clintoncountygov.com/departments/personnel/personnelhomepage.htm', 'https://sites.google.com/a/columbiacountyny.com/civilservice', 'http://www.cortland-co.org/263/personnel-civil%20service', 'http://www.co.delaware.ny.us/departments/pers/pers.htm', 'http://www.co.dutchess.ny.us/countygov/departments/personnel/psexamannouncements.htm', 'http://www.eastfishkillny.org/government/employment.htm', 'http://cityofpoughkeepsie.com/personnel/&', 'http://www.townofpoughkeepsie.com/human_resources/index.html?_sm_au_=ivv8z8lp1wffsnv6', 'http://www.co.dutchess.ny.us/civilserviceinformationsystem/applicantweb/frmannouncementlist.aspx?aspxerrorpath=/civilserviceinformationsystem/applicantweb/frmuserlogin.aspx', 'http://www.erie.gov/employment', 'http://www.amherst.ny.us/govt/govt_dept.asp?dept_id=dept_12&amp;div_id=div_18&amp;menu_id=menu_04&amp;_sm_au_=ivv8z8lp1wffsnv6', 'http://www.ci.buffalo.ny.us/home/city_departments/civil_service', 'http://www.lackawannany.gov/departments/civil-service', 'http://www.tonawandacity.com/residents/civil_service.php', 'http://www.co.essex.ny.us/jobs.asp', 'http://franklincony.org/content/departments/view/6:field=services;/content/departmentservices/view/48', 'http://www.fultoncountyny.gov/node/5', 'http://www.co.genesee.ny.us/departments/humanresources/index.html', 'http://www.batavianewyork.com/fire-department/pages/employment', 'http://greenegovernment.com/departments/human-resources-and-civil-service', 'http://herkimercounty.org/content/departments/view/9', 'http://www.hamiltoncounty.com/government/departments-services', 'http://www.co.jefferson.ny.us/index.aspx?page=83', 'http://www.citywatertown.org/index.asp?nid=111', 'https://www.lewiscounty.org/departments/human-resources/human-resources', 'http://www.co.livingston.state.ny.us/index.aspx?nid=207', 'https://www.madisoncounty.ny.gov/287/personnel', 'http://oneidacity.com/civil-service', 'http://www2.monroecounty.gov/employment-index.php', 'http://www.townofbrighton.org/index.aspx?nid=219&amp;_sm_au_=ivv8z8lp1wffsnv6', 'http://www.townofchili.org/notice-category/job-postings', 'http://www.cityofrochester.gov/article.aspx?id=8589936759', 'http://greeceny.gov/residents/employment-opportunities', 'http://www.irondequoit.org/town-departments/human-resources/town-employment-opportunities?_sm_au_=ivv8z8lp1wffsnv6', 'http://www.penfield.org/human_resources.php', 'http://www.perinton.org/departments/finpers', 'http://www.townofpittsford.org/home-hr?_sm_au_=ivv8z8lp1wffsnv6', 'http://www.ci.webster.ny.us/index.aspx?nid=85&amp;_sm_au_=ivv8z8lp1wffsnv6', 'https://www.co.montgomery.ny.us/sites/public/government/personnel/personnel_development/default.aspx', 'http://www.nassaucivilservice.com/nccsweb/homepage.nsf/homepage?readform', 'http://www.cityofglencoveny.org/index.htm', 'http://www.townofhempstead.org/civil-service-commission?_sm_au_=ivv8z8lp1wffsnv6', 'http://villageofhempstead.org/197/employment-opportunities', 'http://www.longbeachny.org/index.asp?type=b_basic&amp;sec={9c88689c-135f-4293-a9ce-7a50346bea23}', 'http://www.northhempstead.com/employment-opportunities', 'http://oysterbaytown.com/departments/human-resources', 'http://www.rvcny.us/jobs.html?_sm_au_=ivv8z8lp1wffsnv6', 'http://www.vsvny.org/index.asp?type=b_job&amp;sec=%7b05c716c7-40ee-49ee-b5ee-14efa9074ab9%7d&amp;_sm_au_=ivv8z8lp1wffsnv6', 'http://www1.nyc.gov/jobs', 'http://www.cuny.edu/employment/civil-service.html', 'http://www.niagaracounty.com/departments/civilservice.aspx', 'http://niagarafallsusa.org/government/city-departments/human-resources-department', 'http://www.lockportny.gov/residents/city-departments/employment/', 'http://ocgov.net/personnel', 'https://romenewyork.com/civil-service', 'http://www.cityofutica.com/departments/civil-service/index', 'http://www.ongov.net/employment/civilservice.html', 'http://www.ongov.net/employment/jurisdiction.html?_sm_au_=ivvrlpv4fvqpnjqj', 'http://www.ongov.net/employment/jurisdiction.html', 'http://www.co.ontario.ny.us/jobs.aspx', 'http://www.co.ontario.ny.us/index.aspx?nid=94', 'https://www.orangecountygov.com/1137/human-resources', 'http://www.middletown-ny.com/departments/civil-service.html?_sm_au_=ivvrlpv4fvqpnjqj', 'http://www.monroeny.org/departments2/human-resources.html', 'http://www.cityofnewburgh-ny.gov/civil-service', 'http://www.townofwallkill.com/index.php/departments/human-resources', 'http://www.orleansny.com/departments/operations/personnel.aspx', 'http://oswegocounty.com/humanresources.shtml', 'http://www.oswegony.org/government/personnel', 'http://www.otsegocounty.com/depts/per', 'http://www.oneonta.ny.us/departments/personnel', 'http://www.putnamcountyny.com/personneldept', 'http://www.putnamcountyny.com/personneldept/exam-postings', 'http://www.rensco.com/county-job-assistance', 'http://www.troyny.gov/departments/personnel-department', 'http://rocklandgov.com/departments/personnel', 'http://town.clarkstown.ny.us/town_hall/personnel', 'https://www.orangetown.com/groups/department/personnel', 'http://www.ramapo.org/page/personnel-30.html?_sm_au_=ivvt78qz5w7p2qhf', 'http://rocklandgov.com/departments/personnel/civil-service-examinations', 'http://www.saratogacountyny.gov/departments/personnel', 'http://www.cliftonpark.org/services/employment-applications.html', 'http://www.mechanicville.com/index.aspx?nid=563', 'http://www.saratoga-springs.org/jobs.aspx', 'https://mycivilservice.schenectadycounty.com', 'http://www.schenectadycounty.com/fullstory.aspx?m=36&amp;amid=373&amp;_sm_au_=ivvt78qz5w7p2qhf', 'http://www.schenectadycounty.com/fullstory.aspx?m=36&amp;amid=373', 'http://www.cityofschenectady.com/208/human-resources', 'http://www.schohariecounty-ny.gov/countywebsite/personnel/civilserviceservices.html', 'http://www.schuylercounty.us/index.aspx?nid=119', 'https://seneca-portal.mycivilservice.com', 'http://www.co.st-lawrence.ny.us/departments/humanresources/examinationschedule', 'http://www.ogdensburg.org/index.aspx?nid=97', 'http://www.steubencony.org/pages.asp?pgid=32', 'http://www.suffolkcountyny.gov/departments/civilservice.aspx', 'http://www.brookhaven.org/departments/officeofthesupervisor/personnel.aspx?_sm_au_=ivvt78qz5w7p2qhf', 'http://www.huntingtonny.gov/content/13753/13757/17478/17508/default.aspx?_sm_au_=ivvt78qz5w7p2qhf', 'http://isliptown-ny.gov/index.php/i-want-to/apply-for/employment-with-the-town?_sm_au_=ivvt78qz5w7p2qhf', 'http://www.townofriverheadny.gov/pview.aspx?id=2481&amp;catid=118&amp;_sm_au_=ivvt78qz5w7p2qhf', 'http://www.smithtownny.gov/jobs.aspx?_sm_au_=ivvt78qz5w7p2qhf', 'http://www.southamptontownny.gov/jobs.aspx', 'http://co.sullivan.ny.us/departments/departmentsnz/personnel/civilserviceexams/tabid/3382/default.aspx', 'http://www.tiogacountyny.com/departments/personnel-civil-service', 'http://tompkinscountyny.gov/personnel', 'http://www.cityofithaca.org/299/civil-service-examinations', 'http://www.co.ulster.ny.us/personnel', 'http://kingston-ny.gov/employment', 'http://www.warrencountyny.gov/civilservice/exams.php', 'http://www.cityofglensfalls.com/index.aspx?nid=55', 'http://www.washingtoncountyny.gov/jobs.aspx', 'http://web.co.wayne.ny.us/human-resources', 'http://humanresources.westchestergov.com/job-seekers/civil-service-exams', 'http://www.townofcortlandt.com/cit-e-access/webpage.cfm?tid=20&amp;tpid=2522&amp;_sm_au_=ivvt78qz5w7p2qhf', 'http://www.eastchester.org/departments/comptoller.php', 'http://www.greenburghny.com/cit-e-access/webpage.cfm?tid=10&amp;tpid=2491&amp;_sm_au_=ivvt78qz5w7p2qhf', 'http://cmvny.com/departments/civil-service', 'http://www.newrochelleny.com/index.aspx?nid=362', 'http://www.townofossining.com/cms/resources/human-resources', 'http://www.villageofossining.org/personnel-department', 'http://www.cityofpeekskill.com/human-resources/pages/about-human-resources', 'http://www.ryeny.gov/human-resources.cfm', 'http://ny-whiteplains.civicplus.com/index.aspx?nid=98', 'http://www.yonkersny.gov/work/jobs-civil-service-exams', 'http://www.yorktownny.org/jobs', 'http://www.wyomingco.net/164/civil-service', 'http://www.yatescounty.org/203/personnel']
    
    
    schools_list = ['http://academyofthecity.org', 'http://albanycommunitycs.org', 'http://aldenschools.org', 'http://bemusptcsd.org', 'http://bphs.democracyprep.org', 'http://brillacollegeprep.org', 'http://brillacollegeprep.org/our-schools', 'http://brooklyncompass.org', 'http://brooklyneastcollegiate.uncommonschools.org/brooklyn-east/our-school', 'http://brownsvillecollegiate.uncommonschools.org', 'http://campacharter.org', 'http://cazenoviacsd.com', 'http://classicalcharterschools.org/about/schools/south-bronx-classical-charter-school-iii', 'http://classicalcharterschools.org/about/schools/south-bronx-classical-charter-school-iv', 'http://comsewogue.k12.ny.us', 'http://croton-harmonschools.org', 'http://cvweb.wnyric.org', 'http://democracyprep.org', 'http://district.uniondaleschools.org', 'http://dpems.democracyprep.org', 'http://ecs.schoolwires.com', 'http://ecsli.org', 'http://elmcharterschool.org', 'http://enterprisecharter.org', 'http://eufsd.org/site/default.aspx?pageid=1', 'http://excellenceboys.uncommonschools.org', 'http://excellencegirls.uncommonschools.org', 'http://gilboa-conesville.k12.ny.us', 'http://gufsd.org', 'http://hammondcsd.schoolwires.net/site/default.aspx', 'http://healthsciencescharterschool.org', 'http://hpes.democracyprep.org', 'http://imaginemeleadership.org', 'http://inletcommonschool.wordpress.com', 'http://integrationcharterschools.org/lois-and-richard-nicotra-early-college-charter-school', 'http://integrationcharterschools.org/richmond-preparatory-charter-school', 'http://ivyhillprep.org', 'http://jerichoschools.org', 'http://kingscollegiate.uncommonschools.org', 'http://lcsd.k12.ny.us/lcsd/site/default.asp', 'http://leadershipprepbedstuy.uncommonschools.org/lpbs/our-school/elementary-academy', 'http://leadershipprepbrownsville.uncommonschools.org/lpbv/our-school/elementary-academy', 'http://leadershipprepcanarsie.uncommonschools.org/lpcs/our-school/elementary-academy', 'http://leadershipprepoceanhill.uncommonschools.org/lpoh/our-school/elementary-academy', 'http://legacycollegeprep.org', 'http://lisboncs.schoolwires.com', 'http://lmcs.k12.ny.us', 'http://mesacharter.org', 'http://middlevillageprep.org', 'http://motthallcharterschool.org', 'http://newrootsschool.org', 'http://northport.k12.ny.us', 'http://northshore.k12.ny.us', 'http://obenschools.org', 'http://oceanhillcollegiate.uncommonschools.org', 'http://onteora.schoolwires.com', 'http://ripleyelementary.weebly.com', 'http://rochesterprep.uncommonschools.org/rpcs/our-school', 'http://romuluscsd.org', 'http://rsufsd.weebly.com', 'http://scio.schooltools.us', 'http://scotiaglenvilleschools.org', 'http://sewanhaka.k12.ny.us', 'http://shermancsd.org', 'http://southbronxclassical.org', 'http://southoldufsd.com', 'http://storefrontacademy.org', 'http://successacademies.org/schools/bed-stuy-1', 'http://successacademies.org/schools/bed-stuy-2', 'http://successacademies.org/schools/bensonhurst', 'http://successacademies.org/schools/bergen-beach', 'http://successacademies.org/schools/bronx-1', 'http://successacademies.org/schools/bronx-2', 'http://successacademies.org/schools/bronx-3', 'http://successacademies.org/schools/cobble-hill', 'http://successacademies.org/schools/crown-heights', 'http://successacademies.org/schools/fort-greene', 'http://successacademies.org/schools/harlem-1', 'http://successacademies.org/schools/harlem-2', 'http://successacademies.org/schools/harlem-3', 'http://successacademies.org/schools/harlem-4', 'http://successacademies.org/schools/harlem-5', 'http://successacademies.org/schools/hells-kitchen', 'http://successacademies.org/schools/prospect-heights', 'http://successacademies.org/schools/springfield-gardens', 'http://successacademies.org/schools/union-square', 'http://successacademies.org/schools/upper-west', 'http://successacademies.org/schools/washington-heights', 'http://successacademies.org/schools/williamsburg', 'http://swcs.wnyric.org', 'http://sweethomeschools.org', 'http://tfoaprofessionalprep.org', 'http://troyprep.uncommonschools.org', 'http://tullyschools.org', 'http://unityprep.org', 'http://upchs.org', 'http://westbuffalocharter.org', 'http://williamsburgcollegiate.uncommonschools.org', 'http://www.1000islandsschools.org', 'http://www.3villagecsd.k12.ny.us', 'http://www.aacs.wnyric.org', 'http://www.academycharterschool.org', 'http://www.academycharterschool.org/our-schools/the-academy-charter-elementary-school-uniondale', 'http://www.achievementfirst.org/schools/new-york-schools/achievement-first-apollo-elementary-school/about', 'http://www.achievementfirst.org/schools/new-york-schools/achievement-first-aspire-elementary-school/about', 'http://www.achievementfirst.org/schools/new-york-schools/achievement-first-brownsville-elementary-school/about', 'http://www.achievementfirst.org/schools/new-york-schools/achievement-first-bushwick-elementary-school/about', 'http://www.achievementfirst.org/schools/new-york-schools/achievement-first-crown-heights-elementary-school/about', 'http://www.achievementfirst.org/schools/new-york-schools/achievement-first-east-new-york-elementary-school/about', 'http://www.achievementfirst.org/schools/new-york-schools/achievement-first-endeavor-elementary-school/about', 'http://www.achievementfirst.org/schools/new-york-schools/achievement-first-linden-elementary-school/about', 'http://www.achievementfirst.org/schools/new-york-schools/achievement-first-north-brooklyn-prep-elementary-school/about', 'http://www.addisoncsd.org', 'http://www.adirondackcsd.org', 'http://www.adjcharter.org.', 'http://www.afton.stier.org', 'http://www.akronschools.org', 'http://www.albanyleadershiphigh.org', 'http://www.albanyschools.org', 'http://www.albionk12.org', 'http://www.alcsbronx.org', 'http://www.alcsny.org/site/default.aspx?pageid=1', 'http://www.alexandercsd.org', 'http://www.alexandriacentral.org', 'http://www.amanicharter.org', 'http://www.amherstschools.org', 'http://www.amityvilleschools.org', 'http://www.andescentralschool.org', 'http://www.andovercsd.org/site/default.aspx?pageid=1', 'http://www.apw.cnyric.org', 'http://www.ardsleyschools.org', 'http://www.argylecsd.org', 'http://www.arlingtonschools.org/pages/arlington_schools', 'http://www.ascendlearning.org', 'http://www.ascendlearning.org/school/central-brooklyn-ascend-lower', 'http://www.ascendlearning.org/schools', 'http://www.ascendlearning.org/schools/bushwick-ascend-lower', 'http://www.atmosphereacademy.org', 'http://www.atticacsd.org', 'http://www.auburn.wednet.edu', 'http://www.avcs.org', 'http://www.averillpark.k12.ny.us', 'http://www.avocacsd.org', 'http://www.avoncsd.org', 'http://www.babylon.k12.ny.us', 'http://www.baldwinschools.org', 'http://www.barkercsd.net', 'http://www.bascs.org', 'http://www.bataviacsd.org', 'http://www.bathcsd.org', 'http://www.bayshore.k12.ny.us', 'http://www.bbpschools.org', 'http://www.bbschools.org', 'http://www.bcsd.k12.ny.us', 'http://www.bcsd.org', 'http://www.bcsdk12.org', 'http://www.bcsdny.org', 'http://www.beaconcityk12.org', 'http://www.bedstuycollegiate.org', 'http://www.belfast.wnyric.org', 'http://www.bellmore-merrick.k12.ny.us', 'http://www.bellmore.k12.ny.us', 'http://www.berkshirefarm.org/programs_and_services/berkshire_union_free_school_district_7_srvm.htm', 'http://www.berlincentral.org', 'http://www.bethpagecommunity.com', 'http://www.bfcsd.org', 'http://www.bgcsd.org', 'http://www.bgligschool.org', 'http://www.bhbl.org', 'http://www.bhpanthers.org', 'http://www.binghamtonschools.org', 'http://www.bkwcsd.k12.ny.us', 'http://www.blindbrook.org', 'http://www.bloomfieldcsd.org', 'http://www.bmcsd.org', 'http://www.boltoncsd.org', 'http://www.bpcsd.org', 'http://www.bradfordcsd.org', 'http://www.brcs.wnyric.org', 'http://www.brcsd.org', 'http://www.brewsterschools.org', 'http://www.briarcliffschools.org', 'http://www.bridgehampton.k12.ny.us', 'http://www.brighterchoice.org/boys', 'http://www.brighterchoice.org/girls', 'http://www.brittonkill.k12.ny.us', 'http://www.brockport.k12.ny.us', 'http://www.broctoncsd.org', 'http://www.bronxbetterlearning.org', 'http://www.bronxcommunity.org', 'http://www.bronxexcellence.org', 'http://www.brookfieldcsd.org/site/default.aspx?pageid=1', 'http://www.brooklyncharter.org', 'http://www.brooklynlaboratoryschool.org', 'http://www.broomestreetacademy.org', 'http://www.bscsd.org', 'http://www.bsnbcs.org', 'http://www.buffaloschools.org', 'http://www.bufsd.org', 'http://www.bville.org', 'http://www.bwccs2.org', 'http://www.byramhills.org', 'http://www.cairodurham.org', 'http://www.cal-mum.org', 'http://www.cambridgecsd.org', 'http://www.camdenschools.org', 'http://www.canajoharieschools.org', 'http://www.canandaiguaschools.org', 'http://www.canastotacsd.org', 'http://www.candorcsd.org', 'http://www.carmelschools.org', 'http://www.carthagecsd.org', 'http://www.catomeridian.org', 'http://www.cattlv.wnyric.org', 'http://www.cc.cnyric.org', 'http://www.cccsd.org', 'http://www.ccs.edu', 'http://www.ccsd.edu', 'http://www.ccsdk12.org', 'http://www.ccsdli.org', 'http://www.ccsdny.org', 'http://www.ccsknights.org', 'http://www.centermoriches.k12.ny.us', 'http://www.centralislip.k12.ny.us', 'http://www.centralqueensacademy.org', 'http://www.centralsquareschools.org', 'http://www.cforks.org', 'http://www.cg.wnyric.org', 'http://www.challengeprepcharter.org', 'http://www.charlottevalleycs.org', 'http://www.charterschoolofeducationalexcellence.org', 'http://www.charterschoolofinquiry.org', 'http://www.chateaugaycsd.org', 'http://www.chathamcentralschools.com', 'http://www.chazy.org', 'http://www.cheektowagacentral.org', 'http://www.chittenangoschools.org', 'http://www.chslawandsocialjustice.org', 'http://www.cityschoolofthearts.org', 'http://www.clake.org', 'http://www.clarenceschools.org', 'http://www.clevehill.wnyric.org', 'http://www.cliftonfine.org', 'http://www.clydesavannah.org', 'http://www.clymercsd.org', 'http://www.cmcs.org/news-events/stories/charter-school-countdown', 'http://www.cohoes.org', 'http://www.commack.k12.ny.us', 'http://www.communityroots.org', 'http://www.comsewogue.k12.ny.us', 'http://www.coneyislandprep.org/our-schools/elementary-school', 'http://www.cooperstowncs.org', 'http://www.copiague.k12.ny.us', 'http://www.corinthcsd.com', 'http://www.corningareaschools.com', 'http://www.cornwallschools.com', 'http://www.cortlandschools.org', 'http://www.cpcs.us', 'http://www.cpcsschool.org', 'http://www.cpcsteam.org', 'http://www.cps.k12.ny.us', 'http://www.crcs.k12.ny.us', 'http://www.crcs.wnyric.org', 'http://www.csat-k12.org/csat/site/default.asp', 'http://www.cscsd.org', 'http://www.csh.k12.ny.us', 'http://www.cvcsd.stier.org', 'http://www.cvscs.org', 'http://www.dansvillecsd.org', 'http://www.dcseagles.org', 'http://www.deerparkschools.org', 'http://www.delhischools.org', 'http://www.depewschools.org', 'http://www.depositcsd.org', 'http://www.deruyter.k12.ny.us', 'http://www.dfsd.org', 'http://www.dolgeville.org', 'http://www.doverschools.org', 'http://www.dreamschoolnyc.org', 'http://www.dryden.k12.ny.us', 'http://www.dundeecs.org', 'http://www.dunkirkcsd.org', 'http://www.eastauroraschools.org/site/default.aspx?pageid=1', 'http://www.eastchester.k12.ny.us', 'http://www.easthamptonschools.org', 'http://www.eastharlemscholars.org', 'http://www.eastmeadow.k12.ny.us', 'http://www.eastquogue.k12.ny.us', 'http://www.eastrockawayschools.org', 'http://www.ecs.k12.ny.us', 'http://www.edencsd.org', 'http://www.edgemont.org', 'http://www.edinburgcs.org', 'http://www.edmestoncentralschool.net', 'http://www.egcsd.org', 'http://www.eicsd.k12.ny.us', 'http://www.eischools.org', 'http://www.ekcsk12.org', 'http://www.elbacsd.org', 'http://www.ellicottvillecentral.com', 'http://www.elmiracityschools.com', 'http://www.elmontschools.org', 'http://www.elwood.k12.ny.us', 'http://www.emblazeacademy.org', 'http://www.emhcharter.org', 'http://www.emoschools.org', 'http://www.equalitycharterschool.org/news', 'http://www.ercsd.org/pages/east_ramapo_csd', 'http://www.erschools.org', 'http://www.esmonline.org', 'http://www.esmschools.org', 'http://www.evcsbuffalo.org', 'http://www.ewsdonline.org', 'http://www.explorenetwork.org/empower-charter-school', 'http://www.explorenetwork.org/exceed-charter-school', 'http://www.explorenetwork.org/excel-charter-school', 'http://www.explorenetwork.org/explore-charter-school', 'http://www.fabiuspompey.org', 'http://www.fairport.org', 'http://www.falconerschools.org', 'http://www.fallsburgcsd.net', 'http://www.farmingdaleschools.org', 'http://www.fi.k12.ny.us', 'http://www.fillmorecsd.org', 'http://www.fischool.com', 'http://www.floralpark.k12.ny.us', 'http://www.floridaufsd.org', 'http://www.fmschools.org', 'http://www.fondafultonvilleschools.org', 'http://www.forestville.com', 'http://www.fortannschool.org', 'http://www.fortedward.org', 'http://www.forteprep.org', 'http://www.fortplain.org', 'http://www.frankfort-schuyler.org', 'http://www.franklincsd.org', 'http://www.franklinsquare.k12.ny.us', 'http://www.fredonia.wnyric.org', 'http://www.freeportschools.org', 'http://www.frewsburgcsd.org', 'http://www.friendship.wnyric.org', 'http://www.frontier.wnyric.org', 'http://www.fulton.cnyric.org', 'http://www.futureleadersinstitute.org', 'http://www.galwaycsd.org', 'http://www.gananda.org', 'http://www.gardencity.k12.ny.us', 'http://www.gasd.org', 'http://www.gateschili.org', 'http://www.gblions.org', 'http://www.gcacs.org', 'http://www.gccschool.org', 'http://www.gcsk12.org', 'http://www.gcsny.org', 'http://www.geneseocsd.org', 'http://www.genevacsd.org', 'http://www.genvalley.org', 'http://www.germantowncsd.org', 'http://www.gfsd.org', 'http://www.gjrufsd.org', 'http://www.glencove.k12.ny.us', 'http://www.globalccs.org', 'http://www.globalcommunitycs.org', 'http://www.gloversvilleschools.org', 'http://www.gmucsd.org', 'http://www.gowcsd.com', 'http://www.granvillecsd.org', 'http://www.greatneck.k12.ny.us', 'http://www.greece.k12.ny.us', 'http://www.greenburgh-graham.org', 'http://www.greenburgheleven.org', 'http://www.greenburghnorthcastleschools.com', 'http://www.greenecsd.org', 'http://www.greenisland.org', 'http://www.greentechhigh.org', 'http://www.greenville.k12.ny.us', 'http://www.greenwichcsd.org', 'http://www.grotoncs.org', 'http://www.gufs.org', 'http://www.gugcs.org', 'http://www.guilderlandschools.org', 'http://www.gwlufsd.org', 'http://www.halfhollowhills.k12.ny.us', 'http://www.hamburgschools.org', 'http://www.hamiltoncentral.org', 'http://www.hammondsportcsd.org', 'http://www.hannibalcsd.org', 'http://www.harborfieldscsd.net', 'http://www.harlemhebrewcharter.org', 'http://www.harlemlink.org', 'http://www.harrisoncsd.org', 'http://www.hartfordcsd.org', 'http://www.hauppauge.k12.ny.us/site/default.aspx?pageid=1', 'http://www.havenacademy.org', 'http://www.hbschools.us', 'http://www.hccs-nys.org', 'http://www.hcks.org', 'http://www.hcs.stier.org', 'http://www.hcsk12.org', 'http://www.hczpromiseacademy.org', 'http://www.healthscienceschool.org', 'http://www.heightsschools.com', 'http://www.heketi.org', 'http://www.hempsteadschools.org', 'http://www.henhudschools.org', 'http://www.henryjohnsoncs.org', 'http://www.herkimercsd.org', 'http://www.herricks.org', 'http://www.hewlett-woodmere.net', 'http://www.hfcsd.org', 'http://www.hffmcsd.org', 'http://www.hflcsd.org', 'http://www.hicksvillepublicschools.org', 'http://www.highland-k12.org', 'http://www.hilton.k12.ny.us', 'http://www.hinsdalebobcats.org', 'http://www.hlacharterschool.org', 'http://www.hlcs.org', 'http://www.hohschools.org/site/default.aspx?pageid=1', 'http://www.holland.wnyric.org', 'http://www.holleycsd.org', 'http://www.homercentral.org', 'http://www.honeoye.org', 'http://www.hoosickfallscsd.org', 'http://www.hoosicvalley.k12.ny.us', 'http://www.hornellcityschools.com', 'http://www.horseheadsdistrict.com', 'http://www.hpschools.org', 'http://www.hsacs.org', 'http://www.htcsbronx.org', 'http://www.hudsoncityschooldistrict.com', 'http://www.hufsd.edu', 'http://www.hydebronxny.org', 'http://www.hydebrooklyn.org', 'http://www.icahncharterschool1.org', 'http://www.icahncharterschool2.org', 'http://www.icahncharterschool3.org', 'http://www.icahncharterschool4.org', 'http://www.icahncharterschool5.org', 'http://www.icahncharterschool6.org', 'http://www.icahncharterschool7.org', 'http://www.ichabodcrane.org', 'http://www.icsd.k12.ny.us', 'http://www.icsnyc.org', 'http://www.ilcsd.org', 'http://www.innovationhs.org', 'http://www.inwoodacademy.org', 'http://www.ips.k12.ny.us', 'http://www.ircsd.org', 'http://www.iroquoiscsd.org', 'http://www.irvingtonschools.org', 'http://www.islandtrees.org', 'http://www.islipufsd.org', 'http://www.jamestownpublicschools.org', 'http://www.jamesvilledewitt.org', 'http://www.jcschools.com', 'http://www.jecsd.org', 'http://www.jeffersoncs.org', 'http://www.johnsburgcsd.org', 'http://www.johnstownschools.org', 'http://www.jtcsd.org', 'http://www.jvlwildcat.org', 'http://www.k12.ginet.org', 'http://www.kccs.org', 'http://www.keenecentralschool.org', 'http://www.kendallschools.org', 'http://www.kenton.k12.ny.us/site/default.aspx?pageid=1', 'http://www.keshequa.org', 'http://www.kingstoncityschools.org', 'http://www.kippnyc.org/schools/kipp-academy-elementary', 'http://www.kippnyc.org/schools/kipp-amp-elementary', 'http://www.kippnyc.org/schools/kipp-infinity-elementary', 'http://www.kippnyc.org/schools/kipp-star-middle-school', 'http://www.kippnyc.org/schools/kipp-washington-heights-middle-school', 'http://www.kipptechvalley.org', 'http://www.klschools.org', 'http://www.lacimacharterschool.org', 'http://www.lackawannaschools.org', 'http://www.lacs-ny.org', 'http://www.lafargevillecsd.org', 'http://www.lafayetteschools.org', 'http://www.lakelandschools.org', 'http://www.lakeshore.wnyric.org', 'http://www.lancasterschools.org', 'http://www.lansingburgh.org', 'http://www.launchschool.org', 'http://www.laurenscs.org', 'http://www.lavelleprep.org', 'http://www.lawrence.org', 'http://www.lbeach.org', 'http://www.leroycsd.org', 'http://www.letchworth.k12.ny.us', 'http://www.levittownschools.com', 'http://www.lew-port.com', 'http://www.lfcsd.org', 'http://www.libertyk12.org', 'http://www.lighthouse-academies.org/schools/bronx', 'http://www.lighthouse-academies.org/schools/metropolitan', 'http://www.lindenhurstschools.org', 'http://www.littleflowerufsd.org', 'http://www.liverpool.k12.ny.us', 'http://www.livoniacsd.org', 'http://www.lkgeorge.org', 'http://www.lockportschools.wnyric.org', 'http://www.longlakecsd.org', 'http://www.longwood.k12.ny.us', 'http://www.lpcsd.org', 'http://www.lpschool.com', 'http://www.lvcsd.k12.ny.us', 'http://www.lymecsd.org', 'http://www.lynbrookschools.org/schools/index.cfm?sid=1', 'http://www.lyncourtschool.org', 'http://www.lyndonvillecsd.org', 'http://www.lyonscsd.org', 'http://www.m-ecs.org', 'http://www.madisoncentralny.org', 'http://www.mahopac.k12.ny.us', 'http://www.malonecsd.org', 'http://www.malverne.k12.ny.us', 'http://www.mamkschools.org', 'http://www.manhattancharterschool.org', 'http://www.marathonschools.org', 'http://www.marcellusschools.org', 'http://www.margaretvillecs.org', 'http://www.marioncs.org', 'http://www.marlboroschools.org', 'http://www.mayfieldk12.com', 'http://www.mcgrawschools.org', 'http://www.me.stier.org', 'http://www.mechanicville.org', 'http://www.medinacsd.org', 'http://www.menands.org', 'http://www.merrick.k12.ny.us', 'http://www.merrickacademy.org', 'http://www.mexico.cnyric.org', 'http://www.middleburgh.k12.ny.us', 'http://www.middlecountry.k12.ny.us', 'http://www.middletowncityschools.org', 'http://www.midlakes.org', 'http://www.millbrookcsd.org', 'http://www.millerplace.k12.ny.us', 'http://www.mineola.k12.ny.us', 'http://www.minervasd.org', 'http://www.minisink.com', 'http://www.mmcsd.org/site/default.aspx?pageid=1', 'http://www.mohonasen.org', 'http://www.montaukschool.org', 'http://www.monticelloschools.net', 'http://www.moraviaschool.org', 'http://www.moriahk12.org', 'http://www.morriscs.org', 'http://www.mpbschools.org', 'http://www.mpcsny.org', 'http://www.msd.k12.ny.us', 'http://www.mtmorriscsd.org', 'http://www.mtplcsd.org', 'http://www.mtsinai.k12.ny.us', 'http://www.mtvernoncsd.org', 'http://www.mufsd.com/cms', 'http://www.mw.k12.ny.us', 'http://www.mwcsd.org', 'http://www.mwcsk12.org', 'http://www.nacs1.org', 'http://www.nanuetsd.org', 'http://www.naplescsd.org', 'http://www.nccscougar.org', 'http://www.ncsharlem.org', 'http://www.ncsharlem.org/bronx', 'http://www.ndchsbrooklyn.org', 'http://www.newark.k12.ny.us/newarkcsd/site/default.asp', 'http://www.newburghschools.org', 'http://www.newcombcsd.org', 'http://www.newfane.wnyric.org', 'http://www.newfieldschools.org', 'http://www.newhartfordschools.org', 'http://www.newheightsacademy.org', 'http://www.newlebanoncsd.org', 'http://www.newpaltz.k12.ny.us', 'http://www.newsuffolkschool.com', 'http://www.newventurescharterschool.org', 'http://www.newvisions.org/ams4', 'http://www.newvisions.org/charter', 'http://www.newvisions.org/charter/humii', 'http://www.newvisions.org/schools/entry/ams3', 'http://www.newvisions.org/schools/entry/amsii', 'http://www.newvisions.org/schools/entry/hum3', 'http://www.newvisions.org/schools/entry/humanities-iv', 'http://www.newworldprep.org', 'http://www.newyorkcharters.org/progress/schools/success-academy-charter-school-bed-stuy-3', 'http://www.newyorkmills.org', 'http://www.nfschools.net', 'http://www.nhp-gcp.org', 'http://www.niagaracharter.org', 'http://www.niskayunaschools.org', 'http://www.nncsk12.org', 'http://www.northbabylonschools.net', 'http://www.northbellmoreschools.org', 'http://www.northcolonie.org', 'http://www.northgreenbushcommon.org', 'http://www.northsalemschools.org', 'http://www.northsidechs.org', 'http://www.northwarren.k12.ny.us', 'http://www.norwichcsd.org', 'http://www.nrcsd.org', 'http://www.nred.org', 'http://www.nrwcs.org', 'http://www.nscsd.org', 'http://www.ntschools.org', 'http://www.nvcs.stier.org', 'http://www.nwcsd.k12.ny.us', 'http://www.nyackschools.org', 'http://www.nycacharterschool.org', 'http://www.nycautismcharterschool.org', 'http://www.nycmcs.org', 'http://www.oacsd.org', 'http://www.oceansideschools.org', 'http://www.ocs.cnyric.org', 'http://www.odyoungcsd.org', 'http://www.oesj.org', 'http://www.ogdensburgk12.org', 'http://www.oleanschools.org', 'http://www.omschools.org', 'http://www.oneidacsd.org', 'http://www.oneontacsd.org', 'http://www.opportunitycharter.org', 'http://www.opschools.org', 'http://www.oriskanycsd.org', 'http://www.ossiningufsd.org', 'http://www.oswego.org', 'http://www.ovcs.org', 'http://www.owncs.org', 'http://www.oxac.org', 'http://www.oysterponds.org', 'http://www.pacs.cnyric.org', 'http://www.palmaccsd.org', 'http://www.pancent.org', 'http://www.pavilioncsd.org', 'http://www.pawlingschools.org', 'http://www.pbcschools.org', 'http://www.pearlriver.org', 'http://www.peekskillcsd.org', 'http://www.pelhamschools.org', 'http://www.pembrokecsd.org', 'http://www.penfield.edu', 'http://www.peninsulaprep.org', 'http://www.perry.k12.ny.us', 'http://www.perucsd.org', 'http://www.phoenixcsd.org', 'http://www.pinebushschools.org', 'http://www.pioneerschools.org', 'http://www.pisecoschool.com', 'http://www.pittsfordschools.org', 'http://www.plainedgeschools.org', 'http://www.plattscsd.org', 'http://www.pleasantvilleschools.com', 'http://www.pocanticohills.org', 'http://www.polandcs.org', 'http://www.portchesterschools.org', 'http://www.portjeff.k12.ny.us', 'http://www.portjerviscsd.k12.ny.us', 'http://www.portnet.k12.ny.us', 'http://www.portville.wnyric.org', 'http://www.potsdam.k12.ny.us', 'http://www.poughkeepsieschools.org', 'http://www.ppcsd.org', 'http://www.publicprep.org/our-schools/boysprep', 'http://www.putnamcsd.org', 'http://www.pval.org', 'http://www.pvcsd.org', 'http://www.queensburyschool.org', 'http://www.railroaders.net', 'http://www.randolphacademy.org', 'http://www.randolphcsd.org', 'http://www.rcacs.org', 'http://www.rccsd.org', 'http://www.rcscsd.org', 'http://www.rcsd.k12.ny.us', 'http://www.rcsdk12.org', 'http://www.reachacademycharter.org', 'http://www.redhookcentralschools.org', 'http://www.redjacket.org', 'http://www.remsencsd.org', 'http://www.renacad.org', 'http://www.renaissancecharter.org', 'http://www.rhinebeckcsd.org', 'http://www.richfieldcsd.org', 'http://www.riverhead.net', 'http://www.riverheadcharterschool.org', 'http://www.rocachieve.org', 'http://www.rockypointschools.org', 'http://www.romecsd.org', 'http://www.rondout.k12.ny.us', 'http://www.roscoe.k12.ny.us', 'http://www.roslynschools.org', 'http://www.roxburycs.org', 'http://www.royhart.org', 'http://www.rvcschools.org', 'http://www.ryeneck.k12.ny.us', 'http://www.ryeschools.org', 'http://www.sachem.k12.ny.us', 'http://www.sacketspatriots.org', 'http://www.sagaponackschool.com', 'http://www.sagharborschools.org', 'http://www.salamancany.org', 'http://www.salemcsd.org', 'http://www.saratogaschools.org', 'http://www.sascs.org', 'http://www.saugerties.k12.ny.us', 'http://www.scarsdaleschools.k12.ny.us', 'http://www.schalmont.org', 'http://www.schenectady.k12.ny.us', 'http://www.schenevuscsd.org', 'http://www.schodack.k12.ny.us', 'http://www.schoharie.k12.ny.us', 'http://www.schroonschool.org', 'http://www.schuylervilleschools.org', 'http://www.scsd.org', 'http://www.seaford.k12.ny.us', 'http://www.secsd.org', 'http://www.sfcs.k12.ny.us', 'http://www.sgfallssd.org', 'http://www.sharonsprings.org', 'http://www.shelterisland.k12.ny.us', 'http://www.shenet.org', 'http://www.shufsd.org', 'http://www.sidneycsd.org', 'http://www.silvercreekschools.org/', 'http://www.sisuluwalker.org', 'http://www.skanschools.org', 'http://www.skcs.org', 'http://www.slcs.org', 'http://www.sloanschools.org', 'http://www.smithtown.k12.ny.us', 'http://www.soduscsd.org', 'http://www.solvayschools.org', 'http://www.somersschools.org/site/default.aspx?pageid=1', 'http://www.southamptonschools.org', 'http://www.southbronxclassical.org', 'http://www.southbronxcommunity.org', 'http://www.southbuffalocs.org', 'http://www.southcolonieschools.org', 'http://www.southcountry.org', 'http://www.southerncayuga.org', 'http://www.southlewis.org', 'http://www.southseneca.com', 'http://www.spackenkillschools.org', 'http://www.spartanpride.org', 'http://www.spencerportschools.org', 'http://www.springsschool.org', 'http://www.springvillegi.org', 'http://www.srk12.org', 'http://www.stamfordcs.org', 'http://www.starpointcsd.org', 'http://www.sthopeleadershipacademy.org', 'http://www.stockbridgevalley.org', 'http://www.successacademies.org/schools/bushwick', 'http://www.successacademies.org/schools/far-rockaway', 'http://www.successacademies.org/schools/flatbush', 'http://www.successacademies.org/schools/harlem-6', 'http://www.successacademies.org/schools/hudson-yards', 'http://www.successacademies.org/schools/south-jamaica', 'http://www.sufferncentral.org', 'http://www.summitacademycharterschool.org', 'http://www.svcsd.org', 'http://www.svecsd.org', 'http://www.svsabers.org', 'http://www.swcsd.org', 'http://www.swrschools.org', 'http://www.syosset.k12.ny.us', 'http://www.syracusecityschools.com', 'http://www.taconichills.k12.ny.us', 'http://www.tapestryschool.org/academic-and-social-programs/k-8', 'http://www.tbafcs.org/site/default.aspx?pageid=1', 'http://www.tbcsc.org', 'http://www.tburgschools.org', 'http://www.tepcharter.org', 'http://www.theamericandreamschool.org', 'http://www.thewcs.org', 'http://www.ticonderogak12.org', 'http://www.tiogacentral.org', 'http://www.tonawandacsd.org', 'http://www.towschool.org', 'http://www.troycsd.org', 'http://www.tuckahoeschools.org', 'http://www.tufsd.org', 'http://www.tupperlakecsd.net', 'http://www.tuxedoufsd.org', 'http://www.uascs.org', 'http://www.udteam.org', 'http://www.uek12.org', 'http://www.unatego.org', 'http://www.uncommonschools.org/our-schools/new-york-city-brooklyn', 'http://www.unionspringscsd.org', 'http://www.upreprochester.org', 'http://www.urbanchoicecharter.org', 'http://www.uticaschools.org', 'http://www.uvstorm.org', 'http://www.valhallaschools.org', 'http://www.valleystream13.com', 'http://www.valleystream30.com', 'http://www.valleystreamdistrict24.org', 'http://www.vcsd.k12.ny.us', 'http://www.vertusschool.org', 'http://www.vestal.stier.org', 'http://www.victorschools.org', 'http://www.vliet.neric.org', 'http://www.voicecharterschool.org', 'http://www.voorheesville.org/site/default.aspx?pageid=1', 'http://www.vschsd.org', 'http://www.vvsschools.org', 'http://www.wacs.wnyric.org', 'http://www.wainscottschool.org', 'http://www.wajcs.org', 'http://www.wallkillcsd.k12.ny.us', 'http://www.waltoncsd.org', 'http://www.wantaghschools.org', 'http://www.wappingersschools.org', 'http://www.warsaw.k12.ny.us', 'http://www.warwickvalleyschools.com', 'http://www.watertowncsd.org', 'http://www.watervillecsd.org/site/default.aspx?pageid=1', 'http://www.waverlyschools.com', 'http://www.wboro.org', 'http://www.wbschools.org', 'http://www.wccsk12.org', 'http://www.wcsd.org', 'http://www.web.milfordcentral.org', 'http://www.websterschools.org', 'http://www.weedsport.org', 'http://www.wellscsd.org', 'http://www.wellsville.wnyric.org', 'http://www.westburyschools.org', 'http://www.westcanada.org', 'http://www.westgenesee.org', 'http://www.westhamptonbeach.k12.ny.us', 'http://www.westhillschools.org', 'http://www.westirondequoit.org', 'http://www.westminsterccs.org', 'http://www.westmorelandschool.org', 'http://www.westportcs.org', 'http://www.wfsd.k12.ny.us', 'http://www.wgcsd.org', 'http://www.wheatland.k12.ny.us', 'http://www.whitesville.wnyric.org', 'http://www.whufsd.com', 'http://www.whufsd.org', 'http://www.wi.k12.ny.us', 'http://www.williamsoncentral.org', 'http://www.williamsvillek12.org', 'http://www.willsborocsd.org', 'http://www.wilson.wnyric.org', 'http://www.windsor-csd.org', 'http://www.worcestercs.org', 'http://www.wpcsd.org', 'http://www.ws.k12.ny.us', 'http://www.wscschools.org', 'http://www.wufsk8.com', 'http://www.wvalley.wnyric.org', 'http://www.wyandanch.k12.ny.us', 'http://www.wynantskillufsd.org', 'http://www.wyomingcsd.org', 'http://www.yonkerspublicschools.org', 'http://www.yorkcsd.org', 'http://www.yorktown.org', 'http://www.youngwomenscollegeprep.org', 'http://yalowcharter.org', 'https://boldschools.org', 'https://catskillcsd.org', 'https://hlacharterschool.org', 'https://paveschools.org', 'https://sbecacs.org', 'https://sites.google.com/a/northvillecsd.org/ncsd', 'https://sites.google.com/htcschools.org/htc/home', 'https://stradfordprep.org', 'https://urbanassembly.org', 'https://www.abewing.org/aws', 'https://www.achievementfirst.org/schools/new-york-schools', 'https://www.ambercharter.org', 'https://www.arkportcsd.org', 'https://www.aufsd.org', 'https://www.belahs.org', 'https://www.bronxbetterlearning.org/apps/pages/index.jsp?urec_id=772803&amp;type=d&amp;prec_id=1173266', 'https://www.bronxvilleschool.org', 'https://www.buffalocollegiate.org', 'https://www.cacsd.org', 'https://www.ccsd.ws', 'https://www.creoprep.org', 'https://www.cvalleycsd.org', 'https://www.duanesburg.org', 'https://www.elcsd.org', 'https://www.ercsd.org', 'https://www.explorationrochester.org', 'https://www.greenburghcsd.org', 'https://www.haldaneschool.org', 'https://www.hancock.stier.org', 'https://www.hdcsk12.org', 'https://www.heuvelton.k12.ny.us', 'https://www.hpcsd.org', 'https://www.keycollegiate.org', 'https://www.kippnyc.org/schools/kipp-freedom', 'https://www.kpcsd.org', 'https://www.manhassetschools.org', 'https://www.maryvaleufsd.org', 'https://www.mcs.k12.ny.us', 'https://www.newvisions.org/aim1', 'https://www.newvisions.org/aim2', 'https://www.northcollins.com', 'https://www.oahornets.org', 'https://www.oesj.org', 'https://www.persistenceprep.org/mission', 'https://www.phcsd.org', 'https://www.pmschools.org', 'https://www.pobschools.org', 'https://www.prattsburghcsd.org', 'https://www.pycsd.org', 'https://www.quogueschool.com', 'https://www.rhnet.org/page/9', 'https://www.rooseveltufsd.org', 'https://www.sandycreekcsd.org', 'https://www.sayvilleschools.org', 'https://www.schoolinthesquare.org', 'https://www.socsd.org', 'https://www.stregiscsd.org', 'https://www.successacademies.org/schools', 'https://www.theuftcharterschool.org', 'https://www.trivalleycsd.org', 'https://www.valencecollegeprep.org', 'https://www.waterloocsd.org', 'https://www.waynecsd.org', 'https://www.webutuckschools.org', 'https://www.whiteplainspublicschools.org', 'https://zetaschools.org']



    uni_list = ['http://cas.nyu.edu', 'http://ccny.cuny.edu/csom', 'http://columbia.edu', 'http://cornell.edu', 'http://drama.newschool.edu', 'http://einstein.yu.edu', 'http://engineering.columbia.edu', 'http://engineering.nyu.edu', 'http://fordham.edu', 'http://gallatin.nyu.edu', 'http://globe.edu', 'http://gradschool.cshl.edu', 'http://gradschool.weill.cornell.edu', 'http://gsas.columbia.edu', 'http://icahn.mssm.edu', 'http://journalism.columbia.edu', 'http://journalism.cuny.edu', 'http://lcm.touro.edu', 'http://liu.edu/brooklyn.aspx', 'http://mailman.columbia.edu', 'http://newschool.edu/public-engagement', 'http://nursing.columbia.edu', 'http://pace.edu', 'http://ps.columbia.edu', 'http://socialwork.nyu.edu', 'http://sph.cuny.edu', 'http://sps.columbia.edu', 'http://steinhardt.nyu.edu', 'http://strose.edu', 'http://suny.buffalostate.edu', 'http://suny.oneonta.edu', 'http://sunypoly.edu', 'http://tech.cornell.edu', 'http://tisch.nyu.edu', 'http://tkc.edu', 'http://touro.edu', 'http://tourocom.touro.edu', 'http://usma.edu', 'http://utica.edu', 'http://wagner.edu', 'http://weill.cornell.edu', 'http://www.acphs.edu', 'http://www.adelphi.edu', 'http://www.albany.edu', 'http://www.alfred.edu', 'http://www.alfredstate.edu', 'http://www.arch.columbia.edu', 'http://www.asa.edu', 'http://www.bankstreet.edu', 'http://www.bard.edu', 'http://www.barnard.edu', 'http://www.baruch.cuny.edu', 'http://www.bcc.cuny.edu', 'http://www.berkeleycollege.edu/index.htm', 'http://www.binghamton.edu', 'http://www.bmcc.cuny.edu', 'http://www.brockport.edu', 'http://www.brooklaw.edu', 'http://www.brooklyn.cuny.edu', 'http://www.buffalo.edu', 'http://www.canisius.edu', 'http://www.canton.edu', 'http://www.cardozo.yu.edu', 'http://www.cayuga-cc.edu', 'http://www.cazenovia.edu', 'http://www.ccny.cuny.edu', 'http://www.ciachef.edu', 'http://www.cims.nyu.edu', 'http://www.citytech.cuny.edu', 'http://www.clarkson.edu', 'http://www.clinton.edu', 'http://www.cnr.edu', 'http://www.cobleskill.edu', 'http://www.colgate.edu', 'http://www.college.columbia.edu', 'http://www.columbia.edu/cu/ssw', 'http://www.concordia-ny.edu', 'http://www.cooper.edu', 'http://www.cortland.edu', 'http://www.cshl.edu', 'http://www.csi.cuny.edu', 'http://www.cuny.edu', 'http://www.daemen.edu', 'http://www.davisny.edu', 'http://www.dc.edu', 'http://www.delhi.edu', 'http://www.dental.columbia.edu', 'http://www.downstate.edu', 'http://www.dyc.edu', 'http://www.ecc.edu', 'http://www.elmira.edu', 'http://www.esc.edu', 'http://www.esf.edu', 'http://www.esm.rochester.edu', 'http://www.excelsior.edu', 'http://www.farmingdale.edu', 'http://www.fitnyc.edu', 'http://www.flcc.edu', 'http://www.fmcc.suny.edu', 'http://www.fredonia.edu', 'http://www.ftc.edu', 'http://www.gc.cuny.edu', 'http://www.genesee.edu', 'http://www.geneseo.edu', 'http://www.gs.columbia.edu', 'http://www.gsb.columbia.edu', 'http://www.gts.edu', 'http://www.guttman.cuny.edu', 'http://www.hamilton.edu', 'http://www.hartwick.edu', 'http://www.helenefuld.edu', 'http://www.herkimer.edu', 'http://www.hilbert.edu', 'http://www.hofstra.edu', 'http://www.holycross.edu/departments/library/website/hiatt/righteous.htm', 'http://www.hostos.cuny.edu', 'http://www.houghton.edu', 'http://www.huc.edu', 'http://www.hunter.cuny.edu', 'http://www.hvcc.edu', 'http://www.hws.edu', 'http://www.ilr.cornell.edu', 'http://www.iona.edu', 'http://www.ithaca.edu', 'http://www.ithaca.edu/hs/index.php', 'http://www.ithaca.edu/music', 'http://www.jjay.cuny.edu', 'http://www.jtsa.edu', 'http://www.juilliard.edu', 'http://www.keuka.edu', 'http://www.kingsborough.edu', 'http://www.lagcc.cuny.edu', 'http://www.law.columbia.edu', 'http://www.law.cuny.edu', 'http://www.law.nyu.edu', 'http://www.lehman.cuny.edu', 'http://www.lemoyne.edu', 'http://www.liberalstudies.nyu.edu', 'http://www.limcollege.edu', 'http://www.liu.edu', 'http://www.liu.edu/post', 'http://www.macaulay.cuny.edu', 'http://www.manhattan.edu', 'http://www.marist.edu', 'http://www.mcny.edu/index.php', 'http://www.mec.cuny.edu', 'http://www.med.nyu.edu', 'http://www.medaille.edu', 'http://www.mercy.edu', 'http://www.mmm.edu', 'http://www.molloy.edu', 'http://www.monroecc.edu', 'http://www.monroecollege.edu', 'http://www.morrisville.edu', 'http://www.mountsaintvincent.edu', 'http://www.msmc.edu', 'http://www.msmnyc.edu', 'http://www.mvcc.edu', 'http://www.mville.edu', 'http://www.naz.edu', 'http://www.ncc.edu', 'http://www.nccc.edu', 'http://www.newpaltz.edu', 'http://www.newschool.edu/jazz', 'http://www.newschool.edu/lang', 'http://www.newschool.edu/mannes', 'http://www.niagara.edu', 'http://www.niagaracc.suny.edu', 'http://www.nyack.edu', 'http://www.nycc.edu', 'http://www.nyit.edu', 'http://www.nyts.edu', 'http://www.nyu.edu/gsas/dept/fineart', 'http://www.oldwestbury.edu', 'http://www.oswego.edu', 'http://www.paulsmiths.edu', 'http://www.potsdam.edu', 'http://www.potsdam.edu/crane', 'http://www.pratt.edu', 'http://www.purchase.edu', 'http://www.qc.cuny.edu', 'http://www.qcc.cuny.edu', 'http://www.rit.edu', 'http://www.roberts.edu', 'http://www.rochester.edu', 'http://www.rochester.edu/college', 'http://www.rpi.edu', 'http://www.sage.edu', 'http://www.sarahlawrence.edu', 'http://www.sbu.edu', 'http://www.sfc.edu', 'http://www.simon.rochester.edu', 'http://www.sjcny.edu', 'http://www.sjfc.edu', 'http://www.skidmore.edu', 'http://www.stac.edu', 'http://www.stern.nyu.edu', 'http://www.stjohns.edu', 'http://www.stlawu.edu', 'http://www.stonybrook.edu', 'http://www.suny.edu', 'http://www.sunyacc.edu', 'http://www.sunybroome.edu', 'http://www.sunycgcc.edu', 'http://www.sunydutchess.edu', 'http://www.sunyjcc.edu', 'http://www.sunyjefferson.edu', 'http://www.sunymaritime.edu', 'http://www.sunyocc.edu', 'http://www.sunyopt.edu', 'http://www.sunyorange.edu', 'http://www.sunyrockland.edu', 'http://www.sunysccc.edu', 'http://www.sunysuffolk.edu', 'http://www.sunysullivan.edu', 'http://www.sunyulster.edu', 'http://www.sunywcc.edu', 'http://www.syracuse.edu', 'http://www.tompkinscortland.edu', 'http://www.tourolaw.edu', 'http://www.trocaire.edu', 'http://www.union.edu', 'http://www.upstate.edu', 'http://www.usmma.edu', 'http://www.utsnyc.edu', 'http://www.vassar.edu', 'http://www.vaughn.edu', 'http://www.villa.edu', 'http://www.warner.rochester.edu', 'http://www.webb.edu', 'http://www.wells.edu', 'http://www.york.cuny.edu', 'http://www.yu.edu', 'http://www.yu.edu/riets', 'http://www.yu.edu/stern', 'http://www.yu.edu/syms', 'https://cals.cornell.edu', 'https://sipa.columbia.edu', 'https://web.archive.org/web/20090323023104/http://www.siena.edu/level3col.aspx?menu_id=528&amp;id=108', 'https://www.devry.edu', 'https://www.hofstra.edu/academics/colleges/zarb', 'https://www.human.cornell.edu', 'https://www.newschool.edu', 'https://www.newschool.edu/performing-arts', 'https://www.nyfa.edu', 'https://www.nyu.edu', 'https://www.plattsburgh.edu', 'https://www.suny.edu/campuses/cornell-vet']
    
    
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













