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

def insert_test():
    db_conn = pymysql.connect(host = 'localhost', user= 'root', passwd = 'root',
                            database='option_data',port=3306,charset='utf8')
    cursor = db_conn.cursor()
    for i in range(1000):
        sql = 'update iv_mean set iv = %s where id = %s'
        print(i%244)
        cursor.execute(sql,[random.randint(1,100),i%244])
        db_conn.commit()
        time.sleep(0.5)
    db_conn.close()


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
        
        # print(list_day)
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

if __name__ == '__main__':
    while True:
        volume()
        time.sleep(10)
    
