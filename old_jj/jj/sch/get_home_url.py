
# Desc: Use Google search api to get home url

# Use output from get_org_name_civ.py


from googlesearch import search


old = [
['Sagaponack Common School District', 'http://www.sagaponackschool.com/', 'http://www.sagaponackschool.com'],
['Salamanca City School District', 'http://www.salamancany.org', 'salamancany.org'],
['Salem Central School District', 'http://www.salemcsd.org/', 'salemcsd.org/'],
['Salmon River Central School District', 'http://www.srk12.org/', 'srk12.org/'],
['Sandy Creek Central School District', 'http://www.sccs.cnyric.org/'],
['Saranac Central School District', 'http://www.saranac.org', 'saranac.org'],
['Saugerties Central School District', 'http://saugerties.schoolwires.com/', 'saugerties.schoolwires.com/'],
['Sayville Union Free School District', 'http://www.sayville.k12.ny.us/'],
['Schalmont Central School District', 'http://www.schalmont.org/', 'schalmont.org/'],
['Schenectady City School District', 'http://www.schenectady.k12.ny.us/', 'schenectady.k12.ny.us/'],
['Schenevus Central School District', 'https://www.schenevuscsd.org/', 'https://www.schenevuscsd.org/EmploymentOpportunities.aspx'],
['Schoharie Central School District', 'http://www.schoharie.k12.ny.us/', 'http://www.schoharie.k12.ny.us'],
['Scotia-Glenville Central School District', 'http://www.sgcsd.neric.org/'],
['Shelter Island Union Free School District', 'http://sischool.dev6.hamptons.com/'],
['Sherman Central School District', 'http://shermancsd.org/', 'http://shermancsd.org/employment/'],
['Silver Creek Central School District', 'http://www.silvercreek.wnyric.org'],
['Somers Central School District', 'http://https://www.edline.net/pages/Somers_CSD'],
['South Huntington Union Free School District', 'http://www.shuntington.k12.ny.us/'],
['South Orangetown Central School District', 'http://www.socsd.k12.ny.us/'],
['Southern Cayuga Central School District', 'http://www.southerncayuga.org', 'http://www.southerncayuga.org'],
['Southold Union Free School District', 'http://www.southoldufsd.net/'],
['Spencer-Van Etten Central School District', 'http://www.svecsd.org/', 'svecsd.org/'],
['Springs Union Free School District', 'http://www.springs.k12.ny.us/'],
['St Johnsville Central School District', 'http://sjcsd.org/'],
['St Regis Falls Central School District', 'http://stregisfallscsd.org/', 'stregisfallscsd.org/'],
['Staten Island Schools - NYC District #31', '_ERROR._url_not_found'],
['Stillwater Central School District', 'http://www.scsd.org/', 'http://romuluscsd.org/employment_opportunities', 'http://www.bscsd.org/Page/559', 'http://www.hoosickfallscsd.org', 'http://www.iroquoiscsd.org/domain/12', 'http://www.lyonscsd.org/Page/1374', 'http://www.mtmorriscsd.org', 'http://www.naplescsd.org/districtpage.cfm?pageid=550', 'http://www.nscsd.org', 'http://www.plattscsd.org/district/human-resources/employment-opportunities', 'http://www.schenevuscsd.org/EmploymentOpportunities.aspx', 'http://www.unionspringscsd.org/districtpage.cfm?pageid=193', 'http://www.wellscsd.org/district-information/employment-opportunities', 'https://www.rcscsd.org/about-us/employment', 'https://www.scsd.org/employment', 'https://www.stregiscsd.org/faculty-staff'],
['Stockbridge Valley Central School District', 'http://www.stockbridgevalley.org/', 'http://www.stockbridgevalley.org'],
['Sullivan West Central School District', 'http://www.swcsd.org/', 'http://www.swcsd.org/Page/194', 'http://www.wcsd.org/district/employment_opportunities', 'swcsd.org/', 'wcsd.org/'],
['Sweet Home Central School District', 'http://www.shs.k12.ny.us/'],
['Thousand Islands Central School District', 'http://www.1000islandsschools.org', 'http://www.1000islandsschools.org'],
['Tioga Central School District', 'http://www.tcsaa.org/'],
['Tri-Valley Central School District', 'http://tvcs.k12.ny.us/'],
['Troy City School District', 'http://www.troy.k12.ny.us/'],
['Trumansburg Central School District', 'http://www.tburg.k12.ny.us/'],
['Tuckahoe Common School District', 'http://www.tuckahoe.k12.ny.us/'],
['Tupper Lake Central School District', 'http://www.tupperlakecsd.net/', 'tupperlakecsd.net/'],
['Tuxedo Union Free School District', 'http://www.tuxedoufsd.org/', 'http://www.tuxedoufsd.org/district_services/business_office/employment_opportunities'],
['Union Springs Central School District', 'http://www.unionspringscsd.org/', 'http://www.unionspringscsd.org/districtpage.cfm?pageid=193'],
['Union-Endicott Central School District', 'https://www.uek12.org/', 'https://www.uek12.org/Employment.aspx'],
['Valhalla Union Free School', 'http://www.valhalla.k12.ny.us/'],
['Valley Central School District', 'http://www.vcsd.k12.ny.us/valleycentralsd/site/default.asp'],
['Van Hornesville-Owen D. Young Central School District', '_ERROR._url_not_found'],
['Vestal Central School District', 'http://www.vestal.k12.ny.us', 'vestal.k12.ny.us'],
['Voorheesville Central School District', 'http://vcsdk12.org/'],
['Wainscott Common School District', 'http://www.wainscottschool.com/'],
['Walton Central School District', 'http://www.waltoncsd.stier.org'],
['Wantagh Union Free School District', 'http://www.wms.wantaghufsd.k12.ny.us/'],
['Wappingers Central School District', '_ERROR._url_not_found'],
['Warrensburg Central School District', 'http://www.wcsd.org/', 'wcsd.org/'],
['Waterford-Halfmoon Union Free School District', 'http://www.whufsd.org', 'http://www.whufsd.org'],
['Waterville Central School District', 'http://www.watervilleschools.org/'],
['Watervliet City School District', 'http://www.watervlietcityschools.org/', 'https://www.watervlietcityschools.org/employment'],
['Watkins Glen Central School District', 'http://www.watkinsglenschools.com/'],
['Wayland-Cohocton Central School District', 'http://www.wccsk12.org/', 'wccsk12.org/'],
['Wayne Central School District', 'http://wayne.k12.ny.us/', 'wayne.k12.ny.us/'],
['Webster Central School District', 'http://www.websterschools.org', 'websterschools.org'],
['Weedsport Central School District', 'http://www.weedsport.org', 'weedsport.org'],
['Wells Central School District', 'http://www.wellscsd.com/main/'],
['West Babylon Union Free School District', 'http://www.westbabylon.k12.ny.us/'],
['West Irondequoit Central School District', 'http://www.westirondequoit.org/'],
['West Park Union Free School District', '_ERROR._url_not_found'],
['Westbury Union Free School District', 'http://www.westburyschools.org/', 'http://www.westburyschools.org'],
['Wheelerville Union Free School District', 'http://www.wufselementary.k12.ny.us/'],
['White Plains City School District', 'https://www.whiteplainspublicschools.org/', 'https://www.whiteplainspublicschools.org/Page/546'],
['Wyoming Central School District', 'http://www.wyoming.k12.ny.us/'],
['Yorkshire-Pioneer Central School District', 'http://www.pioneerschools.org', 'http://www.erschools.org/departments/employment/employment_opportunities', 'http://www.pioneerschools.org/domain/48', 'pioneerschools.org'],
['Yorktown Central School District', 'http://www.yorktowncsd.org/']
]






for i in old:

    if len(i) > 2 or i[1].startswith('_'):
        continue


    string = i[0] + ' ny -wikipedia.org -hometownlocator.com'

    for url in search(string, stop=1, num=1, pause=2):

        i.insert(1, url)
        print(i)



print('\n\n\n', old)



























