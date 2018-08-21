data = \
[87, 51, 56, 59, 90, 67, 74, 96, 73, 80,
 92, 68, 92, 79, 95, 68, 87, 93, 91, 80,
 65, 92, 77, 94, 89, 74, 96, 85, 93, 72,
 49, 79, 65, 62, 70, 76, 87, 74, 63, 94,
 86, 86, 69, 88, 89, 97, 91, 54, 83, 73]


def make_class(low, c, width):
    res = []
    i = 0
    while i < c:
        upper = low + width - 1
        res.append([low, upper])
        low = upper + 1
        i += 1
    return res


def count_frequency(li, min_n, max_n):
    ctr = 0
    for x in li:
        if min_n <= x <= max_n:
            ctr += 1
    return ctr


def count_freq_in_range(class_lim):
    res = []
    for elem in class_lim:
        res.append(count_frequency(data, elem[0], elem[1]))
    return res


def cal_le_th(fre):
    init = 0
    res = []
    for e in fre:
        init += e
        res.append(init)
    return res


def cal_mo_th(fre):
    init = 0
    length = len(data)
    res = []
    for e in fre:
        length -= init
        res.append(length)
        init = e
    return res


def display_frequency_table(low, c, width):
    tot = len(data)
    class_lim = make_class(low, c, width)
    fomat_class = ['{} - {}'.format(e[0], e[1]) for e in class_lim]

    class_bds = [[e[0] - 0.5, e[1] + 0.5] for e in class_lim]
    fomat_bds = ['{} - {}'.format(e[0], e[1]) for e in class_bds]
    fre_count = count_freq_in_range(class_lim)
    rela_fre  = [e/tot for e in fre_count]
    re_les_th = cal_le_th(fre_count)
    re_mo_th = cal_mo_th(fre_count)
    cu_les_th = [e / tot for e in re_les_th]
    cu_mo_th = [e / tot for e in re_mo_th]
    print("  Limit      Bds        Freq   RelFre  re_les   re_mo_th   cu_les_th  cu_mo_th ")
    print("+----------+----------+------+--------+--------+---------+-----------+---------")
    for i in range(len(class_bds)):
        print('{:>9} {:>19}'.format(fomat_class[i], fomat_bds[i]))


display_frequency_table(min(data), 5, 10)














