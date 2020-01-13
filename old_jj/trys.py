# https://stackoverflow.com/questions/7947579/getting-all-visible-text-from-a-webpage-using-selenium

# Desc: Use Selenium to extract dynamically-loaded content and print only the visible text.
# Works!

import datetime
startTime = datetime.datetime.now()


import contextlib
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.options import Options
import lxml.html as LH
import lxml.html.clean as clean



url = "https://www.friendship.wnyric.org/domain/9"


options = Options()

# don't open gui browser
options.headless = True
#options.add_argument('--headless') ## this works too


firefox_profile = webdriver.FirefoxProfile()

# disable images
firefox_profile.set_preference('permissions.default.image', 2)

# disable flash
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

ignore_tags=('script','noscript','style')
with contextlib.closing(webdriver.Firefox(options=options, firefox_profile=firefox_profile)) as browser:
    browser.get(url) # Load page
    content=browser.page_source
        
    cleaner=clean.Cleaner()
    content=cleaner.clean_html(content)    

    doc=LH.fromstring(content)
    for elt in doc.iterdescendants():
        if elt.tag in ignore_tags: continue
        text=elt.text or ''
        tail=elt.tail or ''
        words=' '.join((text,tail)).strip()
        if words:
            print(words, '\n')
            
duration = datetime.datetime.now() - startTime
print('duration =', duration)



browser.quit()




































