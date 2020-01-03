

# Desc: Merge output from em_finder into main db


# To do:




# Overwrite this list with new enties after you update the db list below
# This list doesn't need to contain all entries
e_l = [




]


# Overwrite this list with output from this program after supplying new entries above
# This list must contain all entries
db = [

['Art Institute of New York City', '', 'http://www.artinstitutes.edu', (40.7549303706, -73.988503444)],

['Asa College, Inc.', '', 'http://www.asa.edu', (40.6922729032, -73.9860830633)],

['Berkeley College - Main Campus', 'http://www.berkeleycollege.edu/index.htm', 'http://www.berkeleycollege.edu', (40.7538847351, -73.9795071152)],

['Berkeley College - Westchester', 'http://www.berkeleycollege.edu/index.htm', 'http://www.berkeleycollege.edu', (41.0346335886, -73.7679309244)],

['Bryant & Stratton Business College - North Syracuse', '', 'http://www.bryantstratton.edu', (43.1891227204, -76.2390537897)],

['Bryant & Stratton College - Albany', '', 'http://www.bryantstratton.edu', (42.6981365193, -73.8099631495)],

['Bryant & Stratton College - Buffalo', '', 'http://www.bryantstratton.edu', (42.8865731643, -78.8735239766)],

['Bryant & Stratton College - Greece', '', 'http://www.bryantstratton.edu', (43.2406605054, -77.6960945905)],

['Bryant & Stratton College - Henrietta', '', 'http://www.bryantstratton.edu', (43.0855524211, -77.6024060802)],

['Bryant & Stratton College - Southtowns Campus', '', 'http://www.bryantstratton.edu', (42.7906774624, -78.7672821844)],

['Bryant & Stratton College- Amherst', '', 'http://www.bryantstratton.edu', (43.0408165743, -78.7428249282)],

['Bryant Stratton College - Syracuse', '', 'http://www.bryantstratton.edu', (43.0590713535, -76.137047667)],

["Christie's Education, Inc", '', 'http://www.christies.edu', (40.7589337089, -73.9808982956)],

['The College of Westchester', '', 'http://www.cw.edu', (41.0336489614, -73.7843757839)],


['Devry College of New York', '', 'https://www.devry.edu/', (40.7474651252, -73.9833739393)],

['Elmira Business Inst', '', 'http://www.ebi.edu', (42.0901041677, -76.8091666394)],

['Elmira Business Institute - Vestal Executive Park', '', 'http://www.ebi.edu', (42.0970600729, -75.9754069723)],

['Five Towns College', 'https://www.ftc.edu/employment', 'http://www.ftc.edu', (40.7909330678, -73.3673848429)],

['Globe Inst of Tech Inc', '', 'http://www.globe.edu/', (40.7531259805, -73.9892959517)],

['Island Drafting & Tech Inst', '', 'http://www.idti.edu', (40.6756418059, -73.4169787759)],

['Jamestown Business College', '', 'http://www.jbcny.edu', (42.0955017298, -79.24973674660001)],

['Laboratory Inst of Merchandising', 'https://www.limcollege.edu/about-lim/careers', 'http://www.limcollege.edu/', (40.7599322687, -73.9749658552)],

['Long Island Business Inst', '', 'http://www.libi.edu', (40.8418417242, -73.2923288658)],

['Long Island Business Institute - Flushing', '', 'http://www.libi.edu', (40.7602512526, -73.8299011581)],

['Mandl School Inc', '', 'http://www.mandl.edu', (40.7644424202, -73.9837128667)],

['Mildred Elley School', '', 'http://www.mildred-elley.edu', (42.6808311178, -73.7885586328)],

['Mildred Elley-Nyc', '', 'http://mildred-elley.edu', (40.7684987, -73.98245132)],

['Monroe College', 'https://www.monroecollege.edu/About/Employment/', 'http://www.monroecollege.edu', (40.8640027093, -73.9003298963)],

['Monroe College-New Rochelle Br Camps', 'https://www.monroecollege.edu/About/Employment/', 'http://www.monroecollege.edu', (40.9102540531, -73.778953921)],

['New York Automotive & Diesel Institute', '', 'http://', (40.7052209641, -73.7806300408)],

['New York Conservatory For Dramatic Arts', '', 'http://www.nycda.edu', (40.7400530462, -73.9934381828)],

['New York Film Academy', '', 'https://www.nyfa.edu', (40.7051424269, -74.0160109667)],

['Pacific College of Oriental Medicine', '', 'http://www.pacificcollege.edu', (40.7397145034, -73.9897681745)],

['Plaza College', '', 'http://www.plazacollege.edu', (40.7150542328, -73.8317057321)],

['SBI Campus - An Affiliate of Sanford-Brown', '', 'http://www.sbmelville.edu', (40.7788017594, -73.4154488084)],

['School of Visual Arts', '', 'http://www.sva.edu', (40.7386405929, -73.9823203964)],

["Sotheby's Institute of Art - NY", '', 'http://www.sothebysinstitute.com/newyork/index.html', (40.7568516928, -73.9722762363)],

["St. Paul's School of Nursing - Queens", '', 'http://www.stpaulsschoolofnursing.edu/', (40.7290214294, -73.8585980421)],

["St. Paul's School of Nursing - Staten Island", '', 'http://www.stpaulsschoolofnursing.com', (40.6057066799, -74.1799169809)],

['Swedish Institute Inc', '', 'http://www.swedishinstitute.edu', (40.7464409241, -73.9955751328)],

['Tri-State College of Acupuncture', '', 'http://www.tsca.edu', (40.7399128907, -74.0021760433)],

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
        print('\n', str(ii) + ',')


    # Display entries with missing coords
    if ii[3] == (0.0, 0.0):
        count += 1
        #print('\n', str(ii) + ',')


    # Display all entries
    #print(str(ii) + ',')
    


print('\nMissing:', count, '\nTotal entries:', len(db))













