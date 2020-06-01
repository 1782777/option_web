from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from option_view.models import options,iv_mean,volume,etf

# Create your views here.
def test_view(request):
    return render(request,'index.html')
    #return render(request,'index.html')

def get_ivmean(request):
    ivall = iv_mean.objects.all()
    print (len(ivall))
    msg_dic ={'type':'onepath'}
    iv50list = []
    iv300list = []
    timelist =[]
    for iv in ivall:
        iv50list.append(iv.iv_50)
        iv300list.append(iv.iv_300)
        timelist.append(iv.time)
    dic ={'iv_50':iv50list,'iv_300':iv300list,'time':timelist}
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
    e50,e300,es = [],[],[]
    for e in etf_:
        e50.append(e.etf50)
        e300.append(e.etf300)
        es.append(e.es)
    dic ={'etf50':e50,'etf300':e300,'es':es}
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
