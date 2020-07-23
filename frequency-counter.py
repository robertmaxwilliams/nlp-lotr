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
if '.csv' not in out_file:
    print('outfile should be .csv')
    quit()

identifiers_file = sys.argv[2]

for filename in sys.argv[3:]:
    text += open(filename).read()

names = [line.split(' : ')[0].strip() for line in open(identifiers_file).readlines()]

name_counts = defaultdict(int)
for name in names:
    name_counts[name] += len([(name, m.start()) for m in re.finditer(name, text)])

out_lines = []
for (name, count) in name_counts.items():
    out_lines += f'{name},{count}\n'

open(out_file, 'w').write(''.join(out_lines))


