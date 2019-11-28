
# Desc: Combine URLs and coordinates for every SUNY university

# Must use similar code to get each school type. eg: SUNY, CUNY, Independent, Proprietary

# URLs' HTML source: http://eservices.nysed.gov/collegedirectory/index.htm
# Must copy and paste relevant elements starting at <tbody>

# Coords source: http://eservices.nysed.gov/sedreports/list?id=1
# All Institutions: Active Institutions with GIS coordinates and OITS Accuracy Code - Select by County






from bs4 import BeautifulSoup
import pandas as pd



html = '''
<tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="A">A</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Adirondack Community College<br/>
                        640 Bay Road<br/>
                        Glens Falls, NY&nbsp;12804<br/>
                        <div id="phone0">&nbsp;</div>
                        
                        <a href="http://www.sunyacc.edu">http://www.sunyacc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone0").innerHTML = displayStaticPhoneNumber("5187432200") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Kristine&nbsp;Duffy,&nbsp;Chief Executive Officer<br/>
                        SUNY Community Colleges<br/>
                        Capital District Regents Region<br/>
                        Warren County<br/>
                        Judicial District IV
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
                        Broome Community College<br/>
                        Upper Front Street<br/>
                        Binghamton, NY&nbsp;13902<br/>
                        <div id="phone1">&nbsp;</div>
                        
                        <a href="http://www.sunybroome.edu">http://www.sunybroome.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone1").innerHTML = displayStaticPhoneNumber("6077785000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Kevin&nbsp;Drumm,&nbsp;Chief Executive Officer<br/>
                        SUNY Community Colleges<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="C">C</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Cayuga Community College - Fulton Center<br/>
                        11 River Glen Plaza<br/>
                        Fulton, NY&nbsp;13069<br/>
                        <div id="phone2">&nbsp;</div>
                        
                        <a href="http://WWW.CAYUGA-CC.EDU">http://www.cayuga-cc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone2").innerHTML = displayStaticPhoneNumber("3155924143") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Brian&nbsp;Durant,&nbsp;Chief Executive Officer<br/>
                        SUNY Community Colleges<br/>
                        Central New York Regents Region<br/>
                        Oswego County<br/>
                        Judicial District V
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Cayuga County Community College<br/>
                        197 Franklin St<br/>
                        Auburn, NY&nbsp;13021-1743<br/>
                        <div id="phone3">&nbsp;</div>
                        
                        <a href="http://www.cayuga-cc.edu">http://www.cayuga-cc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone3").innerHTML = displayStaticPhoneNumber("3152551743") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Brian&nbsp;Durant,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        Central New York Regents Region<br/>
                        Cayuga County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Clinton Community College<br/>
                        136 Clinton Point Drive<br/>
                        Plattsburgh, NY&nbsp;12901<br/>
                        <div id="phone4">&nbsp;</div>
                        
                        <a href="http://www.clinton.edu">http://www.clinton.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone4").innerHTML = displayStaticPhoneNumber("5185624200") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Ray&nbsp;Dipasquale,&nbsp;Chief Executive Officer<br/>
                        SUNY Community Colleges<br/>
                        Northern Regents Region<br/>
                        Clinton County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Columbia-Greene Community College<br/>
                        4400 Route 23<br/>
                        Hudson, NY&nbsp;12534<br/>
                        <div id="phone5">&nbsp;</div>
                        
                        <a href="http://www.sunycgcc.edu">http://www.sunycgcc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone5").innerHTML = displayStaticPhoneNumber("5188284181") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Carlee&nbsp;Drummer,&nbsp;Chief Executive Officer<br/>
                        SUNY Community Colleges<br/>
                        Capital District Regents Region<br/>
                        Columbia County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Cornell Un Inst Res Dev<br/>
                        Cornell Un Inst Res Dev<br/>
                        Ithaca, NY&nbsp;14850<br/>
                        <div id="phone6">&nbsp;</div>
                        
                        <a href="http://">http://</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone6").innerHTML = displayStaticPhoneNumber("") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;David&nbsp;Skorton,&nbsp;President<br/>
                        SUNY Statutory Colleges<br/>
                        Southern Tier Regents Region<br/>
                        Tompkins County<br/>
                        Judicial District VI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Corning Community College<br/>
                        1 Academic Dr<br/>
                        Corning, NY&nbsp;14830<br/>
                        <div id="phone7">&nbsp;</div>
                        
                        <a href="http://www.corning-cc.edu">http://www.corning-cc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone7").innerHTML = displayStaticPhoneNumber("6079629222") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;William&nbsp;Mullaney,&nbsp;Chief Executive Officer<br/>
                        SUNY Community Colleges<br/>
                        Southern Tier Regents Region<br/>
                        Steuben County<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="D">D</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Dutchess Community College<br/>
                        53 Pendell Rd<br/>
                        Poughkeepsie, NY&nbsp;12601<br/>
                        <div id="phone8">&nbsp;</div>
                        
                        <a href="http://www.sunydutchess.edu">http://www.sunydutchess.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone8").innerHTML = displayStaticPhoneNumber("8454318000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Pamela&nbsp;Edington,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="E">E</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Erie Community College-City Campus<br/>
                        121 Ellicott St<br/>
                        Buffalo, NY&nbsp;14203-2698<br/>
                        <div id="phone9">&nbsp;</div>
                        
                        <a href="http://www.ecc.edu">http://www.ecc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone9").innerHTML = displayStaticPhoneNumber("7168511000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Dan&nbsp;Hocoy,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        Western New York Regents Region<br/>
                        Erie County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Erie Community College-North Campus<br/>
                        6205 Main St<br/>
                        Williamsville, NY&nbsp;14221<br/>
                        <div id="phone10">&nbsp;</div>
                        
                        <a href="http://www.ecc.edu">http://www.ecc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone10").innerHTML = displayStaticPhoneNumber("7168511000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Dan&nbsp;Hocoy,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        Western New York Regents Region<br/>
                        Erie County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Erie Community College-South Campus<br/>
                        4041 Southwestern Blvd<br/>
                        Orchard Park, NY&nbsp;14127<br/>
                        <div id="phone11">&nbsp;</div>
                        
                        <a href="http://www.ecc.edu">http://www.ecc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone11").innerHTML = displayStaticPhoneNumber("7168511000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Dan&nbsp;Hocoy,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="F">F</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Fashion Institute of Technology<br/>
                        7th Ave at 27th St<br/>
                        New York, NY&nbsp;10001<br/>
                        <div id="phone12">&nbsp;</div>
                        
                        <a href="http://www.fitnyc.edu">http://www.fitnyc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone12").innerHTML = displayStaticPhoneNumber("2122177999") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Joyce&nbsp;Brown,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Finger Lakes Community College<br/>
                        3325 Marvin Sands Dr<br/>
                        Canandaigua, NY&nbsp;14424-8395<br/>
                        <div id="phone13">&nbsp;</div>
                        
                        <a href="http://www.fingerlakes.edu">http://www.fingerlakes.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone13").innerHTML = displayStaticPhoneNumber("5853943500") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Robert&nbsp;Nye,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        Finger Lakes Regents Region<br/>
                        Ontario County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Fulton-Montgomery Community College<br/>
                        2805 State Highway 67<br/>
                        Johnstown, NY&nbsp;12095-3790<br/>
                        <div id="phone14">&nbsp;</div>
                        
                        <a href="http://www.fmcc.suny.edu">http://www.fmcc.suny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone14").innerHTML = displayStaticPhoneNumber("5187363622") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Gregory&nbsp;Truckenmiller,&nbsp;Chief Executive Officer<br/>
                        SUNY Community Colleges<br/>
                        Mohawk Valley Regents Region<br/>
                        Montgomery County<br/>
                        Judicial District IV
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
                        Genesee Community College<br/>
                        One College Rd<br/>
                        Batavia, NY&nbsp;14020<br/>
                        <div id="phone15">&nbsp;</div>
                        
                        <a href="http://www.genesee.edu">http://www.genesee.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone15").innerHTML = displayStaticPhoneNumber("5853430055") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;James&nbsp;Sunser,&nbsp;Chief Executive Officer<br/>
                        SUNY Community Colleges<br/>
                        Finger Lakes Regents Region<br/>
                        Genesee County<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="H">H</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Herkimer County Community College<br/>
                        Reservoir Rd<br/>
                        Herkimer, NY&nbsp;13350<br/>
                        <div id="phone16">&nbsp;</div>
                        
                        <a href="http://www.herkimer.edu/">http://www.herkimer.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone16").innerHTML = displayStaticPhoneNumber("3158660300") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Cathleen&nbsp;McColgin,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        Mohawk Valley Regents Region<br/>
                        Herkimer County<br/>
                        Judicial District V
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Hudson Valley Community College<br/>
                        80 Vandenburgh Ave<br/>
                        Troy, NY&nbsp;12180<br/>
                        <div id="phone17">&nbsp;</div>
                        
                        <a href="http://www.hvcc.edu">http://www.hvcc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone17").innerHTML = displayStaticPhoneNumber("5186294822") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Roger&nbsp;Ramsammy,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        Capital District Regents Region<br/>
                        Rensselaer County<br/>
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
        
    </tbody>
</table>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="J">J</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Jamestown Community College<br/>
                        525 Falconer St<br/>
                        Jamestown, NY&nbsp;14701<br/>
                        <div id="phone18">&nbsp;</div>
                        
                        <a href="http://www.sunyjcc.edu">http://www.sunyjcc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone18").innerHTML = displayStaticPhoneNumber("7163381000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Daniel&nbsp;Demarte,&nbsp;Chief Executive Officer<br/>
                        SUNY Community Colleges<br/>
                        Western New York Regents Region<br/>
                        Chautauqua County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Jamestown Community College Cattaraugus County Campus<br/>
                        260 N Union St<br/>
                        Olean, NY&nbsp;14760<br/>
                        <div id="phone19">&nbsp;</div>
                        
                        <a href="http://www.sunyjcc.edu">http://www.sunyjcc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone19").innerHTML = displayStaticPhoneNumber("7163767500") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Daniel&nbsp;Demarte,&nbsp;Chief Executive Officer<br/>
                        SUNY Community Colleges<br/>
                        Western New York Regents Region<br/>
                        Cattaraugus County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Jefferson Community College<br/>
                        1220 Coffeen St<br/>
                        Watertown, NY&nbsp;13601<br/>
                        <div id="phone20">&nbsp;</div>
                        
                        <a href="http://www.sunyjefferson.edu">http://www.sunyjefferson.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone20").innerHTML = displayStaticPhoneNumber("3157862277") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Ty&nbsp;Stone,&nbsp;Chief Executive Officer<br/>
                        SUNY Community Colleges<br/>
                        Northern Regents Region<br/>
                        Jefferson County<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="M">M</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Mohawk Valley Community College<br/>
                        1101 Sherman Dr<br/>
                        Utica, NY&nbsp;13501-5394<br/>
                        <div id="phone21">&nbsp;</div>
                        
                        <a href="http://www.mvcc.edu">http://www.mvcc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone21").innerHTML = displayStaticPhoneNumber("3157925400") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Randall&nbsp;Vanwagoner,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        Mohawk Valley Regents Region<br/>
                        Oneida County<br/>
                        Judicial District V
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Mohawk Valley Community College-Rome Campus<br/>
                        1101 Floyd Ave<br/>
                        Rome, NY&nbsp;13440-4699<br/>
                        <div id="phone22">&nbsp;</div>
                        
                        <a href="http://www.mvcc.edu">http://www.mvcc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone22").innerHTML = displayStaticPhoneNumber("3153393470") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Randall&nbsp;Vanwagoner,&nbsp;Chief Executive Officer<br/>
                        SUNY Community Colleges<br/>
                        Mohawk Valley Regents Region<br/>
                        Oneida County<br/>
                        Judicial District V
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Monroe Community College<br/>
                        1000 E Henrietta Rd<br/>
                        Rochester, NY&nbsp;14623-5780<br/>
                        <div id="phone23">&nbsp;</div>
                        
                        <a href="http://www.monroecc.edu/">http://www.monroecc.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone23").innerHTML = displayStaticPhoneNumber("5852922000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Anne&nbsp;Kress,&nbsp;Chief Executive Officer<br/>
                        SUNY Community Colleges<br/>
                        Finger Lakes Regents Region<br/>
                        Monroe County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Monroe Community College - Downtown Campus<br/>
                        321 State St<br/>
                        Rochester, NY&nbsp;14650<br/>
                        <div id="phone24">&nbsp;</div>
                        
                        <a href="http://www.monroecc.edu/downtown">http://www.monroecc.edu/downtown</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone24").innerHTML = displayStaticPhoneNumber("5852621600") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Joel&nbsp;Frater,&nbsp;Executive Dean<br/>
                        SUNY Community Colleges<br/>
                        Finger Lakes Regents Region<br/>
                        Monroe County<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="N">N</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Nassau Community College<br/>
                        One Education Dr<br/>
                        Garden City, NY&nbsp;11530<br/>
                        <div id="phone25">&nbsp;</div>
                        
                        <a href="http://www.ncc.edu">http://www.ncc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone25").innerHTML = displayStaticPhoneNumber("5165727501") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Jermaine&nbsp;Williams,&nbsp;Chief Executive Officer<br/>
                        SUNY Community Colleges<br/>
                        Long Island Regents Region<br/>
                        Nassau County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York State College of Agriculture And Life Sciences at Cornell<br/>
                        260 Roberts Hall<br/>
                        Ithaca, NY&nbsp;14853-5901<br/>
                        <div id="phone26">&nbsp;</div>
                        
                        <a href="http://https://cals.cornell.edu/">http://https://cals.cornell.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone26").innerHTML = displayStaticPhoneNumber("6072545137") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Martha&nbsp;Pollack,&nbsp;President<br/>
                        SUNY Statutory Colleges<br/>
                        Southern Tier Regents Region<br/>
                        Tompkins County<br/>
                        Judicial District VI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York State College of Human Ecology at Cornell University<br/>
                        College of Human Ecology<br/>
                        Ithaca, NY&nbsp;14853<br/>
                        <div id="phone27">&nbsp;</div>
                        
                        <a href="http://www.human.cornell.edu">http://www.human.cornell.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone27").innerHTML = displayStaticPhoneNumber("6072552247") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Martha&nbsp;Pollack,&nbsp;President<br/>
                        SUNY Statutory Colleges<br/>
                        Southern Tier Regents Region<br/>
                        Tompkins County<br/>
                        Judicial District VI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York State College of Veterinary Medicine at Cornell University<br/>
                        College of Veterinary Medicine<br/>
                        Ithaca, NY&nbsp;14853<br/>
                        <div id="phone28">&nbsp;</div>
                        
                        <a href="http://https://www.vet.cornell.edu/">http://https://www.vet.cornell.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone28").innerHTML = displayStaticPhoneNumber("6072533000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Martha&nbsp;Pollack,&nbsp;Chief Executive Officer<br/>
                        SUNY Statutory Colleges<br/>
                        Southern Tier Regents Region<br/>
                        Tompkins County<br/>
                        Judicial District VI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        New York State School of Industrial And Labor Relations at Cornell<br/>
                        Sch of Industrial And Labor Rels<br/>
                        Ithaca, NY&nbsp;14851<br/>
                        <div id="phone29">&nbsp;</div>
                        
                        <a href="http://www.ilr.cornell.edu">http://www.ilr.cornell.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone29").innerHTML = displayStaticPhoneNumber("6072552185") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Martha&nbsp;Pollack,&nbsp;Chief Executive Officer<br/>
                        SUNY Statutory Colleges<br/>
                        Southern Tier Regents Region<br/>
                        Tompkins County<br/>
                        Judicial District VI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Niagara County Community College<br/>
                        3111 Saunders Settlement Rd<br/>
                        Sanborn, NY&nbsp;14132<br/>
                        <div id="phone30">&nbsp;</div>
                        
                        <a href="http://niagaracc.suny.edu">http://niagaracc.suny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone30").innerHTML = displayStaticPhoneNumber("7166146222") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;William&nbsp;Murabito,&nbsp;Chief Executive Director<br/>
                        SUNY Community Colleges<br/>
                        Western New York Regents Region<br/>
                        Niagara County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        North Country Community College<br/>
                        23 Santanoni Ave<br/>
                        Saranac Lake, NY&nbsp;12983<br/>
                        <div id="phone31">&nbsp;</div>
                        
                        <a href="http://www.nccc.edu">http://www.nccc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone31").innerHTML = displayStaticPhoneNumber("5188912915") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Joseph&nbsp;Keegan,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        Northern Regents Region<br/>
                        Essex County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        North Country Community College-Elizabethtown Campus<br/>
                        Hubbard Hall<br/>
                        Elizabethtown, NY&nbsp;12932<br/>
                        <div id="phone32">&nbsp;</div>
                        
                        <a href="http://">http://</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone32").innerHTML = displayStaticPhoneNumber("") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Carol&nbsp;Brown,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        Northern Regents Region<br/>
                        Essex County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        North Country Community College-Malone Campus<br/>
                        Harrison School<br/>
                        Malone, NY&nbsp;12953<br/>
                        <div id="phone33">&nbsp;</div>
                        
                        <a href="http://www.nccc.edu">http://www.nccc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone33").innerHTML = displayStaticPhoneNumber("5188912915") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Joseph&nbsp;Keegan,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        Northern Regents Region<br/>
                        Franklin County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        North Country Community College-Ticonderoga Campus<br/>
                        Montcalm St<br/>
                        Ticonderoga, NY&nbsp;12883<br/>
                        <div id="phone34">&nbsp;</div>
                        
                        <a href="http://www.nccc.edu">http://www.nccc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone34").innerHTML = displayStaticPhoneNumber("5188912915") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Joseph&nbsp;Keegan,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        Northern Regents Region<br/>
                        Essex County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        NYS College of Ceramics at Alfred University<br/>
                        2 Pine Street<br/>
                        Alfred, NY&nbsp;14802-1296<br/>
                        <div id="phone35">&nbsp;</div>
                        
                        <a href="http://www.alfred.edu">http://www.alfred.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone35").innerHTML = displayStaticPhoneNumber("6078712115") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Mark&nbsp;Zupan,&nbsp;Chief Executive Officer<br/>
                        SUNY Statutory Colleges<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="O">O</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Onondaga Community College<br/>
                        4585 West Seneca Turnpike<br/>
                        Syracuse, NY&nbsp;13215<br/>
                        <div id="phone36">&nbsp;</div>
                        
                        <a href="http://www.sunyocc.edu">http://www.sunyocc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone36").innerHTML = displayStaticPhoneNumber("3154982622") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Kathleen&nbsp;Crabill,&nbsp;Chief Executive Officer<br/>
                        SUNY Community Colleges<br/>
                        Central New York Regents Region<br/>
                        Onondaga County<br/>
                        Judicial District V
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Orange County Comm College - Newburgh<br/>
                        One Washinton Ctr<br/>
                        Newburgh, NY&nbsp;12550<br/>
                        <div id="phone37">&nbsp;</div>
                        
                        <a href="http://www.sunyorange.edu">http://www.sunyorange.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone37").innerHTML = displayStaticPhoneNumber("8453414700") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Kristine&nbsp;Young,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        Hudson Valley Regents Region<br/>
                        Orange County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Orange County Community College<br/>
                        115 South St<br/>
                        Middletown, NY&nbsp;10940<br/>
                        <div id="phone38">&nbsp;</div>
                        
                        <a href="http://www.sunyorange.edu">http://www.sunyorange.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone38").innerHTML = displayStaticPhoneNumber("8453446222") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Kristine&nbsp;Young,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        Hudson Valley Regents Region<br/>
                        Orange County<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="R">R</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Rockland Community College<br/>
                        145 College Rd<br/>
                        Suffern, NY&nbsp;10901<br/>
                        <div id="phone39">&nbsp;</div>
                        
                        <a href="http://www.sunyrockland.edu">http://www.sunyrockland.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone39").innerHTML = displayStaticPhoneNumber("8455744000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Michael&nbsp;Baston,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        Hudson Valley Regents Region<br/>
                        Rockland County<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="S">S</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Schenectady County Community College<br/>
                        78 Washington Ave<br/>
                        Schenectady, NY&nbsp;12305<br/>
                        <div id="phone40">&nbsp;</div>
                        
                        <a href="http://sunysccc.edu">http://sunysccc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone40").innerHTML = displayStaticPhoneNumber("5183811200") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Steady&nbsp;Moono,&nbsp;Chief Executive Officer<br/>
                        SUNY Community Colleges<br/>
                        Capital District Regents Region<br/>
                        Schenectady County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University College at Plattsburgh<br/>
                        101 Broad Street<br/>
                        Plattsburgh, NY&nbsp;12901<br/>
                        <div id="phone41">&nbsp;</div>
                        
                        <a href="http://www.plattsburgh.edu">http://www.plattsburgh.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone41").innerHTML = displayStaticPhoneNumber("5185642000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Josee&nbsp;Larochelle,&nbsp;Chief Executive Officer<br/>
                        SUNY University Colleges<br/>
                        Northern Regents Region<br/>
                        Clinton County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University College of Oswego - Metro Center<br/>
                        2 Clinton Square<br/>
                        Syracuse, NY&nbsp;13202<br/>
                        <div id="phone42">&nbsp;</div>
                        
                        <a href="http://https://www.oswego.edu/syracuse/">http://https://www.oswego.edu/syracuse/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone42").innerHTML = displayStaticPhoneNumber("3153994100") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Deborah&nbsp;Stanley,&nbsp;Chief Executive Officer<br/>
                        SUNY Health Science Centers<br/>
                        Central New York Regents Region<br/>
                        Onondaga County<br/>
                        Judicial District V
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York at Albany<br/>
                        1400 Washington Avenue<br/>
                        Albany, NY&nbsp;12222<br/>
                        <div id="phone43">&nbsp;</div>
                        
                        <a href="http://www.albany.edu">http://www.albany.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone43").innerHTML = displayStaticPhoneNumber("5184223300") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Havidan&nbsp;Rodriguez,&nbsp;President<br/>
                        SUNY University Centers<br/>
                        Capital District Regents Region<br/>
                        Albany County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York at Binghamton<br/>
                        4400 Vestal Parkway East<br/>
                        Binghamton, NY&nbsp;13902-6000<br/>
                        <div id="phone44">&nbsp;</div>
                        
                        <a href="http://www.binghamton.edu">http://www.binghamton.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone44").innerHTML = displayStaticPhoneNumber("6077772000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Harvey&nbsp;Stenger,&nbsp;President<br/>
                        SUNY University Centers<br/>
                        Southern Tier Regents Region<br/>
                        Broome County<br/>
                        Judicial District VI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York at Buffalo<br/>
                        12 Capen Hall<br/>
                        Buffalo, NY&nbsp;14260-1660<br/>
                        <div id="phone45">&nbsp;</div>
                        
                        <a href="http://www.buffalo.edu">http://www.buffalo.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone45").innerHTML = displayStaticPhoneNumber("7166452000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Satish&nbsp;Tripathi,&nbsp;Chief Executive Officer<br/>
                        SUNY University Centers<br/>
                        Western New York Regents Region<br/>
                        Erie County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York at Stony Brook<br/>
                        310 Administration<br/>
                        Stony Brook, NY&nbsp;11794-701<br/>
                        <div id="phone46">&nbsp;</div>
                        
                        <a href="http://www.stonybrook.edu">http://www.stonybrook.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone46").innerHTML = displayStaticPhoneNumber("6316326000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Michael&nbsp;Bernstein,&nbsp;Chief Executive Officer<br/>
                        SUNY University Centers<br/>
                        Long Island Regents Region<br/>
                        Suffolk County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York College at Brockport<br/>
                        350 New Campus Drive<br/>
                        Brockport, NY&nbsp;14420<br/>
                        <div id="phone47">&nbsp;</div>
                        
                        <a href="http://https://www.brockport.edu">http://https://www.brockport.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone47").innerHTML = displayStaticPhoneNumber("5853952361") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Heidi&nbsp;Macpherson,&nbsp;Chief Executive Officer<br/>
                        SUNY University Colleges<br/>
                        Finger Lakes Regents Region<br/>
                        Monroe County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York College at Buffalo<br/>
                        1300 Elmwood Ave<br/>
                        Buffalo, NY&nbsp;14222<br/>
                        <div id="phone48">&nbsp;</div>
                        
                        <a href="http://suny.buffalostate.edu">http://suny.buffalostate.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone48").innerHTML = displayStaticPhoneNumber("7168784000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Kathleen&nbsp;Conway Turner,&nbsp;Chief Executive Officer<br/>
                        SUNY University Colleges<br/>
                        Western New York Regents Region<br/>
                        Erie County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York College at Cortland<br/>
                        SUNY Cortland<br/>
                        Cortland, NY&nbsp;13045-900<br/>
                        <div id="phone49">&nbsp;</div>
                        
                        <a href="http://www2.cortland.edu">http://www2.cortland.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone49").innerHTML = displayStaticPhoneNumber("6077532011") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Erik&nbsp;Bitterbaum,&nbsp;President<br/>
                        SUNY University Colleges<br/>
                        Central New York Regents Region<br/>
                        Cortland County<br/>
                        Judicial District VI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York College at Fredonia<br/>
                        SUNY Fredonia<br/>
                        Fredonia, NY&nbsp;14063<br/>
                        <div id="phone50">&nbsp;</div>
                        
                        <a href="http://www.fredonia.edu">http://www.fredonia.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone50").innerHTML = displayStaticPhoneNumber("7166733111") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Dennis&nbsp;Hefner,&nbsp;President<br/>
                        SUNY University Colleges<br/>
                        Western New York Regents Region<br/>
                        Chautauqua County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York College at Geneseo<br/>
                        1 College Circle<br/>
                        Geneseo, NY&nbsp;14454<br/>
                        <div id="phone51">&nbsp;</div>
                        
                        <a href="http://www.geneseo.edu">http://www.geneseo.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone51").innerHTML = displayStaticPhoneNumber("5852455000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Denise&nbsp;Battles,&nbsp;President<br/>
                        SUNY University Colleges<br/>
                        Finger Lakes Regents Region<br/>
                        Livingston County<br/>
                        Judicial District VII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York College at New Paltz<br/>
                        One Hawk Dr<br/>
                        New Paltz, NY&nbsp;12561-2443<br/>
                        <div id="phone52">&nbsp;</div>
                        
                        <a href="http://www.newpaltz.edu">http://www.newpaltz.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone52").innerHTML = displayStaticPhoneNumber("8452577869") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Donald&nbsp;Christian,&nbsp;Chief Executive Officer<br/>
                        SUNY University Colleges<br/>
                        Hudson Valley Regents Region<br/>
                        Ulster County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York College at Old Westbury<br/>
                        223 Store Hill Rd<br/>
                        Old Westbury, NY&nbsp;11568<br/>
                        <div id="phone53">&nbsp;</div>
                        
                        <a href="http://www.oldwestbury.edu">http://www.oldwestbury.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone53").innerHTML = displayStaticPhoneNumber("5168763000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Calvin&nbsp;Butts,&nbsp;President<br/>
                        SUNY University Colleges<br/>
                        Long Island Regents Region<br/>
                        Nassau County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York College at Oneonta<br/>
                        Ravine Parkway<br/>
                        Oneonta, NY&nbsp;13820-4015<br/>
                        <div id="phone54">&nbsp;</div>
                        
                        <a href="http://www.oneonta.edu">http://www.oneonta.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone54").innerHTML = displayStaticPhoneNumber("6074363500") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Barbara&nbsp;Morris,&nbsp;President<br/>
                        SUNY University Colleges<br/>
                        Mohawk Valley Regents Region<br/>
                        Otsego County<br/>
                        Judicial District VI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York College at Oswego<br/>
                        Rm 706, Culkin Hall<br/>
                        Oswego, NY&nbsp;13126<br/>
                        <div id="phone55">&nbsp;</div>
                        
                        <a href="http://www.oswego.edu">http://www.oswego.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone55").innerHTML = displayStaticPhoneNumber("3153122500") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Deborah&nbsp;Stanley,&nbsp;President<br/>
                        SUNY University Colleges<br/>
                        Central New York Regents Region<br/>
                        Oswego County<br/>
                        Judicial District V
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York College at Potsdam<br/>
                        44 Pierrepont Ave<br/>
                        Potsdam, NY&nbsp;13676-2294<br/>
                        <div id="phone56">&nbsp;</div>
                        
                        <a href="http://www.potsdam.edu">http://www.potsdam.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone56").innerHTML = displayStaticPhoneNumber("3152672000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Kristin&nbsp;Esterberg,&nbsp;Chief Executive Officer<br/>
                        SUNY University Colleges<br/>
                        Northern Regents Region<br/>
                        Saint Lawrence County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York College at Purchase<br/>
                        735 Anderson Hill Road<br/>
                        Purchase, NY&nbsp;10577-1400<br/>
                        <div id="phone57">&nbsp;</div>
                        
                        <a href="http://www.purchase.edu">http://www.purchase.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone57").innerHTML = displayStaticPhoneNumber("9142516010") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Dennis&nbsp;Craig,&nbsp;President<br/>
                        SUNY University Colleges<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York College of Environmental Science And Forestry<br/>
                        224 Bray Hall<br/>
                        Syracuse, NY&nbsp;13210<br/>
                        <div id="phone58">&nbsp;</div>
                        
                        <a href="http://www.esf.edu">http://www.esf.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone58").innerHTML = displayStaticPhoneNumber("3154706500") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;David&nbsp;Amberg,&nbsp;Chief Executive Officer<br/>
                        SUNY Specialized Colleges<br/>
                        Central New York Regents Region<br/>
                        Onondaga County<br/>
                        Judicial District V
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York College of Optometry<br/>
                        33 West 42nd Street<br/>
                        New York, NY&nbsp;10036<br/>
                        <div id="phone59">&nbsp;</div>
                        
                        <a href="http://www.sunyopt.edu">http://www.sunyopt.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone59").innerHTML = displayStaticPhoneNumber("2129384000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;David&nbsp;Heath,&nbsp;President<br/>
                        SUNY Specialized Colleges<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York College of Technology at Delhi<br/>
                        454 Delhi Dr<br/>
                        Delhi, NY&nbsp;13753<br/>
                        <div id="phone60">&nbsp;</div>
                        
                        <a href="http://www.delhi.edu">http://www.delhi.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone60").innerHTML = displayStaticPhoneNumber("6077464000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Michael&nbsp;Laliberte,&nbsp;Chief Executive Officer<br/>
                        SUNY Ag And Tech Colleges<br/>
                        Southern Tier Regents Region<br/>
                        Delaware County<br/>
                        Judicial District VI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York Empire State College<br/>
                        One Union Ave<br/>
                        Saratoga Springs, NY&nbsp;12866<br/>
                        <div id="phone61">&nbsp;</div>
                        
                        <a href="http://www.esc.edu">http://www.esc.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone61").innerHTML = displayStaticPhoneNumber("5185872100") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;James&nbsp;Malatras,&nbsp;Chief Executive Officer<br/>
                        SUNY University Colleges<br/>
                        Capital District Regents Region<br/>
                        Saratoga County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York Health Science Center at Brooklyn<br/>
                        450 Clarkson Avenue<br/>
                        Brooklyn, NY&nbsp;11203-3780<br/>
                        <div id="phone62">&nbsp;</div>
                        
                        <a href="http://www.downstate.edu/">http://www.downstate.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone62").innerHTML = displayStaticPhoneNumber("7182701000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Wayne&nbsp;Riley,&nbsp;Chief Executive Officer<br/>
                        SUNY Health Science Centers<br/>
                        New York City Regents Region<br/>
                        Kings County<br/>
                        Judicial District II
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York Health Science Center at Syracuse<br/>
                        750 East Adams Street<br/>
                        Syracuse, NY&nbsp;13210<br/>
                        <div id="phone63">&nbsp;</div>
                        
                        <a href="http://www.upstate.edu/">http://www.upstate.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone63").innerHTML = displayStaticPhoneNumber("3154645540") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        &nbsp;Mantosh&nbsp;Dewan,&nbsp;Chief Executive Officer<br/>
                        SUNY Health Science Centers<br/>
                        Central New York Regents Region<br/>
                        Onondaga County<br/>
                        Judicial District V
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        State University of New York System Administration<br/>
                        State University Plaza<br/>
                        Albany, NY&nbsp;12246<br/>
                        <div id="phone64">&nbsp;</div>
                        
                        <a href="http://www.suny.edu">http://www.suny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone64").innerHTML = displayStaticPhoneNumber("5183201240") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Kristina&nbsp;Johnson,&nbsp;Chancellor<br/>
                        SUNY University Centers<br/>
                        Capital District Regents Region<br/>
                        Albany County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        SUC at Plattsburgh at Adirondack Community College<br/>
                        667 Bay Rd<br/>
                        Queensbury, NY&nbsp;12804<br/>
                        <div id="phone65">&nbsp;</div>
                        
                        <a href="http://www.plattsburgh.edu/">http://www.plattsburgh.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone65").innerHTML = displayStaticPhoneNumber("5187925425") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Josee&nbsp;Larochelle,&nbsp;Chief Executive Officer<br/>
                        SUNY University Centers<br/>
                        Capital District Regents Region<br/>
                        Warren County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Suffolk County Community College<br/>
                        533 College Rd<br/>
                        Selden, NY&nbsp;11784<br/>
                        <div id="phone66">&nbsp;</div>
                        
                        <a href="http://www.sunysuffolk.edu">http://www.sunysuffolk.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone66").innerHTML = displayStaticPhoneNumber("6314514000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Shaun&nbsp;McKay,&nbsp;Chief Executive Officer<br/>
                        SUNY Community Colleges<br/>
                        Long Island Regents Region<br/>
                        Suffolk County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Suffolk County Community College Eastern Campus<br/>
                        Speonk-Riverhead Rd<br/>
                        Riverhead, NY&nbsp;11901<br/>
                        <div id="phone67">&nbsp;</div>
                        
                        <a href="http://www.sunysuffolk.edu">http://www.sunysuffolk.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone67").innerHTML = displayStaticPhoneNumber("6315482565") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Shaun&nbsp;McKay,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        Long Island Regents Region<br/>
                        Suffolk County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Suffolk County Community College Western Campus<br/>
                        Western Campus Crooked Hill Rd<br/>
                        Brentwood, NY&nbsp;11717<br/>
                        <div id="phone68">&nbsp;</div>
                        
                        <a href="http://www.sunysuffolk.edu">http://www.sunysuffolk.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone68").innerHTML = displayStaticPhoneNumber("6314346782") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Shaun&nbsp;McKay,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        Long Island Regents Region<br/>
                        Suffolk County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Sullivan County Community College<br/>
                        112 College Rd<br/>
                        Loch Sheldrake, NY&nbsp;12759<br/>
                        <div id="phone69">&nbsp;</div>
                        
                        <a href="http://www.sunysullivan.edu">http://www.sunysullivan.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone69").innerHTML = displayStaticPhoneNumber("8454345750") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Jay&nbsp;Quaintance,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        Hudson Valley Regents Region<br/>
                        Sullivan County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        SUNY Coll of Ag & Tech at Delhi - Sccc<br/>
                        78 Washington Ave<br/>
                        Schenectady, NY&nbsp;12305<br/>
                        <div id="phone70">&nbsp;</div>
                        
                        <a href="http://WWW.DELHI.EDU">http://www.delhi.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone70").innerHTML = displayStaticPhoneNumber("5183811497") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Michael&nbsp;Laliberte,&nbsp;Chief Executive Officer<br/>
                        SUNY Ag And Tech Colleges<br/>
                        Capital District Regents Region<br/>
                        Schenectady County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        SUNY College of  Agriculture And Technology at Morrisville<br/>
                        SUNY Morrisville<br/>
                        Morrisville, NY&nbsp;13408<br/>
                        <div id="phone71">&nbsp;</div>
                        
                        <a href="http://www.morrisville.edu">http://www.morrisville.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone71").innerHTML = displayStaticPhoneNumber("3156846000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;David&nbsp;Rogers,&nbsp;Chief Executive Officer<br/>
                        SUNY Ag And Tech Colleges<br/>
                        Central New York Regents Region<br/>
                        Madison County<br/>
                        Judicial District VI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        SUNY College of  Technology at Alfred Wellsville Campus<br/>
                        Wellsville Campus<br/>
                        Wellsville, NY&nbsp;14895<br/>
                        <div id="phone72">&nbsp;</div>
                        
                        <a href="http://www.alfredstate.edu">http://www.alfredstate.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone72").innerHTML = displayStaticPhoneNumber("6075874111") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Irby&nbsp;Sullivan,&nbsp;Chief Executive Officer<br/>
                        SUNY Ag And Tech Colleges<br/>
                        Western New York Regents Region<br/>
                        Allegany County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        SUNY College of Agriculture And Technology at Cobleskill<br/>
                        SUNY Cobleskill<br/>
                        Cobleskill, NY&nbsp;12043<br/>
                        <div id="phone73">&nbsp;</div>
                        
                        <a href="http://www.cobleskill.edu">http://www.cobleskill.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone73").innerHTML = displayStaticPhoneNumber("5182345011") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Marion&nbsp;Terenzio,&nbsp;Chief Executive Officer<br/>
                        SUNY Ag And Tech Colleges<br/>
                        Mohawk Valley Regents Region<br/>
                        Schoharie County<br/>
                        Judicial District III
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        SUNY College of Agriculture And Technology at Morrisville - Norwich Campus<br/>
                        16 South Broad Street<br/>
                        Norwich, NY&nbsp;13815<br/>
                        <div id="phone74">&nbsp;</div>
                        
                        <a href="http://www.morrisville.edu/norwich">http://www.morrisville.edu/norwich</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone74").innerHTML = displayStaticPhoneNumber("6073345144") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;David&nbsp;Rogers,&nbsp;Chief Executive Officer<br/>
                        SUNY Ag And Tech Colleges<br/>
                        Southern Tier Regents Region<br/>
                        Chenango County<br/>
                        Judicial District VI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        SUNY College of Technology at Alfred<br/>
                        SUNY Alfred<br/>
                        Alfred, NY&nbsp;14802<br/>
                        <div id="phone75">&nbsp;</div>
                        
                        <a href="http://www.alfredstate.edu">http://www.alfredstate.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone75").innerHTML = displayStaticPhoneNumber("6075874111") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Irby&nbsp;Sullivan,&nbsp;Chief Executive Officer<br/>
                        SUNY Ag And Tech Colleges<br/>
                        Western New York Regents Region<br/>
                        Allegany County<br/>
                        Judicial District VIII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        SUNY College of Technology at Canton<br/>
                        34 Cornell Drive<br/>
                        Canton, NY&nbsp;13617<br/>
                        <div id="phone76">&nbsp;</div>
                        
                        <a href="http://www.canton.edu/">http://www.canton.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone76").innerHTML = displayStaticPhoneNumber("8003887123") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Zvi&nbsp;Szafran,&nbsp;Chief Executive Officer<br/>
                        SUNY Ag And Tech Colleges<br/>
                        Northern Regents Region<br/>
                        Saint Lawrence County<br/>
                        Judicial District IV
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        SUNY College of Technology at Farmingdale<br/>
                        2350 Broadhollow Rd<br/>
                        Farmingdale, NY&nbsp;11735<br/>
                        <div id="phone77">&nbsp;</div>
                        
                        <a href="http://www.farmingdale.edu">http://www.farmingdale.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone77").innerHTML = displayStaticPhoneNumber("6314202000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;John&nbsp;Nader,&nbsp;President<br/>
                        SUNY Ag And Tech Colleges<br/>
                        Long Island Regents Region<br/>
                        Suffolk County<br/>
                        Judicial District X
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        SUNY Maritime College<br/>
                        Fort Schuyler<br/>
                        Bronx, NY&nbsp;10465<br/>
                        <div id="phone78">&nbsp;</div>
                        
                        <a href="http://www.sunymaritime.edu">http://www.sunymaritime.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone78").innerHTML = displayStaticPhoneNumber("7184097200") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Rear Admiral&nbsp;Michael&nbsp;Alfultis,&nbsp;Chief Executive Officer<br/>
                        SUNY Specialized Colleges<br/>
                        New York City Regents Region<br/>
                        Bronx County<br/>
                        Judicial District XII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        SUNY Polytechnic Institute<br/>
                        100 Seymour Rd<br/>
                        Utica, NY&nbsp;13502<br/>
                        <div id="phone79">&nbsp;</div>
                        
                        <a href="http://www.sunypoly.edu">http://www.sunypoly.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone79").innerHTML = displayStaticPhoneNumber("3157927100") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Grace&nbsp;Wang,&nbsp;Chief Executive Officer<br/>
                        SUNY University Colleges<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="T">T</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Tompkins Cortland Community College<br/>
                        170 North St<br/>
                        Dryden, NY&nbsp;13053<br/>
                        <div id="phone80">&nbsp;</div>
                        
                        <a href="http://www.tc3.edu">http://www.tc3.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone80").innerHTML = displayStaticPhoneNumber("6078448211") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Orinthia&nbsp;Montague,&nbsp;Chief Executive Officer<br/>
                        SUNY Community Colleges<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="U">U</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Ulster County Community College<br/>
                        Cottekill Rd<br/>
                        Stone Ridge, NY&nbsp;12484<br/>
                        <div id="phone81">&nbsp;</div>
                        
                        <a href="http://www.sunyulster.edu">http://www.sunyulster.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone81").innerHTML = displayStaticPhoneNumber("8456875000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Alan&nbsp;Roberts,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        Hudson Valley Regents Region<br/>
                        Ulster County<br/>
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
        
    </tbody>
</table>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="W">W</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Westchester Community College<br/>
                        75 Grasslands Rd<br/>
                        Valhalla, NY&nbsp;10595-1693<br/>
                        <div id="phone82">&nbsp;</div>
                        
                        <a href="http://www.sunywcc.edu/">http://www.sunywcc.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone82").innerHTML = displayStaticPhoneNumber("9146066600") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Belinda&nbsp;Miles,&nbsp;President<br/>
                        SUNY Community Colleges<br/>
                        Hudson Valley Regents Region<br/>
                        Westchester County<br/>
                        Judicial District IX
                    </td>
                </tr>
            
    </tbody>
'''





soup = BeautifulSoup(html, 'html5lib')

org_url_list = []
fin = []


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






















