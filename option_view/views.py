from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.
def test_view(request):
    return render(request,'index.html')
    #return render(request,'index.html')

def test(request):
    result = {"categories":['1','2','3','4','5','6'], "data":[1,2,3,4,5,6]}
    return JsonResponse(result)