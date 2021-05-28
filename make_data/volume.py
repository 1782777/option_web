import pymysql
import datetime
import random
import time
from requests import get
import json
import pandas as pd
import sqlalchemy
import threading
# import matplotlib.pyplot as plt

class volume:

    def __init__(self):
        print('init_volume')
        # self.makedata_dfcf()
        self.t = threading.Thread(target=self.loop)
        self.t.setDaemon(True)
        self.t.start()

    def loop(self):
        while True:
            self.makedata_dfcf()
            time.sleep(15)

    def makedata(self):
        # http://quote.eastmoney.com/stock_list.html
        # http://img1.money.126.net/data/hs/kline/day/history/2020/0600795.json
        url = "http://img1.money.126.net/data/hs/time/4days/0000016.json"
        pf_volume = pd.DataFrame()
        try:
            data = get(url).json()['data']
            for i in range(4):
                oneday = data[i]['data']
                list_day =[]
                for k in range(len(oneday)):
                    onemin = oneday[k][3]  
                    list_day.append(onemin)
                pf_volume[i] = list_day
            #print(pf_volume)
        except:
            pass 
        pf_volume['Col_sum'] = pf_volume.apply(lambda x: x.sum()/4, axis=1)
        pf_volume['sum'] = pf_volume['Col_sum'].cumsum()
        
        
        url = 'http://img1.money.126.net/data/hs/time/today/0000016.json'
        pf_today = pd.DataFrame()
        try:
            data = get(url).json()['data']
            list_day =[]
            for k in range(len(data)):
                onemin = data[k][3]  
                list_day.append(onemin)
        except:
            print('erorr')
            pass 
        
        df_today = pd.DataFrame(list_day, columns=['today'])
        df_today = df_today.cumsum()
        
        df_all = pd.concat([pf_volume,df_today],axis =1)
        df_all['chu']= df_all['today']/df_all['sum']
        df_sql = pd.DataFrame()
        df_sql['id'] = df_all.index
        df_sql['volume'] = df_all['chu']
        print(df_sql)
        print('---------------------------------')
        engine = sqlalchemy.create_engine('mysql+pymysql://root:root@localhost/option_data?charset=utf8')
        df_sql.to_sql('volume', engine, index=False, if_exists='replace')

    def makedata_dfcf(self):
        pf_volume = pd.DataFrame()
        url = 'http://push2his.eastmoney.com/api/qt/stock/trends2/get?secid=1.000016&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6%2Cf7%2Cf8%2Cf9%2Cf10%2Cf11&fields2=f51%2Cf53%2Cf56%2Cf58&iscr=0&ndays=5'
        data =[]
        try:
            data = get(url).json()['data']['trends']
            print(len(data))

        except:
            pass
        lengh = len(data)
        arr = []
        for i in range(241):
            arr.append(0) 

        for i in range(4): 
            list_day =[]
            for j in range(0,241):
                #print(data[241*i+j].split(' ')[1].split(',')[2])
                str_vol = data[241*i+j].split(' ')[1].split(',')[2]
                int_vol = int(str_vol)
                arr[j] = arr[j]+int_vol
                list_day.append(int_vol)
                # print(int_vol)
            pf_volume[i] = list_day    
        # print(arr)
        
        pf_volume['Col_sum'] = pf_volume.apply(lambda x: x.sum()/4, axis=1)
        today_list = []
        for i in range(241*4,241*5):
            int_vol= 0
            if(i<lengh):
                str_vol = data[i].split(' ')[1].split(',')[2]
                int_vol = int(str_vol)
            today_list.append(int_vol)
        print(today_list)
        pf_volume['today'] = today_list
        pf_volume= pf_volume.cumsum()
        pf_volume.at[241*5,'today'] =0
        pf_volume.at[241*5-1,'today'] =0
        print(pf_volume)
        pf_volume['res'] = pf_volume['today'] / pf_volume['Col_sum']
        
        # pf_volume['res'].plot()
        # print(pf_volume)
        # plt.show()

        df_sql = pd.DataFrame()
        
        df_sql['volume'] = pf_volume['res']
        
        # print(df_sql)
        engine = sqlalchemy.create_engine('mysql+pymysql://root:root@localhost/option_data?charset=utf8')
        df_sql.to_sql('volume', engine, index=False, if_exists='replace')
        #http://push2.eastmoney.com/api/qt/stock/trends2/get?secid=1.000016&fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58&ut=fa5fd1943c7b386f172d6893dbfba10b

if __name__ == '__main__':
    volume()

    a = input("input:")
