

# Desc: Merge output from em_finder into main db


# To do:
# if duplicate homepages exists, then use duplicate em URL



# Overwrite this list with new enties after you update the db list below
# This list doesn't need to contain all entries
e_l = [
['Adirondack Community College', 'https://www.sunyacc.edu/job-listings', 'http://www.sunyacc.edu'],
['Broome Community College', 'http://www1.sunybroome.edu/about/employment/', 'http://www.sunybroome.edu'],
['Cayuga Community College - Fulton Center', 'https://www.cayuga-cc.edu/about/human-resources/', 'http://www.cayuga-cc.edu'],
['Cayuga County Community College', 'https://www.cayuga-cc.edu/about/human-resources/', 'http://www.cayuga-cc.edu'],
['Corning Community College', 'https://www.schooljobs.com/careers/corningcc', 'http://www.corning-cc.edu'],
['Dutchess Community College', 'https://sunydutchess.interviewexchange.com/static/clients/539DCM1/index.jsp;jsessionid=12D96992248D3646BB215D3A46B10370', 'http://www.sunydutchess.edu'],
['Erie Community College-City Campus', 'https://www.ecc.edu/work/', 'http://www.ecc.edu'],
['Erie Community College-North Campus', 'https://www.ecc.edu/work/', 'http://www.ecc.edu'],
['Erie Community College-South Campus', 'https://www.ecc.edu/work/', 'http://www.ecc.edu'],
['Fashion Institute of Technology', 'https://fitnyc.interviewexchange.com/static/clients/391FIM1/index.jsp;jsessionid=41A4FBA9B0DC2612935C2529A73C2936', 'http://www.fitnyc.edu'],
['Finger Lakes Community College', 'https://www.flcc.edu/jobs/', 'http://www.fingerlakes.edu'],
['Fulton-Montgomery Community College', 'https://www.fmcc.edu/about/employment-opportunities/', 'http://www.fmcc.suny.edu'],
['Genesee Community College', 'https://genesee.interviewexchange.com/static/clients/374GCM1/index.jsp;jsessionid=032F128C35FC8E9F02FBCB965C03D848', 'http://www.genesee.edu'],
['Herkimer County Community College', 'https://herkimer.interviewexchange.com/static/clients/505HCM1/index.jsp;jsessionid=2DCDC23D61BD00CB222FF98880598D2C', 'http://www.herkimer.edu/'],
['Hudson Valley Community College', 'https://hvcc.edu/hr/employment-opportunities.html', 'http://www.hvcc.edu'],
['Jefferson Community College', 'https://sunyjefferson.interviewexchange.com/static/clients/559JCM1/index.jsp;jsessionid=DD4F461844EFD22B0B47F6FDC030CB98', 'http://www.sunyjefferson.edu'],
['Monroe Community College', 'https://monroecc.interviewexchange.com/static/clients/547MCM1/index.jsp;jsessionid=265A02EF8806ED68595CD2F7A81343BE', 'http://www.monroecc.edu/'],
['Monroe Community College - Downtown Campus', 'https://monroecc.interviewexchange.com/static/clients/547MCM1/index.jsp', 'http://www.monroecc.edu/downtown'],
['Nassau Community College', 'https://ncc.interviewexchange.com/static/clients/489NCM1/index.jsp;jsessionid=E72EDA6634B3056F7C3E5155EFA64D9E', 'http://www.ncc.edu'],
['New York State College of Agriculture And Life Sciences at Cornell', 'https://hr.cornell.edu/jobs', 'http://cals.cornell.edu/'],
['New York State College of Human Ecology at Cornell University', 'https://hr.cornell.edu/jobs', 'http://www.human.cornell.edu'],
['New York State College of Veterinary Medicine at Cornell University', 'https://hr.cornell.edu/jobs', 'http://www.vet.cornell.edu/'],
['New York State School of Industrial And Labor Relations at Cornell', 'https://hr.cornell.edu/jobs', 'http://www.ilr.cornell.edu'],
['Niagara County Community College', 'https://niagaracc-suny.peopleadmin.com/', 'http://niagaracc.suny.edu'],
['NYS College of Ceramics at Alfred University', 'https://alfredstate.interviewexchange.com/static/clients/481ASM1/index.jsp;jsessionid=1FD9618F09A506C78E0848272B52CDCD', 'http://www.alfred.edu'],
['Onondaga Community College', 'https://sunyocc.peopleadmin.com/postings/search', 'http://www.sunyocc.edu'],
['Orange County Comm College - Newburgh', 'https://occc.interviewexchange.com/static/clients/437SOM1/index.jsp;jsessionid=3BB2BD6D43B23F2E29388594F2024ECD', 'http://www.sunyorange.edu'],
['Orange County Community College', 'https://occc.interviewexchange.com/static/clients/437SOM1/index.jsp', 'http://www.sunyorange.edu'],
['Schenectady County Community College', 'https://sunysccc.edu/About-Us/Office-of-Human-Resources/Employment-Opportunities', 'http://sunysccc.edu'],
['State University College at Plattsburgh', 'https://jobs.plattsburgh.edu/postings/search', 'http://www.plattsburgh.edu'],
['State University College of Oswego - Metro Center', 'https://oswego.interviewexchange.com/static/clients/313OSM1/index.jsp;jsessionid=962E3760E33B26C1DD9E4B538ACBBA70', 'http://www.oswego.edu/syracuse/'],
['State University of New York at Albany', 'https://albany.interviewexchange.com/jobsearchfrm.jsp;jsessionid=47159D01875C2A813E6B2E434302860C', 'http://www.albany.edu'],
['State University of New York at Binghamton', 'https://www.binghamton.edu/human-resources/employment-opportunities/index.html', 'http://www.binghamton.edu'],
['State University of New York at Buffalo', 'https://www.ubjobs.buffalo.edu/', 'http://www.buffalo.edu'],
['State University of New York at Stony Brook', 'https://www.stonybrookmedicine.edu/careers', 'http://www.stonybrook.edu'],
['State University of New York College at Brockport', 'https://www.brockport.edu/support/human_resources/empop/vacancies/', 'http://www.brockport.edu'],
['State University of New York College at Buffalo', 'https://jobs.buffalostate.edu/', 'http://suny.buffalostate.edu'],
['State University of New York College at Cortland', 'https://jobs.cortland.edu/', 'http://www2.cortland.edu'],
['State University of New York College at Fredonia', 'https://fredonia.interviewexchange.com/static/clients/471SFM1/index.jsp;jsessionid=9975E214DCC775D2E316B2806F660F31', 'http://www.fredonia.edu'],
['State University of New York College at Geneseo', 'https://jobs.geneseo.edu/postings/search', 'http://www.geneseo.edu'],
['State University of New York College at New Paltz', 'https://www.newpaltz.edu/hr/jobs.html', 'http://www.newpaltz.edu'],
['State University of New York College at Old Westbury', 'https://oldwestbury.interviewexchange.com/static/clients/519OWM1/index.jsp;jsessionid=3D0D3BEDEDADFE0BEBB6F16FA5A5BDF4', 'http://www.oldwestbury.edu'],
['State University of New York College at Oneonta', 'https://suny.oneonta.edu/sponsored-programs/employment-opportunities', 'http://www.oneonta.edu'],
['State University of New York College at Oswego', 'https://oswego.interviewexchange.com/static/clients/313OSM1/index.jsp', 'http://www.oswego.edu'],
['State University of New York College at Potsdam', 'https://employment.potsdam.edu/postings/search', 'http://www.potsdam.edu'],
['State University of New York College of Environmental Science And Forestry', 'https://esf.interviewexchange.com/static/clients/444ESM1/index.jsp;jsessionid=EE14095FB9422A0DFC464092AF86C37E', 'http://www.esf.edu'],
['State University of New York College of Optometry', 'https://sunyopt.peopleadmin.com/postings/search', 'http://www.sunyopt.edu'],
['State University of New York College of Technology at Delhi', 'https://delhi.interviewexchange.com/static/clients/409SDM1/index.jsp;jsessionid=6C541E649E9E2E0105BCC95BC2D6F747', 'http://www.delhi.edu'],
['State University of New York Empire State College', 'https://www.esc.edu/human-resources/employment-opportunities/', 'http://www.esc.edu'],
['State University of New York Health Science Center at Brooklyn', 'https://www.downstate.edu/human_resources/links.html', 'http://www.downstate.edu/'],
['State University of New York Health Science Center at Syracuse', 'https://jobsatupstate.peopleadmin.com/applicants/jsp/shared/Welcome_css.jsp', 'http://www.upstate.edu/'],
['State University of New York System Administration', 'https://www.suny.edu/careers/employment/index.cfm?s=y', 'http://www.suny.edu'],
['SUC at Plattsburgh at Adirondack Community College', 'https://jobs.plattsburgh.edu/postings/search', 'http://www.plattsburgh.edu/'],
['Suffolk County Community College', 'https://www3.sunysuffolk.edu/About/Employment.asp', 'http://www.sunysuffolk.edu'],
['Suffolk County Community College Eastern Campus', 'https://www3.sunysuffolk.edu/About/Employment.asp', 'http://www.sunysuffolk.edu'],
['Suffolk County Community College Western Campus', 'https://www3.sunysuffolk.edu/About/Employment.asp', 'http://www.sunysuffolk.edu'],
['Sullivan County Community College', 'https://sunysullivan.edu/offices/associate-vp-for-planning-human-resources-facilities/job-opportunities/', 'http://www.sunysullivan.edu'],
['SUNY Coll of Ag & Tech at Delhi - Sccc', 'https://delhi.interviewexchange.com/static/clients/409SDM1/index.jsp', 'http://www.delhi.edu'],
['SUNY College of  Agriculture And Technology at Morrisville', 'https://morrisville.interviewexchange.com/static/clients/463MSM1/index.jsp', 'http://www.morrisville.edu'],
['SUNY College of  Technology at Alfred Wellsville Campus', 'https://alfredstate.interviewexchange.com/static/clients/481ASM1/index.jsp', 'http://www.alfredstate.edu'],
['SUNY College of Agriculture And Technology at Cobleskill', 'https://cobleskill.interviewexchange.com/static/clients/474SCM1/index.jsp;jsessionid=BD5806BB8389AC4E3A21040DBA7646FC', 'http://www.cobleskill.edu'],
['SUNY College of Agriculture And Technology at Morrisville - Norwich Campus', 'https://morrisville.interviewexchange.com/static/clients/463MSM1/index.jsp', 'http://www.morrisville.edu/norwich'],
['SUNY College of Technology at Alfred', 'https://alfredstate.interviewexchange.com/static/clients/481ASM1/index.jsp', 'http://www.alfredstate.edu'],
['SUNY College of Technology at Canton', 'https://www.canton.edu/hr/job_opportunities.html', 'http://www.canton.edu/'],
['SUNY College of Technology at Farmingdale', 'https://farmingdale.interviewexchange.com/static/clients/383FAM1/index.jsp;jsessionid=B3E8444AFCB21A8C30C04A967C355EAF', 'http://www.farmingdale.edu'],
['SUNY Maritime College', 'https://maritime.interviewexchange.com/static/clients/373SMM1/index.jsp;jsessionid=6516C4382FC514F6FFAD3AE945594A1C', 'http://www.sunymaritime.edu'],
['SUNY Polytechnic Institute', 'https://sunypoly.interviewexchange.com/static/clients/511SPM1/hiring.jsp;jsessionid=5131A63D403D63CAB03C2D549AE995E1', 'http://www.sunypoly.edu'],
['Tompkins Cortland Community College', 'https://www.tompkinscortland.edu/academics/programs/human-services', 'http://www.tc3.edu'],
['Ulster County Community College', 'https://www.sunyulster.edu/campus_and_culture/about_us/jobs.php', 'http://www.sunyulster.edu'],
['Westchester Community College', 'https://www.sunywcc.edu/about/jobshuman-resources/', 'http://www.sunywcc.edu/'],
]



# Overwrite this list with output from this program after supplying new entries above
# This list must contain all entries
db = [
['Adirondack Community College', 'http://www.sunyacc.edu/job-listings', 'http://www.sunyacc.edu'],
['Broome Community College', 'http://www1.sunybroome.edu/about/employment', 'http://www.sunybroome.edu'],
['Cayuga Community College - Fulton Center', 'http://www.cayuga-cc.edu/about/human-resources', 'http://www.cayuga-cc.edu'],
['Cayuga County Community College', 'http://www.cayuga-cc.edu/about/human-resources', 'http://www.cayuga-cc.edu'],
['Clinton Community College', 'http://clinton.interviewexchange.com/static/clients/552CCM1/index.jsp', 'http://www.clinton.edu'],
['Columbia-Greene Community College', 'http://www.sunycgcc.edu/about-cgcc/employment-cgcc', 'http://www.sunycgcc.edu'],
['Cornell Un Inst Res Dev', '', ''],
['Corning Community College', 'http://www.schooljobs.com/careers/corningcc', 'http://www.corning-cc.edu'],
['Dutchess Community College', 'http://sunydutchess.interviewexchange.com/static/clients/539DCM1/index.jsp', 'http://www.sunydutchess.edu'],
['Erie Community College-City Campus', 'http://www.ecc.edu/work', 'http://www.ecc.edu'],
['Erie Community College-North Campus', 'http://www.ecc.edu/work', 'http://www.ecc.edu'],
['Erie Community College-South Campus', 'http://www.ecc.edu/work', 'http://www.ecc.edu'],
['Fashion Institute of Technology', 'http://fitnyc.interviewexchange.com/static/clients/391FIM1/index.jsp', 'http://www.fitnyc.edu'],
['Finger Lakes Community College', 'http://www.flcc.edu/jobs/', 'http://www.fingerlakes.edu'],
['Fulton-Montgomery Community College', 'http://www.fmcc.edu/about/employment-opportunities/', 'http://www.fmcc.suny.edu'],
['Genesee Community College', 'http://genesee.interviewexchange.com/static/clients/374GCM1/index.jsp', 'http://www.genesee.edu'],
['Herkimer County Community College', 'http://herkimer.interviewexchange.com/static/clients/505HCM1/index.jsp', 'http://www.herkimer.edu/'],
['Hudson Valley Community College', 'http://hvcc.edu/hr/employment-opportunities.html', 'http://www.hvcc.edu'],
['Jamestown Community College', 'http://www.sunyjcc.edu/about/human-resources/jobs', 'http://www.sunyjcc.edu'],
['Jamestown Community College Cattaraugus County Campus', 'http://www.sunyjcc.edu/about/human-resources/jobs', 'http://www.sunyjcc.edu'],
['Jefferson Community College', 'http://sunyjefferson.interviewexchange.com/static/clients/559JCM1/index.jsp', 'http://www.sunyjefferson.edu'],
['Mohawk Valley Community College', 'http://mvcc.csod.com/ats/careersite/search.aspx', 'http://www.mvcc.edu'],
['Mohawk Valley Community College-Rome Campus', 'http://mvcc.csod.com/ats/careersite/search.aspx', 'http://www.mvcc.edu'],
['Monroe Community College', 'http://monroecc.interviewexchange.com/static/clients/547MCM1/index.jsp', 'http://www.monroecc.edu/'],
['Monroe Community College - Downtown Campus', 'http://monroecc.interviewexchange.com/static/clients/547MCM1/index.jsp', 'http://www.monroecc.edu/downtown'],
['Nassau Community College', 'http://ncc.interviewexchange.com/static/clients/489NCM1/index.jsp', 'http://www.ncc.edu'],
['New York State College of Agriculture And Life Sciences at Cornell', 'http://hr.cornell.edu/jobs', 'http://cals.cornell.edu/'],
['New York State College of Human Ecology at Cornell University', 'http://hr.cornell.edu/jobs', 'http://www.human.cornell.edu'],
['New York State College of Veterinary Medicine at Cornell University', 'http://hr.cornell.edu/jobs', 'http://www.vet.cornell.edu/'],
['New York State School of Industrial And Labor Relations at Cornell', 'http://hr.cornell.edu/jobs', 'http://www.ilr.cornell.edu'],
['Niagara County Community College', 'http://niagaracc-suny.peopleadmin.com/', 'http://niagaracc.suny.edu'],
['North Country Community College', 'http://www.nccc.edu/careers-2', 'http://www.nccc.edu'],
['North Country Community College-Elizabethtown Campus', 'http://www.nccc.edu/careers-2', 'http://www.nccc.edu'],
['North Country Community College-Malone Campus', 'http://www.nccc.edu/careers-2', 'http://www.nccc.edu'],
['North Country Community College-Ticonderoga Campus', 'http://www.nccc.edu/careers-2', 'http://www.nccc.edu'],
['NYS College of Ceramics at Alfred University', 'http://alfredstate.interviewexchange.com/static/clients/481ASM1/index.jsp', 'http://www.alfred.edu'],
['Onondaga Community College', 'http://sunyocc.peopleadmin.com/postings/search', 'http://www.sunyocc.edu'],
['Orange County Comm College - Newburgh', 'http://occc.interviewexchange.com/static/clients/437SOM1/index.jsp', 'http://www.sunyorange.edu'],
['Orange County Community College', 'http://occc.interviewexchange.com/static/clients/437SOM1/index.jsp', 'http://www.sunyorange.edu'],
['Rockland Community College', 'http://www.sunyrockland.edu/about/careers-jobs', 'http://www.sunyrockland.edu'],
['Schenectady County Community College', 'http://sunysccc.edu/About-Us/Office-of-Human-Resources/Employment-Opportunities', 'http://sunysccc.edu'],
['State University College at Plattsburgh', 'http://jobs.plattsburgh.edu/postings/search', 'http://www.plattsburgh.edu'],
['State University College of Oswego - Metro Center', 'http://oswego.interviewexchange.com/static/clients/313OSM1/index.jsp', 'http://www.oswego.edu/syracuse/'],
['State University of New York at Albany', 'http://albany.interviewexchange.com/jobsearchfrm.jsp', 'http://www.albany.edu'],
['State University of New York at Binghamton', 'http://www.binghamton.edu/human-resources/employment-opportunities/index.html', 'http://www.binghamton.edu'],
['State University of New York at Buffalo', 'http://www.ubjobs.buffalo.edu', 'http://www.buffalo.edu'],
['State University of New York at Stony Brook', 'http://www.stonybrookmedicine.edu/careers', 'http://www.stonybrook.edu'],
['State University of New York College at Brockport', 'http://www.brockport.edu/support/human_resources/empop/vacancies', 'http://www.brockport.edu'],
['State University of New York College at Buffalo', 'http://jobs.buffalostate.edu', 'http://suny.buffalostate.edu'],
['State University of New York College at Cortland', 'http://jobs.cortland.edu', 'http://www2.cortland.edu'],
['State University of New York College at Fredonia', 'http://fredonia.interviewexchange.com/static/clients/471SFM1/index.jsp', 'http://www.fredonia.edu'],
['State University of New York College at Geneseo', 'http://jobs.geneseo.edu/postings/search', 'http://www.geneseo.edu'],
['State University of New York College at New Paltz', 'http://www.newpaltz.edu/hr/jobs.html', 'http://www.newpaltz.edu'],
['State University of New York College at Old Westbury', 'http://oldwestbury.interviewexchange.com/static/clients/519OWM1/index.jsp', 'http://www.oldwestbury.edu'],
['State University of New York College at Oneonta', 'http://suny.oneonta.edu/sponsored-programs/employment-opportunities', 'http://www.oneonta.edu'],
['State University of New York College at Oswego', 'http://oswego.interviewexchange.com/static/clients/313OSM1/index.jsp', 'http://www.oswego.edu'],
['State University of New York College at Potsdam', 'http://employment.potsdam.edu/postings/search', 'http://www.potsdam.edu'],
['State University of New York College at Purchase', 'http://jobs.purchase.edu/applicants/jsp/shared/frameset/Frameset.jsp', 'http://www.purchase.edu'],
['State University of New York College of Environmental Science And Forestry', 'http://esf.interviewexchange.com/static/clients/444ESM1/index.jsp', 'http://www.esf.edu'],
['State University of New York College of Optometry', 'http://sunyopt.peopleadmin.com/postings/search', 'http://www.sunyopt.edu'],
['State University of New York College of Technology at Delhi', 'http://delhi.interviewexchange.com/static/clients/409SDM1/index.jsp', 'http://www.delhi.edu'],
['State University of New York Empire State College', 'http://www.esc.edu/human-resources/employment-opportunities', 'http://www.esc.edu'],
['State University of New York Health Science Center at Brooklyn', 'http://www.downstate.edu/human_resources/links.html', 'http://www.downstate.edu/'],
['State University of New York Health Science Center at Syracuse', 'http://jobsatupstate.peopleadmin.com/applicants/jsp/shared/Welcome_css.jsp', 'http://www.upstate.edu/'],
['State University of New York System Administration', 'http://www.suny.edu/careers/employment/index.cfm?s=y', 'http://www.suny.edu'],
['SUC at Plattsburgh at Adirondack Community College', 'http://jobs.plattsburgh.edu/postings/search', 'http://www.plattsburgh.edu/'],
['Suffolk County Community College', 'http://www3.sunysuffolk.edu/About/Employment.asp', 'http://www.sunysuffolk.edu'],
['Suffolk County Community College Eastern Campus', 'http://www3.sunysuffolk.edu/About/Employment.asp', 'http://www.sunysuffolk.edu'],
['Suffolk County Community College Western Campus', 'http://www3.sunysuffolk.edu/About/Employment.asp', 'http://www.sunysuffolk.edu'],
['Sullivan County Community College', 'http://sunysullivan.edu/offices/associate-vp-for-planning-human-resources-facilities/job-opportunities', 'http://www.sunysullivan.edu'],
['SUNY Coll of Ag & Tech at Delhi - Sccc', 'http://delhi.interviewexchange.com/static/clients/409SDM1/index.jsp', 'http://www.delhi.edu'],
['SUNY College of  Agriculture And Technology at Morrisville', 'http://www.morrisville.edu/contact/offices/human-resources/employment-opportunities', 'http://www.morrisville.edu'],
['SUNY College of  Technology at Alfred Wellsville Campus', 'http://alfredstate.interviewexchange.com/static/clients/481ASM1/index.jsp', 'http://www.alfredstate.edu'],
['SUNY College of Agriculture And Technology at Cobleskill', 'http://cobleskill.interviewexchange.com/static/clients/474SCM1/index.jsp', 'http://www.cobleskill.edu'],
['SUNY College of Agriculture And Technology at Morrisville - Norwich Campus', 'http://www.morrisville.edu/contact/offices/human-resources/employment-opportunities', 'http://www.morrisville.edu/norwich'],
['SUNY College of Technology at Alfred', 'http://alfredstate.interviewexchange.com/static/clients/481ASM1/index.jsp', 'http://www.alfredstate.edu'],
['SUNY College of Technology at Canton', 'http://www.canton.edu/hr/job_opportunities.html', 'http://www.canton.edu/'],
['SUNY College of Technology at Farmingdale', 'http://farmingdale.interviewexchange.com/static/clients/383FAM1/index.jsp', 'http://www.farmingdale.edu'],
['SUNY Maritime College', 'http://maritime.interviewexchange.com/static/clients/373SMM1/index.jsp', 'http://www.sunymaritime.edu'],
['SUNY Polytechnic Institute', 'http://sunypoly.interviewexchange.com/static/clients/511SPM1/hiring.jsp', 'http://www.sunypoly.edu'],
['Tompkins Cortland Community College', 'http://www.tompkinscortland.edu/academics/programs/human-services', 'http://www.tc3.edu'],
['Ulster County Community College', 'http://www.sunyulster.edu/campus_and_culture/about_us/jobs.php', 'http://www.sunyulster.edu'],
['Westchester Community College', 'http://www.sunywcc.edu/about/jobshuman-resources', 'http://www.sunywcc.edu/'],
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
    #if ii[3] == (0.0, 0.0):
        #count += 1
        #print('\n' + str(ii) + ',')


    # Display all entries
    print(str(ii) + ',')
    


print('\nMissing:', count, '\nTotal entries:', len(db))













