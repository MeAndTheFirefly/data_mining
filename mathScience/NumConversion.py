
def baby_num(baby_symbol):   # use coma to separate each column.
    token = baby_symbol.split(' ')
    tot = 0
    for i in range(len(token)):
        tot += (count_occur('v', token[i]) + count_occur('<', token[i])*10)*(60**(len(token) - (i+1)))
    print(baby_symbol, "=>", tot)


def count_occur(symbol, sentence):
    return sentence.count(symbol)


def mayan_to_num(numb):   # put the from top to bottom
    tot = 0
    token = numb.split()
    col_size = len(token)
    tot += int(token[col_size - 1]) + int(token[col_size - 2])*20
    for i in range(col_size - 2):
        tot += int(token[i])*(18*(20**(col_size - 2)))
    print(numb, '=>', tot)


baby_num('vv <v <<vv')
baby_num('v < vv')

mayan_to_num('14 0 7 12')
mayan_to_num('0 0 7 12')
mayan_to_num('1 1 1')
