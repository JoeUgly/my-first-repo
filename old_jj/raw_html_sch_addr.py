

# Desc: get school addresses from website and add to grudb



# http://www.nysed.gov/admin/admindex.html





html = '''
<A HREF="660413/660413.html">Abbott UFSD</A><BR>
<A HREF="570101/570101.html">Addison CSD</A><BR>
<A HREF="410401/410401.html">Adirondack CSD</A><BR>
<A HREF="080101/080101.html">Afton CSD</A><BR>
<A HREF="142101/142101.html">Akron CSD</A><BR>
<A HREF="010100/010100.html">Albany City SD</A><BR>
<A HREF="450101/450101.html">Albion CSD</A><BR>
<A HREF="140101/140101.html">Alden CSD</A><BR>
<A HREF="180202/180202.html">Alexander CSD</A><BR>
<A HREF="220202/220202.html">Alexandria CSD</A><BR>
<A HREF="020101/020101.html">Alfred-Almond CSD</A><BR>
<A HREF="040302/040302.html">Allegany-Limestone CSD</A><BR>
<A HREF="460102/460102.html">Altmar-Parish-Williamstown CSD</A><BR>
<A HREF="580303/580303.html">Amagansett UFSD</A><BR>
<A HREF="140201/140201.html">Amherst CSD</A><BR>
<A HREF="580106/580106.html">Amityville UFSD</A><BR>
<A HREF="270100/270100.html">Amsterdam City SD</A><BR>
<A HREF="120102/120102.html">Andes CSD</A><BR>
<A HREF="020601/020601.html">Andover CSD</A><BR>
<A HREF="660405/660405.html">Ardsley UFSD</A><BR>
<A HREF="640101/640101.html">Argyle CSD</A><BR>
<A HREF="571901/571901.html">Arkport CSD</A><BR>
<A HREF="131601/131601.html">Arlington CSD</A><BR>
<A HREF="670201/670201.html">Attica CSD</A><BR>
<A HREF="050100/050100.html">Auburn City SD</A><BR>
<A HREF="090201/090201.html">Ausable Valley CSD</A><BR>
<A HREF="491302/491302.html">Averill Park CSD</A><BR>
<A HREF="570201/570201.html">Avoca CSD</A><BR>
<A HREF="240101/240101.html">Avon CSD</A><BR>



<HR>
<FONT size=+3><A NAME="BLIST">B</A><BR></FONT>
<A HREF="580101/580101.html">Babylon UFSD</A><BR>
<A HREF="080201/080201.html">Bainbridge-Guilford CSD</A><BR>
<A HREF="280210/280210.html">Baldwin UFSD</A><BR>
<A HREF="420901/420901.html">Baldwinsville CSD</A><BR>
<A HREF="521301/521301.html">Ballston Spa CSD</A><BR>
<A HREF="401301/401301.html">Barker CSD</A><BR>
<A HREF="180300/180300.html">Batavia City SD</A><BR>
<A HREF="570302/570302.html">Bath CSD</A><BR>
<A HREF="580501/580501.html">Bay Shore UFSD</A><BR>
<A HREF="580505/580505.html">Bayport-Blue Point UFSD</A><BR>
<A HREF="130200/130200.html">Beacon City SD</A><BR>
<A HREF="231301/231301.html">Beaver River CSD</A><BR>
<A HREF="660102/660102.html">Bedford CSD</A><BR>
<A HREF="090301/090301.html">Beekmantown CSD</A><BR>
<A HREF="020801/020801.html">Belfast CSD</A><BR>
<A HREF="220909/220909.html">Belleville-Henderson CSD</A><BR>
<A HREF="280207/280207.html">Bellmore UFSD</A><BR>
<A HREF="280253/280253.html">Bellmore-Merrick Central HS District</A><BR>
<A HREF="061001/061001.html">Bemus Point CSD</A><BR>
<A HREF="100308/100308.html">Berkshire UFSD</A><BR>
<A HREF="490101/490101.html">Berlin CSD</A><BR>
<A HREF="010201/010201.html">Berne-Knox-Westerlo CSD</A><BR>
<A HREF="010306/010306.html">Bethlehem CSD</A><BR>
<A HREF="280521/280521.html">Bethpage UFSD</A><BR>
<A HREF="030200/030200.html">Binghamton City SD</A><BR>
<A HREF="661905/661905.html">Blind Brook-Rye UFSD</A><BR>
<A HREF="022902/022902.html">Bolivar-Richburg CSD</A><BR>
<A HREF="630101/630101.html">Bolton CSD</A><BR>
<A HREF="151801/151801.html">Boquet Valley CSD</A><BR>
<A HREF="570401/570401.html">Bradford CSD</A><BR>
<A HREF="510101/510101.html">Brasher Falls CSD</A><BR>
<A HREF="580512/580512.html">Brentwood UFSD</A><BR>
<A HREF="480601/480601.html">Brewster CSD</A><BR>
<A HREF="661402/661402.html">Briarcliff Manor UFSD</A><BR>
<A HREF="580909/580909.html">Bridgehampton UFSD</A><BR>
<A HREF="260101/260101.html">Brighton CSD</A><BR>
<A HREF="171102/171102.html">Broadalbin-Perth CSD</A><BR>
<A HREF="261801/261801.html">Brockport CSD</A><BR>
<A HREF="062301/062301.html">Brocton CSD</A><BR>
<A HREF="660303/660303.html">Bronxville UFSD</A><BR>
<A HREF="250109/250109.html">Brookfield CSD</A><BR>
<A HREF="580203/580203.html">Brookhaven-Comsewogue UFSD</A><BR>
<A HREF="039000/039000.html">Broome-Delaware-Tioga Boces</A><BR>
<A HREF="490202/490202.html">Brunswick CSD (Brittonkill)</A><BR>
<A HREF="161601/161601.html">Brushton-Moira CSD</A><BR>
<A HREF="140600/140600.html">Buffalo City SD</A><BR>
<A HREF="520101/520101.html">Burnt Hills-Ballston Lake CSD</A><BR>
<A HREF="661201/661201.html">Byram Hills CSD</A><BR>
<A HREF="180701/180701.html">Byron-Bergen CSD</A><BR>



<HR>
<FONT size=+3><A NAME="CLIST">C</A><BR></FONT>
<A HREF="190301/190301.html">Cairo-Durham CSD</A><BR>
<A HREF="240201/240201.html">Caledonia-Mumford CSD</A><BR>
<A HREF="641610/641610.html">Cambridge CSD</A><BR>
<A HREF="410601/410601.html">Camden CSD</A><BR>
<A HREF="570603/570603.html">Campbell-Savona CSD</A><BR>
<A HREF="270301/270301.html">Canajoharie CSD</A><BR>
<A HREF="430300/430300.html">Canandaigua City SD</A><BR>
<A HREF="021102/021102.html">Canaseraga CSD</A><BR>
<A HREF="250901/250901.html">Canastota CSD</A><BR>
<A HREF="600301/600301.html">Candor CSD</A><BR>
<A HREF="571502/571502.html">Canisteo-Greenwood CSD</A><BR>
<A HREF="510201/510201.html">Canton CSD</A><BR>
<A HREF="019000/019000.html">Capital Region Boces</A><BR>
<A HREF="280411/280411.html">Carle Place UFSD</A><BR>
<A HREF="480102/480102.html">Carmel CSD</A><BR>
<A HREF="222201/222201.html">Carthage CSD</A><BR>
<A HREF="060401/060401.html">Cassadaga Valley CSD</A><BR>
<A HREF="050401/050401.html">Cato-Meridian CSD</A><BR>
<A HREF="190401/190401.html">Catskill CSD</A><BR>
<A HREF="049000/049000.html">Cattar-Allegany-Erie-Wyoming Boces</A><BR>
<A HREF="042302/042302.html">Cattaraugus-Little Valley CSD</A><BR>
<A HREF="059000/059000.html">Cayuga-Onondaga Boces</A><BR>
<A HREF="250201/250201.html">Cazenovia CSD</A><BR>
<A HREF="580233/580233.html">Center Moriches UFSD</A><BR>
<A HREF="580513/580513.html">Central Islip UFSD</A><BR>
<A HREF="460801/460801.html">Central Square CSD</A><BR>
<A HREF="212101/212101.html">Central Valley CSD At Ilion-Mohawk</A><BR>
<A HREF="661004/661004.html">Chappaqua CSD</A><BR>
<A HREF="120401/120401.html">Charlotte Valley CSD</A><BR>
<A HREF="160801/160801.html">Chateaugay CSD</A><BR>
<A HREF="101001/101001.html">Chatham CSD</A><BR>
<A HREF="060503/060503.html">Chautauqua Lake CSD</A><BR>
<A HREF="090601/090601.html">Chazy UFSD</A><BR>
<A HREF="140701/140701.html">Cheektowaga CSD</A><BR>
<A HREF="140702/140702.html">Cheektowaga-Maryvale UFSD</A><BR>
<A HREF="140709/140709.html">Cheektowaga-Sloan UFSD</A><BR>
<A HREF="030101/030101.html">Chenango Forks CSD</A><BR>
<A HREF="030701/030701.html">Chenango Valley CSD</A><BR>
<A HREF="472202/472202.html">Cherry Valley-Springfield CSD</A><BR>
<A HREF="440201/440201.html">Chester UFSD</A><BR>
<A HREF="251601/251601.html">Chittenango CSD</A><BR>
<A HREF="261501/261501.html">Churchville-Chili CSD</A><BR>
<A HREF="110101/110101.html">Cincinnatus CSD</A><BR>
<A HREF="140801/140801.html">Clarence CSD</A><BR>
<A HREF="500101/500101.html">Clarkstown CSD</A><BR>
<A HREF="140703/140703.html">Cleveland Hill UFSD</A><BR>
<A HREF="510401/510401.html">Clifton-Fine CSD</A><BR>
<A HREF="411101/411101.html">Clinton CSD</A><BR>
<A HREF="099000/099000.html">Clinton-Essex-Warren-Washing Boces</A><BR>
<A HREF="650301/650301.html">Clyde-Savannah CSD</A><BR>
<A HREF="060701/060701.html">Clymer CSD</A><BR>
<A HREF="541102/541102.html">Cobleskill-Richmondville CSD</A><BR>
<A HREF="010500/010500.html">Cohoes City SD</A><BR>
<A HREF="580402/580402.html">Cold Spring Harbor CSD</A><BR>
<A HREF="510501/510501.html">Colton-Pierrepont CSD</A><BR>
<A HREF="580410/580410.html">Commack UFSD</A><BR>
<A HREF="580507/580507.html">Connetquot CSD</A><BR>
<A HREF="471701/471701.html">Cooperstown CSD</A><BR>
<A HREF="230201/230201.html">Copenhagen CSD</A><BR>
<A HREF="580105/580105.html">Copiague UFSD</A><BR>
<A HREF="520401/520401.html">Corinth CSD</A><BR>
<A HREF="571000/571000.html">Corning City SD</A><BR>
<A HREF="440301/440301.html">Cornwall CSD</A><BR>
<A HREF="110200/110200.html">Cortland City SD</A><BR>
<A HREF="190501/190501.html">Coxsackie-Athens CSD</A><BR>
<A HREF="660202/660202.html">Croton-Harmon UFSD</A><BR>
<A HREF="150203/150203.html">Crown Point CSD</A><BR>
<A HREF="022302/022302.html">Cuba-Rushford CSD</A><BR>
'''
'''

<HR>
<FONT size=+3><A NAME="DLIST">D</A><BR></FONT>
<A HREF="241101/241101.html">Dalton-Nunda CSD (Keshequa)</A><BR>
<A HREF="241001/241001.html">Dansville CSD</A><BR>
<A HREF="580107/580107.html">Deer Park UFSD</A><BR>
<A HREF="120501/120501.html">Delaware Academy CSD At Delhi</A><BR>
<A HREF="129000/129000.html">Delaw-Chenango-Madison-Otsego Boces</A><BR>
<A HREF="140707/140707.html">Depew UFSD</A><BR>
<A HREF="031301/031301.html">Deposit CSD</A><BR>
<A HREF="250301/250301.html">Deruyter CSD</A><BR>
<A HREF="660403/660403.html">Dobbs Ferry UFSD</A><BR>
<A HREF="211003/211003.html">Dolgeville CSD</A><BR>
<A HREF="130502/130502.html">Dover UFSD</A><BR>
<A HREF="120301/120301.html">Downsville CSD</A><BR>
<A HREF="610301/610301.html">Dryden CSD</A><BR>
<A HREF="530101/530101.html">Duanesburg CSD</A><BR>
<A HREF="680801/680801.html">Dundee CSD</A><BR>
<A HREF="060800/060800.html">Dunkirk City SD</A><BR>
<A HREF="139000/139000.html">Dutchess Boces</A><BR>


<HR>
<FONT size=+3><A NAME="ELIST">E</A><BR></FONT>
<A HREF="140301/140301.html">East Aurora UFSD</A><BR>
<A HREF="430501/430501.html">East Bloomfield CSD</A><BR>
<A HREF="490301/490301.html">East Greenbush CSD</A><BR>
<A HREF="580301/580301.html">East Hampton UFSD</A><BR>
<A HREF="260801/260801.html">East Irondequoit CSD</A><BR>
<A HREF="580503/580503.html">East Islip UFSD</A><BR>
<A HREF="280203/280203.html">East Meadow UFSD</A><BR>
<A HREF="580234/580234.html">East Moriches UFSD</A><BR>
<A HREF="580917/580917.html">East Quogue UFSD</A><BR>
<A HREF="500402/500402.html">East Ramapo CSD (Spring Valley)</A><BR>
<A HREF="261313/261313.html">East Rochester UFSD</A><BR>
<A HREF="280219/280219.html">East Rockaway UFSD</A><BR>
<A HREF="420401/420401.html">East Syracuse Minoa CSD</A><BR>
<A HREF="280402/280402.html">East Williston UFSD</A><BR>
<A HREF="660301/660301.html">Eastchester UFSD</A><BR>
<A HREF="589100/589100.html">Eastern Suffolk Boces</A><BR>
<A HREF="580912/580912.html">Eastport-South Manor CSD</A><BR>
<A HREF="141201/141201.html">Eden CSD</A><BR>
<A HREF="660406/660406.html">Edgemont UFSD</A><BR>
<A HREF="520601/520601.html">Edinburg Common SD</A><BR>
<A HREF="470501/470501.html">Edmeston CSD</A><BR>
<A HREF="513102/513102.html">Edwards-Knox CSD</A><BR>
<A HREF="180901/180901.html">Elba CSD</A><BR>
<A HREF="590801/590801.html">Eldred CSD</A><BR>
<A HREF="622002/622002.html">Ellenville CSD</A><BR>
<A HREF="040901/040901.html">Ellicottville CSD</A><BR>
<A HREF="070600/070600.html">Elmira City SD</A><BR>
<A HREF="070902/070902.html">Elmira Heights CSD</A><BR>
<A HREF="280216/280216.html">Elmont UFSD</A><BR>
<A HREF="660409/660409.html">Elmsford UFSD</A><BR>
<A HREF="580401/580401.html">Elwood UFSD</A><BR>
<A HREF="149100/149100.html">Erie 1 Boces</A><BR>
<A HREF="149200/149200.html">Erie 2-Chautauqua-Cattaraugus Boces</A><BR>
<A HREF="141401/141401.html">Evans-Brant CSD (Lake Shore)</A><BR>


<HR>
<FONT size=+3><A NAME="FLIST">F</A><BR></FONT>
<A HREF="420601/420601.html">Fabius-Pompey CSD</A><BR>
<A HREF="261301/261301.html">Fairport CSD</A><BR>
<A HREF="061101/061101.html">Falconer CSD</A><BR>
<A HREF="590501/590501.html">Fallsburg CSD</A><BR>
<A HREF="280522/280522.html">Farmingdale UFSD</A><BR>
<A HREF="421001/421001.html">Fayetteville-Manlius CSD</A><BR>
<A HREF="022001/022001.html">Fillmore CSD</A><BR>
<A HREF="580514/580514.html">Fire Island UFSD</A><BR>
<A HREF="581004/581004.html">Fishers Island UFSD</A><BR>
<A HREF="280222/280222.html">Floral Park-Bellerose UFSD</A><BR>
<A HREF="442115/442115.html">Florida UFSD</A><BR>
<A HREF="270601/270601.html">Fonda-Fultonville CSD</A><BR>
<A HREF="061503/061503.html">Forestville CSD</A><BR>
<A HREF="640502/640502.html">Fort Ann CSD</A><BR>
<A HREF="640601/640601.html">Fort Edward UFSD</A><BR>
<A HREF="270701/270701.html">Fort Plain CSD</A><BR>
<A HREF="210402/210402.html">Frankfort-Schuyler CSD</A><BR>
<A HREF="120701/120701.html">Franklin CSD</A><BR>
<A HREF="280217/280217.html">Franklin Square UFSD</A><BR>
<A HREF="169000/169000.html">Franklin-Essex-Hamilton Boces</A><BR>
<A HREF="041101/041101.html">Franklinville CSD</A><BR>
<A HREF="062201/062201.html">Fredonia CSD</A><BR>
<A HREF="280209/280209.html">Freeport UFSD</A><BR>
<A HREF="060301/060301.html">Frewsburg CSD</A><BR>
<A HREF="021601/021601.html">Friendship CSD</A><BR>
<A HREF="141604/141604.html">Frontier CSD</A><BR>
<A HREF="460500/460500.html">Fulton City SD</A><BR>


<HR>
<FONT size=+3><A NAME="GLIST">G</A><BR></FONT>
<A HREF="520701/520701.html">Galway CSD</A><BR>
<A HREF="650902/650902.html">Gananda CSD</A><BR>
<A HREF="280218/280218.html">Garden City UFSD</A><BR>
<A HREF="480404/480404.html">Garrison UFSD</A><BR>
<A HREF="260401/260401.html">Gates-Chili CSD</A><BR>
<A HREF="220401/220401.html">General Brown CSD</A><BR>
<A HREF="249000/249000.html">Genesee Valley Boces</A><BR>
<A HREF="020702/020702.html">Genesee Valley CSD</A><BR>
<A HREF="240401/240401.html">Geneseo CSD</A><BR>
<A HREF="430700/430700.html">Geneva City SD</A><BR>
<A HREF="610327/610327.html">George Junior Republic UFSD</A><BR>
<A HREF="081401/081401.html">Georgetown-South Otselic CSD</A><BR>
<A HREF="100902/100902.html">Germantown CSD</A><BR>
<A HREF="470202/470202.html">Gilbertsville-Mount Upton CSD</A><BR>
<A HREF="540801/540801.html">Gilboa-Conesville CSD</A><BR>
<A HREF="280100/280100.html">Glen Cove City SD</A><BR>
<A HREF="630300/630300.html">Glens Falls City SD</A><BR>
<A HREF="630918/630918.html">Glens Falls Comn SD</A><BR>
<A HREF="170500/170500.html">Gloversville City SD</A><BR>
<A HREF="430901/430901.html">Gorham-Middlesex CSD (Marcus Whitman</A><BR>
<A HREF="440601/440601.html">Goshen CSD</A><BR>
<A HREF="511101/511101.html">Gouverneur CSD</A><BR>
<A HREF="042801/042801.html">Gowanda CSD</A><BR>
<A HREF="141501/141501.html">Grand Island CSD</A><BR>
<A HREF="640701/640701.html">Granville CSD</A><BR>
<A HREF="280407/280407.html">Great Neck UFSD</A><BR>
<A HREF="559000/559000.html">Greater Southern Tier Boces</A><BR>
<A HREF="260501/260501.html">Greece CSD</A><BR>
<A HREF="010701/010701.html">Green Island UFSD</A><BR>
<A HREF="660407/660407.html">Greenburgh CSD</A><BR>
<A HREF="660411/660411.html">Greenburgh Eleven UFSD</A><BR>
<A HREF="660410/660410.html">Greenburgh-Graham UFSD</A><BR>
<A HREF="660412/660412.html">Greenburgh-North Castle UFSD</A><BR>
<A HREF="080601/080601.html">Greene CSD</A><BR>
<A HREF="581010/581010.html">Greenport UFSD</A><BR>
<A HREF="190701/190701.html">Greenville CSD</A><BR>
<A HREF="640801/640801.html">Greenwich CSD</A><BR>
<A HREF="442111/442111.html">Greenwood Lake UFSD</A><BR>
<A HREF="610501/610501.html">Groton CSD</A><BR>
<A HREF="010802/010802.html">Guilderland CSD</A><BR>


<HR>
<FONT size=+3><A NAME="HLIST">H</A><BR></FONT>
<A HREF="630801/630801.html">Hadley-Luzerne CSD</A><BR>
<A HREF="480401/480401.html">Haldane CSD</A><BR>
<A HREF="580405/580405.html">Half Hollow Hills CSD</A><BR>
<A HREF="141601/141601.html">Hamburg CSD</A><BR>
<A HREF="250701/250701.html">Hamilton CSD</A><BR>
<A HREF="209000/209000.html">Hamilton-Fulton-Montgomery Boces</A><BR>
<A HREF="511201/511201.html">Hammond CSD</A><BR>
<A HREF="572901/572901.html">Hammondsport CSD</A><BR>
<A HREF="580905/580905.html">Hampton Bays UFSD</A><BR>
<A HREF="120906/120906.html">Hancock CSD</A><BR>
<A HREF="460701/460701.html">Hannibal CSD</A><BR>
<A HREF="580406/580406.html">Harborfields CSD</A><BR>
<A HREF="030501/030501.html">Harpursville CSD</A><BR>
<A HREF="660501/660501.html">Harrison CSD</A><BR>
<A HREF="230301/230301.html">Harrisville CSD</A><BR>
<A HREF="641001/641001.html">Hartford CSD</A><BR>
<A HREF="660404/660404.html">Hastings-On-Hudson UFSD</A><BR>
<A HREF="580506/580506.html">Hauppauge UFSD</A><BR>
<A HREF="500201/500201.html">Haverstraw-Stony Point CSD (North Ro</A><BR>
<A HREF="660803/660803.html">Hawthorne-Cedar Knolls UFSD</A><BR>
<A HREF="280201/280201.html">Hempstead UFSD</A><BR>
<A HREF="660203/660203.html">Hendrick Hudson CSD</A><BR>
<A HREF="219000/219000.html">Herk-Fulton-Hamilton-Otsego Boces</A><BR>
<A HREF="210601/210601.html">Herkimer CSD</A><BR>
<A HREF="511301/511301.html">Hermon-Dekalb CSD</A><BR>
<A HREF="280409/280409.html">Herricks UFSD</A><BR>
<A HREF="512404/512404.html">Heuvelton CSD</A><BR>
<A HREF="280214/280214.html">Hewlett-Woodmere UFSD</A><BR>
<A HREF="280517/280517.html">Hicksville UFSD</A><BR>
<A HREF="620803/620803.html">Highland CSD</A><BR>
<A HREF="440901/440901.html">Highland Falls CSD</A><BR>
<A HREF="261101/261101.html">Hilton CSD</A><BR>
<A HREF="041401/041401.html">Hinsdale CSD</A><BR>
<A HREF="141701/141701.html">Holland CSD</A><BR>
<A HREF="412201/412201.html">Holland Patent CSD</A><BR>
<A HREF="450704/450704.html">Holley CSD</A><BR>
<A HREF="110701/110701.html">Homer CSD</A><BR>
<A HREF="431401/431401.html">Honeoye CSD</A><BR>
<A HREF="260901/260901.html">Honeoye Falls-Lima CSD</A><BR>
<A HREF="491401/491401.html">Hoosic Valley CSD</A><BR>
<A HREF="490501/490501.html">Hoosick Falls CSD</A><BR>
<A HREF="141603/141603.html">Hopevale UFSD At Hamburg</A><BR>
<A HREF="571800/571800.html">Hornell City SD</A><BR>
<A HREF="070901/070901.html">Horseheads CSD</A><BR>
<A HREF="101300/101300.html">Hudson City SD</A><BR>
<A HREF="641301/641301.html">Hudson Falls CSD</A><BR>
<A HREF="190901/190901.html">Hunter-Tannersville CSD</A><BR>
<A HREF="580403/580403.html">Huntington UFSD</A><BR>
<A HREF="130801/130801.html">Hyde Park CSD</A><BR>


<HR>
<FONT size=+3><A NAME="ILIST">I</A><BR></FONT>
<A HREF="200401/200401.html">Indian Lake CSD</A><BR>
<A HREF="220301/220301.html">Indian River CSD</A><BR>
<A HREF="200501/200501.html">Inlet Comn SD</A><BR>
<A HREF="141301/141301.html">Iroquois CSD</A><BR>
<A HREF="660402/660402.html">Irvington UFSD</A><BR>
<A HREF="280231/280231.html">Island Park UFSD</A><BR>
<A HREF="280226/280226.html">Island Trees UFSD</A><BR>
<A HREF="580502/580502.html">Islip UFSD</A><BR>
<A HREF="610600/610600.html">Ithaca City SD</A><BR>


<HR>
<FONT size=+3><A NAME="JLIST">J</A><BR></FONT>
<A HREF="061700/061700.html">Jamestown City SD</A><BR>
<A HREF="420411/420411.html">Jamesville-Dewitt CSD</A><BR>
<A HREF="572702/572702.html">Jasper-Troupsburg CSD</A><BR>
<A HREF="229000/229000.html">Jeffer-Lewis-Hamil-Herk-Oneida Boces</A><BR>
<A HREF="540901/540901.html">Jefferson CSD</A><BR>
<A HREF="280515/280515.html">Jericho UFSD</A><BR>
<A HREF="630601/630601.html">Johnsburg CSD</A><BR>
<A HREF="031502/031502.html">Johnson City CSD</A><BR>
<A HREF="170600/170600.html">Johnstown City SD</A><BR>
<A HREF="420501/420501.html">Jordan-Elbridge CSD</A><BR>


<HR>
<FONT size=+3><A NAME="KLIST">K</A><BR></FONT>
<A HREF="660101/660101.html">Katonah-Lewisboro UFSD</A><BR>
<A HREF="150601/150601.html">Keene CSD</A><BR>
<A HREF="450607/450607.html">Kendall CSD</A><BR>
<A HREF="142601/142601.html">Kenmore-Tonawanda UFSD</A><BR>
<A HREF="101401/101401.html">Kinderhook CSD</A><BR>
<A HREF="580805/580805.html">Kings Park CSD</A><BR>
<A HREF="620600/620600.html">Kingston City SD</A><BR>
<A HREF="441202/441202.html">Kiryas Joel Village UFSD</A><BR>


<HR>
<FONT size=+3><A NAME="LLIST">L</A><BR></FONT>
<A HREF="221401/221401.html">La Fargeville CSD</A><BR>
<A HREF="141800/141800.html">Lackawanna City SD</A><BR>
<A HREF="420807/420807.html">Lafayette CSD</A><BR>
<A HREF="630701/630701.html">Lake George CSD</A><BR>
<A HREF="151102/151102.html">Lake Placid CSD</A><BR>
<A HREF="200601/200601.html">Lake Pleasant CSD</A><BR>
<A HREF="662401/662401.html">Lakeland CSD</A><BR>
<A HREF="141901/141901.html">Lancaster CSD</A><BR>
<A HREF="610801/610801.html">Lansing CSD</A><BR>
<A HREF="490601/490601.html">Lansingburgh CSD</A><BR>
<A HREF="470801/470801.html">Laurens CSD</A><BR>
<A HREF="280215/280215.html">Lawrence UFSD</A><BR>
<A HREF="181001/181001.html">Le Roy CSD</A><BR>
<A HREF="670401/670401.html">Letchworth CSD</A><BR>
<A HREF="280205/280205.html">Levittown UFSD</A><BR>
<A HREF="400301/400301.html">Lewiston-Porter CSD</A><BR>
<A HREF="590901/590901.html">Liberty CSD</A><BR>
<A HREF="580104/580104.html">Lindenhurst UFSD</A><BR>
<A HREF="511602/511602.html">Lisbon CSD</A><BR>
<A HREF="210800/210800.html">Little Falls City SD</A><BR>
<A HREF="580603/580603.html">Little Flower UFSD</A><BR>
<A HREF="421501/421501.html">Liverpool CSD</A><BR>
<A HREF="591302/591302.html">Livingston Manor CSD</A><BR>
<A HREF="240801/240801.html">Livonia CSD</A><BR>
<A HREF="400400/400400.html">Lockport City SD</A><BR>
<A HREF="280503/280503.html">Locust Valley CSD</A><BR>
<A HREF="280300/280300.html">Long Beach City SD</A><BR>
<A HREF="200701/200701.html">Long Lake CSD</A><BR>
<A HREF="580212/580212.html">Longwood CSD</A><BR>
<A HREF="230901/230901.html">Lowville Academy & CSD</A><BR>
<A HREF="221301/221301.html">Lyme CSD</A><BR>
<A HREF="280220/280220.html">Lynbrook UFSD</A><BR>
<A HREF="421504/421504.html">Lyncourt UFSD</A><BR>
<A HREF="451001/451001.html">Lyndonville CSD</A><BR>
<A HREF="650501/650501.html">Lyons CSD</A><BR>


<HR>
<FONT size=+3><A NAME="MLIST">M</A><BR></FONT>
<A HREF="251101/251101.html">Madison CSD</A><BR>
<A HREF="259000/259000.html">Madison-Oneida Boces</A><BR>
<A HREF="511901/511901.html">Madrid-Waddington CSD</A><BR>
<A HREF="480101/480101.html">Mahopac CSD</A><BR>
<A HREF="031101/031101.html">Maine-Endwell CSD</A><BR>
<A HREF="161501/161501.html">Malone CSD</A><BR>
<A HREF="280212/280212.html">Malverne UFSD</A><BR>
<A HREF="660701/660701.html">Mamaroneck UFSD</A><BR>
<A HREF="431101/431101.html">Manchester-Shortsville CSD (Red Jack</A><BR>
<A HREF="280406/280406.html">Manhasset UFSD</A><BR>
<A HREF="110901/110901.html">Marathon CSD</A><BR>
<A HREF="421101/421101.html">Marcellus CSD</A><BR>
<A HREF="121401/121401.html">Margaretville CSD</A><BR>
<A HREF="650701/650701.html">Marion CSD</A><BR>
<A HREF="621001/621001.html">Marlboro CSD</A><BR>
<A HREF="280523/280523.html">Massapequa UFSD</A><BR>
<A HREF="512001/512001.html">Massena CSD</A><BR>
<A HREF="581012/581012.html">Mattituck-Cutchogue UFSD</A><BR>
<A HREF="170801/170801.html">Mayfield CSD</A><BR>
<A HREF="110304/110304.html">McGraw CSD</A><BR>
<A HREF="521200/521200.html">Mechanicville City SD</A><BR>
<A HREF="450801/450801.html">Medina CSD</A><BR>
<A HREF="010615/010615.html">Menands UFSD</A><BR>
<A HREF="280225/280225.html">Merrick UFSD</A><BR>
<A HREF="460901/460901.html">Mexico CSD</A><BR>
<A HREF="580211/580211.html">Middle Country CSD</A><BR>
<A HREF="541001/541001.html">Middleburgh CSD</A><BR>
<A HREF="441000/441000.html">Middletown City SD</A><BR>
<A HREF="471101/471101.html">Milford CSD</A><BR>
<A HREF="132201/132201.html">Millbrook CSD</A><BR>
<A HREF="580208/580208.html">Miller Place UFSD</A><BR>
<A HREF="280410/280410.html">Mineola UFSD</A><BR>
<A HREF="150801/150801.html">Minerva CSD</A><BR>
<A HREF="441101/441101.html">Minisink Valley CSD</A><BR>
<A HREF="269100/269100.html">Monroe 1 Boces</A><BR>
<A HREF="269200/269200.html">Monroe 2-Orleans Boces</A><BR>
<A HREF="441201/441201.html">Monroe-Woodbury CSD</A><BR>
<A HREF="580306/580306.html">Montauk UFSD</A><BR>
<A HREF="591401/591401.html">Monticello CSD</A><BR>
<A HREF="051301/051301.html">Moravia CSD</A><BR>
<A HREF="150901/150901.html">Moriah CSD</A><BR>
<A HREF="471201/471201.html">Morris CSD</A><BR>
<A HREF="512101/512101.html">Morristown CSD</A><BR>
<A HREF="250401/250401.html">Morrisville-Eaton CSD</A><BR>
<A HREF="212001/212001.html">Mount Markham CSD</A><BR>
<A HREF="240901/240901.html">Mt Morris CSD</A><BR>
<A HREF="660801/660801.html">Mt Pleasant CSD</A><BR>
<A HREF="660806/660806.html">Mt Pleasant-Blythedale UFSD</A><BR>
<A HREF="660804/660804.html">Mt Pleasant-Cottage UFSD</A><BR>
<A HREF="580207/580207.html">Mt Sinai UFSD</A><BR>
<A HREF="660900/660900.html">Mt Vernon School District</A><BR>


<HR>
<FONT size=+3><A NAME="NLIST">N</A><BR></FONT>
<A HREF="500108/500108.html">Nanuet UFSD</A><BR>
<A HREF="431201/431201.html">Naples CSD</A><BR>
<A HREF="289000/289000.html">Nassau Boces</A><BR>
<A HREF="411501/411501.html">New Hartford CSD</A><BR>
<A HREF="280405/280405.html">New Hyde Park-Garden City Park UFSD</A><BR>
<A HREF="101601/101601.html">New Lebanon CSD</A><BR>
<A HREF="621101/621101.html">New Paltz CSD</A><BR>
<A HREF="661100/661100.html">New Rochelle City SD</A><BR>
<A HREF="581015/581015.html">New Suffolk Comn SD</A><BR>
<A HREF="650101/650101.html">Newark CSD</A><BR>
<A HREF="600402/600402.html">Newark Valley CSD</A><BR>
<A HREF="441600/441600.html">Newburgh City SD</A><BR>
<A HREF="151001/151001.html">Newcomb CSD</A><BR>
<A HREF="400601/400601.html">Newfane CSD</A><BR>
<A HREF="610901/610901.html">Newfield CSD</A><BR>
<A HREF="400800/400800.html">Niagara Falls City SD</A><BR>
<A HREF="400701/400701.html">Niagara-Wheatfield CSD</A><BR>
<A HREF="530301/530301.html">Niskayuna CSD</A><BR>
<A HREF="580103/580103.html">North Babylon UFSD</A><BR>
<A HREF="280204/280204.html">North Bellmore UFSD</A><BR>
<A HREF="142201/142201.html">North Collins CSD</A><BR>
<A HREF="010623/010623.html">North Colonie CSD</A><BR>
<A HREF="490801/490801.html">North Greenbush Comn SD (Williams)</A><BR>
<A HREF="280229/280229.html">North Merrick UFSD</A><BR>
<A HREF="651501/651501.html">North Rose-Wolcott CSD</A><BR>
<A HREF="661301/661301.html">North Salem CSD</A><BR>
<A HREF="280501/280501.html">North Shore CSD</A><BR>
<A HREF="420303/420303.html">North Syracuse CSD</A><BR>
<A HREF="400900/400900.html">North Tonawanda City SD</A><BR>
<A HREF="630202/630202.html">North Warren CSD</A><BR>
<A HREF="131101/131101.html">Northeast CSD</A><BR>
<A HREF="090501/090501.html">Northeastern Clinton CSD</A><BR>
<A HREF="090901/090901.html">Northern Adirondack CSD</A><BR>
<A HREF="580404/580404.html">Northport-East Northport UFSD</A><BR>
<A HREF="170901/170901.html">Northville CSD</A><BR>
<A HREF="081200/081200.html">Norwich City SD</A><BR>
<A HREF="512201/512201.html">Norwood-Norfolk CSD</A><BR>
<A HREF="411504/411504.html">NY Mills UFSD</A><BR>
<A HREF="500304/500304.html">Nyack UFSD</A><BR>
<A HREF="300000/300000.html">NYC Chancellor's Office</A><BR>
<A HREF="310100/310100.html">NYC Geog Dist # 1 - Manhattan</A><BR>
<A HREF="310200/310200.html">NYC Geog Dist # 2 - Manhattan</A><BR>
<A HREF="310300/310300.html">NYC Geog Dist # 3 - Manhattan</A><BR>
<A HREF="310400/310400.html">NYC Geog Dist # 4 - Manhattan</A><BR>
<A HREF="310500/310500.html">NYC Geog Dist # 5 - Manhattan</A><BR>
<A HREF="310600/310600.html">NYC Geog Dist # 6 - Manhattan</A><BR>
<A HREF="320700/320700.html">NYC Geog Dist # 7 - Bronx</A><BR>
<A HREF="320800/320800.html">NYC Geog Dist # 8 - Bronx</A><BR>
<A HREF="320900/320900.html">NYC Geog Dist # 9 - Bronx</A><BR>
<A HREF="321000/321000.html">NYC Geog Dist #10 - Bronx</A><BR>
<A HREF="321100/321100.html">NYC Geog Dist #11 - Bronx</A><BR>
<A HREF="321200/321200.html">NYC Geog Dist #12 - Bronx</A><BR>
<A HREF="331300/331300.html">NYC Geog Dist #13 - Brooklyn</A><BR>
<A HREF="331400/331400.html">NYC Geog Dist #14 - Brooklyn</A><BR>
<A HREF="331500/331500.html">NYC Geog Dist #15 - Brooklyn</A><BR>
<A HREF="331600/331600.html">NYC Geog Dist #16 - Brooklyn</A><BR>
<A HREF="331700/331700.html">NYC Geog Dist #17 - Brooklyn</A><BR>
<A HREF="331800/331800.html">NYC Geog Dist #18 - Brooklyn</A><BR>
<A HREF="331900/331900.html">NYC Geog Dist #19 - Brooklyn</A><BR>
<A HREF="332000/332000.html">NYC Geog Dist #20 - Brooklyn</A><BR>
<A HREF="332100/332100.html">NYC Geog Dist #21 - Brooklyn</A><BR>
<A HREF="332200/332200.html">NYC Geog Dist #22 - Brooklyn</A><BR>
<A HREF="332300/332300.html">NYC Geog Dist #23 - Brooklyn</A><BR>
<A HREF="342400/342400.html">NYC Geog Dist #24 - Queens</A><BR>
<A HREF="342500/342500.html">NYC Geog Dist #25 - Queens</A><BR>
<A HREF="342600/342600.html">NYC Geog Dist #26 - Queens</A><BR>
<A HREF="342700/342700.html">NYC Geog Dist #27 - Queens</A><BR>
<A HREF="342800/342800.html">NYC Geog Dist #28 - Queens</A><BR>
<A HREF="342900/342900.html">NYC Geog Dist #29 - Queens</A><BR>
<A HREF="343000/343000.html">NYC Geog Dist #30 - Queens</A><BR>
<A HREF="353100/353100.html">NYC Geog Dist #31 - Staten Island</A><BR>
<A HREF="333200/333200.html">NYC Geog Dist #32 - Brooklyn</A><BR>
<A HREF="307500/307500.html">NYC Spec Schools - Dist 75</A><BR>


<HR>
<FONT size=+3><A NAME="OLIST">O</A><BR></FONT>
<A HREF="181101/181101.html">Oakfield-Alabama CSD</A><BR>
<A HREF="280211/280211.html">Oceanside UFSD</A><BR>
<A HREF="550101/550101.html">Odessa-Montour CSD</A><BR>
<A HREF="512300/512300.html">Ogdensburg City SD</A><BR>
<A HREF="042400/042400.html">Olean City SD</A><BR>
<A HREF="251400/251400.html">Oneida City SD</A><BR>
<A HREF="419000/419000.html">Oneida-Herkimer-Madison Boces</A><BR>
<A HREF="471400/471400.html">Oneonta City SD</A><BR>
<A HREF="421201/421201.html">Onondaga CSD</A><BR>
<A HREF="429000/429000.html">Onondaga-Cortland-Madison Boces</A><BR>
<A HREF="621201/621201.html">Onteora CSD</A><BR>
<A HREF="271201/271201.html">Oppenheim-Ephratah-St. Johnsville Cs</A><BR>
<A HREF="449000/449000.html">Orange-Ulster Boces</A><BR>
<A HREF="142301/142301.html">Orchard Park CSD</A><BR>
<A HREF="412901/412901.html">Oriskany CSD</A><BR>
<A HREF="459000/459000.html">Orleans-Niagara Boces</A><BR>
<A HREF="661401/661401.html">Ossining UFSD</A><BR>
<A HREF="469000/469000.html">Oswego Boces</A><BR>
<A HREF="461300/461300.html">Oswego City SD</A><BR>
<A HREF="471601/471601.html">Otego-Unadilla CSD</A><BR>
<A HREF="199000/199000.html">Otsego-Delaw-Schoharie-Greene Boces</A><BR>
<A HREF="600601/600601.html">Owego-Apalachin CSD</A><BR>
<A HREF="081501/081501.html">Oxford Academy & CSD</A><BR>
<A HREF="280506/280506.html">Oyster Bay-East Norwich CSD</A><BR>
<A HREF="581002/581002.html">Oysterponds UFSD</A><BR>


<HR>
<FONT size=+3><A NAME="PLIST">P</A><BR></FONT>
<A HREF="650901/650901.html">Palmyra-MacEdon CSD</A><BR>
<A HREF="061601/061601.html">Panama CSD</A><BR>
<A HREF="512501/512501.html">Parishville-Hopkinton CSD</A><BR>
<A HREF="580224/580224.html">Patchogue-Medford UFSD</A><BR>
<A HREF="181201/181201.html">Pavilion CSD</A><BR>
<A HREF="131201/131201.html">Pawling CSD</A><BR>
<A HREF="500308/500308.html">Pearl River UFSD</A><BR>
<A HREF="661500/661500.html">Peekskill City SD</A><BR>
<A HREF="661601/661601.html">Pelham UFSD</A><BR>
<A HREF="181302/181302.html">Pembroke CSD</A><BR>
<A HREF="261201/261201.html">Penfield CSD</A><BR>
<A HREF="680601/680601.html">Penn Yan CSD</A><BR>
<A HREF="671201/671201.html">Perry CSD</A><BR>
<A HREF="091101/091101.html">Peru CSD</A><BR>
<A HREF="431301/431301.html">Phelps-Clifton Springs CSD</A><BR>
<A HREF="462001/462001.html">Phoenix CSD</A><BR>
<A HREF="440401/440401.html">Pine Bush CSD</A><BR>
<A HREF="131301/131301.html">Pine Plains CSD</A><BR>
<A HREF="060601/060601.html">Pine Valley CSD (South Dayton)</A><BR>
<A HREF="200101/200101.html">Piseco Comn SD</A><BR>
<A HREF="261401/261401.html">Pittsford CSD</A><BR>
<A HREF="280518/280518.html">Plainedge UFSD</A><BR>
<A HREF="280504/280504.html">Plainview-Old Bethpage CSD</A><BR>
<A HREF="091200/091200.html">Plattsburgh City SD</A><BR>
<A HREF="660809/660809.html">Pleasantville UFSD</A><BR>
<A HREF="660802/660802.html">Pocantico Hills CSD</A><BR>
<A HREF="211103/211103.html">Poland CSD</A><BR>
<A HREF="051101/051101.html">Port Byron CSD</A><BR>
<A HREF="661904/661904.html">Port Chester-Rye UFSD</A><BR>
<A HREF="580206/580206.html">Port Jefferson UFSD</A><BR>
<A HREF="441800/441800.html">Port Jervis City SD</A><BR>
<A HREF="280404/280404.html">Port Washington UFSD</A><BR>
<A HREF="042901/042901.html">Portville CSD</A><BR>
<A HREF="512902/512902.html">Potsdam CSD</A><BR>
<A HREF="131500/131500.html">Poughkeepsie City SD</A><BR>
<A HREF="572301/572301.html">Prattsburgh CSD</A><BR>
<A HREF="461801/461801.html">Pulaski CSD</A><BR>
<A HREF="641401/641401.html">Putnam CSD</A><BR>
<A HREF="480503/480503.html">Putnam Valley CSD</A><BR>
<A HREF="489000/489000.html">Putnam-Northern Westchester Boces</A><BR>


<HR>
<FONT size=+3><A NAME="QLIST">Q</A><BR></FONT>
<A HREF="630902/630902.html">Queensbury UFSD</A><BR>
<A HREF="499000/499000.html">Questar III (R-C-G) Boces</A><BR>
<A HREF="580903/580903.html">Quogue UFSD</A><BR>


<HR>
<FONT size=+3><A NAME="RLIST">R</A><BR></FONT>
<A HREF="043011/043011.html">Randolph Acad UFSD</A><BR>
<A HREF="043001/043001.html">Randolph CSD</A><BR>
<A HREF="200702/200702.html">Raquette Lake UFSD</A><BR>
<A HREF="010402/010402.html">Ravena-Coeymans-Selkirk CSD</A><BR>
<A HREF="651503/651503.html">Red Creek CSD</A><BR>
<A HREF="131701/131701.html">Red Hook CSD</A><BR>
<A HREF="411701/411701.html">Remsen CSD</A><BR>
<A HREF="580901/580901.html">Remsenburg-Speonk UFSD</A><BR>
<A HREF="491200/491200.html">Rensselaer City SD</A><BR>
<A HREF="131801/131801.html">Rhinebeck CSD</A><BR>
<A HREF="472001/472001.html">Richfield Springs CSD</A><BR>
<A HREF="062401/062401.html">Ripley CSD</A><BR>
<A HREF="580602/580602.html">Riverhead CSD</A><BR>
<A HREF="261600/261600.html">Rochester City SD</A><BR>
<A HREF="509000/509000.html">Rockland Boces</A><BR>
<A HREF="280221/280221.html">Rockville Centre UFSD</A><BR>
<A HREF="580209/580209.html">Rocky Point UFSD</A><BR>
<A HREF="411800/411800.html">Rome City SD</A><BR>
<A HREF="560603/560603.html">Romulus CSD</A><BR>
<A HREF="620901/620901.html">Rondout Valley CSD</A><BR>
<A HREF="280208/280208.html">Roosevelt UFSD</A><BR>
<A HREF="591301/591301.html">Roscoe CSD</A><BR>
<A HREF="280403/280403.html">Roslyn UFSD</A><BR>
<A HREF="530515/530515.html">Rotterdam-Mohonasen CSD</A><BR>
<A HREF="121502/121502.html">Roxbury CSD</A><BR>
<A HREF="401201/401201.html">Royalton-Hartland CSD</A><BR>
<A HREF="261701/261701.html">Rush-Henrietta CSD</A><BR>
<A HREF="661800/661800.html">Rye City SD</A><BR>
<A HREF="661901/661901.html">Rye Neck UFSD</A><BR>


<HR>
<FONT size=+3><A NAME="SLIST">S</A><BR></FONT>
<A HREF="580205/580205.html">Sachem CSD</A><BR>
<A HREF="221001/221001.html">Sackets Harbor CSD</A><BR>
<A HREF="580305/580305.html">Sag Harbor UFSD</A><BR>
<A HREF="580910/580910.html">Sagaponack Comn SD</A><BR>
<A HREF="043200/043200.html">Salamanca City SD</A><BR>
<A HREF="641501/641501.html">Salem CSD</A><BR>
<A HREF="161201/161201.html">Salmon River CSD</A><BR>
<A HREF="461901/461901.html">Sandy Creek CSD</A><BR>
<A HREF="091402/091402.html">Saranac CSD</A><BR>
<A HREF="161401/161401.html">Saranac Lake CSD</A><BR>
<A HREF="521800/521800.html">Saratoga Springs City SD</A><BR>
<A HREF="621601/621601.html">Saugerties CSD</A><BR>
<A HREF="411603/411603.html">Sauquoit Valley CSD</A><BR>
<A HREF="580504/580504.html">Sayville UFSD</A><BR>
<A HREF="662001/662001.html">Scarsdale UFSD</A><BR>
<A HREF="530501/530501.html">Schalmont CSD</A><BR>
<A HREF="530600/530600.html">Schenectady City SD</A><BR>
<A HREF="470901/470901.html">Schenevus CSD</A><BR>
<A HREF="491501/491501.html">Schodack CSD</A><BR>
<A HREF="541201/541201.html">Schoharie CSD</A><BR>
<A HREF="151401/151401.html">Schroon Lake CSD</A><BR>
<A HREF="521701/521701.html">Schuylerville CSD</A><BR>
<A HREF="022401/022401.html">Scio CSD</A><BR>
<A HREF="530202/530202.html">Scotia-Glenville CSD</A><BR>
<A HREF="280206/280206.html">Seaford UFSD</A><BR>
<A HREF="560701/560701.html">Seneca Falls CSD</A><BR>
<A HREF="280252/280252.html">Sewanhaka Central HS District</A><BR>
<A HREF="541401/541401.html">Sharon Springs CSD</A><BR>
<A HREF="580701/580701.html">Shelter Island UFSD</A><BR>
<A HREF="520302/520302.html">Shenendehowa CSD</A><BR>
<A HREF="082001/082001.html">Sherburne-Earlville CSD</A><BR>
<A HREF="062601/062601.html">Sherman CSD</A><BR>
<A HREF="412000/412000.html">Sherrill City SD</A><BR>
<A HREF="580601/580601.html">Shoreham-Wading River CSD</A><BR>
<A HREF="121601/121601.html">Sidney CSD</A><BR>
<A HREF="061501/061501.html">Silver Creek CSD</A><BR>
<A HREF="421601/421601.html">Skaneateles CSD</A><BR>
<A HREF="580801/580801.html">Smithtown CSD</A><BR>
<A HREF="651201/651201.html">Sodus CSD</A><BR>
<A HREF="420702/420702.html">Solvay UFSD</A><BR>
<A HREF="662101/662101.html">Somers CSD</A><BR>
<A HREF="010601/010601.html">South Colonie CSD</A><BR>
<A HREF="580235/580235.html">South Country CSD</A><BR>
<A HREF="521401/521401.html">South Glens Falls CSD</A><BR>
<A HREF="580413/580413.html">South Huntington UFSD</A><BR>
<A HREF="220101/220101.html">South Jefferson CSD</A><BR>
<A HREF="121702/121702.html">South Kortright CSD</A><BR>
<A HREF="231101/231101.html">South Lewis CSD</A><BR>
<A HREF="030201/030201.html">South Mountain-Hickory Comn SD At Bi</A><BR>
<A HREF="500301/500301.html">South Orangetown CSD</A><BR>
<A HREF="560501/560501.html">South Seneca CSD</A><BR>
<A HREF="580906/580906.html">Southampton UFSD</A><BR>
<A HREF="050701/050701.html">Southern Cayuga CSD</A><BR>
<A HREF="581005/581005.html">Southold UFSD</A><BR>
<A HREF="060201/060201.html">Southwestern CSD At Jamestown</A><BR>
<A HREF="131602/131602.html">Spackenkill UFSD</A><BR>
<A HREF="261001/261001.html">Spencerport CSD</A><BR>
<A HREF="600801/600801.html">Spencer-Van Etten CSD</A><BR>
<A HREF="580304/580304.html">Springs UFSD</A><BR>
<A HREF="141101/141101.html">Springville-Griffith Inst CSD</A><BR>
<A HREF="519000/519000.html">St Lawrence-Lewis Boces</A><BR>
<A HREF="161801/161801.html">St Regis Falls CSD</A><BR>
<A HREF="121701/121701.html">Stamford CSD</A><BR>
<A HREF="401001/401001.html">Starpoint CSD</A><BR>
<A HREF="522001/522001.html">Stillwater CSD</A><BR>
<A HREF="251501/251501.html">Stockbridge Valley CSD</A><BR>
<A HREF="500401/500401.html">Suffern CSD</A><BR>
<A HREF="599000/599000.html">Sullivan Boces</A><BR>
<A HREF="591502/591502.html">Sullivan West CSD</A><BR>
<A HREF="030601/030601.html">Susquehanna Valley CSD</A><BR>
<A HREF="140207/140207.html">Sweet Home CSD</A><BR>
<A HREF="280502/280502.html">Syosset CSD</A><BR>
<A HREF="421800/421800.html">Syracuse City SD</A><BR>


<HR>
<FONT size=+3><A NAME="TLIST">T</A><BR></FONT>
<A HREF="100501/100501.html">Taconic Hills CSD</A><BR>
<A HREF="220701/220701.html">Thousand Islands CSD</A><BR>
<A HREF="580201/580201.html">Three Village CSD</A><BR>
<A HREF="151501/151501.html">Ticonderoga CSD</A><BR>
<A HREF="600903/600903.html">Tioga CSD</A><BR>
<A HREF="619000/619000.html">Tompkins-Seneca-Tioga Boces</A><BR>
<A HREF="142500/142500.html">Tonawanda City SD</A><BR>
<A HREF="211901/211901.html">Town Of Webb UFSD</A><BR>
<A HREF="591201/591201.html">Tri-Valley CSD</A><BR>
<A HREF="491700/491700.html">Troy City SD</A><BR>
<A HREF="611001/611001.html">Trumansburg CSD</A><BR>
<A HREF="580913/580913.html">Tuckahoe Comn SD</A><BR>
<A HREF="660302/660302.html">Tuckahoe UFSD</A><BR>
<A HREF="421902/421902.html">Tully CSD</A><BR>
<A HREF="160101/160101.html">Tupper Lake CSD</A><BR>
<A HREF="441903/441903.html">Tuxedo UFSD</A><BR>


<HR>
<FONT size=+3><A NAME="ULIST">U</A><BR></FONT>
<A HREF="660401/660401.html">UFSD-Tarrytowns</A><BR>
<A HREF="629000/629000.html">Ulster Boces</A><BR>
<A HREF="081003/081003.html">Unadilla Valley CSD</A><BR>
<A HREF="051901/051901.html">Union Springs CSD</A><BR>
<A HREF="280202/280202.html">Uniondale UFSD</A><BR>
<A HREF="031501/031501.html">Union-Endicott CSD</A><BR>
<A HREF="412300/412300.html">Utica City SD</A><BR>


<HR>
<FONT size=+3><A NAME="VLIST">V</A><BR></FONT>
<A HREF="660805/660805.html">Valhalla UFSD</A><BR>
<A HREF="441301/441301.html">Valley CSD (Montgomery)</A><BR>
<A HREF="280213/280213.html">Valley Stream 13 UFSD</A><BR>
<A HREF="280224/280224.html">Valley Stream 24 UFSD</A><BR>
<A HREF="280230/280230.html">Valley Stream 30 UFSD</A><BR>
<A HREF="280251/280251.html">Valley Stream Central HS District</A><BR>
<A HREF="211701/211701.html">Van Hornesville-Owen D Young CSD</A><BR>
<A HREF="031601/031601.html">Vestal CSD</A><BR>
<A HREF="431701/431701.html">Victor CSD</A><BR>
<A HREF="011003/011003.html">Voorheesville CSD</A><BR>


<HR>
<FONT size=+3><A NAME="WLIST">W</A><BR></FONT>
<A HREF="580302/580302.html">Wainscott Comn SD</A><BR>
<A HREF="621801/621801.html">Wallkill CSD</A><BR>
<A HREF="121901/121901.html">Walton CSD</A><BR>
<A HREF="280223/280223.html">Wantagh UFSD</A><BR>
<A HREF="132101/132101.html">Wappingers CSD</A><BR>
<A HREF="631201/631201.html">Warrensburg CSD</A><BR>
<A HREF="671501/671501.html">Warsaw CSD</A><BR>
<A HREF="442101/442101.html">Warwick Valley CSD</A><BR>
<A HREF="649000/649000.html">Washing-Sara-War-Hamltn-Essex Boces</A><BR>
<A HREF="440102/440102.html">Washingtonville CSD</A><BR>
<A HREF="522101/522101.html">Waterford-Halfmoon UFSD</A><BR>
<A HREF="561006/561006.html">Waterloo CSD</A><BR>
<A HREF="222000/222000.html">Watertown City SD</A><BR>
<A HREF="411902/411902.html">Waterville CSD</A><BR>
<A HREF="011200/011200.html">Watervliet City SD</A><BR>
<A HREF="550301/550301.html">Watkins Glen CSD</A><BR>
<A HREF="600101/600101.html">Waverly CSD</A><BR>
<A HREF="573002/573002.html">Wayland-Cohocton CSD</A><BR>
<A HREF="650801/650801.html">Wayne CSD</A><BR>
<A HREF="439000/439000.html">Wayne-Finger Lakes Boces</A><BR>
<A HREF="261901/261901.html">Webster CSD</A><BR>
<A HREF="050301/050301.html">Weedsport CSD</A><BR>
<A HREF="200901/200901.html">Wells CSD</A><BR>
<A HREF="022601/022601.html">Wellsville CSD</A><BR>
<A HREF="580102/580102.html">West Babylon UFSD</A><BR>
<A HREF="210302/210302.html">West Canada Valley CSD</A><BR>
<A HREF="420101/420101.html">West Genesee CSD</A><BR>
<A HREF="280227/280227.html">West Hempstead UFSD</A><BR>
<A HREF="260803/260803.html">West Irondequoit CSD</A><BR>
<A HREF="580509/580509.html">West Islip UFSD</A><BR>
<A HREF="620202/620202.html">West Park UFSD</A><BR>
<A HREF="142801/142801.html">West Seneca CSD</A><BR>
<A HREF="040204/040204.html">West Valley CSD</A><BR>
<A HREF="280401/280401.html">Westbury UFSD</A><BR>
<A HREF="669000/669000.html">Westchester Boces</A><BR>
<A HREF="589300/589300.html">Western Suffolk Boces</A><BR>
<A HREF="062901/062901.html">Westfield CSD</A><BR>
<A HREF="580902/580902.html">Westhampton Beach UFSD</A><BR>
<A HREF="420701/420701.html">Westhill CSD</A><BR>
<A HREF="412801/412801.html">Westmoreland CSD</A><BR>
<A HREF="262001/262001.html">Wheatland-Chili CSD</A><BR>
<A HREF="170301/170301.html">Wheelerville UFSD</A><BR>
<A HREF="662200/662200.html">White Plains City SD</A><BR>
<A HREF="641701/641701.html">Whitehall CSD</A><BR>
<A HREF="412902/412902.html">Whitesboro CSD</A><BR>
<A HREF="022101/022101.html">Whitesville CSD</A><BR>
<A HREF="031401/031401.html">Whitney Point CSD</A><BR>
<A HREF="580232/580232.html">William Floyd UFSD</A><BR>
<A HREF="651402/651402.html">Williamson CSD</A><BR>
<A HREF="140203/140203.html">Williamsville CSD</A><BR>
<A HREF="151701/151701.html">Willsboro CSD</A><BR>
<A HREF="401501/401501.html">Wilson CSD</A><BR>
<A HREF="191401/191401.html">Windham-Ashland-Jewett CSD</A><BR>
<A HREF="031701/031701.html">Windsor CSD</A><BR>
<A HREF="472506/472506.html">Worcester CSD</A><BR>
<A HREF="580109/580109.html">Wyandanch UFSD</A><BR>
<A HREF="490804/490804.html">Wynantskill UFSD</A><BR>
<A HREF="671002/671002.html">Wyoming CSD</A><BR>


<HR>
<FONT size=+3><A NAME="YLIST">Y</A><BR></FONT>
<A HREF="662300/662300.html">Yonkers City SD</A><BR>
<A HREF="241701/241701.html">York CSD</A><BR>
<A HREF="043501/043501.html">Yorkshire-Pioneer CSD</A><BR>
<A HREF="662402/662402.html">Yorktown CSD</A><BR>
'''



from bs4 import BeautifulSoup
from http.cookiejar import CookieJar
import urllib.parse, urllib.request, re


user_agent_str = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'


em_list = []
fin = []


soup = BeautifulSoup(html, 'html5lib')



for i in soup.find_all('a'):

    working = []

    url = i.get('href')


    if not url == None:
        #print('\n\n', str(i.text), '\n', url)

        working.append(str(i.text))

        url = 'http://www.nysed.gov/admin/' + url
        working.append(url)

        em_list.append(working)



for i in em_list:

    working = []


    cj = CookieJar()
    req = urllib.request.Request(i[1], headers={'User-Agent': user_agent_str})
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    html = opener.open(req, timeout=10)

    h_soup = BeautifulSoup(html, 'html5lib')


    target = h_soup.find_all('a')[1].get('href')


    print('\n\nOrg name:', i[0], '\nTarget:', target)



    working.append(i[0])
    working.append(target)


    req = urllib.request.Request(target, headers={'User-Agent': user_agent_str})
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    html = opener.open(req, timeout=10)

    s = BeautifulSoup(html, 'html5lib')

    for ii in s.find_all('h3'):

        #print('~~~~~~~', ii)

        if 'Mailing Address:' in str(ii):

            addr = str(ii).split('Mailing Address:')[1].split('Phone:')[0].strip()

            addr = addr.replace('\n', ',')

            addr = re.sub(' +', ' ', addr)


            print('Addr:', addr)
            working.append(addr)



    fin.append(working)



print('\n\n\nFin:')
for i in fin:
    print(i)












grudb_list = [
['Green Island Union Free School District', 'http://www.greenisland.org/'],
['Guilderland Central School District', 'http://www.guilderlandschools.org/'],
['Maplewood Common School District', 'http://www.maplewoodschool.org/'],
['Menands Union Free School District', 'http://www.menandsschool.nycap.rr.com/'],
['Ravena-Coeymans-Selkirk Central School District', 'http://www.rcscsd.org/', 'https://cscsd.recruitfront.com/JobOpportunities', 'https://www.scsd.org/employment', 'https://www.rcscsd.org/about-us/employment'],
['Voorheesville Central School District', 'http://vcsdk12.org/'],
['Watervliet City School District', 'http://www.watervlietcityschools.org/'],
['Alfred-Almond Central School District', 'http://www.aacs.wnyric.org/'],
['Fillmore Central School District', 'http://www.fillmore.wnyric.org'],
['Genesee Valley Central School District', 'http://www.gvcs.wnyric.org'],
['New York City District # 7', 'http://www.schooldigger.com'],
['New York City District # 8', '_ERROR._url_not_found'],
['New York City District # 9', '_ERROR._url_not_found'],
['New York City District #10', '_ERROR._url_not_found'],
['New York City District #11', '_ERROR._url_not_found'],
['New York City District #12', 'http://www.newyorkschools.com/districts/nyc-district-12.html'],
['Binghamton School District', 'http://www.binghamtonschools.org'],
['Chenango Valley Central School District', 'http://www.cvcsd.stier.org'],
['Deposit Central School District', 'http://www.depositcsd.org'],
['Union-Endicott Central School District', 'http://www.uetigers.stier.org'],
['Vestal Central School District', 'http://www.vestal.k12.ny.us'],
['Allegany - Limestone Central School District', 'http://www.alli.wnyric.org'],
['Ellicottville Central School District', 'http://www.ellicottvillecentral.com'],
['Franklinville Central School District', 'http://www.tbafcs.org'],
['Portville Central School District', 'http://www.portville.wnyric.org'],
['Randolph Academy UFSD', 'http://www.randolphacademy.org'],
['Randolph Central School District', 'http://www.randolphcsd.org', 'http://www.randolphcsd.org/domain/24', 'https://www.phcsd.org/apps/pages/index.jsp?uREC_ID=1161786&type=d&pREC_ID=1415161'],
['Salamanca City School District', 'http://www.salamancany.org'],
['Yorkshire-Pioneer Central School District', 'http://www.pioneerschools.org', 'http://www.erschools.org/departments/employment/employment_opportunities', 'http://www.pioneerschools.org/domain/48'],
['Auburn City School District', 'http://district.auburn.cnyric.org'],
['Port Byron Central School District', 'http://portbyron.cnyric.org/'],
['Southern Cayuga Central School District', 'http://www.southerncayuga.org'],
['Union Springs Central School District', 'http://www.uscsd.info'],
['Weedsport Central School District', 'http://www.weedsport.org'],
['Bemus Point Central School District', 'http://www.mghs.org'],
['Clymer Central School District', 'http://www.clymer.wnyric.org'],
['Dunkirk City School District', 'http://www.dunkirkcsd.org'],
['Jamestown City School District', 'http://www.jamestownpublicschools.org'],
['Ripley Central School District', 'http://ripleycsd.wnyric.org'],
['Sherman Central School District', 'http://www.sherman.wnyric.org/'],
['Silver Creek Central School District', 'http://www.silvercreek.wnyric.org'],
['Elmira City School District', 'http://www.elmiracityschools.com'],
['Elmira Heights Central School District', 'http://www.heightsschools.com'],
['Horseheads Central School District', 'http://www.horseheadsdistrict.com'],
['Georgetown-South Otselic Central School District', 'http://www.ovcs.org'],
['Greene Central School District', 'http://www.greenecsd.org'],
['Norwich City School District', 'http://www.norwichcityschooldistrict.com'],
['Beekmantown Central School District', 'http://www.bcsdk12.org'],
['Northeastern Clinton Central School District', 'http://www.nccscougars.org'],
['Plattsburgh City School District', 'http://plattsburgh.neric.org'],
['Saranac Central School District', 'http://www.saranac.org'],
['Berkshire Union Free School District', 'http://www.berkshirefarm.org'],
['Germantown Central School District', 'http://www.germantownny.org/'],
['Delhi Central School District', 'http://www.delhischools.org'],
['Roxbury Central School District', 'http://www.roxburycs.org'],
['Walton Central School District', 'http://www.waltoncsd.stier.org'],
['Hyde Park Central School District', 'http://www.hydeparkschools.org'],
['Pawling Central School District', 'http://www.pawlingschools.org'],
['Red Hook Central School District', 'http://www.redhookcentralschools.org'],
['Wappingers Central School District', '_ERROR._url_not_found'],
['Cheektowaga Central School District', 'http://www.cheektowagacentral.org'],
['Cheektowaga-Maryvale Union Free School District', 'http://www.maryvale.wnyric.org'],
['Depew Union Free School District', 'http://www.depewschools.org'],
['East Aurora Union Free School District', 'http://www.eaur.wnyric.org'],
['Hopevale Union Free School District', 'http://www.hopevale.com/'],
['Kenmore-Tonawanda Union Free School District', 'http://www.kenton.k12.ny.us/'],
['Lackawanna City School District', 'http://www.lackawannaschools.org'],
['Sweet Home Central School District', 'http://www.shs.k12.ny.us/'],
['Keene Central School District', 'http://www.kcs.neric.org/'],
['Minerva Central School District', 'http://www.minervasd.org/minervasd/site/default.asp'],
['Newcomb Central School District', 'http://www.newcombcsd.org/education/district/district.php?sectionid=1', 'https://bcsd.recruitfront.com/JobOpportunities.aspx', 'https://plus.google.com/s/%23Employment/posts'],
['Brushton-Moira Central School District', 'http://www.fehb.org'],
['Chateaugay Central School District', 'http://www.chateaugay.org/'],
['Malone Central School District', 'http://www.malone.k12.ny.us/'],
['Salmon River Central School District', 'http://www.srk12.org/'],
['St Regis Falls Central School District', 'http://stregisfallscsd.org/'],
['Tupper Lake Central School District', 'http://www.tupperlakecsd.net/'],
['Mayfield Central School District', 'http://www.mayfieldk12.com/'],
['Northville Central School District', 'http://northvillecsd.k12.ny.us/'],
['Oppenheim-Ephratah Central School District', 'http://www.oecs.k12.ny.us'],
['Wheelerville Union Free School District', 'http://www.wufselementary.k12.ny.us/'],
['Oakfield-Alabama Central School District', 'http://www.oacs.k12.ny.us/'],
['Pavilion Central School District', 'http://www.pavilioncsd.org/'],
['Pembroke Central School District', 'http://www.pembroke.k12.ny.us/'],
['Coxsackie-Athens Central School District', 'http://www.coxsackie-athens.org/'],
['Hunter-Tannersville Central School District', 'http://www.htcsd.org/'],
['Indian Lake Central School District', 'http://www.ilcsd.org/'],
['Inlet Common School District', '_ERROR._url_not_found'],
['Lake Pleasant Central School District', 'http://www.lpschool.com/'],
['Piseco Common School District', '_ERROR._url_not_found'],
['Raquette Lake Union Free School District', 'http://www.fehb.org/raquette.htm'],
['Wells Central School District', 'http://www.wellscsd.com/main/'],
['Bridgewater-West Winfield Central School District', 'http://www.mmcsd.org/'],
['Dolgeville Central School District', 'http://www.dolgeville.org/'],
['Ilion Central School District', 'http://www.ilioncsd.org/'],
['Little Falls City School District', 'http://www.lfcsd.org'],
['Mohawk Central School District', 'http://www.mohawk.k12.ny.us/'],
['Poland Central School District', 'http://www.polandcs.com'],
['Van Hornesville-Owen D. Young Central School District', '_ERROR._url_not_found'],
['Carthage Central School District', 'http://www.carthagecsd.org/'],
['Thousand Islands Central School District', 'http://www.1000islandsschools.org'],
['New York City District  #15', '_ERROR._url_not_found'],
['New York City District #13', '_ERROR._url_not_found'],
['New York City District #14', '_ERROR._url_not_found'],
['New York City District #16', '_ERROR._url_not_found'],
['New York City District #17', '_ERROR._url_not_found'],
['New York City District #18', '_ERROR._url_not_found'],
['New York City District #19', 'http://www.newyorkschools.com'],
['New York City District #20', '_ERROR._url_not_found'],
['New York City District #21', '_ERROR._url_not_found'],
['New York City District #22', '_ERROR._url_not_found'],
['New York City District #23', '_ERROR._url_not_found'],
['New York City District #32', 'http://www.newyorkschools.com/districts/nyc-district-32.html'],
['Beaver River Central School District', 'http://www.brcsd.org'],
['Copenhagen Central School District', 'http://www.ccsknights.org/ccsknights/site/default.asp'],
['Lowville Acad & Central School District', 'http://www.lacs-ny.org'],
['Mt Morris Central School District', 'http://www.mtmorriscsd.org/'],
['Brookfield Central School District', 'http://www.bcsbeavers.org'],
['Canastota Central School District', 'http://www.canastotacsd.org'],
['Cazenovia Central School District', 'http://www.caz.cnyric.org/'],
['Chittenango Central School District', 'http://www.chittenangoschools.org/'],
['De Ruyter Central School District', '_ERROR._url_not_found'],
['Madison Central School District', 'http://madison.k12.sd.us/'],
['Oneida City School District', 'http://www.oneidacsd.org/'],
['Stockbridge Valley Central School District', 'http://www.stockbridgevalley.org/'],
['Brighton Central School District', 'http://www.bcsd.org'],
['Brockport Central School District', 'http://www.brockport.k12.ny.us/'],
['East Irondequoit Central School District', 'http://eicsd.k12.ny.us/'],
['East Rochester Union Free School District', 'http://www.erschools.org/'],
['Greece Central School District', 'http://web001.greece.k12.ny.us'],
['Rush-Henrietta Central School District', 'http://www.rhnet.org/'],
['Webster Central School District', 'http://www.websterschools.org'],
['West Irondequoit Central School District', 'http://www.westirondequoit.org/'],
['St Johnsville Central School District', 'http://sjcsd.org/'],
['Baldwin Union Free School District', 'http://www.baldwin.k12.ny.us/'],
['Bellmore Union Free School District', 'http://www.bellmore.k12.ny.us'],
['Bellmore-Merrick Central High School District', 'http://www.bellmore-merrick.k12.ny.us/', 'http://www.bellmore-merrick.k12.ny.us/district/opportunities', 'http://www.merrick.k12.ny.us/district/job_opportunities'],
['Carle Place Union Free School District', 'http://carle.ny.schoolwebpages.com/'],
['Elmont Union Free School District', 'http://www.elmontschools.org/', 'http://www.elmontschools.org/Page/381', 'https://www.ntschools.org//site/Default.aspx?PageID=5052'],
['Franklin Square Union Free School District', 'http://franklinsquare.k12.ny.us/'],
['Hicksville Union Free School District', 'http://www.hicksvillepublicschools.org/'],
['Jericho Union Free School District', 'http://www.bestschools.org/'],
['Lawrence Union Free School District', 'http://www.lawrence.org/'],
['Locust Valley Central School District', 'http://www.lvcsd.k12.ny.us/', 'http://www.vcsd.k12.ny.us/Page/114', 'https://www.pnwboces.org/olas/#!/default?ReturnUrl=%2Fteacherapplication%2F'],
['Lynbrook Union Free School District', 'http://www.lynbrook.k12.ny.us'],
['Manhasset Union Free School District', 'http://www.manhasset.k12.ny.us/'],
['Merrick Union Free School District', 'http://www.merrick-k6.org/'],
['North Merrick Union Free School District', 'http://www.nmerrickschools.org/'],
['Oceanside Union Free School District', 'http://www.oceanside.k12.ny.us/'],
['Plainview-Old Bethpage Central School District', 'http://www.pob.k12.ny.us/'],
['Roosevelt Union Free School District', 'http://www.rooseveltufsd.com/'],
['Wantagh Union Free School District', 'http://www.wms.wantaghufsd.k12.ny.us/'],
['Westbury Union Free School District', 'http://www.westburyschools.org/'],
['New York City District # 1', '_DUP._http://www.newyorkschools.com'],
['New York City District # 2', '_ERROR._url_not_found'],
['New York City District # 3', '_ERROR._url_not_found'],
['New York City District # 4', '_ERROR._url_not_found'],
['New York City District # 5', '_ERROR._url_not_found'],
['New York City District # 6', '_ERROR._url_not_found'],
['NYC Alternative High School District', '_ERROR._url_not_found'],
['NYC Special Schools - District 75', 'http://schools.nycenet.edu/d75/default.htm'],
['Niagara-Wheatfield Central School District', 'http://www.livestrong.com'],
['North Tonawanda City School District', 'http://www.ntschools.org/ntschools/site/default.asp'],
['Rome City School District', 'http://www.romecsd.org/'],
['Waterville Central School District', 'http://www.watervilleschools.org/'],
['Lyncourt Union Free School District', 'http://www.edline.net/pages/Lyncourt_School'],
['North Syracuse Central School District', 'http://www.nscsd.org/'],
['Gorham-Middlesex Central School District', '_ERROR._url_not_found'],
['Naples Central School District', 'http://www.naples.k12.ny.us/'],
['Chester Union Free School District', 'http://chester.ny.schoolwebpages.com/education/school/school.php?sectionid=2'],
['Greenwood Lake Union Free School District', 'http://gwl.ouboces.org/'],
['Kiryas Joel Village Union Free School District', '_ERROR._url_not_found'],
['Middletown City School District', 'http://www.middletowncityschools.org'],
['Tuxedo Union Free School District', 'http://www.tuxedoschooldistrict.com/'],
['Valley Central School District', 'http://www.vcsd.k12.ny.us/valleycentralsd/site/default.asp'],
['Lyndonville Central School District', 'http://www.lyndonvillecsd.org/'],
['Hannibal Central School District', 'http://www.hannibalcsd.org/'],
['Phoenix Central School District', 'http://www.phoenix.k12.ny.us/'],
['Sandy Creek Central School District', 'http://www.sccs.cnyric.org/'],
['Cooperstown Central School District', 'http://www.cooperstowncs.org/', 'http://www.owncs.org/about/employment', 'https://www.cooperstowncs.org/o/cooperstown-csd/page/employment-information--13'],
['Milford Central School District', 'http://www.schoolworld.milfordcentral.org/'],
['Morris Central School District', 'http://www.morriscs.org/'],
['Otego-Unadilla Central School District', 'http://www.unatego.org'],
['Schenevus Central School District', 'http://www.schenevuscs.org/'],
['Carmel Central School District', 'http://www.ccsd.k12.ny.us/'],
['New York City District #24', '_ERROR._url_not_found'],
['New York City District #25', '_ERROR._url_not_found'],
['New York City District #26', '_ERROR._url_not_found'],
['New York City District #27', '_ERROR._url_not_found'],
['New York City District #28', '_ERROR._url_not_found'],
['New York City District #29', '_ERROR._url_not_found'],
['New York City District #30', '_ERROR._url_not_found'],
['Brunswick Central School District', 'http://www.brittonkill.k12.ny.us'],
['East Greenbush Central School District', 'http://www.egcsd.org/'],
['Hoosick Falls Central School District', 'http://www.hoosick-falls.k12.ny.us'],
['North Greenbush Common School District', '_ERROR._url_not_found'],
['Troy City School District', 'http://www.troy.k12.ny.us/'],
['Staten Island Schools - NYC District #31', '_ERROR._url_not_found'],
['East Ramapo Central School District (Spring Valley)', 'http://www.eram.k12.ny.us'],
['Nanuet Union Free School District', 'http://nanunet.lhric.org/'],
['Nyack Union Free School District', 'http://www.nyackschools.com/'],
['Pearl River Union Free School District', 'http://www.pearlriver.k12.ny.us/'],
['Ramapo Central School District (Suffern)', 'http://www.ramapocentral.org/'],
['South Orangetown Central School District', 'http://www.socsd.k12.ny.us/'],
['Ballston Spa Central School District', 'http://www.ballstonspa.k12.ny.us/'],
['Burnt Hills-Ballston Lake Central School District', 'http://www.bhbl.org/'],
['Galway Central School District', 'http://www.galwaycsd.org/'],
['Stillwater Central School District', 'http://www.scsd.org/'],
['Waterford-Halfmoon Union Free School District', 'http://www.whufsd.org'],
['Duanesburg Central School District', 'http://dcs.neric.org/'],
['Niskayuna Central School District', 'http://www.niskyschools.org/'],
['Schalmont Central School District', 'http://www.schalmont.org/'],
['Schenectady City School District', 'http://www.schenectady.k12.ny.us/'],
['Scotia-Glenville Central School District', 'http://www.sgcsd.neric.org/'],
['Cobleskill-Richmondville Central School District', 'http://www.crcs.k12.ny.us/'],
['Middleburgh Central School District', 'http://www.middleburgh.k12.ny.us/'],
['Schoharie Central School District', 'http://www.schoharie.k12.ny.us/'],
['Watkins Glen Central School District', 'http://www.watkinsglenschools.com/'],
['Romulus Central School District', 'http://www.rcs.k12.ny.us/'],
['Canton Central School District', 'http://www.ccsdk12.org'],
['Clifton-Fine Central School District', 'http://www.cfeagles.org'],
['Colton-Pierrepont Central School District', 'http://www.cpcs.k12.ny.us'],
['Gouverneur Central School District', 'http://gcs.neric.org/'],
['Hammond Central School District', 'http://www.hammond.sllboces.org/'],
['Heuvelton Central School District', 'http://heuvelton.schoolfusion.us/'],
['Madrid-Waddington Central School District', 'http://www.mwcsk12.org/'],
['Morristown Central School District', 'http://mcsd.schoolfusion.us/'],
['Parishville-Hopkinton Central School District', 'http://phcs.neric.org/'],
['Arkport Central School District', 'http://acs.stev.net/'],
['Campbell-Savona Central School District', 'http://www.campbellsavona.wnyric.org/'],
['Canisteo-Greenwood Central School District', 'http://www.canisteo.wnyric.org/'],
['Jasper-Troupsburg Central School District', 'http://www.jt.wnyric.org/'],
['Prattsburgh Central School District', 'http://www.prattsburgh.wnyric.org/'],
['Wayland-Cohocton Central School District', 'http://www.wccsk12.org/'],
['Amagansett Union Free School District', 'http://www.amagansettschool.org/'],
['Brentwood Union Free School District', 'http://www.brentwood.k12.ny.us/'],
['Central Islip Union Free School District', 'http://www.centralislip.k12.ny.us/'],
['Connetquot Central School District', 'http://www.connetquot.k12.ny.us/'],
['East Hampton Union Free School District', 'http://www.easthampton.k12.ny.us/'],
['East Quogue Union Free School District', 'http://www.eastquogue.k12.ny.us/'],
['Fishers Island Union Free School District', 'http://www.fischool.com/'],
['Greenport Union Free School District', 'http://www.greenport.k12.ny.us/'],
['Hauppauge Union Free School District', 'http://www.hauppauge.k12.ny.us/'],
['Kings Park Central School District', 'http://www.kpcsd.k12.ny.us/'],
['Little Flower Union Free School District', 'http://www.littleflower.schoolfusion.us/'],
['Longwood Central School District', 'http://www.longwood.k12.ny.us/'],
['Mattituck-Cutchogue Union Free School District', 'http://www.mufsd.com/'],
['New Suffolk Common School District', 'http://newsuffolkschool.com'],
['Oysterponds Union Free School District', 'http://www.oysterponds.k12.ny.us/'],
['Patchogue-Medford Union Free School District', 'http://www.pat-med.k12.ny.us/'],
['Port Jefferson Union Free School District', 'http://portjefferson.ny.schoolwebpages.com/'],
['Quogue Union Free School District', 'http://www.quogue.k12.ny.us/'],
['Remsenburg-Speonk Union Free School District', 'http://rsufsd.wordpress.com/'],
['Rocky Point Union Free School District', 'http://www.rockypointschools.org/'],
['Sachem Central School District', 'http://www.sachem.edu/'],
['Sag Harbor Union Free School District', 'http://www.sagharbor.k12.ny.us/'],
['Sagaponack Common School District', 'http://www.sagaponackschool.com/'],
['Sayville Union Free School District', 'http://www.sayville.k12.ny.us/'],
['Shelter Island Union Free School District', 'http://sischool.dev6.hamptons.com/'],
['South Huntington Union Free School District', 'http://www.shuntington.k12.ny.us/'],
['Southold Union Free School District', 'http://www.southoldufsd.net/'],
['Springs Union Free School District', 'http://www.springs.k12.ny.us/'],
['Tuckahoe Common School District', 'http://www.tuckahoe.k12.ny.us/'],
['Wainscott Common School District', 'http://www.wainscottschool.com/'],
['West Babylon Union Free School District', 'http://www.westbabylon.k12.ny.us/'],
['Fallsburg Central School District', 'http://www.fallsburgcsd.net/'],
['Sullivan West Central School District', 'http://www.swcsd.org/', 'http://www.swcsd.org/Page/194', 'http://www.wcsd.org/district/employment_opportunities'],
['Tri-Valley Central School District', 'http://tvcs.k12.ny.us/'],
['Candor Central School District', 'http://www.candor.org/'],
['Newark Valley Central School District', 'http://nvcs.stier.org/'],
['Spencer-Van Etten Central School District', 'http://www.svecsd.org/'],
['Tioga Central School District', 'http://www.tcsaa.org/'],
['Dryden Central School District', 'http://www.dryden.k12.ny.us/'],
['George Junior Republic Union Free School District', 'http://www.georgejuniorrepublic.com/'],
['Ithaca City School District', 'http://www.icsd.k12.ny.us/'],
['Lansing Central School District', 'http://www.lansingschools.org/'],
['Newfield Central School District', 'http://www.newfieldschools.org/'],
['Trumansburg Central School District', 'http://www.tburg.k12.ny.us/'],
['Ellenville Central School District', 'http://www.ecs.k12.ny.us/'],
['Kingston City School District', 'http://www.kingstoncityschools.org/'],
['Onteora Central School District', 'http://www.onteora.k12.ny.us/'],
['Rondout Valley Central School District', 'http://www.rondout.k12.ny.us/'],
['Saugerties Central School District', 'http://saugerties.schoolwires.com/'],
['West Park Union Free School District', '_ERROR._url_not_found'],
['Bolton Central School District', 'http://www.boltoncsd.org/'],
['Glens Falls City School District', 'http://www.gfsd.org/'],
['Glens Falls Common School District', '_DUP._http://www.gfsd.org/'],
['Johnsburg Central School District', 'http://www.johnsburgcsd.org/'],
['Warrensburg Central School District', 'http://www.wcsd.org/'],
['Fort Edward Union Free School District', 'http://www.fortedward.org/'],
['Hudson Falls Central School District', 'http://www.hfcsd.org/'],
['Putnam Central School District', 'http://putnamcs.neric.org/'],
['Salem Central School District', 'http://www.salemcsd.org/'],
['Newark Central School District', 'http://www.newark.k12.ny.us/'],
['Wayne Central School District', 'http://wayne.k12.ny.us/'],
['Abbott Union Free School District', '_ERROR._url_not_found'],
['Blind Brook-Rye Union Free School District', 'http://www.blindbrook.org/'],
['Bronxville Union Free School District', 'http://www.bronxville.k12.ny.us/'],
['Chappaqua Central School District', 'http://www.chappaqua.k12.ny.us/'],
['Croton-Harmon Union Free School District', 'http://www.croton-harmonschools.org/'],
['Eastchester Union Free School District', 'http://www.eastchester.k12.ny.us/'],
['Elmsford Union Free School District', 'http://www.elmsfordschools.k12.ny.us'],
['Greenburgh Central School District', 'http://www.greenburgh.k12.ny.us/'],
['Greenburgh Eleven Union Free School District', '_ERROR._url_not_found'],
['Greenburgh-Graham Union Free School District', 'http://www.greenburghgraham.org/'],
['Greenburgh-North Castle Union Free School District', '_ERROR._url_not_found'],
['Hastings-On-Hudson Union Free School District', 'http://www.hastings.k12.ny.us/'],
['Mount Pleasant Cottage School District', 'http://www.mpcsny.org'],
['Mt Pleasant Central School District', 'http://www.mtplcsd.org'],
['Mt Pleasant-Blythedale Union Free School District', 'http://www.mpbschools.org/'],
['Ossining Union Free School District', 'http://www.ossiningufsd.org/', 'http://gufsd.org/district/employment-opportunities', 'https://ossiningufsd.org/departments/human-resources'],
['Pelham Union Free School District', 'http://www.pelhamschools.org/'],
['Pleasantville Union Free School District', 'http://www2.lhric.org/pleasantville/'],
['Rye City School District', 'http://www.ryecityschools.lhric.org/'],
['Rye Neck Union Free School District', 'http://www.ryeneck.k12.ny.us/default.aspx'],
['Somers Central School District', 'http://https://www.edline.net/pages/Somers_CSD'],
['Valhalla Union Free School', 'http://www.valhalla.k12.ny.us/'],
['White Plains City School District', 'http://www.wpcsd.k12.ny.us/'],
['Yorktown Central School District', 'http://www.yorktowncsd.org/'],
['Wyoming Central School District', 'http://www.wyoming.k12.ny.us/']
]






for grudb in grudb_list:
    sch = grudb[0].split(' Central School District')[0]
    sch = sch.split(' Union Free School')[0]
    sch = sch.split(' School District')[0]
    sch = sch.split(' Free School')[0]
    sch = sch.split(' UFSD')[0]




    for i in fin:

        if len(i) < 3:
            print('\n\n\n@@@@@ Bad len at:', i)
            continue

        if sch in i[0]:

            grudb.append(i[2])

            print('\n\n\n~~~~~~~:', grudb, '\n', i[0])

    #print(str(i.text), '\n', i.get('href'))









































