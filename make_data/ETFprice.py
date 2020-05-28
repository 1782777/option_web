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

class ETFPrice:
    def __init__(self):
        print('ETFPrice')
        self.rest_df()
        # print(self.df)

        self.t = threading.Thread(target=self.loop)
        self.t.setDaemon(True)
        self.t.start()

    def loop(self):
        while True:
            self.makedata()
            time.sleep(15)

            

    def rest_df(self):
        time = pd.date_range('9:30:00',freq='30S',periods=330*2+1)
        self.df = pd.DataFrame(columns=['50','300','es','sz','hs'])
        self.df['time']= time.time
        self.df['id'] = self.df.index
        print(self.df)

    def makedata(self):
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
        es = (float(data[3]) - float(data[2])) / float(data[2])*100

        time_ = data[6]
        current_time= pd.to_datetime(time_).time()
        index = self.df[self.df['time']>current_time].iloc[0]['id']
        self.df.loc[index,['50','300','es','sz','hs']] = [etf_50,etf_300,es,0,0]
        #self.df[self.df['time']>current_time].iloc[0]['50','300','es']=[etf_50,etf_300,es]
        # last.loc[0,['50','300','es','sz','hs']] =[etf_50,etf_300,es,4,4]
        # print(self.df)

if __name__ == '__main__':
    # ETFPrice()
    # a = input("input:")

    t = datetime.time(17,42,00)
    c = datetime.datetime.now().time()
    print (t>c)

    
