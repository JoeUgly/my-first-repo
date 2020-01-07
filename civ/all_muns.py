
# Desc:
# Get URLs for counties, cities, towns, and villages
# Get coordinates for counties, cities, towns, and villages
# Combine entries from both lists


# URLs' source: https://data.ny.gov/Government-Finance/New-York-State-Locality-Hierarchy-with-Websites/55k6-h6qq/data
# Coords source: http://eservices.nysed.gov/sedreports/list?id=1
# All Institutions: Active Institutions with GIS coordinates and OITS Accuracy Code - Select by County



import pandas as pd




# Open URL file
url_file = pd.read_csv("New_York_State_Locality_Hierarchy_with_Websites.csv")

# Select column
mun_col = url_file['Municipality']

# Put results here
url_l = []


# Iterate through each row
for each_row in url_file.index:

    # Get municipality type
    mun_type = url_file['Type'][each_row]

    # Get municipality name
    mun_name = str(mun_col[each_row])
    
    # Use County column for counties
    if mun_type == 'County':
        mun_name = url_file['County Name'][each_row]

    # Get URL
    url = url_file['Website'][each_row]

    # Convert floating point nan to None
    if str(url) == 'nan': url = None

    # Form legal name
    leg_name = str(mun_type + ' of ' + mun_name)

    #print('\n', leg_name, '\n', url)

    # Put results into list
    url_l.append([leg_name, url])




## Make list of org names and coords
# Open coords file
coords_file = pd.ExcelFile("civ_coords.xlsx")

# Select sheet number
coords_sheet = coords_file.parse()

# Select column
name_col = coords_sheet['Legal Name']


# Iterate through each org's URL
for html_org in url_l:

    # Iterate through each org's coords
    for i in coords_sheet.index:

        # Find matching org names
        if coords_sheet['Legal Name'][i].lower().strip() == html_org[0].lower():

            coords = (coords_sheet['GIS Latitude (Y)'][i], coords_sheet['GIS Longitute (X)'][i])

            print(str([html_org[0], html_org[1], coords]) + ',')
            break

    else: 
        print('no match:', str([html_org[0], html_org[1], (0.0, 0.0)])  + ',')


















