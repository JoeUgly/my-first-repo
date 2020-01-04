

# Desc: Merge output from em_finder into main db


# To do:
# if duplicate homepages exists, then use duplicate em URL



# Overwrite this list with new enties after you update the db list below
# This list doesn't need to contain all entries
e_l = [




]


# Overwrite this list with output from this program after supplying new entries above
# This list must contain all entries
db = [
['Borough of Manhattan Comm College', 'https://www.bmcc.cuny.edu/hr/jobs-2/', 'http://www.bmcc.cuny.edu/j2ee/index.jsp', (40.7172404578, -74.0121790072)],
['Bronx Community College', '_cuny', 'http://www.bcc.cuny.edu/', (40.8571748658, -73.9097961945)],
['City University of New York Brooklyn College', '_cuny', 'http://www.brooklyn.cuny.edu', (40.6316289309, -73.9528670048)],
['City University of New York Central Administration', '', 'http://www.cuny.edu', (40.7506640729, -73.9737941049)],
['City University of New York College of Staten Island', 'http://www.csi.cuny.edu/faculty-staff/human-resources/recruitment/jobs-csi', 'http://www.csi.cuny.edu', (40.6080474954, -74.1532403516)],
['City University of New York Herbert H. Lehman College', '_cuny', 'http://www.lehman.cuny.edu', (40.8744790403, -73.8916151123)],
['City University of New York John Jay College of Criminal Justice', 'http://www.jjay.cuny.edu/employment-opportunities', 'http://www.jjay.cuny.edu', (40.7701641615, -73.9880095816)],
['CUNY Bernard M. Baruch College', 'https://www.baruch.cuny.edu/hr/jobs/', 'http://www.baruch.cuny.edu', (40.7391335672, -73.9848434121)],
['CUNY City College', 'https://www.ccny.cuny.edu/hr', 'http://www.ccny.cuny.edu', (40.8196114231, -73.9506187115)],
['CUNY Graduate School And University Center', 'https://www.gc.cuny.edu/About-the-GC/Administrative-Services/Human-Resources/Employment-Opportunities', 'http://www.gc.cuny.edu', (40.6712788451, -73.9843543293)],
['CUNY Hunter College', 'http://www.hunter.cuny.edu/hr/Employment/Jobs%20Page', 'http://www.hunter.cuny.edu/', (40.7687286586, -73.9651801586)],
['CUNY Law School at Queens', 'https://www.law.cuny.edu/human-resources/', 'http://www.law.cuny.edu', (40.7363855707, -73.8249758017)],
['CUNY NYC College of Technology', '', 'http://www.citytech.cuny.edu', (40.6952706095, -73.9873058902)],
['CUNY Queens College', '_cuny', 'http://www.qc.cuny.edu', (40.7286450477, -73.8152910843)],
['CUNY School of Professional Studies', 'https://sps.cuny.edu/about/directory/office-faculty-and-staff-resources/jobs', 'http://', (40.74835575, -73.99002523)],
['CUNY Stella And Charles Guttman Community College', '', 'http://www.guttman.cuny.edu/index.html', (40.7529398926, -73.9839704481)],
['CUNY York College', '_cuny', 'http://www.york.cuny.edu/', (40.7015558773, -73.7964298467)],
['Eugenio Maria De Hostos Comm College', 'http://www.hostos.cuny.edu/Administrative-Offices/Office-of-Human-Resources/Career-Opportunities/Hostos', 'http://www.hostos.cuny.edu/', (40.8180441895, -73.9278054492)],
['Fiorello H. La Guardia Comm College', 'https://www.laguardia.edu/employment/', 'http://www.lagcc.cuny.edu/', (40.7448797176, -73.9352029079)],
['Kingsborough Community College', 'http://www.kbcc.cuny.edu/humanresources/kccjoblistings.html', 'http://www.kbcc.cuny.edu', (40.5778062737, -73.9355594261)],
['Medgar Evers College', 'https://ares.mec.cuny.edu/human-resources/', 'http://www.mec.cuny.edu', (40.6660717819, -73.9569882032)],
['Queensborough Community College', 'http://www.qcc.cuny.edu/employment/index.html', 'http://www.qcc.cuny.edu', (40.7525132363, -73.7594240874)],




]




# Use this when supplying only the home URL and em URL
'''
for ii in db:

    for i in e_l:

        # Find matching homepages from em_finder output and incomplete db
        if ii[2] in i[0]:

            # Fill in em_url and homepage into db
            ii[1] = i[1]
            ii[2] = i[0]
    
    # Display org name and full entry
    if not ii[1].strip():
        count += 1
        print('\n', ii[0])
        print(ii)
'''




count = 0

# Use this when supplying the full entry. ie: [org name, em url, home url, (coords)],
for ii in db:

    for i in e_l:

        # Find matching org names from em_finder output and incomplete db
        if ii[0] == i[0]:

                # Replace incomplete db entry with new entry
                ii = i


    # Display applitrack URLs
    #if ii[1] == '_AP':
        #print(ii)
    
    
    # Display entries with missing em URL
    if not ii[1].strip():
        count += 1
        #print('\n', ii[0])
        #print('\n' + str(ii) + ',')


    # Display entries with missing coords
    if ii[3] == (0.0, 0.0):
        count += 1
        #print('\n' + str(ii) + ',')


    # Display all entries
    print(str(ii) + ',')
    


print('\nMissing:', count, '\nTotal entries:', len(db))













