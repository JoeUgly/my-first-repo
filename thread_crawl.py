
import threading
import datetime
startTime = datetime.datetime.now()

import urllib.request, urllib.parse, urllib.error, os, platform
from threading import Thread

allcivurls = []


civfile = open(r'''/home/joepers/code/current/civ_crawl/civil_ny''')
for civline0 in civfile:
    civline = civline0.strip()
    allcivurls.append(civline)

numcivurls = len(allcivurls)


num_shell = 43
block_size = int(numcivurls / num_shell + 1)
block_count = 0
block_begin = 0
block_end = block_size
urlblock = 'aaa'


# Define the crawling function
def worker(urlblock):
    print('\n\n\nblock_count = ', block_count, '\nurlblock length =', len(urlblock), '\n', urlblock, '\n')
    for eachurl in urlblock:
        print('\neachurl = ', eachurl)



# Create blocks of URLs
while block_count <= num_shell:
    urlblock = allcivurls[block_begin:block_end]
    
    # Assign blocks to new threads until empty
    if urlblock:
        t = threading.Thread(target=worker, args=(urlblock,))
        t.start()
        block_begin += block_size
        block_end += block_size
        block_count += 1
    elif not urlblock:
        break


        

























