
# Description: Get org name and home url from raw html



# https://www.4icu.org/us/





import urllib.parse, urllib.request
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup

the_db = []
domain = 'https://www.4icu.org'
user_agent_str = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'





# Open raw html file
f = open('raw_html_uni.txt', mode='rb')


soup = BeautifulSoup(f, 'html5lib')



# Get all anchor elements
for i in soup.find_all('a'):

    # Get org name
    org_name = i.text

    # Continue with errors
    try:
        nysch_url = domain + i.get('href')
        print('\nGoing to:', nysch_url)




        # Go to nysch url
        cj = CookieJar()
        req = urllib.request.Request(nysch_url, headers={'User-Agent': user_agent_str})
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        html = opener.open(req, timeout=10)


        bs_html = BeautifulSoup(html, 'html5lib')




        # Get tr elements
        for each_tr in bs_html.find_all('tr'):


            ## This may be too strict
            # Find the 'tr' element called 'Name' which will contain the url we want
            if each_tr.text.strip() == 'Name\n' + org_name:


                # Find home_url based on first url
                home_url = each_tr.find('a').get('href')
                print('Home URL:', home_url)
                break

        # Catch no url error
        else:
            print('ERROR. Couldnt find url at:', org_name, nysch_url)
            home_url = '_ERROR._url_not_found'


        # Get tr elements
        for each_tr in bs_html.find_all('tr'):

            # Find the 'tr' element called 'Name' which will contain the street address
            if 'Address' in each_tr.text.strip():
                addr = each_tr.text.strip()
                print('~~~ loc:', addr)
                break

        else:
            print('ERROR. Couldnt find loc at:', org_name, nysch_url)



    # Catch all errors and continue
    except Exception as errex:
        print(errex)
        home_url = '_ERROR._url_not_found'



    # Omit non NY unis
    if not 'New York United States' in addr:
        print('Omitting:', org_name)
        continue



    # Create work_list based of org name and home url
    work_list = []

    work_list.append(org_name)
    work_list.append(home_url)
    work_list.append(addr)


    # Mark dups as such
    for each_item in the_db:
        if home_url == each_item[1]:

            # Dont add 'DUP' if its a placeholder for an error
            if not home_url == '_ERROR._url_not_found':
                work_list[1] = '_DUP._' + work_list[1]
                break

    # Append work_list to the_db if not a dup
    the_db.append(work_list)


    ## Can delete this
    for i in the_db:
        print(i, '\n')


print('\n\n\n\n')
for i in the_db:
    print(i)

print('\n\n\nTotal:', len(the_db))
















