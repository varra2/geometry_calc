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

    classes = Figure.get_types()
    print(classes)
    fig = classes[0][1]
    t = None

    if request.method == "GET":
        print(request.GET.get('type',''))
        for type in classes:
            if type[0] == request.GET.get('type',''):
                fig = type[1]

    if request.method == "POST":
        for type in classes:
            if type[0] == request.POST['title']:
                fig = type[1]
        t = [int(request.POST[item]) for item in request.POST if not (item == 'csrfmiddlewaretoken' or item =='title')] 

    #my_square = Square(x)
    if t:
        my_square = fig(*t)
    else:
        my_square = fig()
    #my_square = Triangle()
    figure = my_square.plot()
    context = {"classes": classes ,"type": my_square.title, "params": my_square.input.items(), "results": my_square.output.items(), "picture": figure}

    return render(request, "home.html", context=context)

def imageResponse(request):

    return HttpResponse('Hello')
    