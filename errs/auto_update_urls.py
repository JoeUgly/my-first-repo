
# Desc: Replace old URLs with new URLs





new_l = [
['City of Beacon', 'https://www.cityofbeacon.org/index.php/employment-opportunities/'],
['City of Jamestown', 'https://www.jamestownny.net/employment-opportunities/'],
['City of Long Beach', 'https://www.longbeachny.gov/index.asp?type=b_basic&amp;sec=%7B9c88689c-135f-4293-a9ce-7a50346bea23%7D'],
['City of Plattsburgh', 'https://www.clintoncountygov.com/employment'],
['City of Rochester', 'https://www.cityofrochester.gov/article.aspx?id=8589936759'],
['County of Broome', 'https://www.gobroomecounty.com/personnel/cs'],
['County of Cattaraugus', 'https://cattco-portal.mycivilservice.com'],
['County of Clinton', 'https://www.clintoncountygov.com/employment'],
['County of Monroe', 'https://www.monroecounty.gov/hr-careers'],
['County of Montgomery', 'https://www.co.montgomery.ny.us/web/sites/departments/personnel/default.asp'],
['County of Oneida', 'https://ocgov.net//personnel'],
['County of Tioga', 'https://www.tiogacountyny.com/departments/personnel-civil-service'],
['County of Tompkins', 'https://www2.tompkinscountyny.gov/personnel'],
['Town of Alden', 'https://www2.erie.gov/alden/index.php?q=employment-opportunities'],
['Town of Amherst', 'http://www.amherst.ny.us/'],
['Town of Beekman', 'https://www.townofbeekman.com/index.asp?Type=B_BASIC&SEC=%7B03E912D9-3F74-4E1F-8BE3-FAB7141BE80F%7D'],
['Town of Clarence', 'https://www2.erie.gov/clarence/index.php?q=jobs'],
['Town of Cortlandt', 'https://www.townofcortlandt.com/'],
['Town of East Greenbush', 'https://www.eastgreenbush.org/departments/human-resources/employment-opportunities'],
['Town of Eastchester', 'https://www.eastchester.org/departments/comptoller.php'],
['Town of Huntington', 'https://www.huntingtonny.gov/content/13753/13757/17478/17508/default.aspx?_sm_au_=ivvt78qz5w7p2qhf'],
['Town of Newburgh', 'https://www.townofnewburgh.org/cn/Employment/?tpid=12612'],
['Town of Newstead', 'https://www2.erie.gov/newstead/index.php?q=legal-notices-job-postings'],
['Town of Oyster Bay', 'https://oysterbaytown.com/departments/human-resources/'],
['Town of Penfield', 'http://www.penfield.org/'],
['Town of Sardinia', 'https://www2.erie.gov/sardinia/index.php?q=employment'],
['Town of Wappinger', 'https://townofwappingerny.gov/employment-opportunities/'],
['Town of Williamson', 'https://town.williamson.ny.us/employment-opportunities/'],
['Village of Bronxville', 'https://www.villageofbronxville.com/clerk/pages/employment-opportunities'],
['Village of Candor', 'https://www.tiogacountyny.com/departments/personnel-civil-service/'],
['Village of Coxsackie', 'https://villageofcoxsackie.com/job-archive-page/'],
['Village of Valley Stream', 'https://www.vsvny.org/index.asp?type=b_job&amp;sec=%7B05c716c7-40ee-49ee-b5ee-14efa9074ab9%7D&amp;_sm_au_=ivv8z8lp1wffsnv6'],
]



# DB to be updated
f_path = '/home/joepers/code/jj_v22/dbs/civ_db'


with open(f_path) as f:
    f = eval(f.read())


with open(f_path, "w") as f_file:
    f_file.write('[\n')



for line in f:
    for new_i in new_l:

        if line[0] == new_i[0]:
            line[1] = new_i[1]

            break

    with open(f_path, "a") as f_file:
        f_file.write(str(line) + ',\n')




with open(f_path, "a") as f_file:
    f_file.write('\n]')





'''
# loop thru all db files
for i in glob.glob('/home/joepers/code/jj_v22/dbs/*'):
    f = open(i).read()


    # find by url or org name?
    for line in f.split('\n'):
        if line
'''




























