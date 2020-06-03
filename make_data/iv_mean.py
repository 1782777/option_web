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
import numpy as np

NIGHT_TIME = datetime.time(15,5,00)
MONING_TIME = datetime.time(9,28,00)
pd.set_option('display.max_rows', None)

class iv_mean:
    def __init__(self):
        print('iv_mean')
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
            time.sleep(15)

            

    def rest_df(self):
        time_AM = pd.date_range('9:30:00',freq='60S',periods=120+1)
        time_PM = pd.date_range('13:00:00',freq='60S',periods=120+1)
       
        df_am = pd.DataFrame(columns=['iv_50','iv_300'])
        df_pm = pd.DataFrame(columns=['iv_50','iv_300'])
        df_am['time']= time_AM.time
        df_pm['time']= time_PM.time
        self.df = pd.concat([df_am,df_pm],ignore_index=True)
        self.df['id'] = self.df.index
        #print(self.df)

    def makedata(self):
        print('iv_mean_makedata')
        url = "http://hq.sinajs.cn/list=sh510050"
        needTry = True
        while needTry:
            try:
                data = get(url).content.decode('gbk')
                needTry = False
            except:
                needTry = True
        data = data[data.find('"') + 1: data.rfind('"')].split(',')
        etf_50 = float(data[3]) 
        
        url = "http://hq.sinajs.cn/list=sh510300"
        needTry = True
        while needTry:
            try:
                data = get(url).content.decode('gbk')
                needTry = False
            except:
                needTry = True
        data = data[data.find('"') + 1: data.rfind('"')].split(',')
        etf_300 = float(data[3])
        # print(data)
        time_ = data[31]
        # print(time_)
        current_time= pd.to_datetime(time_).time()
        tmp = self.df[self.df['time']>current_time]
        #print (tmp)
        engine = sqlalchemy.create_engine('mysql+pymysql://root:root@localhost/option_data?charset=utf8')
        sql = ' select * from options; '
        df_option = pd.read_sql_query(sql, engine)
        # print(df_option,etf_50,etf_300)

        df_50 = df_option[df_option.name.str.contains('50ETF')]
        df_300 = df_option[df_option.name.str.contains('300ETF')]
        df_50 = df_50[df_50['iv'].astype(float)>0.01]
        df_300 = df_300[df_300['iv'].astype(float)>0.01]

        df_300['weight'] = 1/ abs(df_300['eprice'].astype(float)- etf_300)
        iv_300 = np.array(df_300['iv'].astype(float))

        df_50['weight'] = 1/ abs(df_50['eprice'].astype(float)- etf_50)
        iv_50 = np.array(df_50['iv'].astype(float))
        
        weight_300 = np.array(df_300['weight'])
        mean_300 = np.average(iv_300,weights=weight_300)
        weight_50 = np.array(df_50['weight'])
        mean_50 = np.average(iv_50,weights=weight_50)
        #print(mean_50,mean_300)

        # self.df.loc[0,['iv_50','iv_300']] = [np.float(mean_50),np.float(mean_300)]
        # print(self.df)
            
        # self.df.to_sql('iv_mean', engine, index=False, if_exists='replace')

        if len(tmp.index) > 0:
            index = tmp.iloc[0]['id']
            #print(index)
            self.df.loc[index,['iv_50','iv_300']] = [np.float(mean_50)*100,np.float(mean_300)*100]
            #print(self.df)
            
            self.df.to_sql('iv_mean', engine, index=False, if_exists='replace')

if __name__ == '__main__':
    iv_mean()
    a = input("input:")

    

    
