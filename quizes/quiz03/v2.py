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


def get_output(p):
    res = holdout(data, p)
    train = res[0]
    test = res[1]
    x_tr = count_labels(train)
    x_te = count_labels(test)
    print("Train sample data in total = {} Iris-versicolor = {} , Iris-virginica = {}, Iris-setosa = {}".
          format(len(train), x_tr[0], x_tr[1], x_tr[2]))
    print('Top 5 rows Train_X')
    display_top_5_x(train)
    print('Top 5 row Train_Y')
    display_top_5_y(train)

    print("Test sample data in total = {} Iris-versicolor = {} , Iris-virginica = {}, Iris-setosa = {}".
          format(len(test), x_te[0], x_te[1], x_te[2]))
    print('Top 5 rows Test_X')
    display_top_5_x(test)

    print('Top 5 rows Test_Y')
    display_top_5_y(test)


def display_top_5_x(dat02):
    for e in dat02[:4]:
        print("index: {:<5} {}".format(data.index(e), e[:4]))


def display_top_5_y(dat03):
    for e in dat03[:4]:
        print("index: {:<5} {}".format(data.index(e), e[-1]))


get_output(0.83)  # please adjust the fraction here