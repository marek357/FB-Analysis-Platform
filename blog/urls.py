from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='platf_home'),
    path('about/', views.about, name='platf_about'),
    path('changedir/', views.changedir, name='platf_stats'),
    path('messagestats/', views.messagestats, name='platf_stats'),
    path('adstats/', views.adstats, name='platf_stats'),
    path('wordstats/', views.wordstats, name='platf_stats'),
]
