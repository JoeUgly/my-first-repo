
# Desc: take list of failing urls and org names, and fix em





all_l = [
['City of Dunkirk', 'http://www.dunkirktoday.com/city-offices/personnel'],
['County of Franklin', 'http://countyfranklin.digitaltowpath.org:10078/content/Departments/View/6:field=services;/content/DepartmentServices/View/50'],
['County of Fulton', 'http://www.fultoncountyny.gov/node/5'],
['Town of Brutus', 'http://townbrutus.digitaltowpath.org:10148/content/JobCategories'],
['Town of Carlisle', 'http://www2.schohariecounty-ny.gov/PdfPostingsWebApp/faces/ExamAnnouncementIndex.xhtml'],
['Town of Caneadea', 'http://towncaneadea.digitaltowpath.org:10139/content/JobCategories'],
['Town of Conesus', 'http://townconesus.digitaltowpath.org:10010/content/JobCategories'],
['Town of Deerfield', 'http://towndeerfield.digitaltowpath.org:10063/content/JobCategories'],
['Town of Fine', 'http://townfine.digitaltowpath.org:10054/content/JobCategories'],
['Town of Galen', 'http://towngalen.digitaltowpath.org:10476/content/JobCategories'],
['Town of Hartwick', 'http://townhartwick.digitaltowpath.org:10113/content/JobCategories'],
['Town of Indian Lake', 'http://townindianlake.digitaltowpath.org:10201/content/JobCategories'],
['Town of Marcy', 'http://townmarcy.digitaltowpath.org:10019/content/JobCategories'],
['Town of Mayfield', 'http://townmayfield.digitaltowpath.org:10052/content/404'],
['Town of Paris', 'http://townparis.digitaltowpath.org:10026/content/JobCategories'],
['Town of Pinckney', 'http://townpinckney.digitaltowpath.org:10161/content/JobCategories'],
['Town of Princetown', 'http://townprincetown.digitaltowpath.org:10095/content/JobCategories'],
['Town of Richmond', 'http://townrichmond.digitaltowpath.org:10135/content/JobCategories'],
['Town of Royalton', 'http://townroyalton.digitaltowpath.org:10057/content/JobCategories'],
['Town of Russia', 'http://townrussia.digitaltowpath.org:10221/content/JobCategories'],
['Town of Springwater', 'http://townspringwater.digitaltowpath.org:10071/content/JobCategories'],
['Town of Sullivan', 'http://townsullivan.digitaltowpath.org:10021/content/JobCategories'],
['Town of Trenton', 'http://towntrenton.digitaltowpath.org:10031/content/JobCategories'],
['Town of Verona', 'http://townverona.digitaltowpath.org:10032/content/JobCategories'],
['Town of Wayland', 'http://townwayland.digitaltowpath.org:10163/content/JobCategories'],
['Town of Whitestown', 'http://townwhitestown.digitaltowpath.org:10034/content/JobCategories'],
['Village of Fonda', 'http://villagefonda.digitaltowpath.org:10193/content/JobCategories'],
['Village of Laurel Hollow', 'http://villagelaurelhollow.digitaltowpath.org:10216/content/JobCategories'],
['Village of Middleport', 'http://villagemiddleport.digitaltowpath.org:10141/content/JobCategories'],
['Village of New Hartford', 'http://villagenewhartford.digitaltowpath.org:10114/content/JobCategories'],
['Village of New York Mills', 'http://villagenewyorkmills.digitaltowpath.org:10028/content/JobCategories'],
['Village of Otisville', 'http://villageotisville.digitaltowpath.org:10202/content/JobCategories'],
['Village of Pulaski', 'http://villagepulaski.digitaltowpath.org:10789/content/JobCategories'],
['Village of Stewart Manor', 'http://villagestewartmanor.digitaltowpath.org:10254/content/JobCategories'],
['Village of West Carthage', 'http://villagewestcarthage.digitaltowpath.org:10087/content/JobCategories'],
['Village of Wilson', 'http://villagewilson.digitaltowpath.org:10199/content/JobCategories'],
['Canton Central School District', 'http://www.ccsdk12.org'],
['Canisteo-Greenwood Csd', 'https://www.cgcsd.org:443/Page/51'],
['Central Valley Csd At Ilion-Mohawk', 'https://www.cvalleycsd.org/human-resources/'],
['Eastchester Union Free School District', 'https://district.eastchesterschools.org/m2/'],
['Edmeston Central School District', 'http://www.edmestoncentralschool.net/job-of-the-week'],
['Portville Central School District', 'http://www.portville.wnyric.org'],
['Tri-State College of Acupuncture', 'http://www.tsca.edu/site/acupuncture/contact-job-office/']
]


import requests, urllib3
urllib3.disable_warnings()




user_agent_str = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0'






# Static HTML requester
def static_requester_f(workingurl):
    try:
        resp = requests.get(workingurl, timeout=15, headers={'User-Agent': user_agent_str}, verify=False)


        # Success
        return resp.url, resp.status_code, resp.text

    # Catch request errors
    except Exception as errex:
        print('error:', workingurl, errex)
        return False





fixed_urls_l = [] 
failed_urls_l = []




for i in all_l:
    print('\n\nBegin:', i)
    orig_url = i[1]
    workingurl = orig_url

    # Change to https
    if 'digitaltowpath' in orig_url:
        workingurl = orig_url.replace('http://', 'https://')

    # Request
    resp_red_t = static_requester_f(workingurl)

    # Success
    if isinstance(resp_red_t, tuple) and resp_red_t[1] == 200:
        print('\nsuccess:', i[0], workingurl)
        fixed_urls_l.append([orig_url, workingurl])


    # Failed
    else:
        print('\nfail:', i[0], workingurl)
        failed_urls_l.append([orig_url, workingurl])








print('\n\n\nsucc:')
for i in fixed_urls_l: print(i)


print('\n\n\nfail:')
for i in failed_urls_l: print(i)




























