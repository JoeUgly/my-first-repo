
# Desc: Get get org name, home page, and street address from get_org_name_uni.py and pair them with the coords.

# If zip codes disagree, remove street address and city. only use zip



import geopy
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="jj")




all_list = [
['Cornell University', 'http://www.cornell.edu', 'Address\n300 Day Hall Ithaca (population range: 10,000-49,999) 14853 New York United States'],
['Columbia University in the City of New York', 'http://www.columbia.edu', 'Address\nWest 116 Street and Broadway New York City (population range: over 5,000,000) 10027 New York United States'],
['New York University', 'http://www.nyu.edu', 'Address\n70 Washington Square South New York City (population range: over 5,000,000) 10012-1091 New York United States'],
['University at Buffalo, State University of New York', 'http://www.buffalo.edu', 'Address\n12 Capen Hall Buffalo (population range: 250,000-499,999) 14260-1660 New York United States'],
['University of Rochester', 'http://www.rochester.edu', 'Address\n300 Wilson Boulevard Rochester (population range: 50,000-249,999) 14627-0011 New York United States'],
['Rochester Institute of Technology', 'http://www.rit.edu', 'Address\n1 Lomb Memorial Drive Rochester (population range: 50,000-249,999) 14623-5603 New York United States'],
['Rensselaer Polytechnic Institute', 'http://www.rpi.edu', 'Address\n110 8Th Street Troy (population range: 10,000-49,999) 12180-3590 New York United States'],
['Fordham University', 'http://www.fordham.edu', 'Address\n441 E Fordham Road The Bronx (population range: 1,000,000-5,000,000) 10458 New York United States'],
['Stony Brook University', 'http://www.stonybrook.edu', 'Address\n100 Nicolls Road Stony Brook (population range: 10,000-49,999) 11794 New York United States'],
['Syracuse University', 'http://www.syracuse.edu', 'Address\n900 South Crouse Avenue Syracuse (population range: 50,000-249,999) 13244-1100 New York United States'],
['University at Albany, State University of New York', 'http://www.albany.edu', 'Address\n1400 Washington Avenue Albany (population range: 50,000-249,999) 12222 New York United States'],
['The New School', 'http://www.newschool.edu', 'Address\n66 W 12th Street New York City (population range: over 5,000,000) 10011-8603 New York United States'],
['Binghamton University, State University of New York', 'http://www.binghamton.edu', 'Address\n4400 Vestal Parkway East Vestal (population range: 10,000-49,999) 13850-6000 New York United States'],
['Pace University', 'http://www.pace.edu', 'Address\n1 Pace Plaza New York City (population range: over 5,000,000) 10038-1598 New York United States'],
['Yeshiva University', 'http://www.yu.edu', 'Address\n500 W 185Th Street New York City (population range: over 5,000,000) 10033-3299 New York United States'],
['Hofstra University', 'http://www.hofstra.edu', 'Address\n100 Hofstra University Hempstead (population range: 50,000-249,999) 11549 New York United States'],
['Marist College', 'http://www.marist.edu', 'Address\n3399 North Road Poughkeepsie (population range: 10,000-49,999) 12601 New York United States'],
['Vassar College', 'http://www.vassar.edu', 'Address\n124 Raymond Avenue Poughkeepsie (population range: 10,000-49,999) 12604 New York United States'],
['Ithaca College', 'http://www.ithaca.edu', 'Address\n953 Danby Road Ithaca (population range: 10,000-49,999) 14850-7002 New York United States'],
['United States Military Academy', 'http://www.usma.edu', 'Address\n646 Swift Road West Point (population range: 2,500-9,999) 10996-1905 New York United States'],
["St. John's University", 'http://www.stjohns.edu', 'Address\n8000 Utopia Parkway Queens (population range: 1,000,000-5,000,000) 11439 New York United States'],
['School of Visual Arts', 'http://www.sva.edu', 'Address\n209 E 23Rd Street New York City (population range: over 5,000,000) 10010 New York United States'],
['Bard College', 'http://www.bard.edu', 'Address\nAnnandale Road Annandale-on-Hudson (population range: 2,500-9,999) 12504-5000 New York United States'],
['Icahn School of Medicine at Mount Sinai', 'http://www.mssm.edu', 'Address\n1 Gustave L Levy Place New York City (population range: over 5,000,000) 10029-6574 New York United States'],
['State University of New York at Oswego', 'http://www.oswego.edu', 'Address\n7060 State Route 104 Oswego (population range: 10,000-49,999) 13126 New York United States'],
['Buffalo State College', 'http://www.buffalostate.edu', 'Address\n1300 Elmwood Avenue Buffalo (population range: 250,000-499,999) 14222 New York United States'],
['The Rockefeller University', 'http://www.rockefeller.edu', 'Address\n1230 York Avenue New York City (population range: over 5,000,000) 10065-6399 New York United States'],
['Fashion Institute of Technology', 'http://www.fitnyc.edu', 'Address\n227 W 27Th Street New York City (population range: over 5,000,000) 10001-5992 New York United States'],
['Colgate University', 'http://www.colgate.edu', 'Address\n13 Oak Drive Hamilton (population range: 2,500-9,999) 13346-1398 New York United States'],
['Clarkson University', 'http://www.clarkson.edu', 'Address\n8 Clarkson Avenue Potsdam (population range: 10,000-49,999) 13699-5557 New York United States'],
['Pratt Institute', 'http://www.pratt.edu', 'Address\n200 Willoughby Avenue Brooklyn (population range: 1,000,000-5,000,000) 11205 New York United States'],
['Hobart and William Smith Colleges', 'http://www.hws.edu', 'Address\n337 Pulteney Street Geneva (population range: 10,000-49,999) 14456 New York United States'],
['Hamilton College', 'http://www.hamilton.edu', 'Address\n198 College Hill Road Clinton (population range: 2,500-9,999) 13323-1293 New York United States'],
['Long Island University', 'http://www.liu.edu', 'Address\n1 University Plaza Brooklyn (population range: 1,000,000-5,000,000) 11201-8423 New York United States'],
['State University of New York at New Paltz', 'http://www.newpaltz.edu', 'Address\n1 Hawk Drive New Paltz (population range: 2,500-9,999) 12561-2443 New York United States'],
['Union College', 'http://www.union.edu', 'Address\n807 Union Street Schenectady (population range: 50,000-249,999) 12308-2311 New York United States'],
['Skidmore College', 'http://www.skidmore.edu', 'Address\n815 N Broadway Saratoga Springs (population range: 10,000-49,999) 12866 New York United States'],
['The Juilliard School', 'http://www.juilliard.edu', 'Address\n60 Lincoln Center Plaza New York City (population range: over 5,000,000) 10023-6588 New York United States'],
['Adelphi University', 'http://www.adelphi.edu', 'Address\nSouth Avenue Garden City (population range: 10,000-49,999) 11530-0701 New York United States'],
['Barnard College', 'http://barnard.edu', 'Address\n3009 Broadway New York City (population range: over 5,000,000) 10027-6598 New York United States'],
['New York Institute of Technology', 'http://www.nyit.edu', 'Address\nNorthern Boulevard Old Westbury (population range: 2,500-9,999) 11568-8000 New York United States'],
['The Cooper Union for the Advancement of Science and Art', 'http://cooper.edu', 'Address\n7 East 7Th Street New York City (population range: over 5,000,000) 10003-7120 New York United States'],
['SUNY Geneseo', 'http://www.geneseo.edu', 'Address\n1 College Circle Geneseo (population range: 10,000-49,999) 14454-1465 New York United States'],
['SUNY College of Environmental Science and Forestry', 'http://www.esf.edu', 'Address\n1 Forestry Drive Syracuse (population range: 50,000-249,999) 13210 New York United States'],
['SUNY Upstate Medical University', 'http://www.upstate.edu', 'Address\n750 E Adams Street Syracuse (population range: 50,000-249,999) 13210 New York United States'],
['The Culinary Institute of America', 'http://www.ciachef.edu', 'Address\n1946 Campus Drive Hyde Park (population range: 10,000-49,999) 12538-1499 New York United States'],
['Touro College', 'http://www.touro.edu', 'Address\n500 7th Avenue New York City (population range: over 5,000,000) 10018 New York United States'],
['SUNY College at Oneonta', 'http://www.oneonta.edu', 'Address\nRavine Parkway Oneonta (population range: 10,000-49,999) 13820-4015 New York United States'],
['SUNY Empire State College', 'http://www.esc.edu', 'Address\n1 Union Avenue Saratoga Springs (population range: 10,000-49,999) 12866-4391 New York United States'],
['SUNY Cortland', 'http://www.cortland.edu', 'Address\nMiller Administration Building, Graham Avenue Cortland (population range: 10,000-49,999) 13045-0900 New York United States'],
['The State University of New York at Potsdam', 'http://www.potsdam.edu', 'Address\n44 Pierrepont Avenue Potsdam (population range: 10,000-49,999) 13676-2294 New York United States'],
['Le Moyne College', 'http://www.lemoyne.edu', 'Address\n1419 Salt Springs Road Syracuse (population range: 50,000-249,999) 13214-1399 New York United States'],
['St. Lawrence University', 'http://www.stlawu.edu', 'Address\n23 Romoda Drive Canton (population range: 2,500-9,999) 13617 New York United States'],
['SUNY Downstate Medical Center', 'http://www.downstate.edu', 'Address\n450 Clarkson Avenue Brooklyn (population range: 1,000,000-5,000,000) 11203-2098 New York United States'],
['The College at Brockport', 'http://www.brockport.edu', 'Address\n350 New Campus Drive Brockport (population range: 2,500-9,999) 14420-2919 New York United States'],
['SUNY Polytechnic Institute', 'http://sunypoly.edu', 'Address\n100 Seymour Road Utica (population range: 50,000-249,999) 13502 New York United States'],
['State University of New York College at Plattsburgh', 'http://www.plattsburgh.edu', 'Address\n101 Broad Street Plattsburgh (population range: 10,000-49,999) 12901-2681 New York United States'],
['Sarah Lawrence College', 'http://www.sarahlawrence.edu', 'Address\nOne Meadway Bronxville (population range: 2,500-9,999) 10708 New York United States'],
['Alfred University', 'http://www.alfred.edu', 'Address\nOne Saxon Drive Alfred (population range: 2,500-9,999) 14802-1205 New York United States'],
['Siena College', 'http://www.siena.edu', 'Address\n515 Loudon Road Loudonville (population range: 2,500-9,999) 12211-1462 New York United States'],
['Canisius College', 'http://www.canisius.edu', 'Address\n2001 Main Street Buffalo (population range: 250,000-499,999) 14208-1098 New York United States'],
['State University of New York at Fredonia', 'http://www.fredonia.edu', 'Address\n280 Central Avenue Fredonia (population range: 10,000-49,999) 14063-1136 New York United States'],
['Purchase College, State University of New York', 'http://www.purchase.edu', 'Address\n735 Anderson Hill Road Purchase (population range: 2,500-9,999) 10577-1400 New York United States'],
['Utica College', 'http://www.utica.edu', 'Address\n1600 Burrstone Road Utica (population range: 50,000-249,999) 13502-4892 New York United States'],
['St. Bonaventure University', 'http://www.sbu.edu', 'Address\n3261 W. State Road St. Bonaventure (population range: 2,500-9,999) 14778 New York United States'],
['Farmingdale State College', 'http://www.farmingdale.edu', 'Address\n2350 Broadhollow Road Farmingdale (population range: 2,500-9,999) 11735-1021 New York United States'],
['St. John Fisher College', 'http://www.sjfc.edu', 'Address\n3690 East Avenue Rochester (population range: 50,000-249,999) 14618-3597 New York United States'],
['Niagara University', 'http://www.niagara.edu', 'Address\n5795 Lewiston Road Niagara University (population range: 10,000-49,999) 14109 New York United States'],
['Manhattan College', 'http://manhattan.edu', 'Address\n4513 Manhattan College Parkway Riverdale (population range: 1,000,000-5,000,000) 10471-4098 New York United States'],
['The College of Saint Rose', 'http://www.strose.edu', 'Address\n432 Western Avenue Albany (population range: 50,000-249,999) 12203-1490 New York United States'],
['Albany Medical College', 'http://www.amc.edu', 'Address\n47 New Scotland Avenue Albany (population range: 50,000-249,999) 12208-3479 New York United States'],
['Brooklyn Law School', 'http://www.brooklaw.edu', 'Address\n250 Joralemon Street Brooklyn (population range: 1,000,000-5,000,000) 11201 New York United States'],
['Iona College', 'http://www.iona.edu', 'Address\n715 North Avenue New Rochelle (population range: 50,000-249,999) 10801-1890 New York United States'],
['New York Law School', 'http://www.nyls.edu', 'Address\n185 West Broadway New York City (population range: over 5,000,000) 10013-2960 New York United States'],
['Lehman College, CUNY', 'http://www.lehman.edu', 'Address\n250 Bedford Park Boulevard W The Bronx (population range: 1,000,000-5,000,000) 10468 New York United States'],
['The Sage Colleges', 'http://www.sage.edu', 'Address\n65 1st Street Troy (population range: 10,000-49,999) 12180 New York United States'],
["D'Youville College", 'http://www.dyc.edu', 'Address\n320 Porter Avenue Buffalo (population range: 250,000-499,999) 14201-1084 New York United States'],
['Mercy College', 'http://www.mercy.edu', 'Address\n555 Broadway Dobbs Ferry (population range: 10,000-49,999) 10522 New York United States'],
['Hartwick College', 'http://www.hartwick.edu', 'Address\nOne Hartwick Drive Oneonta (population range: 10,000-49,999) 13820-4020 New York United States'],
['Manhattanville College', 'http://www.mville.edu', 'Address\n2900 Purchase Street Purchase (population range: 2,500-9,999) 10577 New York United States'],
['Hunter College, CUNY', 'http://www.hunter.cuny.edu', 'Address\n695 Park Avenue New York City (population range: over 5,000,000) 10065 New York United States'],
['Berkeley College', 'http://berkeleycollege.edu', 'Address\n3 East 43 Street New York City (population range: over 5,000,000) 10017 New York United States'],
['Nazareth College', 'http://www.naz.edu', 'Address\n4245 East Avenue Rochester (population range: 50,000-249,999) 14618-3790 New York United States'],
['United States Merchant Marine Academy', 'http://www.usmma.edu', 'Address\n300 Steamboat Road Kings Point (population range: 2,500-9,999) 11024-1699 New York United States'],
['New York Medical College', 'http://www.nymc.edu', 'Address\nAdministration Building Valhalla (population range: 2,500-9,999) 10595 New York United States'],
['Manhattan School of Music', 'http://www.msmnyc.edu', 'Address\n120 Claremont Avenue New York City (population range: over 5,000,000) 10027-4698 New York United States'],
['Alfred State College', 'http://www.alfredstate.edu', 'Address\n10 Upper College Drive Alfred (population range: 2,500-9,999) 14802 New York United States'],
['Daemen College', 'http://www.daemen.edu', 'Address\n4380 Main Street Amherst (population range: 50,000-249,999) 14226-3592 New York United States'],
['Morrisville State College', 'http://www.morrisville.edu', 'Address\n80 Eaton Street Morrisville (population range: under 2,500) 13408 New York United States'],
['Mount Saint Mary College', 'http://www.msmc.edu', 'Address\n330 Powell Avenue Newburgh (population range: 10,000-49,999) 12550 New York United States'],
['Dominican College', 'http://www.dc.edu', 'Address\n470 Western Highway Orangeburg (population range: 2,500-9,999) 10962-1210 New York United States'],
['Wagner College', 'http://wagner.edu', 'Address\nOne Campus Road Staten Island (population range: 500,000-1,000,000) 10301-4495 New York United States'],
['The College of New Rochelle', 'http://www.cnr.edu', 'Address\n29 Castle Place New Rochelle (population range: 50,000-249,999) 10805-2339 New York United States'],
['SUNY Canton', 'http://www.canton.edu', 'Address\n34 Cornell Drive Canton (population range: 2,500-9,999) 13617-1098 New York United States'],
['Elmira College', 'http://www.elmira.edu', 'Address\nOne Park Place Elmira (population range: 10,000-49,999) 14901 New York United States'],
['Molloy College', 'http://www.molloy.edu', 'Address\n1000 Hempstead Avenue Rockville Centre (population range: 10,000-49,999) 11571-5002 New York United States'],
['SUNY Delhi', 'http://www.delhi.edu', 'Address\n2 Main Street Delhi (population range: 2,500-9,999) 13753-1100 New York United States'],
['Roberts Wesleyan College', 'http://www.roberts.edu', 'Address\n2301 Westside Drive Rochester (population range: 50,000-249,999) 14624 New York United States'],
['SUNY Maritime College', 'http://www.sunymaritime.edu', 'Address\n6 Pennyfield Avenue Throggs Neck (population range: 1,000,000-5,000,000) 10465-4198 New York United States'],
['Bank Street College of Education', 'http://www.bankstreet.edu', 'Address\n610 W 112 Street New York City (population range: over 5,000,000) 10025 New York United States'],
['Houghton College', 'http://www.houghton.edu', 'Address\n1 Willard Avenue Houghton (population range: under 2,500) 14744 New York United States'],
['Concordia College-New York', 'http://www.concordia-ny.edu', 'Address\n171 White Plains Road Bronxville (population range: 2,500-9,999) 10708-1998 New York United States'],
['Monroe College', 'http://www.monroecollege.edu', 'Address\n2501 Jerome Avenue Bronx (population range: 1,000,000-5,000,000) 10468 New York United States'],
['Baruch College, CUNY', 'http://www.baruch.cuny.edu', 'Address\nOne Bernard Baruch Way New York City (population range: over 5,000,000) 10010 New York United States'],
['Brooklyn College', 'http://www.brooklyn.cuny.edu', 'Address\n2900 Bedford Avenue Brooklyn (population range: 1,000,000-5,000,000) 11210-2889 New York United States'],
['SUNY College at Old Westbury', 'http://www.oldwestbury.edu', 'Address\n223 Store Hill Road Old Westbury (population range: 2,500-9,999) 11568-0210 New York United States'],
['The Graduate Center, CUNY', 'http://www.gc.cuny.edu', 'Address\n365 Fifth Avenue New York City (population range: over 5,000,000) 10016-4309 New York United States'],
['Nyack College', 'http://www.nyack.edu', 'Address\n1 South Boulevard Nyack (population range: 2,500-9,999) 10960-3698 New York United States'],
['SUNY Cobleskill', 'http://www.cobleskill.edu', 'Address\nState Route 7 Cobleskill (population range: 2,500-9,999) 12043 New York United States'],
['Wells College', 'http://www.wells.edu', 'Address\n170 Main Street Aurora (population range: under 2,500) 13026-0500 New York United States'],
["Paul Smith's College", 'http://www.paulsmiths.edu', 'Address\n7777 State Route 30 Paul Smiths (population range: under 2,500) 12970-0265 New York United States'],
['Medaille College', 'http://www.medaille.edu', 'Address\n18 Agassiz Circle Buffalo (population range: 250,000-499,999) 14214-2695 New York United States'],
['St. Francis College', 'http://www.sfc.edu', 'Address\n180 Remsen Street Brooklyn Heights (population range: 1,000,000-5,000,000) 11201-9902 New York United States'],
['Keuka College', 'http://www.keuka.edu', 'Address\n141 Central Avenue Keuka Park (population range: under 2,500) 14478 New York United States'],
['Bryant and Stratton College', 'http://www.bryantstratton.edu', 'Address\n465 Main Street Buffalo (population range: 250,000-499,999) 14203 New York United States'],
['LIM College', 'http://www.limcollege.edu', 'Address\n12 E 53Rd Street New York City (population range: over 5,000,000) 10022-5268 New York United States'],
["St. Joseph's College", 'http://www.sjcny.edu', 'Address\n245 Clinton Avenue Brooklyn (population range: 1,000,000-5,000,000) 11772-2399 New York United States'],
['Marymount Manhattan College', 'http://www.mmm.edu', 'Address\n221 E 71st Street New York City (population range: over 5,000,000) 10021-4597 New York United States'],
['Cazenovia College', 'http://www.cazenovia.edu', 'Address\n22 Sullivan Street Cazenovia (population range: 2,500-9,999) 13035 New York United States'],
['Albany Law School', 'http://www.albanylaw.edu', 'Address\n80 New Scotland Avenue Albany (population range: 50,000-249,999) 12208 New York United States'],
['College of Mount Saint Vincent', 'http://mountsaintvincent.edu', 'Address\n6301 Riverdale Avenue The Bronx (population range: 1,000,000-5,000,000) 10471-1093 New York United States'],
['Albany College of Pharmacy and Health Sciences', 'http://www.acphs.edu', 'Address\n106 New Scotland Avenue Albany (population range: 50,000-249,999) 12208-3492 New York United States'],
['The City College of New York', 'http://www.ccny.cuny.edu', 'Address\n160 Convent Avenue New York City (population range: over 5,000,000) 10031-9101 New York United States'],
['SUNY College of Optometry', 'http://www.sunyopt.edu', 'Address\n33 West 42Nd Street New York City (population range: over 5,000,000) 10036-8003 New York United States'],
['St. Thomas Aquinas College', 'http://www.stac.edu', 'Address\n125 Route 340 Sparkill (population range: 10,000-49,999) 10976-1050 New York United States'],
['John Jay College of Criminal Justice', 'http://www.jjay.cuny.edu', 'Address\n524 W 59th Street New York City (population range: over 5,000,000) 10019 New York United States'],
['Hilbert College', 'http://www.hilbert.edu', 'Address\n5200 S Park Avenue Hamburg (population range: 50,000-249,999) 14075-1597 New York United States'],
['Vaughn College of Aeronautics and Technology', 'http://www.vaughn.edu', 'Address\n86-01 23Rd Avenue Flushing (population range: 1,000,000-5,000,000) 11369 New York United States'],
['Queens College, City University of New York', 'http://www.qc.cuny.edu', 'Address\n65-30 Kissena Boulevard Flushing (population range: 1,000,000-5,000,000) 11367-0904 New York United States'],
['Metropolitan College of New York', 'http://www.mcny.edu', 'Address\n431 Canal Street New York City (population range: over 5,000,000) 10013-1919 New York United States'],
['York College, City University of New York', 'http://www.york.cuny.edu', 'Address\n94-20 Guy R. Brewer Boulevard Jamaica (population range: 1,000,000-5,000,000) 11451 New York United States'],
["The King's College", 'http://www.tkc.edu', 'Address\n56 Broadway New York City (population range: over 5,000,000) 10004 New York United States'],
['New York School of Interior Design', 'http://www.nysid.edu', 'Address\n170 East 70Th Street New York City (population range: over 5,000,000) 10021 New York United States'],
['New York College of Podiatric Medicine', 'http://www.nycpm.edu', 'Address\n53 E 124 Street New York City (population range: over 5,000,000) 10035-1940 New York United States'],
['Villa Maria College', 'http://www.villa.edu', 'Address\n240 Pine Ridge Road Buffalo (population range: 50,000-249,999) 14225-3999 New York United States'],
['Trocaire College', 'http://trocaire.edu', 'Address\n360 Choate Avenue Buffalo (population range: 250,000-499,999) 14220-2094 New York United States'],
['Relay Graduate School of Education', 'http://relay.edu', 'Address\n40 W 20th Street New York City (population range: over 5,000,000) 10011 New York United States'],
['New York Academy of Art', 'http://nyaa.edu', 'Address\n111 Franklin Street New York City (population range: over 5,000,000) 10013-2911 New York United States'],
['Webb Institute', 'http://www.webb.edu', 'Address\n298 Crescent Beach Road Glen Cove (population range: 10,000-49,999) 11542-1398 New York United States'],
['Davis College', 'http://www.davisny.edu', 'Address\n400 Riverside Drive Johnson City (population range: 10,000-49,999) 13790-2712 New York United States'],
['Maria College', 'http://mariacollege.edu', 'Address\n700 New Scotland Avenue Albany (population range: 50,000-249,999) 12208 New York United States'],
['New York City College of Technology, CUNY', 'http://www.citytech.cuny.edu', 'Address\n300 Jay Street Brooklyn (population range: 1,000,000-5,000,000) 11201-2983 New York United States'],
['The College of Westchester', 'http://www.cw.edu', 'Address\n325 Central Avenue White Plains (population range: 50,000-249,999) 10606-1200 New York United States'],
['Five Towns College', 'http://www.ftc.edu', 'Address\n305 N Service Road Dix Hills (population range: 10,000-49,999) 11746-5871 New York United States'],
['Boricua College', 'http://www.boricuacollege.edu', 'Address\n3755 Broadway New York City (population range: over 5,000,000) 10032-1560 New York United States'],
['College of Staten Island', 'http://www.csi.cuny.edu', 'Address\n2800 Victory Boulevard Staten Island (population range: 500,000-1,000,000) 10314 New York United States'],
['Briarcliffe College', 'http://www.briarcliffe.edu', 'Address\n1055 Stewart Avenue Bethpage (population range: 10,000-49,999) 11714-3545 New York United States'],
['Jamestown Business College', 'http://www.jbc.edu', 'Address\n7 Fairmount Avenue Jamestown (population range: 10,000-49,999) 14701-4756 New York United States'],
['Plaza College', 'http://www.plazacollege.edu', 'Address\n118-33 Queens Boulevard, Forest Hills New York City (population range: over 5,000,000) 11375 New York United States'],
['Medgar Evers College', 'http://www.mec.cuny.edu', 'Address\n1650 Bedford Avenue Brooklyn (population range: 1,000,000-5,000,000) 11225-2010 New York United States'],
['Helene Fuld College of Nursing', 'http://www.helenefuld.edu', 'Address\n24 East 120th Street New York City (population range: over 5,000,000) 10035-2737 New York United States'],
['CUNY School of Law', 'http://www.law.cuny.edu', 'Address\n2 Court Square Long Island City (population range: 1,000,000-5,000,000) 11101 New York United States']
]


fin = []


'''
street=<housenumber> <streetname>
city=<city>
county=<county>
state=<state>
country=<country>
postalcode=<postalcode

location = geolocator.geocode({'street': '123 Main Street', 'city': 'Los Angeles', 'state': 'CA', 'postalcode': 90034, 'country': 'USA'})

better
location = geolocator.geocode('1 Lomb Memorial Drive Rochester', {'state': 'New York', 'postalcode': '14623-5603', 'country': 'United States'})
'''


# Form the address
for each_item in all_list:

    print('\n\n Starting:', each_item[0])


    workin = []

    addr = each_item[2]
    addr = addr.split('\n')[1]

    # Grab zip code
    zip = addr.split('New York United States')[0]
    zip = zip.split(') ')[1].strip()

    # Use only 5 digit zip cuz hyphen might be recognized as subtraction. Or make zip a string.
    zip = zip[:5]

    # Form the address
    addr = addr.split('(pop')[0].strip()
    orig_addr = addr + ', ' + zip
    print('addr:', addr)



    # Feed addr into geopy to get coords
    location = geolocator.geocode(addr,  {'state': 'New York', 'postalcode': zip, 'country': 'United States'})

    '''
    ## Use only zip if coords cannot be found?
    if str(type(location)) == "<class 'NoneType'>":



        addr = zip + ', New York, USA'

        print('Changed to:', addr)
    '''

    ## must continue in for loop after break
    # Remove first word of addr if coords cannot be found
    while str(type(location)) == "<class 'NoneType'>":

        # Break before nothing is left
        if addr.count(' ') < 1:
            break
        print('empty')
        addr = ' '.join(addr.split(' ')[1:])
        location = geolocator.geocode(addr,  {'state': 'New York', 'postalcode': zip, 'country': 'United States'})


    # If zip codes disagree, remove street address and city. only use zip
    if not zip in str(location):
        print('Zips disagree. Trying only zip. \nOrig:', zip, '\nloc:', location)
        location = geolocator.geocode({'state': 'New York', 'postalcode': zip, 'country': 'United States'})

    ## implement while loop to add more words to city
    # If geopy returns 'None' use the last word of address as city
    if str(type(location)) == "<class 'NoneType'>":
        print('NoneType returned. Trying one word city...')
        addr = addr.split(' ')[-1]
        location = geolocator.geocode({'city': addr, 'state': 'New York', 'postalcode': zip, 'country': 'United States'})



    # Detect errors and continue
    if str(type(location)) == "<class 'NoneType'>":
        print('I give up.')
        location = '_ERROR._'
        workin.append(each_item[0])
        workin.append(each_item[1])
        workin.append(orig_addr)
        workin.append(location)
        continue

    # Add successful entry
    else:
        coords = location.latitude, location.longitude

        print('Success. geopy:', location, coords, '\n')

        workin.append(each_item[0])
        workin.append(each_item[1])
        workin.append(orig_addr)
        workin.append(location.address)
        workin.append(coords)

        fin.append(workin)

        #for i in sorted(fin):
            #print(i, '\n')

print('~~~  END  ~~')
for i in sorted(fin):
    print(i, '\n')


print('Total:', len(fin))



## Use this to check results for all five fields
##  \n\n\[(('|").*?('|"), ){4}\(.*?\)\]














