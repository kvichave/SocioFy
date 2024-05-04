from django.shortcuts import render,redirect
from django.http import HttpResponse
from  .models import UserSocial
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
import json
import ast
from .instafetch import *
import plotly.graph_objects as go
from django.core.cache import cache


def home(request):
    return render(request, 'Home.html')


def userlogin(request):

    if request.method == "POST":

        username=request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user is None:
            messages.error(request,"Invalid Credentials")
            return redirect('/login/')
        
        else:   
            login(request,user)
            return redirect('/accounts/')

        
        

    return render(request,'login.html')


def userregister(request):
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')

        user = User.objects.filter(username=name)

        if user.exists():
            messages.error(request,"Username already exist")
            return redirect('/register/')
        

        user = User.objects.create(
            username=name,
            email=email
        )
        user.set_password(password)

        user.save()

        messages.info(request,"User created successfully")


        return redirect('/login/')

    return render(request,'register.html')


@login_required(login_url='/login/')
def accounts(request):
    
    if str(request.user)=='AnonymousUser':
        social_accounts=[]
        
    else :
        social_accounts = UserSocial.objects.filter(user_id=request.user)

    facebook_flag=False
    instagram_flag=False
    insta_profile_img=""
    for account in social_accounts:
        
        if 'facebook' in account.social_app:
            facebook_flag=True
        
        if "instagram" in account.social_app:
            instagram_flag=True
            account.page_id
            insta_profile_img = ast.literal_eval(account.data)["profile_picture_url"]
    
    

    return render(request, 'accounts.html',{'social_accounts': social_accounts, 'facebook_flag':facebook_flag,"instagram_flag":instagram_flag,"insta_profile_img":insta_profile_img})


global gender_data
gender_data=""

global gender_fig
gender_fig=""

global age_data
age_data=""

global age_fig
age_fig=""

global city_data
city_data=""

global city_fig
city_fig=""

global country_data
country_data=""

global country_fig
country_fig=""

global images
images=""

global videos
videos="" 

global comments_dir   
comments_dir=""   

global media_list  
media_list = []

global comments_list 
comments_list = []

global response_list  
response_list = []

global media_url
media_url=[]



def analytics(request):
    

    
    

    cached_data = cache.get('cached_data')
    if cached_data is not None:
        
            return render(request, 'analytics.html',cached_data)
    
    else:

        instagram = UserSocial.objects.filter(user_id=request.user,social_app="instagram")
        if instagram.exists:
            facebook = UserSocial.objects.filter(user_id=request.user,social_app="facebook")
            id=instagram[0].page_id
            access_token=facebook[0].data
            access_token= ast.literal_eval(facebook[0].data)["access_token"]
            
            

            
            gender_data,gender_fig=gender_func(insta_id=id,access_token=access_token)
            gender_fig=gender_fig.to_json()
            
            age_data,age_fig=age_func(insta_id=id,access_token=access_token)
            age_fig=age_fig.to_json()

            
            city_data,city_fig=city_func(insta_id=id,access_token=access_token)
            city_fig=city_fig.to_json()

            country_data,country_fig=country_func(insta_id=id,access_token=access_token)
            country_fig=country_fig.to_json()
            
            
            postana_data,postana_fig=postsanalytics(insta_id=id,access_token=access_token)
            postana_fig=postana_fig.to_json() 
            comments_dir = comment_analysis(insta_id=id,access_token=access_token)
            
            
            
    

            images,videos=posts_url(insta_id=id,access_token=access_token)
            media_url=media_urls(insta_id=id,access_token=access_token)
            
            for i in comments_dir.keys():
                comments_dir[i]+=[media_url[i]]
            
            context={"media_url":media_url,'comments_dir':comments_dir,"videos":videos,"images":images,"postana_fig":postana_fig,'gender_data':gender_data,   'gender_fig' :gender_fig,  'age_data'  :age_data,   'age_fig' :age_fig,  'city_data' : city_data,    'city_fig':city_fig,   'country_data' :country_data,   'country_fig' :country_fig}       
            
            cache.set('cached_data', context)
            
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(comments_dir, f, ensure_ascii=False, indent=4)
            
            return render(request, 'analytics.html',context)
        else:
            return redirect('/accounts/')
            
            
