from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from dashboard.models import UserSocial
from django.contrib.auth.decorators import login_required
from dashboard.instafetch import get_comments
# from sociofy.dashboard.instafetch import *
import ast



# Create your views here.



@login_required
def success(request):
    return render(request,'success.html')


base="https://graph.facebook.com/v18.0/me/accounts?fields="


# url= "https://graph.facebook.com/v18.0/me/accounts?fields=  id%2Cname%2Cpicture&access_token=EAATyJSzqOE8BO2zRUWSudm1vtb3R0AFny2ghTRwTQbsy2nwOR3bTSF98OnvotYzohYumaYQg1edSLnyobbU52AesEp65T1mE1ehuBHEA96Ln1Ic0wOMwo5vGljQMWvXnJ0XAZCW9X9Uyk8hmnmUTwtuyaJKzrKsFwzwkh1zv8ml2pQOSfmjNs7QASATYHbYBokWDkxMl0ZBRd7dngBgXy2iZCu8HUOF7OePntSfjAZDZD"

def instagram_verify(request):

 
    
    return render(request, 'accounts.html')

def remove(request):
    
    socials = UserSocial.objects.filter(user_id=request.user)
    socials.delete()

    return redirect("/accounts/")


def gen_reply(request):
    if request.method=="GET":
        id=request.GET.get('id')
        print(id)
        facebook = UserSocial.objects.filter(user_id=request.user,social_app="facebook")
        # access_token=facebook[0].data
        # #print("id",id,"access : ",access_token)
        access_token= ast.literal_eval(facebook[0].data)["access_token"]
        comments_list=get_comments(post_id=id,access_token=access_token)
        
        
        context={"comments_list":comments_list} 
        return render(request, "gen_reply.html",context)

    
    if request.method=="POST":
        value=request.POST.get('comment_id')
        
        return JsonResponse({"value":value})
    
    # return render(request, "gen_reply.html",context)
# def accounts(request):

#     if str(request.user)=='AnonymousUser':
#         social_accounts=[]

#     else :
#         social_accounts = UserSocialAuth.objects.filter(user=request.user)


#     return render(request, 'accounts.html',{'social_accounts': social_accounts})


