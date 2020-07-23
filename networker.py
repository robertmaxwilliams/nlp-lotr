import re
import sys
from collections import defaultdict
import json
import math

text = ''
if len(sys.argv) < 4:
    print('Arguments are out_file names_file corpus1 corpus2 ...')
    quit()

out_file = sys.argv[1]
if 'json' not in out_file:
    print('outfile should be .json')
    quit()

identifiers_file = sys.argv[2]
for filename in sys.argv[3:]:
    text += open(filename).read()

names = [line.split(' : ')[0].strip() for line in open(identifiers_file).readlines()]

name_locations = []
for name in names:
    name_locations += [(name, m.start()) for m in re.finditer(name, text)]


num_locations = len(name_locations)
print('num locations:', len(name_locations))
print('num chars:', len(names))

num_rels = 0
relationships = defaultdict(float)
relationships_counts = defaultdict(float)
for (name1, location1) in name_locations:
    for (name2, location2) in name_locations:

        if (name1 == name2):
            continue
        elif (name1 < name2):
            # sum of inverse square distance as metric
            num_rels += 1
            if num_rels % 500000 == 0:
                print(num_rels, 'steps completed out of approximaely', num_locations**2)
            if location1 == location2:
                print('same location for', name1, 'and', name2, 'at', location1)
            else:
                relationships[(name1, name2)] += 1/(location1 - location2)**2
                relationships_counts[(name1, name2)] += 1

# divide by the number of times that pair appears
for key in relationships:
    relationships[key] = relationships[key] / relationships_counts[key]

print('num rels:', num_rels)

json.dump(list(relationships.items()), open(out_file, 'w'))
print('dumped to' + out_file)

# print sorted for easy evluation
for pair, rel in sorted(relationships.items(), key=lambda x: x[1], reverse=True):
    print(f'{pair} : ({rel})')
