#!/usr/bin/python3
import csv
import time
import matplotlib.pyplot as plt
import gmplot
import sys
start_time = time.time()
try:
    datafile = sys.argv[1]
except IndexError:
    print("expecting two arguments")
    exit(1)

print("*Parsing data file...")
with open(datafile, 'r') as f:
    reader = csv.reader(f)
    data = list(reader)
stat_nam = []
pro_max = {}
pro_min = {}
state = []
for i in range(1, len(data)):
        row = ''.join(data[i]).split(';')
        name = row[8]
        maxv = (float(row[6])-32)*5/9
        minv = (float(row[7])-32)*5/9
        lon = float(row[2])
        lat = float(row[3])
        st = row[10]
        if name in stat_nam:
            if maxv > pro_max[name][0]:
                pro_max[name] = [maxv, lon, lat]
            if minv < pro_min[name][0]:
                pro_min[name] = [minv, lon, lat]
        else:
            if name != '"0"':
                stat_nam.append(name)
                state.append(st)
                pro_max[name] = [maxv, lon, lat]
                pro_min[name] = [minv, lon, lat]

print('**Total samples parsed = {} '.format(len(data)))
print('**Total columns parsed = {}'.format(len(''.join(data[0]).split(';'))))
print('**Total time parsing data file from CSV format = {:.8f} seconds'.format(time.time() - start_time))
print('Generating information....')
print('Total states = {}'.format(len(set(state))-1))  # strip off the coma at the end


max_v = [(nam, pro_max[nam][0]) for nam in sorted(pro_max, key=pro_max.get, reverse=True)]
min_v = [(nam, pro_min[nam][0]) for nam in sorted(pro_min, key=pro_min.get)]
max_by_state = sorted(max_v, key=lambda x: x[0])  # sort temp by state name - alphabetic order
min_by_state = sorted(min_v, key=lambda x: x[0])
Location = [(e[1], e[2]) for e in pro_max.values()]  # Locations of all highest temperature across America

max_ten = max_v[:10]
min_ten = min_v[:10]


def display_info(t_arr):
    print('       State Name            Temperature')
    print('+----------------------------------------+')
    for k in range(len(t_arr)):
        print('{:>2} {:>15} {:>18.2f} \u00b0c'.format(k + 1, t_arr[k][0].strip('"'), t_arr[k][1]))
    print('\n')


def draw_heat_map(locat):
    gmap = gmplot.GoogleMapPlotter(locat[0][0], locat[0][1], 4)
    lats, lons = zip(*Location)
    gmap.heatmap(lats, lons)
    gmap.draw("./images/heat_map.html")


def plot_bar_chart(lis, la_x, la_y, f_name, title):
    plt.xlabel(la_x)
    plt.xticks(rotation='vertical', fontsize=8)
    plt.ylabel(la_y)
    plt.title(title)
    x = []
    y = []
    for e in lis:
        x.append(e[0].strip('"'))
        y.append(e[1])
    plt.bar(x, y)
    plt.tight_layout()
    plt.savefig('./images/{}.png'.format(f_name))
    plt.show()


display_info(max_ten)
display_info(min_ten)
plot_bar_chart(max_by_state, 'State Name', 'Max Temp in \u00b0c', 'States_max_temp',
               'Max temperature of each state in the US')
plot_bar_chart(min_by_state, 'State Name', 'Min Temp in \u00b0c', 'States_min_temp',
               'Min temperature of each state in the US')
draw_heat_map(Location)
print('**Total time of getting all outputs = {:.8f} seconds'.format(time.time() - start_time))




















