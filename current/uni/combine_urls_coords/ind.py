
# Desc: Combine URLs and coordinates for every Independent university

# Must use similar code to get each school type. eg: SUNY, CUNY, Independent, Proprietary

# URLs' HTML source: http://eservices.nysed.gov/collegedirectory/index.htm
# Coords source: http://eservices.nysed.gov/sedreports/list?id=1
# All Institutions: Active Institutions with GIS coordinates and OITS Accuracy Code - Select by County






from bs4 import BeautifulSoup
import pandas as pd



html = '''
<table>
 <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="A">A</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Academy For Jewish Religion<br/>
                        28 Wellls Ave<br/>
                        Yonkers, NY&nbsp;10701<br/>
                        <div id="phone0">&nbsp;</div>
                        
                        <a href="http://ajrsem.org">http://ajrsem.org</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone0").innerHTML = displayStaticPhoneNumber("9147090900") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Ora&nbsp;Horn Prouser,&nbsp;Executive Vp And Academic Dean<br/>
                        Graduate Programs Only<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Adelphi University<br/>
                        One South Avenue<br/>
                        Garden City, NY&nbsp;11530<br/>
                        <div id="phone1">&nbsp;</div>
                        
                        <a href="http://www.adelphi.edu">http://www.adelphi.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone1").innerHTML = displayStaticPhoneNumber("5168773231") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Christine&nbsp;Riordan,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Long Island Regents Region<br/>
                        Nassau County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Albany College of Pharmacy And Health Sciences<br/>
                        106 New Scotland Avenue<br/>
                        Albany, NY&nbsp;12208<br/>
                        <div id="phone2">&nbsp;</div>
                        
                        <a href="http://www.acphs.edu">http://www.acphs.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone2").innerHTML = displayStaticPhoneNumber("5186947200") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Greg&nbsp;Dewey,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Capital District Regents Region<br/>
                        Albany County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Albany Law School<br/>
                        80 New Scotland Avenue<br/>
                        Albany, NY&nbsp;12208<br/>
                        <div id="phone3">&nbsp;</div>
                        
                        <a href="http://www.albanylaw.edu">http://www.albanylaw.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone3").innerHTML = displayStaticPhoneNumber("5184452315") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Alicia&nbsp;Ouellette,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        Capital District Regents Region<br/>
                        Albany County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Albany Medical College<br/>
                        47 New Scotland Avenue<br/>
                        Albany, NY&nbsp;12208<br/>
                        <div id="phone4">&nbsp;</div>
                        
                        <a href="http://www.amc.edu">http://www.amc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone4").innerHTML = displayStaticPhoneNumber("5182623125") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Vincent&nbsp;Verdile,&nbsp;President<br/>
                        Graduate Programs Only<br/>
                        Capital District Regents Region<br/>
                        Albany County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Alfred University<br/>
                        One Saxon Dr<br/>
                        Alfred, NY&nbsp;14802<br/>
                        <div id="phone5">&nbsp;</div>
                        
                        <a href="http://www.alfred.edu">http://www.alfred.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone5").innerHTML = displayStaticPhoneNumber("6078712115") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Mark&nbsp;Zupan,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Western New York Regents Region<br/>
                        Allegany County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Amer Academy of Dramatic Arts<br/>
                        120 Madison Ave<br/>
                        New York, NY&nbsp;10016<br/>
                        <div id="phone6">&nbsp;</div>
                        
                        <a href="http://www.aada.edu">http://www.aada.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone6").innerHTML = displayStaticPhoneNumber("2126869244") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Susan&nbsp;Zech,&nbsp;Chief Executive Officer<br/>
                        2 Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        American Acad McAllister Inst<br/>
                        619 W 54 St<br/>
                        New York, NY&nbsp;10019<br/>
                        <div id="phone7">&nbsp;</div>
                        
                        <a href="http://www.funeraleducation.org">http://www.funeraleducation.org</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone7").innerHTML = displayStaticPhoneNumber("2127571190") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mrs.&nbsp;Tracy&nbsp;Lentz,&nbsp;Chief Executive Officer<br/>
                        2 Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="B">B</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Bank Street College of Education<br/>
                        610 W 112th St<br/>
                        New York, NY&nbsp;10025<br/>
                        <div id="phone8">&nbsp;</div>
                        
                        <a href="http://www.bankstreet.edu">http://www.bankstreet.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone8").innerHTML = displayStaticPhoneNumber("2128754467") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Shael&nbsp;Polakow-Suransky,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Bard College<br/>
                        Bard College<br/>
                        Annandale On Hudson, NY&nbsp;12504<br/>
                        <div id="phone9">&nbsp;</div>
                        
                        <a href="http://www.bard.edu">http://www.bard.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone9").innerHTML = displayStaticPhoneNumber("8457586822") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Leon&nbsp;Botstein,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Dutchess County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Bard College at Brooklyn Public Central Library<br/>
                        10 Grand Army Plaza<br/>
                        Brooklyn, NY&nbsp;11238<br/>
                        <div id="phone10">&nbsp;</div>
                        
                        <a href="http://bpi.bard.edu">http://bpi.bard.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone10").innerHTML = displayStaticPhoneNumber("8457587308") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Leon&nbsp;Botstein,&nbsp;President<br/>
                        2 Year Independent<br/>
                        New York City Regents Region<br/>
                        Kings County<br/>
                        Judicial District II
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Bard Grad Ctr For Decorative Arts<br/>
                        18 W 86th St<br/>
                        New York, NY&nbsp;10024<br/>
                        <div id="phone11">&nbsp;</div>
                        
                        <a href="http://www.bgc.bard.edu">http://www.bgc.bard.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone11").innerHTML = displayStaticPhoneNumber("2125013000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Leon&nbsp;Botstein,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Barnard College<br/>
                        3009 Broadway<br/>
                        New York, NY&nbsp;10027<br/>
                        <div id="phone12">&nbsp;</div>
                        
                        <a href="http://www.barnard.edu">http://www.barnard.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone12").innerHTML = displayStaticPhoneNumber("2128545262") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Sian&nbsp;Beilock,&nbsp;President<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Boricua College<br/>
                        3755 Broadway<br/>
                        New York, NY&nbsp;10032<br/>
                        <div id="phone13">&nbsp;</div>
                        
                        <a href="http://www.boricuacollege.edu">http://www.boricuacollege.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone13").innerHTML = displayStaticPhoneNumber("2126941000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Victor&nbsp;Alicea,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Boricua College - Bronx<br/>
                        890 Washington Ave<br/>
                        Bronx, NY&nbsp;10451<br/>
                        <div id="phone14">&nbsp;</div>
                        
                        <a href="http://www.boricuacollege.edu">http://www.boricuacollege.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone14").innerHTML = displayStaticPhoneNumber("3479648600") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Victor&nbsp;Alicea,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Bronx County<br/>
                        Judicial District XII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Boricua College - Brooklyn<br/>
                        9 Graham Ave<br/>
                        Brooklyn, NY&nbsp;11206<br/>
                        <div id="phone15">&nbsp;</div>
                        
                        <a href="http://www.boricuacollege.edu">http://www.boricuacollege.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone15").innerHTML = displayStaticPhoneNumber("2126941000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Victor&nbsp;Alicea,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Kings County<br/>
                        Judicial District II
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Brooklyn Law School<br/>
                        250 Joralemon Street<br/>
                        Brooklyn, NY&nbsp;11201<br/>
                        <div id="phone16">&nbsp;</div>
                        
                        <a href="http://www.brooklaw.edu">http://www.brooklaw.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone16").innerHTML = displayStaticPhoneNumber("7186252200") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Maryellen&nbsp;Fullerton,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        Kings County<br/>
                        Judicial District II
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="C">C</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Canisius College<br/>
                        2001 Main St<br/>
                        Buffalo, NY&nbsp;14208<br/>
                        <div id="phone17">&nbsp;</div>
                        
                        <a href="http://www.canisius.edu/">http://www.canisius.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone17").innerHTML = displayStaticPhoneNumber("7168882200") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;John&nbsp;Hurley,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Western New York Regents Region<br/>
                        Erie County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Cazenovia College<br/>
                        Cazenovia College<br/>
                        Cazenovia, NY&nbsp;13035<br/>
                        <div id="phone18">&nbsp;</div>
                        
                        <a href="http://WWW.CAZENOVIA.EDU">http://www.cazenovia.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone18").innerHTML = displayStaticPhoneNumber("8006543210") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Ronald&nbsp;Chesbrough,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Central New York Regents Region<br/>
                        Madison County<br/>
                        Judicial District VI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Christ the King Seminary<br/>
                        711 Knox Rd<br/>
                        East Aurora, NY&nbsp;14052<br/>
                        <div id="phone19">&nbsp;</div>
                        
                        <a href="http://www.cks.edu">http://www.cks.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone19").innerHTML = displayStaticPhoneNumber("7166528900") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Kevin&nbsp;Creagh,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        Western New York Regents Region<br/>
                        Erie County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        City Seminary of New York Graduate Center<br/>
                        302 West 119th St<br/>
                        New York, NY&nbsp;10026<br/>
                        <div id="phone20">&nbsp;</div>
                        
                        <a href="http://www.cityseminaryny.org">http://www.cityseminaryny.org</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone20").innerHTML = displayStaticPhoneNumber("2127492717") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Mark&nbsp;Gornik,&nbsp;President<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Clarkson University<br/>
                        8 Clarkson Ave<br/>
                        Potsdam, NY&nbsp;13699<br/>
                        <div id="phone21">&nbsp;</div>
                        
                        <a href="http://www.clarkson.edu/">http://www.clarkson.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone21").innerHTML = displayStaticPhoneNumber("3152686400") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Anthony&nbsp;Collins,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Northern Regents Region<br/>
                        Saint Lawrence County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Clarkson University Capital Region<br/>
                        80 Nott Terrace<br/>
                        Schenectady, NY&nbsp;12308<br/>
                        <div id="phone22">&nbsp;</div>
                        
                        <a href="http://www.clarkson.edu">http://www.clarkson.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone22").innerHTML = displayStaticPhoneNumber("5186319831") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Anthony&nbsp;Collins,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Capital District Regents Region<br/>
                        Schenectady County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Cochran Sch Nursing St John Rvrdl Ho<br/>
                        Andrus Pavilion<br/>
                        Yonkers, NY&nbsp;10701<br/>
                        <div id="phone23">&nbsp;</div>
                        
                        <a href="http://www.cochranschoolofnursing.us">http://www.cochranschoolofnursing.us</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone23").innerHTML = displayStaticPhoneNumber("9149644225") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Ron&nbsp;Corti,&nbsp;Chief Executive Officer<br/>
                        2 Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Cold Spring Harbor--watson School of Biological Sciences<br/>
                        Urey<br/>
                        Cold Spring Harbor, NY&nbsp;11724<br/>
                        <div id="phone24">&nbsp;</div>
                        
                        <a href="http://www.cshl.edu/gradschool">http://www.cshl.edu/gradschool</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone24").innerHTML = displayStaticPhoneNumber("5163676890") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Bruce&nbsp;Stillman,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        Long Island Regents Region<br/>
                        Nassau County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Colgate University<br/>
                        13 Oak Dr<br/>
                        Hamilton, NY&nbsp;13346<br/>
                        <div id="phone25">&nbsp;</div>
                        
                        <a href="http://www.colgate.edu">http://www.colgate.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone25").innerHTML = displayStaticPhoneNumber("3152281000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Brian&nbsp;Casey,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Central New York Regents Region<br/>
                        Madison County<br/>
                        Judicial District VI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Colgate-Rochester Divinity School<br/>
                        320 North Goodman St<br/>
                        Rochester, NY&nbsp;14607<br/>
                        <div id="phone26">&nbsp;</div>
                        
                        <a href="http://www.crcds.edu">http://www.crcds.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone26").innerHTML = displayStaticPhoneNumber("5852711320") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Angela&nbsp;Sims,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        Finger Lakes Regents Region<br/>
                        Monroe County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Coll New Rochelle Dist Coun 31 Cmps<br/>
                        140 Park Pl<br/>
                        New York, NY&nbsp;10007<br/>
                        <div id="phone27">&nbsp;</div>
                        
                        <a href="http://www.cnr.edu">http://www.cnr.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone27").innerHTML = displayStaticPhoneNumber("") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Stephen&nbsp;Sweeny,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Coll New Rochelle Rosa Parks Campus<br/>
                        144 W 125th St<br/>
                        New York, NY&nbsp;10027<br/>
                        <div id="phone28">&nbsp;</div>
                        
                        <a href="http://www.cnr.edu">http://www.cnr.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone28").innerHTML = displayStaticPhoneNumber("6467620167") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;William&nbsp;Latimer,&nbsp;President<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Coll of New Rochelle at NY Theo Semi<br/>
                        5 W 29th St<br/>
                        New York, NY&nbsp;10001<br/>
                        <div id="phone29">&nbsp;</div>
                        
                        <a href="http://www.cnr.edu">http://www.cnr.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone29").innerHTML = displayStaticPhoneNumber("") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Stephen&nbsp;Sweeny,&nbsp;President<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Coll of New Rochelle Brooklyn Campus<br/>
                        1368 Fulton St<br/>
                        Brooklyn, NY&nbsp;11216<br/>
                        <div id="phone30">&nbsp;</div>
                        
                        <a href="http://www.cnr.edu">http://www.cnr.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone30").innerHTML = displayStaticPhoneNumber("7186382500") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Dorothy&nbsp;Escribano,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Kings County<br/>
                        Judicial District II
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        College of Mt St Vincent<br/>
                        College of Mt St Vincent<br/>
                        Bronx, NY&nbsp;10471-1093<br/>
                        <div id="phone31">&nbsp;</div>
                        
                        <a href="http://www.mountsaintvincent.edu">http://www.mountsaintvincent.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone31").innerHTML = displayStaticPhoneNumber("7184053200") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Charles&nbsp;Flynn,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Bronx County<br/>
                        Judicial District XII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        College of New Rochelle<br/>
                        29 Castle Pl<br/>
                        New Rochelle, NY&nbsp;10805<br/>
                        <div id="phone32">&nbsp;</div>
                        
                        <a href="http://www.cnr.edu">http://www.cnr.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone32").innerHTML = displayStaticPhoneNumber("9146545000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;William&nbsp;Latimer,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        College of New Rochelle John Cardinal O'Connor Campus<br/>
                        332 E 149th St<br/>
                        Bronx, NY&nbsp;10451<br/>
                        <div id="phone33">&nbsp;</div>
                        
                        <a href="http://WWW.CNR.EDU">http://www.cnr.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone33").innerHTML = displayStaticPhoneNumber("7186651310") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;William&nbsp;Latimer,&nbsp;President<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Bronx County<br/>
                        Judicial District XII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        College of Saint Rose<br/>
                        432 Western Ave<br/>
                        Albany, NY&nbsp;12203<br/>
                        <div id="phone34">&nbsp;</div>
                        
                        <a href="http://WWW.STROSE.EDU">http://www.strose.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone34").innerHTML = displayStaticPhoneNumber("5184545111") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Carolyn&nbsp;Stefanco,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Capital District Regents Region<br/>
                        Albany County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Columbia University<br/>
                        535 West 116th St<br/>
                        New York, NY&nbsp;10027-7041<br/>
                        <div id="phone35">&nbsp;</div>
                        
                        <a href="http://WWW.COLUMBIA.EDU">http://www.columbia.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone35").innerHTML = displayStaticPhoneNumber("2128541754") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Lee&nbsp;Bollinger,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Concordia College<br/>
                        171 White Plains Rd<br/>
                        Bronxville, NY&nbsp;10708<br/>
                        <div id="phone36">&nbsp;</div>
                        
                        <a href="http://www.concordia-ny.edu">http://www.concordia-ny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone36").innerHTML = displayStaticPhoneNumber("9143379300") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Reverend&nbsp;John&nbsp;Nunes,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Cooper Union For the Advancement of Science And Art<br/>
                        30 Cooper Sq<br/>
                        New York, NY&nbsp;10003-7183<br/>
                        <div id="phone37">&nbsp;</div>
                        
                        <a href="http://www.cooper.edu">http://www.cooper.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone37").innerHTML = displayStaticPhoneNumber("2123534100") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Laura&nbsp;Sparks,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Cornell Univ Medical Campus<br/>
                        1300 York Ave<br/>
                        New York, NY&nbsp;10065<br/>
                        <div id="phone38">&nbsp;</div>
                        
                        <a href="http://www.weill.cornell.edu">http://www.weill.cornell.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone38").innerHTML = displayStaticPhoneNumber("2127461050") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Martha&nbsp;Pollack,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Cornell University<br/>
                        Day Hall<br/>
                        Ithaca, NY&nbsp;14853-4301<br/>
                        <div id="phone39">&nbsp;</div>
                        
                        <a href="http://WWW.CORNELL.EDU">http://www.cornell.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone39").innerHTML = displayStaticPhoneNumber("6072544636") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Martha&nbsp;Pollack,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Southern Tier Regents Region<br/>
                        Tompkins County<br/>
                        Judicial District VI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Cornell University - Cornellnyc Tech Campus<br/>
                        2 West Loop Rd<br/>
                        New York, NY&nbsp;10041<br/>
                        <div id="phone40">&nbsp;</div>
                        
                        <a href="http://tech.cornell.edu">http://tech.cornell.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone40").innerHTML = displayStaticPhoneNumber("6469713717") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Martha&nbsp;Pollack&nbsp;<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Crouse-Irving Memorial Hospital School of Nursing<br/>
                        736 Irving Ave<br/>
                        Syracuse, NY&nbsp;13210<br/>
                        <div id="phone41">&nbsp;</div>
                        
                        <a href="http://WWW.CROUSE.ORG/NURSING">http://www.crouse.org/nursing</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone41").innerHTML = displayStaticPhoneNumber("3154707481") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mrs.&nbsp;Patricia&nbsp;Morgan,&nbsp;Chief Executive Officer<br/>
                        2 Year Independent<br/>
                        Central New York Regents Region<br/>
                        Onondaga County<br/>
                        Judicial District V
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Culinary Institute of America 697<br/>
                        1946 Campus Dr<br/>
                        Hyde Park, NY&nbsp;12538<br/>
                        <div id="phone42">&nbsp;</div>
                        
                        <a href="http://www.ciachef.edu">http://www.ciachef.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone42").innerHTML = displayStaticPhoneNumber("8454529600") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Tim&nbsp;Ryan,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Dutchess County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="D">D</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        D'Youville College<br/>
                        320 Porter Ave<br/>
                        Buffalo, NY&nbsp;14201<br/>
                        <div id="phone43">&nbsp;</div>
                        
                        <a href="http://www.dyc.edu">http://www.dyc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone43").innerHTML = displayStaticPhoneNumber("7168297600") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Lorrie&nbsp;Clemo,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Western New York Regents Region<br/>
                        Erie County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Daemen College<br/>
                        4380 Main St<br/>
                        Amherst, NY&nbsp;14226<br/>
                        <div id="phone44">&nbsp;</div>
                        
                        <a href="http://www.daemen.edu">http://www.daemen.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone44").innerHTML = displayStaticPhoneNumber("7168393600") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Gary&nbsp;Olson,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Western New York Regents Region<br/>
                        Erie County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Davis College<br/>
                        1 Chrisfield Ave<br/>
                        Johnson City, NY&nbsp;13790<br/>
                        <div id="phone45">&nbsp;</div>
                        
                        <a href="http://www.davisny.edu">http://www.davisny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone45").innerHTML = displayStaticPhoneNumber("6077291581") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Doug&nbsp;Blanc,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Southern Tier Regents Region<br/>
                        Broome County<br/>
                        Judicial District VI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Dominican Coll of Blauvelt<br/>
                        470 Western Hwy<br/>
                        Orangeburg, NY&nbsp;10962-1210<br/>
                        <div id="phone46">&nbsp;</div>
                        
                        <a href="http://WWW.DC.EDU">http://www.dc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone46").innerHTML = displayStaticPhoneNumber("8453597800") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Mary Eileen&nbsp;O'Brien,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Rockland County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Dowling College<br/>
                        150 Idle Hour Blvd<br/>
                        Oakdale, NY&nbsp;11769<br/>
                        <div id="phone47">&nbsp;</div>
                        
                        <a href="http://WWW.DOWLING.EDU">http://www.dowling.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone47").innerHTML = displayStaticPhoneNumber("6312443000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Albert&nbsp;Inserra,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Long Island Regents Region<br/>
                        Suffolk County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Dowling College - Brookhaven Center<br/>
                        1300 William Floyd Parkway<br/>
                        Shirley, NY&nbsp;11967<br/>
                        <div id="phone48">&nbsp;</div>
                        
                        <a href="http://www.dowling.edu">http://www.dowling.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone48").innerHTML = displayStaticPhoneNumber("6312443000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Albert&nbsp;Inserra,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Long Island Regents Region<br/>
                        Suffolk County<br/>
                        Judicial District X
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="E">E</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Elim Bible Institute & College<br/>
                        7245 College St<br/>
                        Lima, NY&nbsp;14485<br/>
                        <div id="phone49">&nbsp;</div>
                        
                        <a href="http://www.elim.edu">http://www.elim.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone49").innerHTML = displayStaticPhoneNumber("5855821230") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Reverend&nbsp;Michael&nbsp;Cavanaugh,&nbsp;President<br/>
                        2 Year Independent<br/>
                        Finger Lakes Regents Region<br/>
                        Livingston County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Ellis Medicine-Thebelanger School of Nursing<br/>
                        650 McCellan St<br/>
                        Schenectady, NY&nbsp;12304<br/>
                        <div id="phone50">&nbsp;</div>
                        
                        <a href="http://www.ellisbelangerschoolofnursing.org">http://www.ellisbelangerschoolofnursing.org</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone50").innerHTML = displayStaticPhoneNumber("5188318810") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Marilyn&nbsp;Stapleton,&nbsp;Chief Executive Officer<br/>
                        2 Year Independent<br/>
                        Capital District Regents Region<br/>
                        Schenectady County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Elmira College<br/>
                        College Ave<br/>
                        Elmira, NY&nbsp;14901<br/>
                        <div id="phone51">&nbsp;</div>
                        
                        <a href="http://WWW.ELMIRA.EDU">http://www.elmira.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone51").innerHTML = displayStaticPhoneNumber("6077351800") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Charles&nbsp;Lindsay,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Southern Tier Regents Region<br/>
                        Chemung County<br/>
                        Judicial District VI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Elyon College<br/>
                        1400 W Sixth St<br/>
                        Brooklyn, NY&nbsp;11204<br/>
                        <div id="phone52">&nbsp;</div>
                        
                        <a href="http://www.elyon.edu">http://www.elyon.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone52").innerHTML = displayStaticPhoneNumber("7182595600") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Rabbi&nbsp;Chaim&nbsp;Waldman,&nbsp;President<br/>
                        2 Year Independent<br/>
                        New York City Regents Region<br/>
                        Kings County<br/>
                        Judicial District II
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Excelsior College<br/>
                        7 Columbia Cir<br/>
                        Albany, NY&nbsp;12203-5159<br/>
                        <div id="phone53">&nbsp;</div>
                        
                        <a href="http://www.excelsior.edu/">http://www.excelsior.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone53").innerHTML = displayStaticPhoneNumber("8886472388") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;James&nbsp;Baldwin,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Capital District Regents Region<br/>
                        Albany County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        The Elmezzi Graduate School of Molecular Medicine<br/>
                        350 Community Dr<br/>
                        Manhasset, NY&nbsp;11030<br/>
                        <div id="phone173">&nbsp;</div>
                        
                        <a href="http://www.elmezzigraduateschool.org/">http://www.elmezzigraduateschool.org/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone173").innerHTML = displayStaticPhoneNumber("5165621159") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Kevin&nbsp;Tracey,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        Long Island Regents Region<br/>
                        Nassau County<br/>
                        Judicial District X
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="F">F</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Fei Tian College<br/>
                        140 Galley Hill Rd<br/>
                        Cuddebackville, NY&nbsp;12729<br/>
                        <div id="phone54">&nbsp;</div>
                        
                        <a href="http://www.feitian.edu">http://www.feitian.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone54").innerHTML = displayStaticPhoneNumber("8456720550") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Vina&nbsp;Lee,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Orange County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Finger Lakes Health College of Nursing & Health Sciences<br/>
                        196 North St<br/>
                        Geneva, NY&nbsp;14456<br/>
                        <div id="phone55">&nbsp;</div>
                        
                        <a href="http://www.flhcon.edu">http://www.flhcon.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone55").innerHTML = displayStaticPhoneNumber("3157874003") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Jose&nbsp;Acevedo,&nbsp;Chief Executive Officer<br/>
                        2 Year Independent<br/>
                        Finger Lakes Regents Region<br/>
                        Ontario County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Fordham Univ (Rose Hill-Lincoln Ctr)<br/>
                        441 E Fordham Rd<br/>
                        Bronx, NY&nbsp;10458<br/>
                        <div id="phone56">&nbsp;</div>
                        
                        <a href="http://www.fordham.edu">http://www.fordham.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone56").innerHTML = displayStaticPhoneNumber("7188171000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Reverend&nbsp;Joseph&nbsp;McShane,&nbsp;President<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Bronx County<br/>
                        Judicial District XII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Fordham University - Westchester Campus<br/>
                        400 Westchester Ave<br/>
                        West Harrison, NY&nbsp;10604<br/>
                        <div id="phone57">&nbsp;</div>
                        
                        <a href="http://www.fordham.edu">http://www.fordham.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone57").innerHTML = displayStaticPhoneNumber("9143673426") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Reverend&nbsp;Joseph&nbsp;McShane,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="G">G</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Gamla College<br/>
                        1213 Elm Ave<br/>
                        Brooklyn, NY&nbsp;11230<br/>
                        <div id="phone58">&nbsp;</div>
                        
                        <a href="http://gamlacollege.com">http://gamlacollege.com</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone58").innerHTML = displayStaticPhoneNumber("7183394747") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Shlomo&nbsp;Teichman,&nbsp;Chief Executive Officer<br/>
                        2 Year Independent<br/>
                        New York City Regents Region<br/>
                        Kings County<br/>
                        Judicial District II
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        General Theological Seminary<br/>
                        440 West 21st St<br/>
                        New York, NY&nbsp;10011-9761<br/>
                        <div id="phone59">&nbsp;</div>
                        
                        <a href="http://WWW.GTS.EDU">http://www.gts.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone59").innerHTML = displayStaticPhoneNumber("2122435150") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Reverend&nbsp;Kurt&nbsp;Dunkle,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Glasgow Caledonian New York College<br/>
                        64 Wooster St<br/>
                        New York, NY&nbsp;10012<br/>
                        <div id="phone60">&nbsp;</div>
                        
                        <a href="http://https://www.gcnyc.com">http://https://www.gcnyc.com</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone60").innerHTML = displayStaticPhoneNumber("6467685300") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Pamela&nbsp;Gillies,&nbsp;President<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="H">H</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Hamilton College<br/>
                        198 College Hill Rd<br/>
                        Clinton, NY&nbsp;13323<br/>
                        <div id="phone61">&nbsp;</div>
                        
                        <a href="http://WWW.HAMILTON.EDU">http://www.hamilton.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone61").innerHTML = displayStaticPhoneNumber("3158594011") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;David&nbsp;Wippman,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Mohawk Valley Regents Region<br/>
                        Oneida County<br/>
                        Judicial District V
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Hartwick College<br/>
                        1 Hartwick College<br/>
                        Oneonta, NY&nbsp;13820<br/>
                        <div id="phone62">&nbsp;</div>
                        
                        <a href="http://WWW.HARTWICK.EDU">http://www.hartwick.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone62").innerHTML = displayStaticPhoneNumber("6074314000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Margaret&nbsp;Drugovich,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Mohawk Valley Regents Region<br/>
                        Otsego County<br/>
                        Judicial District VI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Hebrew Union College - Jewish Institute of Religion<br/>
                        1 W 4th St<br/>
                        New York, NY&nbsp;10012<br/>
                        <div id="phone63">&nbsp;</div>
                        
                        <a href="http://www.huc.edu">http://www.huc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone63").innerHTML = displayStaticPhoneNumber("2126745300") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Andrew&nbsp;Rehfeld,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Helene Fuld College of Nursing<br/>
                        24 E 120th  St<br/>
                        New York, NY&nbsp;10035<br/>
                        <div id="phone64">&nbsp;</div>
                        
                        <a href="http://www.helenefuld.edu">http://www.helenefuld.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone64").innerHTML = displayStaticPhoneNumber("2126167200") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Joyce&nbsp;Griffin-Sobel,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Hilbert College<br/>
                        5200 S Park Avenue<br/>
                        Hamburg, NY&nbsp;14075<br/>
                        <div id="phone65">&nbsp;</div>
                        
                        <a href="http://www.hilbert.edu">http://www.hilbert.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone65").innerHTML = displayStaticPhoneNumber("7166497900") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Michael&nbsp;Brophy,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Western New York Regents Region<br/>
                        Erie County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Hobart & Wm Smith Colleges<br/>
                        Hobart & Wm Smith Colleges<br/>
                        Geneva, NY&nbsp;14456<br/>
                        <div id="phone66">&nbsp;</div>
                        
                        <a href="http://WWW.HWS.EDU">http://www.hws.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone66").innerHTML = displayStaticPhoneNumber("3157813000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Joyce&nbsp;Jacobsen,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Finger Lakes Regents Region<br/>
                        Ontario County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Hofstra University-Main Campus<br/>
                        128 Hofstra University<br/>
                        Hempstead, NY&nbsp;11549<br/>
                        <div id="phone67">&nbsp;</div>
                        
                        <a href="http://WWW.HOFSTRA.EDU">http://www.hofstra.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone67").innerHTML = displayStaticPhoneNumber("5164636600") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Stuart&nbsp;Rabinowitz,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Long Island Regents Region<br/>
                        Nassau County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Holy Trinity Orthodox Seminary<br/>
                        1407 Robinson Rd<br/>
                        Jordanville, NY&nbsp;13361<br/>
                        <div id="phone68">&nbsp;</div>
                        
                        <a href="http://www.hts.edu">http://www.hts.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone68").innerHTML = displayStaticPhoneNumber("3158580945") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Reverend&nbsp;Luke&nbsp;Murianka,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Mohawk Valley Regents Region<br/>
                        Herkimer County<br/>
                        Judicial District V
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Houghton College<br/>
                        1 Willard Ave<br/>
                        Houghton, NY&nbsp;14744<br/>
                        <div id="phone69">&nbsp;</div>
                        
                        <a href="http://www.houghton.edu">http://www.houghton.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone69").innerHTML = displayStaticPhoneNumber("5855679200") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Shirley&nbsp;Mullen,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Western New York Regents Region<br/>
                        Allegany County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="I">I</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Inst of Design & Construction<br/>
                        141 Willoughby St<br/>
                        Brooklyn, NY&nbsp;11201<br/>
                        <div id="phone70">&nbsp;</div>
                        
                        <a href="http://www.idc.edu">http://www.idc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone70").innerHTML = displayStaticPhoneNumber("7188553661") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Vincent&nbsp;Battista,&nbsp;Chief Executive Officer<br/>
                        2 Year Independent<br/>
                        New York City Regents Region<br/>
                        Kings County<br/>
                        Judicial District II
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Iona College<br/>
                        715 North Ave<br/>
                        New Rochelle, NY&nbsp;10801<br/>
                        <div id="phone71">&nbsp;</div>
                        
                        <a href="http://www.iona.edu">http://www.iona.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone71").innerHTML = displayStaticPhoneNumber("9146332000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Seamus&nbsp;Carey,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Iona College Rockland Campus<br/>
                        1 Dutch Hill Rd<br/>
                        Orangeburg, NY&nbsp;10962<br/>
                        <div id="phone72">&nbsp;</div>
                        
                        <a href="http://www.iona.edu/rockland/">http://www.iona.edu/rockland/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone72").innerHTML = displayStaticPhoneNumber("8456201350") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Joseph&nbsp;Nyre,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Rockland County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Ithaca College<br/>
                        953 Danby Rd<br/>
                        Ithaca, NY&nbsp;14850-7002<br/>
                        <div id="phone73">&nbsp;</div>
                        
                        <a href="http://www.ithaca.edu">http://www.ithaca.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone73").innerHTML = displayStaticPhoneNumber("6072743124") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Shirley&nbsp;Collado,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Southern Tier Regents Region<br/>
                        Tompkins County<br/>
                        Judicial District VI
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="J">J</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Jewish Theological Semnry of America<br/>
                        3080 Broadway<br/>
                        New York, NY&nbsp;10027<br/>
                        <div id="phone74">&nbsp;</div>
                        
                        <a href="http://www.jtsa.edu">http://www.jtsa.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone74").innerHTML = displayStaticPhoneNumber("2126788000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Marc&nbsp;Gary,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        The Juilliard School<br/>
                        60 Lincoln Center Plz<br/>
                        New York, NY&nbsp;10023-6588<br/>
                        <div id="phone174">&nbsp;</div>
                        
                        <a href="http://www.juilliard.edu/">http://www.juilliard.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone174").innerHTML = displayStaticPhoneNumber("2127995000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Damian&nbsp;Woetzel,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="K">K</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Keuka College<br/>
                        Keuka College<br/>
                        Keuka Park, NY&nbsp;14478<br/>
                        <div id="phone75">&nbsp;</div>
                        
                        <a href="http://www.keuka.edu">http://www.keuka.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone75").innerHTML = displayStaticPhoneNumber("3152795000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Amy&nbsp;Storey,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Finger Lakes Regents Region<br/>
                        Yates County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Keuka College-Corning CC Campus<br/>
                        One Academic Dr<br/>
                        Corning, NY&nbsp;14830<br/>
                        <div id="phone76">&nbsp;</div>
                        
                        <a href="http://WWW.KEUKA.EDU">http://www.keuka.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone76").innerHTML = displayStaticPhoneNumber("3152795000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Amy&nbsp;Storey,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Southern Tier Regents Region<br/>
                        Steuben County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Keuka-Onondaga Community College Branch<br/>
                        Keuka College -Onondaga CC Branch<br/>
                        Syracuse, NY&nbsp;13215<br/>
                        <div id="phone77">&nbsp;</div>
                        
                        <a href="http://WWW.KEUKA.EDU">http://www.keuka.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone77").innerHTML = displayStaticPhoneNumber("3152795000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Amy&nbsp;Storey,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Central New York Regents Region<br/>
                        Onondaga County<br/>
                        Judicial District V
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        The King's College<br/>
                        56 Broadway<br/>
                        New York, NY&nbsp;10004<br/>
                        <div id="phone175">&nbsp;</div>
                        
                        <a href="http://WWW.TKC.EDU">http://www.tkc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone175").innerHTML = displayStaticPhoneNumber("2126597200") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Thomas&nbsp;Gibson,&nbsp;President<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="L">L</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Le Moyne College<br/>
                        1419 Salt Springs Rd<br/>
                        Syracuse, NY&nbsp;13214-1301<br/>
                        <div id="phone78">&nbsp;</div>
                        
                        <a href="http://www.lemoyne.edu">http://www.lemoyne.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone78").innerHTML = displayStaticPhoneNumber("3154454100") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Linda&nbsp;Le Mura,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Central New York Regents Region<br/>
                        Onondaga County<br/>
                        Judicial District V
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Long Island College Hospital Sch Nursing<br/>
                        530 Henry St<br/>
                        Brooklyn, NY&nbsp;11201<br/>
                        <div id="phone79">&nbsp;</div>
                        
                        <a href="http://">http://</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone79").innerHTML = displayStaticPhoneNumber("") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Nancy&nbsp;Dimauro,&nbsp;Chief Executive Officer<br/>
                        2 Year Independent<br/>
                        New York City Regents Region<br/>
                        Kings County<br/>
                        Judicial District II
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Long Island College Hospital School of Nursing<br/>
                        339 Hicks St<br/>
                        Brooklyn, NY&nbsp;11201<br/>
                        <div id="phone80">&nbsp;</div>
                        
                        <a href="http://www.futurenurselich.org">http://www.futurenurselich.org</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone80").innerHTML = displayStaticPhoneNumber("") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Nancy&nbsp;Dimauro,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Kings County<br/>
                        Judicial District II
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Long Island University - New York University Campus<br/>
                        E  H  Bobst Library<br/>
                        New York, NY&nbsp;10012<br/>
                        <div id="phone81">&nbsp;</div>
                        
                        <a href="http://WWW.LIU.EDU">http://www.liu.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone81").innerHTML = displayStaticPhoneNumber("5162993444") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Kimberly&nbsp;Cline,&nbsp;President<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Long Island University - Riverhead<br/>
                        121 Speonk -- Riverhead Rd<br/>
                        Riverhead, NY&nbsp;11901-3409<br/>
                        <div id="phone82">&nbsp;</div>
                        
                        <a href="http://www.liu.edu">http://www.liu.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone82").innerHTML = displayStaticPhoneNumber("6312878010") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Kimberly&nbsp;Cline,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Long Island Regents Region<br/>
                        Suffolk County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Long Island University Central Administration<br/>
                        700 Northern Blvd<br/>
                        Greenvale, NY&nbsp;11548<br/>
                        <div id="phone83">&nbsp;</div>
                        
                        <a href="http://www.liu.edu">http://www.liu.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone83").innerHTML = displayStaticPhoneNumber("5162992501") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;David&nbsp;Steinberg,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Long Island Regents Region<br/>
                        Nassau County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Long Island University-Brentwood Campus<br/>
                        1001 Crooked Hill Rd<br/>
                        Brentwood, NY&nbsp;11717<br/>
                        <div id="phone84">&nbsp;</div>
                        
                        <a href="http://liu.edu/brentwood">http://liu.edu/brentwood</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone84").innerHTML = displayStaticPhoneNumber("6312735112") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Kimberly&nbsp;Cline,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Long Island Regents Region<br/>
                        Suffolk County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Long Island University-Brooklyn Campus<br/>
                        1 Univ Plz<br/>
                        Brooklyn, NY&nbsp;11201<br/>
                        <div id="phone85">&nbsp;</div>
                        
                        <a href="http://WWW.LIU.EDU">http://www.liu.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone85").innerHTML = displayStaticPhoneNumber("7184881011") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Kimberly&nbsp;Cline,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Kings County<br/>
                        Judicial District II
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Long Island University-CW Post Campus<br/>
                        720 Northern Blvd<br/>
                        Brookville, NY&nbsp;11548<br/>
                        <div id="phone86">&nbsp;</div>
                        
                        <a href="http://WWW.LIU.EDU">http://www.liu.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone86").innerHTML = displayStaticPhoneNumber("5162992000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Kimberly&nbsp;Cline,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Long Island Regents Region<br/>
                        Nassau County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Long Island University-Southampton Campus<br/>
                        Montauk Hwy<br/>
                        Southampton, NY&nbsp;11968<br/>
                        <div id="phone87">&nbsp;</div>
                        
                        <a href="http://WWW.LIU.EDU">http://www.liu.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone87").innerHTML = displayStaticPhoneNumber("") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;David&nbsp;Steinberg,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Long Island Regents Region<br/>
                        Suffolk County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Long Island University-Westchester Campus<br/>
                        735 Anderson Hill Rd<br/>
                        Purchase, NY&nbsp;10577<br/>
                        <div id="phone88">&nbsp;</div>
                        
                        <a href="http://WWW.LIU.EDU">http://www.liu.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone88").innerHTML = displayStaticPhoneNumber("9148312700") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Kimberly&nbsp;Cline,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Louis V. Gerstner Grad Scho of Biomed Sci, Memorial Sloan-Kettering Cancer Center<br/>
                        1275 York Ave<br/>
                        New York, NY&nbsp;10021-6007<br/>
                        <div id="phone89">&nbsp;</div>
                        
                        <a href="http://WWW.SLOANKETTERING.EDU">http://www.sloankettering.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone89").innerHTML = displayStaticPhoneNumber("6468886639") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Craig&nbsp;Thompson,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="M">M</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Manhattan College<br/>
                        Riverdale<br/>
                        Bronx, NY&nbsp;10471<br/>
                        <div id="phone90">&nbsp;</div>
                        
                        <a href="http://WWW.MANHATTAN.EDU">http://www.manhattan.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone90").innerHTML = displayStaticPhoneNumber("7188628000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Brennan&nbsp;O'Donnell,&nbsp;President<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Bronx County<br/>
                        Judicial District XII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Manhattan School of Music<br/>
                        120 Claremont Ave<br/>
                        New York, NY&nbsp;10027-4698<br/>
                        <div id="phone91">&nbsp;</div>
                        
                        <a href="http://msmnyc.edu">http://msmnyc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone91").innerHTML = displayStaticPhoneNumber("9174934418") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;James&nbsp;Gandre,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Manhattanville College<br/>
                        Manhattanville College<br/>
                        Purchase, NY&nbsp;10577<br/>
                        <div id="phone92">&nbsp;</div>
                        
                        <a href="http://WWW.mville.EDU">http://www.mville.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone92").innerHTML = displayStaticPhoneNumber("9146942200") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Michael&nbsp;Geisler,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Maria College of Albany<br/>
                        700 New Scotland Ave<br/>
                        Albany, NY&nbsp;12208<br/>
                        <div id="phone93">&nbsp;</div>
                        
                        <a href="http://www.mariacollege.edu">http://www.mariacollege.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone93").innerHTML = displayStaticPhoneNumber("5184383111") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Thomas&nbsp;Gamble,&nbsp;Chief Executive Officer/Transitional Ldr<br/>
                        4-Year Independent<br/>
                        Capital District Regents Region<br/>
                        Albany County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Marist College<br/>
                        3399 North Road<br/>
                        Poughkeepsie, NY&nbsp;12601<br/>
                        <div id="phone94">&nbsp;</div>
                        
                        <a href="http://www.marist.edu">http://www.marist.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone94").innerHTML = displayStaticPhoneNumber("8455753000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Dennis&nbsp;Murray,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Dutchess County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Marymount Manhattan College<br/>
                        221 E 71 St<br/>
                        New York, NY&nbsp;10021<br/>
                        <div id="phone95">&nbsp;</div>
                        
                        <a href="http://WWW.MMM.EDU">http://www.mmm.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone95").innerHTML = displayStaticPhoneNumber("2125170400") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Kerry&nbsp;Walk,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Medaille College<br/>
                        18 Agassiz Cir<br/>
                        Buffalo, NY&nbsp;14214<br/>
                        <div id="phone96">&nbsp;</div>
                        
                        <a href="http://WWW.MEDAILLE.EDU">http://www.medaille.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone96").innerHTML = displayStaticPhoneNumber("7168802000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Kenneth&nbsp;Macur,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Western New York Regents Region<br/>
                        Erie County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Medaille College - Rochester Campus<br/>
                        18880 S Winton Rd, Ste 1<br/>
                        Rochester, NY&nbsp;14618<br/>
                        <div id="phone97">&nbsp;</div>
                        
                        <a href="http://WWW.MEDAILLE.EDU">http://www.medaille.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone97").innerHTML = displayStaticPhoneNumber("5852720030") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Kenneth&nbsp;Macur,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Finger Lakes Regents Region<br/>
                        Monroe County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Memorial Hospital School of Nursing<br/>
                        600 Northern Blvd<br/>
                        Albany, NY&nbsp;12204-1004<br/>
                        <div id="phone98">&nbsp;</div>
                        
                        <a href="http://www.sphp.com/sons">http://www.sphp.com/sons</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone98").innerHTML = displayStaticPhoneNumber("5184713260") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Patricia&nbsp;Cannistraci,&nbsp;Chief Executive Officer<br/>
                        2 Year Independent<br/>
                        Capital District Regents Region<br/>
                        Albany County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Mercy College<br/>
                        555 Broadway<br/>
                        Dobbs Ferry, NY&nbsp;10522<br/>
                        <div id="phone99">&nbsp;</div>
                        
                        <a href="http://WWW.MERCY.EDU">http://www.mercy.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone99").innerHTML = displayStaticPhoneNumber("8776372946") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Timothy&nbsp;Hall,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Mercy College - Manhattan Campus<br/>
                        47 W 34th St<br/>
                        New York, NY&nbsp;10001<br/>
                        <div id="phone100">&nbsp;</div>
                        
                        <a href="http://WWW.MERCY.EDU">http://www.mercy.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone100").innerHTML = displayStaticPhoneNumber("8776372946") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Timothy&nbsp;Hall,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Mercy College Bronx Campus<br/>
                        1200 Waters Pl<br/>
                        Bronx, NY&nbsp;10461<br/>
                        <div id="phone101">&nbsp;</div>
                        
                        <a href="http://WWW.MERCY.EDU">http://www.mercy.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone101").innerHTML = displayStaticPhoneNumber("8776372946") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Timothy&nbsp;Hall,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Bronx County<br/>
                        Judicial District XII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Mercy College-Yorktown Hts Campus<br/>
                        2651 Strang Blvd<br/>
                        Yorktown Heights, NY&nbsp;10598<br/>
                        <div id="phone102">&nbsp;</div>
                        
                        <a href="http://WWW.MERCY.EDU">http://www.mercy.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone102").innerHTML = displayStaticPhoneNumber("8776372946") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Timothy&nbsp;Hall,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Metropolitan College of New York<br/>
                        60 West St, 8th Fl<br/>
                        New York, NY&nbsp;10006<br/>
                        <div id="phone103">&nbsp;</div>
                        
                        <a href="http://https://www.mcny.edu">http://https://www.mcny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone103").innerHTML = displayStaticPhoneNumber("2123431234") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Joanne&nbsp;Passaro,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Metropolitan College of Ny-Brc<br/>
                        463 East 149th St<br/>
                        Bronx, NY&nbsp;10455<br/>
                        <div id="phone104">&nbsp;</div>
                        
                        <a href="http://https://www.mcny.edu/mcny-bronx/">http://https://www.mcny.edu/mcny-bronx/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone104").innerHTML = displayStaticPhoneNumber("2123431234") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Joanne&nbsp;Passaro,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Mid-America Baptist Theol Seminary - NE Branch<br/>
                        2810 Curry Rd Ext<br/>
                        Schenectady, NY&nbsp;12303-3463<br/>
                        <div id="phone105">&nbsp;</div>
                        
                        <a href="http://WWW.MABTSNE.EDU">http://www.mabtsne.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone105").innerHTML = displayStaticPhoneNumber("5183554000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Michael&nbsp;Haggard,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Capital District Regents Region<br/>
                        Albany County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Molloy College<br/>
                        1000 Hempstead Ave<br/>
                        Rockville Centre, NY&nbsp;11571-5002<br/>
                        <div id="phone106">&nbsp;</div>
                        
                        <a href="http://WWW.MOLLOY.EDU">http://www.molloy.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone106").innerHTML = displayStaticPhoneNumber("8884665569") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Drew&nbsp;Bogner,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Long Island Regents Region<br/>
                        Nassau County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Montefiore School of Nursing<br/>
                        53 Valentine St<br/>
                        Mount Vernon, NY&nbsp;10550-2009<br/>
                        <div id="phone107">&nbsp;</div>
                        
                        <a href="http://www.montefiorehealthsystem.org">http://www.montefiorehealthsystem.org</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone107").innerHTML = displayStaticPhoneNumber("9143616537") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Anthony&nbsp;Alfano,&nbsp;Chief Executive Officer<br/>
                        2 Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Mount Saint Mary College<br/>
                        330 Powell Ave<br/>
                        Newburgh, NY&nbsp;12550<br/>
                        <div id="phone108">&nbsp;</div>
                        
                        <a href="http://WWW.MSMC.EDU">http://www.msmc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone108").innerHTML = displayStaticPhoneNumber("8455610800") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Jason&nbsp;Adsit,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Orange County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Mt Sinai School of Medicine<br/>
                        1 Gustave L Levy Pl<br/>
                        New York, NY&nbsp;10029<br/>
                        <div id="phone109">&nbsp;</div>
                        
                        <a href="http://icahn.mssm.edu">http://icahn.mssm.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone109").innerHTML = displayStaticPhoneNumber("2122417006") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Dennis&nbsp;Charney,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="N">N</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Nazareth College of Rochester<br/>
                        4245 East Ave<br/>
                        Rochester, NY&nbsp;14618<br/>
                        <div id="phone110">&nbsp;</div>
                        
                        <a href="http://www.naz.edu">http://www.naz.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone110").innerHTML = displayStaticPhoneNumber("5853892525") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Daan&nbsp;Braveman,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Finger Lakes Regents Region<br/>
                        Monroe County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New School University - NYS Office of Mental Health<br/>
                        44 Holland Ave<br/>
                        Albany, NY&nbsp;12229<br/>
                        <div id="phone111">&nbsp;</div>
                        
                        <a href="http://www.newschool.edu/">http://www.newschool.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone111").innerHTML = displayStaticPhoneNumber("") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Robert&nbsp;Kerrey&nbsp;<br/>
                        4-Year Independent<br/>
                        Capital District Regents Region<br/>
                        Albany County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York College of Health Professions<br/>
                        6801 Jericho Tpke<br/>
                        Syosset, NY&nbsp;11791<br/>
                        <div id="phone112">&nbsp;</div>
                        
                        <a href="http://www.nycollege.edu">http://www.nycollege.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone112").innerHTML = displayStaticPhoneNumber("5163640808") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;A Li&nbsp;Song,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Long Island Regents Region<br/>
                        Nassau County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York College of Podiatric Medicine<br/>
                        53 E 124 St<br/>
                        New York, NY&nbsp;10035<br/>
                        <div id="phone113">&nbsp;</div>
                        
                        <a href="http://www.nycpm.edu">http://www.nycpm.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone113").innerHTML = displayStaticPhoneNumber("2124108000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Louis&nbsp;Levine,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York College of Traditional Chinese Medicine<br/>
                        200 Old Country Rd, Ste 500<br/>
                        Mineola, NY&nbsp;11501<br/>
                        <div id="phone114">&nbsp;</div>
                        
                        <a href="http://www.nyctcm.edu">http://www.nyctcm.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone114").innerHTML = displayStaticPhoneNumber("5167391545") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Yemeng&nbsp;Chen,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Long Island Regents Region<br/>
                        Nassau County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York Graduate School of Psychoanalysis<br/>
                        16 West 10th  St<br/>
                        New York, NY&nbsp;10011<br/>
                        <div id="phone115">&nbsp;</div>
                        
                        <a href="http://www.nygsp.bgsp.edu/">http://www.nygsp.bgsp.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone115").innerHTML = displayStaticPhoneNumber("2122607050") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Jane&nbsp;Snyder,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York Institute For Technology-Manhattan Campus<br/>
                        1855 Broadway<br/>
                        New York, NY&nbsp;10023<br/>
                        <div id="phone116">&nbsp;</div>
                        
                        <a href="http://www.nyit.edu">http://www.nyit.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone116").innerHTML = displayStaticPhoneNumber("2122611500") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Henry&nbsp;Foley,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York Institute of Technology - Islip Campus<br/>
                        Carleton Ave<br/>
                        Central Islip, NY&nbsp;11722<br/>
                        <div id="phone117">&nbsp;</div>
                        
                        <a href="http://www.nyit.edu">http://www.nyit.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone117").innerHTML = displayStaticPhoneNumber("8005736948") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Rahmat&nbsp;Shoureshi,&nbsp;Dean<br/>
                        4-Year Independent<br/>
                        Long Island Regents Region<br/>
                        Suffolk County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York Institute of Technology Old Westbury Campus<br/>
                        Po Box 8000<br/>
                        Old Westbury, NY&nbsp;11568<br/>
                        <div id="phone118">&nbsp;</div>
                        
                        <a href="http://www.nyit.edu">http://www.nyit.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone118").innerHTML = displayStaticPhoneNumber("5166861000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Henry&nbsp;Foley,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Long Island Regents Region<br/>
                        Nassau County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York Law School<br/>
                        185 W Broadway<br/>
                        New York, NY&nbsp;10013-2921<br/>
                        <div id="phone119">&nbsp;</div>
                        
                        <a href="http://www.nyls.edu">http://www.nyls.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone119").innerHTML = displayStaticPhoneNumber("2124312100") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Anthony&nbsp;Crowell,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York Studio School<br/>
                        8 W 8th St<br/>
                        New York, NY&nbsp;10011<br/>
                        <div id="phone120">&nbsp;</div>
                        
                        <a href="http://WWW.NYSS.ORG">http://www.nyss.org</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone120").innerHTML = displayStaticPhoneNumber("2126736466") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Graham&nbsp;Nickson,&nbsp;Dean<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York Theological Seminary<br/>
                        475 Riverside Dr, Ste 500<br/>
                        New York, NY&nbsp;10115<br/>
                        <div id="phone121">&nbsp;</div>
                        
                        <a href="http://www.nyts.edu">http://www.nyts.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone121").innerHTML = displayStaticPhoneNumber("2128701211") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Dale&nbsp;Irvin,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York University<br/>
                        70 Washington Square South<br/>
                        New York, NY&nbsp;10012<br/>
                        <div id="phone122">&nbsp;</div>
                        
                        <a href="http://www.nyu.edu">http://www.nyu.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone122").innerHTML = displayStaticPhoneNumber("2129981212") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Andrew&nbsp;Hamilton,&nbsp;President<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York University - St. Thomas Aquinas College<br/>
                        125 Route 340<br/>
                        Sparkill, NY&nbsp;10976<br/>
                        <div id="phone123">&nbsp;</div>
                        
                        <a href="http://www.nyu.edu">http://www.nyu.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone123").innerHTML = displayStaticPhoneNumber("8453596084") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Andrew&nbsp;Hamilton,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Rockland County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York University at Manhattanville College<br/>
                        NYU at Manhattanville<br/>
                        Purchase, NY&nbsp;10577<br/>
                        <div id="phone124">&nbsp;</div>
                        
                        <a href="http://www.nyu.edu">http://www.nyu.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone124").innerHTML = displayStaticPhoneNumber("") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;John&nbsp;Sexton,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Niagara University<br/>
                        Niagara University<br/>
                        Niagara University, NY&nbsp;14109<br/>
                        <div id="phone125">&nbsp;</div>
                        
                        <a href="http://www.niagara.edu">http://www.niagara.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone125").innerHTML = displayStaticPhoneNumber("8004622111") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Reverend&nbsp;James&nbsp;Maher,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Western New York Regents Region<br/>
                        Niagara County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Northeaster Seminary at Roberts Wesleyan College<br/>
                        2265 Westside Dr<br/>
                        Rochester, NY&nbsp;14624-1997<br/>
                        <div id="phone126">&nbsp;</div>
                        
                        <a href="http://www.nes.edu/">http://www.nes.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone126").innerHTML = displayStaticPhoneNumber("5855946802") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Deana&nbsp;Porterfield,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        Finger Lakes Regents Region<br/>
                        Monroe County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        NY Chiropractic College<br/>
                        2360 State Rt 89<br/>
                        Seneca Falls, NY&nbsp;13148<br/>
                        <div id="phone127">&nbsp;</div>
                        
                        <a href="http://www.nycc.edu">http://www.nycc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone127").innerHTML = displayStaticPhoneNumber("3155683000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Michael&nbsp;Mestan,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Finger Lakes Regents Region<br/>
                        Seneca County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        NY Medical College<br/>
                        Administration Bldg<br/>
                        Valhalla, NY&nbsp;10595<br/>
                        <div id="phone128">&nbsp;</div>
                        
                        <a href="http://www.nymc.edu">http://www.nymc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone128").innerHTML = displayStaticPhoneNumber("9145944495") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Edward&nbsp;Halperin,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        NY School of Interior Design<br/>
                        170 E 70th St<br/>
                        New York, NY&nbsp;10021<br/>
                        <div id="phone129">&nbsp;</div>
                        
                        <a href="http://www.nysid.edu">http://www.nysid.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone129").innerHTML = displayStaticPhoneNumber("2124721500") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;David&nbsp;Sprouls,&nbsp;President<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Nyack College<br/>
                        1 S Blvd<br/>
                        Nyack, NY&nbsp;10960<br/>
                        <div id="phone130">&nbsp;</div>
                        
                        <a href="http://www.nyack.edu">http://www.nyack.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone130").innerHTML = displayStaticPhoneNumber("8456754400") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Michael&nbsp;Scales,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Rockland County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        The New School<br/>
                        66 W 12th St<br/>
                        New York, NY&nbsp;10012<br/>
                        <div id="phone176">&nbsp;</div>
                        
                        <a href="http://www.newschool.edu/">http://www.newschool.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone176").innerHTML = displayStaticPhoneNumber("2122295600") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;David&nbsp;Van Zandt,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        The New York Academy of Art<br/>
                        111 Franklin St<br/>
                        New York, NY&nbsp;10013<br/>
                        <div id="phone177">&nbsp;</div>
                        
                        <a href="http://www.nyaa.edu">http://www.nyaa.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone177").innerHTML = displayStaticPhoneNumber("2129660300") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;David&nbsp;Kratz,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
    </tbody>
</table>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="P">P</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Pace University - NYC Campus<br/>
                        1 Pace Plaza<br/>
                        New York, NY&nbsp;10038-1502<br/>
                        <div id="phone131">&nbsp;</div>
                        
                        <a href="http://www.pace.edu">http://www.pace.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone131").innerHTML = displayStaticPhoneNumber("8667223338") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Marvin&nbsp;Krislov,&nbsp;President<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Pace University College at White Plains<br/>
                        78 N Broadway<br/>
                        White Plains, NY&nbsp;10603<br/>
                        <div id="phone132">&nbsp;</div>
                        
                        <a href="http://www.pace.edu">http://www.pace.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone132").innerHTML = displayStaticPhoneNumber("8008747223") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Marvin&nbsp;Krislov,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Pace University Pleasantville<br/>
                        861 Bedford Rd<br/>
                        Pleasantville, NY&nbsp;10570<br/>
                        <div id="phone133">&nbsp;</div>
                        
                        <a href="http://www.pace.edu">http://www.pace.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone133").innerHTML = displayStaticPhoneNumber("8008747223") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Marvin&nbsp;Krislov,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Paul Smiths College<br/>
                        Paul Smith's College<br/>
                        Paul Smiths, NY&nbsp;12970<br/>
                        <div id="phone134">&nbsp;</div>
                        
                        <a href="http://www.paulsmiths.edu">http://www.paulsmiths.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone134").innerHTML = displayStaticPhoneNumber("5183276000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Cathy&nbsp;Dove,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Northern Regents Region<br/>
                        Franklin County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Phillips Beth Israel Sch of Nursing<br/>
                        776 6th Ave, 4th Fl<br/>
                        New York, NY&nbsp;10001-6354<br/>
                        <div id="phone135">&nbsp;</div>
                        
                        <a href="http://www.pson.edu">http://www.pson.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone135").innerHTML = displayStaticPhoneNumber("2126146110") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Todd&nbsp;Ambrosia,&nbsp;Chief Executive Officer<br/>
                        2 Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Polytechnic Inst of NY - Westchester Campus<br/>
                        36 Saw Mill River Rd<br/>
                        Hawthorne, NY&nbsp;10532<br/>
                        <div id="phone136">&nbsp;</div>
                        
                        <a href="http://www.poly.edu/">http://www.poly.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone136").innerHTML = displayStaticPhoneNumber("9143232000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Katepalli&nbsp;Sreenivasan,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Polytechnic Institute of NY - Main Campus<br/>
                        Six Metrotech Ctr<br/>
                        Brooklyn, NY&nbsp;11201<br/>
                        <div id="phone137">&nbsp;</div>
                        
                        <a href="http://www.poly.edu/">http://www.poly.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone137").innerHTML = displayStaticPhoneNumber("7182603600") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Katepalli&nbsp;Sreenivasan,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Kings County<br/>
                        Judicial District II
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Polytechnic Institute of NYU - Long Island Center<br/>
                        Rt 110<br/>
                        Farmingdale, NY&nbsp;11735<br/>
                        <div id="phone138">&nbsp;</div>
                        
                        <a href="http://www.poly.edu/">http://www.poly.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone138").innerHTML = displayStaticPhoneNumber("7182603600") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Katepalli&nbsp;Sreenivasan,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Long Island Regents Region<br/>
                        Nassau County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Pratt Institute<br/>
                        200 Willoughby Ave<br/>
                        Brooklyn, NY&nbsp;11205<br/>
                        <div id="phone139">&nbsp;</div>
                        
                        <a href="http://www.pratt.edu">http://www.pratt.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone139").innerHTML = displayStaticPhoneNumber("7186363646") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Frances&nbsp;Bronet,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Kings County<br/>
                        Judicial District II
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Pratt Institute Manhattan Center<br/>
                        144 West 14th St<br/>
                        New York, NY&nbsp;10011<br/>
                        <div id="phone140">&nbsp;</div>
                        
                        <a href="http://www.pratt.edu">http://www.pratt.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone140").innerHTML = displayStaticPhoneNumber("8003310834") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Frances&nbsp;Bronet,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Professional Business College<br/>
                        408 Broadway<br/>
                        New York, NY&nbsp;10002<br/>
                        <div id="phone141">&nbsp;</div>
                        
                        <a href="http://www.pbcny.edu">http://www.pbcny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone141").innerHTML = displayStaticPhoneNumber("2122267300") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Leon&nbsp;Lee,&nbsp;Chief Executive Officer<br/>
                        2 Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
    </tbody>
</table>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="R">R</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Rabbi Isaac Elchanan Theo Seminary<br/>
                        2540 Amsterdam Ave<br/>
                        New York, NY&nbsp;10033<br/>
                        <div id="phone142">&nbsp;</div>
                        
                        <a href="http://www.yu.edu/riets/">http://www.yu.edu/riets/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone142").innerHTML = displayStaticPhoneNumber("2129605224") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Ari&nbsp;Berman,&nbsp;President<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Relay School of Education<br/>
                        25 Broadway, 3rd Fl<br/>
                        New York, NY&nbsp;10004<br/>
                        <div id="phone143">&nbsp;</div>
                        
                        <a href="http://www.relay.edu">http://www.relay.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone143").innerHTML = displayStaticPhoneNumber("2122281888") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Pamela&nbsp;Inbasekaran,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Rensselaer Polytech Institute<br/>
                        Rensselaer Polytech Inst<br/>
                        Troy, NY&nbsp;12180-3590<br/>
                        <div id="phone144">&nbsp;</div>
                        
                        <a href="http://www.rpi.edu">http://www.rpi.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone144").innerHTML = displayStaticPhoneNumber("5182766000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Shirley&nbsp;Jackson,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Capital District Regents Region<br/>
                        Rensselaer County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Roberts Wesleyan College<br/>
                        2301 Westside Dr<br/>
                        Rochester, NY&nbsp;14624<br/>
                        <div id="phone145">&nbsp;</div>
                        
                        <a href="http://www.roberts.edu">http://www.roberts.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone145").innerHTML = displayStaticPhoneNumber("8007774792") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Deana&nbsp;Porterfield,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Finger Lakes Regents Region<br/>
                        Monroe County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Rochester Institute of Technology<br/>
                        1 Lomb Memorial Dr<br/>
                        Rochester, NY&nbsp;14623-5603<br/>
                        <div id="phone146">&nbsp;</div>
                        
                        <a href="http://www.rit.edu">http://www.rit.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone146").innerHTML = displayStaticPhoneNumber("5854752411") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;David&nbsp;Munson,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Finger Lakes Regents Region<br/>
                        Monroe County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Rockefeller University<br/>
                        1230 York Ave<br/>
                        New York, NY&nbsp;10065-6399<br/>
                        <div id="phone147">&nbsp;</div>
                        
                        <a href="http://www.rockefeller.edu/">http://www.rockefeller.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone147").innerHTML = displayStaticPhoneNumber("2123278000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Richard&nbsp;Lifton,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="S">S</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Saint Joseph's Seminary And College<br/>
                        Dunwoodie<br/>
                        Yonkers, NY&nbsp;10704-1896<br/>
                        <div id="phone148">&nbsp;</div>
                        
                        <a href="http://https://dunwoodie.edu/">http://https://dunwoodie.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone148").innerHTML = displayStaticPhoneNumber("9149686200") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Father&nbsp;Peter&nbsp;Vaccari,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Saint Lawrence University<br/>
                        St. Lawrence University<br/>
                        Canton, NY&nbsp;13617<br/>
                        <div id="phone149">&nbsp;</div>
                        
                        <a href="http://www.stlawu.edu">http://www.stlawu.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone149").innerHTML = displayStaticPhoneNumber("3152295011") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;William&nbsp;Fox,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Northern Regents Region<br/>
                        Saint Lawrence County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Salvation Army College For Officer Training<br/>
                        201 Lafayette Ave<br/>
                        Suffern, NY&nbsp;10901<br/>
                        <div id="phone150">&nbsp;</div>
                        
                        <a href="http://www.tsacfotny.edu">http://www.tsacfotny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone150").innerHTML = displayStaticPhoneNumber("8453573501") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;David&nbsp;Kelly,&nbsp;Chief Executive Officer<br/>
                        2 Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Rockland County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Samaritan Hospital School of Nursing<br/>
                        1300 Massachusetts Ave<br/>
                        Troy, NY&nbsp;12180<br/>
                        <div id="phone151">&nbsp;</div>
                        
                        <a href="http://sphp.com/son">http://sphp.com/son</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone151").innerHTML = displayStaticPhoneNumber("5182685010") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Patricia&nbsp;Cannistraci,&nbsp;Chief Executive Officer<br/>
                        2 Year Independent<br/>
                        Capital District Regents Region<br/>
                        Rensselaer County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Sarah Lawrence College<br/>
                        Sarah Lawrence College<br/>
                        Bronxville, NY&nbsp;10708<br/>
                        <div id="phone152">&nbsp;</div>
                        
                        <a href="http://www.sarahlawrence.edu">http://www.sarahlawrence.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone152").innerHTML = displayStaticPhoneNumber("9143370700") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Cristle&nbsp;Judd,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Siena College<br/>
                        515 Loudon Rd<br/>
                        Loudonville, NY&nbsp;12211<br/>
                        <div id="phone153">&nbsp;</div>
                        
                        <a href="http://www.siena.edu/">http://www.siena.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone153").innerHTML = displayStaticPhoneNumber("5187832300") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Margaret&nbsp;Madden,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Capital District Regents Region<br/>
                        Albany County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Skidmore College<br/>
                        815 North Broadway<br/>
                        Saratoga Springs, NY&nbsp;12866<br/>
                        <div id="phone154">&nbsp;</div>
                        
                        <a href="http://www.skidmore.edu">http://www.skidmore.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone154").innerHTML = displayStaticPhoneNumber("5185805000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Phillip&nbsp;Glotzbach,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Capital District Regents Region<br/>
                        Saratoga County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        St Bonaventure University<br/>
                        3261 W State Rd<br/>
                        Saint Bonaventure, NY&nbsp;14778<br/>
                        <div id="phone155">&nbsp;</div>
                        
                        <a href="http://www.sbu.edu">http://www.sbu.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone155").innerHTML = displayStaticPhoneNumber("7163752000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Dennis&nbsp;Deperro,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Western New York Regents Region<br/>
                        Cattaraugus County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        St Elizabeth Hospital College of Nursing<br/>
                        2215 Genesee St<br/>
                        Utica, NY&nbsp;13501<br/>
                        <div id="phone156">&nbsp;</div>
                        
                        <a href="http://www.secon.edu">http://www.secon.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone156").innerHTML = displayStaticPhoneNumber("3158018253") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mrs.&nbsp;Varinya&nbsp;Sheppard,&nbsp;Chief Executive Officer<br/>
                        2 Year Independent<br/>
                        Mohawk Valley Regents Region<br/>
                        Oneida County<br/>
                        Judicial District V
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        St Francis College<br/>
                        180 Remsen St<br/>
                        Brooklyn, NY&nbsp;11201<br/>
                        <div id="phone157">&nbsp;</div>
                        
                        <a href="http://www.sfc.edu">http://www.sfc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone157").innerHTML = displayStaticPhoneNumber("7185222300") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Miguel&nbsp;Martinez Saenz,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Kings County<br/>
                        Judicial District II
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        St John Fisher College<br/>
                        3690 East Ave<br/>
                        Rochester, NY&nbsp;14618-3597<br/>
                        <div id="phone158">&nbsp;</div>
                        
                        <a href="http://www.sjfc.edu">http://www.sjfc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone158").innerHTML = displayStaticPhoneNumber("5853858000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Gerard&nbsp;Rooney,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Finger Lakes Regents Region<br/>
                        Monroe County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        St Johns University-Staten Island<br/>
                        300 Howard Ave<br/>
                        Staten Island, NY&nbsp;10301<br/>
                        <div id="phone159">&nbsp;</div>
                        
                        <a href="http://www.stjohns.edu">http://www.stjohns.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone159").innerHTML = displayStaticPhoneNumber("7183904545") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Conrado&nbsp;Gempesaw,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Richmond County<br/>
                        Judicial District Xiii
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        St Joseph's College<br/>
                        245 Clinton Ave<br/>
                        Brooklyn, NY&nbsp;11205<br/>
                        <div id="phone160">&nbsp;</div>
                        
                        <a href="http://www.sjcny.edu">http://www.sjcny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone160").innerHTML = displayStaticPhoneNumber("7189405300") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Donald&nbsp;Boomgaarden,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Kings County<br/>
                        Judicial District II
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        St Joseph's College - Suffolk Campus<br/>
                        155 W Roe Blvd<br/>
                        Patchogue, NY&nbsp;11772<br/>
                        <div id="phone161">&nbsp;</div>
                        
                        <a href="http://www.sjcny.edu">http://www.sjcny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone161").innerHTML = displayStaticPhoneNumber("6316875100") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Donald&nbsp;Boomgaarden,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Long Island Regents Region<br/>
                        Suffolk County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        St Joseph's College of Nursing at St Joseph's Hospital Health Center<br/>
                        206 Prospect Pl<br/>
                        Syracuse, NY&nbsp;13203-0<br/>
                        <div id="phone162">&nbsp;</div>
                        
                        <a href="http://https://www.sjhcon.edu/">http://https://www.sjhcon.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone162").innerHTML = displayStaticPhoneNumber("3154485040") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Leslie&nbsp;Luke,&nbsp;Chief Executive Officer<br/>
                        2 Year Independent<br/>
                        Central New York Regents Region<br/>
                        Onondaga County<br/>
                        Judicial District V
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        St Thomas Aquinas College<br/>
                        Rt 340<br/>
                        Sparkill, NY&nbsp;10976<br/>
                        <div id="phone163">&nbsp;</div>
                        
                        <a href="http://www.stac.edu">http://www.stac.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone163").innerHTML = displayStaticPhoneNumber("8453984100") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Margaret&nbsp;Fitzpatrick, Sc,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Rockland County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        St Vladimir's Orthodox Theol Seminry<br/>
                        575 Scarsdale Rd<br/>
                        Yonkers, NY&nbsp;10707<br/>
                        <div id="phone164">&nbsp;</div>
                        
                        <a href="http://www.svots.edu/">http://www.svots.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone164").innerHTML = displayStaticPhoneNumber("9149618313") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Reverend&nbsp;Chad&nbsp;Hatfield,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        St. Bernard's School of Theology And Ministry<br/>
                        120 French Rd<br/>
                        Rochester, NY&nbsp;14618<br/>
                        <div id="phone165">&nbsp;</div>
                        
                        <a href="http://WWW.STBERNARDS.EDU">http://www.stbernards.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone165").innerHTML = displayStaticPhoneNumber("5852713657") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Stephen&nbsp;Loughlin,&nbsp;President<br/>
                        Graduate Programs Only<br/>
                        Finger Lakes Regents Region<br/>
                        Monroe County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        St. John's University<br/>
                        8000 Utopia Parkway<br/>
                        Jamaica, NY&nbsp;11439<br/>
                        <div id="phone166">&nbsp;</div>
                        
                        <a href="http://www.stjohns.edu">http://www.stjohns.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone166").innerHTML = displayStaticPhoneNumber("7189906161") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Conrado&nbsp;Gempesaw,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Queens County<br/>
                        Judicial District XI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        St. John's University - Manhattan Branch<br/>
                        101 Astor Pl<br/>
                        New York, NY&nbsp;10003<br/>
                        <div id="phone167">&nbsp;</div>
                        
                        <a href="http://www.stjohns.edu">http://www.stjohns.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone167").innerHTML = displayStaticPhoneNumber("7189902000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Conrado&nbsp;Gempesaw,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        St. Joseph's Seminary & College-Douglaston<br/>
                        7200 Douglaston Parkway<br/>
                        Douglaston, NY&nbsp;11362<br/>
                        <div id="phone168">&nbsp;</div>
                        
                        <a href="http://https://cathedralseminary.org/">http://https://cathedralseminary.org/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone168").innerHTML = displayStaticPhoneNumber("7186314600") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Father&nbsp;Peter&nbsp;Vaccari,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        Richmond County<br/>
                        Judicial District Xiii
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        St. Joseph's Seminary & College-Huntington<br/>
                        440 West Neck Rd<br/>
                        Huntington, NY&nbsp;11743<br/>
                        <div id="phone169">&nbsp;</div>
                        
                        <a href="http://www.icseminary.edu">http://www.icseminary.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone169").innerHTML = displayStaticPhoneNumber("6314230483") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Father&nbsp;Peter&nbsp;Vaccari,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        Long Island Regents Region<br/>
                        Suffolk County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        St. Joseph's Seminary & College-Somers<br/>
                        54 Ny-138<br/>
                        Somers, NY&nbsp;10589<br/>
                        <div id="phone170">&nbsp;</div>
                        
                        <a href="http://">http://</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone170").innerHTML = displayStaticPhoneNumber("") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Father&nbsp;Peter&nbsp;Vaccari,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        Hudson Valley Regents Region<br/>
                        Dutchess County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Syracuse University<br/>
                        Crouse-Hinds Hall<br/>
                        Syracuse, NY&nbsp;13244-1100<br/>
                        <div id="phone171">&nbsp;</div>
                        
                        <a href="http://syracuse.edu">http://syracuse.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone171").innerHTML = displayStaticPhoneNumber("3154431870") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Kent&nbsp;Syverud,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Central New York Regents Region<br/>
                        Onondaga County<br/>
                        Judicial District V
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        The Sage Colleges<br/>
                        65 First St<br/>
                        Troy, NY&nbsp;12180<br/>
                        <div id="phone178">&nbsp;</div>
                        
                        <a href="http://www.sage.edu">http://www.sage.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone178").innerHTML = displayStaticPhoneNumber("5182442000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Christopher&nbsp;Ames,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Capital District Regents Region<br/>
                        Rensselaer County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        The Sage Colleges -  Albany Campus<br/>
                        140 New Scotland Ave<br/>
                        Albany, NY&nbsp;12208<br/>
                        <div id="phone179">&nbsp;</div>
                        
                        <a href="http://www.sage.edu">http://www.sage.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone179").innerHTML = displayStaticPhoneNumber("5182921730") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Christopher&nbsp;Ames,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Capital District Regents Region<br/>
                        Albany County<br/>
                        Judicial District III
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="T">T</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Teachers College<br/>
                        525 W 120th St<br/>
                        New York, NY&nbsp;10027<br/>
                        <div id="phone172">&nbsp;</div>
                        
                        <a href="http://www.tc.columbia.edu/">http://www.tc.columbia.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone172").innerHTML = displayStaticPhoneNumber("2126783000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Thomas&nbsp;Bailey,&nbsp;President<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Touro College<br/>
                        500 Seventh Ave, 4th And 5th Fls<br/>
                        New York, NY&nbsp;10018<br/>
                        <div id="phone180">&nbsp;</div>
                        
                        <a href="http://www.touro.edu">http://www.touro.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone180").innerHTML = displayStaticPhoneNumber("6465656000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Alan&nbsp;Kadish,&nbsp;President<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Touro College<br/>
                        60 Prospect Ave<br/>
                        Middletown, NY&nbsp;10940-6007<br/>
                        <div id="phone181">&nbsp;</div>
                        
                        <a href="http://https://tourocom.touro.edu/about-us/contact">http://https://tourocom.touro.edu/about-us/contact</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone181").innerHTML = displayStaticPhoneNumber("8456481100") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Alan&nbsp;Kadish,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        Hudson Valley Regents Region<br/>
                        Orange County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Touro College - Bayshore<br/>
                        1700 Union Blvd<br/>
                        Bayshore, NY&nbsp;11706<br/>
                        <div id="phone182">&nbsp;</div>
                        
                        <a href="http://www.touro.edu">http://www.touro.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone182").innerHTML = displayStaticPhoneNumber("6316651600") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Alan&nbsp;Kadish,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Long Island Regents Region<br/>
                        Suffolk County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Touro College - Flatbush<br/>
                        1602 Ave J<br/>
                        Brooklyn, NY&nbsp;11230<br/>
                        <div id="phone183">&nbsp;</div>
                        
                        <a href="http://www.touro.edu">http://www.touro.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone183").innerHTML = displayStaticPhoneNumber("7182527800") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Alan&nbsp;Kadish,&nbsp;President<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Kings County<br/>
                        Judicial District II
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Touro College - Harlem<br/>
                        240 E 123rd St<br/>
                        New York, NY&nbsp;10035<br/>
                        <div id="phone184">&nbsp;</div>
                        
                        <a href="http://www.touro.edu">http://www.touro.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone184").innerHTML = displayStaticPhoneNumber("2127221575") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Alan&nbsp;Kadish,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Touro College - Kew Gardens<br/>
                        75-31 150th St<br/>
                        Kew Garden Hills, NY&nbsp;11367<br/>
                        <div id="phone185">&nbsp;</div>
                        
                        <a href="http://www.touro.edu">http://www.touro.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone185").innerHTML = displayStaticPhoneNumber("7188204800") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Alan&nbsp;Kadish&nbsp;<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Queens County<br/>
                        Judicial District XI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Touro College - Valhalla<br/>
                        19 Skyline Dr<br/>
                        Valhalla, NY&nbsp;10595<br/>
                        <div id="phone186">&nbsp;</div>
                        
                        <a href="http://dental.touro.edu/">http://dental.touro.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone186").innerHTML = displayStaticPhoneNumber("9145943865") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Alan&nbsp;Kadish,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Touro College-Central Islip<br/>
                        225 Eastview Dr<br/>
                        Central Islip, NY&nbsp;11722<br/>
                        <div id="phone187">&nbsp;</div>
                        
                        <a href="http://www.touro.edu">http://www.touro.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone187").innerHTML = displayStaticPhoneNumber("6317617000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Alan&nbsp;Kadish,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Long Island Regents Region<br/>
                        Suffolk County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Trocaire College<br/>
                        360 Choate Ave<br/>
                        Buffalo, NY&nbsp;14220<br/>
                        <div id="phone188">&nbsp;</div>
                        
                        <a href="http://www.trocaire.edu">http://www.trocaire.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone188").innerHTML = displayStaticPhoneNumber("7168261200") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Bassam&nbsp;Deeb,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Western New York Regents Region<br/>
                        Erie County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="U">U</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Unification Theological Seminary<br/>
                        4 West 43rd St<br/>
                        New York, NY&nbsp;10036<br/>
                        <div id="phone189">&nbsp;</div>
                        
                        <a href="http://uts.edu/">http://uts.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone189").innerHTML = displayStaticPhoneNumber("2125636647") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Thomas&nbsp;Ward,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        Hudson Valley Regents Region<br/>
                        Dutchess County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Union College<br/>
                        807 Union St<br/>
                        Schenectady, NY&nbsp;12308<br/>
                        <div id="phone190">&nbsp;</div>
                        
                        <a href="http://www.union.edu">http://www.union.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone190").innerHTML = displayStaticPhoneNumber("5183886000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;David&nbsp;Harris,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Capital District Regents Region<br/>
                        Schenectady County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Union Graduate College<br/>
                        80 Nott Terrace<br/>
                        Schenectady, NY&nbsp;12308<br/>
                        <div id="phone191">&nbsp;</div>
                        
                        <a href="http://WWW.UNIONGRADUATECOLLEGE.EDU">http://www.uniongraduatecollege.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone191").innerHTML = displayStaticPhoneNumber("5186319844") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Bela&nbsp;Musits,&nbsp;President<br/>
                        Graduate Programs Only<br/>
                        Capital District Regents Region<br/>
                        Schenectady County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Union Theological Seminary<br/>
                        3041 Broadway<br/>
                        New York, NY&nbsp;10027-5792<br/>
                        <div id="phone192">&nbsp;</div>
                        
                        <a href="http://www.utsnyc.edu">http://www.utsnyc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone192").innerHTML = displayStaticPhoneNumber("2126627100") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Serene&nbsp;Jones,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        University of Rochester<br/>
                        Wilson Blvd-Wallis Hall<br/>
                        Rochester, NY&nbsp;14627-140<br/>
                        <div id="phone193">&nbsp;</div>
                        
                        <a href="http://www.rochester.edu">http://www.rochester.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone193").innerHTML = displayStaticPhoneNumber("5852752121") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Sarah&nbsp;Mangelsdorf,&nbsp;Chief Exective Officer<br/>
                        4-Year Independent<br/>
                        Finger Lakes Regents Region<br/>
                        Monroe County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Utica College<br/>
                        1600 Burrstone Rd<br/>
                        Utica, NY&nbsp;13502<br/>
                        <div id="phone194">&nbsp;</div>
                        
                        <a href="http://www.utica.edu">http://www.utica.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone194").innerHTML = displayStaticPhoneNumber("3157923111") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Laura&nbsp;Casamento,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Mohawk Valley Regents Region<br/>
                        Oneida County<br/>
                        Judicial District V
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="V">V</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Vassar College<br/>
                        124 Raymond Ave<br/>
                        Poughkeepsie, NY&nbsp;12601<br/>
                        <div id="phone195">&nbsp;</div>
                        
                        <a href="http://www.vassar.edu">http://www.vassar.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone195").innerHTML = displayStaticPhoneNumber("9144377000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Elizabeth&nbsp;Bradley,&nbsp;President<br/>
                        4-Year Independent<br/>
                        Hudson Valley Regents Region<br/>
                        Dutchess County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Vaughn College of Aeronautics And Technology<br/>
                        86-01 23rd. Avenue<br/>
                        Flushing, NY&nbsp;11369<br/>
                        <div id="phone196">&nbsp;</div>
                        
                        <a href="http://www.vaughn.edu">http://www.vaughn.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone196").innerHTML = displayStaticPhoneNumber("8666828446") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Sharon&nbsp;Devivo,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Queens County<br/>
                        Judicial District XI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Villa Maria College of Buffalo<br/>
                        240 Pine Ridge Rd<br/>
                        Buffalo, NY&nbsp;14225<br/>
                        <div id="phone197">&nbsp;</div>
                        
                        <a href="http://www.villa.edu/">http://www.villa.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone197").innerHTML = displayStaticPhoneNumber("7168960700") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Matthew&nbsp;Giordano,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Western New York Regents Region<br/>
                        Erie County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="W">W</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Wagner College<br/>
                        One Campus Rd<br/>
                        Staten Island, NY&nbsp;10301<br/>
                        <div id="phone198">&nbsp;</div>
                        
                        <a href="http://www.wagner.edu/">http://www.wagner.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone198").innerHTML = displayStaticPhoneNumber("7183903100") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Joel&nbsp;Martin,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        Richmond County<br/>
                        Judicial District Xiii
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Webb Insttitute<br/>
                        298 Crescent Beach Rd<br/>
                        Glen Cove, NY&nbsp;11542<br/>
                        <div id="phone199">&nbsp;</div>
                        
                        <a href="http://www.webb.edu">http://www.webb.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone199").innerHTML = displayStaticPhoneNumber("5166712213") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;R. Keith&nbsp;Michel,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Long Island Regents Region<br/>
                        Nassau County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Wells College<br/>
                        170 Main St<br/>
                        Aurora, NY&nbsp;13026-500<br/>
                        <div id="phone200">&nbsp;</div>
                        
                        <a href="http://www.wells.edu">http://www.wells.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone200").innerHTML = displayStaticPhoneNumber("3153643264") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Jonathan&nbsp;Gibralter,&nbsp;Chief Executive Officer<br/>
                        4-Year Independent<br/>
                        Central New York Regents Region<br/>
                        Cayuga County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
    </tbody>
</table>

<a href="#TOP" style="margin-left:85%;">Back to Top</a>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
    </tbody>
</table>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="Y">Y</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Yeshiva University<br/>
                        500 W 185th St<br/>
                        New York, NY&nbsp;10033<br/>
                        <div id="phone201">&nbsp;</div>
                        
                        <a href="http://www.yu.edu">http://www.yu.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone201").innerHTML = displayStaticPhoneNumber("2129605400") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Ari&nbsp;Berman,&nbsp;President<br/>
                        4-Year Independent<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
    </tbody>
'''





soup = BeautifulSoup(html, 'html5lib')

org_url_list = []


# Seperate by tr elements
l = soup.find_all('tr')

# Get vis text
for i in l:
    
    info = i.get_text()

    # Skip elements that are used to organize sections alphabetically
    if len(info) == 1: continue


    
    # Split by newline
    info_l = info.strip().split('\n')

    # Org name is first entry
    org = info_l[0]

    # Find URL
    for each_line in info_l:
        
        if 'http' in each_line:
            url = each_line.strip()
            org_url_list.append([org, url])
            break
        
    else:
        print('no match:', info_l)





## Make list of org names and coords
# Open coords file
coords_file = pd.ExcelFile("uni_coords.xlsx")

# Select sheet number
coords_sheet = coords_file.parse()

# Select column
name_col = coords_sheet['Legal Name']


# Iterate through each org's URL
for html_org in org_url_list:

    # Iterate through each org's coords
    for i in coords_sheet.index:

        # Find matching org names
        if coords_sheet['Legal Name'][i].lower().strip() == html_org[0].lower().strip():

            coords = (coords_sheet['GIS Latitude (Y)'][i], coords_sheet['GIS Longitute (X)'][i])

            print(str([html_org[0], html_org[1], coords]) + ',')
            break

    else: 
        print(str((html_org[0], '', (0.0, 0.0))) + ',')



print(len(org_url_list))


















