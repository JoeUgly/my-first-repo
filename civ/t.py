
l = [
['Town of Dickinson (Franklin)', '', '', (44.7530589529, -74.5544829860)],


['Town of Ashland (Greene)', '', 'http://www.ashlandny.com', (42.3044207353, -74.3351915512)],


['Town of Clinton (Dutchess)', '', 'http://www.townofclinton.com', (41.8838681183, -73.8044847804)],


['Town of Franklin (Franklin)', '', 'http://www.townoffranklin.com', (44.4516549273, -74.0650046172)],


['Town of Clinton (Clinton)', '', '', (44.9558861473, -73.9282292229)],


['Town of Lewis (Essex)', '', 'http://www.lewisny.com', (44.2761210406, -73.5626885381)],


['Town of Brighton (Franklin)', '', 'http://townofbrighton.net', (44.4763099718, -74.3058500443)],


['Town of Dickinson (Broome)', '', 'http://www.townofdickinson.com', (42.1192815531, -75.9109978392)],


['Town of Franklin (Delaware)', '', '', (42.3694350548, -75.1827050963)],


['Town of Ashland (Chemung)', '', 'http://www.townofashland.net', (42.0220900548, -76.7656799332)],


['Town of Greenville (Greene)', '', 'http://www.townofgreenvilleny.com', (42.4542350944, -74.0298050163)],


['Town of Lewis (Lewis)', '', '', (43.4516558983, -75.4941888361)],


['Town of Brighton (Monroe)', 'http://www.townofbrighton.org/index.aspx?nid=219&amp;_sm_au_=ivv8z8lp1wffsnv6', 'http://www.townofbrighton.org', (43.1266919957, -77.5761677750)],


['Town of Chester (Warren)', '', 'http://www.townofchesterny.org', (43.6283749555, -73.8192950163)],


['Town of Greenville (Orange)', '', 'https://www.greenvilleny.org/', (41.3616362157, -74.6165556692)],


['Town of Albion (Orleans)', '', 'http://www.townofalbion.com', (43.2386624955, -78.1780398160)],


['Town of Albion (Oswego)', '', 'http://www.townofalbion-ny.us', (43.4961649896, -75.9703999462)],


['Town of Fremont (Sullivan)', '', 'http://www.fremontnewyork.us', (41.8451700043, -75.0099750662)],


['Town of Fremont (Steuben)', '', 'https://www.townoffremontny.com/', (42.3944973631, -77.6270583018)],


['Town of Chester (Orange)', '', 'http://thetownofchester.org', (41.3398490744, -74.2755453151)],
]






for i in l:
    orig = i[0].split(' (')[0]
    county = i[0].split(' (')[1].strip(')')

    i[0] = orig
    i.append(county)
    print('\n' + str(i) + ',')




















