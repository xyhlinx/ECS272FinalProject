import pandas as pd
import csv
import json


dset = pd.read_csv('./data/games.csv', encoding='latin1')
df = pd.DataFrame(dset)
print(df[['Genres', 'Categories']].to_csv('tmp.csv'))

genre_set = set()
categories_set = set()
res = {}

with open('tmp.csv') as rf:
    reader = csv.reader(rf)
    for r in reader:
        _id, gs, cs = r
        print(cs)
        for g in gs.split(','):
            if not g:
                continue
            genre_set.add(g)

        for category in cs.split(','):
            if not category:
                continue
            categories_set.add(category)

        
res['categories'] = list(categories_set)
res['genres'] = list(genre_set)
print(len(genre_set), len(categories_set))

with open('filtered.json', 'w') as wf:
    wf.write(json.dumps(res))
