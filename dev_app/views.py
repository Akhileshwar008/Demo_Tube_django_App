from django.shortcuts import render
from django.http import HttpResponse
import requests
from dev_app.models import Users
import jwt
from datetime import datetime, timedelta
# Create your views here.

# def Register(request):
# 	return HttpResponse('Register')

# def Login(request):
# 	return HttpResponse('Login')

# def SignUp(request):
# 	return HttpResponse('SignUp')
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

SECRET_KEY="thfydtrxrerertcygbhbu"

@csrf_exempt
def home(request):
    # print(dict(request.POST.lists()))
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'
    search_params = {
    'part' : 'snippet',
    'q':request.POST.get('search',False),
    'key': settings.YOUTUBE_DATA_API_KEY,
    'maxResults' : 10,
    'type' : 'video'
    
    }
    # if request.method == 'POST':
        
    video_ids = []
    r = requests.get(search_url, params=search_params)
    print(r.text)
    results = (r.json())['items']
    
    video_ids = []
    for result in results:
        video_ids.append(result['id']['videoId'])
    
    # if request.POST.get('submit',False)=='lucky':
    #     return redirect(f'https://www.youtube.com/watch?v={video_ids[0]}')
        
    
    videos_params = {
        'key': settings.YOUTUBE_DATA_API_KEY,
        'part' : 'snippet',
        'id': ','.join(video_ids)
        
    }
    
    r = requests.get(video_url, params=videos_params)
    results = r.json()['items']
    # print(results)
    videos = []
    for result in results:
        print(result)
        video_data = {
            'title' : result['snippet']['title'],
            'id' :result['id'],
            'url':f'https://www.youtube.com/watch?v={result["id"]}',
            'thumbnail' : result['snippet']['thumbnails']['high']['url']  
        }
        # print(video_data)
        videos.append(video_data)
    context = {
        'videos' :videos
        }
    return render(request,'registration/home.html',{'context':context}) 
    
def login(request):
    return render(request,'registration/login.html')
@csrf_exempt
def loginsuccess(request):
    if request.method == 'POST':
        email=request.POST.get("email",None)
        password=request.POST.get('password',None)
        for user in Users.objects.all():
            if email==user.email and password==user.password:
                token = jwt.encode(
                {
                    "user": user.email,
                    "exp": datetime.utcnow() + timedelta(minutes=15),
                },
                SECRET_KEY,
            )
            session["token"] = token
                return render(request,'registration/home.html')
        # return render(request,'registration/login.html')
        return redirect('/login')

def signup(request):
    return render(request,'registration/signup.html')

@csrf_exempt
def signupsuccess(request):
    if request.method == 'POST':
        email=request.POST.get("email",None)
        password=request.POST.get('password',None)
        sex=request.POST.get('sex',None)
        name=request.POST.get('name',None)
        for user in Users.objects.all():
            if name==user.name:
                return HttpResponse("User already present")
            
        Users(email,name,password,sex).save()
        return redirect('/login')
        # if email=="akhil@innovaccer.com" and password=="123":
        #     print("Welcome")
        #     return redirect('/home')
        # return redirect('/')