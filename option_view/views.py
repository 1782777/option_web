from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from option_view.models import options,iv_mean,volume,etf

import logging
import pandas as pd

# Create your views here.
def test_view(request):
    print(11)
    return render(request,'index.html')
    #return render(request,'index.html')

def get_ivmean(request):
    ivall = iv_mean.objects.all()
    print('iv!!!')
    logger = logging.getLogger('django')
    logger.info('123123')

    msg_dic ={'type':'onepath'}
    iv50list = []
    iv300list = []
    timelist =[]
    for iv in ivall:
        iv50list.append(iv.iv_50)
        iv300list.append(iv.iv_300)
        timelist.append(iv.time)

    # url ='http://1.optbbs.com/d/csv/d/data.csv'
    # url300 = 'https://1.optbbs.com/d/csv/d/vix300.csv'
    # needTry = True
    
    # try:
    #     df = pd.read_csv(url)
    #     df300 = pd.read_csv(url300)
    #     needTry = False
    #     print(df,df300)
    # except:
    #     print('iv_load wrong')
    #     needTry = True
    # iv50list = df['QVIX'].values.tolist()
    # iv300list = df300['QVIX'].values.tolist()
    # timelist = df300['Time'].values.tolist()
    dic ={'iv_50':iv50list,'iv_300':iv300list,'time':timelist}
    print(dic)
    return JsonResponse(dic)

def get_volume(request):
    volume_ = volume.objects.all()
    vollist = []
    for v in volume_:
        vollist.append(v.volume)
    dic ={'vol':vollist}
    return JsonResponse(dic)

def get_etf(request):
    etf_ = etf.objects.all()
    e50,e300,es,timel = [],[],[],[]
    for e in etf_:
        e50.append(e.etf50)
        e300.append(e.etf300)
        es.append(e.es)
        timel.append(e.time)
    dic ={'etf50':e50,'etf300':e300,'es':es,'time':timel}
    return JsonResponse(dic)

   
# def test(request):
#     result = {"categories":['1','2','3','4','5','6'], "data":[1,2,3,4,5,6]}
#     return JsonResponse(result)

# def test_add_db(request):
#     test1 = Test2(code='runoob')
#     test1.save()
#     return HttpResponse("<p>数据添加成功！</p>")

# def test_load_db(request):
#     # 初始化
#     response = ""
#     response1 = ""
    
    
#     # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
#     list = Test2.objects.all()
    
    
#     # 输出所有数据
#     for var in list:
#         response1 += var.code + " "
#     response = response1
#     return HttpResponse("<p>" + response + "</p>")
