#!/usr/bin/python3.7

# Description: Search the provided webpages for keyword and attempt relavent crawling.

# To do:
# Phase 1: basic function
# keyword search +
# crawl function +
# proper html parsing 
# spoof user agent
# 
# Phase 2: basic optimization
# prevent dups and checked pages
# blacklist
# error log
# Phase 3: advanced features
# parellelization
# user-defined levels of crawling
# Phase 4: distribution
# enable cross-platform
# Phase 5: GUI

import urllib.request, urllib.parse, urllib.error, os

keyword = 'librarian'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'



allcivurls = []
errorurls = {}
abspath = 'aaa'
#blacklist = open(r'''C:\Users\jschiffler\Desktop\Text_n_Stuff\current\port.txt''')

keywordurlset = set()
urllistprefilter = []
urllistgood = set()
alltags = set()

# Clear errorlog
f = open("errorlog.txt", "w")
f.write('')

# Get portal URLs from file
civfile = open(r'''C:\Users\jschiffler\Desktop\Text_n_Stuff\current\port.txt''')
for civline in civfile:
    allcivurls.append(civline)

for eachcivurl in allcivurls:
    alltags.clear()
    urllistgood.clear()
    urllistprefilter.clear()
    print('\n\n\n\n ====================== Start =====================\n', eachcivurl)
    domain = eachcivurl.rsplit('/', 1)[0]
    print('domain = ', domain)


    # Get html from url
    try:
        #html = urllib.request.urlopen(eachcivurl)
        ##html = response.read()
        
        request = urllib.request.Request(eachcivurl,headers={'User-Agent': user_agent})
        html = urllib.request.urlopen(request)
        
    except Exception as errex:
        print('error 1: url request at', eachcivurl)
        errorurls[eachcivurl] = 'error 1', errex
        continue

    # Decode if necessary
    charset_encoding = html.info().get_content_charset()
    print('Char encoding =', charset_encoding)

    if charset_encoding == None:
        try:
            #dechtml = html.read().decode(errors='ignore')
            dechtml = html.read().decode()
        except Exception as errex:
            print('error 2: decode at ', eachcivurl)
            errorurls[eachcivurl] = 'error 2', errex
            continue

    else:
        try:
            dechtml = html.read().decode(charset_encoding)
        except Exception as errex:
            print('error 2: decode at ', eachcivurl)
            errorurls[eachcivurl] = 'error 2', errex
            continue

    html1 = dechtml.lower()

    # Search for keyword on page
    keycheck = html1.find(keyword)

    # Add to the keywordurl set
    if keycheck != -1:
        print('\n~~~ Found keyword ~~~\n')
        keywordurlset.add(eachcivurl)
    else:
        print('\n~~~ Not today ~~~\n')


    # Seperate html into lines using <a delimiter
    htmllines = html1.split('<a ')
    #htmllines.sort

    # End lines using </a> delimiter and add to alltags set
    for eachhtmlline in htmllines:

        ## Remove?
        # Omit lengthy <!DOCTYPE tag
        if eachhtmlline.startswith('<!doctype'):
            print ('!DOCTYPE tag omitted\n')
            continue
        else:
            loc = eachhtmlline.find('</a>')
            result = eachhtmlline[:loc]
            #print(result)
            alltags.add(result)

    # Set jobwords and bunkwords
    jobwords = ['employment', 'job', 'opening', 'exam', 'test', 'postions', 'civil', 'career', 'human', 'personnel']
    bunkwords = ['javascript:', '.pdf', '.jpg', '.ico', '.doc', 'mailto:', 'tel:', 'description', 'specs', 'specification', 'guide', 'faq', 'images']

    # Determine if the tag contains a jobword
    for tag in alltags:
        if any(xxx in tag for xxx in jobwords):

            ## split by href first?
            # Determine if double or single quote comes first in tag
            dqloc = tag.find('"')
            sqloc = tag.find("'")
            print('\n', dqloc, sqloc)

            if dqloc < sqloc:
                if dqloc > -1:
                    quovar = '"'
                else: quovar = "'"
            elif dqloc > sqloc:
                if sqloc > -1:
                    quovar = "'"
                else: quovar = '"'
            else:
                print('error 3: tag quote at ', tag)
                errorurls[tag] = 'error 3: tag quote'

            # Append only the url to the list
            if tag.count('href=') > 0:
                try:
                    urlline0 = tag.split('href=')[1]
                    urlline = urlline0.split(quovar)[1]

                    # Convert any rel paths to abs
                    abspath = urllib.parse.urljoin(domain, urlline)
                    urllistprefilter.append(abspath)
                    print('tag = ', tag, '\nurlline0 = ', urlline0, '\nurlline = ', urlline,  '\nabsp = ', abspath)

                except Exception as errex:
                    print('error 4: url split at ', tag)
                    errorurls[tag] = 'error 4', errex

                # Exclude if the tag contains a bunkword
                try:
                    if not any(yyy in tag for yyy in bunkwords):
                        urllistgood.add(abspath)
                except Exception as errex:
                    print('error 5: at ', tag)
                    errorurls[tag] = 'error 5', errex

                # Exclude if the abspath is on the Blacklist
                #if not any(zzz in abspath for zzz in blacklist):
                        #urllistgood.add(abspath)

            ## error 6 should not be an error
            else:
                print('error 6: no "href=" at ', tag)
                errorurls[tag] = 'error 6: no href='




    print('urlg =', urllistgood)
    for workingurl in urllistgood:

        print('============= Begin crawl ==============', workingurl)

        # Get html from url
        try:
            workinghtml = urllib.request.urlopen(workingurl)
        except Exception as errex:
            print('error 7: url request at', workingurl, errex)
            errorurls[workingurl] = 'error 7', errex
            continue

        # Decode if necessasry
        charset_encoding = workinghtml.info().get_content_charset()
        if charset_encoding == None:
            try:
                decworkinghtml = html.read().decode(errors='ignore')
            except Exception as errex:
                print('error 8: decode at ', workingurl)
                errorurls[workingurl] = 'error 8', errex
                continue
        else:
            try:
                decworkinghtml = workinghtml.read().decode(charset_encoding)
            except Exception as errex:
                print('error 8: decode at ', workingurl)
                errorurls[workingurl] = 'error 8', errex
                continue

        decworkinghtml1 = decworkinghtml.lower()

        # Search for keyword on page
        keycheck = decworkinghtml1.find(keyword)

        # Add to the keywordurl set
        if keycheck != -1:
            print('\n~~~ Found keyword ~~~\n')
            keywordurlset.add(workingurl)
        else:
            print('\n~~~ Not today ~~~\n')






    print('\n\n~~~~~~~~~~~~ urllistprefilter length =', len(urllistprefilter), ' ~~~~~~~~~~~~\n', sorted(urllistprefilter))

    print('\n\n~~~~~~~~~~~~ urllistgood length =', len(urllistgood), ' ~~~~~~~~~~~~\n', sorted(urllistgood))



print('\n\n ################## ', len(keywordurlset), ' matches found at: \n', keywordurlset)




# Display and write errorlog
writeerrors = open("errorlog.txt", "a")
print('\n\n', len(errorurls), ' errors found at: \n',)
for k, v in errorurls.items():
    print(v, '::', k, '\n')
    vk = str((v, '::', k))
    writeerrors.write(vk + '\n')






















