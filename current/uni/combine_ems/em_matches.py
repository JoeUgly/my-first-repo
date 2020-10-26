
# Desc: Use school URLs from old em list (jj_v1) in new em list.

# Good and bad results are outputted. Good results have em URLs. eg: ['org name', 'em url', 'url', (coords)]
# Bad results have no em URLs. eg: ['org name', 'url', (coords)]
# Duplicate homepages are ignored. Same em URL is used for each one


# Prerequisites:
# some coords are 0.0, 0.0
# some home urls are ' ' '', 'http://', or 'http://http://...'


# To do:
# homepage redirects
# some coords are 0.0, 0.0
# some home urls are ' ' '', 'http://', or 'http://http://...'





new_l = [
['Art Institute of New York City', 'http://www.artinstitutes.edu', (40.7549303706, -73.988503444)],
['Asa College, Inc.', 'http://www.asa.edu', (40.6922729032, -73.9860830633)],
['Berkeley College - Main Campus', 'http://www.berkeleycollege.edu', (40.7538847351, -73.9795071152)],
['Berkeley College - Westchester', 'http://www.berkeleycollege.edu', (41.0346335886, -73.7679309244)],
['Bryant & Stratton Business College - North Syracuse', 'http://www.bryantstratton.edu', (43.1891227204, -76.2390537897)],
['Bryant & Stratton College - Albany', 'http://www.bryantstratton.edu', (42.6981365193, -73.8099631495)],
['Bryant & Stratton College - Buffalo', 'http://www.bryantstratton.edu', (42.8865731643, -78.8735239766)],
['Bryant & Stratton College - Greece', 'http://www.bryantstratton.edu', (43.2406605054, -77.6960945905)],
['Bryant & Stratton College - Henrietta', 'http://www.bryantstratton.edu', (43.0855524211, -77.6024060802)],
['Bryant & Stratton College - Southtowns Campus', 'http://www.bryantstratton.edu', (42.7906774624, -78.7672821844)],
['Bryant & Stratton College- Amherst', 'http://www.bryantstratton.edu', (43.0408165743, -78.7428249282)],
['Bryant Stratton College - Syracuse', 'http://www.bryantstratton.edu', (43.0590713535, -76.137047667)],
["Christie's Education, Inc", 'http://www.christies.edu', (40.7589337089, -73.9808982956)],
['The College of Westchester', 'http://www.cw.edu', (41.0336489614, -73.7843757839)],
['Devry College of New York', 'https://www.devry.edu/', (40.7474651252, -73.9833739393)],
['Elmira Business Inst', 'http://www.ebi.edu', (42.0901041677, -76.8091666394)],
['Elmira Business Institute - Vestal Executive Park', 'http://www.ebi.edu', (42.0970600729, -75.9754069723)],
['Five Towns College', 'http://www.ftc.edu', (40.7909330678, -73.3673848429)],
['Globe Inst of Tech Inc', 'http://www.globe.edu/', (40.7531259805, -73.9892959517)],
['Island Drafting & Tech Inst', 'http://www.idti.edu', (40.6756418059, -73.4169787759)],
['Jamestown Business College', 'http://www.jbcny.edu', (42.0955017298, -79.24973674660001)],
['Laboratory Inst of Merchandising', 'http://www.limcollege.edu/', (40.7599322687, -73.9749658552)],
['Long Island Business Inst', 'http://www.libi.edu', (40.8418417242, -73.2923288658)],
['Long Island Business Institute - Flushing', 'http://www.libi.edu', (40.7602512526, -73.8299011581)],
['Mandl School Inc', 'http://www.mandl.edu', (40.7644424202, -73.9837128667)],
['Mildred Elley School', 'http://www.mildred-elley.edu', (42.6808311178, -73.7885586328)],
['Mildred Elley-Nyc', 'http://mildred-elley.edu', (40.7684987, -73.98245132)],
['Monroe College', 'http://www.monroecollege.edu', (40.8640027093, -73.9003298963)],
['Monroe College-New Rochelle Br Camps', 'http://www.monroecollege.edu', (40.9102540531, -73.778953921)],
['New York Automotive & Diesel Institute', 'http://', (40.7052209641, -73.7806300408)],
['New York Conservatory For Dramatic Arts', 'http://www.nycda.edu', (40.7400530462, -73.9934381828)],
['New York Film Academy', 'https://www.nyfa.edu', (40.7051424269, -74.0160109667)],
['Pacific College of Oriental Medicine', 'http://www.pacificcollege.edu', (40.7397145034, -73.9897681745)],
['Plaza College', 'http://www.plazacollege.edu', (40.7150542328, -73.8317057321)],
['SBI Campus - An Affiliate of Sanford-Brown', 'http://www.sbmelville.edu', (40.7788017594, -73.4154488084)],
['School of Visual Arts', 'http://www.sva.edu', (40.7386405929, -73.9823203964)],
["Sotheby's Institute of Art - NY", 'http://www.sothebysinstitute.com/newyork/index.html', (40.7568516928, -73.9722762363)],
["St. Paul's School of Nursing - Queens", 'http://www.stpaulsschoolofnursing.edu/', (40.7290214294, -73.8585980421)],
["St. Paul's School of Nursing - Staten Island", 'http://www.stpaulsschoolofnursing.com', (40.6057066799, -74.1799169809)],
['Swedish Institute Inc', 'http://www.swedishinstitute.edu', (40.7464409241, -73.9955751328)],
['Tri-State College of Acupuncture', 'http://www.tsca.edu', (40.7399128907, -74.0021760433)],


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
        print(str(i[0]) + ',')
    
    # If one matching em URL then use that one
    elif len(i) == 2:
        one_count += 1
        i[0][1] = i[1]
        print(str(i[0]) + ',')
    
    # If matching em URLs then display them beneath
    else:
        multi_count += 1

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











