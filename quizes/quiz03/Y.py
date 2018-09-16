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
    print("Train sample data in total = {} {}\n".
          format(count_tot_sample(train), tra_c))
    print('Top 5 rows Train_X\n')
    display_top_5(train)
    print("test sample data in total = {} {}\n".
          format(count_tot_sample(test), te_c))
    print('Top 5 rows Test_X\n')
    display_top_5(test)


def display_top_5(dict0):
    keys = list(dict0.keys())
    inx = list(range(len(keys)))
    c = 0
    while c < 5:
        print("index: {:>3} {:>4} {:<10}\n".format
              (res_dat[keys[inx[c % 3]]].index(dict0[keys[inx[c % 3]]][c]), keys[inx[c % 3]],
               ' '.join(str(e) for e in dict0[keys[inx[c % 3]]][c])))
        c += 1


def count_tot_sample(dict1):
    tot_sample = 0
    for key in dict1:
        tot_sample += len(dict1[key])
    return tot_sample


display_info(0.773)  # adjust the fraction here










