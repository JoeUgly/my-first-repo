
# Desc: Combine URLs and coordinates for every CUNY university

# Must use similar code to get each school type. eg: SUNY, CUNY, Independent, Proprietary

# URLs' HTML source: http://eservices.nysed.gov/collegedirectory/index.htm
# Coords source: http://eservices.nysed.gov/sedreports/list?id=1
# All Institutions: Active Institutions with GIS coordinates and OITS Accuracy Code - Select by County






from bs4 import BeautifulSoup
import pandas as pd



html = '''
<table>
 <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="B">B</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Borough of Manhattan Comm College<br/>
                        199 Chambers St<br/>
                        New York, NY&nbsp;10007<br/>
                        <div id="phone0">&nbsp;</div>
                        
                        <a href="http://www.bmcc.cuny.edu/j2ee/index.jsp">http://www.bmcc.cuny.edu/j2ee/index.jsp</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone0").innerHTML = displayStaticPhoneNumber("2122208000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Karrin&nbsp;Wilks,&nbsp;Chief Executive Officer<br/>
                        CUNY Community College<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Bronx Community College<br/>
                        2155 University Ave<br/>
                        Bronx, NY&nbsp;10453<br/>
                        <div id="phone1">&nbsp;</div>
                        
                        <a href="http://www.bcc.cuny.edu/">http://www.bcc.cuny.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone1").innerHTML = displayStaticPhoneNumber("7182895100") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Thomas&nbsp;Isekenegbe,&nbsp;President<br/>
                        CUNY Community College<br/>
                        New York City Regents Region<br/>
                        Bronx County<br/>
                        Judicial District XII
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
                        City University of New York Brooklyn College<br/>
                        2900 Bedford Ave<br/>
                        Brooklyn, NY&nbsp;11210<br/>
                        <div id="phone2">&nbsp;</div>
                        
                        <a href="http://www.brooklyn.cuny.edu">http://www.brooklyn.cuny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone2").innerHTML = displayStaticPhoneNumber("7189515671") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Michelle&nbsp;Anderson,&nbsp;Chief Executive Officer<br/>
                        CUNY 4 Year College<br/>
                        New York City Regents Region<br/>
                        Kings County<br/>
                        Judicial District II
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        City University of New York Central Administration<br/>
                        205 East 42nd St<br/>
                        New York, NY&nbsp;10017<br/>
                        <div id="phone3">&nbsp;</div>
                        
                        <a href="http://www.cuny.edu">http://www.cuny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone3").innerHTML = displayStaticPhoneNumber("6466649100") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Felix&nbsp;Matos Rodriguez,&nbsp;Chief Executive Officer<br/>
                        CUNY Graduate Center<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        City University of New York College of Staten Island<br/>
                        2800 Victory Blvd<br/>
                        Staten Island, NY&nbsp;10314-6600<br/>
                        <div id="phone4">&nbsp;</div>
                        
                        <a href="http://www.csi.cuny.edu">http://www.csi.cuny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone4").innerHTML = displayStaticPhoneNumber("7189822000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;William&nbsp;Fritz,&nbsp;Chief Executive Officer<br/>
                        CUNY Community College<br/>
                        New York City Regents Region<br/>
                        Richmond County<br/>
                        Judicial District Xiii
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        City University of New York Herbert H. Lehman College<br/>
                        Bedford Park Blvd W<br/>
                        Bronx, NY&nbsp;10468<br/>
                        <div id="phone5">&nbsp;</div>
                        
                        <a href="http://www.lehman.cuny.edu">http://www.lehman.cuny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone5").innerHTML = displayStaticPhoneNumber("7188608111") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;Daniel&nbsp;Lemons,&nbsp;Chief Executive Officer<br/>
                        CUNY 4 Year College<br/>
                        New York City Regents Region<br/>
                        Bronx County<br/>
                        Judicial District XII
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        City University of New York John Jay College of Criminal Justice<br/>
                        899 10th Ave<br/>
                        New York, NY&nbsp;10019<br/>
                        <div id="phone6">&nbsp;</div>
                        
                        <a href="http://www.jjay.cuny.edu">http://www.jjay.cuny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone6").innerHTML = displayStaticPhoneNumber("2122378000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Ms.&nbsp;Karol&nbsp;Mason,&nbsp;President<br/>
                        CUNY 4 Year College<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        CUNY Bernard M. Baruch College<br/>
                        17 Lexington Ave<br/>
                        New York, NY&nbsp;10010<br/>
                        <div id="phone7">&nbsp;</div>
                        
                        <a href="http://www.baruch.cuny.edu">http://www.baruch.cuny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone7").innerHTML = displayStaticPhoneNumber("6463121000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Mitchel&nbsp;Wallerstein,&nbsp;President<br/>
                        CUNY 4 Year College<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        CUNY City College<br/>
                        Convent Ave & 138 St<br/>
                        New York, NY&nbsp;10031<br/>
                        <div id="phone8">&nbsp;</div>
                        
                        <a href="http://www.ccny.cuny.edu">http://www.ccny.cuny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone8").innerHTML = displayStaticPhoneNumber("2126507285") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Vincent&nbsp;Boudreau,&nbsp;Chief Executive Officer<br/>
                        CUNY 4 Year College<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        CUNY Graduate School And University Center<br/>
                        365 5th Ave<br/>
                        New York, NY&nbsp;10016<br/>
                        <div id="phone9">&nbsp;</div>
                        
                        <a href="http://www.gc.cuny.edu">http://www.gc.cuny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone9").innerHTML = displayStaticPhoneNumber("2128177000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;James&nbsp;Muyskens,&nbsp;Chief Executive Officer<br/>
                        CUNY Graduate Center<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        CUNY Hunter College<br/>
                        President's Office 695 Park Ave<br/>
                        New York, NY&nbsp;10021<br/>
                        <div id="phone10">&nbsp;</div>
                        
                        <a href="http://www.hunter.cuny.edu/">http://www.hunter.cuny.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone10").innerHTML = displayStaticPhoneNumber("2127724000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Jennifer&nbsp;Raab,&nbsp;President<br/>
                        CUNY 4 Year College<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        CUNY Law School at Queens<br/>
                        6521 Main St<br/>
                        Flushing, NY&nbsp;11367<br/>
                        <div id="phone11">&nbsp;</div>
                        
                        <a href="http://www.law.cuny.edu">http://www.law.cuny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone11").innerHTML = displayStaticPhoneNumber("7183404200") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Mary&nbsp;Bilek,&nbsp;Chief Executive Officer<br/>
                        CUNY Graduate Center<br/>
                        New York City Regents Region<br/>
                        Queens County<br/>
                        Judicial District XI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        CUNY NYC College of Technology<br/>
                        300 Jay St<br/>
                        Brooklyn, NY&nbsp;11201<br/>
                        <div id="phone12">&nbsp;</div>
                        
                        <a href="http://WWW.CITYTECH.CUNY.EDU">http://www.citytech.cuny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone12").innerHTML = displayStaticPhoneNumber("7182605000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Russell&nbsp;Hotzler,&nbsp;Chief Executive Officer<br/>
                        CUNY 4 Year College<br/>
                        New York City Regents Region<br/>
                        Kings County<br/>
                        Judicial District II
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        CUNY Queens College<br/>
                        65-30 Kissena Blvd<br/>
                        Flushing, NY&nbsp;11367<br/>
                        <div id="phone13">&nbsp;</div>
                        
                        <a href="http://www.qc.cuny.edu">http://www.qc.cuny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone13").innerHTML = displayStaticPhoneNumber("7189975000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;William&nbsp;Tramontano,&nbsp;Chief Executive Officer<br/>
                        CUNY 4 Year College<br/>
                        New York City Regents Region<br/>
                        Queens County<br/>
                        Judicial District XI
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        CUNY School of Professional Studies<br/>
                        119 West 31st St<br/>
                        New York, NY&nbsp;10001<br/>
                        <div id="phone14">&nbsp;</div>
                        
                        <a href="http://">http://</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone14").innerHTML = displayStaticPhoneNumber("2126522869") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Mr.&nbsp;John&nbsp;Mogulescu,&nbsp;Dean, CUNY School of Professional Studies<br/>
                        CUNY 4 Year College<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        CUNY Stella And Charles Guttman Community College<br/>
                        50 W 40 St<br/>
                        New York, NY&nbsp;10018<br/>
                        <div id="phone15">&nbsp;</div>
                        
                        <a href="http://www.guttman.cuny.edu/index.html">http://www.guttman.cuny.edu/index.html</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone15").innerHTML = displayStaticPhoneNumber("6463138000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Scott&nbsp;Evenbeck,&nbsp;President<br/>
                        CUNY Community College<br/>
                        New York City Regents Region<br/>
                        New York County<br/>
                        Judicial District I
                    </td>
                </tr>
            
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        CUNY York College<br/>
                        94-20 G R Brewer Blvd<br/>
                        Jamaica, NY&nbsp;11451<br/>
                        <div id="phone16">&nbsp;</div>
                        
                        <a href="http://www.york.cuny.edu/">http://www.york.cuny.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone16").innerHTML = displayStaticPhoneNumber("7182622000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Marcia&nbsp;Keizs,&nbsp;Chief Executive Officer<br/>
                        CUNY 4 Year College<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="E">E</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Eugenio Maria De Hostos Comm College<br/>
                        475 Grand Concourse<br/>
                        Bronx, NY&nbsp;10451<br/>
                        <div id="phone17">&nbsp;</div>
                        
                        <a href="http://www.hostos.cuny.edu/">http://www.hostos.cuny.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone17").innerHTML = displayStaticPhoneNumber("7185184444") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;David&nbsp;Gomez,&nbsp;President<br/>
                        CUNY Community College<br/>
                        New York City Regents Region<br/>
                        Bronx County<br/>
                        Judicial District XII
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
                        Fiorello H. La Guardia Comm College<br/>
                        31-10 Thomson Ave<br/>
                        Long Island City, NY&nbsp;11101<br/>
                        <div id="phone18">&nbsp;</div>
                        
                        <a href="http://www.lagcc.cuny.edu/">http://www.lagcc.cuny.edu/</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone18").innerHTML = displayStaticPhoneNumber("7184827200") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Gail&nbsp;Mellow,&nbsp;President<br/>
                        CUNY Community College<br/>
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
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="K">K</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Kingsborough Community College<br/>
                        2001 Oriental Blvd<br/>
                        Brooklyn, NY&nbsp;11235<br/>
                        <div id="phone19">&nbsp;</div>
                        
                        <a href="http://WWW.KBCC.CUNY.EDU">http://www.kbcc.cuny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone19").innerHTML = displayStaticPhoneNumber("7183685000") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Claudia&nbsp;Schrader,&nbsp;Chief Executive Officer<br/>
                        CUNY Community College<br/>
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
        
    </tbody>
</table>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="M">M</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Medgar Evers College<br/>
                        1650 Bedford Ave<br/>
                        Brooklyn, NY&nbsp;11225<br/>
                        <div id="phone20">&nbsp;</div>
                        
                        <a href="http://www.mec.cuny.edu">http://www.mec.cuny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone20").innerHTML = displayStaticPhoneNumber("7182706016") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Rudolph&nbsp;Crew,&nbsp;President<br/>
                        CUNY 4 Year College<br/>
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
        
    </tbody>
</table>

<table border="1" cellspacing="0" summary="New York State College and University Campuses Including Chief Executive Officer Alphabetical by Institution within Sector" style="width:90%;border-collapse:collapse;margin-left:5%;margin-bottom:1em;">
    <thead>
        
    </thead>
    <tbody>
        
                <tr><td colspan="2" class="color8" style="font-weight:bold;text-align:center;"><a name="Q">Q</a></td></tr>
                
                <tr>
                    <td style="width:50%;vertical-align:top;"> 
                        Queensborough Community College<br/>
                        222-05 56th Ave<br/>
                        Flushing, NY&nbsp;11364<br/>
                        <div id="phone21">&nbsp;</div>
                        
                        <a href="http://WWW.QCC.CUNY.EDU">http://www.qcc.cuny.edu</a>
                        
                        <script type="text/javascript">
                            document.getElementById("phone21").innerHTML = displayStaticPhoneNumber("7186316262") + "&nbsp;";
                        </script>
                    </td>
                    <td style="width:50%;vertical-align:top;"> 
                        Dr.&nbsp;Timothy&nbsp;Lynch,&nbsp;Chief Executive Officer<br/>
                        CUNY Community College<br/>
                        New York City Regents Region<br/>
                        Queens County<br/>
                        Judicial District XI
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






















