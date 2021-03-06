from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from stock_app.models import stock_vol

# Create your views here.
def stock_view(request):
    #return HttpResponse("Hello world 111! ")
    return render('stock.html')
    #return render(request,'index.html')

def get_vol(request):
    #return HttpResponse("Hello world ! ")
    stock_ = stock_vol.objects.all()
    vollist,namelist,codelist,changelist = [],[],[],[]
    i =0
    for s in stock_:
        namelist.append(s.name)
        codelist.append(s.code)
        vollist.append(round(s.vol,2))
        changelist.append(round(s.change,2))
        i+=1
        if i>50:
            break
    dic ={'code':codelist,'name':namelist,'vol':vollist,'c':changelist}
    return JsonResponse(dic)
