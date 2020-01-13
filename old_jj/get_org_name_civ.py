
# Description: Get org name and home url from raw html


# https://labor.ny.gov/stats/cslist.shtm




from bs4 import BeautifulSoup

the_db = []

# Open raw html file
f = open('raw_html_civ.txt')


soup = BeautifulSoup(f, 'html5lib')

# Get all anchor elements
for i in soup.find_all('a'):

    # Get org name and home url
    org_name = i.text
    home_url = i.get('href')

    # Create work_list based of org name and home url
    work_list = []

    work_list.append(org_name)
    work_list.append(home_url.strip())

    # Mark dups as such
    for each_item in the_db:
        if home_url == each_item[1]:
            work_list[1] = '_DUP._' + work_list[1]
            break

    # Append work_list to the_db if not a dup
    the_db.append(work_list)



for i in the_db:
    print(str(i) + ',')

print('\n\n\nTotal:', len(the_db))
















