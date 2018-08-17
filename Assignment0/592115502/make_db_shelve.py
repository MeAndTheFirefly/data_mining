from initdata import data
import shelve
db = shelve.open('weather-shelve.dat')
db['set01'] = data
db.close()


