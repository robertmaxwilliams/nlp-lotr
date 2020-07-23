import json
import sys

in_file = sys.argv[1]

assert '.json' in in_file

relationships = json.load(open(in_file))


lines = []

for ((thing1, thing2), relatedness) in relationships:
    lines.append(f'{thing1},{thing2},{relatedness}\n')

print(''.join(lines))
