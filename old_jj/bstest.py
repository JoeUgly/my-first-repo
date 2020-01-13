
# Desc: test how to eliminate hidden elements in HTML


from bs4 import BeautifulSoup
import datetime, os, queue, re, socket, time, urllib.parse, urllib.request
from http.cookiejar import CookieJar
user_agent_str = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'


# compare parsers



url = 'https://www.friendship.wnyric.org/domain/9'

# Request html using a spoofed user agent, cookiejar, and timeout
cj = CookieJar()
req = urllib.request.Request(url, headers={'User-Agent': user_agent_str})
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
html = opener.open(req, timeout=10)



soup = BeautifulSoup(html, features="html.parser")
soup = soup.find('body')

# class="element-invisible"
## check no semi colon

results = []


## case sensitivity, multiple or extended: "display:none; visibility: hidden;"
# Remove hidden elements from the html
style_reg = re.compile("(display\s*:\s*(none|block);?|visibility\s*:\s*hidden;?)")
class_reg = re.compile('(hidden-sections?|sw-channel-dropdown)')


# Iterate through and remove all of the hidden style attributes
r = soup.findAll('', {"style" : style_reg})
for x in r:
    results.append(str(x)+'===================================\n\n')
    x.decompose()

# Type="hidden" attribute
r = soup.findAll('', {"type" : 'hidden'})
for x in r:
    results.append(str(x)+'===================================\n\n')
    x.decompose()

# Hidden section(s) and dropdown classes
for i in soup(class_=class_reg):
    results.append(str(i)+'===================================\n\n')
    i.decompose()



for i in results:
    print(i)


print('remaining!!!!!!!!\n', soup)






























