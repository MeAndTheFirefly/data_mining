#!/usr/bin/python3

import sys, re
from math import ceil

#--- global constants ------------------------------------------------

minv = -9   # min valid value (is "outlier" if outside this range)
maxv = 99   # max valid value
mps = 3     # months per season (change it for fun)

#--- inputs ------------------------------------------------

try:
    infile = sys.argv[1]
except IndexError:
    print("Expects one argument, the data file to process")
    exit(1)

data = []
try:
    for line in open(infile):
        line = re.sub(r'#.*', "", line) # strip comments
        line = re.sub(r',', " ", line)  # allow comma separators
        parts = line.split()            # get separate non-space parts
        if not parts: continue          # ignore lines with no data
        data.append(list(map(float, parts)))    # as list of floats
except ValueError as e:
    print("Bad value: "+str(e))
    exit(1)
except OSError as e:
    print(e.strerror + ": " + e.filename)
    exit(1)

if not data:
    print("No data at all found in file %s" % infile)
    exit(1)

#--- calculations ------------------------------------------------

# functions to check if value is good (valid) or bad (outlier)
def good(v): return v >= minv and v <= maxv
def bad(v):  return v < minv or v > maxv

# function to average a non-empty numeric sequence
def avg(seq): return sum(seq)/len(seq)

# get only good data with outliers removed, tupled with row number
goodrows = [ t for t in enumerate(
                list(filter(good, row)) for row in data
                ) if t[1] ]

# abort if there is no valid data at all
if not goodrows:
    print("No good valid data found in file %s" % infile)
    exit(1)

# now we know there is at least one good data value
# so there will also be at least one good season

# dicts for calulated avg, min, max of each good row
rowavgs = { i: avg(row) for (i, row) in goodrows }
rowmins = { i: min(row) for (i, row) in goodrows }
rowmaxs = { i: max(row) for (i, row) in goodrows }

# number of seasons with any data at all
snum = ceil(max(map(len, data)) / mps)

# extract only the good data for each season
seasons = []
for s in range(snum):
    seasons.append([])
    for row in data:
        vals = row[s*mps:(s+1)*mps]             # mps constant set at top
        seasons[s].extend(filter(good, vals))   # only the good values

# some (not all) seasons may be empty because there was no good data
# make a list of the good seasons, tupled with the season number
goodseas = [ t for t in enumerate(seasons) if t[1] ]

# calc avg, min, max of each good season and store in dicts
seaavgs = { i: avg(s) for (i, s) in goodseas }
seamins = { i: min(s) for (i, s) in goodseas }
seamaxs = { i: max(s) for (i, s) in goodseas }

# get good season numbers in descending order of the average
# (we already know there will be at least one season in this order)
order = [ tup[0] for tup in sorted(seaavgs.items(),
            key=lambda t: t[1], reverse=True) ]

# we needed that decending order anyway,
# and now we can get the min/max seasons for free
minavg = order[-1]  # season with the lowest average
maxavg = order[0]   # season with the highest average

# count outliers in the data
outliers = sum(len(list(filter(bad, row))) for row in data)

#--- results ------------------------------------------------

print("\nCity average, min, and max:")
for i in range(len(data)):
    if i in rowavgs:
        print("City %2d: avg %5.2f, min %2d, max %2d"
                % (i+1, rowavgs[i], rowmins[i], rowmaxs[i]))
    else:
        print("City %2d: --- no good data ---" % (i+1))

print("\nSeason average, min, and max:")
for i in range(snum):
    if i in seaavgs:
        print("Season %d: avg %5.2f, min %2d, max %2d"
                % (i+1, seaavgs[i], seamins[i], seamaxs[i]))
    else:
        print("Season %d: --- no good data ---" % (i+1))

print("\nSeason avg extremes:")
print("Min avg is season %d" % (minavg+1))
print("Max avg is season %d" % (maxavg+1))

print("\nSeasons in decending order of avgerage:")
print(" > ".join([ "Season %d" % (s+1) for s in order ]))

if outliers: print("\nThere were %d outliers" % outliers)
print()
