import csv
from random import shuffle

with open("iris.data", 'r') as f:
    res_dat = {}
    reader = csv.reader(f)
    data = list(reader)
    cla = []
    for i in range(1, len(data) - 1):
        label = data[i][4]
        dat_row = list(map(float, data[i][:4]))
        if label not in cla:
            cla.append(label)
            res_dat[label] = [dat_row]
        else:
            new_val = res_dat[label].append(dat_row)


def holdout(dict_dat, p):
    train_dat = []
    test_dat = []
    tra_c = {}
    te_c = {}
    for e in cla:
        res = chop_data(dict_dat[e], p)
        tra_c[e] = len(res[0])
        te_c[e] = len(res[1])
        train_dat += res[0]
        test_dat += res[1]
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


def display_info():
    res = holdout(res_dat, 0.8)
    train = res[0]
    test = res[1]
    tra_c = res[2]
    te_c = res[3]
    print(tra_c)
    print("Train sample data in total = {} {}".
          format(len(train), tra_c))
    print('Top 5 rows Train_Y')
    display_top_5(train)
    print("Test sample data in total = {} {}".
          format(len(test), te_c))
    print('Top 5 rows Test_Y')
    display_top_5(test)


def display_top_5(dat02):
    for e in dat02[:4]:
        print(e)


display_info()










