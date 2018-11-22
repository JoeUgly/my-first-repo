#!/usr/bin/python3.7

# Description: Search the provided webpages for keyword and attempt crawling.

# To do:
# Phase 1: basic function
# keyword search
# crawl function
# proper html fetching
# Phase 2: basic optimization
# prevent dups and checked pages
# blacklist
# Phase 3: advanced features
# parellelization
# user-defined levels of crawling
# Phase 4: GUI


import urllib.request, urllib.parse, urllib.error


allcivurls = []
errorurls = []
abspath = 'aaa'

keywordurlset = set()
urllistprefilter = []
urllistgood = set()
alltags = set()

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
        html = urllib.request.urlopen(eachcivurl)
    except:
        print('error 1: url request at', eachcivurl)
        errorurls.append(eachcivurl)
        continue

    # Decode if necessary
    charset_encoding = html.info().get_content_charset()
    print('Char encoding =', charset_encoding)

    #html = html.read().decode(errors='ignore')
    try:
        dechtml = html.read().decode(charset_encoding)
    except:
        print('error 2: decode at ', eachcivurl)
        errorurls.append(eachcivurl)
        continue

    html1 = dechtml.lower()

    # Search for keyword on page
    keycheck = html1.find('colonie')

    # Add to the keywordurl set
    if keycheck != -1:
        print('\n~~~ Found keyword ~~~\n')
        keywordurlset.add(eachcivurl)
    else:
        print('\n~~~ Not today ~~~\n')

    # Seperate html into lines using <a delimiter
    htmllines = html1.split('<a')
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
    bunkwords = ['javascript:', '.pdf', '.jpg', '.ico', '.doc', '^mailto:', '^tel:', 'description', 'specs', 'specification', 'guide', 'faq', 'images']

    # Determine if the tag contains a jobword
    for tag in alltags:
        if any(x in tag for x in jobwords):

            ## split by href first?
            # Determine if double or single quote comes first in tag
            dqloc = tag.find('"')
            sqloc = tag.find("'")
            print(dqloc, sqloc)

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

            # Append only the url to the list
            if tag.count('href=') > 0:
                try:
                    urlline0 = tag.split('href=')[1]
                    urlline = urlline0.split(quovar)[1]

                    # Convert any rel paths to abs
                    abspath = urllib.parse.urljoin(domain, urlline)
                    urllistprefilter.append(abspath)
                    print('tag = ', tag, 'urlline0 = ', urlline0, 'urlline = ', urlline,  'absp = ', abspath)


                except:
                    print('error 4: url split at ', tag)

            # Exclude if the tag contains a bunkword
                    try:
                        if not any(x in tag for x in bunkwords):
                            urllistgood.add(abspath)
                    except:
                        print('error 5: at ', tag)
            else:
                print('error 6: no "href=" at ', tag)




    print('============= Begin crawl ==============', abspath)

    print('urlg =', urllistgood)
    for workingurl in urllistgood:

        ## This causes many errors
        # Get html from url
        try:
            abspathhtml = urllib.request.urlopen(workingurl)
        except:
            print('error 1: url request at', abspath)
            errorurls.append(abspath)
            continue

        # Decode if necessasry
        charset_encoding = abspathhtml.info().get_content_charset()

        #html = html.read().decode(errors='ignore')
        try:
            decabspathhtml = abspathhtml.read().decode(charset_encoding)
        except:
            print('error 2: decode at ', abspath)
            errorurls.append(abspath)
            continue

        abspathhtml1 = decabspathhtml.lower()

        # Search for keyword on page
        keycheck = abspathhtml1.find('correction officer')

        # Add to the keywordurl set
        if keycheck != -1:
            print('\n~~~ Found keyword ~~~\n')
            keywordurlset.add(abspath)
        else:
            print('\n~~~ Not today ~~~\n')







    print('\n\n~~~~~~~~~~~~ urllistprefilter length =', len(urllistprefilter), ' ~~~~~~~~~~~~\n', urllistprefilter)

    print('\n\n~~~~~~~~~~~~ urllistgood length =', len(urllistgood), ' ~~~~~~~~~~~~\n', urllistgood)



print('\n\n ################## ', len(keywordurlset), ' matches found at: \n', keywordurlset)

print('\n\n', len(errorurls), ' errors found at: \n', errorurls)
