import re
import sys
from collections import defaultdict
import json

text = ''
if len(sys.argv) < 5:
    print('Arguments are out_file names_file places_file corpus1 corpus2 ...')
    quit()

out_file = sys.argv[1]
if 'json' not in out_file:
    print('outfile should be .json')
    quit()

names_file = sys.argv[2]
places_file = sys.argv[3]
for filename in sys.argv[4:]:
    text += open(filename).read()

names = [line.split(' : ')[0].strip() for line in open(names_file).readlines()]
places = [line.split(' : ')[0].strip() for line in open(places_file).readlines()]

name_locations = []
for name in names:
    name_locations += [(name, m.start()) for m in re.finditer(name, text)]

place_locations = []
for place in places:
    place_locations += [(place, m.start()) for m in re.finditer(place, text)]


num_names_found = len(name_locations)
num_places_found = len(place_locations)
print('num name instances found:', num_names_found)
print('num place instances found:', num_places_found)

num_rels = 0
relationships = defaultdict(float)
relationships_counts = defaultdict(float)
for (name, name_loc) in name_locations:
    for (place, place_loc) in place_locations:
        # sum of inverse square distance as metric
        num_rels += 1
        if num_rels % 500000 == 0:
            print(num_rels, 'steps completed out of approximaely', num_names_found * num_places_found)
        if name_loc == place_loc:
            print('same location for', name, 'and', place, 'at', name_loc)
            relationships[(name, place)] += 1
            relationships_counts[(name, place)] += 1
        else:
            relationships[(name, place)] += 1/(name_loc - place_loc)**2
            relationships_counts[(name, place)] += 1

# divide by the number of times that pair appears
for key in relationships:
    relationships[key] = relationships[key] / relationships_counts[key]


print('num rels:', num_rels)

json.dump(list(relationships.items()), open(out_file, 'w'))
print('dumped to' + out_file)

# print sorted for easy evluation
for pair, rel in sorted(relationships.items(), key=lambda x: x[1], reverse=True):
    print(f'{pair} : ({rel})')
