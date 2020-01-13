
# Get visible text with Selenium


#data-parent=<some_var>
#find_element_by_id("<some_var>")

# Selecting an immediate child vs any child under that element:
# Immediate child ('/'): span/form
# Any level deep child ('//'): span//form
# how get visible text on 'https://web.co.wayne.ny.us/index.php/human-resources/current-job-openings/'



import datetime, sys, time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

startTime = datetime.datetime.now()

keyword_list = ['librarian', 'library clerk', 'library aide', 'library media specialist']



options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)



sel_url = 'https://web.co.wayne.ny.us/index.php/human-resources/current-job-openings/'


# https://web.co.wayne.ny.us/index.php/human-resources/current-job-openings/
# https://www.applitrack.com/penfield/onlineapp/default.aspx?all=1


# Request
driver.get(sel_url)

print(driver.page_source)

# Include iframes
count = 0
while True:
    try:
        driver.switch_to.frame(count)
        print('count:', count, '\n', driver.page_source)
        count += 1
    except:
        print('iframe not found at:', count)
        break





#print(driver.execute_script("return document.body.outerHTML"))


# Switch back to main frame
driver.switch_to.default_content()

# Get visible text
sel_text = driver.find_element_by_css_selector("body").text

# Switch to xpath if css fails
if not str(sel_text).strip():
    sel_text = driver.find_element_by_xpath("/html/body").text

    # Exit if xpath also fails
    if not str(sel_text).strip():
        print('\nCSS and Xpath selectors have failed:', sel_url)
        driver.close()
        sys.exit()

print('defualt vis:', sel_text)

# Then check iframes
count = 0
while True:
    try:
        driver.switch_to.frame(count)

        # Get visible text
        sel_text = driver.find_element_by_css_selector("body").text

        # Switch to xpath if css fails
        if not str(sel_text).strip():
            sel_text = driver.find_element_by_xpath("/html/body").text

            # Exit if xpath also fails
            if not str(sel_text).strip():
                print('\nCSS and Xpath selectors have failed:', sel_url)
                driver.close()
                sys.exit()

        print('count:', count, '\n', sel_text)
        count += 1
    except Exception as errex:
        print(errex, 'iframe not found at:', count)
        break

'''
# Get visible text
sel_text = driver.find_element_by_css_selector("body").text

# Switch to xpath if css fails
if not str(sel_text).strip():
    sel_text = driver.find_element_by_xpath("/html/body").text

    # Exit if xpath also fails
    if not str(sel_text).strip():
        print('\nCSS and Xpath selectors have failed:', sel_url)
        driver.close()
        sys.exit()

print('\n\nvvis:', sel_text)
'''


'''
#coll_elems = driver.find_elements_by_xpath("//div[@class='panel-collapse collapse']")

# Find collapsible elements
coll_elems = driver.find_elements_by_xpath("//a[@data-toggle='collapse']")

if len(coll_elems) > 0:

    for i in coll_elems:

        i.click()
        time.sleep(.5)


        ## content and clickable objects are seperate elements. In order to get both you need to go up a few parents
        pp = i.find_element_by_xpath('..')
        pp = pp.find_element_by_xpath('..')
        pp = pp.find_element_by_xpath('..')
        pp = pp.find_element_by_xpath('..')
        print('\n\n\n~~~', pp.text)


        # Must perform search after each click because only one elem is visible at a time
        sel_text = sel_text + driver.find_element_by_css_selector("body").text


print(sel_text)

'''



# Close the tab (or browser if only one tab)
driver.close()

# Close browser
#driver.quit()

print(datetime.datetime.now() - startTime)



























