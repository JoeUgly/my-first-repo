
# Desc: Use Google search api to get home url

# Use output from get_org_name_civ.py



old = [
['Port Chester Village', 'http://humanresources.westchestergov.com/job-seekers/civil-service-exams'],
['Peekskill City', 'http://www.cityofpeekskill.com/human-resources/pages/about-human-resources'],
['Rye City', 'http://www.ryeny.gov/human-resources.cfm'],
['White Plains City', 'http://ny-whiteplains.civicplus.com/index.aspx?nid=98'],
['Yonkers City', 'http://www.yonkersny.gov/work/jobs-civil-service-exams'],
['Yorktown Town', 'http://www.yorktownny.org/jobs'],
['Wyoming County', 'http://www.wyomingco.net/164/Civil-Service'],
['Yates County', 'http://www.yatescounty.org/203/Personnel']
]






from googlesearch import search



for i in old:

    string = i[0] + ' ny -wikipedia.org -hometownlocator.com'

    for url in search(string, stop=1, num=1):

        i.insert(1, url)
        print(i)



print('\n\n\n', old)


























