# Description: Get physical address from URL


import datetime, os, queue, re, socket, time, urllib.parse, urllib.request, webbrowser
from multiprocessing import active_children, Lock, Manager, Process, Queue, Value
from urllib.error import URLError
import geopy.distance
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

dd = {}

# Get html
workingurl_l = ['http://academyofthecity.org', 'http://albanycommunitycs.org', 'http://aldenschools.org', 'http://bemusptcsd.org', 'http://bphs.democracyprep.org', 'http://brillacollegeprep.org', 'http://brillacollegeprep.org/our-schools', 'http://brooklyncompass.org', 'http://brooklyneastcollegiate.uncommonschools.org/brooklyn-east/our-school', 'http://brownsvillecollegiate.uncommonschools.org', 'http://campacharter.org', 'http://cazenoviacsd.com', 'http://classicalcharterschools.org/about/schools/south-bronx-classical-charter-school-iii', 'http://classicalcharterschools.org/about/schools/south-bronx-classical-charter-school-iv', 'http://comsewogue.k12.ny.us', 'http://croton-harmonschools.org', 'http://cvweb.wnyric.org', 'http://democracyprep.org', 'http://district.uniondaleschools.org', 'http://dpems.democracyprep.org', 'http://ecsli.org', 'http://elmcharterschool.org', 'http://enterprisecharter.org', 'http://eufsd.org/site/default.aspx?pageid=1', 'http://excellenceboys.uncommonschools.org', 'http://excellencegirls.uncommonschools.org', 'http://gilboa-conesville.k12.ny.us', 'http://gufsd.org', 'http://hammondcsd.schoolwires.net/site/default.aspx', 'http://healthsciencescharterschool.org', 'http://hpes.democracyprep.org', 'http://imaginemeleadership.org', 'http://inletcommonschool.wordpress.com', 'http://integrationcharterschools.org/lois-and-richard-nicotra-early-college-charter-school', 'http://integrationcharterschools.org/richmond-preparatory-charter-school', 'http://ivyhillprep.org', 'http://jerichoschools.org', 'http://kingscollegiate.uncommonschools.org', 'http://lcsd.k12.ny.us/lcsd/site/default.asp', 'http://leadershipprepbedstuy.uncommonschools.org/lpbs/our-school/elementary-academy']

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'
err_urls = {}

addr_words = ['contact', 'about']


lock = Lock()


# HTML request
def get_html(workingurl):
    print('\n\nworkingurl =', workingurl)
     
    try:
        request = urllib.request.Request(workingurl, headers={'User-Agent': user_agent})
        html = urllib.request.urlopen(request, timeout=10)

    except:
        print('error at', workingurl)
        
            
    # Decode html
    charset_encoding = html.info().get_content_charset()
    try:
        if charset_encoding == None:
            dec_html = html.read().decode()
            
        else:
            dec_html = html.read().decode(charset_encoding)

    # Attempt latin-1 charset encoding
    except Exception as errex:
        try:
            dec_html = html.read().decode('latin-1')                        
        except Exception as errex:
            print('error 2:', charset_encoding, 'decode at', workingurl)
            

    return(dec_html)




try:
    for workingurl in workingurl_l:
        
        dec_html = get_html(workingurl)
                
        # Catch no html
        if dec_html == '':
            print('No HTML at:', workingurl)
            err_urls[workingurl] = 'No HTML'

        # Create strict regex with zip code
        reg = "(?:\w+\s+){0,4}\w+,?\s+(?:ny|new\s+york)\s+\d{5}"
        
        # Find all addresses and use the first
        try:
            addr = re.findall(reg, dec_html, flags=re.DOTALL)[0]
        except:
            addr = re.findall(reg, dec_html, flags=re.DOTALL)
            
        # Crawl if address not found
        if addr == '':
            
            # Get all tags
            tag_regex = 'href=.*?</a>'
            tags = re.findall(tag_regex, dec_html, flags=re.DOTALL)
            
            if len(tags) < 1:
                err_urls[workingurl] = 'No addr_words'
            
            # Discard tag if it doesnt't contain an address word
            tag_switch = False
            for tag in tags:
                if not any(xxx in tag for xxx in addr_words):
                    print('No addr_words at:', tag)
                    continue
                    
            # Catch a URL with no contact or about page
            if tag_switch == False:
                print('No good tags found at:', workingurl)
                err_urls[workingurl] = 'No good tags'
                continue
        
            # Determine if double or single quote comes first in tag
            dqloc = tag.find('"')
            sqloc = tag.find("'")

            if dqloc == sqloc:
                #if verbose_arg: print(os.getpid(), dqloc, 'Malformed quotes at', tag[:99])
                continue
            elif dqloc < sqloc:
                if dqloc > -1:
                    quovar = '"'
                else: quovar = "'"
            elif dqloc > sqloc:
                if sqloc > -1:
                    quovar = "'"
                else: quovar = '"'
            #if verbose_arg: print(os.getpid(), 'quovar =', quovar) 

            # Use the quote as the tag delimiter to form the url
            urlline = tag.split(quovar)[1]
            
            # Create domain
            domain = []
            domain = workingurl.split('/', 3)[:3]
            domain = '/'.join(domain)
            domain = domain.strip()

            # Convert any rel paths to abs
            abspath = urllib.parse.urljoin(domain, urlline)

            get_html(abspath)
            
            print('dec_html =', dec_html[222])
            
            # Catch no html
            if dec_html == '':
                print('No HTML at:', abspath)
                err_urls[abspath] = 'No HTML'

            
            # Create strict regex with zip code
            reg = "(?:\w+\s+){0,4}\w+,?\s+(?:ny|new\s+york)\s+\d{5}"
            
            # Find all addresses and use the first
            try:
                addr = re.findall(reg, dec_html, flags=re.DOTALL)[0]
            except:
                addr = re.findall(reg, dec_html, flags=re.DOTALL)
                
                
                
                
                
                
                
                

        # Create regex without zip code and one word succeeding ny
        if not addr:
            print('try less')
            reg = "\w+,\s+(?:ny|new york)"
            addr = re.findall(reg, dec_html, flags=re.DOTALL)
            try:
                addr = addr[0]
            except:
                pass
        
        #print('addr =', addr)

        # Enter address into geolocator
        geolocator = Nominatim(user_agent="app_name")
        
        try:
            full_loc = geolocator.geocode(addr)

        # Create regex optional comma
        except:
            print('errrrrr')
            reg = "\w+\s+(?:ny|new york)"
            addr = re.findall(reg, dec_html, flags=re.DOTALL)
            addr = addr[0]
            
            try:
                full_loc = geolocator.geocode(addr)
                
            except:
                print('---------- idfk', addr)
                continue
            
        print('addr =', addr)
        
        # Only city?
        #location_3 = str(full_loc).split(',')[0]

        # Convert into coordinates
        try:
            coords = full_loc.latitude, full_loc.longitude
        except:
            print('failure at:', full_loc)
            continue
        
        # Add to dict
        dd[workingurl] = [coords, full_loc]

finally:
    print('\n\n')
    for i in dd.items():
        print(i + '\n')


















