import pymysql
import datetime
import random
import time
from requests import get
import json
import pandas as pd
import sqlalchemy
import threading
import datetime

NIGHT_TIME = datetime.time(15,5,00)
MONING_TIME = datetime.time(9,28,00)

class ETFPrice:
    def __init__(self):
        print('ETFPrice')
        self.isLoop =True
        self.rest_df()
        # print(self.df)

        self.t = threading.Thread(target=self.loop)
        self.t.setDaemon(True)
        self.t.start()

    def loop(self):
        while True:
            c_time = datetime.datetime.now().time()
            if c_time > NIGHT_TIME:
                self.isLoop = False
            if not self.isLoop:
                if c_time > MONING_TIME and c_time < NIGHT_TIME:
                    self.isLoop = True
                    self.rest_df()

            if self.isLoop:
                self.makedata()
            time.sleep(5)

            

    def rest_df(self):
        time_ = pd.date_range('9:30:00',freq='30S',periods=330*2+1)
        self.df = pd.DataFrame(columns=['etf50','etf300','es','sz','hs'])
        self.df['time']= time_.time
        self.df['id'] = self.df.index
        #print(self.df)

    def makedata(self):
        #print('etf_makedata')
        url = "http://hq.sinajs.cn/list=sh510050"
        needTry = True
        while needTry:
            try:
                data = get(url).content.decode('gbk')
                needTry = False
            except:
                needTry = True
        data = data[data.find('"') + 1: data.rfind('"')].split(',')
        etf_50 = (float(data[3]) - float(data[2])) / float(data[2])*100
        
        url = "http://hq.sinajs.cn/list=sh510300"
        needTry = True
        while needTry:
            try:
                data = get(url).content.decode('gbk')
                needTry = False
            except:
                needTry = True
        data = data[data.find('"') + 1: data.rfind('"')].split(',')
        etf_300 = (float(data[3]) - float(data[2])) / float(data[2])*100

        url = "http://hq.sinajs.cn/list=hf_ES"
        needTry = True
        while needTry:
            try:
                data = get(url).content.decode('gbk')
                needTry = False
            except:
                needTry = True
        data = data[data.find('"') + 1: data.rfind('"')].split(',')
        es = (float(data[0]) - float(data[7])) / float(data[7])*100
        #print(es)

        time_ = data[6]
        current_time= pd.to_datetime(time_).time()
        tmp = self.df[self.df['time']>current_time]
        #print(tmp)
        if len(tmp.index) > 0:
            index = tmp.iloc[0]['id']
            self.df.loc[index,['etf50','etf300','es','sz','hs']] = [etf_50,etf_300,es,0,0]
            #print(self.df)
            engine = sqlalchemy.create_engine('mysql+pymysql://root:root@localhost/option_data?charset=utf8')
            self.df.to_sql('etf', engine, index=False, if_exists='replace')

if __name__ == '__main__':
    ETFPrice()
    a = input("input:")

    

    
