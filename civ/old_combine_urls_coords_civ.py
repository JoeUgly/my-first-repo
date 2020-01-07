
# Desc: Combine URLs and coordinates for every civil service municipality


# URLs' HTML source: https://labor.ny.gov/stats/cslist.shtm
# Coords source: http://eservices.nysed.gov/sedreports/list?id=1
# All Institutions: Active Institutions with GIS coordinates and OITS Accuracy Code - Select by County


# Features:
# get org name and URL from HTML
# get org name and coords from spreadsheet
# combine the two into a list
# only use results with one match -


# To do:
# results with multiple matches are included but left blank


# Concerns:
# allow duplicate coords? yes because different URLs have their own job postings
# allow dup URLs?: yes because geo limiter may exclude one and dups will be excluded from queue. (Not yet)



import pandas as pd
from bs4 import BeautifulSoup



html = '''
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://www.usajobs.gov/" mce_href="http://www.usajobs.gov/" mce_serialized="2">United States</A></LI>
<LI mce_serialized="2"><A href="https://www.cs.ny.gov/" mce_href="https://www.cs.ny.gov/" mce_serialized="2">New York State</A></LI>
<LI mce_serialized="2"><A href="https://www.cs.ny.gov/jobseeker/local/textmap.cfm" mce_href="https://www.cs.ny.gov/jobseeker/local/textmap.cfm" mce_serialized="2">Local Government</A></LI>
<LI mce_serialized="2"><A href="https://www.cs.ny.gov/employees/local/local.cfm" mce_href="https://www.cs.ny.gov/employees/local/local.cfm" mce_serialized="2">Municipal Civil Service Agencies</A></LI></UL>
<H4 mce_serialized="2">Local Governments</H4>
<DIV class="grid_6 alpha" mce_serialized="2">
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://www.albanycounty.com/civilservice/" mce_href="http://www.albanycounty.com/civilservice/" mce_serialized="2">Albany County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="https://www.albanyny.gov/Government/Departments/HumanResources/Employment.aspx" mce_href="https://www.albanyny.gov/Government/Departments/HumanResources/Employment.aspx" mce_serialized="2">Albany City</A></LI>
<LI mce_serialized="2"><A title="Bethlehem Town" href="http://www.townofbethlehem.org/137/Human-Resources?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.townofbethlehem.org/137/Human-Resources?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_serialized="2">Bethlehem Town</A></LI>
<LI mce_serialized="2"><A href="https://www.ci.cohoes.ny.us/276/Civil-Service" mce_href="https://www.ci.cohoes.ny.us/276/Civil-Service" mce_serialized="2">Cohoes City</A></LI>
<LI mce_serialized="2"><A href="https://www.colonie.org/departments/civilservice/" mce_href="https://www.colonie.org/departments/civilservice/" mce_serialized="2">Colonie Town</A></LI>
<LI mce_serialized="2"><A title="Guilderland Town" href="http://www.townofguilderland.org/pages/guilderlandny_hr/index?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.townofguilderland.org/pages/guilderlandny_hr/index?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_serialized="2">Guilderland Town</A></LI>
<LI mce_serialized="2"><A href="http://watervliet.com/city/civil-service.htm" mce_href="http://watervliet.com/city/civil-service.htm" mce_serialized="2">Watervliet City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www.alleganyco.com/departments/human-resources-civil-service/" mce_href="http://www.alleganyco.com/departments/human-resources-civil-service/" mce_serialized="2">Allegany County</A></LI>
<LI mce_serialized="2"><A href="http://www1.nyc.gov/jobs/index.page" mce_href="http://www1.nyc.gov/jobs/index.page" mce_serialized="2">Bronx County</A> </LI>
<LI mce_serialized="2"><A href="http://www.gobroomecounty.com/personnel/cs" mce_href="http://www.gobroomecounty.com/personnel/cs" mce_serialized="2">Broome County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://www.binghamton-ny.gov/departments/personnel/employment/employment" mce_href="http://www.binghamton-ny.gov/departments/personnel/employment/employment" mce_serialized="2">Binghamton City</A></LI>
<LI mce_serialized="2"><A href="https://www.townofunion.com/index.php/departments/human-resources" mce_href="https://www.townofunion.com/index.php/departments/human-resources" mce_serialized="2">Union Town</A></LI>
<LI mce_serialized="2"><A title="Vestal Town" href="http://www.vestalny.com/departments/human_resources/job_opportunities.php" mce_href="http://www.vestalny.com/departments/human_resources/job_opportunities.php" mce_serialized="2">Vestal Town</A></LI></UL></LI>
<LI mce_serialized="2"><A href="https://cattco-portal.mycivilservice.com/" mce_href="https://cattco-portal.mycivilservice.com/" mce_serialized="2">Cattaraugus County</A></LI>
<LI mce_serialized="2"><A href="http://www.cayugacounty.us/653/Civil-Service-Commission" mce_href="http://www.cayugacounty.us/653/Civil-Service-Commission" mce_serialized="2">Cayuga County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="https://www.auburnny.gov/civil-service" mce_href="https://www.auburnny.gov/civil-service" mce_serialized="2">Auburn City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www.co.chautauqua.ny.us/314/Human-Resources" mce_href="http://www.co.chautauqua.ny.us/314/Human-Resources" mce_serialized="2">Chautauqua County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://www.co.chautauqua.ny.us/314/Human-Resources" mce_href="http://www.co.chautauqua.ny.us/314/Human-Resources" mce_serialized="2">Jamestown City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www.chemungcountyny.gov/departments/a_-_f_departments/civil_service_personnel/index.php" mce_href="http://www.chemungcountyny.gov/departments/a_-_f_departments/civil_service_personnel/index.php" mce_serialized="2">Chemung County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://www.cityofelmira.net/personnel" mce_href="http://www.cityofelmira.net/personnel" mce_serialized="2">Elmira City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www.co.chenango.ny.us/personnel/examinations/" mce_href="http://www.co.chenango.ny.us/personnel/examinations/" mce_serialized="2">Chenango County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://www.norwichnewyork.net/human_resources.html" mce_href="http://www.norwichnewyork.net/human_resources.html" mce_serialized="2">Norwich City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www.clintoncountygov.com/Departments/Personnel/PersonnelHomePage.htm" mce_href="http://www.clintoncountygov.com/Departments/Personnel/PersonnelHomePage.htm" mce_serialized="2">Clinton County</A>&nbsp;</LI>
<LI mce_serialized="2"><A href="https://sites.google.com/a/columbiacountyny.com/civilservice/" mce_href="https://sites.google.com/a/columbiacountyny.com/civilservice/" mce_serialized="2">Columbia County</A></LI>
<LI mce_serialized="2"><A href="http://www.cortland-co.org/263/Personnel-Civil%20Service" mce_href="http://www.cortland-co.org/263/Personnel-Civil%20Service" mce_serialized="2">Cortland County</A></LI>
<LI mce_serialized="2"><A href="http://www.co.delaware.ny.us/departments/pers/pers.htm" mce_href="http://www.co.delaware.ny.us/departments/pers/pers.htm" mce_serialized="2">Delaware County</A></LI>
<LI mce_serialized="2"><A href="http://www.co.dutchess.ny.us/CountyGov/Departments/Personnel/PSExamAnnouncements.htm" mce_href="http://www.co.dutchess.ny.us/CountyGov/Departments/Personnel/PSExamAnnouncements.htm" mce_serialized="2">Dutchess County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A title="East Fishkill Town" href="http://www.eastfishkillny.org/Government/employment.htm" mce_href="http://www.eastfishkillny.org/Government/employment.htm" mce_serialized="2">East Fishkill Town</A></LI>
<LI mce_serialized="2"><A href="http://cityofpoughkeepsie.com/personnel/" mce_href="http://cityofpoughkeepsie.com/personnel/&#13;&#10;&#9;&#9;" mce_serialized="2">Poughkeepsie City</A></LI>
<LI mce_serialized="2"><A title="Poughkeepsie Town" href="http://www.townofpoughkeepsie.com/human_resources/index.html?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.townofpoughkeepsie.com/human_resources/index.html?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_serialized="2">Poughkeepsie Town</A></LI>
<LI mce_serialized="2"><A title="Wappinger Town" href="http://www.co.dutchess.ny.us/CivilServiceInformationSystem/ApplicantWeb/frmAnnouncementList.aspx?aspxerrorpath=/CivilServiceInformationSystem/ApplicantWeb/frmUserLogin.aspx" mce_href="http://www.co.dutchess.ny.us/CivilServiceInformationSystem/ApplicantWeb/frmAnnouncementList.aspx?aspxerrorpath=/CivilServiceInformationSystem/ApplicantWeb/frmUserLogin.aspx" mce_serialized="2">Wappinger Town</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www.erie.gov/employment/" mce_href="http://www.erie.gov/employment/" mce_serialized="2">Erie County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://www.amherst.ny.us/content/departments.php?dept_id=dept_12&amp;div_id=div_18&amp;menu_id=menu_04" mce_href="http://www.amherst.ny.us/content/departments.php?dept_id=dept_12&amp;div_id=div_18&amp;menu_id=menu_04" mce_serialized="2">Amherst Town</A></LI>
<LI mce_serialized="2"><A href="http://www.ci.buffalo.ny.us/Home/City_Departments/Civil_Service" mce_href="http://www.ci.buffalo.ny.us/Home/City_Departments/Civil_Service" mce_serialized="2">Buffalo City</A></LI>
<LI mce_serialized="2"><A href="http://www.lackawannany.gov/departments/civil-service/" mce_href="http://www.lackawannany.gov/departments/civil-service/" mce_serialized="2">Lackawanna City</A></LI>
<LI mce_serialized="2"><A href="http://www.tonawandacity.com/residents/civil_service.php#.WanWSrKGMnR" mce_href="http://www.tonawandacity.com/residents/civil_service.php#.WanWSrKGMnR" mce_serialized="2">Tonawanda City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www.co.essex.ny.us/jobs.asp" mce_href="http://www.co.essex.ny.us/jobs.asp" mce_serialized="2">Essex County</A></LI>
<LI mce_serialized="2"><A href="http://franklincony.org/content/Departments/View/6:field=services;/content/DepartmentServices/View/48" mce_href="http://franklincony.org/content/Departments/View/6:field=services;/content/DepartmentServices/View/48" mce_serialized="2">Franklin County</A></LI>
<LI mce_serialized="2"><A href="https://www.fultoncountyny.gov/employment-0" mce_href="https://www.fultoncountyny.gov/employment-0" mce_serialized="2">Fulton County</A></LI>
<LI mce_serialized="2"><A href="http://www.co.genesee.ny.us/departments/humanresources/index.html" mce_href="http://www.co.genesee.ny.us/departments/humanresources/index.html" mce_serialized="2">Genesee County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://www.batavianewyork.com/fire-department/pages/employment" mce_href="http://www.batavianewyork.com/fire-department/pages/employment" mce_serialized="2">Batavia City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://greenegovernment.com/departments/human-resources-and-civil-service#civil-service" mce_href="http://greenegovernment.com/departments/human-resources-and-civil-service#civil-service" mce_serialized="2">Greene County</A></LI>
<LI mce_serialized="2"><A href="http://herkimercounty.org/content/Departments/View/9" mce_href="http://herkimercounty.org/content/Departments/View/9" mce_serialized="2">Herkimer County</A></LI>
<LI mce_serialized="2"><A href="http://www.hamiltoncounty.com/government/departments-services#PersonnelDepartment" mce_href="http://www.hamiltoncounty.com/government/departments-services#PersonnelDepartment" mce_serialized="2">Hamilton County</A></LI>
<LI mce_serialized="2"><A href="https://jefferson-portal.mycivilservice.com/" mce_href="https://jefferson-portal.mycivilservice.com/" mce_serialized="2">Jefferson County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="https://www.watertown-ny.gov/index.asp?nid=791" mce_href="https://www.watertown-ny.gov/index.asp?nid=791" mce_serialized="2">Watertown City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www1.nyc.gov/jobs/index.page" mce_href="http://www1.nyc.gov/jobs/index.page" mce_serialized="2">Kings County</A></LI>
<LI mce_serialized="2"><A href="https://www.lewiscounty.org/departments/human-resources/human-resources" mce_href="https://www.lewiscounty.org/departments/human-resources/human-resources" mce_serialized="2">Lewis County</A></LI>
<LI mce_serialized="2"><A href="http://www.co.livingston.state.ny.us/Index.aspx?NID=207" mce_href="http://www.co.livingston.state.ny.us/Index.aspx?NID=207" mce_serialized="2">Livingston County</A></LI>
<LI mce_serialized="2"><A href="https://www.madisoncounty.ny.gov/287/Personnel" mce_href="https://www.madisoncounty.ny.gov/287/Personnel" mce_serialized="2">Madison County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://oneidacity.com/civil-service/" mce_href="http://oneidacity.com/civil-service/" mce_serialized="2">Oneida City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www2.monroecounty.gov/employment-index.php" mce_href="http://www2.monroecounty.gov/employment-index.php" mce_serialized="2">Monroe County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A title="Brighton Town" href="http://www.townofbrighton.org/index.aspx?nid=219&amp;_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.townofbrighton.org/index.aspx?nid=219&amp;_sm_au_=iVV8Z8Lp1WfFsNV6" mce_serialized="2">Brighton Town</A> </LI>
<LI mce_serialized="2"><A href="http://www.townofchili.org/notice-category/job-postings/" mce_href="http://www.townofchili.org/notice-category/job-postings/" mce_serialized="2">Chili Town</A></LI>
<LI mce_serialized="2"><A href="http://www.cityofrochester.gov/article.aspx?id=8589936759" mce_href="http://www.cityofrochester.gov/article.aspx?id=8589936759" mce_serialized="2">Rochester City</A></LI>
<LI mce_serialized="2"><A title="Greece Town" href="http://greeceny.gov/residents/employment-opportunities" mce_href="http://greeceny.gov/residents/employment-opportunities" mce_serialized="2">Greece Town</A> </LI>
<LI mce_serialized="2"><A title="Irondequoit Town" href="http://www.irondequoit.org/town-departments/human-resources/town-employment-opportunities?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.irondequoit.org/town-departments/human-resources/town-employment-opportunities?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_serialized="2">Irondequoit Town</A> </LI>
<LI mce_serialized="2"><A href="http://www.penfield.org/Human_Resources.php" mce_href="http://www.penfield.org/Human_Resources.php" mce_serialized="2">Penfield Town</A> </LI>
<LI mce_serialized="2"><A href="http://www.perinton.org/Departments/finpers/" mce_href="http://www.perinton.org/Departments/finpers/" mce_serialized="2">Perinton Town</A> </LI>
<LI mce_serialized="2"><A title="Pittsford Town" href="http://www.townofpittsford.org/home-hr?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.townofpittsford.org/home-hr?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_serialized="2">Pittsford Town</A></LI>
<LI mce_serialized="2"><A title="Webster Town" href="http://www.ci.webster.ny.us/index.aspx?NID=85&amp;_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.ci.webster.ny.us/index.aspx?NID=85&amp;_sm_au_=iVV8Z8Lp1WfFsNV6" mce_serialized="2">Webster Town</A></LI></UL></LI>
<LI mce_serialized="2"><A href="https://www.co.montgomery.ny.us/sites/public/government/personnel/Personnel_Development/default.aspx" mce_href="https://www.co.montgomery.ny.us/sites/public/government/personnel/Personnel_Development/default.aspx" mce_serialized="2">Montgomery County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="https://www.amsterdamny.gov/government/employment-opportunities" mce_href="https://www.amsterdamny.gov/government/employment-opportunities" mce_serialized="2">Amsterdam City</A></LI>
<LI mce_serialized="2"><A href="http://www.nassaucivilservice.com/NCCSWeb/homepage.nsf/HomePage?ReadForm" mce_href="http://www.nassaucivilservice.com/NCCSWeb/homepage.nsf/HomePage?ReadForm" mce_serialized="2">Nassau County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://www.cityofglencoveny.org/index.htm" mce_href="http://www.cityofglencoveny.org/index.htm" mce_serialized="2">Glen Cove City</A></LI>
<LI mce_serialized="2"><A title="Hempstead Town" href="http://www.townofhempstead.org/civil-service-commission?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.townofhempstead.org/civil-service-commission?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_serialized="2">Hempstead Town</A></LI>
<LI mce_serialized="2"><A href="http://www.nassaucivilservice.com/NCCSWeb/homepage.nsf/HomePage?ReadForm" mce_href="http://www.nassaucivilservice.com/NCCSWeb/homepage.nsf/HomePage?ReadForm" mce_serialized="2">Hempstead Village</A></LI>
<LI mce_serialized="2"><A href="http://www.longbeachny.org/index.asp?Type=B_BASIC&amp;SEC={9C88689C-135F-4293-A9CE-7A50346BEA23}" mce_href="http://www.longbeachny.org/index.asp?Type=B_BASIC&amp;SEC={9C88689C-135F-4293-A9CE-7A50346BEA23}" mce_serialized="2">Long Beach City</A></LI>
<LI mce_serialized="2"><A title="North Hempstead Town" href="http://www.northhempstead.com/Employment-Opportunities" mce_href="http://www.northhempstead.com/Employment-Opportunities" mce_serialized="2">North Hempstead Town</A></LI>
<LI mce_serialized="2"><A title="Oyster Bay Town" href="http://oysterbaytown.com/departments/human-resources/" mce_href="http://oysterbaytown.com/departments/human-resources/" mce_serialized="2">Oyster Bay Town</A></LI>
<LI mce_serialized="2"><A title="Rockville Centre Village" href="http://www.rvcny.us/jobs.html?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.rvcny.us/jobs.html?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_serialized="2">Rockville Centre Village</A></LI>
<LI mce_serialized="2"><A title="Valley Stream Village" href="http://www.vsvny.org/index.asp?Type=B_JOB&amp;SEC=%7b05C716C7-40EE-49EE-B5EE-14EFA9074AB9%7d&amp;_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.vsvny.org/index.asp?Type=B_JOB&amp;SEC=%7b05C716C7-40EE-49EE-B5EE-14EFA9074AB9%7d&amp;_sm_au_=iVV8Z8Lp1WfFsNV6" mce_serialized="2">Valley Stream Village</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www1.nyc.gov/jobs" mce_href="http://www1.nyc.gov/jobs" mce_serialized="2">New York City</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="https://www.cuny.edu/employment/" mce_href="https://www.cuny.edu/employment/" mce_serialized="2">City University of New York (CUNY)</A></LI></UL></LI></UL></LI></UL></DIV>
<DIV class="grid_6 omega" mce_serialized="2">
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://www.niagaracounty.com/Departments/CivilService.aspx" mce_href="http://www.niagaracounty.com/Departments/CivilService.aspx" mce_serialized="2">Niagara County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://niagarafallsusa.org/government/city-departments/human-resources-department/" mce_href="http://niagarafallsusa.org/government/city-departments/human-resources-department/" mce_serialized="2">Niagara Falls City</A></LI>
<LI mce_serialized="2"><A href="http://www.lockportny.gov/residents/city-departments/employment//" mce_href="http://www.lockportny.gov/residents/city-departments/employment//" mce_serialized="2">Lockport City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://ocgov.net/personnel" mce_href="http://ocgov.net/personnel" mce_serialized="2">Oneida County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="https://romenewyork.com/civil-service/" mce_href="https://romenewyork.com/civil-service/" mce_serialized="2">Rome City</A></LI>
<LI mce_serialized="2"><A href="http://www.cityofutica.com/departments/civil-service/index" mce_href="http://www.cityofutica.com/departments/civil-service/index" mce_serialized="2">Utica City</A></LI>
<LI mce_serialized="2"><A href="https://sherrillny.org/city-hall/employment/" mce_href="https://sherrillny.org/city-hall/employment/" mce_serialized="2">Sherrill City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www.ongov.net/employment/civilService.html" mce_href="http://www.ongov.net/employment/civilService.html" mce_serialized="2">Onondaga County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A title="Cicero Town" href="http://www.ongov.net/employment/jurisdiction.html?_sm_au_=iVVrLpv4fvqPNjQj" mce_href="http://www.ongov.net/employment/jurisdiction.html?_sm_au_=iVVrLpv4fvqPNjQj" mce_serialized="2">Cicero Town</A></LI>
<LI mce_serialized="2"><A title="De Witt Town" href="http://www.ongov.net/employment/jurisdiction.html" mce_href="http://www.ongov.net/employment/jurisdiction.html" mce_serialized="2">De Witt Town</A></LI>
<LI mce_serialized="2"><A title="Manlius Town" href="http://www.ongov.net/employment/jurisdiction.html" mce_href="http://www.ongov.net/employment/jurisdiction.html" mce_serialized="2">Manlius Town</A></LI>
<LI mce_serialized="2"><A title="Syracuse City" href="http://www.ongov.net/employment/jurisdiction.html" mce_href="http://www.ongov.net/employment/jurisdiction.html" mce_serialized="2">Syracuse City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www.co.ontario.ny.us/jobs.aspx" mce_href="http://www.co.ontario.ny.us/jobs.aspx" mce_serialized="2">Ontario County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://cityofgenevany.com/available-positions/" mce_href="http://cityofgenevany.com/available-positions/" mce_serialized="2">Geneva City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="https://www.orangecountygov.com/1137/Human-Resources" mce_href="https://www.orangecountygov.com/1137/Human-Resources" mce_serialized="2">Orange County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A title="Middletown City" href="http://www.middletown-ny.com/departments/civil-service.html?_sm_au_=iVVrLpv4fvqPNjQj" mce_href="http://www.middletown-ny.com/departments/civil-service.html?_sm_au_=iVVrLpv4fvqPNjQj" mce_serialized="2">Middletown City</A></LI>
<LI mce_serialized="2"><A href="https://www.monroeny.org/doc-center.html" mce_href="https://www.monroeny.org/doc-center.html" mce_serialized="2">Monroe Town</A></LI>
<LI mce_serialized="2"><A href="http://www.cityofnewburgh-ny.gov/civil-service" mce_href="http://www.cityofnewburgh-ny.gov/civil-service" mce_serialized="2">Newburgh City</A></LI>
<LI mce_serialized="2"><A title="Wallkill Town" href="http://www.townofwallkill.com/index.php/departments/human-resources" mce_href="http://www.townofwallkill.com/index.php/departments/human-resources" mce_serialized="2">Wallkill Town</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www.orleansny.com/Departments/Operations/Personnel.aspx" mce_href="http://www.orleansny.com/Departments/Operations/Personnel.aspx" mce_serialized="2">Orleans County</A></LI>
<LI mce_serialized="2"><A href="https://www.oswegocounty.com/departments/finance_and_personnel/human_resources/exam___employment_information.php" mce_href="https://www.oswegocounty.com/departments/finance_and_personnel/human_resources/exam___employment_information.php" mce_serialized="2">Oswego County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://www.oswegony.org/government/personnel" mce_href="http://www.oswegony.org/government/personnel" mce_serialized="2">Oswego City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="https://www.otsegocounty.com/departments/personnel/index.php" mce_href="https://www.otsegocounty.com/departments/personnel/index.php" mce_serialized="2">Otsego County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://www.oneonta.ny.us/departments/personnel/" mce_href="http://www.oneonta.ny.us/departments/personnel/" mce_serialized="2">Oneonta City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www.putnamcountyny.com/personneldept/" mce_href="http://www.putnamcountyny.com/personneldept/" mce_serialized="2">Putnam County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A title="Carmel Town" href="http://www.putnamcountyny.com/personneldept/exam-postings/" mce_href="http://www.putnamcountyny.com/personneldept/exam-postings/" mce_serialized="2">Carmel Town</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www1.nyc.gov/jobs/index.page" mce_href="http://www1.nyc.gov/jobs/index.page" mce_serialized="2">Queens County</A></LI>
<LI mce_serialized="2"><A href="http://www.rensco.com/county-job-assistance" mce_href="http://www.rensco.com/county-job-assistance" mce_serialized="2">Rensselaer County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://www.troyny.gov/departments/personnel-department/" mce_href="http://www.troyny.gov/departments/personnel-department/" mce_serialized="2">Troy City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www1.nyc.gov/jobs/index.page" mce_href="http://www1.nyc.gov/jobs/index.page" mce_serialized="2">Richmond County</A></LI>
<LI mce_serialized="2"><A href="http://rocklandgov.com/departments/personnel/" mce_href="http://rocklandgov.com/departments/personnel/" mce_serialized="2">Rockland County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://town.clarkstown.ny.us/town_hall/personnel" mce_href="http://town.clarkstown.ny.us/town_hall/personnel" mce_serialized="2">Clarkstown Town</A></LI>
<LI mce_serialized="2"><A href="http://rocklandgov.com/departments/personnel/" mce_href="http://rocklandgov.com/departments/personnel/" mce_serialized="2">Haverstraw Town</A></LI>
<LI mce_serialized="2"><A href="https://www.orangetown.com/groups/department/personnel/" mce_href="https://www.orangetown.com/groups/department/personnel/" mce_serialized="2">Orangetown Town</A></LI>
<LI mce_serialized="2"><A title="Ramapo Town" href="http://www.ramapo.org/page/personnel-30.html?_sm_au_=iVVt78QZ5W7P2qHF" mce_href="http://www.ramapo.org/page/personnel-30.html?_sm_au_=iVVt78QZ5W7P2qHF" mce_serialized="2">Ramapo Town</A></LI>
<LI mce_serialized="2"><A title="Spring Valley Village" href="http://rocklandgov.com/departments/personnel/civil-service-examinations/" mce_href="http://rocklandgov.com/departments/personnel/civil-service-examinations/" mce_serialized="2">Spring Valley Village</A> </LI></UL></LI>
<LI mce_serialized="2"><A title="Saratoga County" href="http://www.saratogacountyny.gov/departments/personnel/" mce_href="http://www.saratogacountyny.gov/departments/personnel/" mce_serialized="2">Saratoga County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://www.cliftonpark.org/services/employment-applications.html" mce_href="http://www.cliftonpark.org/services/employment-applications.html" mce_serialized="2">Clifton Park Town</A></LI>
<LI mce_serialized="2"><A href="http://www.mechanicville.com/index.aspx?nid=563" mce_href="http://www.mechanicville.com/index.aspx?nid=563" mce_serialized="2">Mechanicville</A></LI>
<LI mce_serialized="2"><A href="http://www.saratoga-springs.org/Jobs.aspx" mce_href="http://www.saratoga-springs.org/Jobs.aspx" mce_serialized="2">Saratoga Springs City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="https://mycivilservice.schenectadycounty.com/" mce_href="https://mycivilservice.schenectadycounty.com" mce_serialized="2">Schenectady County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A title="Glenville Town" href="http://www.schenectadycounty.com/FullStory.aspx?m=36&amp;amid=373&amp;_sm_au_=iVVt78QZ5W7P2qHF" mce_href="http://www.schenectadycounty.com/FullStory.aspx?m=36&amp;amid=373&amp;_sm_au_=iVVt78QZ5W7P2qHF" mce_serialized="2">Glenville Town</A></LI>
<LI mce_serialized="2"><A title="Rotterdam Town" href="http://www.schenectadycounty.com/FullStory.aspx?m=36&amp;amid=373" mce_href="http://www.schenectadycounty.com/FullStory.aspx?m=36&amp;amid=373" mce_serialized="2">Rotterdam Town</A></LI>
<LI mce_serialized="2"><A title="Schenectady City" href="http://www.cityofschenectady.com/208/Human-Resources" mce_href="http://www.cityofschenectady.com/208/Human-Resources" mce_serialized="2">Schenectady City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="https://www4.schohariecounty-ny.gov/departments/personnel/" mce_href="https://www4.schohariecounty-ny.gov/departments/personnel/" mce_serialized="2">Schoharie County</A></LI>
<LI mce_serialized="2"><A href="http://www.schuylercounty.us/Index.aspx?NID=119" mce_href="http://www.schuylercounty.us/Index.aspx?NID=119" mce_serialized="2">Schuyler County</A></LI>
<LI mce_serialized="2"><A href="https://seneca-portal.mycivilservice.com/" mce_href="https://seneca-portal.mycivilservice.com/" mce_serialized="2">Seneca County</A></LI>
<LI mce_serialized="2"><A href="http://www.co.st-lawrence.ny.us/Departments/HumanResources/ExaminationSchedule" mce_href="http://www.co.st-lawrence.ny.us/Departments/HumanResources/ExaminationSchedule" mce_serialized="2">St Lawrence County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://www.ogdensburg.org/index.aspx?nid=97" mce_href="http://www.ogdensburg.org/index.aspx?nid=97" mce_serialized="2">Ogdensburg</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www.steubencony.org/Pages.asp?PGID=32" mce_href="http://www.steubencony.org/Pages.asp?PGID=32" mce_serialized="2">Steuben County</A> </LI>
<LI mce_serialized="2"><A href="http://www.suffolkcountyny.gov/departments/civilservice.aspx" mce_href="http://www.suffolkcountyny.gov/departments/civilservice.aspx" mce_serialized="2">Suffolk County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A title="Brookhaven Town" href="http://www.brookhaven.org/Departments/OfficeoftheSupervisor/Personnel.aspx?_sm_au_=iVVt78QZ5W7P2qHF" mce_href="http://www.brookhaven.org/Departments/OfficeoftheSupervisor/Personnel.aspx?_sm_au_=iVVt78QZ5W7P2qHF" mce_serialized="2">Brookhaven Town</A></LI>
<LI mce_serialized="2"><A title="Huntington Town" href="http://www.huntingtonny.gov/content/13753/13757/17478/17508/default.aspx?_sm_au_=iVVt78QZ5W7P2qHF" mce_href="http://www.huntingtonny.gov/content/13753/13757/17478/17508/default.aspx?_sm_au_=iVVt78QZ5W7P2qHF" mce_serialized="2">Huntington Town</A></LI>
<LI mce_serialized="2"><A href="https://islipny.gov/departments/office-of-the-supervisor/personnel?highlight=WyJqb2IiXQ==" mce_href="https://islipny.gov/departments/office-of-the-supervisor/personnel?highlight=WyJqb2IiXQ==" mce_serialized="2">Islip Town</A></LI>
<LI mce_serialized="2"><A title="Lindenhurst Village" href="http://www.suffolkcountyny.gov/Departments/CivilService.aspx" mce_href="http://www.suffolkcountyny.gov/Departments/CivilService.aspx" mce_serialized="2">Lindenhurst Village</A></LI>
<LI mce_serialized="2"><A title="Riverhead Town" href="http://www.townofriverheadny.gov/pview.aspx?id=2481&amp;catID=118&amp;_sm_au_=iVVt78QZ5W7P2qHF" mce_href="http://www.townofriverheadny.gov/pview.aspx?id=2481&amp;catID=118&amp;_sm_au_=iVVt78QZ5W7P2qHF" mce_serialized="2">Riverhead Town</A></LI>
<LI mce_serialized="2"><A title="Smithtown Town" href="http://www.smithtownny.gov/jobs.aspx?_sm_au_=iVVt78QZ5W7P2qHF" mce_href="http://www.smithtownny.gov/jobs.aspx?_sm_au_=iVVt78QZ5W7P2qHF" mce_serialized="2">Smithtown Town</A></LI>
<LI mce_serialized="2"><A title="Southampton Town" href="http://www.southamptontownny.gov/jobs.aspx" mce_href="http://www.southamptontownny.gov/jobs.aspx" mce_serialized="2">Southampton Town</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://sullivanny.us/Departments/Personnel" mce_href="http://sullivanny.us/Departments/Personnel" mce_serialized="2">Sullivan County</A></LI>
<LI mce_serialized="2"><A href="http://www.tiogacountyny.com/departments/personnel-civil-service/" mce_href="http://www.tiogacountyny.com/departments/personnel-civil-service/" mce_serialized="2">Tioga County</A></LI>
<LI mce_serialized="2"><A href="http://tompkinscountyny.gov/personnel" mce_href="http://tompkinscountyny.gov/personnel" mce_serialized="2">Tompkins County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://www.cityofithaca.org/299/Civil-Service-Examinations" mce_href="http://www.cityofithaca.org/299/Civil-Service-Examinations" mce_serialized="2">Ithaca City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www.co.ulster.ny.us/personnel/" mce_href="http://www.co.ulster.ny.us/personnel/" mce_serialized="2">Ulster County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://kingston-ny.gov/Employment" mce_href="http://kingston-ny.gov/Employment" mce_serialized="2">Kingston City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www.warrencountyny.gov/civilservice/exams.php" mce_href="http://www.warrencountyny.gov/civilservice/exams.php" mce_serialized="2">Warren County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A href="http://www.cityofglensfalls.com/index.aspx?NID=55" mce_href="http://www.cityofglensfalls.com/index.aspx?NID=55" mce_serialized="2">Glens Falls City</A></LI></UL></LI>
<LI mce_serialized="2"><A href="http://www.washingtoncountyny.gov/jobs.aspx" mce_href="http://www.washingtoncountyny.gov/jobs.aspx" mce_serialized="2">Washington County</A></LI>
<LI mce_serialized="2"><A href="http://web.co.wayne.ny.us/human-resources/" mce_href="http://web.co.wayne.ny.us/human-resources/" mce_serialized="2">Wayne County</A></LI>
<LI mce_serialized="2"><A href="http://humanresources.westchestergov.com/job-seekers/civil-service-exams" mce_href="http://humanresources.westchestergov.com/job-seekers/civil-service-exams" mce_serialized="2">Westchester County</A> 
<UL mce_serialized="2">
<LI mce_serialized="2"><A title="Cortlandt Town" href="http://www.townofcortlandt.com/Cit-e-Access/webpage.cfm?TID=20&amp;TPID=2522&amp;_sm_au_=iVVt78QZ5W7P2qHF" mce_href="http://www.townofcortlandt.com/Cit-e-Access/webpage.cfm?TID=20&amp;TPID=2522&amp;_sm_au_=iVVt78QZ5W7P2qHF" mce_serialized="2">Cortlandt Town</A> </LI>
<LI mce_serialized="2"><A href="http://www.eastchester.org/departments/comptoller.php" mce_href="http://www.eastchester.org/departments/comptoller.php" mce_serialized="2">Eastchester Town</A></LI>
<LI mce_serialized="2"><A href="https://www.greenburghny.com/477/Employment-Opportunities" mce_href="https://www.greenburghny.com/477/Employment-Opportunities" mce_serialized="2">Greenburgh Town</A></LI>
<LI mce_serialized="2"><A href="http://cmvny.com/departments/civil-service/" mce_href="http://cmvny.com/departments/civil-service/" mce_serialized="2">Mount Vernon City</A></LI>
<LI mce_serialized="2"><A href="http://www.newrochelleny.com/index.aspx?nid=362" mce_href="http://www.newrochelleny.com/index.aspx?nid=362" mce_serialized="2">New Rochelle</A></LI>
<LI mce_serialized="2"><A href="https://www.townofossining.com/cms/human-resources" mce_href="https://www.townofossining.com/cms/human-resources" mce_serialized="2">Ossining Town</A></LI>
<LI mce_serialized="2"><A href="http://www.villageofossining.org/personnel-department" mce_href="http://www.villageofossining.org/personnel-department" mce_serialized="2">Ossining Village</A></LI>
<LI mce_serialized="2"><A title="Port Chester Village" href="http://humanresources.westchestergov.com/job-seekers/civil-service-exams" mce_href="http://humanresources.westchestergov.com/job-seekers/civil-service-exams" mce_serialized="2">Port Chester Village</A></LI>
<LI mce_serialized="2"><A href="http://www.cityofpeekskill.com/human-resources/pages/about-human-resources" mce_href="http://www.cityofpeekskill.com/human-resources/pages/about-human-resources" mce_serialized="2">Peekskill City</A></LI>
<LI mce_serialized="2"><A href="https://www.ryeny.gov/government/personnel/current-job-opportunities" mce_href="https://www.ryeny.gov/government/personnel/current-job-opportunities" mce_serialized="2">Rye City</A></LI>
<LI mce_serialized="2"><A href="http://ny-whiteplains.civicplus.com/index.aspx?nid=98" mce_href="http://ny-whiteplains.civicplus.com/index.aspx?nid=98" mce_serialized="2">White Plains City</A></LI>
<LI mce_serialized="2"><A href="http://www.yonkersny.gov/work/jobs-civil-service-exams" mce_href="http://www.yonkersny.gov/work/jobs-civil-service-exams" mce_serialized="2">Yonkers City</A></LI>
<LI mce_serialized="2"><A href="http://www.yorktownny.org/jobs" mce_href="http://www.yorktownny.org/jobs" mce_serialized="2">Yorktown Town</A> </LI></UL></LI>
<LI mce_serialized="2"><A href="http://www.wyomingco.net/164/Civil-Service" mce_href="http://www.wyomingco.net/164/Civil-Service" mce_serialized="2">Wyoming County</A> 
<UL mce_serialized="2"></UL></LI>
<LI mce_serialized="2"><A href="http://www.yatescounty.org/203/Personnel" mce_href="http://www.yatescounty.org/203/Personnel" mce_serialized="2">Yates County</A> </LI></UL></DIV>

'''



soup = BeautifulSoup(html, 'html5lib')

l = soup.find_all('a')
org_url_list = []
rej = []


# Convert org names to match spreadsheet. eg: "Batavia City" to "City of Batavia"
for i in l:

    # Get org name from anchor tag
    org = i.get_text()
    
    if org.endswith(' City'):
        org = org.replace(' City', '')
        org = 'City of ' + org

    elif org.endswith(' Town'):
        org = org.replace(' Town', '')
        org = 'Town of ' + org

    elif org.endswith(' County'):
        org = org.replace(' County', '')
        org = 'County of ' + org

    elif org.endswith(' Village'):
        org = org.replace(' Village', '')
        org = 'Village of ' + org        

    # Catch org names without anything to convert
    else:
        rej.append(org)
    
    # Get URL from anchor tag
    url = i.get('href')

    # Append results
    org_url_list.append((org, url))



#print('Matches:')
#for i in org_url_list: print(i)


#print('\n\nNo matches at:')
#for i in rej: print(i)


print('\n Searching ...\n\n')


fin_l = []
nm_l = []
mm_l = []


# Open coords file
coords_file = pd.ExcelFile("civ_coords.xlsx")

# Select sheet number
coords_sheet = coords_file.parse()


# Iterate through each org's URL
for html_org in org_url_list:

    url = html_org[1]
    domain = '/'.join(url.split('/')[:3])

    # Iterate through each org's coords
    for i in coords_sheet.index:

        # Find matching org names
        if coords_sheet['Legal Name'][i].lower() == html_org[0].lower():

            # Combine org name, em URL, domain, and coords
            coords = (coords_sheet['GIS Latitude (Y)'][i], coords_sheet['GIS Longitute (X)'][i])
            fin_l.append((coords_sheet['Legal Name'][i], url, domain, coords))
            mm_l.append(url)
            #mm_l.append(coords)
            break ## this should be removed but will ruin the else statement

    # Catch org names with no matches
    else:
        nm_l.append((html_org[0].upper(), html_org[1], domain))



print('\n\n', len(fin_l), 'Matches:')
for i in fin_l: print(str(i) + ',')


print('\n\n', len(nm_l), 'No name matches:')
for i in nm_l: print(str(i) + ',')

print('\n\n Multi URL matches:')
for i in mm_l:
    a = mm_l.count(i)
    if a > 1:
        print('\n\n~~~ dup:', i)
        
        '''
        for ii in fin_l:
            if i in ii: print(ii, i)
        '''

        for ii in fin_l:
            if i == ii[1]:
                print(ii)


















