from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *

# Create your views here.

def product_list(request, category_slug=None, brand_slug=None, slug=None):
    category = None
    brand = None
    brand_by_cat = None
    categories = Category.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.filter(avalible=True)

    if category_slug:     
        category = get_object_or_404(Category, slug=category_slug)
        brand_by_cat = brands.filter(category=category)
        products = products.filter(category=category)

    if brand_slug:
        category = get_object_or_404(Category, slug=category_slug)
        brand = get_object_or_404(Brand, slug=brand_slug)
        products = products.filter(brand=brand)
        
    object_list = products
    paginator = Paginator(object_list, 1)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'catalog/product/list.html', {'page':page,'brand_by_cat':brand_by_cat,'brand':brand,'brands':brands,'category': category, 'categories': categories, 'products': products})

def product_detail(request, category_slug, brand_slug, slug):
    product = get_object_or_404(Product, slug=slug, avalible=True)
    return render(request, 'catalog/product/detail.html', {'product':product})