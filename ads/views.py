from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserCreationForm, SaleAdCreationForm
from .models import SaleAd, WebsiteUser
from django.core.paginator import Paginator
from .utils import create_illustrations
from django.contrib import messages


@csrf_protect
def sign_in(request):
    if request.method == 'POST':
        form_class = LoginForm(request.POST)
        if form_class.is_valid():
            username = form_class.cleaned_data['username']
            password = form_class.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('ads:index')
            else:
                return redirect('ads:login')
    if request.user.is_authenticated:
        return redirect('ads:index')
    # form_class = LoginForm()
    return render(request, 'ads/login.html')


def logout_view(request):
    logout(request)
    return redirect('ads:login')


@login_required(login_url='/login/')
def index(request):
    latest_salead = SaleAd.objects.all()[:6]
    return render(request, 'ads/index.html', {'latest_salead': latest_salead})


@login_required(login_url='/login/')
def user_index(request):
    list_website_users = WebsiteUser.objects.all().order_by('-date_joined')
    paginator = Paginator(list_website_users, 6)
    page_number = request.GET.get('page') if request.GET.get('page') is not None else 1
    website_users = paginator.get_page(page_number)
    return render(request, 'ads/user/index.html', {'website_users': website_users,
                                                   'pages': [value + 1 for value in range(paginator.num_pages)],
                                                   'actual_page': int(page_number)})


@login_required(login_url='/login/')
def user_show(request, index_user: int):
    website_user = WebsiteUser.objects.get(pk=index_user)
    return render(request, 'ads/user/show.html', {'website_user': website_user})


@login_required(login_url='/login/')
def user_edit(request, index_user: int):
    website_user = WebsiteUser.objects.get(pk=index_user)
    return render(request, 'ads/user/edit.html', {'website_user': website_user})


@login_required(login_url='/login/')
def user_delete(request, index_user: int):
    if request.user.is_superuser:
        # website_user = WebsiteUser.objects.get(pk=index_user)
        messages.success(request, "User deleted with success.")
        return redirect('ads:user_index')
    messages.info(request, "You are not authorized to delete an user.")
    return redirect('ads:user_index')


@csrf_protect
@login_required(login_url='/login/')
def user_create(request):
    error = None
    if request.method == 'POST':
        form_class = UserCreationForm(request.POST)
        if form_class.is_valid():
            username = form_class.cleaned_data['username']
            password = form_class.cleaned_data['password']
            user = WebsiteUser.objects.create_user(username=username, password=password)
            if isinstance(user, WebsiteUser):
                return redirect('ads:user_show', user.id)
    form = UserCreationForm()
    return render(request, 'ads/user/create.html', {'form': form, 'error': error})


@login_required(login_url='/login/')
def salead_index(request):
    list_saleads = SaleAd.objects.all().order_by('-date_created')
    paginator = Paginator(list_saleads, 6)
    page_number = request.GET.get('page') if request.GET.get('page') is not None else 1
    saleads = paginator.get_page(page_number)
    return render(request, 'ads/salead/index.html', {'saleads': saleads,
                                                     'pages': [value + 1 for value in range(paginator.num_pages)],
                                                     'actual_page': int(page_number)})


@login_required(login_url='/login/')
def salead_show(request, index_salead):
    salead = SaleAd.objects.get(pk=index_salead)
    return render(request, 'ads/salead/show.html', {'salead': salead, 'illustrations': salead.illustrations.all()})


@login_required(login_url='/login/')
def salead_edit(request, index_salead):
    salead = SaleAd.objects.get(pk=index_salead)
    return render(request, 'ads/salead/edit.html', {'salead': salead})


@login_required(login_url='/login/')
def salead_delete(request, index_salead):
    salead = SaleAd.objects.get(pk=index_salead)
    return render(request, 'ads/salead/edit.html', {'salead': salead})


@csrf_protect
@login_required(login_url='/login/')
def salead_create(request):
    if request.method == 'POST':
        form_class = SaleAdCreationForm(request.POST, request.FILES)
        if form_class.is_valid():
            print(form_class.cleaned_data)
            title = form_class.cleaned_data['title']
            price = form_class.cleaned_data['price']
            description = form_class.cleaned_data['description']
            files = request.FILES.getlist('illustrations')
            salead = SaleAd.objects.create(title=title, price=price, description=description, author=request.user)
            illustrations = create_illustrations(files)
            if illustrations:
                salead.illustrations.add(illustrations, bulk=False)
                redirect('ads:salead_show', salead.id)
            # salead.illustration_set.set(illustrations)
    form = SaleAdCreationForm()
    return render(request, 'ads/salead/create.html', {'form': form})
