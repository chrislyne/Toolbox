some_list = ['abc-123', 'def-456', 'ghi-789', 'abc-456']
#find if string is in a list
if any("abc" in s for s in some_list):
    # whatever
#find matching in list
matching = [s for s in some_list if "abc" in s]
print matching