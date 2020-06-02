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

class option:
    def __init__(self):
        print('optioninfo')
        self.month =[]
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
                if c_time > MONING_TIME:
                    self.isLoop = True
                    self.rest_df()

            if self.isLoop:
                self.makedata()
            time.sleep(15)

            

    def rest_df(self):
        self.month =self.load_month()
        self.codes = self.get_allop_codes(self.month)
        #print(self.codes)
        self.df_all=pd.DataFrame()
        # self.df['id'] = self.df.index
        

    def load_month(self):
        url='http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getStockName'
        try:
            dates = get(url).json()['result']['data']['contractMonth']
            #print(dates)
        except:
            pass
        return dates

    def get_allop_codes(self,month):
        codes =[]
        name = ""
        for mon in month:
            name += "OP_UP_510050" + mon[-5:].replace('-','') +","
            name += "OP_DOWN_510050"+ mon[-5:].replace('-','') +","
            name += "OP_UP_510300"+ mon[-5:].replace('-','') +","
            name += "OP_DOWN_510300"+ mon[-5:].replace('-','') +","
            
        url = "http://hq.sinajs.cn/list=" + name
        #print(url)
        needTry = True
        while needTry:
            try:
                data = str(get(url).content)
                needTry = False
            except:
                needTry = True
        lines = data.split(';')
        for line in lines:
            word = line.replace('"', ',').split(',')
            for i in word:
                if i.startswith('CON_OP_'):
                    codes.append(i.split('_')[2])
        
        return set(codes)

    def get_allop_info(self,codes):
        '''
        con_op
        '''
        name = ""
        for code in codes:
            name +="CON_OP_"+ code + ","
        url = "http://hq.sinajs.cn/list=" + name
        
        names,prices,eprices,edays,days,iv=[],[],[],[],[],[]
        needTry = True
        while needTry:
            try:
                data = get(url).content.decode('gbk')
                needTry = False
            except:
                needTry = True
        lines = data.split(';')
        for line in lines:
            word = line[data.find('"') + 1: data.rfind('"')].split(',')
            #print(word)
            if len(word)>1:
                name =word[37]
                name = name.replace('购','_CALL_')
                name = name.replace('沽','_PUT_')
                name = name.replace('月','_MONTH_')
                names.append(name)
                prices.append(word[2])
                eprices.append(word[7])
                edays.append(word[46])
                days.append(word[47])
        '''
        CON_SO
        '''
        name = ""
        for code in codes:
            name +="CON_SO_"+ code + ","
        url = "http://hq.sinajs.cn/list=" + name
        
        needTry = True
        while needTry:
            try:
                data = get(url).content.decode('gbk')
                needTry = False
            except:
                needTry = True
        lines = data.split(';')
        for line in lines:
            word = line[data.find('"') + 1: data.rfind('"')].split(',')
            #print(word)
            if len(word)>1:
                iv.append(word[9])

        return codes,names,prices,eprices,edays,days,iv

    def makedata(self):
        codes,names,prices,eprices,edays,days,iv = self.get_allop_info(self.codes)
        self.df_all = pd.DataFrame()
        
        self.df_all['code']=list(codes)
        self.df_all['name']=names
        self.df_all['price']=prices
        self.df_all['eprice']=eprices
        self.df_all['eday']=edays
        self.df_all['day']=days
        self.df_all['iv']=iv
        self.df_all['id'] = self.df_all.index
        #print(self.df_all)
        engine = sqlalchemy.create_engine('mysql+pymysql://root:root@localhost/option_data?charset=utf8')
        self.df_all.to_sql('options', engine, index=False, if_exists='replace')
        

if __name__ == '__main__':
    option()
    a = input("input:")

    

    
