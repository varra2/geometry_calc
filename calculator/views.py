#from django.shortcuts import render
from urllib import response

from django.http import HttpResponse
from .models import *
#from django.views.generic.base import TemplateView
from django.shortcuts import render

# class SquareView(TemplateView):
#     model = Square
#     template_name = 'home.html'


def homePageView(request):

    if request.method == "POST":
        x = int(request.POST['side'])
    else:
        x = 5
    
    my_square = Square(x)
    figure = my_square.plot()
    context = {"type": my_square.title, "params": my_square.input.items(), "results": my_square.output.items(), "picture": figure}

    return render(request, "home.html", context=context)

def imageResponse(request):

    return HttpResponse('Hello')
    