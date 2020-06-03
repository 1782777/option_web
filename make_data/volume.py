import pymysql
import datetime
import random
import time
from requests import get
import json
import pandas as pd
import sqlalchemy
import threading

class volume:

    def __init__(self):
        print('init_volume')
        self.t = threading.Thread(target=self.loop)
        self.t.setDaemon(True)
        self.t.start()

    def loop(self):
        while True:
            self.makedata()
            time.sleep(15)

    def makedata(self):
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
            pass 
        
        df_today = pd.DataFrame(list_day, columns=['today'])
        df_today = df_today.cumsum()
        
        df_all = pd.concat([pf_volume,df_today],axis =1)
        df_all['chu']= df_all['today']/df_all['sum']
        df_sql = pd.DataFrame()
        df_sql['id'] = df_all.index
        df_sql['volume'] = df_all['chu']
        #print(df_sql)
        engine = sqlalchemy.create_engine('mysql+pymysql://root:root@localhost/option_data?charset=utf8')
        df_sql.to_sql('volume', engine, index=False, if_exists='replace')
