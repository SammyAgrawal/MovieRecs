from django.shortcuts import render
from .models import UserProfile, Movie, Rating
from .forms import UserForm, ProfileForm, RatingForm

from django.views.generic import ListView

#login stuff
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class Index(ListView):
    template_name = 'movies/index.html'
    queryset = sorted(Movie.objects.all(), key=lambda m: m.get_average_rating(), reverse=True)[:5]
    context_object_name = 'top_movies'

@login_required
def movies(request):
    return(render(request, 'movies/movie_page.html', context={'registered':False}))


def register(request):
    registered = False
    

    if(request.method == 'POST'):
        # new user has been registered
        userform = UserForm(data=request.POST)
        profileform = ProfileForm(data=request.POST)

        if(userform.is_valid() and profileform.is_valid()):
            #https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/#a-full-example
            
            user = userform.save() #.save() creates and saves a model object, 
            user.set_password(user.password)
            user.save()

            profile = profileform.save(commit=False)
            profile.user = user # form only has extra fields, match everything with userform data

            if('picture' in request.FILES):
                profile.picture = request.FILES['picture']
            
            profile.save()

            registered=True
        else:
            print("FORM ERROR")
    else:
        userform = UserForm()
        profileform = ProfileForm()

    c = {
        'userform': UserForm,
        'profileform' : ProfileForm,
        'registered' : registered,
    }

    return(render(request, 'movies/registration.html', context=c))



def user_login(request):
    
    if(request.method == 'POST'):
        username = request.POST.get('username') # standard HTML form, have to use get() for data
        password = request.POST.get('password')
        user = authenticate(username=username, password=password) #heavy lifting of whether real user

        if(user and user.is_active):
                login(request, user)
                return(HttpResponseRedirect(reverse('home')))
        else:
            return(HttpResponse("FAILED LOGIN"))

    c = {}
    return(render(request, 'movies/login.html', context=c))

@login_required
def user_logout(request):
    logout(request)
    return(HttpResponseRedirect(reverse('home')))