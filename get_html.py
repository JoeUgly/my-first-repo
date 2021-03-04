

# Desc: Get HTML


import urllib.request, datetime
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup

#startTime = datetime.datetime.now()



url = 'https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG?ref_=ast_sto_dp'

domain = '/'.join(url.split('/')[:3])

user_agent_str = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'

cj = CookieJar()
req = urllib.request.Request(url, headers={'User-Agent': user_agent_str})
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
html = opener.open(req, timeout=10)
red_url = html.geturl()


h = html.read()

'''
print('redurl=', red_url)
print('html=', html)
print('\n\n\n\n\nh=', h)
'''

soup = BeautifulSoup(h, 'html5lib')

vis = soup.find('body').text
print(vis)

'''
## soup has decomposed elems
# Search for pagination class before checking crawl level
for i in soup.find_all(class_='pagination'):

    ## find or find_all?
    # Find anchor tags
    for xx in i.find_all('a'):
        print('ddfdf', xx)

        # Find "next" page url
        if xx.text.lower() == 'next':

            #Get absolute url
            abspath = urllib.parse.urljoin(domain, xx.get('href'))

            print('~~~', abspath)
'''

#print(datetime.datetime.now() - startTime)














