import csv
from random import shuffle


with open("iris.data", 'r') as f:
    reader = csv.reader(f)
    data = list(reader)[:-1]


def holdout(dat, p):
    ind = list(range(1, 151))
    shuffle(ind)
    x_train = []
    x_test = []
    for i in ind[:int(p*len(ind))]:
        x_train.append(dat[i])
    for j in ind[int(p*len(ind)):]:
        x_test.append(dat[j])
    return x_train, x_test


def count_labels(dat1):
    c_setosa = 0
    c_versicolor = 0
    c_virginica = 0
    for i in range(len(dat1)):
        if dat1[i][4] == 'Iris-versicolor':
            c_versicolor += 1
        elif dat1[i][4] == 'Iris-virginica':
            c_virginica += 1
        elif dat1[i][4] == 'Iris-setosa':
            c_setosa += 1
    return [c_setosa, c_versicolor, c_virginica]


def display_info(p):
    res = holdout(data, p)
    x_train = res[0]
    x_test = res[1]
    x_tr = count_labels(x_train)
    x_te = count_labels(x_test)
    print("Train sample data in total = {} Iris-versicolor = {} , Iris-virginica = {}, Iris-setosa = {}".
          format(len(x_train), x_tr[0], x_tr[1], x_tr[2]))
    print('Top 5 rows Train_X')
    display_top_5(x_train)
    print("Test sample data in total = {} Iris-versicolor = {} , Iris-virginica = {}, Iris-setosa = {}".
          format(len(x_test), x_te[0], x_te[1], x_te[2]))
    print('Top 5 rows Test_X')
    display_top_5(x_test)


def display_top_5(dat02):
    for e in dat02[:4]:
        print("index: {:<5} row = {}".format(data.index(e), e))


display_info(0.79)  # adjust the fraction here
















