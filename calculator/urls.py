from django.urls import path
from .views import home_page_view

urlpatterns = [
    #path('', SquareView.as_view(), name='home'),
    path('', home_page_view, name='home'),
]