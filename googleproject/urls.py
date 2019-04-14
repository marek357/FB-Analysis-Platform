from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='google_home'),
    path('lok/', views.lokalizacja, name='google_lokalizacja'),
    path('changedir/', views.changedir, name='google_chdir'),
    path('images/m1.png', views.image1, name='google_img1'),
    path('images/m2.png', views.image2, name='google_img2'),
    path('images/m3.png', views.image3, name='google_img3'),
    path('images/m4.png', views.image4, name='google_img4'),
    path('images/m5.png', views.image5, name='google_img5'),
]
