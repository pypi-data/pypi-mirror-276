from django.contrib import auth, messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from .forms import UserLoginForm, UserRegistrationForm
from .models import Order


def home(request):
    # if request.user.is_anonymous:
    #     return HttpResponseRedirect(reverse('main:signin'))

    return render(request, "main/index.html")


def signin(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                if user.is_superuser:
                    return HttpResponseRedirect(reverse('admin:index'))
                return HttpResponseRedirect(reverse('main:home'))
    else:
        form = UserLoginForm()
    context = {
        'form': form,
    }
    return render(request, 'main/signin.html', context)


def signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поздравляем! Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('main:signin'))
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'main/signup.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:signin'))


def new_order(request):
    # if request.method == "POST":
    #     form = PaperForm(data=request.POST)
    #     if form.is_valid():
    #         form.instance.user_creator = request.user
    #         form.save()
    #         messages.success(request, 'Вы успешно создали заявление!')
    #         return HttpResponseRedirect(reverse('main:home'))
    # else:
    #     form = PaperForm()
    context = {
        # 'form': form,
    }
    return render(request, 'main/new_order.html', context)


class RobotsTxtView(TemplateView):
    template_name = "main/robots.txt"


class SitemapXmlView(TemplateView):
    template_name = "main/sitemap.xml"


def orders(request):
    ordersData = Order.objects.filter(user_creator=request.user)
    context = {
        "orders": ordersData
    }
    return render(request, 'main/orders.html', context)


def contacts(request):
    return render(request, 'main/contacts.html')
