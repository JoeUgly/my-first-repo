# Description: parse street address results given by addr_mp.py

# To do:
# remove dups from crawling
# Put coords into dict
# remove backslash characters from loc files

# This file contains 
f_h = open('/home/joepers/jorbs/results.txt')
all_urls = []
new_l = []
final_simple = []


# Get URLs
for i in f_h:
    if i == '\n':
        continue
    u = i.split("'")[3]
    u = u.split("'")[0]
    all_urls.append(u)
    
    # Get locations
    i = i.split('::')[1]
    i = i.split('[')[1]
    i = i.split(']')[0]
    #i = i.split("'")
    
    ui = u, i
    final_simple.append(ui)
    print(ui)





# Find which URLs do not have location data
# civ
#orig_h = ['http://cityofpoughkeepsie.com/personnel/&', 'http://cmvny.com/departments/civil-service', 'http://co.sullivan.ny.us/departments/departmentsnz/personnel/civilserviceexams/tabid/3382/default.aspx', 'http://franklincony.org/content/departments/view/6:field=services;/content/departmentservices/view/48', 'http://isliptown-ny.gov/index.php/i-want-to/apply-for/employment-with-the-town?_sm_au_=ivvt78qz5w7p2qhf', 'http://oneidacity.com/civil-service', 'http://oswegocounty.com/humanresources.shtml', 'http://town.clarkstown.ny.us/town_hall/personnel', 'http://web.co.wayne.ny.us/human-resources', 'http://www.albanyny.org/government/departments/humanresources/employment/examschedule.aspx', 'http://www.amherst.ny.us/govt/govt_dept.asp?dept_id=dept_12&amp;div_id=div_18&amp;menu_id=menu_04&amp;_sm_au_=ivv8z8lp1wffsnv6', 'http://www.brookhaven.org/departments/officeofthesupervisor/personnel.aspx?_sm_au_=ivvt78qz5w7p2qhf', 'http://www.cityofelmira.net/personnel', 'http://www.cityofglencoveny.org/index.htm', 'http://www.cityofithaca.org/299/civil-service-examinations', 'http://www.citywatertown.org/index.asp?nid=111', 'http://www.co.delaware.ny.us/departments/pers/pers.htm', 'http://www.co.dutchess.ny.us/countygov/departments/personnel/psexamannouncements.htm', 'http://www.co.essex.ny.us/jobs.asp', 'http://www.co.jefferson.ny.us/index.aspx?page=83', 'http://www.cohoes.com/cit-e-access/webpage.cfm?tid=34&amp;tpid=6383', 'http://www.fultoncountyny.gov/node/5', 'http://www.gobroomecounty.com/personnel/cs', 'http://www.greenburghny.com/cit-e-access/webpage.cfm?tid=10&amp;tpid=2491&amp;_sm_au_=ivvt78qz5w7p2qhf', 'http://www.newrochelleny.com/index.aspx?nid=362', 'http://www.ongov.net/employment/civilservice.html', 'http://www.ongov.net/employment/jurisdiction.html', 'http://www.penfield.org/human_resources.php', 'http://www.rvcny.us/jobs.html?_sm_au_=ivv8z8lp1wffsnv6', 'http://www.ryeny.gov/human-resources.cfm', 'http://www.schenectadycounty.com/fullstory.aspx?m=36&amp;amid=373', 'http://www.schenectadycounty.com/fullstory.aspx?m=36&amp;amid=373&amp;_sm_au_=ivvt78qz5w7p2qhf', 'http://www.schohariecounty-ny.gov/countywebsite/personnel/civilserviceservices.html', 'http://www.smithtownny.gov/jobs.aspx?_sm_au_=ivvt78qz5w7p2qhf', 'http://www.townofcortlandt.com/cit-e-access/webpage.cfm?tid=20&amp;tpid=2522&amp;_sm_au_=ivvt78qz5w7p2qhf', 'http://www.townofhempstead.org/civil-service-commission?_sm_au_=ivv8z8lp1wffsnv6', 'http://www.townofunion.com/depts_services_human_full.html', 'http://www.usajobs.gov', 'http://www1.nyc.gov/jobs', 'https://seneca-portal.mycivilservice.com', 'https://www.co.montgomery.ny.us/sites/public/government/personnel/personnel_development/default.aspx']


# school
orig_h = ['http://www.easthamptonschools.org', 'http://www.edinburgcs.org', 'http://www.evcsbuffalo.org', 'http://www.frontier.wnyric.org', 'http://www.gateschili.org', 'http://www.gccschool.org', 'http://www.genvalley.org', 'http://www.hamburgschools.org', 'http://www.hcsk12.org', 'http://www.hufsd.edu', 'http://www.johnstownschools.org', 'http://www.kipptechvalley.org', 'http://www.lafargevillecsd.org', 'http://www.letchworth.k12.ny.us', 'http://www.moriahk12.org', 'http://www.nfschools.net', 'http://www.oceansideschools.org', 'http://www.sacketspatriots.org', 'http://www.slcs.org', 'http://www.starpointcsd.org', 'http://www.ticonderogak12.org', 'http://www.urbanchoicecharter.org', 'http://www.yonkerspublicschools.org', 'http://www.youngwomenscollegeprep.org', 'https://sbecacs.org', 'https://sites.google.com/a/northvillecsd.org/ncsd', 'https://urbanassembly.org', 'https://www.hdcsk12.org', 'https://www.heuvelton.k12.ny.us', 'https://www.prattsburghcsd.org', 'https://www.webutuckschools.org', 'http://ccny.cuny.edu/csom', 'http://engineering.nyu.edu', 'http://lcm.touro.edu', 'http://www.berkeleycollege.edu/index.htm', 'http://www.delhi.edu', 'http://www.mercy.edu', 'http://www.qcc.cuny.edu']


# uni
#orig_h = ['http://drama.newschool.edu', 'http://engineering.nyu.edu', 'http://gallatin.nyu.edu', 'http://globe.edu', 'http://journalism.cuny.edu', 'http://socialwork.nyu.edu', 'http://usma.edu', 'http://www.asa.edu', 'http://www.bmcc.cuny.edu', 'http://www.downstate.edu', 'http://www.elmira.edu', 'http://www.esf.edu', 'http://www.hamilton.edu', 'http://www.holycross.edu/departments/library/website/hiatt/righteous.htm', 'http://www.keuka.edu', 'http://www.kingsborough.edu', 'http://www.nccc.edu', 'http://www.nyu.edu/gsas/dept/fineart', 'https://web.archive.org/web/20090323023104/http://www.siena.edu/level3col.aspx?menu_id=528&amp;id=108', 'https://www.devry.edu', 'https://www.newschool.edu/performing-arts', 'https://www.nyu.edu']






need = []
num = 0

for i in orig_h:
    i = i.strip()
    num += 1
    if not i in all_urls:
        need.append(i)

print('\n\nStill need data for:', len(need), 'of', num, '\n')

print(sorted(need))


for i in need:
    print(i)




































