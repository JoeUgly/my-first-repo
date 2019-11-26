
# Desc: Combine URLs and coordinates for every civil service municipality


# URLs' HTML source: https://labor.ny.gov/stats/cslist.shtm
# Coords source: http://eservices.nysed.gov/sedreports/list?id=1
# All Institutions: Active Institutions with GIS coordinates and OITS Accuracy Code - Select by County



import pandas as pd
from bs4 import BeautifulSoup


html = '''
<UL>
<LI><A href="http://www.usajobs.gov/" mce_href="http://www.usajobs.gov/">United States</A></LI>
<LI><A href="http://www.cs.ny.gov/" mce_href="http://www.cs.ny.gov/">New York State</A></LI></UL>
<H4>Local Governments</H4>
<DIV class="grid_6 alpha">
<UL>
<LI><A href="http://www.albanycounty.com/civilservice/" mce_href="http://www.albanycounty.com/civilservice/">Albany County</A> 
<UL>
<LI><A href="http://www.albanyny.org/Government/Departments/HumanResources/Employment/ExamSchedule.aspx" mce_href="http://www.albanyny.org/Government/Departments/HumanResources/Employment/ExamSchedule.aspx">Albany City</A></LI>
<LI><A title="Bethlehem Town" href="http://www.townofbethlehem.org/137/Human-Resources?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.townofbethlehem.org/137/Human-Resources?_sm_au_=iVV8Z8Lp1WfFsNV6">Bethlehem Town</A></LI>
<LI><A href="http://www.cohoes.com/Cit-e-Access/webpage.cfm?TID=34&amp;TPID=6383" mce_href="http://www.cohoes.com/Cit-e-Access/webpage.cfm?TID=34&amp;TPID=6383">Cohoes City</A></LI>
<LI><A href="https://www.colonie.org/departments/civilservice/" mce_href="https://www.colonie.org/departments/civilservice/">Colonie Town</A></LI>
<LI><A title="Guilderland Town" href="http://www.townofguilderland.org/pages/guilderlandny_hr/index?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.townofguilderland.org/pages/guilderlandny_hr/index?_sm_au_=iVV8Z8Lp1WfFsNV6">Guilderland Town</A></LI>
<LI><A href="http://watervliet.com/city/civil-service.htm" mce_href="http://watervliet.com/city/civil-service.htm">Watervliet City</A></LI></UL></LI>
<LI><A href="http://www.alleganyco.com/departments/human-resources-civil-service/" mce_href="http://www.alleganyco.com/departments/human-resources-civil-service/">Allegany County</A></LI>
<LI><A href="http://www1.nyc.gov/jobs/index.page" mce_href="http://www1.nyc.gov/jobs/index.page">Bronx County</A> </LI>
<LI><A href="http://www.gobroomecounty.com/personnel/cs" mce_href="http://www.gobroomecounty.com/personnel/cs">Broome County</A> 
<UL>
<LI><A href="http://www.binghamton-ny.gov/departments/personnel/employment/employment" mce_href="http://www.binghamton-ny.gov/departments/personnel/employment/employment">Binghamton City</A></LI>
<LI><A title="Union Town" href="http://www.townofunion.com/depts_services_human_full.html" mce_href="http://www.townofunion.com/depts_services_human_full.html">Union Town</A></LI>
<LI><A title="Vestal Town" href="http://www.vestalny.com/departments/human_resources/job_opportunities.php" mce_href="http://www.vestalny.com/departments/human_resources/job_opportunities.php">Vestal Town</A></LI></UL></LI>
<LI><A href="http://www.cattco.org/jobs" mce_href="http://www.cattco.org/jobs">Cattaraugus County</A></LI>
<LI><A href="http://www.cayugacounty.us/Community/CivilServiceCommission/ExamAnnouncementsVacancies.aspx" mce_href="http://www.cayugacounty.us/Community/CivilServiceCommission/ExamAnnouncementsVacancies.aspx">Cayuga County</A> 
<UL>
<LI><A href="http://www.auburnny.gov/Public_Documents/AuburnNY_CivilService/index" mce_href="http://www.auburnny.gov/Public_Documents/AuburnNY_CivilService/index">Auburn City</A></LI></UL></LI>
<LI><A href="http://www.co.chautauqua.ny.us/314/Human-Resources" mce_href="http://www.co.chautauqua.ny.us/314/Human-Resources">Chautauqua County</A> 
<UL>
<LI><A href="http://www.co.chautauqua.ny.us/314/Human-Resources" mce_href="http://www.co.chautauqua.ny.us/314/Human-Resources">Jamestown City</A></LI></UL></LI>
<LI><A href="http://www.chemungcountyny.gov/departments/a_-_f_departments/civil_service_personnel/index.php" mce_href="http://www.chemungcountyny.gov/departments/a_-_f_departments/civil_service_personnel/index.php">Chemung County</A> 
<UL>
<LI><A href="http://www.cityofelmira.net/personnel" mce_href="http://www.cityofelmira.net/personnel">Elmira City</A></LI></UL></LI>
<LI><A href="http://www.co.chenango.ny.us/personnel/examinations/" mce_href="http://www.co.chenango.ny.us/personnel/examinations/">Chenango County</A> 
<UL>
<LI><A href="http://www.norwichnewyork.net/human_resources.html" mce_href="http://www.norwichnewyork.net/human_resources.html">Norwich City</A></LI></UL></LI>
<LI><A href="http://www.clintoncountygov.com/Departments/Personnel/PersonnelHomePage.htm" mce_href="http://www.clintoncountygov.com/Departments/Personnel/PersonnelHomePage.htm">Clinton County</A>&nbsp;</LI>
<LI><A href="https://sites.google.com/a/columbiacountyny.com/civilservice/" mce_href="https://sites.google.com/a/columbiacountyny.com/civilservice/">Columbia County</A></LI>
<LI><A href="http://www.cortland-co.org/263/Personnel-Civil%20Service" mce_href="http://www.cortland-co.org/263/Personnel-Civil%20Service">Cortland County</A></LI>
<LI><A href="http://www.co.delaware.ny.us/departments/pers/pers.htm" mce_href="http://www.co.delaware.ny.us/departments/pers/pers.htm">Delaware County</A></LI>
<LI><A href="http://www.co.dutchess.ny.us/CountyGov/Departments/Personnel/PSExamAnnouncements.htm" mce_href="http://www.co.dutchess.ny.us/CountyGov/Departments/Personnel/PSExamAnnouncements.htm">Dutchess County</A> 
<UL>
<LI><A title="East Fishkill Town" href="http://www.eastfishkillny.org/Government/employment.htm" mce_href="http://www.eastfishkillny.org/Government/employment.htm">East Fishkill Town</A></LI>
<LI><A href="http://cityofpoughkeepsie.com/personnel/&#9;&#9;" mce_href="http://cityofpoughkeepsie.com/personnel/&#13;&#10;&#9;&#9;">Poughkeepsie City</A></LI>
<LI><A title="Poughkeepsie Town" href="http://www.townofpoughkeepsie.com/human_resources/index.html?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.townofpoughkeepsie.com/human_resources/index.html?_sm_au_=iVV8Z8Lp1WfFsNV6">Poughkeepsie Town</A></LI>
<LI><A title="Wappinger Town" href="http://www.co.dutchess.ny.us/CivilServiceInformationSystem/ApplicantWeb/frmAnnouncementList.aspx?aspxerrorpath=/CivilServiceInformationSystem/ApplicantWeb/frmUserLogin.aspx" mce_href="http://www.co.dutchess.ny.us/CivilServiceInformationSystem/ApplicantWeb/frmAnnouncementList.aspx?aspxerrorpath=/CivilServiceInformationSystem/ApplicantWeb/frmUserLogin.aspx">Wappinger Town</A></LI></UL></LI>
<LI><A href="http://www.erie.gov/employment/" mce_href="http://www.erie.gov/employment/">Erie County</A> 
<UL>
<LI><A title="Amherst Town" href="http://www.amherst.ny.us/govt/govt_dept.asp?dept_id=dept_12&amp;div_id=div_18&amp;menu_id=menu_04&amp;_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.amherst.ny.us/govt/govt_dept.asp?dept_id=dept_12&amp;div_id=div_18&amp;menu_id=menu_04&amp;_sm_au_=iVV8Z8Lp1WfFsNV6">Amherst Town</A></LI>
<LI><A href="http://www.ci.buffalo.ny.us/Home/City_Departments/Civil_Service" mce_href="http://www.ci.buffalo.ny.us/Home/City_Departments/Civil_Service">Buffalo City</A></LI>
<LI><A href="http://www.lackawannany.gov/departments/civil-service/" mce_href="http://www.lackawannany.gov/departments/civil-service/">Lackawanna City</A></LI>
<LI><A href="http://www.tonawandacity.com/residents/civil_service.php#.WanWSrKGMnR" mce_href="http://www.tonawandacity.com/residents/civil_service.php#.WanWSrKGMnR">Tonawanda City</A></LI></UL></LI>
<LI><A href="http://www.co.essex.ny.us/jobs.asp" mce_href="http://www.co.essex.ny.us/jobs.asp">Essex County</A></LI>
<LI><A href="http://franklincony.org/content/Departments/View/6:field=services;/content/DepartmentServices/View/48" mce_href="http://franklincony.org/content/Departments/View/6:field=services;/content/DepartmentServices/View/48">Franklin County</A></LI>
<LI><A href="http://www.fultoncountyny.gov/node/5" mce_href="http://www.fultoncountyny.gov/node/5">Fulton County</A></LI>
<LI><A href="http://www.co.genesee.ny.us/departments/humanresources/index.html" mce_href="http://www.co.genesee.ny.us/departments/humanresources/index.html">Genesee County</A> 
<UL>
<LI><A href="http://www.batavianewyork.com/fire-department/pages/employment" mce_href="http://www.batavianewyork.com/fire-department/pages/employment">Batavia City</A></LI></UL></LI>
<LI><A href="http://greenegovernment.com/departments/human-resources-and-civil-service#civil-service" mce_href="http://greenegovernment.com/departments/human-resources-and-civil-service#civil-service">Greene County</A></LI>
<LI><A href="http://herkimercounty.org/content/Departments/View/9" mce_href="http://herkimercounty.org/content/Departments/View/9">Herkimer County</A></LI>
<LI><A href="http://www.hamiltoncounty.com/government/departments-services#PersonnelDepartment" mce_href="http://www.hamiltoncounty.com/government/departments-services#PersonnelDepartment">Hamilton County</A></LI>
<LI><A href="http://www.co.jefferson.ny.us/index.aspx?page=83" mce_href="http://www.co.jefferson.ny.us/index.aspx?page=83">Jefferson County</A> 
<UL>
<LI><A href="http://www.citywatertown.org/index.asp?nid=111" mce_href="http://www.citywatertown.org/index.asp?nid=111">Watertown City</A></LI></UL></LI>
<LI><A href="http://www1.nyc.gov/jobs/index.page" mce_href="http://www1.nyc.gov/jobs/index.page">Kings County</A></LI>
<LI><A href="https://www.lewiscounty.org/departments/human-resources/human-resources" mce_href="https://www.lewiscounty.org/departments/human-resources/human-resources">Lewis County</A></LI>
<LI><A href="http://www.co.livingston.state.ny.us/Index.aspx?NID=207" mce_href="http://www.co.livingston.state.ny.us/Index.aspx?NID=207">Livingston County</A></LI>
<LI><A href="https://www.madisoncounty.ny.gov/287/Personnel" mce_href="https://www.madisoncounty.ny.gov/287/Personnel">Madison County</A> 
<UL>
<LI><A href="http://oneidacity.com/civil-service/" mce_href="http://oneidacity.com/civil-service/">Oneida City</A></LI></UL></LI>
<LI><A href="http://www2.monroecounty.gov/employment-index.php" mce_href="http://www2.monroecounty.gov/employment-index.php">Monroe County</A> 
<UL>
<LI><A title="Brighton Town" href="http://www.townofbrighton.org/index.aspx?nid=219&amp;_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.townofbrighton.org/index.aspx?nid=219&amp;_sm_au_=iVV8Z8Lp1WfFsNV6">Brighton Town</A> </LI>
<LI><A href="http://www.townofchili.org/notice-category/job-postings/" mce_href="http://www.townofchili.org/notice-category/job-postings/">Chili Town</A></LI>
<LI><A href="http://www.cityofrochester.gov/article.aspx?id=8589936759" mce_href="http://www.cityofrochester.gov/article.aspx?id=8589936759">Rochester City</A></LI>
<LI><A title="Greece Town" href="http://greeceny.gov/residents/employment-opportunities" mce_href="http://greeceny.gov/residents/employment-opportunities">Greece Town</A> </LI>
<LI><A title="Irondequoit Town" href="http://www.irondequoit.org/town-departments/human-resources/town-employment-opportunities?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.irondequoit.org/town-departments/human-resources/town-employment-opportunities?_sm_au_=iVV8Z8Lp1WfFsNV6">Irondequoit Town</A> </LI>
<LI><A href="http://www.penfield.org/Human_Resources.php" mce_href="http://www.penfield.org/Human_Resources.php">Penfield Town</A> </LI>
<LI><A href="http://www.perinton.org/Departments/finpers/" mce_href="http://www.perinton.org/Departments/finpers/">Perinton Town</A> </LI>
<LI><A title="Pittsford Town" href="http://www.townofpittsford.org/home-hr?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.townofpittsford.org/home-hr?_sm_au_=iVV8Z8Lp1WfFsNV6">Pittsford Town</A></LI>
<LI><A title="Webster Town" href="http://www.ci.webster.ny.us/index.aspx?NID=85&amp;_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.ci.webster.ny.us/index.aspx?NID=85&amp;_sm_au_=iVV8Z8Lp1WfFsNV6">Webster Town</A></LI></UL></LI>
<LI><A href="https://www.co.montgomery.ny.us/sites/public/government/personnel/Personnel_Development/default.aspx" mce_href="https://www.co.montgomery.ny.us/sites/public/government/personnel/Personnel_Development/default.aspx">Montgomery County</A></LI>
<LI><A href="http://www.nassaucivilservice.com/NCCSWeb/homepage.nsf/HomePage?ReadForm" mce_href="http://www.nassaucivilservice.com/NCCSWeb/homepage.nsf/HomePage?ReadForm">Nassau County</A> 
<UL>
<LI><A href="http://www.cityofglencoveny.org/index.htm" mce_href="http://www.cityofglencoveny.org/index.htm">Glen Cove City</A></LI>
<LI><A title="Hempstead Town" href="http://www.townofhempstead.org/civil-service-commission?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.townofhempstead.org/civil-service-commission?_sm_au_=iVV8Z8Lp1WfFsNV6">Hempstead Town</A></LI>
<LI><A href="http://villageofhempstead.org/197/Employment-Opportunities" mce_href="http://villageofhempstead.org/197/Employment-Opportunities">Hempstead Village</A></LI>
<LI><A href="http://www.longbeachny.org/index.asp?Type=B_BASIC&amp;SEC={9C88689C-135F-4293-A9CE-7A50346BEA23}" mce_href="http://www.longbeachny.org/index.asp?Type=B_BASIC&amp;SEC={9C88689C-135F-4293-A9CE-7A50346BEA23}">Long Beach City</A></LI>
<LI><A title="North Hempstead Town" href="http://www.northhempstead.com/Employment-Opportunities" mce_href="http://www.northhempstead.com/Employment-Opportunities">North Hempstead Town</A></LI>
<LI><A title="Oyster Bay Town" href="http://oysterbaytown.com/departments/human-resources/" mce_href="http://oysterbaytown.com/departments/human-resources/">Oyster Bay Town</A></LI>
<LI><A title="Rockville Centre Village" href="http://www.rvcny.us/jobs.html?_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.rvcny.us/jobs.html?_sm_au_=iVV8Z8Lp1WfFsNV6">Rockville Centre Village</A></LI>
<LI><A title="Valley Stream Village" href="http://www.vsvny.org/index.asp?Type=B_JOB&amp;SEC=%7b05C716C7-40EE-49EE-B5EE-14EFA9074AB9%7d&amp;_sm_au_=iVV8Z8Lp1WfFsNV6" mce_href="http://www.vsvny.org/index.asp?Type=B_JOB&amp;SEC=%7b05C716C7-40EE-49EE-B5EE-14EFA9074AB9%7d&amp;_sm_au_=iVV8Z8Lp1WfFsNV6">Valley Stream Village</A></LI></UL></LI>
<LI><A href="http://www1.nyc.gov/jobs" mce_href="http://www1.nyc.gov/jobs">New York City</A> 
<UL>
<LI><A href="http://www.cuny.edu/employment/civil-service.html" mce_href="http://www.cuny.edu/employment/civil-service.html">City University of New York (CUNY)</A></LI></UL></LI></UL></DIV>
<DIV class="grid_6 omega">
<UL>
<LI><A href="http://www.niagaracounty.com/Departments/CivilService.aspx" mce_href="http://www.niagaracounty.com/Departments/CivilService.aspx">Niagara County</A> 
<UL>
<LI><A href="http://niagarafallsusa.org/government/city-departments/human-resources-department/" mce_href="http://niagarafallsusa.org/government/city-departments/human-resources-department/">Niagara Falls City</A></LI>
<LI><A href="http://www.lockportny.gov/residents/city-departments/employment//" mce_href="http://www.lockportny.gov/residents/city-departments/employment//">Lockport City</A></LI></UL></LI>
<LI><A href="http://ocgov.net/personnel" mce_href="http://ocgov.net/personnel">Oneida County</A> 
<UL>
<LI><A href="https://romenewyork.com/civil-service/" mce_href="https://romenewyork.com/civil-service/">Rome City</A></LI>
<LI><A href="http://www.cityofutica.com/departments/civil-service/index" mce_href="http://www.cityofutica.com/departments/civil-service/index">Utica City</A></LI></UL></LI>
<LI><A href="http://www.ongov.net/employment/civilService.html" mce_href="http://www.ongov.net/employment/civilService.html">Onondaga County</A> 
<UL>
<LI><A title="Cicero Town" href="http://www.ongov.net/employment/jurisdiction.html?_sm_au_=iVVrLpv4fvqPNjQj" mce_href="http://www.ongov.net/employment/jurisdiction.html?_sm_au_=iVVrLpv4fvqPNjQj">Cicero Town</A></LI>
<LI><A title="De Witt Town" href="http://www.ongov.net/employment/jurisdiction.html" mce_href="http://www.ongov.net/employment/jurisdiction.html">De Witt Town</A></LI>
<LI><A title="Manlius Town" href="http://www.ongov.net/employment/jurisdiction.html" mce_href="http://www.ongov.net/employment/jurisdiction.html">Manlius Town</A></LI>
<LI><A title="Syracuse City" href="http://www.ongov.net/employment/jurisdiction.html" mce_href="http://www.ongov.net/employment/jurisdiction.html">Syracuse City</A></LI></UL></LI>
<LI><A href="http://www.co.ontario.ny.us/jobs.aspx" mce_href="http://www.co.ontario.ny.us/jobs.aspx">Ontario County</A> 
<UL>
<LI><A href="http://www.co.ontario.ny.us/index.aspx?nid=94" mce_href="http://www.co.ontario.ny.us/index.aspx?nid=94">Geneva City</A></LI></UL></LI>
<LI><A href="https://www.orangecountygov.com/1137/Human-Resources" mce_href="https://www.orangecountygov.com/1137/Human-Resources">Orange County</A> 
<UL>
<LI><A title="Middletown City" href="http://www.middletown-ny.com/departments/civil-service.html?_sm_au_=iVVrLpv4fvqPNjQj" mce_href="http://www.middletown-ny.com/departments/civil-service.html?_sm_au_=iVVrLpv4fvqPNjQj">Middletown City</A></LI>
<LI><A href="http://www.monroeny.org/departments2/human-resources.html" mce_href="http://www.monroeny.org/departments2/human-resources.html">Monroe Town</A></LI>
<LI><A href="http://www.cityofnewburgh-ny.gov/civil-service" mce_href="http://www.cityofnewburgh-ny.gov/civil-service">Newburgh City</A></LI>
<LI><A title="Wallkill Town" href="http://www.townofwallkill.com/index.php/departments/human-resources" mce_href="http://www.townofwallkill.com/index.php/departments/human-resources">Wallkill Town</A></LI></UL></LI>
<LI><A href="http://www.orleansny.com/Departments/Operations/Personnel.aspx" mce_href="http://www.orleansny.com/Departments/Operations/Personnel.aspx">Orleans County</A></LI>
<LI><A href="http://oswegocounty.com/humanresources.shtml" mce_href="http://oswegocounty.com/humanresources.shtml">Oswego County</A> 
<UL>
<LI><A href="http://www.oswegony.org/government/personnel" mce_href="http://www.oswegony.org/government/personnel">Oswego City</A></LI></UL></LI>
<LI><A href="http://www.otsegocounty.com/depts/per/" mce_href="http://www.otsegocounty.com/depts/per/">Otsego County</A> 
<UL>
<LI><A href="http://www.oneonta.ny.us/departments/personnel/" mce_href="http://www.oneonta.ny.us/departments/personnel/">Oneonta City</A></LI></UL></LI>
<LI><A href="http://www.putnamcountyny.com/personneldept/" mce_href="http://www.putnamcountyny.com/personneldept/">Putnam County</A> 
<UL>
<LI><A title="Carmel Town" href="http://www.putnamcountyny.com/personneldept/exam-postings/" mce_href="http://www.putnamcountyny.com/personneldept/exam-postings/">Carmel Town</A></LI></UL></LI>
<LI><A href="http://www1.nyc.gov/jobs/index.page" mce_href="http://www1.nyc.gov/jobs/index.page">Queens County</A></LI>
<LI><A href="http://www.rensco.com/county-job-assistance" mce_href="http://www.rensco.com/county-job-assistance">Rensselaer County</A> 
<UL>
<LI><A href="http://www.troyny.gov/departments/personnel-department/" mce_href="http://www.troyny.gov/departments/personnel-department/">Troy City</A></LI></UL></LI>
<LI><A href="http://www1.nyc.gov/jobs/index.page" mce_href="http://www1.nyc.gov/jobs/index.page">Richmond County</A></LI>
<LI><A href="http://rocklandgov.com/departments/personnel/" mce_href="http://rocklandgov.com/departments/personnel/">Rockland County</A> 
<UL>
<LI><A href="http://town.clarkstown.ny.us/town_hall/personnel" mce_href="http://town.clarkstown.ny.us/town_hall/personnel">Clarkstown Town</A></LI>
<LI><A href="http://rocklandgov.com/departments/personnel/" mce_href="http://rocklandgov.com/departments/personnel/">Haverstraw Town</A></LI>
<LI><A href="https://www.orangetown.com/groups/department/personnel/" mce_href="https://www.orangetown.com/groups/department/personnel/">Orangetown Town</A></LI>
<LI><A title="Ramapo Town" href="http://www.ramapo.org/page/personnel-30.html?_sm_au_=iVVt78QZ5W7P2qHF" mce_href="http://www.ramapo.org/page/personnel-30.html?_sm_au_=iVVt78QZ5W7P2qHF">Ramapo Town</A></LI>
<LI><A title="Spring Valley Village" href="http://rocklandgov.com/departments/personnel/civil-service-examinations/" mce_href="http://rocklandgov.com/departments/personnel/civil-service-examinations/">Spring Valley Village</A> </LI></UL></LI>
<LI><A title="Saratoga County" href="http://www.saratogacountyny.gov/departments/personnel/" mce_href="http://www.saratogacountyny.gov/departments/personnel/">Saratoga County</A> 
<UL>
<LI><A href="http://www.cliftonpark.org/services/employment-applications.html" mce_href="http://www.cliftonpark.org/services/employment-applications.html">Clifton Park Town</A></LI>
<LI><A href="http://www.mechanicville.com/index.aspx?nid=563" mce_href="http://www.mechanicville.com/index.aspx?nid=563">Mechanicville</A></LI>
<LI><A href="http://www.saratoga-springs.org/Jobs.aspx" mce_href="http://www.saratoga-springs.org/Jobs.aspx">Saratoga Springs City</A></LI></UL></LI>
<LI><A href="https://mycivilservice.schenectadycounty.com" mce_href="https://mycivilservice.schenectadycounty.com">Schenectady County</A> 
<UL>
<LI><A title="Glenville Town" href="http://www.schenectadycounty.com/FullStory.aspx?m=36&amp;amid=373&amp;_sm_au_=iVVt78QZ5W7P2qHF" mce_href="http://www.schenectadycounty.com/FullStory.aspx?m=36&amp;amid=373&amp;_sm_au_=iVVt78QZ5W7P2qHF">Glenville Town</A></LI>
<LI><A title="Rotterdam Town" href="http://www.schenectadycounty.com/FullStory.aspx?m=36&amp;amid=373" mce_href="http://www.schenectadycounty.com/FullStory.aspx?m=36&amp;amid=373">Rotterdam Town</A></LI>
<LI><A title="Schenectady City" href="http://www.cityofschenectady.com/208/Human-Resources" mce_href="http://www.cityofschenectady.com/208/Human-Resources">Schenectady City</A></LI></UL></LI>
<LI><A href="http://www.schohariecounty-ny.gov/CountyWebSite/Personnel/CivilServiceServices.html" mce_href="http://www.schohariecounty-ny.gov/CountyWebSite/Personnel/CivilServiceServices.html">Schoharie County</A></LI>
<LI><A href="http://www.schuylercounty.us/Index.aspx?NID=119" mce_href="http://www.schuylercounty.us/Index.aspx?NID=119">Schuyler County</A></LI>
<LI><A href="https://seneca-portal.mycivilservice.com/" mce_href="https://seneca-portal.mycivilservice.com/">Seneca County</A></LI>
<LI><A href="http://www.co.st-lawrence.ny.us/Departments/HumanResources/ExaminationSchedule" mce_href="http://www.co.st-lawrence.ny.us/Departments/HumanResources/ExaminationSchedule">St Lawrence County</A> 
<UL>
<LI><A href="http://www.ogdensburg.org/index.aspx?nid=97" mce_href="http://www.ogdensburg.org/index.aspx?nid=97">Ogdensburg</A></LI></UL></LI>
<LI><A href="http://www.steubencony.org/Pages.asp?PGID=32" mce_href="http://www.steubencony.org/Pages.asp?PGID=32">Steuben County</A> </LI>
<LI><A href="http://www.suffolkcountyny.gov/departments/civilservice.aspx" mce_href="http://www.suffolkcountyny.gov/departments/civilservice.aspx">Suffolk County</A> 
<UL>
<LI><A title="Brookhaven Town" href="http://www.brookhaven.org/Departments/OfficeoftheSupervisor/Personnel.aspx?_sm_au_=iVVt78QZ5W7P2qHF" mce_href="http://www.brookhaven.org/Departments/OfficeoftheSupervisor/Personnel.aspx?_sm_au_=iVVt78QZ5W7P2qHF">Brookhaven Town</A></LI>
<LI><A title="Huntington Town" href="http://www.huntingtonny.gov/content/13753/13757/17478/17508/default.aspx?_sm_au_=iVVt78QZ5W7P2qHF" mce_href="http://www.huntingtonny.gov/content/13753/13757/17478/17508/default.aspx?_sm_au_=iVVt78QZ5W7P2qHF">Huntington Town</A></LI>
<LI><A title="Islip Town" href="http://isliptown-ny.gov/index.php/i-want-to/apply-for/employment-with-the-town?_sm_au_=iVVt78QZ5W7P2qHF" mce_href="http://isliptown-ny.gov/index.php/i-want-to/apply-for/employment-with-the-town?_sm_au_=iVVt78QZ5W7P2qHF">Islip Town</A></LI>
<LI><A title="Lindenhurst Village" href="http://www.suffolkcountyny.gov/Departments/CivilService.aspx" mce_href="http://www.suffolkcountyny.gov/Departments/CivilService.aspx">Lindenhurst Village</A></LI>
<LI><A title="Riverhead Town" href="http://www.townofriverheadny.gov/pview.aspx?id=2481&amp;catID=118&amp;_sm_au_=iVVt78QZ5W7P2qHF" mce_href="http://www.townofriverheadny.gov/pview.aspx?id=2481&amp;catID=118&amp;_sm_au_=iVVt78QZ5W7P2qHF">Riverhead Town</A></LI>
<LI><A title="Smithtown Town" href="http://www.smithtownny.gov/jobs.aspx?_sm_au_=iVVt78QZ5W7P2qHF" mce_href="http://www.smithtownny.gov/jobs.aspx?_sm_au_=iVVt78QZ5W7P2qHF">Smithtown Town</A></LI>
<LI><A title="Southampton Town" href="http://www.southamptontownny.gov/jobs.aspx" mce_href="http://www.southamptontownny.gov/jobs.aspx">Southampton Town</A></LI></UL></LI>
<LI><A href="http://co.sullivan.ny.us/Departments/DepartmentsNZ/Personnel/CivilServiceExams/tabid/3382/Default.aspx" mce_href="http://co.sullivan.ny.us/Departments/DepartmentsNZ/Personnel/CivilServiceExams/tabid/3382/Default.aspx">Sullivan County</A></LI>
<LI><A href="http://www.tiogacountyny.com/departments/personnel-civil-service/" mce_href="http://www.tiogacountyny.com/departments/personnel-civil-service/">Tioga County</A></LI>
<LI><A href="http://tompkinscountyny.gov/personnel" mce_href="http://tompkinscountyny.gov/personnel">Tompkins County</A> 
<UL>
<LI><A href="http://www.cityofithaca.org/299/Civil-Service-Examinations" mce_href="http://www.cityofithaca.org/299/Civil-Service-Examinations">Ithaca City</A></LI></UL></LI>
<LI><A href="http://www.co.ulster.ny.us/personnel/" mce_href="http://www.co.ulster.ny.us/personnel/">Ulster County</A> 
<UL>
<LI><A href="http://kingston-ny.gov/Employment" mce_href="http://kingston-ny.gov/Employment">Kingston City</A></LI></UL></LI>
<LI><A href="http://www.warrencountyny.gov/civilservice/exams.php" mce_href="http://www.warrencountyny.gov/civilservice/exams.php">Warren County</A> 
<UL>
<LI><A href="http://www.cityofglensfalls.com/index.aspx?NID=55" mce_href="http://www.cityofglensfalls.com/index.aspx?NID=55">Glens Falls City</A></LI></UL></LI>
<LI><A href="http://www.washingtoncountyny.gov/jobs.aspx" mce_href="http://www.washingtoncountyny.gov/jobs.aspx">Washington County</A></LI>
<LI><A href="http://web.co.wayne.ny.us/human-resources/" mce_href="http://web.co.wayne.ny.us/human-resources/">Wayne County</A></LI>
<LI><A href="http://humanresources.westchestergov.com/job-seekers/civil-service-exams" mce_href="http://humanresources.westchestergov.com/job-seekers/civil-service-exams">Westchester County</A> 
<UL>
<LI><A title="Cortlandt Town" href="http://www.townofcortlandt.com/Cit-e-Access/webpage.cfm?TID=20&amp;TPID=2522&amp;_sm_au_=iVVt78QZ5W7P2qHF" mce_href="http://www.townofcortlandt.com/Cit-e-Access/webpage.cfm?TID=20&amp;TPID=2522&amp;_sm_au_=iVVt78QZ5W7P2qHF">Cortlandt Town</A> </LI>
<LI><A href="http://www.eastchester.org/departments/comptoller.php" mce_href="http://www.eastchester.org/departments/comptoller.php">Eastchester Town</A></LI>
<LI><A title="Greenburgh Town" href="http://www.greenburghny.com/Cit-e-Access/webpage.cfm?TID=10&amp;TPID=2491&amp;_sm_au_=iVVt78QZ5W7P2qHF" mce_href="http://www.greenburghny.com/Cit-e-Access/webpage.cfm?TID=10&amp;TPID=2491&amp;_sm_au_=iVVt78QZ5W7P2qHF">Greenburgh Town</A></LI>
<LI><A href="http://cmvny.com/departments/civil-service/" mce_href="http://cmvny.com/departments/civil-service/">Mount Vernon City</A></LI>
<LI><A href="http://www.newrochelleny.com/index.aspx?nid=362" mce_href="http://www.newrochelleny.com/index.aspx?nid=362">New Rochelle</A></LI>
<LI><A title="Ossining Town" href="http://www.townofossining.com/cms/resources/human-resources" mce_href="http://www.townofossining.com/cms/resources/human-resources">Ossining Town</A></LI>
<LI><A href="http://www.villageofossining.org/personnel-department" mce_href="http://www.villageofossining.org/personnel-department">Ossining Village</A></LI>
<LI><A title="Port Chester Village" href="http://humanresources.westchestergov.com/job-seekers/civil-service-exams" mce_href="http://humanresources.westchestergov.com/job-seekers/civil-service-exams">Port Chester Village</A></LI>
<LI><A href="http://www.cityofpeekskill.com/human-resources/pages/about-human-resources" mce_href="http://www.cityofpeekskill.com/human-resources/pages/about-human-resources">Peekskill City</A></LI>
<LI><A href="http://www.ryeny.gov/human-resources.cfm" mce_href="http://www.ryeny.gov/human-resources.cfm">Rye City</A></LI>
<LI><A href="http://ny-whiteplains.civicplus.com/index.aspx?nid=98" mce_href="http://ny-whiteplains.civicplus.com/index.aspx?nid=98">White Plains City</A></LI>
<LI><A href="http://www.yonkersny.gov/work/jobs-civil-service-exams" mce_href="http://www.yonkersny.gov/work/jobs-civil-service-exams">Yonkers City</A></LI>
<LI><A href="http://www.yorktownny.org/jobs" mce_href="http://www.yorktownny.org/jobs">Yorktown Town</A> </LI></UL></LI>
<LI><A href="http://www.wyomingco.net/164/Civil-Service" mce_href="http://www.wyomingco.net/164/Civil-Service">Wyoming County</A> 
<UL></UL></LI>
<LI><A href="http://www.yatescounty.org/203/Personnel" mce_href="http://www.yatescounty.org/203/Personnel">Yates County</A> </LI></UL></DIV>
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


# Open coords file
coords_file = pd.ExcelFile("C:/Users/jschiffler/Desktop/civ_coords.xlsx")

# Select sheet number
coords_sheet = coords_file.parse()


# Iterate through each org's URL
for html_org in org_url_list:

    # Iterate through each org's coords
    for i in coords_sheet.index:

        # Find matching org names
        if coords_sheet['Legal Name'][i].lower() == html_org[0].lower():

            # Combine org name, URL, and coords
            coords = (coords_sheet['GIS Latitude (Y)'][i], coords_sheet['GIS Longitute (X)'][i])
            fin_l.append((coords_sheet['Legal Name'][i], html_org[1], coords))
            break

    # Catch org names with no matches
    else:
        nm_l.append(html_org)





print('\n\nMatches:')
for i in fin_l: print(i)


print('\n\nNo matches at:')
for i in nm_l: print(i)

























