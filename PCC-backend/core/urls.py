from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from prodcostcalc.settings import MEDIA_URL, MEDIA_ROOT
from . import views

urlpatterns = [
    path('api/categories/', views.get_categories, name='get_categories'),
    path('api/products/<str:category_name>/', views.get_products, name='get_products'),
    path('', views.index),
]

if settings.DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)