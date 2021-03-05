
# Desc: Find which URLs are consistantly failing. Find which urls have final errors in all 3 of the most recent jj_scraper errorlogs






all_err_urls_l = []
e1_urls_l = []
e2_urls_l = []
e3_urls_l = []



# open files and save as dict
# Read 3 most recent errorlog files
with open('/home/joepers/joes_jorbs/01_18_21/errorlog.txt') as f:
    temp_list = eval(f.read())
    e1_d = dict(temp_list)

with open('/home/joepers/joes_jorbs/02_01_21/errorlog.txt') as f:
    temp_list = eval(f.read())
    e2_d = dict(temp_list)

with open('/home/joepers/joes_jorbs/.old_2020/12_07_20/errorlog.txt') as f:
    temp_list = eval(f.read())
    e3_d = dict(temp_list)




# create list of urls with final errors in each of the errorlogs
for i in e1_d.items():
    if 'jj_final_error' in i[1][-1]:
        if i[1][0][-1] == 0:
            e1_urls_l.append([i[1][0][0], i[0]])

for i in e2_d.items():
    if 'jj_final_error' in i[1][-1]:
        if i[1][0][-1] == 0:
            e2_urls_l.append([i[1][0][0], i[0]])

for i in e3_d.items():
    if 'jj_final_error' in i[1][-1]:
        if i[1][0][-1] == 0:
            e3_urls_l.append([i[1][0][0], i[0]])


# how many errors in each errorlog
print(len(e1_urls_l), len(e2_urls_l), len(e3_urls_l))



# which urls are in all 3 lists
for i in e1_urls_l:
    if i in e2_urls_l:
        if i in e3_urls_l: all_err_urls_l.append(i)


# these urls have final errors in all 3 of the most recent jj_scraper errorlogs
for i in all_err_urls_l:
    print(i)
print(len(all_err_urls_l))



















