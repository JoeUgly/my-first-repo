
# Desc: Combine URLs and coordinates for every Proprietary university

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
                        Art Institute of New York City<br/>
                        218-232 W 40 St<br/>
                        New York, NY&nbsp;10018<br/>
                        <div id="phone0">&nbsp;</div>
                        
                        <a href="http://www.artinstitutes.edu">http://www.artinstitutes.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone0").innerHTML = displayStaticPhoneNumber("2122265500") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Jennifer&nbsp;Ramey,&nbsp;President<br/>
                        2 Year Proprietary<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Asa College, Inc.<br/>
                        151 Lawrence St<br/>
                        Brooklyn, NY&nbsp;11201<br/>
                        <div id="phone1">&nbsp;</div>
                        
                        <a href="http://WWW.ASA.EDU">http://www.asa.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone1").innerHTML = displayStaticPhoneNumber("7185229073") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Jose&nbsp;Valencia,&nbsp;President<br/>
                        2 Year Proprietary<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="B">B</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Berkeley College - Main Campus<br/>
                        3 E 43rd St<br/>
                        New York, NY&nbsp;10017<br/>
                        <div id="phone2">&nbsp;</div>
                        
                        <a href="http://www.berkeleycollege.edu">http://www.berkeleycollege.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone2").innerHTML = displayStaticPhoneNumber("2129864343") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Michael&nbsp;Smith,&nbsp;President<br/>
                        4 Year Proprietary<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Berkeley College - Westchester<br/>
                        99 Church St<br/>
                        White Plains, NY&nbsp;10604<br/>
                        <div id="phone3">&nbsp;</div>
                        
                        <a href="http://WWW.BERKELEYCOLLEGE.EDU">http://www.berkeleycollege.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone3").innerHTML = displayStaticPhoneNumber("9146941122") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Michael&nbsp;Smith,&nbsp;Chief Executive Officer<br/>
                        4 Year Proprietary<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Bryant & Stratton Business College - North Syracuse<br/>
                        8687 Carling Rd<br/>
                        Liverpool, NY&nbsp;13090<br/>
                        <div id="phone4">&nbsp;</div>
                        
                        <a href="http://www.bryantstratton.edu">http://www.bryantstratton.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone4").innerHTML = displayStaticPhoneNumber("3156526500") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Susan&nbsp;Cumoletti,&nbsp;Chief Executive Officer<br/>
                        2 Year Proprietary<br/>
                        Central New York Regents Region<br/>
                        Onondaga County<br/>
                        Judicial District V
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Bryant & Stratton College - Albany<br/>
                        1259 Central Ave<br/>
                        Albany, NY&nbsp;12205-5230<br/>
                        <div id="phone5">&nbsp;</div>
                        
                        <a href="http://www.bryantstratton.edu">http://www.bryantstratton.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone5").innerHTML = displayStaticPhoneNumber("5184371802") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Ludwika&nbsp;Nighan,&nbsp;Chief Executive Officer<br/>
                        4 Year Proprietary<br/>
                        Capital District Regents Region<br/>
                        Albany County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Bryant & Stratton College - Buffalo<br/>
                        465 Main St, Ste 400<br/>
                        Buffalo, NY&nbsp;14203<br/>
                        <div id="phone6">&nbsp;</div>
                        
                        <a href="http://www.bryantstratton.edu">http://www.bryantstratton.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone6").innerHTML = displayStaticPhoneNumber("7168849120") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Jeff&nbsp;Tredo,&nbsp;Chief Executive Officer<br/>
                        4 Year Proprietary<br/>
                        Western New York Regents Region<br/>
                        Erie County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Bryant & Stratton College - Greece<br/>
                        Greece Campus<br/>
                        Rochester, NY&nbsp;14612<br/>
                        <div id="phone7">&nbsp;</div>
                        
                        <a href="http://www.bryantstratton.edu">http://www.bryantstratton.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone7").innerHTML = displayStaticPhoneNumber("5857200660") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Michael&nbsp;Mariani,&nbsp;Chief  Executive Officer<br/>
                        2 Year Proprietary<br/>
                        Finger Lakes Regents Region<br/>
                        Monroe County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Bryant & Stratton College - Henrietta<br/>
                        1225 Jefferson Rd<br/>
                        Rochester, NY&nbsp;14623<br/>
                        <div id="phone8">&nbsp;</div>
                        
                        <a href="http://www.bryantstratton.edu">http://www.bryantstratton.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone8").innerHTML = displayStaticPhoneNumber("5852925627") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Michael&nbsp;Mariani,&nbsp;Chief Executive Officer<br/>
                        2 Year Proprietary<br/>
                        Finger Lakes Regents Region<br/>
                        Monroe County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Bryant & Stratton College - Southtowns Campus<br/>
                        200 Redtail<br/>
                        Orchard Park, NY&nbsp;14127<br/>
                        <div id="phone9">&nbsp;</div>
                        
                        <a href="http://www.bryantstratton.edu">http://www.bryantstratton.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone9").innerHTML = displayStaticPhoneNumber("7166779500") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Jeff&nbsp;Tredo,&nbsp;Chief Executive Officer<br/>
                        4 Year Proprietary<br/>
                        Western New York Regents Region<br/>
                        Erie County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Bryant & Stratton College- Amherst<br/>
                        Amherst Campus<br/>
                        Getzville, NY&nbsp;14068<br/>
                        <div id="phone10">&nbsp;</div>
                        
                        <a href="http://www.bryantstratton.edu">http://www.bryantstratton.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone10").innerHTML = displayStaticPhoneNumber("7166256300") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Jeff&nbsp;Tredo,&nbsp;Chief Executive Officer<br/>
                        4 Year Proprietary<br/>
                        Western New York Regents Region<br/>
                        Erie County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Bryant Stratton College - Syracuse<br/>
                        953 James St<br/>
                        Syracuse, NY&nbsp;13203-2502<br/>
                        <div id="phone11">&nbsp;</div>
                        
                        <a href="http://www.bryantstratton.edu">http://www.bryantstratton.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone11").innerHTML = displayStaticPhoneNumber("3154726603") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Michael&nbsp;Sattler,&nbsp;Chief Executive Officer<br/>
                        2 Year Proprietary<br/>
                        Central New York Regents Region<br/>
                        Onondaga County<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="C">C</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Christie's Education, Inc<br/>
                        1230 Ave of the Americas, 20th Fl<br/>
                        New York, NY&nbsp;10020<br/>
                        <div id="phone12">&nbsp;</div>
                        
                        <a href="http://www.christies.edu">http://www.christies.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone12").innerHTML = displayStaticPhoneNumber("2123551501") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Veronique&nbsp;Chagnon-Burke,&nbsp;Director<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        The College of Westchester<br/>
                        325 Central Ave<br/>
                        White Plains, NY&nbsp;10606<br/>
                        <div id="phone39">&nbsp;</div>
                        
                        <a href="http://www.cw.edu">http://www.cw.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone39").innerHTML = displayStaticPhoneNumber("9149484442") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mrs.&nbsp;Mary Beth&nbsp;Del Balzo,&nbsp;Chief Executive Officer<br/>
                        4 Year Proprietary<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="D">D</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Devry College of New York<br/>
                        180 Madison Ave, Ste 1200<br/>
                        New York, NY&nbsp;10016<br/>
                        <div id="phone13">&nbsp;</div>
                        
                        <a href="http://https://www.devry.edu/">http://https://www.devry.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone13").innerHTML = displayStaticPhoneNumber("2123124300") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Anthony&nbsp;Stanziani,&nbsp;Chief Executive Officer<br/>
                        4 Year Proprietary<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="E">E</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Elmira Business Inst<br/>
                        303 N Main St<br/>
                        Elmira, NY&nbsp;14901<br/>
                        <div id="phone14">&nbsp;</div>
                        
                        <a href="http://www.ebi.edu">http://www.ebi.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone14").innerHTML = displayStaticPhoneNumber("6077298915") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Brad&nbsp;Phillips,&nbsp;Chief Executive Officer<br/>
                        2 Year Proprietary<br/>
                        Southern Tier Regents Region<br/>
                        Chemung County<br/>
                        Judicial District VI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Elmira Business Institute - Vestal Executive Park<br/>
                        4100 Vestal Rd<br/>
                        Vestal, NY&nbsp;13850<br/>
                        <div id="phone15">&nbsp;</div>
                        
                        <a href="http://www.ebi.edu">http://www.ebi.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone15").innerHTML = displayStaticPhoneNumber("6077298915") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Brad&nbsp;Phillips,&nbsp;Chief Executive Officer<br/>
                        2 Year Proprietary<br/>
                        Southern Tier Regents Region<br/>
                        Broome County<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="F">F</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Five Towns College<br/>
                        305 N Service Rd<br/>
                        Dix Hills, NY&nbsp;11746<br/>
                        <div id="phone16">&nbsp;</div>
                        
                        <a href="http://www.ftc.edu">http://www.ftc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone16").innerHTML = displayStaticPhoneNumber("6314247000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;David&nbsp;Cohen,&nbsp;Acting President<br/>
                        2 Year Proprietary<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="G">G</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Globe Inst of Tech Inc<br/>
                        500 7th Ave<br/>
                        New York, NY&nbsp;10018<br/>
                        <div id="phone17">&nbsp;</div>
                        
                        <a href="http://www.globe.edu/">http://www.globe.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone17").innerHTML = displayStaticPhoneNumber("2123494330") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Martin&nbsp;Oliner,&nbsp;Chief Executive Officer<br/>
                        4 Year Proprietary<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="I">I</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Island Drafting & Tech Inst<br/>
                        128 Broadway<br/>
                        Amityville, NY&nbsp;11701<br/>
                        <div id="phone18">&nbsp;</div>
                        
                        <a href="http://www.idti.edu">http://www.idti.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone18").innerHTML = displayStaticPhoneNumber("6316918733") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;James&nbsp;Di Liberto,&nbsp;Chief Executive Officer<br/>
                        2 Year Proprietary<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="J">J</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Jamestown Business College<br/>
                        7 Fairmount Ave<br/>
                        Jamestown, NY&nbsp;14701<br/>
                        <div id="phone19">&nbsp;</div>
                        
                        <a href="http://www.jbcny.edu">http://www.jbcny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone19").innerHTML = displayStaticPhoneNumber("7166645100") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;David&nbsp;Conklin,&nbsp;Chief Executive Officer<br/>
                        2 Year Proprietary<br/>
                        Western New York Regents Region<br/>
                        Chautauqua County<br/>
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
        
    </tbody>
</table>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="L">L</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Laboratory Inst of Merchandising<br/>
                        12 E 53rd St<br/>
                        New York, NY&nbsp;10022<br/>
                        <div id="phone20">&nbsp;</div>
                        
                        <a href="http://www.limcollege.edu/">http://www.limcollege.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone20").innerHTML = displayStaticPhoneNumber("8006771323") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Elizabeth&nbsp;Marcuse,&nbsp;Chief Executive Officer<br/>
                        4 Year Proprietary<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Long Island Business Inst<br/>
                        6500 Jericho Tpke, Ste 202<br/>
                        Commack, NY&nbsp;11725<br/>
                        <div id="phone21">&nbsp;</div>
                        
                        <a href="http://www.libi.edu">http://www.libi.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone21").innerHTML = displayStaticPhoneNumber("6314997100") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Monica&nbsp;Foote,&nbsp;Chief Executive Officer<br/>
                        2 Year Proprietary<br/>
                        Long Island Regents Region<br/>
                        Suffolk County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Long Island Business Institute - Flushing<br/>
                        136-18 39th Ave, 5th Fl<br/>
                        Flushing, NY&nbsp;11354<br/>
                        <div id="phone22">&nbsp;</div>
                        
                        <a href="http://WWW.LIBI.EDU">http://www.libi.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone22").innerHTML = displayStaticPhoneNumber("7189395100") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Monica&nbsp;Foote,&nbsp;Chief Executive Officer<br/>
                        2 Year Proprietary<br/>
                        New York City Regents Region<br/>
                        Queens County<br/>
                        Judicial District XI
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
                        Mandl School Inc<br/>
                        254 W 54th St<br/>
                        New York, NY&nbsp;10019<br/>
                        <div id="phone23">&nbsp;</div>
                        
                        <a href="http://www.mandl.edu">http://www.mandl.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone23").innerHTML = displayStaticPhoneNumber("2122473434") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Melvyn&nbsp;Weiner,&nbsp;Chief Executive Officer<br/>
                        2 Year Proprietary<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Mildred Elley School<br/>
                        855 Central Ave<br/>
                        Albany, NY&nbsp;12206<br/>
                        <div id="phone24">&nbsp;</div>
                        
                        <a href="http://www.mildred-elley.edu">http://www.mildred-elley.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone24").innerHTML = displayStaticPhoneNumber("5187860855") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;John&nbsp;McGrath,&nbsp;Chief Executive Officer<br/>
                        2 Year Proprietary<br/>
                        Capital District Regents Region<br/>
                        Albany County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Mildred Elley-Nyc<br/>
                        25 Broadway, Fl 16<br/>
                        New York, NY&nbsp;10004<br/>
                        <div id="phone25">&nbsp;</div>
                        
                        <a href="http://mildred-elley.edu">http://mildred-elley.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone25").innerHTML = displayStaticPhoneNumber("2123809004") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;John&nbsp;McGrath,&nbsp;Chief Executive Officer<br/>
                        2 Year Proprietary<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Monroe College<br/>
                        2501 Jerome Ave<br/>
                        Bronx, NY&nbsp;10468<br/>
                        <div id="phone26">&nbsp;</div>
                        
                        <a href="http://www.monroecollege.edu">http://www.monroecollege.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone26").innerHTML = displayStaticPhoneNumber("7189336700") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Marc&nbsp;Jerome,&nbsp;President<br/>
                        4 Year Proprietary<br/>
                        New York City Regents Region<br/>
                        Bronx County<br/>
                        Judicial District XII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Monroe College-New Rochelle Br Camps<br/>
                        434 Main St<br/>
                        New Rochelle, NY&nbsp;10801<br/>
                        <div id="phone27">&nbsp;</div>
                        
                        <a href="http://www.monroecollege.edu">http://www.monroecollege.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone27").innerHTML = displayStaticPhoneNumber("9146325400") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Marc&nbsp;Jerome,&nbsp;President<br/>
                        4 Year Proprietary<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="N">N</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York Automotive & Diesel Institute<br/>
                        178-18 Liberty Ave<br/>
                        Jamaica, NY&nbsp;11433<br/>
                        <div id="phone28">&nbsp;</div>
                        
                        <a href="http://">http://</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone28").innerHTML = displayStaticPhoneNumber("") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Patrick&nbsp;Hart,&nbsp;President<br/>
                        2 Year Proprietary<br/>
                        New York City Regents Region<br/>
                        Queens County<br/>
                        Judicial District XI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York Conservatory For Dramatic Arts<br/>
                        39 W 19th St<br/>
                        New York, NY&nbsp;10011<br/>
                        <div id="phone29">&nbsp;</div>
                        
                        <a href="http://www.nycda.edu">http://www.nycda.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone29").innerHTML = displayStaticPhoneNumber("2126450030") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Mike&nbsp;Dabidat,&nbsp;Chief Executive Officer<br/>
                        2 Year Proprietary<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York Film Academy<br/>
                        17 Battery Pl<br/>
                        New York, NY&nbsp;10004<br/>
                        <div id="phone30">&nbsp;</div>
                        
                        <a href="http://https://www.nyfa.edu">http://https://www.nyfa.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone30").innerHTML = displayStaticPhoneNumber("2126744300") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Michael&nbsp;Young,&nbsp;President<br/>
                        4 Year Proprietary<br/>
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
                        Pacific College of Oriental Medicine<br/>
                        915 Broadway, 2nd Fl<br/>
                        New York, NY&nbsp;10010-7108<br/>
                        <div id="phone31">&nbsp;</div>
                        
                        <a href="http://WWW.PACIFICCOLLEGE.EDU">http://www.pacificcollege.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone31").innerHTML = displayStaticPhoneNumber("2129823456") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Malcolm&nbsp;Youngren,&nbsp;Chief Executive Officer<br/>
                        4 Year Proprietary<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Plaza College<br/>
                        118-33 Queens Blvd<br/>
                        Forest Hills, NY&nbsp;11375<br/>
                        <div id="phone32">&nbsp;</div>
                        
                        <a href="http://www.plazacollege.edu">http://www.plazacollege.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone32").innerHTML = displayStaticPhoneNumber("7187791430") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Charles&nbsp;Callahan,&nbsp;Chief Executive Officer<br/>
                        4 Year Proprietary<br/>
                        New York City Regents Region<br/>
                        Queens County<br/>
                        Judicial District XI
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
        
    </tbody>
</table>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="S">S</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        SBI Campus - An Affiliate of Sanford-Brown<br/>
                        320 South Service Rd<br/>
                        Melville, NY&nbsp;11747<br/>
                        <div id="phone33">&nbsp;</div>
                        
                        <a href="http://WWW.SBMELVILLE.EDU">http://www.sbmelville.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone33").innerHTML = displayStaticPhoneNumber("6313703300") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;James&nbsp;Swift,&nbsp;Chief Executive Officer<br/>
                        2 Year Proprietary<br/>
                        Long Island Regents Region<br/>
                        Suffolk County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        School of Visual Arts<br/>
                        209 E 23rd St<br/>
                        New York, NY&nbsp;10010<br/>
                        <div id="phone34">&nbsp;</div>
                        
                        <a href="http://www.sva.edu">http://www.sva.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone34").innerHTML = displayStaticPhoneNumber("2125922000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;David&nbsp;Rhodes,&nbsp;Chief Executive Officer<br/>
                        4 Year Proprietary<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Sotheby's Institute of Art - NY<br/>
                        570 Lexington Ave<br/>
                        New York, NY&nbsp;10022<br/>
                        <div id="phone35">&nbsp;</div>
                        
                        <a href="http://www.sothebysinstitute.com/newyork/index.html">http://www.sothebysinstitute.com/newyork/index.html</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone35").innerHTML = displayStaticPhoneNumber("2125173929") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Christine&nbsp;Kuan,&nbsp;Chief Executive Officer<br/>
                        Graduate Programs Only<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        St. Paul's School of Nursing - Queens<br/>
                        97-77 Queens Blvd<br/>
                        Rego Park, NY&nbsp;11374<br/>
                        <div id="phone36">&nbsp;</div>
                        
                        <a href="http://www.stpaulsschoolofnursing.edu/">http://www.stpaulsschoolofnursing.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone36").innerHTML = displayStaticPhoneNumber("7183570500") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Paul&nbsp;Ferrise,&nbsp;Chief Executive Director<br/>
                        2 Year Proprietary<br/>
                        New York City Regents Region<br/>
                        Queens County<br/>
                        Judicial District XI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        St. Paul's School of Nursing - Staten Island<br/>
                        Corporate Commons Two<br/>
                        Staten Island, NY&nbsp;10311<br/>
                        <div id="phone37">&nbsp;</div>
                        
                        <a href="http://WWW.STPAULSSCHOOLOFNURSING.COM">http://www.stpaulsschoolofnursing.com</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone37").innerHTML = displayStaticPhoneNumber("7188186470") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;David&nbsp;Smith,&nbsp;School Director<br/>
                        2 Year Proprietary<br/>
                        New York City Regents Region<br/>
                        Richmond County<br/>
                        Judicial District Xiii
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Swedish Institute Inc<br/>
                        226 W 26th St<br/>
                        New York, NY&nbsp;10001<br/>
                        <div id="phone38">&nbsp;</div>
                        
                        <a href="http://www.swedishinstitute.edu">http://www.swedishinstitute.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone38").innerHTML = displayStaticPhoneNumber("2129245900") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mrs.&nbsp;Erin&nbsp;Shea,&nbsp;Chief Executive Officer<br/>
                        4 Year Proprietary<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="T">T</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Tri-State College of Acupuncture<br/>
                        80 8th Ave, 4th Fl, Rm 400<br/>
                        New York, NY&nbsp;10011<br/>
                        <div id="phone40">&nbsp;</div>
                        
                        <a href="http://www.tsca.edu">http://www.tsca.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone40").innerHTML = displayStaticPhoneNumber("2122422255") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Dennis&nbsp;Moseman,&nbsp;Chief Executive Officer<br/>
                        4 Year Proprietary<br/>
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
    org = info_l[0].strip()

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
        if coords_sheet['Legal Name'][i].lower().strip() == html_org[0].lower():

            coords = (coords_sheet['GIS Latitude (Y)'][i], coords_sheet['GIS Longitute (X)'][i])

            print(str([html_org[0], html_org[1], coords]) + ',')
            break

    else: 
        print('no match:', html_org)






















