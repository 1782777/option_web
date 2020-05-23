import pymysql
import datetime
import random

def make_tabel():
    db_conn = pymysql.connect(host = 'localhost', user= 'root', passwd = 'zx111111',
                            database='option_data',port=3306,charset='utf8')
    cursor = db_conn.cursor()
    d = datetime.datetime(2017, 8, 18, 9, 30, 0)
    for i in range(1440):
        d =  d+datetime.timedelta(seconds=5)
        dd =d.strftime('%H:%M:%S')
        print(dd)
        iv = random.randint(0,9)*2.5
        print(iv)
        sql="insert into iv_mean(time,iv,target) values(%s,22.5,'etf')" 
        
        cursor.execute(sql,dd)

    d = datetime.datetime(2017, 8, 18, 13, 0, 0)
    for i in range(1440):
        d =  d+datetime.timedelta(seconds=5)
        dd =d.strftime('%H:%M:%S')
        print(dd)
        iv = random.randint(0,9)*2.5
        print(iv)
        sql="insert into iv_mean(time,iv,target) values(%s,42.4,'etf')" 
        cursor.execute(sql,dd)
    db_conn.commit()
    cursor.close()

    db_conn.close()


if __name__ == '__main__':
    pass
