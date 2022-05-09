from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.utils.encoding import force_str
from .models import User
from .tokens import generate_token
import practice1.settings as settings
from django.db import transaction
# Create your views here.
from django.utils.http import urlsafe_base64_decode

# Celery
from .tasks import user_signed_up


def home(request):
    return render(request, "user/index.html")


@transaction.atomic()
def sigup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "This user name already exist! Please try again")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "This email already exist! Please try again")
            return redirect('home')

        if pass2 != pass1:
            messages.error(request, 'Password did not match')

        if not username.isalnum():
            messages.error(request, 'User name must be Alpha-Numeric!')
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.is_active = False
        myuser.save()
        messages.success(request, 'Your account has been register successfully. We have sent you a confirm email')

        user_signed_up.delay(request, myuser)
        return redirect('sigin')
    return render(request, 'user/sigup.html')


def sigin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            username = user.username
            return render(request, 'user/index.html', {'username': username})
        else:
            messages.success(request, 'Bad credential')
            return redirect('sigin')
    return render(request, 'user/sigin.html')


def sigout(request):
    # request.user.auth_token.delete()
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')
