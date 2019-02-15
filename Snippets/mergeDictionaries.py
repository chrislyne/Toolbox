from itertools import chain
from collections import defaultdict

#merge dictionaries retaining keys
dict1 = {'img':{'imgpath':'path'}}
dict2 = {'img':{'imgname':'name'}}
dict3 = defaultdict(list)
for k, v in chain(dict1.items(),dict2.items()):
    dict3[k].append(v)
    
    
for k, v in dict3.items():
    print (k,v)

###############################################################################
###############################################################################

#merge dictionaries replacing keys
dict1 = {'imgpath':'path'}
dict2 = {'imgname':'name'}

dict1.update(dict2)
print dict1