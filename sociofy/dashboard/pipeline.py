from django.contrib.auth.models import User
from .models import *
from django.http import HttpResponse
from django.shortcuts import render,redirect




def save_access_token(backend, details, response, user, *args, **kwargs):
    # print("In save access token")
        # Extract the access token
        # print("in if block of save access token")
        # print("backend :::::::::::  ",backend.name)
        # print("backend :::::::::::  ",response)
        
        # print("user id ::::::: ",user.id)



        query=UserSocial.objects.filter(user_id=user.id,social_app=backend.name)


        if query.exists():
            print(query.exists(),"in exist starting")
            query=UserSocial.objects.filter(user_id=user.id,social_app=backend.name).update(data=response)
            print(query," is the update value ")
            print("in exist end")

        else:
            print("in else starting")

            query = UserSocial.objects.create(
                user_id=user.id,
                social_app=backend.name,
                data = response

            )
            query.save()
            print("in exist end")






    



    
        

        # print("backend :::::::::::  ",)
        # access_token = response.get('access_token')

        # print(access_token)

        # Save the access token in your user model or any other storage mechanism
        # user.access_token = access_token
        # user.save()
            



def custom_redirect(backend, details, response, user, *args, **kwargs):
    if backend.name == 'facebook' or backend.name == 'instagram':
        return redirect('/facebook/page/')