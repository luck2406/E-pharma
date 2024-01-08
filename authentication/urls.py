from django.urls import path
from .views import *
urlpatterns = [
    path('login/',signin),
    path('signout/',signout),
    path('signup/',signup),
]