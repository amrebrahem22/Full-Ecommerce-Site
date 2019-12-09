# Django Ecommerce Site

## Getting started

Steps:

1. `pipenv shell`
2. `pipenv install django pillow`
3. `django-admin startproject EcomSite`
4. `python manage.py startapp cors`

## create our model
*now our model will have the `Item` that will display on the site and will have our `Order` that will have a relationship with the user and will have the items that assigned to this order and will have the `OrderItem` which is the `Item` but in the order and will have a relationship with the `Item`* </br>
``` python
from django.conf import settings
from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
```
- then register them in the `admin`
``` python
from django.contrib import admin

from .models import Item, OrderItem, Order


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
```
- then in `views.py` i created theseviews 
``` python
from django.shortcuts import render
from .models import Item

def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)

def checkout(request):
    return render(request, "checkout.html")

def home(request):
    return render(request, "home.html")
```
- and in `urls.py`
``` python
from django.urls import path
from .views import (
    products,
    checkout,
    home
)

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('checkout/', checkout, name='checkout'),
    path('products/', products, name='products')
]
```
- then added it in our main `urls.py`
``` python
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls', namespace='core'))
]
```
- then i installed `django-allauth` and in `settings.py`
``` python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'core'
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_env')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Auth

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)
SITE_ID = 1
```
- then i created our `base.html`
``` html
{% load static %}

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta http-equiv="x-ua-compatible" content="ie=edge">
  <title>Material Design Bootstrap</title>
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.1/css/all.css">
  <link href="{% static 'css/bootstrap.min.css' %}" rel="stylesheet">
  <link href="{% static 'css/mdb.min.css' %}" rel="stylesheet">
  <link href="{% static 'css/style.min.css' %}" rel="stylesheet">
  <style type="text/css">
    html,
    body,
    header,
    .carousel {
      height: 60vh;
    }
    @media (max-width: 740px) {
      html,
      body,
      header,
      .carousel {
        height: 100vh;
      }
    }
    @media (min-width: 800px) and (max-width: 850px) {
      html,
      body,
      header,
      .carousel {
        height: 100vh;
      }
    }
  </style>
</head>

{% include "navbar.html" %}

<body>
    {% block content %}
    {% endblock content %}

    {% include "footer.html" %}
    {% include "scripts.html" %}
</body>
</html>
```
- and in `templates/checkout.html` 
```html
{% extends "base.html" %}
grey lighten-3

{% block content %}

  <main class="mt-5 pt-4">
    <div class="container wow fadeIn">

      <!-- Heading -->
      <h2 class="my-5 h2 text-center">Checkout form</h2>

      <!--Grid row-->
      <div class="row">

        <!--Grid column-->
        <div class="col-md-8 mb-4">

          <!--Card-->
          <div class="card">

            <!--Card content-->
            <form class="card-body">

              <!--Grid row-->
              <div class="row">

                <!--Grid column-->
                <div class="col-md-6 mb-2">

                  <!--firstName-->
                  <div class="md-form ">
                    <input type="text" id="firstName" class="form-control">
                    <label for="firstName" class="">First name</label>
                  </div>

                </div>
                <!--Grid column-->

                <!--Grid column-->
                <div class="col-md-6 mb-2">

                  <!--lastName-->
                  <div class="md-form">
                    <input type="text" id="lastName" class="form-control">
                    <label for="lastName" class="">Last name</label>
                  </div>

                </div>
                <!--Grid column-->

              </div>
              <!--Grid row-->

              <!--Username-->
              <div class="md-form input-group pl-0 mb-5">
                <div class="input-group-prepend">
                  <span class="input-group-text" id="basic-addon1">@</span>
                </div>
                <input type="text" class="form-control py-0" placeholder="Username" aria-describedby="basic-addon1">
              </div>

              <!--email-->
              <div class="md-form mb-5">
                <input type="text" id="email" class="form-control" placeholder="youremail@example.com">
                <label for="email" class="">Email (optional)</label>
              </div>

              <!--address-->
              <div class="md-form mb-5">
                <input type="text" id="address" class="form-control" placeholder="1234 Main St">
                <label for="address" class="">Address</label>
              </div>

              <!--address-2-->
              <div class="md-form mb-5">
                <input type="text" id="address-2" class="form-control" placeholder="Apartment or suite">
                <label for="address-2" class="">Address 2 (optional)</label>
              </div>

              <!--Grid row-->
              <div class="row">

                <!--Grid column-->
                <div class="col-lg-4 col-md-12 mb-4">

                  <label for="country">Country</label>
                  <select class="custom-select d-block w-100" id="country" required>
                    <option value="">Choose...</option>
                    <option>United States</option>
                  </select>
                  <div class="invalid-feedback">
                    Please select a valid country.
                  </div>

                </div>
                <!--Grid column-->

                <!--Grid column-->
                <div class="col-lg-4 col-md-6 mb-4">

                  <label for="state">State</label>
                  <select class="custom-select d-block w-100" id="state" required>
                    <option value="">Choose...</option>
                    <option>California</option>
                  </select>
                  <div class="invalid-feedback">
                    Please provide a valid state.
                  </div>

                </div>
                <!--Grid column-->

                <!--Grid column-->
                <div class="col-lg-4 col-md-6 mb-4">

                  <label for="zip">Zip</label>
                  <input type="text" class="form-control" id="zip" placeholder="" required>
                  <div class="invalid-feedback">
                    Zip code required.
                  </div>

                </div>
                <!--Grid column-->

              </div>
              <!--Grid row-->

              <hr>

              <div class="custom-control custom-checkbox">
                <input type="checkbox" class="custom-control-input" id="same-address">
                <label class="custom-control-label" for="same-address">Shipping address is the same as my billing address</label>
              </div>
              <div class="custom-control custom-checkbox">
                <input type="checkbox" class="custom-control-input" id="save-info">
                <label class="custom-control-label" for="save-info">Save this information for next time</label>
              </div>

              <hr>

              <div class="d-block my-3">
                <div class="custom-control custom-radio">
                  <input id="credit" name="paymentMethod" type="radio" class="custom-control-input" checked required>
                  <label class="custom-control-label" for="credit">Credit card</label>
                </div>
                <div class="custom-control custom-radio">
                  <input id="debit" name="paymentMethod" type="radio" class="custom-control-input" required>
                  <label class="custom-control-label" for="debit">Debit card</label>
                </div>
                <div class="custom-control custom-radio">
                  <input id="paypal" name="paymentMethod" type="radio" class="custom-control-input" required>
                  <label class="custom-control-label" for="paypal">Paypal</label>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="cc-name">Name on card</label>
                  <input type="text" class="form-control" id="cc-name" placeholder="" required>
                  <small class="text-muted">Full name as displayed on card</small>
                  <div class="invalid-feedback">
                    Name on card is required
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <label for="cc-number">Credit card number</label>
                  <input type="text" class="form-control" id="cc-number" placeholder="" required>
                  <div class="invalid-feedback">
                    Credit card number is required
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-md-3 mb-3">
                  <label for="cc-expiration">Expiration</label>
                  <input type="text" class="form-control" id="cc-expiration" placeholder="" required>
                  <div class="invalid-feedback">
                    Expiration date required
                  </div>
                </div>
                <div class="col-md-3 mb-3">
                  <label for="cc-expiration">CVV</label>
                  <input type="text" class="form-control" id="cc-cvv" placeholder="" required>
                  <div class="invalid-feedback">
                    Security code required
                  </div>
                </div>
              </div>
              <hr class="mb-4">
              <button class="btn btn-primary btn-lg btn-block" type="submit">Continue to checkout</button>

            </form>

          </div>
          <!--/.Card-->

        </div>
        <!--Grid column-->

        <!--Grid column-->
        <div class="col-md-4 mb-4">

          <!-- Heading -->
          <h4 class="d-flex justify-content-between align-items-center mb-3">
            <span class="text-muted">Your cart</span>
            <span class="badge badge-secondary badge-pill">3</span>
          </h4>

          <!-- Cart -->
          <ul class="list-group mb-3 z-depth-1">
            <li class="list-group-item d-flex justify-content-between lh-condensed">
              <div>
                <h6 class="my-0">Product name</h6>
                <small class="text-muted">Brief description</small>
              </div>
              <span class="text-muted">$12</span>
            </li>
            <li class="list-group-item d-flex justify-content-between lh-condensed">
              <div>
                <h6 class="my-0">Second product</h6>
                <small class="text-muted">Brief description</small>
              </div>
              <span class="text-muted">$8</span>
            </li>
            <li class="list-group-item d-flex justify-content-between lh-condensed">
              <div>
                <h6 class="my-0">Third item</h6>
                <small class="text-muted">Brief description</small>
              </div>
              <span class="text-muted">$5</span>
            </li>
            <li class="list-group-item d-flex justify-content-between bg-light">
              <div class="text-success">
                <h6 class="my-0">Promo code</h6>
                <small>EXAMPLECODE</small>
              </div>
              <span class="text-success">-$5</span>
            </li>
            <li class="list-group-item d-flex justify-content-between">
              <span>Total (USD)</span>
              <strong>$20</strong>
            </li>
          </ul>
          <!-- Cart -->

          <!-- Promo code -->
          <form class="card p-2">
            <div class="input-group">
              <input type="text" class="form-control" placeholder="Promo code" aria-label="Recipient's username" aria-describedby="basic-addon2">
              <div class="input-group-append">
                <button class="btn btn-secondary btn-md waves-effect m-0" type="button">Redeem</button>
              </div>
            </div>
          </form>
          <!-- Promo code -->

        </div>
        <!--Grid column-->

      </div>
      <!--Grid row-->

    </div>
  </main>

{% endblock content %}
```
## Add-to and remove-from cart
- now in `models.py`
``` python
from django.conf import settings
from django.db import models
from django.shortcuts import reverse

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

```
*now that's will be our item and `the get_add_to_cart()` method will create the url for the add to cart page and the `get_remove_from_cart()` too* </br>

``` python
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.title
        return f"{self.quantity} of {self.item.title}"
```
*and now our order item will have our user and and the `ordered` will be if theat's done or not and item itself and the quantity* </br>

- now in `views.py`
``` python
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.utils import timezone
from .models import Item, OrderItem, Order

class HomeView(ListView):
    model = Item
    template_name = "home.html"
 
 class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

# now it will pass the slug to this url then will get the item with this slug and will get the orderitem or create a new one because this url will add the item to the OrderItem and the Order model contain all OrderItem and will make the ordered=Flase because it will be True when we finish purchising
# now we want to know if there's an order here for this user or now so if there's an order not complteted then get it and check if this order item in the order or not do if exist will increase it by one else will add it to our order items because the order will have the item field that will have a manyToMany relationship
# and if the rder is not exist we will craete a new one and add this item to it
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:product", slug=slug)
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:product", slug=slug)

# this method will get the item and will get the order and if there's order assigned with this user we will check if the order item is in the order and if we will get this order and remove it 
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:product", slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)

```
- then in `urls`
``` python
from django.urls import path
from .views import (
    ItemDetailView,
    checkout,
    HomeView,
    add_to_cart,
    remove_from_cart
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', checkout, name='checkout'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart')
]
```
- and in `base.html` will add the messages
``` html
<div class="mt-5 pt-4">
  {% if messages %}
      {% for message in messages %}
      <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
        {{ message }}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      {% endfor %}
  {% endif %}
  </div>
```
- now in `home.html` will add our products in the products section
``` html
<section class="text-center mb-4">
  <div class="row wow fadeIn">
    {% for item in object_list %}
    <div class="col-lg-3 col-md-6 mb-4">
      <div class="card">
        <!--Card image-->
        <div class="view overlay">
          <img src="{{ item.image.url }}" class="card-img-top"
            alt="">
          <a>
          <a href="{{ item.get_absolute_url }}">
            <div class="mask rgba-white-slight"></div>
          </a>
        </div>
        <!--Card image-->

        <!--Card content-->
        <div class="card-body text-center">
          <a href="" class="grey-text">
            <h5>{{ item.get_category_display }}</h5>
          </a>
          <h5>
            <strong>
              <a href="{{ item.get_absolute_url }}" class="dark-grey-text">{{ item.title }}
                <span class="badge badge-pill {{ item.get_label_display }}-color">NEW</span>
              </a>
              <strong>$
              {% if item.discount_price %}
                {{ item.discount_price }}
              {% else %}
                {{ item.price }}
              {% endif %}
              </strong>
            </strong>           
      </div>
      {% endfor %}
  </div>
</section>
```
- and in the `products.html`
``` html
{% extends "base.html" %}

{% block content %}

  <main class="mt-5 pt-4">
    <div class="container dark-grey-text mt-5">

      <!--Grid row-->
      <div class="row wow fadeIn">

        <!--Grid column-->
        <div class="col-md-6 mb-4">

          <img src="https://mdbootstrap.com/img/Photos/Horizontal/E-commerce/Products/14.jpg" class="img-fluid" alt="">

        </div>
        <!--Grid column-->

        <!--Grid column-->
        <div class="col-md-6 mb-4">

          <!--Content-->
          <div class="p-4">

            <div class="mb-3">
              <a href="">
                <span class="badge purple mr-1">{{ object.get_category_display }}</span>
              </a>
            </div>

            <p class="lead">
              {% if object.discount_price %}
              <span class="mr-1">
                <del>${{ object.price }}</del>
              </span>
              <span>${{ object.discount_price }}</span>
              {% else %}
              <span>${{ object.price }}</span>
              {% endif %}
            </p>

            <p class="lead font-weight-bold">Description</p>

            <p>{{ object.description }}</p>

            {% comment %} <form class="d-flex justify-content-left">
              <!-- Default input -->
              <input type="number" value="1" aria-label="Search" class="form-control" style="width: 100px">
              <button class="btn btn-primary btn-md my-0 p" type="submit">
                Add to cart
                <i class="fas fa-shopping-cart ml-1"></i>
              </button>

            </form> {% endcomment %}
            <a href="{{ object.get_add_to_cart_url }}" class="btn btn-primary btn-md my-0 p">
              Add to cart
              <i class="fas fa-shopping-cart ml-1"></i>
            </a>
            <a href="{{ object.get_remove_from_cart_url }}" class="btn btn-danger btn-md my-0 p">
              Remove from cart
            </a>

          </div>
          <!--Content-->

        </div>
        <!--Grid column-->

      </div>
      <!--Grid row-->

      <hr>

      <!--Grid row-->
      <div class="row d-flex justify-content-center wow fadeIn">

        <!--Grid column-->
        <div class="col-md-6 text-center">

          <h4 class="my-4 h4">Additional information</h4>

          <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Natus suscipit modi sapiente illo soluta odit
            voluptates,
            quibusdam officia. Neque quibusdam quas a quis porro? Molestias illo neque eum in laborum.</p>

        </div>
        <!--Grid column-->

      </div>
      <!--Grid row-->

      <!--Grid row-->
      <div class="row wow fadeIn">

        <!--Grid column-->
        <div class="col-lg-4 col-md-12 mb-4">

          <img src="https://mdbootstrap.com/img/Photos/Horizontal/E-commerce/Products/11.jpg" class="img-fluid" alt="">

        </div>
        <!--Grid column-->

        <!--Grid column-->
        <div class="col-lg-4 col-md-6 mb-4">

          <img src="https://mdbootstrap.com/img/Photos/Horizontal/E-commerce/Products/12.jpg" class="img-fluid" alt="">

        </div>
        <!--Grid column-->

        <!--Grid column-->
        <div class="col-lg-4 col-md-6 mb-4">

          <img src="https://mdbootstrap.com/img/Photos/Horizontal/E-commerce/Products/13.jpg" class="img-fluid" alt="">

        </div>
        <!--Grid column-->

      </div>
      <!--Grid row-->

    </div>
  </main>

{% endblock content %}
```
## Improving the UI
- install crispy-form and add it to installed apps
in `settings.py`
``` python
LOGIN_REDIRECT_URL = '/'

# CRISPY FORMS
CRISPY_TEMPLATE_PACK = 'bootstrap4'
```
- now go to (https://github.com/pennersr/django-allauth/tree/master/allauth/templates) to and download these files to control with the view of the allauth library

- and in `base.html` add this block
``` python
# this in the head
<title>{% block head_title %}{% endblock %}</title>
{% block extra_head %}
{% endblock %}
# this in the footer
{% block extra_body %}
{% endblock %}
```
- now add the pagination `paginate_by = 10` add this to the view and in `home.html`
``` html
<!--Pagination-->

      {% if is_paginated %}
      <nav class="d-flex justify-content-center wow fadeIn">
        <ul class="pagination pg-blue">
            
          {% if page_obj.has_previous %}
          <li class="page-item">
            <a class="page-link" href="?page={{ page_obj.previous_page_number }}" aria-label="Previous">
              <span aria-hidden="true">&laquo;</span>
              <span class="sr-only">Previous</span>
            </a>
          </li>
          {% endif %}

          <li class="page-item active">
            <a class="page-link" href="?page={{ page_obj.number }}">{{ page_obj.number }}
              <span class="sr-only">(current)</span>
            </a>
          </li>

          {% if page_obj.has_next %}
          <li class="page-item">
            <a class="page-link" href="?page={{ page_obj.next_page_number }}" aria-label="Next">
              <span aria-hidden="true">&raquo;</span>
              <span class="sr-only">Next</span>
            </a>
          </li>
          {% endif %}
        </ul>
      </nav>
      {% endif %}

    </div>
  </main>
```
- now in `core/templatetags/cart_template_tags.py` i craeted this file will create a function we will use it everywhere and that's will return the orders items count if the user is authenticated
``` python
from django import template
from core.models import Order

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0
```
- and now in `navbar.html` i will use this method as filter pipe `{{ request.user|cart_item_count }}` and will pass the user as argument that way but load it first
``` html
{% load cart_template_tags %}

<nav class="navbar fixed-top navbar-expand-lg navbar-light white scrolling-navbar">
    <div class="container">

      <!-- Brand -->
      <a class="navbar-brand waves-effect" href="/">
        <strong class="blue-text">DJe-commerce</strong>
      </a>

      <!-- Collapse -->
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Links -->
      <div class="collapse navbar-collapse" id="navbarSupportedContent">

        <!-- Left -->
        <ul class="navbar-nav mr-auto">
          {% comment %} <li class="nav-item active">
            <a class="nav-link waves-effect" href="/">Home
              <span class="sr-only">(current)</span>
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link waves-effect" href="/checkout">
            Checkout</a>
          </li> {% endcomment %}
        </ul>

        <!-- Right -->
        <ul class="navbar-nav nav-flex-icons">
          {% if request.user.is_authenticated %}
          <li class="nav-item">
            <a class="nav-link waves-effect">
              <span class="badge red z-depth-1 mr-1"> {{ request.user|cart_item_count }} </span>
              <i class="fas fa-shopping-cart"></i>
              <span class="clearfix d-none d-sm-inline-block"> Cart </span>
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link waves-effect" href="{% url 'account_logout' %}">
              <span class="clearfix d-none d-sm-inline-block"> Logout </span>
            </a>
          </li>
          {% else %}
          <li class="nav-item">
            <a class="nav-link waves-effect" href="{% url 'account_login' %}">
              <span class="clearfix d-none d-sm-inline-block"> Login </span>
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link waves-effect" href="{% url 'account_signup' %}">
              <span class="clearfix d-none d-sm-inline-block"> Signup </span>
            </a>
          </li>
          {% endif %}
        </ul>
      </div>

    </div>
  </nav>
```
- and in the `login.html' i created my custom style
``` html
{% extends "account/base.html" %}
{% load i18n %}
{% load account socialaccount %}
{% load crispy_forms_tags %}

{% block head_title %}{% trans "Sign In" %}{% endblock %}

{% block content %}
  <main>
    <div class="container">
      <section class="mb-4">
        <div class="row wow fadeIn">
          <div class='col-6 offset-3'>
          <h1>{% trans "Sign In" %}</h1>

          {% get_providers as socialaccount_providers %}

          {% if socialaccount_providers %}
          <p>{% blocktrans with site.name as site_name %}Please sign in with one
          of your existing third party accounts. Or, <a href="{{ signup_url }}">sign up</a>
          for a {{ site_name }} account and sign in below:{% endblocktrans %}</p>

          <div class="socialaccount_ballot">

            <ul class="socialaccount_providers">
              {% include "socialaccount/snippets/provider_list.html" with process="login" %}
            </ul>

            <div class="login-or">{% trans 'or' %}</div>

          </div>

          {% include "socialaccount/snippets/login_extra.html" %}

          {% else %}
          <p>{% blocktrans %}If you have not created an account yet, then please
          <a href="{{ signup_url }}">sign up</a> first.{% endblocktrans %}</p>
          {% endif %}

          <form class="login" method="POST" action="{% url 'account_login' %}">
            {% csrf_token %}
            {{ form|crispy }}
            {% if redirect_field_value %}
            <input type="hidden" name="{{ redirect_field_name }}" value="{{ redirect_field_value }}" />
            {% endif %}
            <a class="btn btn-default" href="{% url 'account_reset_password' %}">{% trans "Forgot Password?" %}</a>
            <button class="btn btn-primary" type="submit">{% trans "Sign In" %}</button>
          </form>
          </div>
        </div>
      </section>
    </div>
  </main>

{% endblock %}
```
## Order summary view
- now in our `OrderItem` in `models.py` i added these functions
``` python
# this method will return the total price
 def get_total_item_price(self):
    return self.quantity * self.item.price

# if there's discount wwill return the total with discount
def get_total_discount_item_price(self):
    return self.quantity * self.item.discount_price

# will return how maney do you saved after discount
def get_amount_saved(self):
    return self.get_total_item_price() - self.get_total_discount_item_price()

# and this method will return the total with discount if there's discount
def get_final_price(self):
    if self.item.discount_price:
        return self.get_total_discount_item_price()
    return self.get_total_item_price()
```
- andn our `Order` in `models.py` i added this function
``` python
# this method will return the total price of all items 
 def get_total(self):
    total = 0
    for order_item in self.items.all():
        total += order_item.get_final_price()
    return total
```
- and in `views.py`
``` python
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from .models import Item, OrderItem, Order

# this will get the order of this user and pass this order to the context
class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")
```
- now in `urls.py`
``` python
from .views import (
    ItemDetailView,
    checkout,
    HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart
    remove_from_cart,
    remove_single_item_from_cart
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', checkout, name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart')
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart')
]
```
- and in `views.py` i added the login required for these methods and update the redirect in these method to be `return redirect("core:order-summary")`
``` python
@login_required
def add_to_cart(request, slug):

@login_required
def remove_from_cart(request, slug):

# then i created this method that will remove single item get the item and the user's order and get the order item just one value and if the quantity is bigger than one minus one and save else remove it
@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
```
- and added the link for that in the `navbar.html` 
``` html
<ul class="navbar-nav nav-flex-icons">
  {% if request.user.is_authenticated %}
  <li class="nav-item">
    <a class="nav-link waves-effect">
    <a href="{% url 'core:order-summary' %}" class="nav-link waves-effect">
      <span class="badge red z-depth-1 mr-1"> {{ request.user|cart_item_count }} </span>
      <i class="fas fa-shopping-cart"></i>
      <span class="clearfix d-none d-sm-inline-block"> Cart </span>
```
- then in `templates/order_summary.html` i displayed the context data
``` html
{% extends "base.html" %}

{% block content %}
  <main>
    <div class="container">

    <div class="table-responsive text-nowrap">
    <h2>Order Summary</h2>
    <table class="table">
        <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Item title</th>
            <th scope="col">Price</th>
            <th scope="col">Quantity</th>
            <th scope="col">Total Item Price</th>
        </tr>
        </thead>
        <tbody>
        {% for order_item in object.items.all %}
        <tr>
            <th scope="row">{{ forloop.counter }}</th>
            <td>{{ order_item.item.title }}</td>
            <td>{{ order_item.item.price }}</td>
            <td>
                <a href="{% url 'core:remove-single-item-from-cart' order_item.item.slug %}"><i class="fas fa-minus mr-2"></i></a>
                {{ order_item.quantity }}
                <a href="{% url 'core:add-to-cart' order_item.item.slug %}"><i class="fas fa-plus ml-2"></i></a>
            </td>
            <td>
            {% if order_item.item.discount_price %}
                ${{ order_item.get_total_discount_item_price }}
                <span class="badge badge-primary">Saving ${{ order_item.get_amount_saved }}</span>
            {% else %}
                ${{ order_item.get_total_item_price }}
            {% endif %}
            <a style='color: red;' href="{% url 'core:remove-from-cart' order_item.item.slug %}">
                <i class="fas fa-trash float-right"></i>
            </a>
            </td>
        </tr>
        {% empty %}
        <tr>
            <td colspan='5'>Your cart is empty</td>
        </tr>
        <tr>
            <td colspan="5">
            <a class='btn btn-primary float-right' href='/'>Continue shopping</a>
            </td>
        </tr>
        {% endfor %}
        {% if object.get_total %}
        <tr>
            <td colspan="4"><b>Order Total</b></td>
            <td><b>${{ object.get_total }}</b></td>
        </tr>
        <tr>
            <td colspan="5">
            <a class='btn btn-warning float-right ml-2' href='/checkout/'>Proceed to checkout</a>
            <a class='btn btn-primary float-right' href='/'>Continue shopping</a>
            </td>
        </tr>
        {% endif %}
        </tbody>
    </table>

    </div>

    </div>
  </main>

{% endblock content %}
```
## Handling billing address and Checkout
- first install `django-country`
- then in `models.py` import it 
``` python
# first import country
from django_countries.fields import CountryField

# second add the billing address to our order
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        'BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)

# third create the  billing address and ad the CountryField
class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
```
- now we will need to create our form `forms.py`
``` python
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Main St',
        'id': 'address'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or suite',
        'id': 'address-2'
    }))
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',

        }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'zip'
    }))
    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
```
- now in `views.py`
``` python
from .forms import CheckoutForm
from .models import Item, OrderItem, Order, BillingAddress

# will pass the form for our html and when we post data to the form we need to get the user's order and if the form is valid we will get all of these data and create a new billing address and assign this billing address to the billing address field in the Order and redirect to checkout
class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # TODO: add functionality for these fields
                # same_shipping_address = form.cleaned_data.get(
                #     'same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # TODO: add redirect to the selected payment option
                return redirect('core:checkout')
            messages.warning(self.request, "Failed checkout")
            return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:order-summary")
```
- then create the url in `urls.py`
``` python
from .views import (
    ItemDetailView,
    checkout,
    CheckoutView,
    HomeView,
    OrderSummaryView,
    add_to_cart,
)

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
```
- and in `checkout.html`
``` html
{% extends "base.html" %}
{% load crispy_forms_tags %}

{% block content %}

  <main >
    <div class="container wow fadeIn">

      <!-- Heading -->
      <h2 class="my-5 h2 text-center">Checkout form</h2>

      <!--Grid row-->
      <div class="row">

        <!--Grid column-->
        <div class="col-md-8 mb-4">

          <!--Card-->
          <div class="card">

            {% comment %} <form method='POST'>  
              {% csrf_token %}
              {{ form|crispy }}
              <button class='btn btn-primary' type='submit'>Checkout</button>
            </form> {% endcomment %}

            <!--Card content-->
            <form method="POST" class="card-body">
              {% csrf_token %}

              <!--address-->
              <div class="md-form mb-5">
                {% comment %} <input type="text" id="address" class="form-control" placeholder="1234 Main St"> {% endcomment %}
                {{ form.street_address }}
                <label for="address" class="">Address</label>
              </div>

              <!--address-2-->
              <div class="md-form mb-5">
                {% comment %} <input type="text" id="address-2" class="form-control" placeholder="Apartment or suite"> {% endcomment %}
                {{ form.apartment_address }}
                <label for="address-2" class="">Address 2 (optional)</label>
              </div>

              <!--Grid row-->
              <div class="row">

                <!--Grid column-->
                <div class="col-lg-4 col-md-12 mb-4">

                  <label for="country">Country</label>
                  {% comment %} <select class="custom-select d-block w-100" id="country" required>
                    <option value="">Choose...</option>
                    <option>United States</option>
                  </select> {% endcomment %}
                  {{ form.country }}
                  <div class="invalid-feedback">
                    Please select a valid country.
                  </div>

                </div>
                <!--Grid column-->

                <!--Grid column-->
                <div class="col-lg-4 col-md-6 mb-4">

                  <label for="zip">Zip</label>
                  {% comment %} <input type="text" class="form-control" id="zip" placeholder="" required> {% endcomment %}
                  {{ form.zip }}
                  <div class="invalid-feedback">
                    Zip code required.
                  </div>

                </div>
                <!--Grid column-->

              </div>
              <!--Grid row-->

              <hr>

              <div class="custom-control custom-checkbox">
                <input {% if form.same_shipping_address.value %}checked{% endif %} type="checkbox" class="custom-control-input" name="same_billing_address" id="same-address">
                <label class="custom-control-label" for="same-address">Shipping address is the same as my billing address</label>
              </div>
              <div class="custom-control custom-checkbox">
                <input {% if form.save_info.value %}checked{% endif %} type="checkbox" class="custom-control-input" name="save_info" id="save-info">
                <label class="custom-control-label" for="save-info">Save this information for next time</label>
              </div>

              <hr>

              <div class="d-block my-3">
                {% for value, name in form.fields.payment_option.choices %}
                <div class="custom-control custom-radio">
                  <input id="{{ name }}" name="payment_option" value="{{ value }}" type="radio" class="custom-control-input" required>
                  <label class="custom-control-label" for="{{ name }}">{{ name }}</label>
                  {% comment %} {{ form.payment_option }} {% endcomment %}
                </div>
                {% endfor %}
                {% comment %} <div class="custom-control custom-radio">
                  <input id="paypal" name="paymentMethod" type="radio" class="custom-control-input" required>
                  <label class="custom-control-label" for="paypal">Paypal</label>
                </div> {% endcomment %}
              </div>

              <hr class="mb-4">
              <button class="btn btn-primary btn-lg btn-block" type="submit">Continue to checkout</button>

            </form>

          </div>
          <!--/.Card-->

        </div>
        <!--Grid column-->

        <!--Grid column-->
        <div class="col-md-4 mb-4">

          <!-- Heading -->
          <h4 class="d-flex justify-content-between align-items-center mb-3">
            <span class="text-muted">Your cart</span>
            <span class="badge badge-secondary badge-pill">3</span>
          </h4>

          <!-- Cart -->
          <ul class="list-group mb-3 z-depth-1">
            <li class="list-group-item d-flex justify-content-between lh-condensed">
              <div>
                <h6 class="my-0">Product name</h6>
                <small class="text-muted">Brief description</small>
              </div>
              <span class="text-muted">$12</span>
            </li>
            <li class="list-group-item d-flex justify-content-between lh-condensed">
              <div>
                <h6 class="my-0">Second product</h6>
                <small class="text-muted">Brief description</small>
              </div>
              <span class="text-muted">$8</span>
            </li>
            <li class="list-group-item d-flex justify-content-between lh-condensed">
              <div>
                <h6 class="my-0">Third item</h6>
                <small class="text-muted">Brief description</small>
              </div>
              <span class="text-muted">$5</span>
            </li>
            <li class="list-group-item d-flex justify-content-between bg-light">
              <div class="text-success">
                <h6 class="my-0">Promo code</h6>
                <small>EXAMPLECODE</small>
              </div>
              <span class="text-success">-$5</span>
            </li>
            <li class="list-group-item d-flex justify-content-between">
              <span>Total (USD)</span>
              <strong>$20</strong>
            </li>
          </ul>
          <!-- Cart -->

          <!-- Promo code -->
          <form class="card p-2">
            <div class="input-group">
              <input type="text" class="form-control" placeholder="Promo code" aria-label="Recipient's username" aria-describedby="basic-addon2">
              <div class="input-group-append">
                <button class="btn btn-secondary btn-md waves-effect m-0" type="button">Redeem</button>
              </div>
            </div>
          </form>
          <!-- Promo code -->

        </div>
        <!--Grid column-->

      </div>
      <!--Grid row-->

    </div>
  </main>

{% endblock content %}
```
## Payment view with stripe
- first install `stripe`
- then in settings.py add the API_KEY `STRIPE_SECRET_KEY = ''` and add the `stripe` in the installed apps
- in `models.py` i added the payment field in the order model and created the payment model
``` python
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        'BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
```
- and in `views.py`
``` python
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone
from .forms import CheckoutForm
from .models import Item, OrderItem, Order, BillingAddress, Payment

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# now in checkout i will add the payment option and redirect to this url and pass this option as argument to our url
class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, "checkout.html", context)
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # TODO: add functionality for these fields
                # same_shipping_address = form.cleaned_data.get(
                #     'same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                
                # NEW CODE HERE
                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:order-summary")


# then i created the payment view that will pass the order to payment.html and will get the data from the post method in our html form and this data will return the stripe token and the amount then will try to charge stripe with amount and token and currency then create the payment model that will have the stripe charge id and the amount and the total then will make ordered to true because it's paid and assign the payment to our payment model otherwise will display the stripe error handlers
class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order
        }
        return render(self.request, "payment.html", context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)

        try:
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                source=token
            )

            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # assign the payment to the order

            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Your order was successful!")
            return redirect("/")

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "Rate limit error")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Not authenticated")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Network error")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(
                self.request, "Something went wrong. You were not charged. Please try again.")
            return redirect("/")

        except Exception as e:
            # send an email to ourselves
            messages.error(
                self.request, "A serious error occurred. We have been notifed.")
            return redirect("/")
```
- and in `urls.py`
``` python
from .views import remove_single_item_from_cart, PaymentView

path('payment/<payment_option>/', PaymentView.as_view(), name='payment')
```
- then create our `payment.html` file and in the javascript code you will pass the `publishable_key`
``` html
{% extends "base.html" %}

{% block extra_head %}
<style>
#stripeBtnLabel {
  font-family: "Helvetica Neue", Helvetica, sans-serif;
  font-size: 16px;
  font-variant: normal;
  padding: 0;
  margin: 0;
  -webkit-font-smoothing: antialiased;
  font-weight: 500;
  display: block;
}
#stripeBtn {
  border: none;
  border-radius: 4px;
  outline: none;
  text-decoration: none;
  color: #fff;
  background: #32325d;
  white-space: nowrap;
  display: inline-block;
  height: 40px;
  line-height: 40px;
  padding: 0 14px;
  box-shadow: 0 4px 6px rgba(50, 50, 93, .11), 0 1px 3px rgba(0, 0, 0, .08);
  border-radius: 4px;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.025em;
  text-decoration: none;
  -webkit-transition: all 150ms ease;
  transition: all 150ms ease;
  float: left;
  margin-left: 12px;
  margin-top: 28px;
}
button:hover {
  transform: translateY(-1px);
  box-shadow: 0 7px 14px rgba(50, 50, 93, .10), 0 3px 6px rgba(0, 0, 0, .08);
  background-color: #43458b;
}
#stripe-form {
  padding: 30px;
  height: 120px;
}
#card-errors {
  height: 20px;
  padding: 4px 0;
  color: #fa755a;
}
.stripe-form-row {
  width: 70%;
  float: left;
}
/**
 * The CSS shown here will not be introduced in the Quickstart guide, but shows
 * how you can use CSS to style your Element's container.
 */
.StripeElement {
  box-sizing: border-box;
  height: 40px;
  padding: 10px 12px;
  border: 1px solid transparent;
  border-radius: 4px;
  background-color: white;
  box-shadow: 0 1px 3px 0 #e6ebf1;
  -webkit-transition: box-shadow 150ms ease;
  transition: box-shadow 150ms ease;
}
.StripeElement--focus {
  box-shadow: 0 1px 3px 0 #cfd7df;
}
.StripeElement--invalid {
  border-color: #fa755a;
}
.StripeElement--webkit-autofill {
  background-color: #fefde5 !important;
}
</style>
{% endblock extra_head %}

{% block content %}

  <main >
    <div class="container wow fadeIn">

      <h2 class="my-5 h2 text-center">Payment</h2>

      <div class="row">

        <div class="col-md-12 mb-4">
          <div class="card">

            <script src="https://js.stripe.com/v3/"></script>

            <form action="." method="post" id="stripe-form">
                {% csrf_token %}
                <div class="stripe-form-row">
                    <label for="card-element" id="stripeBtnLabel">
                        Credit or debit card
                    </label>
                    <div id="card-element" class="StripeElement StripeElement--empty"><div class="__PrivateStripeElement" style="margin: 0px !important; padding: 0px !important; border: none !important; display: block !important; background: transparent !important; position: relative !important; opacity: 1 !important;"><iframe frameborder="0" allowtransparency="true" scrolling="no" name="__privateStripeFrame5" allowpaymentrequest="true" src="https://js.stripe.com/v3/elements-inner-card-19066928f2ed1ba3ffada645e45f5b50.html#style[base][color]=%2332325d&amp;style[base][fontFamily]=%22Helvetica+Neue%22%2C+Helvetica%2C+sans-serif&amp;style[base][fontSmoothing]=antialiased&amp;style[base][fontSize]=16px&amp;style[base][::placeholder][color]=%23aab7c4&amp;style[invalid][color]=%23fa755a&amp;style[invalid][iconColor]=%23fa755a&amp;componentName=card&amp;wait=false&amp;rtl=false&amp;keyMode=test&amp;origin=https%3A%2F%2Fstripe.com&amp;referrer=https%3A%2F%2Fstripe.com%2Fdocs%2Fstripe-js&amp;controllerId=__privateStripeController1" title="Secure payment input frame" style="border: none !important; margin: 0px !important; padding: 0px !important; width: 1px !important; min-width: 100% !important; overflow: hidden !important; display: block !important; height: 19.2px;"></iframe><input class="__PrivateStripeElement-input" aria-hidden="true" aria-label=" " autocomplete="false" maxlength="1" style="border: none !important; display: block !important; position: absolute !important; height: 1px !important; top: 0px !important; left: 0px !important; padding: 0px !important; margin: 0px !important; width: 100% !important; opacity: 0 !important; background: transparent !important; pointer-events: none !important; font-size: 16px !important;"></div></div>

                    <!-- Used to display form errors. -->
                    <div id="card-errors" role="alert"></div>
                </div>

                <button id="stripeBtn">Submit Payment</button>
            </form>

          </div>
        </div>

                <!--Grid column-->
        <div class="col-md-12 mb-4">

          <!-- Heading -->
          <h4 class="d-flex justify-content-between align-items-center mb-3">
            <span class="text-muted">Your cart</span>
            <span class="badge badge-secondary badge-pill">{{ order.items.count }}</span>
          </h4>

          <!-- Cart -->
          <ul class="list-group mb-3 z-depth-1">
            {% for order_item in order.items.all %}
            <li class="list-group-item d-flex justify-content-between lh-condensed">
              <div>
                <h6 class="my-0">{{ order_item.quantity }} x {{ order_item.item.title}}</h6>
                <small class="text-muted">{{ order_item.item.description}}</small>
              </div>
              <span class="text-muted">${{ order_item.get_final_price }}</span>
            </li>
            {% endfor %}
            <li class="list-group-item d-flex justify-content-between bg-light">
              <div class="text-success">
                <h6 class="my-0">Promo code</h6>
                <small>EXAMPLECODE</small>
              </div>
              <span class="text-success">-$5</span>
            </li>
            <li class="list-group-item d-flex justify-content-between">
              <span>Total (USD)</span>
              <strong>${{ order.get_total }}</strong>
            </li>
          </ul>
          <!-- Cart -->

        </div>
        <!--Grid column-->

      </div>

    </div>
  </main>


<script nonce="">  // Create a Stripe client.
  var stripe = Stripe('');
  // Create an instance of Elements.
  var elements = stripe.elements();
  // Custom styling can be passed to options when creating an Element.
  // (Note that this demo uses a wider set of styles than the guide below.)
  var style = {
    base: {
      color: '#32325d',
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: 'antialiased',
      fontSize: '16px',
      '::placeholder': {
        color: '#aab7c4'
      }
    },
    invalid: {
      color: '#fa755a',
      iconColor: '#fa755a'
    }
  };
  // Create an instance of the card Element.
  var card = elements.create('card', {style: style});
  // Add an instance of the card Element into the `card-element` <div>.
  card.mount('#card-element');
  // Handle real-time validation errors from the card Element.
  card.addEventListener('change', function(event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
      displayError.textContent = event.error.message;
    } else {
      displayError.textContent = '';
    }
  });
  // Handle form submission.
  var form = document.getElementById('stripe-form');
  form.addEventListener('submit', function(event) {
    event.preventDefault();
    stripe.createToken(card).then(function(result) {
      if (result.error) {
        // Inform the user if there was an error.
        var errorElement = document.getElementById('card-errors');
        errorElement.textContent = result.error.message;
      } else {
        // Send the token to your server.
        stripeTokenHandler(result.token);
      }
    });
  });
  // Submit the form with the token ID.
  function stripeTokenHandler(token) {
    // Insert the token ID into the form so it gets submitted to the server
    var form = document.getElementById('stripe-form');
    var hiddenInput = document.createElement('input');
    hiddenInput.setAttribute('type', 'hidden');
    hiddenInput.setAttribute('name', 'stripeToken');
    hiddenInput.setAttribute('value', token.id);
    form.appendChild(hiddenInput);
    // Submit the form
    form.submit();
  }
</script>

{% endblock content %}
```
## Coupon codes
- now in `models.py` i will add the coupon field in order model
``` python
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        'BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
        
    # and updated the total so if theres coupon will subtract it from the total
    total = 0
    for order_item in self.items.all():
        total += order_item.get_final_price()
    total -= self.coupon.amount
    return total

# then created the coupon model
class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code
```
- and in `admin.py`
``` python
from django.contrib import admin
from .models import Item, OrderItem, Order, Payment, Coupon

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
```
- then create the form that will submit our coupon code in `forms.py`
``` python
class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))
```
- now in `views.py`
``` python
from .forms import CheckoutForm, CouponForm
from .models import Item, OrderItem, Order, BillingAddress, Payment, Coupon

# i updated our checkout method so it will pass the coupon form and pass this variable `DISPLAY_COUPON_FORM` so if this variable is true we will display this form
class CheckoutView(View):
    try:
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = CheckoutForm()
        context = {
            'form': form,
            'couponform': CouponForm(),
            'order': order,
            'DISPLAY_COUPON_FORM': True
        }
        return render(self.request, "checkout.html", context)
    except ObjectDoesNotExist:
        messages.info(self.request, "You do not have an active order")
        return redirect("core:checkout

# and if there's a billing profile we will not display it and will return him back to checkout
# and after create the payment we will assign the payment to the order
 class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect("core:checkout")
            
      def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)
        try:
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                source=token
            )
            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()
            
            # NEW CODE HERE
            # assign the payment to the order

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

# then create the coupon method that will return the coupon with the passed coupon 
def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")

# now when we submit our coupon will get the coupon from the form and the order of this user and use the above method to return this coupon and add it to our order coupon field
class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")
```
- then create the url in `urls.py`
``` python
from .views import PaymentView,AddCouponView

path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
```
- then i created a new file call `oredr_snippet.html`
``` html
<div class="col-md-12 mb-4">
    <h4 class="d-flex justify-content-between align-items-center mb-3">
    <span class="text-muted">Your cart</span>
    <span class="badge badge-secondary badge-pill">{{ order.items.count }}</span>
    </h4>
    <ul class="list-group mb-3 z-depth-1">
    {% for order_item in order.items.all %}
    <li class="list-group-item d-flex justify-content-between lh-condensed">
        <div>
        <h6 class="my-0">{{ order_item.quantity }} x {{ order_item.item.title}}</h6>
        <small class="text-muted">{{ order_item.item.description}}</small>
        </div>
        <span class="text-muted">${{ order_item.get_final_price }}</span>
    </li>
    {% endfor %}
    <li class="list-group-item d-flex justify-content-between bg-light">
        <div class="text-success">
        <h6 class="my-0">Promo code</h6>
        <small>{{ order.coupon.code }}</small>
        </div>
        <span class="text-success">-${{ order.coupon.amount }}</span>
    </li>
    <li class="list-group-item d-flex justify-content-between">
        <span>Total (USD)</span>
        <strong>${{ order.get_total }}</strong>
    </li>
    </ul>

    {% if DISPLAY_COUPON_FORM %}
    <form class="card p-2" action="{% url 'core:add-coupon' %}" method="POST">
        {% csrf_token %}
        <div class="input-group">
            {{ couponform.code }}
            <div class="input-group-append">
            <button class="btn btn-secondary btn-md waves-effect m-0" type="submit">Redeem</button>
            </div>
        </div>
    </form>
    {% endif %}

</div>
```
- and included it in the `checkout.html`
``` html
{% extends "base.html" %}
{% load crispy_forms_tags %}

{% block content %}

  <main >
    <div class="container wow fadeIn">
      <h2 class="my-5 h2 text-center">Checkout form</h2>
      <div class="row">
        <div class="col-md-8 mb-4">
          <div class="card">
            <form method="POST" class="card-body">
              {% csrf_token %}

              <div class="md-form mb-5">
                {{ form.street_address }}
                <label for="address" class="">Address</label>
              </div>

              <div class="md-form mb-5">
                {{ form.apartment_address }}
                <label for="address-2" class="">Address 2 (optional)</label>
              </div>

              <div class="row">
                <div class="col-lg-4 col-md-12 mb-4">
                  <label for="country">Country</label>
                  {{ form.country }}
                  <div class="invalid-feedback">
                    Please select a valid country.
                  </div>
                </div>

                <div class="col-lg-4 col-md-6 mb-4">
                  <label for="zip">Zip</label>
                  {{ form.zip }}
                  <div class="invalid-feedback">
                    Zip code required.
                  </div>
                </div>

              </div>

              <hr>

              <div class="custom-control custom-checkbox">
                <input {% if form.same_shipping_address.value %}checked{% endif %} type="checkbox" class="custom-control-input" name="same_billing_address" id="same-address">
                <label class="custom-control-label" for="same-address">Shipping address is the same as my billing address</label>
              </div>
              <div class="custom-control custom-checkbox">
                <input {% if form.save_info.value %}checked{% endif %} type="checkbox" class="custom-control-input" name="save_info" id="save-info">
                <label class="custom-control-label" for="save-info">Save this information for next time</label>
              </div>

              <hr>

              <div class="d-block my-3">
                {% for value, name in form.fields.payment_option.choices %}
                <div class="custom-control custom-radio">
                  <input id="{{ name }}" name="payment_option" value="{{ value }}" type="radio" class="custom-control-input" required>
                  <label class="custom-control-label" for="{{ name }}">{{ name }}</label>
                </div>
                {% endfor %}
              </div>

              <hr class="mb-4">
              <button class="btn btn-primary btn-lg btn-block" type="submit">Continue to checkout</button>

            </form>

          </div>

        </div>

        <div class="col-md-4 mb-4">
          {% include "order_snippet.html" %}
        </div>

      </div>

    </div>
  </main>

{% endblock content %}
```
- and also added it in `payment.html`
- and updated our `order_summary.html` to display the coupon if exist
``` html
{% extends "base.html" %}

{% block content %}
  <main>
    <div class="container">

    <div class="table-responsive text-nowrap">
    <h2>Order Summary</h2>
    <table class="table">
        <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Item title</th>
            <th scope="col">Price</th>
            <th scope="col">Quantity</th>
            <th scope="col">Total Item Price</th>
        </tr>
        </thead>
        <tbody>
        {% for order_item in object.items.all %}
        <tr>
            <th scope="row">{{ forloop.counter }}</th>
            <td>{{ order_item.item.title }}</td>
            <td>{{ order_item.item.price }}</td>
            <td>
                <a href="{% url 'core:remove-single-item-from-cart' order_item.item.slug %}"><i class="fas fa-minus mr-2"></i></a>
                {{ order_item.quantity }}
                <a href="{% url 'core:add-to-cart' order_item.item.slug %}"><i class="fas fa-plus ml-2"></i></a>
            </td>
            <td>
            {% if order_item.item.discount_price %}
                ${{ order_item.get_total_discount_item_price }}
                <span class="badge badge-primary">Saving ${{ order_item.get_amount_saved }}</span>
            {% else %}
                ${{ order_item.get_total_item_price }}
            {% endif %}
            <a style='color: red;' href="{% url 'core:remove-from-cart' order_item.item.slug %}">
                <i class="fas fa-trash float-right"></i>
            </a>
            </td>
        </tr>
        {% empty %}
        <tr>
            <td colspan='5'>Your cart is empty</td>
        </tr>
        <tr>
            <td colspan="5">
            <a class='btn btn-primary float-right' href='/'>Continue shopping</a>
            </td>
        </tr>
        {% endfor %}
        {% if object.coupon %}
        <tr>
            <td colspan="4"><b>Coupon</b></td>
            <td><b>-${{ object.coupon.amount }}</b></td>
        </tr>
        {% endif %}
        {% if object.get_total %}
        <tr>
            <td colspan="4"><b>Order Total</b></td>
            <td><b>${{ object.get_total }}</b></td>
        </tr>
        <tr>
            <td colspan="5">
            <a class='btn btn-warning float-right ml-2' href='/checkout/'>Proceed to checkout</a>
            <a class='btn btn-primary float-right' href='/'>Continue shopping</a>
            </td>
        </tr>
        {% endif %}
        </tbody>
    </table>

    </div>

    </div>
  </main>

{% endblock content %}
```
## Order management and Refund
- in `models.py` i added new fields for the refound
``` python
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        'BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''
    
    # and update our method to subtract the coupon amount if there's coupon
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

# then create the refound model
class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"
```
- and in `admin.py`
``` python
from .models import Item, OrderItem, Order, Payment, Coupon, Refund

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

make_refund_accepted.short_description = 'Update orders to refund granted'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'billing_address',
                    'payment',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
```
- and in `forms.py` i created the refund form
``` python
class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()
```
- and in `views.py`
``` python
from .forms import CheckoutForm, CouponForm, RefundForm
from .models import Item, OrderItem, Order, BillingAddress, Payment, Coupon, Refund

import random
import string
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# this method will generate a random string
def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
    
# --------------- and in the paymentView - in the post method - in the try block
# i will assign the order code to our new string generator
# assign the payment to the order
order_items = order.items.all()
order_items.update(ordered=True)
for item in order_items:
    item.save()

order.ordered = True
order.payment = payment
order.ref_code = create_ref_code()
order.save()


# then create our refun view that will display our form and if the form is valid will get the order with that id and will make the requested to True and save and add the rfund to our order refund fields
class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("core:request-refund")
```
- now in `urls.py`
``` python
AddCouponView, RequestRefundView

path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
path('request-refund/', RequestRefundView.as_view(), name='request-refund')
```
- and in `order_snippet.html`
``` html
{% if order.coupon %}
<li class="list-group-item d-flex justify-content-between bg-light">
    <div class="text-success">
    <h6 class="my-0">Promo code</h6>
    <small>{{ order.coupon.code }}</small>
    </div>
    <span class="text-success">-${{ order.coupon.amount }}</span>
</li>
{% endif %}
```
- and in `request_refund.html`
``` html
{% extends "base.html" %}
{% load crispy_forms_tags %}

{% block content %}
  <main>
    <div class="container">

    <h2>Request Refund</h2>
    <form method="POST">
        {% csrf_token %}
        {{ form|crispy }}
        <button type='submit' class='btn btn-primary'>Submit</button>
    </form>

    </div>
  </main>

{% endblock content %}
```
## Default address functionality

















