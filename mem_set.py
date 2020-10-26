# Desc: Add webpage files to memcache


# To do:
# use most recent results dir
# run memcached in bash +
# paths cannot contain whitespace +
# content must be ascii safe +
# path corrections are gonna wreak havoc in results.py
# pip install on server
# run on startup
# find alternative to backslashes in urls
# error hnadling: max char key length
# fallback to disk?




import os, subprocess, time
from pymemcache.client.base import Client



# Start memcached with bash
process = subprocess.Popen('memcached') # Run command
time.sleep(3)


# Start memcached python client
client = Client('localhost')


count1 = 0
count2 = 0


# Open webpage text file
for root, subdirs, files in os.walk('/home/joepers/joes_jorbs/09_16_20/results/sch'):

    for each_file in files:

        count1 += 1

        # Abs path
        file_path = os.path.join(root, each_file)

        # File content
        file_content = open(file_path).read()

        # Make content ascii safe
        ## unn after two more scrapes
        if not file_content.isascii(): file_content = file_content.encode('ascii', 'ignore')

        # Remove space from path
        #new_path = each_file.replace(' ', '_') # unn because no spaces in URLs?

        #if new_path.endswith('\\'):
            #print('yup', new_path)
        #    new_path = new_path[:-1]

        print(each_file)

        client.set(each_file, file_content)

        count2 += 1



print(count1, count2)








