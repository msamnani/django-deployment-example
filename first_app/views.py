from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from first_app.models import Topic,Webpage,AccessRecord,FirstAppUser
from . import forms
from first_app.forms import NewUserForm, UserForm, UserProfileInfoForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def index(request):
    return render(request,'first_app/index.html')

def staticandfilter(request):
    my_dict = {'insert_me':"Hello I am from views.py",'text':'Hello World!','number':100}
    return render(request, 'first_app/staticandfilter.html', context=my_dict)

def help(request):
    return HttpResponse("<em>Help Page</em>")

def sites(request):

    webpages_list = AccessRecord.objects.order_by('date')
    date_dict = {'access_records':webpages_list}
    return render(request, 'first_app/sites.html', context=date_dict)

def users(request):

    users_list = FirstAppUser.objects.order_by('first_name')
    user_dict = {'users':users_list}
    return render(request, 'first_app/users.html', context=user_dict)

def form_name_view(request):
    form = forms.FormName()
    if request.method == 'POST':
        form = forms.FormName(request.POST)
        if form.is_valid():
            print("VALIDATION SUCCESS!")
            print("NAME: "+ form.cleaned_data['name'])
            print("EMAIL: "+ form.cleaned_data['email'])
            print("TEXT: "+ form.cleaned_data['text'])
    return render(request,'first_app/form_page.html',{'form':form})

def signup(request):

    newform = NewUserForm()

    if request.method == "POST":
        form = NewUserForm(request.POST)
    
        if form.is_valid():
           form.save(commit=True)
           return users(request)
        else:
            print("ERROR FROM INVALID")

    return render(request, 'first_app/signup.html', {'form':newform})

def other(request):
    return render(request,'first_app/other.html')

def relative(request):
    return render(request,'first_app/relative_url_templates.html')

def firstappindex(request):
    return render(request,'first_app/firstappindex.html')

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user.form.errors, profile_form.errors)
        
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'first_app/registration.html',
                            {'user_form':user_form,
                            'profile_form':profile_form,
                            'registered':registered})

def user_login(request):

    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('first_app:firstappindex'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied!")
    else:
        return render(request,'first_app/login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('first_app:firstappindex'))

@login_required
def special(request):
    return HttpResponse("You are logged in NICE!")

