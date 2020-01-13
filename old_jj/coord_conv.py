# Convert street addresses to coords and place in dict with URL


import geopy.distance
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

bad_l = []
dd = {}


# Get street addrs
f_h = [
('http://www.hufsd.edu', "'huntington, ny 11743', 'huntington station, new york 11746'"),
('http://ccny.cuny.edu/csom', "'new york, ny 10031', 'new york, ny 10031'"),
('http://www.hamburgschools.org', "'hamburg, ny 14075', '5305 abbott rd hamburg, ny 14075', '5305 abbott rd hamburg, ny 14075'"),
('http://www.ticonderogak12.org', "'ticonderoga,ny                        12883'"),
('http://www.delhi.edu', "'delhi, ny 13753'"),
('http://www.lafargevillecsd.org', "'lafargeville, ny 13656'"),
('http://www.slcs.org', "'saranac lake, ny 12983', 'saranac lake, ny 12983'"),
('http://www.gccschool.org', "'rochester, ny 14607'"),
('http://www.frontier.wnyric.org', "'hamburg, ny 14075', '5120 orchard avenue hamburg, ny 14075'"),
('https://sbecacs.org', "'bronx, ny 10455', 'bronx, ny 10455', 'bronx, ny 10455'"),
('http://www.letchworth.k12.ny.us', "'gainesville, ny 14066', '5550 school road gainesville, ny 14066'"),
('http://lcm.touro.edu', "'kew gardens hills, ny 11367', 'kew gardens hills, ny 11367', 'kew gardens hills, ny 11367'"),
('http://www.moriahk12.org', "'port henry, ny 12974'"),
('http://www.gateschili.org', "'rochester ny 14624', 'rochester, ny 14624'"),
('http://www.qcc.cuny.edu', "'bayside, ny 11364'"),
('http://www.hcsk12.org', "'harrisville, ny 13648', 'harrisville, ny 13648', '14371 pirate lane harrisville, ny 13648', '14371 pirate lane harrisville, ny 13648'"),
('http://www.youngwomenscollegeprep.org', "'rochester, ny 14613'"),
('https://www.heuvelton.k12.ny.us', "'heuvelton ny 13654', 'heuvelton, ny 13654'"),
('http://www.genvalley.org', "'belmont, ny 14813', '1 jaguar drive belmont, ny 14813', '1 jaguar drive belmont, ny 14813'"),
('https://www.webutuckschools.org', "'amenia ny 12501', 'amenia, ny 12501'"),
('http://www.nfschools.net', "'niagara falls ny 14304', 'niagara falls, ny 14304'"),
('http://www.starpointcsd.org', "'lockport ny 14094', 'lockport, ny 14094'"),
('https://www.hdcsk12.org', "'de kalb junction, ny 13630', 'kalb road de kalb junction, ny 13630', 'kalb road de kalb junction, ny 13630'"),
('http://www.kipptechvalley.org', "'albany, ny 12210', '830 south pearl street albany, ny 12202'"),
('http://engineering.nyu.edu', "'new york, ny 10003', 'brooklyn, ny 11201', 'brooklyn, ny 11201', 'brooklyn, ny 11201'"),
('http://www.johnstownschools.org', "'johnstown, ny 12095'"),
('https://sites.google.com/a/northvillecsd.org/ncsd', "'northville, ny 12134'"),
('https://www.prattsburghcsd.org', "'prattsburgh, ny 14873', 'one academy street prattsburgh, ny 14873'"),
('http://www.mercy.edu', "'ferry, ny 10522', '145 palisades st dobbs ferry ny 10522'"),
('http://www.yonkerspublicschools.org', "'yonkers ny 10701', 'yonkers, ny 10701'"),
('https://urbanassembly.org', "'new york, ny 10004'"),
('http://www.berkeleycollege.edu/index.htm', "'new york, ny 10017', 'new york, ny 10017', 'new york, ny 10017', 'brooklyn, ny 11201', 'white plains, ny 10601'"),
('http://www.evcsbuffalo.org', "'buffalo, ny 14207', 'buffalo, ny 14201', 'buffalo, ny 14201', 'buffalo, ny 14201', 'buffalo, ny 14207', 'buffalo, ny 14207'"),
('http://www.easthamptonschools.org', "'hampton, new york 11937'"),
('http://www.urbanchoicecharter.org', "'rochester, ny 14610'")
]

for i in f_h:
    list_iter = 3
    print('\n\ni =', i)

    ## use odd numbers for addr list
    i = str(i)
    sp_l = i.split("'")
    u = sp_l[1]

    # Convert to coords
    while True:
        
        # Enter address into geolocator
        try:
            addr = sp_l[list_iter]
            geolocator = Nominatim(user_agent="app_name")
            full_loc = geolocator.geocode(addr)
            coord = full_loc.latitude, full_loc.longitude
            break

        except Exception as errex:

            # Try next address
            if "object has no attribute" in str(errex):
                print('Address not found. Trying another...', errex, addr)
                list_iter += 2

            # If no addresses are usable
            if 'index out of range' in str(errex):
                print('No more addresses to use.', errex, u)
                bad_l.append(addr)
                coord = None
                break
            
            # Catch all other errors
            else:
                print('Unknown error:', errex, addr)
                coord = None
                break


    # Add to dict
    dd[u] = coord
    print(u, coord)



print('\n\nbad_l:', bad_l),
print('\n\ndd :', dd),

'''
mydict = {
    "key1": 1,
    "key2": 2,
    "key3": 3,
}
'''


















