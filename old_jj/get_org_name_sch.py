
# Description: Get org name and home url from raw html

# Using:
# http://www.newyorkschools.com/public-schools/

# Other source, multiple pages:
# https://data.nysed.gov/lists.php?start=65&type=district
# https://data.nysed.gov/lists.php?start=90&type=district





import urllib.parse, urllib.request
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup

the_db = []
domain = 'http://www.newyorkschools.com'
user_agent_str = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'





# Open raw html file
f = open('raw_html_sch.txt', mode='rb')


soup = BeautifulSoup(f, 'html5lib')


# Remove extra elements
r = soup.find_all('', {"class" : 'width-header-50'})
for i in r:
    print('dec:', i)
    i.decompose()
print('\n\n\n')


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

        # Get anchor elements
        for each_anchor in bs_html.find_all('a'):

            # Find home_url
            if 'Visit District Website' in each_anchor.text:
                home_url = each_anchor.get('href')
                print('Home URL:', home_url)
                break

        # Catch no url error
        else:
            print('ERROR. Couldnt find url at:', org_name, nysch_url)
            home_url = '_ERROR._url_not_found'

    # Catch all errors and continue
    except:
        home_url = '_ERROR._url_not_found'





    # Create work_list based of org name and home url
    work_list = []

    work_list.append(org_name)
    work_list.append(home_url)

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
        print(i)


print('\n\n\n\n')
for i in the_db:
    print(i)

print('\n\n\nTotal:', len(the_db))
















