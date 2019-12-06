


import pandas as pd



# Open coords file
coords_file = pd.ExcelFile("civ_coords_desc.xlsx")




# Select sheet number
coords_sheet = coords_file.parse()

l = []
g_l = ['COUNTIES', 'CITIES', 'TOWNS', 'VILLAGES']


# Iterate through each org's coords
for i in coords_sheet.index:

    s = coords_sheet['Desc Sub'][i]

    if not s in g_l: continue

    # Find matching org names
    n = coords_sheet['Legal Name'][i]
    c = (coords_sheet['GIS Latitude (Y)'][i], coords_sheet['GIS Longitute (X)'][i])
    

    l.append([n, c])

for i in l: print(i)
























