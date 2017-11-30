from django.shortcuts import render,redirect
from firstapp.forms import UserForm,UserProfileInform

from .models import UserProfileInfo,User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login as auth_login,logout
from User.models import SellItemInfo

def error_404(request):
    return render(request,'firstapp/404.html')

def error_500(request):
    return render(request,'firstapp/404.html')

def index(request):
    items = SellItemInfo.objects.all()
    args = {'items' : items}
    return render(request,'firstapp/index.html', args,)



@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == "POST":
        userform = UserForm(data=request.POST)
        profileform = UserProfileInform(data=request.POST)

        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()

            profile = profileform.save(commit=False)
            profile.user = user

            if 'profilepic' in request.FILES:
                profile.profilepic = request.FILES['profilepic']

            profile.save()
            registered = True

        else :
            print('Not possible')
    else:
        userform = UserForm()
        profileform = UserProfileInform()

    return render(request,'firstapp/registration.html',
    {
        'userform':userform,
        'profileform':profileform,
        'registered':registered
    })


def userlogin(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        global userName

        userName = username
        user = authenticate(username=username,password=password)


        if user:
            if user.is_active:
                auth_login( request , user )
                return redirect('/User/home/')
            else:
                return HttpResponse("Account is not active")
        else:
            context = {
                'Notice':'Please User Correct UserName or Password'

            }
            return render(request,'firstapp/login.html',context)
    else:
        return render(request,'firstapp/login.html')
