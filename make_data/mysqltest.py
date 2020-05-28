import pymysql
import datetime
import random
import time
from requests import get
import json
import pandas as pd
import sqlalchemy

def make_tabel():
    db_conn = pymysql.connect(host = 'localhost', user= 'root', passwd = 'root',
                            database='option_data',port=3306,charset='utf8')
    cursor = db_conn.cursor()
    d = datetime.datetime(2017, 8, 18, 9, 29, 0)
    for i in range(122):
        d =  d+datetime.timedelta(minutes=1)
        dd =d.strftime('%H:%M:%S')
        print(dd)
        iv = random.randint(0,9)*2.5
        print(iv)
        sql="insert into iv_mean(time,iv,target) values(%s,22.5,'etf')" 
        
        cursor.execute(sql,dd)

    d = datetime.datetime(2017, 8, 18, 12, 59, 0)
    for i in range(122):
        d =  d+datetime.timedelta(minutes=1)
        dd =d.strftime('%H:%M:%S')
        print(dd)
        iv = random.randint(0,9)*2.5
        print(iv)
        sql="insert into iv_mean(time,iv,target) values(%s,42.4,'etf')" 
        cursor.execute(sql,dd)
    db_conn.commit()
    cursor.close()

    db_conn.close()

def make_tabel_45():
    db_conn = pymysql.connect(host = 'localhost', user= 'root', passwd = 'root',
                            database='option_data',port=3306,charset='utf8')
    cursor = db_conn.cursor()
    d = datetime.datetime(2017, 8, 18, 9, 30, 0)
    for i in range(330*6):
        d =  d+datetime.timedelta(seconds=10)
        dd =d.strftime('%H:%M:%S')
        print(dd)
        iv = random.randint(0,9)*2.5
        print(iv)
        sql="insert into etf(time,etf_50,etf_300,es,etf_hs,etf_sz) values(%s,0,0,0,0,0)" 
        
        cursor.execute(sql,dd)

    db_conn.commit()
    cursor.close()

    db_conn.close()



# def insert_test():
#     db_conn = pymysql.connect(host = 'localhost', user= 'root', passwd = 'root',
#                             database='option_data',port=3306,charset='utf8')
#     cursor = db_conn.cursor()
#     for i in range(1000):
#         sql = 'update iv_mean set iv = %s where id = %s'
#         print(i%244)
#         cursor.execute(sql,[random.randint(1,100),i%244])
#         db_conn.commit()
#         time.sleep(0.5)
#     db_conn.close()


def volume():
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
    print(df_sql)
    engine = sqlalchemy.create_engine('mysql+pymysql://root:root@localhost/option_data?charset=utf8')
    df_sql.to_sql('volume', engine, index=False, if_exists='replace')

class Option:
    def __init__(self):
        self.month =[]
        self.df_all=pd.DataFrame()
        pass
    
    def load_month(self):
        url='http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getStockName'
        try:
            dates = get(url).json()['result']['data']['contractMonth']
            print(dates)
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

    def updata(self):
        self.month = self.load_month()
        self.codes = self.get_allop_codes(self.month)
        #print(self.codes)
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
        print(self.df_all)
        engine = sqlalchemy.create_engine('mysql+pymysql://root:root@localhost/option_data?charset=utf8')
        self.df_all.to_sql('options', engine, index=False, if_exists='replace')

    def calculation_iv_mean(self,e50,e300):
        #notzero =self.df_all[self.df_all['iv'].astype('float')>0.001] 
        # tmp = (notzero['day'].astype('int') - 40) / 3 * (notzero['iv'].astype('float'))
        notzero =self.df_all
        tmp = notzero['iv'].astype('float').mean()
        print(tmp)

class Etf_price:
    def __init__(self):
        pass

    def load(self):
        url = "http://hq.sinajs.cn/list=sh510050"
        needTry = True
        while needTry:
            try:
                data = get(url).content.decode('gbk')
                needTry = False
            except:
                needTry = True
        data = data[data.find('"') + 1: data.rfind('"')].split(',')
        etf_50 = data[3]

        url = "http://hq.sinajs.cn/list=sh510300"
        needTry = True
        while needTry:
            try:
                data = get(url).content.decode('gbk')
                needTry = False
            except:
                needTry = True
        data = data[data.find('"') + 1: data.rfind('"')].split(',')
        etf_300 = data[3]

        return etf_50,etf_300

if __name__ == '__main__':
    # while True:
    #     volume()
    #     time.sleep(10)

    # op = Option()
    # while True:
    #     op.updata()
    
    #     op.calculation_iv()
    #     time.sleep(10)
    make_tabel_45()
    # op = Option()

    # etf =Etf_price()
    # e50,e300 = etf.load()
    # op.updata()
    # op.calculation_iv_mean(e50,e300)
    
