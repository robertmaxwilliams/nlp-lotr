
Process:

First, the texts were copied from these three pages:

<http://ae-lib.org.ua/texts-c/tolkien__the_lord_of_the_rings_1__en.htm>

<http://ae-lib.org.ua/texts-c/tolkien__the_lord_of_the_rings_2__en.htm>

<http://ae-lib.org.ua/texts-c/tolkien__the_lord_of_the_rings_3__en.htm>

Then, `name-finder.py` is ran on all three;

`python3 name-finder.py lotr1.txt lotr2.txt lotr3.txt > names.txt`

A lot of these names were places, and many were of little importance or were not proper nouns at
all, so only the first 39 names and 27 places were kept, in `names-edited.txt` and
`places-edited.txt`. 

Next, we find the relationship strength between each pair of words. 
To do this, each pair of names adds 1/k^2 to the relationship between those two characters, where k is
the distance (in words) between those two appearances of those names.  This takes n^2 times, where n
is the number of times that each of the 39 names appears. This works out to 7,926,854 steps we have
to do, just for book one. Adding two more books will take 9 times longer, which should still
terminate in a few minutes of time.


```
python3 networker.py place-relationship.json places-edited.txt lotr1.txt lotr2.txt lotr3.txt
python3 networker.py name-relationship.json names-edited.txt lotr1.txt lotr2.txt lotr3.txt
```

The output goes to `name-relationship.json` as a list of items like the following:

`[["Frodo", "Sam"], 0.6032697649825776]`

And `place-relationship` is about the same.

A similar program, `name-place-joiner.py` does the same but for (name, place) pairs.

```
python3 name-place-joiner.py name-place-relationship.json names-edited.txt places-edited.txt lotr1.txt lotr2.txt lotr3.txt
```

Which produces `name-place-relationship.json` which is a list of items like the following:

`[["Frodo", "Shire"], 0.08242872238132659]`

with the name, then the place. 


The next step is to convert these into a format that neo4j can read. CSV is the easiest. I made
`json-to-csv.py` to do this. Making them csv to begin with might have been smarter but that's okay.

```
python3 json-to-csv.py name-place-relationship.json > name-place.csv
python3 json-to-csv.py name-relationship.json  > name-name.csv
python3 json-to-csv.py place-relationship.json   > place-place.csv
```

We also want the counts of each character and places appearance:

```
python frequency-counter.py names.csv names-edited.txt lotr1.txt lotr2.txt lotr3.txt
python frequency-counter.py places.csv places-edited.txt lotr1.txt lotr2.txt lotr3.txt
```

Now copy all of these csv files into the import directory and fire up a database.

```
LOAD CSV FROM 'file:///names.csv' AS line
MERGE (a:Person {name: line[0], frequency: toInteger(line[1])});

LOAD CSV FROM 'file:///places.csv' AS line
MERGE (a:Place {name: line[0], frequency: toInteger(line[1])});

LOAD CSV FROM 'file:///name-name.csv' AS line
MATCH (a:Person { name: line[0] })
MATCH (b:Person { name: line[1]})
MERGE (a)-[:EDGE { weight: toFloat(line[2]) }]->(b);

LOAD CSV FROM 'file:///name-place.csv' AS line
MATCH (a:Person { name: line[0] })
MATCH (b:Place { name: line[1]})
MERGE (a)-[:EDGE { weight: toFloat(line[2]) }]->(b);

LOAD CSV FROM 'file:///place-place.csv' AS line
MATCH (a:Place { name: line[0] })
MATCH (b:Place { name: line[1]})
MERGE (a)-[:EDGE { weight: toFloat(line[2]) }]->(b);

match ()-[e:EDGE]->()
set e.log_weight = log(e.weight)
```

Now we can start visualizing this thing.

This is hard because the graph is completely connected, so we have to filter which relationships we
show.

```
match (a:Person)-[e:EDGE]->(b:Person)
where a.frequency > 20
return a, e, b 
order by e.weight DESC
limit 30

