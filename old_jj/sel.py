# Getting started with Selenium

'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get('http://www.google.com')
element = driver.find_element_by_id('gbqfba') #this element is visible
if element.is_displayed():
  print("Element found")
else:
  print("Element not found")

'''



from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import lxml.html as LH
import lxml.html.clean as clean


options = Options()
options.add_argument('--headless')


driver = webdriver.Firefox(options=options)
driver.get('https://www.hilbert.edu/about/human-resources/hilbert-job-openings')


bod = driver.find_element_by_xpath("/html/body")


print(bod.text)



driver.close()
driver.quit()






























