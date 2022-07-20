from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Index'),
    path('finder_tool', views.finder_tool, name='Finder Tool'),
    path('about_us', views.about_us, name='About Us'),
    path('result', views.result, name='Result')
]
