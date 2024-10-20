from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from accounts.models import MyUser
from django.db.models import Q
from .models import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import generics, permissions
from .serializers import FeedSerializer

# Create your views here.

@login_required(login_url='login')
def main(request):

    feed=Feeds.objects.all().order_by('-id')   

    return render(request, 'main/feeds.html',{'feeds':feed})

@login_required()
def newpost(request):
    if request.method == "POST":
        photos = request.FILES.getlist('images')
        text = request.POST.get('feed_text')
        post_model = Feeds(user=request.user, text=text)
        post_model.save()
                
        for picture in photos:
            obj = Images(feed=post_model, images = picture)
            obj.save()
        return redirect("main")
            
    return render(request, 'main/newpost.html')

@login_required()      
def deletepost(request, post_id):
    obj = Feeds.objects.get(pk=post_id)
    obj.delete()
    if obj:
        return redirect("main")
    
def insert_comment(request):
    if request.method == "POST":
        comment = request.POST['comment']
        feed_id = request.POST['feed_id']
        feed = get_object_or_404(Feeds, id=feed_id)
        # user = request.user.id
        muser = get_object_or_404(MyUser, id=request.user.id)
        
        obj=comments()
        obj.user=request.user
        obj.feed=feed
        obj.comment=comment
        obj.save()

        return redirect('feeds')
    return HttpResponse("insert ")

def messages(request):
    return HttpResponse("message")

def friends(request):
    template_name = "main/friends.html"
    friends = Friendship.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    )
    friends_ids=[]
    for f_id in friends:
        if f_id.user1 == request.user:
            friends_ids.append(f_id.user2_id)
        else:
            friends_ids.append(f_id.user1_id)
            
    print(friends_ids)
            
    all_friends=MyUser.objects.filter(id__in=friends_ids)
            
    context={
        "friends": all_friends,
    }
    return render(request, template_name, context)

def new_friends(request):
    template_name="main/new_friends.html"
    
    user_id = request.GET.get('user_id')

    if user_id:
        get_user = MyUser.objects.get(pk=user_id)
        
        obj =Friendship(user1=get_user, user2=request.user)
        obj.save()
        if obj:
            return redirect('new_friends')
        else:
            return HttpResponse("Noooo")
    
    friends = Friendship.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).values_list('user1', 'user2')
    # friend_ids = set(friend_id for pair in friends for friend_id in pair)
    friend_ids = set()

    for pair in friends:
        for friend_id in pair:
            friend_ids.add(friend_id)
    unfriend_user=MyUser.objects.exclude(id__in=friend_ids).exclude(id=request.user.id)
    
    context={
        "users": unfriend_user
    }
    return render(request, template_name, context)

def followers(request):
    return HttpResponse("followers")

def follow_user(request):
    return HttpResponse("follow_user")

def unfollow_user(request):
    return HttpResponse("unfollow_user")

def feedlikes(request, feed_id):
    if request.method == 'GET':
        validlikes= Likescount.objects.filter(feed= feed_id, user=request.user.id)
        feed_update= Feeds.objects.get(pk=feed_id)
        if validlikes:
            validlikes= Likescount.objects.get(feed= feed_id, user=request.user.id)
            likes_status=validlikes.status
            if likes_status == 0:
                feed_update.likes = feed_update.likes +1
                feed_update.save()
                if feed_update:
                    validlikes.status = 1
                    validlikes.save()
                    if validlikes:
                        return HttpResponse(feed_update.likes)
            else:
                feed_update.likes = feed_update.likes -1
                feed_update.save()
                if feed_update:
                    validlikes.status = 0
                    validlikes.save()
                    if validlikes:
                        return HttpResponse(feed_update.likes) 
            return HttpResponse(feed_update.likes)
        else:
            feed_update.likes = feed_update.likes +1
            feed_update.save()
            if feed_update:
                obj = Likescount(feed=feed_id, user=request.user.id)
                obj.save()
                if obj:
                    return HttpResponse(feed_update.likes)
                else:
                    return HttpResponse("byanze")
            else:
                return HttpResponse("Not Done")
            
    return HttpResponse("Access Restricted")

class FeedListCreateView(generics.ListCreateAPIView):
    queryset = Feeds.objects.all()
    serializer_class = FeedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Associate the post with the logged-in user
        serializer.save(user=self.request.user)

class FeedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feeds.objects.all()
    serializer_class = FeedSerializer
    permission_classes = [permissions.IsAuthenticated]


        