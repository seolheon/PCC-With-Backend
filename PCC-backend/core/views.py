from django.http import HttpResponse, JsonResponse
from .models import Category, Product
from django.shortcuts import redirect, render

def index(request):
    return redirect('http://localhost:5173/')

def get_categories(request):
    categories = Category.objects.all()
    data = [{'name': category.name} for category in categories]
    return JsonResponse(data, safe=False)


def get_products(request, category_name):
    category = Category.objects.get(name=category_name)
    products = Product.objects.filter(category=category)
    data = [{'name': product.name, 'cost': product.price, 'image': product.image.url} for product in products]
    return JsonResponse(data, safe=False)