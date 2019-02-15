from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='platf_home'),
    path('about/', views.about, name='platf_about'),
    path('changedir/', views.changedir, name='platf_chdir'),
    path('messagestats/', views.messagestats, name='platf_msgstats'),
    path('adstats/', views.adstats, name='platf_adstats'),
    path('wordstats/', views.wordstats, name='platf_wordstats'),
]
