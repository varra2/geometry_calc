from django.urls import path
from .views import homePageView

urlpatterns = [
    #path('', SquareView.as_view(), name='home'),
    path('', homePageView, name='home'),
]