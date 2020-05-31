from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
def stock_view(request):
    return render('stock.html')
    #return render(request,'index.html')