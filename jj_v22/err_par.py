
# Desc: Interpret jj errorlog



import glob, json



dater = glob.glob("/home/joepers/joes_jorbs/*")
dater.sort(reverse=True)


with open(dater[0] + '/errorlog.txt', 'r') as f:
    errorlog_d = json.loads(f.read())

with open(dater[1] + '/errorlog.txt', 'r') as f:
    errorlog_d2 = json.loads(f.read())

#with open(dater[2] + '/errorlog.txt', 'r') as f:
#    errorlog_d3 = json.loads(f.read())




# Count all errors
port_err = []
count = 0
for k,v in errorlog_d.items():
    count += len(v[1])
    if v[0][2] < 1:
        port_err.append(k)



print('\nTotal errors:', count)

#for i in port_err: print(i)

print('Portal errors:', len(port_err))





# Final errors
fin_l = []
count = 0
for k,v in errorlog_d.items():
    if 'jj_final_error' in v:
        count += 1
        fin_l.append(k)
print('Total final errors:', count)



# Fallback success
count = 0
for k,v in errorlog_d.items():
    if 'fallback_success' in v:
        count += 1
print('Portal fallback sucesses:', count)








# Second most recent
fin_l2 = []
count = 0
for k,v in errorlog_d2.items():
    if 'jj_final_error' in v:
        count += 1
        fin_l2.append(k)

'''
# Third most recent
fin_l3 = []
count = 0
for k,v in errorlog_d3.items():
    if 'jj_final_error' in v:
        count += 1
        fin_l3.append(k)
'''


# Find reoccuring error urls
count = 0
for i in fin_l:
#    if i in fin_l2 and i in fin_l3:
    if i in fin_l2:
        print(i)
        count += 1

print('\nReoccuring error urls:', count)






tally_d = {}
for i in range(1,10): tally_d[i] = 0

# Tally freq of each jj_error
for v in errorlog_d.values():
    if not 'jj_final_error' in v: continue
    for i in tally_d:
        if v[1][-1][0][9] == str(i): tally_d[i] += 1
        ## use this for jj error 10 and higher or to include letter designation: v[1][-1][0].split(' ')[1]


# Display errors
print('   Error code:     Description | Frequency')
print('  -----------------------------|-------------')
print('      Error 1:   Unknown error |', tally_d[1])
print('      Error 2:        Non-HTML |', tally_d[2])
print('      Error 3: Request timeout |', tally_d[3])
print('      Error 4:  HTTP 404 / 403 |', tally_d[4])
print('      Error 5:   Other request |', tally_d[5])
print('      Error 6:  Splash failure |', tally_d[6])
print('      Error 7:  Empty vis text |', tally_d[7])
print('      Error 8:    Selenium req |', tally_d[8])
print('      Error 9:      Static req |', tally_d[9])











    













