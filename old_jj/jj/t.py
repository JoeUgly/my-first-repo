from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup as BSoup


def get_states():
    url = 'https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States'
    driver = webdriver.Chrome()
    driver.get(url)

    bs_obj = BSoup(driver.page_source, 'html.parser')
    rows = bs_obj.find_all('table')[0].find('tbody').find_all('tr')

    states = []

    for row in rows:
        cells = row.find_all('td')
        name = row.find('th').get_text()
        abbr = cells[0].get_text()
        established = cells[-9].get_text()
        population = cells[-8].get_text()
        total_area_km = cells[-6].get_text()
        land_area_km = cells[-4].get_text()
        water_area_km = cells[-2].get_text()

        states.append([
            name, abbr, established, population, total_area_km, land_area_km,
            water_area_km
        ])
    driver.quit()
    return states


if __name__ == '__main__':
    start = datetime.now()
    states = get_states()
    finish = datetime.now() - start
    print(finish)