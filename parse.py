import json

with open('equipmentItem') as json_file:
    f = open('equipmentItem',)
    data = json.load(f)
    for items in data['BookList']:
            print(items['name'] + " " + str(items['elementAffinity']))
    f.close()
