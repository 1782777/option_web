from volume import volume
from ETFprice import ETFPrice
from option_info import option
from iv_mean import iv_mean get_QVIX
from stock import stork_volume
import time

if __name__ == '__main__':
    volume()
    ETFPrice()
    option()
    get_QVIX()
    stork_volume()
    while True:
        # print('alive')
        time.sleep(100)
