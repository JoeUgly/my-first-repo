

import json


with open('/home/joepers/code/jj_v22/dbs/civ_db', 'r') as f:
    civ_f = json.loads(f.read())


count = 0

for i in civ_f:
    if not i[1]:
        count += 1
        print(i)



print(count, len(civ_f))

















