import pymysql
import datetime

db_conn = pymysql.connect(host = 'localhost', user= 'root', passwd = 'zx111111',
                          database='option_data',port=3306,charset='utf8')

d = datetime.datetime(2017, 8, 18, 9, 30, 0)
for i in range(1440):
    d =  d+datetime.timedelta(seconds=5)
    dd =d.strftime('%H:%M:%S')

    sql="insert into option_view_option(time) values('%d')" 

    data=(

    create_time,update_time

    )

    cursor.excute(sql%data)
        
    conn.commit()

    cursor.close()

    conn.close()
    print(dd)
