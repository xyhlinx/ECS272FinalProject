import json

res = {}

def delete_from_dict(dic, key, *args, **kwargs):
    if key in dic:
        del dic[key]

def filter_array(func):
    def wrapper(dic, key, *args, **kwargs):
        if key in dic and isinstance(dic[key], list) and func(dic[key]):
            dic[key] = [dic[key][0]] if dic[key] else []
    return wrapper

def filter_value(func):
    def wrapper(dic, key, _id, removal_ids, *args, **kwargs):
        if key not in dic:
            return
        if not func(dic[key]):
            removal_ids.add(_id)
    return wrapper

def filter_genre(dic, key, _id, removal_ids, *args, **kwargs):
    ordered_match = [
        'Indie',
        'Action',
        'Casual',
        'Adventure',
        'Simulation',
        'Strategy',
        'RPG',
        'Early Access',
        'Free to Play',
        'Sports'
    ]
    match = set(ordered_match)
    if key not in dic:
        return
    overlap = set(dic[key]) & match
    if len(overlap) > 1 and 'tags' in dic and isinstance(dic['tags'], dict):
        for k, v in sorted(dic['tags'].items(), key=lambda x: -x[1]):
            if k in overlap:
                dic[key] = k
                del dic['tags']
                return
    elif len(overlap) == 1:
        dic[key] = list(overlap)[0]
        if 'tags' in dic:
            del dic['tags']
        return
    else:
        pass
    removal_ids.add(_id)

filter_dict = {
    'average_playtime_2weeks': delete_from_dict,
    'mean_playtime_2weeks': delete_from_dict,
    'median_playtime_forever': delete_from_dict,
    'detailed_description': delete_from_dict,
    'about_the_game': delete_from_dict,
    'short_description': delete_from_dict,
    'support_email': delete_from_dict,
    'reviews': delete_from_dict,
    'genres': filter_genre,
    'required_age': delete_from_dict,
    'header_image': delete_from_dict,
    'website': delete_from_dict,
    'support_url': delete_from_dict,
    'windows': delete_from_dict,
    'mac': delete_from_dict,
    'linux': delete_from_dict,
    'metacritic_url': delete_from_dict,
    'notes': delete_from_dict,
    'supported_languages': delete_from_dict,
    'full_audio_languages': delete_from_dict,
    'packages': delete_from_dict,
    'categories': delete_from_dict,
    'screenshots': delete_from_dict,
    'movies': delete_from_dict,
    'metacritic_score': filter_value(lambda x: x > 0),
    'achievements': delete_from_dict
    }

with open('data/games.json') as f:
    dset = json.load(f)
    removal_ids = set()
    for _id, v in dset.items():
        if ('average_playtime_forever' in v
            and (v['average_playtime_forever'] == 0
            or not isinstance(v['average_playtime_forever'], int))):
            continue
        else:
            for key, func in filter_dict.items():
                func(v, key, _id, removal_ids)
            res[_id] = v
    for rid in removal_ids:
        del res[rid]

with open('./data/filtered.json', 'w') as wf:
    wf.write(json.dumps(res, indent=4))
