from django.shortcuts import render,redirect
from dashboard.models import UserSocial
import ast,requests

# Create your views here.



# url= "https://graph.facebook.com/v18.0/me/accounts?fields=id%2Cname%2Cpicture&access_token=EAATyJSzqOE8BO1kmQfTUqMBZB7iADU5k3yilR7dt3Qwjj6Bh3fBJNsCIaVn3PhMpKMCH08E2jhiAneRZCMUMtT2yNXG86qUQAgpWiaZCB7nfOrZAcciOHgRvfQZCAZBXevfmZAHWvMpHgFdn4MS642OsS0higJy6ZChtTCZAHgkzjL2q8YMfD0LI59JQZAIUz7a2u6wRgNNEZBUFaOvnCjdh9MeQ1DuxzA1YG6PzOL1CWjvBZCFzQX07ZAAqgB8leVx81CR7Ih0SyXtx6FgZDZD"

def facebook_page_verify(request):
    user=UserSocial.objects.filter(user_id=request.user.id,social_app='facebook')
    token=ast.literal_eval(user[0].data)['access_token']
    print("user id : ",user[0].user_id)


    if request.method=='POST':
        
        page_id=request.POST.get('page_id')
        print(page_id)

        user.update(page_id=page_id)
        
        if UserSocial.objects.filter(user_id=request.user.id,social_app='instagram').exists() == False:

            
            instaacc = "https://graph.facebook.com/v18.0/{}/?fields=connected_instagram_account&access_token={}".format(page_id, token)
            response=requests.get(instaacc).json()
            instaid=response["connected_instagram_account"]['id']
            data = "https://graph.facebook.com/v18.0/{}/?fields=id,name,profile_picture_url&access_token={}".format(instaid, token)

            print("connected insta ::  ",response["connected_instagram_account"]['id'])
            data=requests.get(data).json()
            data['access_token']=token
            instaobj=UserSocial.objects.create(social_app="instagram",user_id=user[0].user_id,page_id=instaid,data=data)
            instaobj.save()
        
        

        
        
        
        
        
        return redirect('/accounts/')

    # if UserSocial.objects.filter(user_id=request.user.id,social_app='instagram').exists():
    #     return redirect('/accounts/')

    
    # if UserSocial.objects.filter(user_id=request.user.id,social_app='facebook').exists():

    #     return render(request ,'/home/kunal/Desktop/Projects/SocioFy-project/sociofy/dashboard/templates/accounts.html')
    
    print("print access token == ",ast.literal_eval(user[0].data)['access_token'])

    base="https://graph.facebook.com/v18.0/me/accounts?fields=id%2Cname%2Cpicture&access_token="
    # response=requests.get(base+'id,name,picture&'+token)
    response=requests.get(base+token)
    page_select=response.json()





    
    
    return render(request, 'accounts.html',{'page_select':page_select})

