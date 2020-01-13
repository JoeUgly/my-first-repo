
# Testing multi pages with Selenium



import datetime, time, queue
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from multiprocessing import active_children, Lock, Manager, Process, Queue, Value


startTime = datetime.datetime.now()



keyword_list = ['librarian', 'library clerk', 'library aide', 'library media specialist']

url_list = [
'http://buffaloschools.applicantstack.com/x/openings',
#'http://aldenschools.org/Page/25',
#'http://academyofthecity.org/about_us/employment',
#'http://bemusptcsd.org/district/employment_information',
#'http://berlincentral.org/district/employment',
#'http://bit.ly/2xbEAIJ',
#'http://bphs.democracyprep.org'
#'http://brillacollegeprep.org/careers',
#'http://brooklyncompass.org/careers',
#'http://brooklyneastcollegiate.uncommonschools.org/brooklyn-east/careers',
#'http://brownsvillecollegiate.uncommonschools.org/bvc/careers',
#'http://buffaloschools.applicantstack.com/x/openings'
]


lock = Lock()


options = Options()
options.add_argument('--headless')


sel_q = Queue()


for i in url_list:
    sel_q.put(i)




def scraper(sel_q):

    while True:

        try:
            with lock:
                each_url = sel_q.get(False)

        # Close process if queue is empty
        except queue.Empty:
            print('empty')
            break


        # Request
        driver = webdriver.Firefox(options=options)
        driver.get(each_url)

        #print('got0:', each_url, driver)

        # Get body
        sel_text = driver.find_element_by_css_selector("body").text

        # Switch to xpath if css fails
        if not str(sel_text).strip():
            print('trying xpath')
            sel_text = driver.find_element_by_xpath("/html/body").text

            # Exit if xpath also fails
            if not str(sel_text).strip():
                print('dub err')
                continue

        print('got2:', each_url, type(sel_text))

        if any(sss in str(sel_text).lower() for sss in keyword_list):
            print('yabadadaddoooooo@@@@@@@@')

        print('~~~', str(sel_text).lower(), '~~~')


        driver.close()


    # Close browser
    driver.quit()



# Create child processes
for ii in range(1):
    worker = Process(target=scraper, args=(sel_q,))
    worker.start()



while len(active_children()) > 0:
    time.sleep(3)


print(datetime.datetime.now() - startTime)



























