#!/usr/bin/python3

from math import ceil

dat = [ 87, 51, 56, 59, 90, 67, 74, 96, 73, 80,
        92, 68, 92, 79, 95, 68, 87, 93, 91, 80,
        65, 92, 77, 94, 89, 74, 96, 85, 93, 72,
        49, 79, 65, 62, 70, 76, 87, 74, 63, 94,
        86, 86, 69, 88, 89, 97, 91, 54, 83, 73 ]

minv = min(dat)         # find minimum value
maxv = max(dat)         # find maximum value
rang = maxv - minv      # calc range
itvl = ceil(rang / 10)  # calc interval width to make 10 fit (with discrete values)
# display the calculation used
print(maxv, "-", minv, "=", rang, "so itvl =", rang / 10, "rounded up to", itvl)

# calc and display the boundaries
bnds = list(x-0.5 for x in range(minv,maxv+itvl,itvl))
print("so bounds are", bnds)
print()

# count the frequencies of the data for each interval
freq = [ 0 for x in range(10) ]
for v in dat:
    for i in range(len(bnds)-1):
        if v < bnds[i+1]:
            freq[i] += 1
            break

# display the frequency table
tot = len(dat)
cum = 0
relcum = 0
print(" Row   Limits   Boundaries  Freq Cum  More RelFreq CumRel  MoreRel ")
print("+----+--------+------------+----+----+----+-------+-------+-------+")
for i in range(len(bnds)-1):
    low = round(bnds[i] + 0.5)
    high = round(bnds[i+1] - 0.5)
    cum += freq[i]
    rel = freq[i] / tot
    relcum += rel
    more = tot - cum + freq[i]
    relmore = 1 - relcum + rel
    print("| %2d | %2d--%2d | %4.1f--%4.1f | %2d | %2d | %2d | %5.3f | %5.3f | %5.3f |"
        % (i+1, low, high, bnds[i], bnds[i+1], freq[i], cum, more, rel, relcum, relmore))

print("+----+--------+------------+----+----+----+-------+-------+-------+")
