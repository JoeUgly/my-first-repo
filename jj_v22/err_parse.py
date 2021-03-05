
# Desc: Parse errorlog



# To do:
# there will never be jj_error 8 (sel errors) final error because it will always attempt static req after
# count sel and static successes +
# count how many recoveries from each error
# check if splash groups 4xx and 5xx errors into 'host not found' (caught by jj error 4)
# merge with recurring error checker + could be cleaned up tho





import glob, json





# Open most recent errorlog as dict
dater = glob.glob("/home/joepers/joes_jorbs/*")
dater.sort(reverse=True)
print(dater[0].split('/')[4])
print(dater[1].split('/')[4])
print(dater[2].split('/')[4])

with open(dater[0] + '/errorlog', 'r') as f:
    errorlog_d1 = json.loads(f.read())

with open(dater[1] + '/errorlog', 'r') as f:
    errorlog_d2 = json.loads(f.read())

with open(dater[2] + '/errorlog', 'r') as f:
    errorlog_d3 = json.loads(f.read())








fallback_l = []
jj_7a_l = []
jj_7b_l = []
jj_7c_l = []

# Init jj_error dicts with empty lists
total_d = {}
for i in range(1,10): total_d[str(i)] = []

final_d = {}
for i in range(1,10): final_d[str(i)] = []



for url, value in errorlog_d1.items():

    info_l = value[0]
    org_name = value[0][0]
    db_type = value[0][1]
    crawl_level = value[0][2]

    err_l = value[1]
    final_l = value[-1]


    for each_err in err_l:

        err_num = each_err[1].split('jj_error ')[1][0] # get error number from last error. exclude letter from 7b etc
        
        # Tally all errors
        total_d[err_num].append(url)


    ## use only last err num? record all err nums?
    # Tally final errors
    if 'jj_final_error' in final_l: final_d[err_num].append(url)

 
    if 'fallback_success' in final_l: fallback_l.append(url)

    if ["Empty vis text", "jj_error 7a"] in err_l: jj_7a_l.append(url)
    if ["Empty vis text", "jj_error 7b"] in err_l: jj_7b_l.append(url)
    if ["Empty vis text", "jj_error 7c"] in err_l: jj_7c_l.append(url)




print('\njj_error 1: Unknown error')
print('jj_error 2: Non-HTML - Splash')
print('jj_error 3: Request timeout - Splash')
print('jj_error 4: HTTP 404 / 403 - Splash')
print('jj_error 5: Other request - Splash')
print('jj_error 6: failure - Splash')
print('jj_error 7: Empty vis text')
print('jj_error 8: Selenium req')
print('jj_error 9: Static req')



total = 0
print('\ntotal errors:')
for k,v in total_d.items():
    print('jj_error', k + ':', len(v))
    total += len(v)
print(total)


total = 0
print('\nfinal errors:')
for k,v in final_d.items():
    print('jj_error', k + ':', len(v))
    total += len(v)
print(total)


print('\n\nfallback successes:', len(fallback_l))


print('\njj_7a_tally:', len(jj_7a_l))
print('jj_7b_tally:', len(jj_7b_l))

'''
# URLs recovered from 7a error
for i in jj_7a_l:
    if not i in jj_7b_l: print(i)
'''

print('jj_7c_tally:', len(jj_7c_l))

'''
# URLs recovered from 7b error
for i in jj_7b_l:
    if not i in jj_7c_l: print(i)
'''





# Final errors in most recent
fin_l = []
count1 = 0
for k,v in errorlog_d1.items():
    if 'jj_final_error' in v[-1]:
        count1 += 1
        fin_l.append(k)


# Second most recent
fin_l2 = []
count2 = 0
for k,v in errorlog_d2.items():
    if 'jj_final_error' in v[-1]:
        count2 += 1
        fin_l2.append(k)


# Third most recent
fin_l3 = []
count3 = 0
for k,v in errorlog_d3.items():
    if 'jj_final_error' in v[-1]:
        count3 += 1
        fin_l3.append(k)


# Find recurring error urls
count4 = 0
for i in fin_l:
    if i in fin_l2 and i in fin_l3:
#    if i in fin_l2: # just two most recent errorlogs
        print(i) # Show error URLs
        count4 += 1



print('\n\nerrorlog 1 final errors:', count1)
print('errorlog 2 final errors:', count2)
print('errorlog 3 final errors:', count3)
print('\nRecurring final error urls:', count4)
















