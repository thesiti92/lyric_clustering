import json

def make_unique(original_list):
    unique_list = []
    [unique_list.append(obj) for obj in original_list if obj not in unique_list]
    return unique_list

with open("country_songs.json", mode='r') as file:
    list = json.load(file)
    print len(list)
    print len(make_unique(list))
