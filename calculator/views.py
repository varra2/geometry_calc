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
        #x = int(request.POST['side'])
        a = int(request.POST['a_side'])
        b = int(request.POST['b_side'])
        c = int(request.POST['c_side'])

    else:
        #x = 5
        a = 5
        b = 4
        c = 3
    
    #my_square = Square(x)
    #my_square = Rectangle(a,b)
    my_square = Triangle(a,b,c)
    figure = my_square.plot()
    context = {"type": my_square.title, "params": my_square.input.items(), "results": my_square.output.items(), "picture": figure}

    return render(request, "home.html", context=context)

def imageResponse(request):

    return HttpResponse('Hello')
    