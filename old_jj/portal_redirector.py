
# Desc: convert portal URLs to redirected URLs




import urllib.request
from http.cookiejar import CookieJar




portals = [
['http://cityofpoughkeepsie.com/personnel/', 0, (41.7065779, -73.9284101)],
['http://www.greenegovernment.com/departments/human-resources-and-civil-service', 0, (42.1956438, -74.1337508)],
['http://humanresources.westchestergov.com/job-seekers/civil-service-exams', 0, (41.0339862, -73.7629097)],
['https://kingston-ny.gov/employment', 0, (41.9287812, -74.0023702)],
['http://niagarafallsusa.org/government/city-departments/human-resources-department/', 0, (43.1030928, -79.0302618)],
['https://www.cityofwhiteplains.com/98/Personnel', 0, (41.0335885, -73.7639768)],
['http://ocgov.net/personnel', 0, (43.104752, -75.2229497)],
['http://oneidacity.com/473-2/', 0, (43.2144051, -75.4039155)],
['http://oswegocounty.com/humanresources/openings.php', 0, (43.4547284, -76.5095967)],
['http://oysterbaytown.com/departments/human-resources/', 0, (40.6806564, -73.4742914)],
['http://rocklandgov.com/departments/personnel/civil-service-examinations', 0, (41.1469917, -73.9902998)],
['http://sullivanny.us/index.php/Departments/Personnel', 0, (41.6556465, -74.6893282)],
['http://tompkinscountyny.gov/personnel', 0, (42.4396039, -76.4968019)],
['https://www.villageofhempstead.org/197/Employment-Opportunities', 0, (40.7063185, -73.618684)],
['http://watervliet.com/city/civil-service.htm', 0, (42.7282483, -73.7014649039252)],
['https://web.co.wayne.ny.us/', 0, (43.0642305, -76.9902456)],
['http://www.albanycounty.com/Government/Departments/DepartmentofCivilService.aspx', 0, (42.6511674, -73.754968)],
['http://www.alleganyco.com/departments/human-resources-civil-service/', 0, (42.2231241, -78.0344506)],
['http://www.amherst.ny.us', 0, (42.9637836, -78.7377258)],
['http://www.auburnny.gov/public_documents/auburnny_civilservice/index', 0, (42.9320202, -76.5672029)],
['https://www.batavianewyork.com/fire-department/pages/employment', 0, (42.9980144, -78.1875515)],
['http://www.binghamton-ny.gov/departments/personnel/employment/employment', 0, (42.096968, -75.914341)],
['https://www.brookhavenny.gov/', 0, (40.8312096, -73.029552)],
['https://www.cattco.org/human-resources/jobs', 0, (42.252563, -78.80559)],
['https://www.chemungcountyny.gov/departments/a_-_f_departments/civil_service_personnel/index.php', 0, (42.0897965, -76.8077338)],
['https://www.buffalony.gov/', 0, (42.8867166, -78.8783922)],
['http://www.ci.webster.ny.us/85/Human-Resources', 0, (43.263428, -77.4334757)],
['http://www.cityofelmira.net/personnel', 0, (42.0897965, -76.8077338)],
['http://www.cityofglencoveny.org/index.htm', 0, (40.862755, -73.6336094)],
['http://www.cityofglensfalls.com/55/Human-Resources-Department', 0, (43.3772932, -73.6131714)],
['https://ithaca-portal.mycivilservice.com/', 0, (42.4396039, -76.4968019)],
['https://www.cityofnewburgh-ny.gov/civil-service', 0, (41.5034271, -74.0104179)],
['https://www.cityofpeekskill.com/human-resources/pages/about-human-resources', 0, (41.289811, -73.9204922)],
['https://www.cityofrochester.gov/article.aspx?id=8589936759', 0, (43.157285, -77.615214)],
['http://www.cityofschenectady.com/208/Human-Resources', 0, (42.8143922952735, -73.9420906329747)],
['http://www.cityofutica.com/departments/civil-service/index', 0, (43.1009031, -75.2326641)],
['https://www.cliftonpark.org/services/employment-applications.html', 0, (42.8656325, -73.7709535)],
['https://www.clintoncountygov.com/employment', 0, (44.69282, -73.45562)],
['http://www.co.chautauqua.ny.us/314/Human-Resources', 0, (42.253947, -79.504491)],
['http://www.co.chenango.ny.us/personnel/examinations/', 0, (42.531184, -75.5235149)],
['http://www.co.delaware.ny.us/departments/pers/jobs.htm', 0, (42.2781401, -74.9159946)],
['http://www.co.dutchess.ny.us/civilserviceinformationsystem/applicantweb/frmannouncementlist.aspx?aspxerrorpath=/civilserviceinformationsystem/applicantweb/frmuserlogin', 0, (41.7065779, -73.9284101)],
['https://www.dutchessny.gov/Departments/Human-Resources/Human-Resources.htm', 0, (41.7065779, -73.9284101)],
['http://www.co.essex.ny.us/jobs.asp', 0, (44.216171, -73.591232)],
['http://www.co.genesee.ny.us/departments/humanresources/index.php', 0, (42.9980144, -78.1875515)],
['https://co.jefferson.ny.us/', 0, (43.9747838, -75.9107565)],
['https://www.livingstoncounty.us/207/Personnel-Department', 0, (42.795896, -77.816947)],
['http://www.co.ontario.ny.us/jobs.aspx', 0, (42.8844625, -77.278399)],
['https://www.stlawco.org/departments/humanresources/examinationschedule', 0, (44.5956163, -75.1690942)],
['https://ulstercountyny.gov/personnel/index.html', 0, (41.9287812, -74.0023702)],
['https://www.ci.cohoes.ny.us/', 0, (42.7742446, -73.7001187)],
['http://www.cortland-co.org/263/Personnel-Civil-Service', 0, (42.6000833, -76.1804347)],
['https://www.cs.ny.gov/', 0, (42.6511674, -73.754968)],
['https://www2.cuny.edu/employment/civil-service/', 0, (40.7308619, -73.9871558)],
['http://www.eastchester.org/departments/comptoller.php', 0, (40.9562415, -73.8129474)],
['http://eastfishkillny.gov/government/employment.htm', 0, (41.5839824, -73.8087442)],
['http://www2.erie.gov/employment/', 0, (42.8867166, -78.8783922)],
['https://www.fultoncountyny.gov/node/5', 0, (43.0068689, -74.3676437)],
['http://www.gobroomecounty.com/personnel/cs', 0, (42.1156308, -75.9588092)],
['http://www.greenburghny.com', 0, (41.0447887, -73.803487)],
['https://www.hamiltoncounty.com/government/departments-services', 0, (43.47111, -74.412804)],
['http://www.huntingtonny.gov/content/13753/13757/17478/17508/default.aspx?_sm_au_=ivvt78qz5w7p2qhf', 0, (40.868154, -73.425676)],
['http://www.irondequoit.org/town-departments/human-resources/town-employment-opportunities?_sm_au_=ivv8z8lp1wffsnv6', 0, (43.1854754, -77.6106861508176)],
['http://lackawannany.gov/government/civil-service/', 0, (42.8262, -78.820732)],
['https://www.lockportny.gov/current-exams-and-openings/', 0, (43.168863, -78.6929557832681)],
['https://www.longbeachny.gov/index.asp?type=b_basic&amp;sec={9c88689c-135f-4293-a9ce-7a50346bea23}', 0, (40.58888905, -73.6648751135986)],
['http://www.mechanicville.com/index.aspx?nid=563', 0, (42.903367, -73.686416)],
['https://www.middletown-ny.com/en/departments/civil-service.html?_sm_au_=ivvrlpv4fvqpnjqj', 0, (41.44591415, -74.4224417389405)],
['http://www.nassaucivilservice.com/nccsweb/homepage.nsf/homepage?readform', 0, (40.7063185, -73.618684)],
['https://www.newrochelleny.com/362/Civil-Service', 0, (40.9114459, -73.7841684271834)],
['http://www.niagaracounty.com/Departments/Civil-Service', 0, (43.168863, -78.6929557832681)],
['https://www.northhempsteadny.gov/employment-opportunities', 0, (40.7978787, -73.6995749)],
['https://www.norwichnewyork.net/government/human-resources.php', 0, (42.531184, -75.5235149)],
['http://www.ogdensburg.org/index.aspx?nid=97', 0, (44.694285, -75.486374)],
['http://www.oneonta.ny.us/departments/personnel', 0, (42.453492, -75.0629531)],
['http://www.ongov.net/employment/civilService.html', 0, (43.0481221, -76.1474244)],
['http://www.ongov.net/employment/jurisdiction.html', 0, (43.158679, -76.33271)],
['http://www.ongov.net/employment/jurisdiction.html?_sm_au_=ivvrlpv4fvqpnjqj', 0, (43.0481221, -76.1474244)],
['http://www.orleansny.com/personnel', 0, (43.246488, -78.193516)],
['http://www.oswegony.org/government/personnel', 0, (43.4547284, -76.5095967)],
['http://www.otsegocounty.com/depts/per/', 0, (42.7006303, -74.924321)],
['http://www.penfield.org', 0, (43.1301133, -77.4759588)],
['http://www.perinton.org/departments/finpers', 0, (43.0993, -77.443014)],
['https://www.putnamcountyny.com/personneldept/', 0, (41.4266361, -73.6788272)],
['https://www.putnamcountyny.com/personneldept/exam-postings/', 0, (41.4266361, -73.6788272)],
['http://www.ramapo.org/page/personnel-30.html?_sm_au_=ivvt78qz5w7p2qhf', 0, (41.1151372, -74.1493948)],
['http://www.rensco.com/county-job-assistance/', 0, (42.7284117, -73.6917878)],
['http://www.rvcny.us/jobs.html?_sm_au_=ivv8z8lp1wffsnv6', 0, (40.6574186, -73.6450664)],
['https://www.ryeny.gov/', 0, (40.9808209, -73.684294)],
['http://www.saratoga-springs.org/jobs.aspx', 0, (43.0821793, -73.7853915)],
['https://www.saratogacountyny.gov/departments/personnel/', 0, (43.0009087, -73.8490111)],
['https://www.schenectadycounty.com/', 0, (42.8143922952735, -73.9420906329747)],
['https://www4.schohariecounty-ny.gov/', 0, (42.5757217, -74.4390277)],
['http://www.schuylercounty.us/119/Civil-Service', 0, (42.3810555, -76.8705777)],
['http://www.smithtownny.gov/jobs.aspx?_sm_au_=ivvt78qz5w7p2qhf', 0, (40.8559314, -73.2006687)],
['http://www.southamptontownny.gov/jobs.aspx', 0, (40.884267, -72.3895296)],
['https://www.steubencony.org/pages.asp?pgid=32', 0, (42.3370164, -77.3177577)],
['https://www.suffolkcountyny.gov/Departments/Civil-Service', 0, (40.8256537, -73.2026138)],
['http://www.tiogacountyny.com/departments/personnel-civil-service', 0, (42.1034075, -76.2621549)],
['https://www.tonawandacity.com/residents/civil_service.php', 0, (42.991733, -78.8824886119079)],
['http://www.townofbethlehem.org/137/Human-Resources?_sm_au_=ivv8z8lp1wffsnv6', 0, (42.6220235, -73.8326232)],
['https://www.townofbrighton.org/219/Human-Resources', 0, (43.1635257, -77.6083784825996)],
['http://www.townofchili.org/notice-category/job-postings/', 0, (43.157285, -77.615214)],
['http://www.townofcortlandt.com', 0, (41.248774, -73.9086846461571)],
['https://www.townofguilderland.org/human-resource-department?_sm_au_=ivv8z8lp1wffsnv6', 0, (42.704522, -73.911513)],
['https://www.townofossining.com/cms/resources/human-resources', 0, (41.1613168, -73.8620367)],
['http://www.townofpittsford.org/home-hr?_sm_au_=ivv8z8lp1wffsnv6', 0, (43.090959, -77.515298)],
['https://www.townofriverheadny.gov/pview.aspx?id=2481&amp;catid=118&amp;_sm_au_=ivvt78qz5w7p2qhf', 0, (40.9170435, -72.6620402)],
['https://www.townofunion.com/', 0, (42.1128526, -76.021034)],
['https://www.townofwallkill.com/index.php/departments/human-resources', 0, (41.44591415, -74.4224417389405)],
['http://www.troyny.gov/departments/personnel-department/', 0, (42.7284117, -73.6917878)],
['https://www.usajobs.gov/', 0, (44.933143, 7.540121)],
['https://www.vestalny.com/departments/human_resources/job_opportunities.php', 0, (42.0850747, -76.053813)],
['https://www.villageofossining.org/personnel-department', 0, (41.1613168, -73.8620367)],
['https://www.vsvny.org/index.asp?type=b_job&amp;sec=%7b05c716c7-40ee-49ee-b5ee-14efa9074ab9%7d&amp;_sm_au_=ivv8z8lp1wffsnv6', 0, (40.6715969, -73.6982991)],
['http://www.warrencountyny.gov/civilservice/exams.php', 0, (43.425996, -73.712425)],
['http://www.washingtoncountyny.gov/jobs.aspx', 0, (43.267206, -73.584709)],
['http://www.wyomingco.net/164/Civil-Service', 0, (42.74271215, -78.1326011420972)],
['https://www.yatescounty.org/203/Personnel', 0, (42.6609248, -77.0563316)],
['https://www.yonkersny.gov/work/jobs-civil-service-exams', 0, (40.9312099, -73.8987469)],
['https://www.yorktownny.org/jobs', 0, (41.2709274, -73.7776336)],
['https://www1.nyc.gov/jobs', 0, (40.7308619, -73.9871558)],
['https://www1.nyc.gov/jobs/index.page', 0, (40.7308619, -73.9871558)],
['https://www2.monroecounty.gov/careers', 0, (43.157285, -77.615214)],
['https://countyfranklin.digitaltowpath.org:10078/content/Departments/View/6:field=services;/content/DepartmentServices/View/48', 0, (44.831732274226, -74.5184874695369)],
['https://countyherkimer.digitaltowpath.org:10069/content/Departments/View/9', 0, (43.0256259, -74.9859889)],
['https://mycivilservice.rocklandgov.com', 0, (41.1670394, -74.043197)],
['https://mycivilservice.schenectadycounty.com', 0, (42.8143922952735, -73.9420906329747)],
['https://romenewyork.com/civil-service/', 0, (43.2128473, -75.4557304)],
['https://seneca-portal.mycivilservice.com', 0, (42.9047884, -76.8627368)],
['https://sites.google.com/a/columbiacountyny.com/civilservice/', 0, (42.2528649, -73.790959)],
['https://www.albanyny.gov/government/departments/humanresources/employment', 0, (42.6511674, -73.754968)],
['https://www.colonie.org/departments/civilservice/', 0, (42.7442986, -73.7614799)],
['https://www.lewiscounty.org/departments/human-resources/human-resources', 0, (43.7884182, -75.4935757)],
['https://www.madisoncounty.ny.gov/287/Personnel', 0, (43.075408, -75.70713)],
['https://www.monroeny.org/doc-center/town-of-monroe-job-opportunities.html', 0, (41.3304767, -74.1866348)],
['https://www.orangecountygov.com/1137/Human-Resources', 0, (41.4020382, -74.3243191)],
['https://www.orangetown.com/groups/department/personnel/', 0, (41.0465776, -73.9496707)],
['http://www.cayugacounty.us/QuickLinks.aspx?CID=103', 0, (42.932628, -76.5643831)],
['https://hempsteadny.gov/employment-services', 0, (40.7063185, -73.618684)],
['https://www.co.montgomery.ny.us/web/sites/departments/personnel/employment.asp', 0, (42.9545179, -74.3765241)],
['http://cmvny.com/departments/civil-service/job-postings', 0, (40.9125992, -73.8370786)],
['http://www.townofpoughkeepsie.com/human_resources/index.html?_sm_au_=ivv8z8lp1wffsnv6', 0, (41.7065779, -73.9284101)],
['https://www.watertown-ny.gov/index.asp?nid=791', 0, (43.9747838, -75.9107565)],
['https://www.townofislip-ny.gov/?Itemid=220', 0, (40.7360109, -73.2089705862445)]
]


user_agent_str = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'

# Define HTML request function
def html_requester(workingurl):

    # Request html using a spoofed user agent, cookiejar, and timeout
    try:
        cj = CookieJar()
        req = urllib.request.Request(workingurl, headers={'User-Agent': user_agent_str})
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        html = opener.open(req, timeout=10)
        return html

    ## Catch and log HTTP request errors
    except Exception as errex:

        print('Error at:', workingurl, str(errex))
        bad_l.append(workingurl)
        return False


bad_l = []
fin_l = []


for workinglist in portals:

    workingurl = workinglist[0]

    html = html_requester(workingurl)

    if html == False: continue

    red_url = html.geturl()
    if red_url != workingurl:
        print('redirect from/to', workingurl, red_url)
    else:
        print('No redirect at:', red_url)

    final_list = [red_url, workinglist[1], workinglist[2]]

    fin_l.append(final_list)



print('\n\nFinal list:')
for i in fin_l:
    ii = str(i)+','
    print(ii)


print('\n\nError list:')
for i in bad_l:
    print(i)



















