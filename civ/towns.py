
# Desc: Get org name and URLs from website


from bs4 import BeautifulSoup


f = open("/home/joepers/Desktop/code/current/civ/New York Towns.html")

soup = BeautifulSoup(f, 'html5lib')



g_c = 0
b_c = 0

for i in soup.find_all(class_='field-content town-name'):
    name = i.text

    anchor = i.find('a')
    if anchor:
        url = anchor.get('href')
        g_c += 1
    else:
        url = None
        b_c += 1

    print('\n\n', name, '\n', url)
    #print(name)
    #print(i)



print(g_c, b_c)




















