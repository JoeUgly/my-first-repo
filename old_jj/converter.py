# Desc: Convert error URLs to non error


import urllib.request, urllib.parse, os, platform, time, queue, webbrowser, sys, re
from urllib.error import URLError

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'
#user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'



url_l = ['http://classicalcharterschools.org/about/schools/south-bronx-classical-charter-school-iv', 'http://enterprisecharter.org', 'http://ivyhillprep.org', 'http://jerichoschools.org', 'http://successacademies.org/schools/bed-stuy-1', 'http://successacademies.org/schools/bed-stuy-2', 'http://successacademies.org/schools/bensonhurst', 'http://successacademies.org/schools/bergen-beach', 'http://successacademies.org/schools/bronx-1', 'http://successacademies.org/schools/bronx-2', 'http://successacademies.org/schools/bronx-3', 'http://successacademies.org/schools/cobble-hill', 'http://successacademies.org/schools/crown-heights', 'http://successacademies.org/schools/fort-greene', 'http://successacademies.org/schools/harlem-1', 'http://successacademies.org/schools/harlem-2', 'http://successacademies.org/schools/harlem-3', 'http://successacademies.org/schools/harlem-4', 'http://successacademies.org/schools/harlem-5', 'http://successacademies.org/schools/hells-kitchen', 'http://successacademies.org/schools/prospect-heights', 'http://successacademies.org/schools/springfield-gardens', 'http://successacademies.org/schools/union-square', 'http://successacademies.org/schools/upper-west', 'http://successacademies.org/schools/washington-heights', 'http://successacademies.org/schools/williamsburg', 'http://www.1000islandsschools.org', 'http://www.aacs.wnyric.org', 'http://www.arlingtonschools.org/pages/arlington_schools', 'http://www.auburn.wednet.edu', 'http://www.bellmore.k12.ny.us', 'http://www.bhbl.org', 'http://www.binghamtonschools.org', 'http://www.boltoncsd.org', 'http://www.brcsd.org', 'http://www.brockport.k12.ny.us', 'http://www.carthagecsd.org', 'http://www.ccsdk12.org', 'http://www.cliftonfine.org', 'http://www.clydesavannah.org', 'http://www.dolgeville.org', 'http://www.ecs.k12.ny.us', 'http://www.ercsd.org/pages/east_ramapo_csd', 'http://www.erschools.org', 'http://www.explorenetwork.org/empower-charter-school', 'http://www.explorenetwork.org/explore-charter-school', 'http://www.fortedward.org', 'http://www.franklinsquare.k12.ny.us', 'http://www.galwaycsd.org', 'http://www.gfsd.org', 'http://www.greenisland.org', 'http://www.hccs-nys.org', 'http://www.hicksvillepublicschools.org', 'http://www.hlcs.org', 'http://www.hoosicvalley.k12.ny.us', 'http://www.icahncharterschool2.org', 'http://www.icsd.k12.ny.us', 'http://www.innovationhs.org', 'http://www.ircsd.org', 'http://www.jamestownpublicschools.org', 'http://www.johnsburgcsd.org', 'http://www.lackawannaschools.org', 'http://www.lacs-ny.org', 'http://www.lawrence.org', 'http://www.littleflowerufsd.org', 'http://www.longwood.k12.ny.us', 'http://www.morriscs.org', 'http://www.ncsharlem.org/bronx', 'http://www.newventurescharterschool.org', 'http://www.niagaracharter.org', 'http://www.ovcs.org', 'http://www.peninsulaprep.org', 'http://www.portjeff.k12.ny.us', 'http://www.rockypointschools.org', 'http://www.romecsd.org', 'http://www.rvcschools.org', 'http://www.sacketspatriots.org', 'http://www.sascs.org', 'http://www.schalmont.org', 'http://www.schenectady.k12.ny.us', 'http://www.tapestryschool.org/academic-and-social-programs/k-8', 'http://www.tepcharter.org', 'http://www.theamericandreamschool.org', 'http://www.uascs.org', 'http://www.westirondequoit.org', 'http://www.wyomingcsd.org', 'http://yalowcharter.org', 'https://boldschools.org', 'https://www.bronxbetterlearning.org/apps/pages/index.jsp?urec_id=772803&amp;type=d&amp;prec_id=1173266', 'https://www.persistenceprep.org/mission']


def convert(workingurl):
    if workingurl.endswith('/'):
        workingurl = workingurl.rsplit('/',1)[0]

    #print('\nold workingurl =', workingurl)
    workingurl = workingurl.rsplit('/',1)[0]
    #print('\nnew workingurl =', workingurl)
    return(workingurl)

bad_list = []
finalg = []



for workingurl in url_l:
    workingurl1 = workingurl

    # Spoof user agent
    while True:

        if workingurl == 'http:' or workingurl == 'https:': 
            print('final error at:', workingurl1)
            bad_list.append(workingurl1)
            break

        try:
            request = urllib.request.Request(workingurl, headers={'User-Agent': user_agent})
            html = urllib.request.urlopen(request, timeout=10)
            break

        except Exception as errex:
            workingurl = convert(workingurl)
            continue

    if workingurl == 'http:' or workingurl == 'https:': 
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
            print('error 2:', charset_encoding, 'decode at', workingurl)
            continue

    
    print('Complete:', workingurl)
    finalg.append(workingurl)


print('\n\nBad list:')
for i in bad_list:
    print(i)

print('\n\nGood list:')
for i in finalg:
    print(i)


# Replace error entries in file
for x in finalg:
    for i in url_l:
        if x in i:
            i = x

print('\n\nNew Good list:')
for i in finalg:
    print(i)








Bad list:
http://enterprisecharter.org
http://www.bellmore.k12.ny.us
http://www.bhbl.org
http://www.gfsd.org
http://www.greenisland.org
http://www.icsd.k12.ny.us
http://www.innovationhs.org
http://www.lacs-ny.org
http://www.newventurescharterschool.org
http://www.schalmont.org
http://www.westirondequoit.org


Good list:
http://classicalcharterschools.org/about/schools
http://ivyhillprep.org
http://jerichoschools.org
http://successacademies.org/schools/bed-stuy-1
http://successacademies.org/schools/bed-stuy-2
http://successacademies.org/schools/bensonhurst
http://successacademies.org/schools/bergen-beach
http://successacademies.org/schools/bronx-1
http://successacademies.org/schools/bronx-2
http://successacademies.org/schools/bronx-3
http://successacademies.org/schools/cobble-hill
http://successacademies.org/schools/crown-heights
http://successacademies.org/schools/fort-greene
http://successacademies.org/schools/harlem-1
http://successacademies.org/schools/harlem-2
http://successacademies.org/schools/harlem-3
http://successacademies.org/schools/harlem-4
http://successacademies.org/schools/harlem-5
http://successacademies.org/schools/hells-kitchen
http://successacademies.org/schools/prospect-heights
http://successacademies.org/schools/springfield-gardens
http://successacademies.org/schools/union-square
http://successacademies.org/schools/upper-west
http://successacademies.org/schools/washington-heights
http://successacademies.org/schools/williamsburg
http://www.1000islandsschools.org
http://www.aacs.wnyric.org
http://www.arlingtonschools.org
http://www.auburn.wednet.edu
http://www.binghamtonschools.org
http://www.boltoncsd.org
http://www.brcsd.org
http://www.brockport.k12.ny.us
http://www.carthagecsd.org
http://www.ccsdk12.org
http://www.cliftonfine.org
http://www.clydesavannah.org
http://www.dolgeville.org
http://www.ecs.k12.ny.us
http://www.ercsd.org
http://www.erschools.org
http://www.explorenetwork.org/empower-charter-school
http://www.explorenetwork.org/explore-charter-school
http://www.fortedward.org
http://www.franklinsquare.k12.ny.us
http://www.galwaycsd.org
http://www.hccs-nys.org
http://www.hicksvillepublicschools.org
http://www.hlcs.org
http://www.hoosicvalley.k12.ny.us
http://www.icahncharterschool2.org
http://www.ircsd.org
http://www.jamestownpublicschools.org
http://www.johnsburgcsd.org
http://www.lackawannaschools.org
http://www.lawrence.org
http://www.littleflowerufsd.org
http://www.longwood.k12.ny.us
http://www.morriscs.org
http://www.ncsharlem.org
http://www.niagaracharter.org
http://www.ovcs.org
http://www.peninsulaprep.org
http://www.portjeff.k12.ny.us
http://www.rockypointschools.org
http://www.romecsd.org
http://www.rvcschools.org
http://www.sacketspatriots.org
http://www.sascs.org
http://www.schenectady.k12.ny.us
http://www.tapestryschool.org
http://www.tepcharter.org
http://www.theamericandreamschool.org
http://www.uascs.org
http://www.wyomingcsd.org
http://yalowcharter.org
https://boldschools.org
https://www.bronxbetterlearning.org/apps
https://www.persistenceprep.org/mission


New Good list:
http://classicalcharterschools.org/about/schools
http://ivyhillprep.org
http://jerichoschools.org
http://successacademies.org/schools/bed-stuy-1
http://successacademies.org/schools/bed-stuy-2
http://successacademies.org/schools/bensonhurst
http://successacademies.org/schools/bergen-beach
http://successacademies.org/schools/bronx-1
http://successacademies.org/schools/bronx-2
http://successacademies.org/schools/bronx-3
http://successacademies.org/schools/cobble-hill
http://successacademies.org/schools/crown-heights
http://successacademies.org/schools/fort-greene
http://successacademies.org/schools/harlem-1
http://successacademies.org/schools/harlem-2
http://successacademies.org/schools/harlem-3
http://successacademies.org/schools/harlem-4
http://successacademies.org/schools/harlem-5
http://successacademies.org/schools/hells-kitchen
http://successacademies.org/schools/prospect-heights
http://successacademies.org/schools/springfield-gardens
http://successacademies.org/schools/union-square
http://successacademies.org/schools/upper-west
http://successacademies.org/schools/washington-heights
http://successacademies.org/schools/williamsburg
http://www.1000islandsschools.org
http://www.aacs.wnyric.org
http://www.arlingtonschools.org
http://www.auburn.wednet.edu
http://www.binghamtonschools.org
http://www.boltoncsd.org
http://www.brcsd.org
http://www.brockport.k12.ny.us
http://www.carthagecsd.org
http://www.ccsdk12.org
http://www.cliftonfine.org
http://www.clydesavannah.org
http://www.dolgeville.org
http://www.ecs.k12.ny.us
http://www.ercsd.org
http://www.erschools.org
http://www.explorenetwork.org/empower-charter-school
http://www.explorenetwork.org/explore-charter-school
http://www.fortedward.org
http://www.franklinsquare.k12.ny.us
http://www.galwaycsd.org
http://www.hccs-nys.org
http://www.hicksvillepublicschools.org
http://www.hlcs.org
http://www.hoosicvalley.k12.ny.us
http://www.icahncharterschool2.org
http://www.ircsd.org
http://www.jamestownpublicschools.org
http://www.johnsburgcsd.org
http://www.lackawannaschools.org
http://www.lawrence.org
http://www.littleflowerufsd.org
http://www.longwood.k12.ny.us
http://www.morriscs.org
http://www.ncsharlem.org
http://www.niagaracharter.org
http://www.ovcs.org
http://www.peninsulaprep.org
http://www.portjeff.k12.ny.us
http://www.rockypointschools.org
http://www.romecsd.org
http://www.rvcschools.org
http://www.sacketspatriots.org
http://www.sascs.org
http://www.schenectady.k12.ny.us
http://www.tapestryschool.org
http://www.tepcharter.org
http://www.theamericandreamschool.org
http://www.uascs.org
http://www.wyomingcsd.org
http://yalowcharter.org
https://boldschools.org
https://www.bronxbetterlearning.org/apps
https://www.persistenceprep.org/mission

















