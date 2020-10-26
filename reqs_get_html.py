# Desc: Get static HTML using Requests lib


import requests



workingurl = 'http://joesjorbs.com'


user_agent_str = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'


try:
    resp = requests.get(workingurl, timeout=15, headers={'User-Agent': user_agent_str}, verify=False)

    print(resp.text)
    print(resp.url)
    print('\nheaders =', resp.headers)
    print('\nstat code =', resp.status_code)
except Exception as errex:
    print(errex)




'''
>>> jar = requests.cookies.RequestsCookieJar()
>>> jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies')
>>> jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere')
>>> url = 'https://httpbin.org/cookies'
>>> r = requests.get(url, cookies=jar)
>>> r.text
'''




















