from .models import *
from django.shortcuts import render


def home_page_view(request):

    classes = Flat.get_types() + Volumetric.get_types()
    fig = classes[0][1]
    t = []

    if request.method == "GET":
        print(request.GET.get("type", ""))
        for type in classes:
            if type[0] == request.GET.get("type", ""):
                fig = type[1]

    if request.method == "POST":
        for type in classes:
            if type[0] == request.POST["title"]:
                fig = type[1]
        t = [
            int(request.POST[item])
            for item in request.POST
            if not (item == "csrfmiddlewaretoken" or item == "title")
        ]

    my_figure = fig(*t)

    figure = my_figure.plot()
    context = {
        "classes": classes,
        "type": my_figure.title,
        "params": my_figure.input.items(),
        "results": my_figure.output.items(),
        "picture": figure,
    }

    return render(request, "home.html", context=context)
