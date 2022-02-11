from django.urls import path
from .views import homePageView, imageResponse

urlpatterns = [
    #path('', SquareView.as_view(), name='home'),
    path('', homePageView, name='home'),
    path('image/', imageResponse, name='image')
]