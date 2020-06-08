import requests
from requests import get
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
import datetime
import threading
import sqlalchemy

MAXCOUNT = 5000
NIGHT_TIME = datetime.time(15,5,00)
MONING_TIME = datetime.time(9,00,00)

class stork_volume:
    def __init__(self):
        self.df_code=pd.DataFrame(columns=['code','name','vol','vol_day_mean','change','date'])
        self.initcode()
        self.isLoop =True
        self.rest_df()
        self.t = threading.Thread(target=self.loop)
        self.t.setDaemon(True)
        self.t.start()

    def initcode(self):
        url ='http://quote.eastmoney.com/stock_list.html'
        strhtml = requests.get(url)        #Get方式获取网页数据
        strhtml.encoding = 'gbk'  # 改变编码
        soup=BeautifulSoup(strhtml.text,'lxml')
        div = soup.find('div',class_='quotebody')
        alist = div.find_all('a')
        codelist,namelist =[],[]
        for a in alist:
            if '(' in a.text:
                name = a.text.split('(')[0]
                code = a.text.split('(')[1][:-1]
                namelist.append(name)
                codelist.append(code)
        self.df_code['code']=codelist
        self.df_code['name']=namelist
        # print(self.df_code)

    def rest_df(self):
        print('start rest stock mean vol')
        i = 0
        for tup in self.df_code.itertuples():
            code = tup.code
            if code[0] == '6':
                try:
                    self.one_stock_mean('0',code)
                except:
                    pass
            if code[0] == '0':
                try:
                    self.one_stock_mean('1',code)
                except:
                    pass
            i+=1
            if i>MAXCOUNT:
                break
           
            

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
                #print('make')
                self.makedata()
            time.sleep(10)  

    def one_stock_mean(self,starturl,code):
        url = 'http://img1.money.126.net/data/hs/kline/day/history/2020/%s%s.json' %(starturl,code)
        #print(url)
        vol_list =[]
        #print(url)
        data = get(url).json()['data']
        #print (data)
        for d in range(len(data)-1,len(data)-10,-1):
            volume = data[d][5]
            vol_list.append(volume)
        vol_nparr = np.array(vol_list)
        vol_mean = vol_nparr.mean()
        #print (vol_mean)
        self.df_code.loc[self.df_code['code']==code,'vol_day_mean']=vol_mean
        

    def curren_stock(self):
        i ,longth= 0,0
        shlist,szlist =[],[]
        sh,sz ='',''
        for tup in self.df_code.itertuples():
            code = tup.code
            #print(code)
            if code[0] == '6':
                sh +='sh' + code +','
                longth +=1
                i+=1
                if longth>500:
                    shlist.append(sh)
                    sh=''
                    longth =0    
            if code[0] == '0':
                sz +='sz' + code +','
                longth +=1
                i+=1
                if longth>500:
                    szlist.append(sz)
                    sz=''
                    longth =0   
            
            # if i>MAXCOUNT:
            #     break
        #print (len(shlist),len(szlist))
        
        cout =0
        for z in zip(shlist,szlist):
            for url in z:
                url = 'http://hq.sinajs.cn/list=%s' %url
                needTry = True
                while needTry:
                    try:
                        data = get(url).content.decode('gbk')
                        needTry = False
                    except:
                        needTry = True
                onecontect = data.split(';')
                for oneline in onecontect:
                    data = oneline[oneline.find('"') + 1: oneline.rfind('"')].split(',')
                    cout +=1
                    code = oneline[14:20]
                    #print(data)
                    try:
                        change = (float(data[3]) - float(data[2])) / float(data[2])*100
                        vol = float(data[8])
                        #print(code,change,vol)
                        
                    except:
                        continue
                    res = vol/self.df_code.loc[self.df_code['code']==code,'vol_day_mean']
                    self.df_code.loc[self.df_code['code']==code,'vol']=res
                    self.df_code.loc[self.df_code['code']==code,'change']=change
                    
        # self.df_code.to_excel('./test.xlsx')    
        print('finish')

        # res = vol_sum/self.df_code.loc[self.df_code['code']==code,'vol_day_mean']
        # self.df_code.loc[self.df_code['code']==code,'vol']=res
        # self.df_code.loc[self.df_code['code']==code,'change']=change
        
    def current(self):
        pass

    def makedata(self):
        res_list =[]
        self.curren_stock()

        self.df_code = self.df_code.sort_values(['vol'], ascending = False) 
        self.df_code.reset_index(drop=True, inplace=True)
        self.df_code['id'] = self.df_code.index
        #print(self.df_code)
        engine = sqlalchemy.create_engine('mysql+pymysql://root:root@localhost/option_data?charset=utf8')
        try:
            self.df_code.to_sql('stock_vol', engine, index=False, if_exists='replace')
        except:
            print('stock info insert mysql error')
        print('stock info insert mysql finish')
        # self.df_code.to_excel('./test.xlsx')  
        
            
            
 

if __name__ == '__main__':
    sv =stork_volume()
    a = input("input:")
    # url = 'http://img1.money.126.net/data/hs/time/today/0600031.json'
    # vol_list =[]
    #     #print(url)
    # dataall = get(url).json()
    #     #print (data)
    # data = dataall['data']
    # yestclose = dataall['yestclose']
    # print(yestclose)
    # for k in range(len(data)):
    #     onemin = data[k][3]  
    #     price = data[k][1]  
    #     vol_list.append(onemin)
    # vol_nparr = np.array(vol_list)
    # vol_sum = vol_nparr.sum()

    # change = (price - yestclose)/yestclose*100
    # print(change)
