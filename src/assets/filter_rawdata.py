import pandas as pd
import csv
import json
import collections


dset = pd.read_csv('./data/games.csv', encoding='latin1')
df = pd.DataFrame(dset)
df[['Genres', 'Categories']].to_csv('tmp.csv')

genre_set = collections.defaultdict(int)
categories_set = set()
res = {}

with open('tmp.csv') as rf:
    reader = csv.reader(rf)
    for r in reader:
        _id, gs, cs = r
        for g in gs.split(','):
            if not g:
                continue
            genre_set[g] += 1

        for category in cs.split(','):
            if not category:
                continue
            categories_set.add(category)    

for k, v in sorted(genre_set.items(), key=lambda x: -x[1]):
    print(k, v)
        
res['categories'] = list(categories_set)
res['genres'] = list(genre_set)
# print(len(genre_set), len(categories_set))

with open('filtered.json', 'w') as wf:
    wf.write(json.dumps(res))
