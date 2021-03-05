
# Desc: try new requests-html package for dynamic scraping







from requests_html import HTMLSession
session = HTMLSession()

url = 'https://www.applitrack.com/penfield/onlineapp/default.aspx?all=1'

resp = session.get(url)

resp.html.text

resp.html.find('body')[0].text # actually longer wtf


# Load dynamic content
resp.html.render() # will replace var named resp











'''
from requests_html import AsyncHTMLSession
asession = AsyncHTMLSession()
async def get_pythonorg():
    r = await asession.get('https://python.org/')
    return r

async def get_reddit():
    r = await asession.get('https://reddit.com/')
    return r

async def get_google():
    r = await asession.get('https://google.com/')
    return r

results = asession.run(get_pythonorg, get_reddit, get_google)
results # check the requests all returned a 200 (success) code
[<Response [200]>, <Response [200]>, <Response [200]>]

# Each item in the results list is a response object and can be interacted with as such
for result in results:
    print(result.html.url)
'''



























