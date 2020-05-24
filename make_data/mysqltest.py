import pymysql
import datetime
import random
import time

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

if __name__ == '__main__':
    insert_test()
    pass
