
# Desc: Download most recent Jeopardy episode


# To do:
# Deluge port forwarding - port needs to be added to router settings
# fix uploaders list
# download older episodes that were missed. remove final else statement
# deluge doesn't restore tors from prev session
# %U ?
# actually check if deluge is running +





import os, ssl, urllib.request, re, glob, subprocess, time
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup




# Compile regex pattern with positive lookbehind for "Jeopardy" and then the date
date_regex = re.compile("(?<=Jeopardy\.)[0-9]{4}\.[0-9]{2}\.[0-9]{2}")

# List of approved uploaders
uploader_l = ['/user/cptnkirk/', '/user/mwoz/', 'https://pirateproxy.live/user/cptnkirk/', 'https://pirateproxy.live/user/mwoz/']
tor_l = [] # List of torrents to download

user_agent_str = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'




# Get most recent episode on disk
file_date_l = glob.glob('/home/joepers/Videos/tors/*')
file_date_l = sorted(file_date_l, reverse=True)
file_date_l2 = []


# Select only Jeopardy episodes
for i in file_date_l:
    name = i.split('/')[-1]

    if name.startswith('Jeopardy.'):
        file_date_l2.append(i)

# Select the date from the episode name
file_date = file_date_l2[0].split('/')[-1]
file_date = '.'.join(file_date.split('.')[1:4])





# Check VPN connection status
vpn_status = os.popen('piactl get connectionstate').read().strip()

if vpn_status != 'Connected':

    # silence output?
    # VPN client is running but disconnected
    if os.popen('pgrep pia-client').read():
        print('Connecting VPN ...')
        os.popen('piactl connect')

    # Run VPN client
    else:
        print('\nStarting VPN ...')
        os.popen('/opt/piavpn/bin/pia-client > /dev/null 2>&1 &')

    # Wait for VPN to connect
    for i in range(15):
        print('Please wait ...')
        time.sleep(1)

        # Break after successful connection
        if os.popen('piactl get connectionstate').read().strip() == 'Connected':
            print('\nVPN has been started')
            break

    # Exit on VPN connection timeout
    else:
        print('VPN failed to connect. Exiting ...')
        raise SystemExit

# VPN was already on
else:
    print('VPN is on')



# Define HTML request function
def html_requester_f(workingurl):

    ## Ignore SSL certificate errros
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context


    # Request html using a spoofed user agent, cookiejar, and timeout
    try:
        cj = CookieJar()
        req = urllib.request.Request(workingurl, headers={'User-Agent': user_agent_str}, unverifiable=False)
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        html = opener.open(req, timeout=10)
        
        return html # Success

    # Catch HTTP request errors
    except Exception as errex:
        print(errex)
        raise SystemExit



# Request HTML
#https://piratemirror.live/search/jeopardy/0/3/0
html = html_requester_f('https://pirateproxy.live/search/jeopardy/1/3/0')
soup = BeautifulSoup(html, 'html5lib')

# Select td elements
tds = soup.find_all('td')

# Loop through each td tag
for i in tds:

    # Skip td tag if it doesn't contain a div tag with class of detName
    det = i.find(class_='detName')

    if not det:
        #print('\ndetName not found. Skipping:', i)
        continue


    # Select torrent name
    tor_name = i.find('a').text

    if not 'Jeopardy' in tor_name:
        print('Tor name error. Skipping:', tor_name)
        continue


    # Select magnet URL
    all_anchors = i.find_all('a')
    for each_anchor in all_anchors:
        mag_link = each_anchor.get('href')
        if mag_link.startswith('magnet:?xt='):
            break

    # Skip td tag if URL can not be found
    else:
        print('\nMagnet URL not found. Skipping:', tor_name)
        continue



    # Select name of uploader
    uploader = all_anchors[-1].get('href')

    # Skip td tag if approved uploader can not be found
    if not uploader in uploader_l:
        print('\nUnapproved uploader:', uploader, '\nSkipping:', tor_name)
        continue



    # Select date from name using regex
    tor_date = re.search(date_regex, tor_name)
    
    if tor_date:
        tor_date = tor_date.group(0) # Select entire resulting match

    # Skip if date match not found
    else:
        print('\nDate not found. Skipping:', tor_name)
        continue
    

    # Append relevant info to tor list
    tor_l.append([tor_name, tor_date, mag_link])
    #print('\n\n\n', tor_name, '\n', tor_date, '\n', uploader, '\n', mag_link)



print('\n\nMost recent episode on disk:', file_date)


# Sort by tor name
tor_l.sort(reverse=True)


# Loop thorough all episode canidates
for idx, item in enumerate(tor_l):

    tor_name = item[0]
    tor_date = item[1]
    mag_link = item[2]

    print('\n\nChecking online episode:\n', tor_date)

    # Compare online date to file date
    if tor_date > file_date:
        print('Adding to Deluge:', tor_name)

        # Check if Deluge is running only on first iteration
        if idx == 0:

            # Check if Deluge is already running
            try:
                del_check = subprocess.check_output(['pidof', 'deluge-gtk'])
                print('\nDeluge is already runnning')

            # Start Deluge
            except:
                print('\nStarting Deluge ...')
                p = subprocess.Popen('deluge-gtk', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

                # Wait for Deluge to start
                while True:
                    time.sleep(2)

                    try:
                        del_check = subprocess.check_output(['pidof', 'deluge-gtk'])
                        print('\nDeluge is running')
                        break
                    except:
                        print('Please wait ...')



        # Add torrent to Deluge and silence all output
        p = subprocess.Popen(['deluge-gtk', mag_link], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)



    # Exit when online episode is older or equal to disk episode
    else:
        print('\nEpisode on disk is most recent. Exiting ...\n\n')
        break

    




















