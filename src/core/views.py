from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect 
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Movie, MovieList
import re
# Create your views here.

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "The email you entered does exsist")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return redirect('signup')               
            else:
                user = User(username=username, email=email, password=password)
                user.save()
                return redirect('login')
            
        else:
            messages.info(request, "Passwords don't match")
            return redirect('signup')
    else:
        return render(request, 'signup.html', {})
    
    
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user=user)
            return render(request, "index.html")
        else:
            messages.info(request, "failed to login please try again")
            return redirect('login')
            
    else:
        return render(request, "login.html" )
        

login_required(login_url='login')
def index(request):
    movies = Movie.objects.all()
    featured_movie = movies.last()
    context = {
        "movies":movies,
        "featured_movie":featured_movie
        
    }
    return render(request, 'index.html',context)

login_required(login_url='login')
def my_list(request):
    movie_list = MovieList.objects.select_related('movie').filter(owner_user=request.user)
    user_movie_list = [ml.movie for ml in movie_list]
    context = {
        'movies':user_movie_list
    }
    return render(request, 'my_list.html', context)

login_required(login_url='login')
def add_to_list(request):
    if request.method == 'POST':
        movie_url_id = request.POST.get('movie_id')
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        match = re.search(uuid_pattern, movie_url_id)
        movie_id = match.group() if match else None

        movie = get_object_or_404(Movie, uu_id=movie_id)
        movie_list, created = MovieList.objects.get_or_create(owner_user=request.user, movie=movie)

        if created:
            response_data = {'status': 'success', 'message': 'Added ✓'}
        else:
            response_data = {'status': 'info', 'message': 'Movie already in list'}

        return JsonResponse(response_data)
    else:
        # return error
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

login_required(login_url='login')
def movie(request, uu_id):
    movie = Movie.objects.get(uu_id=uu_id)
    return render(request, 'movie.html',{'movie_details':movie})

def genre(request,genre):
    movie_genre = genre
    movies_genre_based = Movie.objects.filter(genre=movie_genre)
    context = {
        'movies':movies_genre_based,
        'movie_genre': movie_genre
    }
    return render(request, "genre.html", context)



def search(request):
    if request.method == "POST":
        search_term = request.POST['search_term']
        movies = Movie.objects.filter(title__icontains= search_term)
        context = {
            'movies':movies,
            'search_term':search_term
        }
        return render(request, 'search.html', context)
    else:
        return redirect('index')
    
    
login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')