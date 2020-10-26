
# Desc: Compare speed of reading from files and reading from memcached
# Don't forget to run `memcached &' in bash then run mem_set.py



# to do:
# Use pymemcache.client.base.Client.get_many() 
# performance increase is because of skipping incorrectly formatted keys
# 12.9, 1399
# 22.3, 2463
# ~ 40% fewer results


# Results:

# keyword = librarian
# original = 3.7 s
# memcache = 2.3 s
# ~ 38% improvement

# keywords = ['officer', 'correctional officer', 'corrections officer', 'prison guard'
# original = 22.3 s
# memcache = 13.5 s
# ~ 39% improvement


'''
Memcached method = False
14.4394 seconds
1373 1373

Memcached method = True
14.7844 seconds
1373 1373

Memcached method = True
9.1209 seconds
840 840
'''




import regex, datetime, os, subprocess
from pymemcache.client.base import Client



startTime = datetime.datetime.now()






client = Client('localhost')




keyword_list = ['officer', 'correctional officer', 'corrections officer', 'prison guard']
#keyword_list = ['librarian']


# Lists containing keywords separated by keyword length
edit_2_l = []
edit_1_l = []
edit_0_l = []




# Sort keywords into lists based on keyword length. Longer keywords get more regex edits
for keyword in keyword_list:
    
    if len(keyword) > 17: edit_2_l.append(keyword)
    elif len(keyword) > 8: edit_1_l.append(keyword)
    else: edit_0_l.append(keyword)


reg_pat = '' ## unn?


# Append 0 edit regex pattern(s)
if edit_0_l:

    # Form regex pattern made of each item in keyword list. Start by adding a paren to beginning of string
    reg_pat='('

    # Separate each list item with a pipe
    for i in edit_0_l: reg_pat+=i+'|'

    # Remove trailing pipe then append max number of edits
    reg_pat=reg_pat[:-1]+')'


# Append 1 edit regex pattern(s)
if edit_1_l:

    # Previous 0 edit entry
    if edit_0_l:
        reg_pat += '|'

    # Form regex pattern made of each item in keyword list. Start by adding a paren to beginning of string
    reg_pat=reg_pat+'('

    # Separate each list item with a pipe
    for i in edit_1_l: reg_pat+=i+'|'

    # Remove trailing pipe then append max number of edits
    reg_pat=reg_pat[:-1]+'){e<=1}'



# Append 2 edit regex pattern(s)
if edit_2_l:

    # Previous 0 or 1 edit entry
    if edit_0_l or edit_1_l:
        reg_pat += '|'

    # Form regex pattern made of each item in keyword list. Start by adding a paren to beginning of string
    reg_pat=reg_pat+'('

    # Separate each list item with a pipe
    for i in edit_2_l: reg_pat+=i+'|'

    # Remove trailing pipe then append max number of edits
    reg_pat=reg_pat[:-1]+'){e<=2}'




print('\nedit_0_l =', edit_0_l, '\nedit_1_l =', edit_1_l, '\nedit_2_l =', edit_2_l, '\n\n reg_pat =', reg_pat, '\n\n')

# Compile regex pattern
reg_pat = regex.compile(reg_pat, regex.BESTMATCH)

count1 = 0
count2 = 0




new_l = [] # list to put all memcached keys so this script doesn't need to read keys from disk



####   Comment this section out to use original/disk/non memcached method
''''''
bashCommand = 'memcdump --servers=localhost' # Bash command to get all memcached keys
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE) # Run command
output = process.communicate() # Get output
## must fix. \n occurs when not referring to newline
for i in str(output)[3:-7].split('\\n'): # Format output for python
    if  i =="'": continue
    print(i)
    count1 += 1
    new_l.append(i.replace('\\\\', '\\'))


newD = client.get_many(new_l)



# Memcached method
if new_l:
	
    memcache = True

    for memK, memV in newD.items():

        

        #new_path = each_file.replace(' ', '_') # unn because no spaces in URLs?

        file_contents = str(memV)

        # Search text file for compiled pattern
        reg_res = regex.search(reg_pat, file_contents)

        count2 += 1

        # Calculate percent similarity
        if reg_res:

            # Count number of edits
            t = 0
            for i in reg_res.fuzzy_counts: t+=i

            # Calculate percent similarity
            fuzzy_percent = round(len(reg_res.group()) / (len(reg_res.group()) + t) * 100, 1)

            # Disallow match if below threshold. This is needed for short keywords
            if fuzzy_percent > 89: 

                # Append percent sign
                fuzzy_percent = str(fuzzy_percent) + '%'

                # Get new match
                fuzzy_match = reg_res.group()

                # Display results
                print('\n', fuzzy_percent, fuzzy_match, memK)










# Original method from disk
else:

    memcache = False

    # Open webpage text file
    for root, subdirs, files in os.walk('/home/joepers/joes_jorbs/09_16_20/results/sch'):

        for each_file in files:

            count1 += 1

            file_path = os.path.join(root, each_file)

            #new_path = each_file.replace(' ', '_') # unn because no spaces in URLs?

            file_contents=open(file_path).read()

            # Search text file for compiled pattern
            reg_res = regex.search(reg_pat, file_contents)

            count2 += 1

            # Calculate percent similarity
            if reg_res:

                # Count number of edits
                t = 0
                for i in reg_res.fuzzy_counts: t+=i

                # Calculate percent similarity
                fuzzy_percent = round(len(reg_res.group()) / (len(reg_res.group()) + t) * 100, 1)

                # Disallow match if below threshold. This is needed for short keywords
                if fuzzy_percent > 89: 

                    # Append percent sign
                    fuzzy_percent = str(fuzzy_percent) + '%'

                    # Get new match
                    fuzzy_match = reg_res.group()

                    # Display results
                    print('\n', fuzzy_percent, fuzzy_match, each_file)




# Display duration
print('\n\nMemcached method =', memcache)
print(str(round((datetime.datetime.now() - startTime).total_seconds(), 4)) + ' seconds')
print(count1, count2)











