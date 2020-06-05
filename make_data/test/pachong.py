import requests
from requests import get
from bs4 import    BeautifulSoup
import time
import pandas as pd
import numpy as np

class stork_volume:
    def __init__(self):
        self.df_code=pd.DataFrame(columns=['code','name','vol','vol_day_mean','change'])
        self.initcode()
        self.loop()

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
        print(self.df_code)

    def loop(self):
        self.makedata()
        # while True:
        #     self.makedata()
        #     time.sleep(15)  

    def one_stock_mean(self,code):
        url = 'http://img1.money.126.net/data/hs/kline/day/history/2020/0%s.json' %code
        vol_list =[]
        #print(url)
        data = get(url).json()['data']
        #print (data)
        for d in range(len(data)-1,len(data)-10,-1):
            volume = data[d][5]
            vol_list.append(volume)
        vol_nparr = np.array(vol_list)
        vol_mean = vol_nparr.mean()
        self.df_code.loc[self.df_code['code']==code,'vol_day_mean']=vol_mean

    def one_stock(self,code):
        # url = 'http://img1.money.126.net/data/hs/kline/day/history/2020/0%s.json' %code
        # vol_list =[]
        
        # data = get(url).json()['data']
        # for d in range(len(data)-1,len(data)-10,-1):
        #     volume = data[d][5]
        #     vol_list.append(volume)
        # vol_nparr = np.array(vol_list)
        # vol_mean = vol_nparr.mean()
        # #print(vol_mean)   
        

        url = 'http://img1.money.126.net/data/hs/time/today/0%s.json' %code
        vol_list =[]
        #print(url)
        dataall = get(url).json()
        #print (data)
        data = dataall['data']
        yestclose = dataall['yestclose']
        print(yestclose)
        for k in range(len(data)):
            onemin = data[k][3]  
            price = data[k][1]  
            vol_list.append(onemin)
        vol_nparr = np.array(vol_list)
        vol_sum = vol_nparr.sum()

        change = (price - yestclose)/yestclose*100
        #print(vol_sum)
        

        res = vol_sum/self.df_code.loc[self.df_code['code']==code,'vol_day_mean']
        self.df_code.loc[self.df_code['code']==code,'vol']=res
        self.df_code.loc[self.df_code['code']==code,'change']=change
        

    def makedata(self):
        res_list =[]
        i = 0
        for tup in self.df_code.itertuples():
            code = tup.code
            if code[0] != '6' and code[0] != '0':
                continue
            # i+=1
            # if i>20:
            #     break
           
            try:
                self.one_stock_mean(code)
                self.one_stock(code)
                # self.df_code.loc[self.df_code['code']==code,'vol']=res
                # print(code,':',res)
            except:
                print ('error')
                pass 

        self.df_code = self.df_code.sort_values(['vol'], ascending = False) 
        # print(self.df_code[self.df_code['vol'] is not np.nan])
        self.df_code.to_excel('./vol2.xlsx')
            
            
 

if __name__ == '__main__':
    sv =stork_volume()

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
