import csv
from random import shuffle, randint

with open("iris.data", 'r') as f:
    res_dat = {}
    reader = csv.reader(f)
    data = list(reader)
    cla = []
    for i in range(1, len(data) - 1):
        label = data[i][4]
        dat_row = list(map(float, data[i][:4]))
        dat_row.append(i)   # append the index of each record
        if label not in cla:
            cla.append(label)
            res_dat[label] = [dat_row]
        else:
            new_val = res_dat[label].append(dat_row)


def holdout(dict_dat, p):
    train_dat = {}
    test_dat = {}
    tra_c = {}
    te_c = {}
    for e in cla:
        res = chop_data(dict_dat[e], p)
        tra_c[e] = len(res[0])
        te_c[e] = len(res[1])
        if e in train_dat.keys():
            train_dat[e].append(res[0])
            test_dat[e].append(res[1])
        else:
            train_dat[e] = res[0]
            test_dat[e] = res[1]
    return train_dat, test_dat, tra_c, te_c


def chop_data(dat1, p):
    train = []
    test = []
    ind = list(range(0, len(dat1)))
    shuffle(ind)
    for k in ind[:int(p*len(ind))]:
        train.append(dat1[k])
    for j in ind[int(p*len(ind)):]:
        test.append(dat1[j])
    return train, test


def display_info(p):
    res = holdout(res_dat, p)
    train = res[0]
    test = res[1]
    tra_c = res[2]
    te_c = res[3]
    print("Total train sample = {} {}".
          format(count_tot_sample(train), tra_c))
    print('\n')
    print('Top 5 rows Train_X\n')
    train_set = top_5(train)
    display_x(train_set)
    print('\n')
    print('Top 5 rows Train_Y\n')
    display_y(train_set)

    print('\n')
    print("Total test sample = {} {}\n".
          format(count_tot_sample(test), te_c))

    test_set = top_5(test)

    print('Top 5 rows Test_X\n')
    display_x(test_set)
    print('\n')
    print('Top 5 rows Test_Y\n')
    display_y(test_set)


def display_x(tup):
    for e in tup:
        print("index: {}, {}".format(e[0][-1], e[0][:4]))


def display_y(tup):
    for e in tup:
        print("index: {}, {}".format(e[0][-1], e[1]))


def top_5(dict0):
    keys = list(dict0.keys())  # get the list of keys (Ys)
    c = 0
    res = []
    while c < 5:
        rad = randint(0, len(keys) - 1)  # get random index of keys
        y = keys[rad]
        x = dict0[y][c]
        res.append((x, y))
        c += 1
    return res


def count_tot_sample(dict1):
    tot_sample = 0
    for key in dict1:
        tot_sample += len(dict1[key])
    return tot_sample


display_info(0.7)  # adjust the fraction here










