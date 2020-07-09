from django.test import TestCase
import pandas as pd

# Create your tests here.

url ='http://1.optbbs.com/d/csv/d/data.csv'
url300 = 'https://1.optbbs.com/d/csv/d/vix300.csv'
needTry = True
# df =pd.DataFrame()
# df300 =pd.DataFrame()   
try:
    df = pd.read_csv(url)
    df300 = pd.read_csv(url300)
    needTry = False
    print(df,df300)
except:
    print('iv_load wrong')
    needTry = True
