import json

res = {}

def delete_from_dict(dic, key):
    if key in dic:
        del dic[key]

def filtered_amount(dic, key, amount=1):
    if key in dic and isinstance(dic[key], list):
        dic[key] = [dic[key][0]] if dic[key] else []

filter_dict = {'average_playtime_2weeks': delete_from_dict,
    'mean_playtime_2weeks': delete_from_dict,
    'median_playtime_forever': delete_from_dict,
    'detailed_description': delete_from_dict,
    'about_the_game': delete_from_dict,
    'short_description': delete_from_dict,
    'support_email': delete_from_dict,
    'reviews': delete_from_dict,
    'screenshots': filtered_amount}

with open('data/games.json') as f:
    dset = json.load(f)
    for _id, v in dset.items():
        if ('average_playtime_forever' in v
            and (v['average_playtime_forever'] == 0
            or not isinstance(v['average_playtime_forever'], int))):
                continue
        else:
            for key, func in filter_dict.items():
                func(v, key)
            res[_id] = v

with open('filtered.json', 'w') as wf:
    wf.write(json.dumps(res, indent=4))
