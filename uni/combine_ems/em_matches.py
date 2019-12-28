
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

['Academy For Jewish Religion', 'http://ajrsem.org', (40.9364060697, -73.898634461)],
['Adelphi University', 'http://www.adelphi.edu', (40.7222430099, -73.6510515826)],
['Albany College of Pharmacy And Health Sciences', 'http://www.acphs.edu', (42.6521801281, -73.7785803492)],
['Albany Law School', 'http://www.albanylaw.edu', (42.6500456455, -73.7775088575)],
['Albany Medical College', 'http://www.amc.edu', (42.6532407287, -73.7739752764)],
['Alfred University', 'http://www.alfred.edu', (42.2561789656, -77.7882588252)],
['Amer Academy of Dramatic Arts', 'http://www.aada.edu', (40.7455070816, -73.9847588977)],
['American Acad McAllister Inst', 'http://www.funeraleducation.org', (40.7689206361, -73.9938294193)],
['Bank Street College of Education', 'http://www.bankstreet.edu', (40.805678904, -73.966576371)],
['Bard College', 'http://www.bard.edu', (42.0212190417, -73.9065792655)],
['Bard College at Brooklyn Public Central Library', 'http://bpi.bard.edu', (40.672385107, -73.9681647537)],
['Bard Grad Ctr For Decorative Arts', 'http://www.bgc.bard.edu', (40.7856118202, -73.9705318395)],
['Barnard College', 'http://www.barnard.edu', (40.8088109366, -73.9635231179)],
['Boricua College', 'http://www.boricuacollege.edu', (40.8333897817, -73.9456977179)],
['Boricua College - Bronx', 'http://www.boricuacollege.edu', (40.823585313, -73.9110466197)],
['Boricua College - Brooklyn', 'http://www.boricuacollege.edu', (40.7167069894, -73.9576172706)],
['Brooklyn Law School', 'http://www.brooklaw.edu', (40.6921576493, -73.9898297028)],
['Canisius College', 'http://www.canisius.edu/', (42.9255866422, -78.8534827977)],
['Cazenovia College', 'http://www.cazenovia.edu', (42.9318683477, -75.8540739167)],
['Christ the King Seminary', 'http://www.cks.edu', (42.7766998662, -78.6566123121)],
['City Seminary of New York Graduate Center', 'http://www.cityseminaryny.org', (40.7390307143, -73.9668120498)],
['Clarkson University', 'http://www.clarkson.edu/', (44.6668978047, -74.9941051289)],
['Clarkson University Capital Region', 'http://www.clarkson.edu', (42.8138873062, -73.9341950475)],
['Cochran Sch Nursing St John Rvrdl Ho', 'http://www.cochranschoolofnursing.us', (40.9687964271, -73.8863259432)],
['Cold Spring Harbor--watson School of Biological Sciences', 'http://www.cshl.edu/gradschool', (40.8611650109, -73.4691350824)],
['Colgate University', 'http://www.colgate.edu', (42.8165164934, -75.5325655086)],
['Colgate-Rochester Divinity School', 'http://www.crcds.edu', (43.1321158158, -77.6000675596)],
['Coll New Rochelle Dist Coun 31 Cmps', 'http://www.cnr.edu', (40.7147732989, -74.0128284296)],
['Coll New Rochelle Rosa Parks Campus', 'http://www.cnr.edu', (40.8084367094, -73.947492888)],
['Coll of New Rochelle at NY Theo Semi', 'http://www.cnr.edu', (40.7457240089, -73.9875609033)],
['Coll of New Rochelle Brooklyn Campus', 'http://www.cnr.edu', (40.6800585075, -73.9458815453)],
['College of Mt St Vincent', 'http://www.mountsaintvincent.edu', (40.9136881584, -73.9087379397)],
['College of New Rochelle', 'http://www.cnr.edu', (40.901372521, -73.7815964899)],
["College of New Rochelle John Cardinal O'Connor Campus", 'http://www.cnr.edu', (40.8166075558, -73.9203497842)],
['College of Saint Rose', 'http://www.strose.edu', (42.6646075556, -73.7860610659)],
['Columbia University', 'http://www.columbia.edu', (40.8079890307, -73.9620177274)],
['Concordia College', 'http://www.concordia-ny.edu', (40.9425657208, -73.8207636546)],
['Cooper Union For the Advancement of Science And Art', 'http://www.cooper.edu', (40.7280657627, -73.9914604017)],
['Cornell Univ Medical Campus', 'http://www.weill.cornell.edu', (40.7648896034, -73.9549391409)],
['Cornell University', 'http://www.cornell.edu', (42.4470150296, -76.4823949559)],
['Cornell University - Cornellnyc Tech Campus', 'http://tech.cornell.edu', (0.0, 0.0)],
['Crouse-Irving Memorial Hospital School of Nursing', 'http://www.crouse.org/nursing', (43.0409937183, -76.1379398537)],
['Culinary Institute of America 697', 'http://www.ciachef.edu', (41.745751189, -73.9331335732)],
["D'Youville College", 'http://www.dyc.edu', (42.9022574547, -78.8904776633)],
['Daemen College', 'http://www.daemen.edu', (42.9640165422, -78.7899685237)],
['Davis College', 'http://www.davisny.edu', (0.0, 0.0)],
['Dominican Coll of Blauvelt', 'http://www.dc.edu', (41.0512617261, -73.9527385505)],
['Dowling College', 'http://www.dowling.edu', (40.7415915528, -73.1474167819)],
['Dowling College - Brookhaven Center', 'http://www.dowling.edu', (40.8278969864, -72.8819429176)],
['Elim Bible Institute & College', 'http://www.elim.edu', (42.908518804, -77.6147357204)],
['Ellis Medicine-Thebelanger School of Nursing', 'http://www.ellisbelangerschoolofnursing.org', (42.8055884888, -73.9168545562)],
['Elmira College', 'http://www.elmira.edu', (42.1196260543, -76.8231759498)],
['Elyon College', 'http://www.elyon.edu', (40.6110547033, -73.9804759397)],
['Excelsior College', 'http://www.excelsior.edu/', (42.705436733, -73.8630575803)],
['The Elmezzi Graduate School of Molecular Medicine', 'http://www.elmezzigraduateschool.org/', (40.7819201717, -73.7039516746)],
['Fei Tian College', 'http://www.feitian.edu', (41.4529346524, -74.5891858298)],
['Finger Lakes Health College of Nursing & Health Sciences', 'http://www.flhcon.edu', (42.8762578081, -76.9876894515)],
['Fordham Univ (Rose Hill-Lincoln Ctr)', 'http://www.fordham.edu', (40.8611039429, -73.8875646756)],
['Fordham University - Westchester Campus', 'http://www.fordham.edu', (41.0292387951, -73.7288980026)],
['Gamla College', 'http://gamlacollege.com', (40.6171572317, -73.9621890813)],
['General Theological Seminary', 'http://www.gts.edu', (40.7456283873, -74.0036644478)],
['Glasgow Caledonian New York College', 'http://www.gcnyc.com', (40.7390307143, -73.9668120498)],
['Hamilton College', 'http://www.hamilton.edu', (43.0514413048, -75.402117956)],
['Hartwick College', 'http://www.hartwick.edu', (42.4610282773, -75.0701668682)],
['Hebrew Union College - Jewish Institute of Religion', 'http://www.huc.edu', (40.7288012661, -73.9948235492)],
['Helene Fuld College of Nursing', 'http://www.helenefuld.edu', (40.8028611543, -73.9438474104)],
['Hilbert College', 'http://www.hilbert.edu', (42.7548232015, -78.8245211425)],
['Hobart & Wm Smith Colleges', 'http://www.hws.edu', (42.8589157462, -76.9858302479)],
['Hofstra University-Main Campus', 'http://www.hofstra.edu', (40.7163803809, -73.5995207899)],
['Holy Trinity Orthodox Seminary', 'http://www.hts.edu', (42.9277195844, -74.9336856615)],
['Houghton College', 'http://www.houghton.edu', (42.4280063974, -78.1547581109)],
['Inst of Design & Construction', 'http://www.idc.edu', (40.6921634518, -73.9830600399)],
['Iona College', 'http://www.iona.edu', (40.9252432042, -73.7882413524)],
['Iona College Rockland Campus', 'http://www.iona.edu/rockland/', (41.0485317405, -73.9525586308)],
['Ithaca College', 'http://www.ithaca.edu', (42.4221514807, -76.5000368308)],
['Jewish Theological Semnry of America', 'http://www.jtsa.edu', (40.8118490724, -73.9606737505)],
['The Juilliard School', 'http://www.juilliard.edu/', (40.7733956594, -73.9828002776)],
['Keuka College', 'http://www.keuka.edu', (42.6151105935, -77.0906192216)],
['Keuka College-Corning CC Campus', 'http://www.keuka.edu', (42.1166659128, -77.071690501)],
['Keuka-Onondaga Community College Branch', 'http://www.keuka.edu', (43.0061837356, -76.1981302617)],
["The King's College", 'http://www.tkc.edu', (40.7634337245, -73.9287215064)],
['Le Moyne College', 'http://www.lemoyne.edu', (43.0491913085, -76.0848876812)],
['Long Island College Hospital Sch Nursing', '', (40.6830878574, -74.0000432328)],
['Long Island College Hospital School of Nursing', 'http://www.futurenurselich.org', (40.6908534019, -73.9977410887)],
['Long Island University - New York University Campus', 'http://www.liu.edu', (40.7294899346, -73.9972596293)],
['Long Island University - Riverhead', 'http://www.liu.edu', (40.8766617264, -72.7002490474)],
['Long Island University Central Administration', 'http://www.liu.edu', (40.8126010433, -73.6167466338)],
['Long Island University-Brentwood Campus', 'http://liu.edu/brentwood', (40.8029993911, -73.285274135)],
['Long Island University-Brooklyn Campus', 'http://www.liu.edu', (40.6916867462, -73.9814831539)],
['Long Island University-CW Post Campus', 'http://www.liu.edu', (40.8126541126, -73.616525216)],
['Long Island University-Southampton Campus', 'http://www.liu.edu', (40.8853530054, -72.478100023)],
['Long Island University-Westchester Campus', 'http://www.liu.edu', (41.039038225, -73.6962345232)],
['Louis V. Gerstner Grad Scho of Biomed Sci, Memorial Sloan-Kettering Cancer Center', 'http://www.sloankettering.edu', (40.7640369956, -73.9560230672)],
['Manhattan College', 'http://www.manhattan.edu', (40.890237552, -73.9012322052)],
['Manhattan School of Music', 'http://msmnyc.edu', (40.8124890622, -73.9617394867)],
['Manhattanville College', 'http://www.mville.edu', (41.0310593009, -73.7148083319)],
['Maria College of Albany', 'http://www.mariacollege.edu', (42.6583265456, -73.8076581449)],
['Marist College', 'http://www.marist.edu', (41.7233294164, -73.9320898598)],
['Marymount Manhattan College', 'http://www.mmm.edu', (40.7686329247, -73.9598045844)],
['Medaille College', 'http://www.medaille.edu', (42.9296313432, -78.8552047502)],
['Medaille College - Rochester Campus', 'http://www.medaille.edu', (43.1086317223, -77.5720499965)],
['Memorial Hospital School of Nursing', 'http://www.sphp.com/sons', (42.6741639047, -73.7486829022)],
['Mercy College', 'http://www.mercy.edu', (41.0213716724, -73.8699690554)],
['Mercy College - Manhattan Campus', 'http://www.mercy.edu', (40.7501618927, -73.9868612518)],
['Mercy College Bronx Campus', 'http://www.mercy.edu', (40.8524534315, -73.8378911685)],
['Mercy College-Yorktown Hts Campus', 'http://www.mercy.edu', (41.2944448671, -73.8191852919)],
['Metropolitan College of New York', 'http://www.mcny.edu', (40.7088727965, -74.0147720915)],
['Metropolitan College of Ny-Brc', 'http://www.mcny.edu/mcny-bronx/', (40.8153862021, -73.9158630335)],
['Mid-America Baptist Theol Seminary - NE Branch', 'http://www.mabtsne.edu', (42.7513005326, -73.9177628057)],
['Molloy College', 'http://www.molloy.edu', (40.6811769793, -73.628967714)],
['Montefiore School of Nursing', 'http://www.montefiorehealthsystem.org', (40.91208021, -73.8404194)],
['Mount Saint Mary College', 'http://www.msmc.edu', (41.513007242, -74.0147427736)],
['Mt Sinai School of Medicine', 'http://icahn.mssm.edu', (40.7903736896, -73.9533895103)],
['Nazareth College of Rochester', 'http://www.naz.edu', (43.1039850232, -77.5234477002)],
['New School University - NYS Office of Mental Health', 'http://www.newschool.edu/', (42.6478465136, -73.774182006)],
['New York College of Health Professions', 'http://www.nycollege.edu', (40.8100017735, -73.5169487481)],
['New York College of Podiatric Medicine', 'http://www.nycpm.edu', (40.8049396848, -73.9406042039)],
['New York College of Traditional Chinese Medicine', 'http://www.nyctcm.edu', (40.7394968641, -73.6388842048)],
['New York Graduate School of Psychoanalysis', 'http://www.nygsp.bgsp.edu/', (40.7337598681, -73.9965400551)],
['New York Institute For Technology-Manhattan Campus', 'http://www.nyit.edu', (40.7696286804, -73.982398747)],
['New York Institute of Technology - Islip Campus', 'http://www.nyit.edu', (40.790602046, -73.202009032)],
['New York Institute of Technology Old Westbury Campus', 'http://www.nyit.edu', (40.8101610875, -73.6032821778)],
['New York Law School', 'http://www.nyls.edu', (40.7180828612, -74.0071048348)],
['New York Studio School', 'http://www.nyss.org', (40.7325102354, -73.9972369615)],
['New York Theological Seminary', 'http://www.nyts.edu', (40.810939099, -73.9640163243)],
['New York University', 'http://www.nyu.edu', (40.7296504349, -73.9970161424)],
['New York University - St. Thomas Aquinas College', 'http://www.nyu.edu', (41.0420416981, -73.9364386301)],
['New York University at Manhattanville College', 'http://www.nyu.edu', (41.0310593009, -73.7148083319)],
['Niagara University', 'http://www.niagara.edu', (43.1371098129, -79.0380449288)],
['Northeaster Seminary at Roberts Wesleyan College', 'http://www.nes.edu/', (43.1260918496, -77.7974158143)],
['NY Chiropractic College', 'http://www.nycc.edu', (42.9114587441, -76.7538967241)],
['NY Medical College', 'http://www.nymc.edu', (41.08500151, -73.81006245)],
['NY School of Interior Design', 'http://www.nysid.edu', (40.7686703487, -73.9623794411)],
['Nyack College', 'http://www.nyack.edu', (41.0861216895, -73.9300085756)],
['The New School', 'http://www.newschool.edu/', (40.73557935, -73.9969989)],
['The New York Academy of Art', 'http://www.nyaa.edu', (40.7184411618, -74.0059019288)],
['Pace University - NYC Campus', 'http://www.pace.edu', (40.7116591422, -74.0054227605)],
['Pace University College at White Plains', 'http://www.pace.edu', (41.0395773844, -73.766694506)],
['Pace University Pleasantville', 'http://www.pace.edu', (41.1284649279, -73.80838717)],
['Paul Smiths College', 'http://www.paulsmiths.edu', (44.4373167524, -74.2529946064)],
['Phillips Beth Israel Sch of Nursing', 'http://www.pson.edu', (40.7448494113, -73.9912907691)],
['Polytechnic Inst of NY - Westchester Campus', 'http://www.poly.edu/', (41.0939312216, -73.8147736623)],
['Polytechnic Institute of NY - Main Campus', 'http://www.poly.edu/', (40.6943573162, -73.9864574955)],
['Polytechnic Institute of NYU - Long Island Center', 'http://www.poly.edu/', (40.7726011592, -73.4129140464)],
['Pratt Institute', 'http://www.pratt.edu', (40.6918957425, -73.9639616366)],
['Pratt Institute Manhattan Center', 'http://www.pratt.edu', (40.7380983369, -73.9990084787)],
['Professional Business College', 'http://www.pbcny.edu', (40.7189568257, -74.0020664246)],
['Rabbi Isaac Elchanan Theo Seminary', 'http://www.yu.edu/riets/', (40.8515810832, -73.9285990394)],
['Relay School of Education', 'http://www.relay.edu', (40.7405456779, -73.9932910229)],
['Rensselaer Polytech Institute', 'http://www.rpi.edu', (42.7296105935, -73.6802067256)],
['Roberts Wesleyan College', 'http://www.roberts.edu', (43.1256048122, -77.8013082192)],
['Rochester Institute of Technology', 'http://www.rit.edu', (43.0847578962, -77.6753621235)],
['Rockefeller University', 'http://www.rockefeller.edu/', (40.7629956519, -73.9564672926)],
["Saint Joseph's Seminary And College", 'http://dunwoodie.edu/', (40.9201600754, -73.8630100825)],
['Saint Lawrence University', 'http://www.stlawu.edu', (44.5883474893, -75.1598172519)],
['Salvation Army College For Officer Training', 'http://www.tsacfotny.edu', (41.1137143951, -74.1407862011)],
['Samaritan Hospital School of Nursing', 'http://sphp.com/son', (42.74282684, -73.67644282)],
['Sarah Lawrence College', 'http://www.sarahlawrence.edu', (40.9354310286, -73.8436968994)],
['Siena College', 'http://www.siena.edu/', (42.717915027, -73.7553350204)],
['Skidmore College', 'http://www.skidmore.edu', (43.094951787, -73.7800194799)],
['St Bonaventure University', 'http://www.sbu.edu', (42.0795050049, -78.4849799242)],
['St Elizabeth Hospital College of Nursing', 'http://www.secon.edu', (43.0834478231, -75.2674174685)],
['St Francis College', 'http://www.sfc.edu', (40.6932834665, -73.9920614542)],
['St John Fisher College', 'http://www.sjfc.edu', (43.1175935637, -77.5166739799)],
['St Johns University-Staten Island', 'http://www.stjohns.edu', (40.6221249432, -74.089553458)],
["St Joseph's College", 'http://www.sjcny.edu', (40.6903589538, -73.9679493284)],
["St Joseph's College - Suffolk Campus", 'http://www.sjcny.edu', (40.7746849948, -73.0233178286)],
["St Joseph's College of Nursing at St Joseph's Hospital Health Center", 'http://www.sjhcon.edu/', (43.0547501798, -76.1484215884)],
['St Thomas Aquinas College', 'http://www.stac.edu', (41.0420293949, -73.9384034211)],
["St Vladimir's Orthodox Theol Seminry", 'http://www.svots.edu/', (40.96988799, -73.82415561)],
["St. Bernard's School of Theology And Ministry", 'http://www.stbernards.edu', (43.1021829757, -77.5264984514)],
["St. John's University", 'http://www.stjohns.edu', (40.7256720182, -73.7918247118)],
["St. John's University - Manhattan Branch", 'http://www.stjohns.edu', (40.7300709717, -73.992834118)],
["St. Joseph's Seminary & College-Douglaston", 'http://cathedralseminary.org/', (40.74636212, -73.73310234)],
["St. Joseph's Seminary & College-Huntington", 'http://www.icseminary.edu', (40.90515869, -73.47090101)],
["St. Joseph's Seminary & College-Somers", '', (0.0, 0.0)],
['Syracuse University', 'http://syracuse.edu', (43.0402401915, -76.1369455708)],
['The Sage Colleges', 'http://www.sage.edu', (42.7282013924, -73.6937086081)],
['The Sage Colleges -  Albany Campus', 'http://www.sage.edu', (42.6527156078, -73.7831997513)],
['Teachers College', 'http://www.tc.columbia.edu/', (40.8100945923, -73.9606417774)],
['Touro College', 'http://www.touro.edu', (40.75313425, -73.98929738)],
['Touro College', 'http://tourocom.touro.edu/about-us/contact', (40.75313425, -73.98929738)],
['Touro College - Bayshore', 'http://www.touro.edu', (40.7244854646, -73.2513380684)],
['Touro College - Flatbush', 'http://www.touro.edu', (40.6251624576, -73.9599657735)],
['Touro College - Harlem', 'http://www.touro.edu', (40.8015644265, -73.9351031801)],
['Touro College - Kew Gardens', 'http://www.touro.edu', (40.7248816812, -73.8158841816)],
['Touro College - Valhalla', 'http://dental.touro.edu/', (41.0853086341, -73.8175326375)],
['Touro College-Central Islip', 'http://www.touro.edu', (40.76197743, -73.1876853439)],
['Trocaire College', 'http://www.trocaire.edu', (42.8467543251, -78.8119072161)],
['Unification Theological Seminary', 'http://uts.edu/', (0.0, 0.0)],
['Union College', 'http://www.union.edu', (42.8175712882, -73.9285185308)],
['Union Graduate College', 'http://www.uniongraduatecollege.edu', (42.8135812884, -73.9344484824)],
['Union Theological Seminary', 'http://www.utsnyc.edu', (40.8112300852, -73.961898663)],
['University of Rochester', 'http://www.rochester.edu', (43.1263561927, -77.6311742772)],
['Utica College', 'http://www.utica.edu', (43.0970213153, -75.2706579866)],
['Vassar College', 'http://www.vassar.edu', (41.6865376709, -73.897705087)],
['Vaughn College of Aeronautics And Technology', 'http://www.vaughn.edu', (40.7786150523, -73.839777103)],
['Villa Maria College of Buffalo', 'http://www.villa.edu/', (42.9127511236, -78.7971828612)],
['Wagner College', 'http://www.wagner.edu/', (40.6149084222, -74.0942924431)],
['Webb Insttitute', 'http://www.webb.edu', (40.8826862651, -73.6462725744)],
['Wells College', 'http://www.wells.edu', (42.7436626701, -76.6992195176)],
['Yeshiva University', 'http://www.yu.edu', (40.8506479647, -73.9298665465)]

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











