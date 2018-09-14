#!/usr/bin/python3

import sys, re, time
import matplotlib.pyplot as plt                             # graphing library
from matplotlib.ticker import MultipleLocator as tick_every # tick interval object
from getopt import gnu_getopt, GetoptError                  # command line option parser

# my own modules
from tableprinter import TablePrinter           # for printing neatly formatted tables
from csvsimple import csv_rows, csv_records     # for parsing basic CSV

#--- global constants -----------------------------------------------

csv_sep = ';'   # unusual CSV field separator is ';'

#--- command line args and file checks -------------------------------

# get the program leaf name
leafname = re.sub(r'^.*/', '', sys.argv[0])

# usage string
usage = """Usage: %s [ -v ] [ -d ] [ <infile> ]  [ <outfile> ]

    If input is not from a pipe or redirection then the first
    non-option argument will be used as the input filename.

    Optional <outfile> will be used as the base name for the
    output graphs. If not given the graphs will be displayed
    interactively instead.

    -d for "display" displays the graphs interactively even
    when you have provided an outfile for saving them on disk.

    -v for "verbose" causes more stats to be printed textually.
    You may need to widen your terminal window to see it all.
""" % leafname

# display all messages given to stderr and exit neatly
def die(*msgs):
    print('Error:', end=' ', file=sys.stderr)
    for msg in msgs:
        print(msg, file=sys.stderr)
    exit(1)

# parse the options, error if invalid
try:
    opts, args = gnu_getopt(sys.argv[1:], 'hvd')
    opts = dict(opts)       # duplicate options do not matter, so put then in a dict for speed
    verbose = '-v' in opts
    display = '-d' in opts
    if '-h' in opts:        # if -h (help) option used
        print(usage)        # print the usage message
        exit()
except GetoptError as e:
    die(e, usage)           # display usage message if options are wrong

# check we can open the input
if not sys.stdin.isatty():      # if input from a pipe
    infile = sys.stdin          # then use stdin as the input file
else:                           # but if no piped input, file must be the first argument
    if len(args) < 1:           # if there's no input file then die with usage message
        die('Needs an input file or piped input', usage)
    try:
        infile  = open(args[0]) # open the first arg as a file
        args = args[1:]         # then shift the args down so that only the outfile remains
    except OSError as e:
        die(e.strerror + (': ' + e.filename if e.filename else ''))

# get output path if given, path will be used as a base name for the graphs
if len(args) == 1:
    outpath = args[0]
else:
    outpath = None
if len(args) > 1:
    die('Too many args', usage)

def lc(s): return s.lower()     # lowercase mapping function used for the field names

#--- main processing loop -------------------------------------------

rec_count = 0                       # count of all records in the CSV file
good_count = 0                      # count of good records in the CSV file
data = {}                           # dict of states where each value is
                                    #   a dict record of min, max, sum, num, avg

start = time.time()                 # start timing the CSV reading/parsing
csv = csv_rows(infile, sep=csv_sep) # start the CSV row parser
fields = list(map(lc, next(csv)))   # read lowercase field names from 1st row

print('\nReading CSV file...', end=' ', flush=True) # flush to make it visible immediately
for rec in csv_records(csv, fields):    # get each line of CSV parsed into a dict
    rec_count += 1                  # count the total number of records
    if not rec['state']: continue   # ignore data with no state (airports)
    good_count += 1                 # count the good records we can use

    state = rec['statename']        # get state name from this line record
    if state in data:               # if state is already in our data
        st = data[state]            # then get existing state record
    else:                           # else
        st = {                      # add a new state record to the data
            'state': state,
            'min': rec['mintemp'],
            'max': rec['maxtemp'],
            'sum': 0,               # to sum the averages (and later divide by the num)
            'num': 0,               # to count the number of avg samples
        }

    # keep track of the min and max temperature for each state
    if rec['mintemp'] < st['min']: st['min'] = rec['mintemp']
    if rec['maxtemp'] > st['max']: st['max'] = rec['maxtemp']

    # also sum and count average temperature
    st['sum'] += rec['avgtemp'] # sum
    st['num'] += 1              # count
    data[state] = st    # store updated state record back into the data

# finished reading CSV file, so report how long it took
time_csv = time.time() - start
print('took %.2f seconds' % time_csv, flush=True)

if not data: die('No data at all found in the input')

# report what we found in the CSV file
print('Found {:,} records of {} fields with '
        'data for {} states'.format(rec_count, len(fields), len(data)))
print('but ignored %d stateless records (airports)'
                                    % (rec_count - good_count))

#--- calculations ------------------------------------------------

start = time.time()
print('\nCalculating...', end=' ', flush=True)

# calculate the average temperatures for each state
for st in data.values():
    st['avg'] = st['sum'] / st['num']
    del st['sum']   # remove the sum as we no longer need it

# convert fahrenheit temperatures to celsius
for st in data.values():
    for k in ('min', 'max', 'avg'):
        st[k] = (st[k]-32)*5/9

# find the temperature range of each state
for st in data.values():
    st['range'] = st['max'] - st['min']

# get the records sorted in various different orders
st_asc   = sorted(data.values(), key=lambda rec: rec['state'])
max_asc  = sorted(data.values(), key=lambda rec: rec['max'])
max_desc = sorted(data.values(), key=lambda rec: rec['max'], reverse=True)
min_asc  = sorted(data.values(), key=lambda rec: rec['min'])
avg_asc  = sorted(data.values(), key=lambda rec: rec['avg'])
rng_asc  = sorted(data.values(), key=lambda rec: rec['range'])
rng_desc = sorted(data.values(), key=lambda rec: rec['range'], reverse=True)
# I did not use all these orders in the end

# get some overall stats (min, max, avg of all)
max_of_max = max_desc[0]['max']
min_of_min = min_asc[0]['min']
avg_of_avg = sum(st['avg'] for st in data.values()) / len(data)

# report how long all the calculations took
time_calc = time.time() - start
print('took %.4f seconds' % time_calc, flush=True)

#--- results ------------------------------------------------

# use TablePrinter with row numbering enabled
tp = TablePrinter().num(1)

# set the formats for all floating ponit numbers to two decimal places
tp.forms({ f: '.2f' for f in ('min', 'max', 'avg', 'range') })

# if the verbose option was used print lots more tables of stats
if verbose:
    tp.indent('  ').sep('  ').parts(3) # in 3 parts
    print('\nAll states by max temperature:\n')
    tp.fields(['state', 'max']).print(max_desc)

    print('\nAll states by min temperature:\n')
    tp.sep(' ') # closer parts using one space
    tp.fields(['state', 'min']).print(min_asc)

    print('\nAll states by avg temperature:\n')
    tp.sep('  ') # back to two spaces
    tp.fields(['state', 'avg']).print(avg_asc)

    tp.parts(2) # in two parts because the table is wider
    print('\nAll states by temperature range (biggest first):\n')
    tp.fields(['state', 'min', 'max', 'range']).print(rng_desc)

# regardless of verbose option print the tables requested by the assignment
tp.indent('    ').parts(2)  # in two parts
print('\nTen highest max temperature states:\n')
tp.fields(['state', 'max']).print(max_desc[:10])

print('\nTen lowest min temperature states:\n')
tp.fields(['state', 'min']).print(min_asc[:10])

if verbose:
    print('\nExtra statistics were printed, so you may need to scroll up to see.')

print()

#--- graphs -------------------------------------------------

# four graphs are similar, so put it all in a function that we call 4 times
# args: data is the list of records to use
#       sort is a string describing the sort order which is used as part of the file name
#       title is the title for the graph
def state_graph(data, sort, title):
    # create the "figure" with the size in inches and the resolution in dpi (dots per inch)
    fig = plt.figure(figsize=(12,6), dpi=100)
    # create the graph (axes object) within the figure using these margin sizes
    ax = fig.add_axes((0.05, 0.21, 0.92, 0.73)) # (left, bottom, width, height)
    ax.set_title(title)
    ax.bar([ rec['state'] for rec in data ],    # plot bars of states
            [ rec['max'] for rec in data ],     # against the max temp
            label='max', color='red')           # red bars, "max" in legend
    ax.bar([ rec['state'] for rec in data ],    # plot bars of states
            [ rec['min'] for rec in data ],     # against min temp
            label='min', color='blue')          # blue bars, "min" in legend
    ax.plot([ rec['state'] for rec in data ],   # plot diamons for states
            [ rec['avg'] for rec in data ],     # against the average temp
            # use avg in the legend, light green, diamonds, with no linestyle (ls)
            label='avg', color='lightgreen', ls='', marker='D', markersize=6)
    # put the state names at angle -90 in a small font
    ax.tick_params(axis='x', labelsize='small', rotation=-90)
    # limit the x scale so that the bars fill the available space neatly
    ax.set_xlim(-0.5, len(data)-0.5)
    # change the rotation and label of the y axis
    ax.set_ylabel('Celsius', rotation=-90)
    # default tick spacing too big so set it every 10 degrees celsius
    ax.yaxis.set_major_locator(tick_every(10))
    # turn on the grid as a dotted line
    ax.grid(linestyle=':')
    # place the legend in the upper center with a drop shadow
    ax.legend(loc='upper center', shadow=True)
    # the graph will be shown on screen interactively if no output path given
    # or if the -d display option was used
    if display or not outpath:
        plt.show()
    # if there is an outpath then save the graph, and say where it is being saved
    if outpath:
        filename = outpath + '_' + sort + '.png'
        print('Saving graph "' + title + '" to ' + filename)
        fig.savefig(filename)

# graph title reminds us how many states were in this data set
title = 'Temperatures for %d states - sorted by ' % len(data)

state_graph(max_asc, 'max', title + 'max')      # sorted by max
state_graph(min_asc, 'min', title + 'min')      # sorted by min
state_graph(avg_asc, 'avg', title + 'avg')      # sorted by avg
state_graph(rng_asc, 'rng', title + 'range')    # sorted by range
print('Finished')
