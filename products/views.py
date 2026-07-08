from django.shortcuts import render
from .models import Product
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Product, Category
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProductForm
def admin_required(user):
    return user.is_superuser

def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        'products/product_detail.html',
        {
            'product': product
        }
    )

def product_list(request):

    products = Product.objects.all()

    categories = Category.objects.all()

    category_id = request.GET.get('category')

    if category_id:
        products = products.filter(
            category_id=category_id
        )

    query = request.GET.get('q')

    if query:
        products = products.filter(
            name__icontains=query
        )

    return render(
        request,
        'products/product_list.html',
        {
            'products': products,
            'categories': categories
        }
    )
@login_required
@user_passes_test(admin_required)
def admin_products(request):

    products = Product.objects.all().order_by('-id')

    return render(
        request,
        'products/admin_products.html',
        {
            'products': products
        }
    )
@login_required
@user_passes_test(admin_required)
def add_product(request):

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            return redirect('admin_products')

    else:
        form = ProductForm()

    return render(
        request,
        'products/product_form.html',
        {
            'form': form,
            'title': 'Add Product'
        }
    )
@login_required
@user_passes_test(admin_required)
def edit_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():
            form.save()
            return redirect('admin_products')

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        'products/product_form.html',
        {
            'form': form,
            'title': 'Edit Product'
        }
    )


@login_required
@user_passes_test(admin_required)
def delete_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == "POST":

        product.delete()

        return redirect(
            'admin_products'
        )

    return render(
        request,
        'products/delete_product.html',
        {
            'product': product
        }
    )