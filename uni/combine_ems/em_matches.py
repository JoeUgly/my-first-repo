
# Desc: Use school URLs from old em list (jj_v1) in new em list.

# Good and bad results are outputted. Good results have em URLs. eg: ['org name', 'em url', 'url', (coords)]
# Bad results have no em URLs. eg: ['org name', '', 'url', (coords)]
# Duplicate homepages are ignored. Same em URL is used for each one


# Prerequisites:
# some coords are 0.0, 0.0
# some home urls are ' ' '', 'http://', or 'http://http://...'


# To do:
# homepage redirects
# some coords are 0.0, 0.0
# some home urls are ' ' '', 'http://', or 'http://http://...'





new_l = [
['Broome Community College', 'http://www.sunybroome.edu', (42.1279320389, -75.9066929229)],
['Cayuga Community College - Fulton Center', 'http://www.cayuga-cc.edu', (43.3087811976, -76.3943832625)],
['Cayuga County Community College', 'http://www.cayuga-cc.edu', (42.942427686, -76.5428448566)],
['Clinton Community College', 'http://www.clinton.edu', (44.6484916509, -73.4397809665)],
['Columbia-Greene Community College', 'http://www.sunycgcc.edu', (42.2212174558, -73.8205788249)],
['Cornell Un Inst Res Dev', '', (42.4454850661, -76.5180349008)],
['Corning Community College', 'http://www.corning-cc.edu', (42.1181543973, -77.0777321582)],
['Dutchess Community College', 'http://www.sunydutchess.edu', (41.7221410762, -73.9068827009)],
['Erie Community College-City Campus', 'http://www.ecc.edu', (42.8820923579, -78.8730977283)],
['Erie Community College-North Campus', 'http://www.ecc.edu', (42.9660782722, -78.7192292156)],
['Erie Community College-South Campus', 'http://www.ecc.edu', (42.7739702025, -78.8005024656)],
['Fashion Institute of Technology', 'http://www.fitnyc.edu', (40.7467530244, -73.9941400194)],
['Finger Lakes Community College', 'http://www.fingerlakes.edu', (42.8677755341, -77.2418809729)],
['Fulton-Montgomery Community College', 'http://www.fmcc.suny.edu', (42.9824581854, -74.2981857881)],
['Genesee Community College', 'http://www.genesee.edu', (43.0169179769, -78.138075555)],
['Herkimer County Community College', 'http://www.herkimer.edu/', (43.0363179282, -75.0121490434)],
['Hudson Valley Community College', 'http://www.hvcc.edu', (42.6969513827, -73.6826586168)],
['Jamestown Community College', 'http://www.sunyjcc.edu', (42.1155017134, -79.2201867741)],
['Jamestown Community College Cattaraugus County Campus', 'http://www.sunyjcc.edu', (42.080750755, -78.4296767225)],
['Jefferson Community College', 'http://www.sunyjefferson.edu', (43.9906225707, -75.936591213)],
['Mohawk Valley Community College', 'http://www.mvcc.edu', (43.0771112935, -75.2197380475)],
['Mohawk Valley Community College-Rome Campus', 'http://www.mvcc.edu', (43.2201612777, -75.4291580028)],
['Monroe Community College', 'http://www.monroecc.edu/', (43.1039514379, -77.6135699885)],
['Monroe Community College - Downtown Campus', 'http://www.monroecc.edu/downtown', (43.16057467, -77.61904511)],
['Nassau Community College', 'http://www.ncc.edu', (40.7305643961, -73.5915572062)],
['New York State College of Agriculture And Life Sciences at Cornell', 'https://cals.cornell.edu/', (42.4470150296, -76.4823949559)],
['New York State College of Human Ecology at Cornell University', 'http://www.human.cornell.edu', (42.4470150296, -76.4823949559)],
['New York State College of Veterinary Medicine at Cornell University', 'https://www.vet.cornell.edu/', (42.4470150296, -76.4823949559)],
['New York State School of Industrial And Labor Relations at Cornell', 'http://www.ilr.cornell.edu', (42.4411150027, -76.4962899763)],
['Niagara County Community College', 'http://niagaracc.suny.edu', (43.1433897065, -78.8771693901)],
['North Country Community College', 'http://www.nccc.edu', (44.3196603443, -74.1217755726)],
['North Country Community College-Elizabethtown Campus', 'http://www.nccc.edu', (44.2071799834, -73.6125850881)],
['North Country Community College-Malone Campus', 'http://www.nccc.edu', (44.7281199535, -74.2771800816)],
['North Country Community College-Ticonderoga Campus', 'http://www.nccc.edu', (43.8483589211, -73.4348090122)],
['NYS College of Ceramics at Alfred University', 'http://www.alfred.edu', (42.2562561522, -77.78738279)],
['Onondaga Community College', 'http://www.sunyocc.edu', (43.003121379, -76.197967636)],
['Orange County Comm College - Newburgh', 'http://www.sunyorange.edu', (41.5002076512, -74.0080464557)],
['Orange County Community College', 'http://www.sunyorange.edu', (41.4385663747, -74.4253941399)],
['Rockland Community College', 'http://www.sunyrockland.edu', (41.1316525826, -74.0845787256)],
['Schenectady County Community College', 'http://sunysccc.edu', (42.815763278, -73.9493207653)],
['State University College at Plattsburgh', 'http://www.plattsburgh.edu', (44.6944204269, -73.4660847546)],
['State University College of Oswego - Metro Center', 'https://www.oswego.edu/syracuse/', (43.05026807, -76.15269074)],
['State University of New York at Albany', 'http://www.albany.edu', (42.6894994696, -73.8202347679)],
['State University of New York at Binghamton', 'http://www.binghamton.edu', (42.0922160443, -75.9480719501)],
['State University of New York at Buffalo', 'http://www.buffalo.edu', (43.0014292257, -78.7901062945)],
['State University of New York at Stony Brook', 'http://www.stonybrook.edu', (40.9154653167, -73.1228381196)],
['State University of New York College at Brockport', 'https://www.brockport.edu', (43.20995983, -77.95214253)],
['State University of New York College at Buffalo', 'http://suny.buffalostate.edu', (42.9326738069, -78.8770408526)],
['State University of New York College at Cortland', 'http://www2.cortland.edu', (42.5972462055, -76.1897096475)],
['State University of New York College at Fredonia', 'http://www.fredonia.edu', (42.4518385924, -79.3402424121)],
['State University of New York College at Geneseo', 'http://www.geneseo.edu', (42.7957246342, -77.819335919)],
['State University of New York College at New Paltz', 'http://www.newpaltz.edu', (41.7427460961, -74.0841046273)],
['State University of New York College at Old Westbury', 'http://www.oldwestbury.edu', (40.7794946985, -73.5740357667)],
['State University of New York College at Oneonta', 'http://www.oneonta.edu', (42.4654780432, -75.0680041033)],
['State University of New York College at Oswego', 'http://www.oswego.edu', (43.451412138, -76.5441351481)],
['State University of New York College at Potsdam', 'http://www.potsdam.edu', (44.6637806926, -74.9784114574)],
['State University of New York College at Purchase', 'http://www.purchase.edu', (41.039038225, -73.6962345232)],
['State University of New York College of Environmental Science And Forestry', 'http://www.esf.edu', (43.0347425343, -76.1347373878)],
['State University of New York College of Optometry', 'http://www.sunyopt.edu', (40.7539557509, -73.9818868515)],
['State University of New York College of Technology at Delhi', 'http://www.delhi.edu', (42.268528646, -74.922171006)],
['State University of New York Empire State College', 'http://www.esc.edu', (43.0778907316, -73.7815188994)],
['State University of New York Health Science Center at Brooklyn', 'http://www.downstate.edu/', (40.6553620016, -73.945075892)],
['State University of New York Health Science Center at Syracuse', 'http://www.upstate.edu/', (43.042630081, -76.1405422462)],
['State University of New York System Administration', 'http://www.suny.edu', (42.6948500932, -73.7220800677)],
['SUC at Plattsburgh at Adirondack Community College', 'http://www.plattsburgh.edu/', (43.3542111568, -73.6575985465)],
['Suffolk County Community College', 'http://www.sunysuffolk.edu', (40.845934881, -73.0535317455)],
['Suffolk County Community College Eastern Campus', 'http://www.sunysuffolk.edu', (40.8843680211, -72.6971870692)],
['Suffolk County Community College Western Campus', 'http://www.sunysuffolk.edu', (40.7980535929, -73.2712463165)],
['Sullivan County Community College', 'http://www.sunysullivan.edu', (41.7645685528, -74.669718954)],
['SUNY Coll of Ag & Tech at Delhi - Sccc', 'http://www.delhi.edu', (42.815763278, -73.9493207653)],
['SUNY College of  Agriculture And Technology at Morrisville', 'http://www.morrisville.edu', (42.8966574697, -75.6400895954)],
['SUNY College of  Technology at Alfred Wellsville Campus', 'http://www.alfredstate.edu', (42.1104065249, -77.9444174266)],
['SUNY College of Agriculture And Technology at Cobleskill', 'http://www.cobleskill.edu', (42.6725149621, -74.4981810245)],
['SUNY College of Agriculture And Technology at Morrisville - Norwich Campus', 'http://www.morrisville.edu/norwich', (42.5306561225, -75.5238100519)],
['SUNY College of Technology at Alfred', 'http://www.alfredstate.edu', (42.2552374966, -77.7946833152)],
['SUNY College of Technology at Canton', 'http://www.canton.edu/', (44.6072664206, -75.1850279439)],
['SUNY College of Technology at Farmingdale', 'http://www.farmingdale.edu', (40.7534814826, -73.422346327)],
['SUNY Maritime College', 'http://www.sunymaritime.edu', (40.8071954798, -73.7954153272)],
['SUNY Polytechnic Institute', 'http://www.sunypoly.edu', (43.1330529952, -75.226662082)],
['Tompkins Cortland Community College', 'http://www.tc3.edu', (42.5013825027, -76.2915156589)],
['Ulster County Community College', 'http://www.sunyulster.edu', (41.8573690608, -74.1338430926)],
['Westchester Community College', 'http://www.sunywcc.edu/', (41.0700872135, -73.7843656064)],

]






old_l = (
'http://careers.canisius.edu/cw/en-us/listing',
'http://careers.marist.edu/cw/en-us/listing',
'http://cooper.edu/work/employment-opportunities',
'http://einstein.yu.edu/administration/human-resources/career-opportunities.html',
'http://gts.edu/job-postings',
'http://huc.edu/about/employment-opportunities',
'http://humanresources.vassar.edu/jobs',
'http://inside.manhattan.edu/offices/human-resources/jobs.php',
'http://jobs.medaille.edu',
'http://jobs.union.edu/cw/en-us/listing',
'http://liu.edu/brooklyn.aspx',
'http://newschool.edu/public-engagement',
'http://niagaracc.suny.edu/careers/nccc-jobs.php',
'http://sunysccc.edu/About-Us/Office-of-Human-Resources/Employment-Opportunities',
'http://utica.edu/hr/employment.cfm',
'http://www.bard.edu/employment/employment',
'http://www.berkeleycollege.edu/index.htm',
'http://www.canton.edu/human_resources/job_opportunities.html',
'http://www.cazenovia.edu/campus-resources/human-resources/employment-opportunities',
'http://www.colgate.edu/working-at-colgate',
'http://www.college.columbia.edu',
'http://www.columbia.edu/cu/ssw',
'http://www.dental.columbia.edu',
'http://www.dyc.edu/about/administrative-offices/human-resources/career-opportunities.aspx',
'http://www.gs.columbia.edu',
'http://www.houghton.edu/campus/human-resources/employment',
'http://www.hunter.cuny.edu/hr/Employment',
'http://www.jtsa.edu/jobs-at-jts',
'http://www.law.columbia.edu',
'http://www.liu.edu/post',
'http://www.mcny.edu/index.php',
'http://www.monroecc.edu/employment',
'http://www.nccc.edu/careers-2',
'http://www.nycc.edu/employment-opportunities',
'http://www.nyts.edu',
'http://www.nyu.edu/about/careers-at-nyu.html',
'http://www.paulsmiths.edu/humanresources/employment',
'http://www.potsdam.edu/crane',
'http://www.qcc.cuny.edu/employment/index.html',
'http://www.rit.edu/employment_rit.html',
'http://www.rochester.edu/working/hr/jobs',
'http://www.simon.rochester.edu/faculty-and-research/faculty-directory/faculty-recruitment/index.aspx',
'http://www.sunyacc.edu/job-listings',
'http://www.sunywcc.edu/about/jobshuman-resources',
'http://www.webb.edu/employment',
'http://www.youngwomenscollegeprep.org',
'http://www1.cuny.edu/sites/onboard/homepage/getting-started/campus/medgar-evers-college',
'http://www1.sunybroome.edu/about/employment',
'https://albany.interviewexchange.com/jobsrchresults.jsp',
'https://alfredstate.interviewexchange.com/static/clients/481ASM1/index.jsp',
'https://apply.interfolio.com/14414/positions',
'https://careers-nyit.icims.com/jobs/search?ss=1',
'https://careers.barnard.edu',
'https://careers.columbia.edu',
'https://careers.columbia.edu/content/how-apply',
'https://careers.mountsinai.org/jobs?page=1',
'https://careers.newschool.edu',
'https://careers.pace.edu/postings/search',
'https://careers.pageuppeople.com/876/cw/en-us/listing',
'https://careers.skidmore.edu/postings/search',
'https://clarkson.peopleadmin.com',
'https://clinton.interviewexchange.com/static/clients/552CCM1/index.jsp',
'https://cobleskill.interviewexchange.com/static/clients/474SCM1/index.jsp',
'https://cshl.peopleadmin.com/postings/search',
'https://cuny.jobs',
'https://daemen.applicantpro.com/jobs',
'https://employment.acphs.edu/postings/search',
'https://employment.potsdam.edu/postings/search',
'https://employment.stlawu.edu/postings/search',
'https://farmingdale.interviewexchange.com/static/clients/383FAM1/index.jsp',
'https://fitnyc.interviewexchange.com/static/clients/391FIM1/index.jsp',
'https://fredonia.interviewexchange.com/static/clients/471SFM1/index.jsp',
'https://genesee.interviewexchange.com/static/clients/374GCM1/index.jsp',
'https://herkimer.interviewexchange.com/static/clients/505HCM1/index.jsp',
'https://hr.adelphi.edu/position-openings',
'https://hr.cornell.edu/jobs',
'https://hvcc.edu/hr/employment-opportunities.html',
'https://iona-openhire.silkroad.com/epostings/index.cfm?fuseaction=app.jobsearch',
'https://ithaca.peopleadmin.com',
'https://jobs.buffalostate.edu',
'https://jobs.cortland.edu',
'https://jobs.excelsior.edu',
'https://jobs.geneseo.edu/postings/search',
'https://jobs.liu.edu/#/list',
'https://jobs.mercy.edu/postings/search',
'https://jobs.naz.edu/postings/search',
'https://jobs.niagara.edu/JobPostings.aspx',
'https://jobs.plattsburgh.edu/postings/search',
'https://jobs.purchase.edu/applicants/jsp/shared/frameset/Frameset.jsp',
'https://jobs.sjfc.edu',
'https://jobsatupstate.peopleadmin.com/applicants/jsp/shared/search/SearchResults_css.jsp',
'https://law-touro-csm.symplicity.com/students/index.php/pid170913',
'https://maritime.interviewexchange.com/static/clients/373SMM1/index.jsp',
'https://mountsaintvincent.edu/campus-life/campus-services/human-resources/employment-opportunities',
'https://mvcc.csod.com/ats/careersite/search.aspx',
'https://ncc.interviewexchange.com/static/clients/489NCM1/index.jsp',
'https://occc.interviewexchange.com/static/clients/437SOM1/index.jsp',
'https://oldwestbury.interviewexchange.com/static/clients/519OWM1/index.jsp',
'https://oswego.interviewexchange.com/static/clients/313OSM1/index.jsp',
'https://pa334.peopleadmin.com/postings/search',
'https://recruiting.ultipro.com/CUL1001CLNRY/JobBoard/5d1a692d-cf6b-4b4f-8652-c60b25898609/?q=&o=postedDateDesc',
'https://rpijobs.rpi.edu',
'https://strose.interviewexchange.com/jobsrchresults.jsp',
'https://suny.oneonta.edu/sponsored-programs/employment-opportunities',
'https://sunydutchess.interviewexchange.com/static/clients/539DCM1/index.jsp',
'https://sunyocc.peopleadmin.com/postings/search',
'https://sunyopt.peopleadmin.com/postings/search',
'https://sunypoly.interviewexchange.com/static/clients/511SPM1/hiring.jsp',
'https://sunysullivan.edu/offices/associate-vp-for-planning-human-resources-facilities/job-opportunities',
'https://touro.peopleadmin.com/postings/search',
'https://trocaire.applicantpro.com/jobs',
'https://utsnyc.edu/about/careers-at-union',
'https://wagner.edu/hr/hr_openings',
'https://workforcenow.adp.com/mdf/recruitment/recruitment.html?cid=b635a855-6cf7-4ee7-ba36-6da36d9f2eea&ccId=19000101_000001&type=MP',
'https://www.alfred.edu/jobs-at-alfred/index.cfm',
'https://www.bankstreet.edu/about-bank-street/job-opportunities',
'https://www.binghamton.edu/human-resources/employment-opportunities/index.html',
'https://www.brockport.edu/support/human_resources/empop/vacancies',
'https://www.brooklaw.edu/about-us/job-opportunities.aspx',
'https://www.cayuga-cc.edu/about/human-resources',
'https://www.cnr.edu/employment-opportunities',
'https://www.davisny.edu/jobs',
'https://www.dc.edu/human-resources',
'https://www.ecc.edu/work',
'https://www.elmira.edu/Student/Offices_Resources/Employment_Opportunities/index.html',
'https://www.esc.edu/human-resources/employment-opportunities',
'https://www.flcc.edu/jobs',
'https://www.fmcc.edu/about/employment-opportunities',
'https://www.fordham.edu/info/23411/job_opportunities',
'https://www.ftc.edu/employment',
'https://www.hamilton.edu/offices/human-resources/employment/job-opportunities',
'https://www.hartwick.edu/about-us/employment/human-resources/employment-opportunities',
'https://www.helenefuld.edu/employment',
'https://www.hilbert.edu/about/human-resources/hilbert-job-openings',
'https://www.hofstra.edu/about/jobs/index.html',
'https://www.hofstra.edu/academics/colleges/zarb',
'https://www.hws.edu/offices/hr/employment/index.aspx',
'https://www.juilliard.edu/jobs',
'https://www.keuka.edu/hr/employment-opportunities',
'https://www.laguardia.edu/employment',
'https://www.lemoyne.edu/Work-at-Le-Moyne',
'https://www.limcollege.edu/about-lim/careers',
'https://www.mmm.edu/offices/human-resources/Employment',
'https://www.molloy.edu/about-molloy-college/human-resources/careers-at-molloy',
'https://www.monroecollege.edu/About/Employment/u',
'https://www.morrisville.edu/contact/offices/human-resources/careers',
'https://www.msmc.edu/employment',
'https://www.msmnyc.edu/about/employment-at-msm',
'https://www.mville.edu/about-manhattanville/human-resources',
'https://www.newpaltz.edu/hr/jobs.html',
'https://www.newschool.edu/performing-arts',
'https://www.nyack.edu/site/employment-opportunities',
'https://www.paycomonline.net/v4/ats/web.php/jobs',
'https://www.qc.cuny.edu/HR/Pages/JobListings.aspx',
'https://www.roberts.edu/employment',
'https://www.rochester.edu/faculty-recruiting/positions',
'https://www.sage.edu/about/human-resources/employment-opportunities',
'https://www.sarahlawrence.edu/human-resources/job-openings.html',
'https://www.sbu.edu/jobs-at-sbu',
'https://www.sfc.edu/about/careers',
'https://www.sjcny.edu/employment',
'https://www.stac.edu/about-stac/jobs-stac',
'https://www.stjohns.edu/about/administrative-offices/human-resources/recruitment',
'https://www.stonybrookmedicine.edu/careers',
'https://www.sujobopps.com/postings/search',
'https://www.suny.edu/campuses/cornell-vet',
'https://www.suny.edu/careers/employment/index.cfm?s=y',
'https://www.sunycgcc.edu/about-cgcc/employment-cgcc',
'https://www.sunyjcc.edu/about/human-resources/jobs',
'https://www.sunyjefferson.edu/careers-jefferson/open-positions.php',
'https://www.sunyulster.edu/campus_and_culture/about_us/jobs.php',
'https://www.tkc.edu/careers-at-kings',
'https://www.tompkinscortland.edu/college-info/employment',
'https://www.ubjobs.buffalo.edu',
'https://www.usmma.edu/about/employment/career-opportunities',
'https://www.vaughn.edu/jobs',
'https://www.villa.edu/about-us/employment-opportunities',
'https://www.warner.rochester.edu/faculty/positions',
'https://www.wells.edu/jobs',
'https://www.york.cuny.edu/administrative/human-resources/jobs',
'https://www.yu.edu/hr/opportunities',
'https://www2.appone.com/Search/Search.aspx?ServerVar=ConcordiaCollege.appone.com&results=yes',
'https://www3.sunysuffolk.edu/About/Employment.asp'
)





# Removes extra info from urls
def dup_checker_f(dup_checker):

    # Remove scheme
    if dup_checker.startswith('http://') or dup_checker.startswith('https://'):
        dup_checker = dup_checker.split('://')[1]

    # Remove www. and variants
    if dup_checker.startswith('www.'):
        dup_checker = dup_checker.split('www.')[1]
    elif dup_checker.startswith('www2.'):
        dup_checker = dup_checker.split('www2.')[1]
    elif dup_checker.startswith('www3.'):
        dup_checker = dup_checker.split('www3.')[1]

    # Remove fragments
    dup_checker = dup_checker.split('#')[0]

    # Remove trailing whitespace and slash and then lowercase it
    dup_checker = dup_checker.strip().strip('/').lower()

    ## Remove double forward slashes?
    dup_checker = dup_checker.replace('//', '/')

    ## Remove domain?
    if dup_checker.endswith('.edu') or dup_checker.endswith('.com'):

        if dup_checker.count('.') > 1:
            dup_checker = '.'.join(dup_checker.split('.')[1:])
        else:
            dup_checker = dup_checker.rsplit('.')[0]

    
    return dup_checker



fin = [] # List contents: [ [org name, '', homepage, (coords)], em url1, em url2, ... ]

err_count = 0 # count number of errors
count = 0 # count total number of matches ## kinda useless
no_count = 0 # count number of home URLs with no matching em URL
one_count = 0 # count number of home URLs with one matching em URL
multi_count = 0 # count number of home URLs with multiple matching em URLs


# Append all matching em URLs to list also containing full entry
for i in new_l:

    dup = dup_checker_f(i[1])
    #print('~~~ ', dup)

    ## This is solved by the dup_checker_f 
    if dup == 'https':
        err_count += 1
        print('\nError:', dup, i)
        #count += 1
        #continue


    # Use this list to add org name once and all em URL matches
    item_l = []
    item_l.append(i)

    # Don't look for em URL matches if homepage is blank
    if not dup:
        count += 1
        err_count += 1
        print('\nError:', dup, i)

    # Find em URL matches
    else:
        for ii in old_l:

            if dup in ii:

                item_l.append(ii)

        count += 1

    # Append org name and all em matches
    fin.append(item_l)

print('\n old total:', len(old_l), '\n new total:', len(new_l), '\n total matches:', count, '\n\n')




# Pretty print
for i in fin:
    #print('\n\n\n', len(i))
    print('')

    # Create em URL placeholder
    i[0].insert(1, '')

    # Create homepage placeholder if homepage is blank
    if not i[0][2]:
        print(str(i[0]) + ',')
        continue

    # If no matching em URLs then just print blank em URL
    if len(i) == 1:
        no_count += 1
        #print(str(i[0]) + ',')
    
    # If one matching em URL then use that one
    elif len(i) == 2:
        one_count += 1
        i[0][1] = i[1]
        print(str(i[0]) + ',')
    
    # If matching em URLs then display them beneath
    else:
        multi_count += 1
        #print(str(i[0]) + ',')

        # Don't print comma after em URLs
        for ii in i:
            if not ii: continue
            if i.index(ii) == 0:
                print(str(ii) + ',')
            else:
                print(ii)
    

print('\n\n\n\nthese should match:', len(fin), count, len(new_l), '\n\n')
print('zero, one, and multi matches:', no_count, one_count, multi_count)
print('\n\n errors:', err_count, '\n\n')




# Find missing coords
print('\n\n Missing coords:')
for i in new_l:
    if i[3] == (0.0, 0.0):
        print('\n', i)


# Find missing homepages
print('\n\n Missing homepage:')
for i in new_l:
    if not i[2]:
        print('\n', i)











