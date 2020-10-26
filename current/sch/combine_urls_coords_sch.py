
# Desc: Combine URLs and coordinates from school districts


# http://eservices.nysed.gov/sedreports/list?id=1
# URLs source: School Districts: Active School District Superintendent Contact Info and Institution URL
# Coords source: All Institutions: Active Institutions with GIS coordinates and OITS Accuracy Code - Select by County




import csv
import pandas as pd



coord_l = []
url_l = []


## Make list of org names and coords
# Open coords file
coords_file = pd.ExcelFile("sch_coords.xlsx")

# Select sheet number
coords_sheet = coords_file.parse()

# Select column
name_col = coords_sheet['Legal Name']

# Get number of rows
num_rows = len(coords_sheet.index)

for i in range(num_rows):

    # Select org name by row
    org_name = name_col[i]

    # Select coords by col and row
    coords = (coords_sheet['GIS Latitude (Y)'][i], coords_sheet['GIS Longitute (X)'][i])

    ws = (org_name, coords)
    coord_l.append(ws)




## Make list of org names and URLs
# Open URL file, specify unusual encoding and delimiter
with open('sch_urls.csv', newline='', encoding='utf-16') as f:
    reader = csv.reader(f, delimiter='\t')

    for row in reader:

        # Select org name
        org_name = row[0]

        # Select URL
        url = row[2]

        ws = (org_name, url)
        url_l.append(ws)




fin_l = []
err_l = []


# Match org names from URLs list and coords list
for ic in coord_l:

    for iu in url_l:

        # Find matching org names
        if ic[0] == iu[0]:

            # Append org name, URL, and coords
            ws = (ic[0], iu[1], ic[1])
            fin_l.append(ws)

            ## Remove URL from list?
            #url_l.remove(iu)
            break

    # Catch no matches
    else:
        err_l.append(ic[0])



for i in fin_l: print(str(i) + ',')
print(len(fin_l), 'Good list up there\n\n Unused coords down here:', len(err_l))
for i in err_l: print(i)
print('\n Unused urls:', len(url_l), url_l)





print('\n\n\n\n', coord_l)
print('\n\n\n\n', url_l)


url_l













