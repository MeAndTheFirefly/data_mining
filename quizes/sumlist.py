import random
import time
import sys

sys.setrecursionlimit(10**6)


def sum_list(lis):
    sum_tot = 0
    for num in lis:
        sum_tot += num
    return sum_tot


def sum_recur(n):
    if len(n) == 0:
        return 0
    else:
        return n[0] + sum_recur(n[1:])


def get_rand_num(range_num):
    res = []
    for _ in range(range_num):
        res.append(random.randint(1, 100))
    return res


if __name__ == '__main__':
    data = [get_rand_num(10), get_rand_num(100), get_rand_num(1000), get_rand_num(10000)]
    for arr in data:

        start_time = time.time()
        print("{:>6} Iteration {:>8}: time executed: {:.8f} seconds".
              format(sum_list(arr), len(arr), float(time.time() - start_time)))

        print("{:>6} Recursion {:>8}: time executed: {:.8f} seconds ".
              format(sum_recur(arr), len(arr), float(time.time() - start_time)))











