from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from accounts.forms import PaymentForm, ProfileForm, MyUserForm
from accounts.models import Payment


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # successful login
            login(request, user)
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next'))
            return HttpResponseRedirect(reverse('ticketing:showtime_list'))
        else:
            # undefined user or incorrect password
            context = {
                'username': username,
                'error': "کاربری با این مشخصات یافت نشد."
            }
    else:
        if request.user.is_authenticated:
            # user is logged in.
            return HttpResponseRedirect(reverse('ticketing:showtime_list'))
        context = {}
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    # if there is a logged-in request's user, this function make it to logout.
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))


@login_required
def profile_details(request):
    profile = request.user.profile
    context = {
        'profile': profile
    }
    return render(request, 'accounts/profile_details.html', context)


@login_required
def payment_list(request):
    payments = Payment.objects.filter(profile=request.user.profile).order_by('-transaction_time')
    context = {
        'payments': payments
    }
    return render(request, 'accounts/payment_list.html', context)


@login_required
def payment_create(request):
    if request.method == 'POST':
        # bound form
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save(
                commit=False)  # this returns an object so we stored this object in payment variable.
            payment.profile = request.user.profile
            payment.save()
            request.user.profile.deposit(payment.amount)
            return HttpResponseRedirect(reverse('accounts:payment_list'))
    else:
        # unbound form
        payment_form = PaymentForm()
    context = {
        'payment_form': payment_form
    }
    return render(request, 'accounts/payment_create.html', context)


@login_required
def profile_edit(request):
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, files=request.FILES, instance=request.user.profile)
        user_form = MyUserForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return HttpResponseRedirect(reverse("accounts:profile_details"))
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        user_form = MyUserForm(instance=request.user)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/profile_edit.html', context)
