

import datetime, docker, requests, psutil, json, gzip, os, queue, re, socket, time, traceback, urllib.parse, urllib.request, webbrowser, ssl
from os.path import expanduser
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup




workingurl = 'https://www.nowinstock.net/videogaming/consoles/sonyps5/'



'''

# Must run Docker daemon with: systemctl start docker
# Must run Docker with sudo and without VPN
# Start Docker container
print(os.getpid(), 'Starting Splash Docker container...')
client = docker.from_env()
client.containers.run("scrapinghub/splash", name='jj_con', ports={'8050/tcp': 8050}, command='--disable-private-mode --disable-browser-caches --slots 100', detach=True, remove =True)
#client.containers.run("scrapinghub/splash", name='jj_con', ports={'8050/tcp': 8050}, detach=True, remove=True)

# Wait for Splash to be ready
while True:
    try:
        resp = requests.post('http://localhost:8050/_gc')
        print(os.getpid(), 'Splash is running')
        break

    except Exception as eee:
        if 'Connection reset by peer' in str(eee):
            print(os.getpid(), '...')
            time.sleep(1)
            continue


# Get container name
container = client.containers.get('jj_con')
'''



# Define HTML request function
# Make request on port 8050 so Splash handles it
## "connection reset by peer" and "broken pipe" errors fixed by lowering json wait
resp = requests.post('http://localhost:8050/render.json', json={
    'url': workingurl,
    'headers': {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}, 
    'plugins_enabled': 'true', # May help with rendering
    'indexeddb_enabled': 'true', # May help with rendering
    'wait': 0.01, # Wait for dyanamic content to render.
    'render_all': 1, # Render the entire page
    'html': 1, # Static HTML
    'iframes': 1, # Dynamic content. JSON element is called 'childFrames'
    'images': 0, # Disable images for speed
    'geometry': 0, # Exclude unnecessary items
    'timeout': 20
})

# Get status code
stat_code = resp.status_code

# Catch errors
if stat_code != 200:
    print('stat_code=', stat_code, workingurl)

    # Get relevant error info
    ## stat_info for timeout errors will be a dict, not a string. Also it will not have ['info']['text']
    try:
        stat_info = json.loads(resp.text)['info']['text']
    except:
        stat_info = str(json.loads(resp.text)['info'])
    print('status=', stat_info, workingurl)

    # Get redirected URL
    ## Must use ['info']['url'] when non 200 status to get redirected url
    try:
        red_url = json.loads(resp.text)['info']['url']
        print('red=', red_url) 
    except:
        red_url = workingurl





# Get HTML and dynamic content
html_text = json.loads(resp.text)['html']
dy_text = json.loads(resp.text)['childFrames']

# Red url
red_url = json.loads(resp.text)['url']

# Combine HTML and dynamic content
rendered_html = html_text + str(dy_text)
#print(rendered_html)


# Select body
soup = BeautifulSoup(rendered_html, 'html5lib')
soup = soup.find('body')



# Keep a soup for finding links and another for saving visible text
vis_soup = soup



# Compile regex paterns for reducing whitespace in written files
white_reg = re.compile("\s{2,}")

# Compile regex paterns for finding hidden HTML elements
style_reg = re.compile("(display\s*:\s*(none|block);?|visibility\s*:\s*hidden;?)")
class_reg = re.compile('(hidden-sections?|dropdown|has-dropdown|sw-channel-dropdown|dropdown-toggle)')



# Remove script, style, and empty elements
for i in vis_soup(["script", "style"]):
    i.decompose()

## unn
# Iterate through and remove all of the hidden style attributes
r = vis_soup.find_all('', {"style" : style_reg})
for x in r:
    #print(os.getpid(), 'Decomposed:', workingurl, x)
    x.decompose()

# Type="hidden" attribute
r = vis_soup.find_all('', {"type" : 'hidden'})
for x in r:
    #print(os.getpid(), 'Decomposed:', workingurl, x)
    x.decompose()

# Hidden section(s) and dropdown classes
for x in vis_soup(class_=class_reg):
    #print(os.getpid(), 'Decomposed:', workingurl, x)
    x.decompose()


## This preserves whitespace across lines. Prevents: 'fire departmentapparatuscode compliance'
# Remove unnecessary whitespace. eg: multiple newlines, spaces, and tabs
vis_soup = str(vis_soup.text)
vis_soup = re.sub(white_reg, " ", vis_soup)





for i in soup.find_all('div'):
    try:
        if len(i.text.lower()) > 999: continue
        if 'add to cart' in i.text.lower():
            i.click()
    except: pass







#print(html_text, '\n~~~~~~ end of plain html\n\n\n\n\n\n')

#print(vis_soup)
#print('\n\n~~~~~~', rendered_html)


#container.stop()







