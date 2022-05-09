from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponseRedirect
from .models import Category, Product, Image
from .forms import CategoryForm, ProductForm, ProductFormFull


# Create your views here.
@transaction.atomic()
def all_categories(request):
    category_list = Category.objects.all().select_related(None).order_by('category_name')
    p = Paginator(category_list, 3)
    page = request.GET.get('page')
    categories = p.get_page(page)
    nums = 'a' * categories.paginator.num_pages
    return render(request, 'catalog/category_list.html',
                  {'category_list': category_list,
                   'categories': categories,
                   'nums': nums})


@transaction.atomic()
def all_products(request):
    product_list = Product.objects.all().prefetch_related(None).order_by("product_name")
    image_list = []
    p = Paginator(product_list, 3)
    page = request.GET.get('page')
    products = p.get_page(page)
    nums = 'a' * products.paginator.num_pages
    return render(request, 'catalog/product_list.html',
                  {'product_list': product_list,
                   'products': products,
                   'nums': nums,
                   'image_list': image_list,
                   })


@transaction.atomic()
def show_category(request, category_id):
    category = Category.objects.select_related(None).get(pk=category_id)
    return render(request, 'catalog/show_category.html',
                  {'category': category})


@transaction.atomic()
def show_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    category_list = product.category.all()
    image_list = product.image.all()
    return render(request, 'catalog/show_product.html',
                  {'product': product,
                   'image_list': image_list,
                   'category': category_list})


@transaction.atomic()
def add_category(request):
    submitted = False
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('add_category?submitted=True')
    else:
        form = CategoryForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'catalog/add_category.html', {'form': form, 'submitted': submitted})


@transaction.atomic()
def add_product(request):
    submitted = False
    if request.method == "POST":
        form = ProductFormFull(request.POST, request.FILES or None)
        files = request.FILES.getlist('images')
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            if files:
                for f in files:
                    Image.objects.create(product=post, image=f)
            return HttpResponseRedirect('add_product?submitted=True')
    else:
        form = ProductFormFull
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'catalog/add_product.html', {'form': form, 'submitted': submitted})


@transaction.atomic()
def update_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    form = CategoryForm(request.POST or None, request.FILES or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('list-category')
    return render(request, 'catalog/update_category.html',
                  {'category': category, 'form': form})


@transaction.atomic()
def update_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    form = ProductFormFull(request.POST or None, request.FILES or None, instance=product)
    files = request.FILES.getlist('images')
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        if files:
            for f in files:
                Image.objects.create(product=post, image=f)
        # form.save()
        return redirect('list-product')
    return render(request, 'catalog/update_product.html',
                  {'product': product, 'form': form})


def delete_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.delete()
    return redirect('list-product')


def delete_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    category.delete()
    return redirect('list-category')
