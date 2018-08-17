import shelve
db = shelve.open('weather-shelve.dat')


def cal_year_avg(key):
    return [a/12 for a in list(map(sum, db[key]))]


def cal_ses_avg(key):
    return [sum(ses) / 3 for ses in chop_seasons(key)]


def find_max_ses(key):
    return [max(ses) for ses in chop_seasons(key)]


def find_min_ses(key):
    return [min(ses) for ses in chop_seasons(key)]


def find_avg_across_all_city(key):
    season_avg = cal_ses_avg(key)
    i = 0
    res = []
    while i < len(season_avg):
        res.append(season_avg[i:i + 4])
        i += 4

    return [sum(col) / len(col) for col in list(zip(*res))]


def order_ses_avg(key):
    res = []
    avg_temp = [sum(ses) / 3 for ses in chop_seasons(key)]
    i = 0
    while i < len(avg_temp):
        res += (sorted(avg_temp[i:i+4], reverse=True))
        i += 4
    return res


def chop_seasons(key):
    season = [slice(0, 3), slice(3, 6), slice(6, 9), slice(9, 12)]
    res = []
    for data in db[key]:
        for each_ses in season:
            res.append(data[each_ses])
    return res


def display_yearly_avg(key):
    year_avg = cal_year_avg(key)
    for i in range(len(year_avg)): print('City {:>2}  Temp AVG = {}'.format(i + 1, year_avg[i]))


def display_season_avg(key):
    season_avg = cal_ses_avg(key)
    city_counter = 1
    ses_counter = 1
    for i in range(len(season_avg)):
        print('City {:>2} season {} Temp AVG: = {} '.format(city_counter, ses_counter, season_avg[i]))
        ses_counter += 1
        if (i + 1) % 4 == 0:
            city_counter += 1
            ses_counter = 1


def display_max_temp(key):
    city_counter = 1
    ses_counter = 1
    res = find_max_ses(key)
    for i in range(len(res)):
        print('City {:>2} Season {} Max = {}'.format(city_counter, ses_counter, res[i]))
        ses_counter += 1
        if (i+1) % 4 == 0:
            city_counter += 1
            ses_counter = 1


def display_min_temp(key):
    city_counter = 1
    ses_counter = 1
    res = find_min_ses(key)
    for i in range(len(res)):
        print('City {:>2} Season {} Min = {}'.format(city_counter, ses_counter, res[i]))
        ses_counter += 1
        if (i + 1) % 4 == 0:
            city_counter += 1
            ses_counter = 1


def display_ses_avg_across_city(key):
    avg_res = find_avg_across_all_city(key)
    ses_counter = 1
    for i in range(len(avg_res)):
        print(("Average across all city in season {} AVG = {}".format(ses_counter, avg_res[i])))
        ses_counter += 1

    print("Max = Season {}".format(avg_res.index(max(avg_res))+1))
    print("Min = Season {}".format(avg_res.index(min(avg_res)) + 1))


def display_ses_des_order_all_city(key):
    avg_res = find_avg_across_all_city(key)
    sorted_res = sorted(avg_res, reverse=True)
    for temp in sorted_res:
        print(("season {} {}".format(avg_res.index(temp) + 1, '> ')), end='')


def display_des_order(key):
    city_counter = 1
    ses_counter = 1
    res = order_ses_avg(key)
    for i in range(len(res)):
        print(("{:>19} {:>3}".format(res[i], '>')), end='')
        ses_counter += 1
        if (i + 1) % 4 == 0:
            city_counter += 1
            ses_counter = 1
            print('\n')


if __name__ == '__main__':
    display_yearly_avg('set01')
    print('\n')
    display_ses_avg_across_city('set01')
    print('\n')
    display_ses_des_order_all_city('set01')
    print('\n')
    display_season_avg('set01')
    print('\n')
    display_max_temp('set01')
    print('\n')
    display_min_temp('set01')
    print('\n')
    display_des_order('set01')

db.close()
