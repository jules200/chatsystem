from django.db import models
from login import settings
from accounts.models import MyUser

# Create your models here
class Feeds(models.Model):
    user = models.ForeignKey(MyUser, null=True, related_name="user_post", on_delete= models.SET_NULL)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return "%s"%self.id

class Feeds_comments(models.Model):
    user = models.ForeignKey(MyUser, null=True,  related_name="user_commet", on_delete= models.SET_NULL)
    feed = models.ForeignKey(Feeds, null=True, related_name="feed_comment", on_delete= models.SET_NULL)
    parent = models.ForeignKey('Feeds_comments', null=True, related_name="comment_comment", on_delete=models.SET_NULL)
    comment = models.CharField(max_length=100)
    likes = models.IntegerField(null=False, default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return self.comment

class Feeds_likes(models.Model):
    feed = models.ForeignKey(Feeds, null=True, related_name="feed_likes", on_delete= models.SET_NULL)
    user = models.ForeignKey(MyUser, null=True,  related_name="user_likes", on_delete= models.SET_NULL)
    status = models.IntegerField(null=False, default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return self.user

class Messages(models.Model):
    sender = models.ForeignKey(MyUser, null=True, related_name="sender",  on_delete= models.SET_NULL)
    receiver = models.ForeignKey(MyUser, null=True, related_name="receiver",  on_delete= models.SET_NULL)
    message = models.CharField(max_length=250)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return self.message    

class Images(models.Model):
    feed = models.ForeignKey(Feeds, null=True, related_name="feed_images", on_delete= models.SET_NULL)
    message = models.ForeignKey('Messages', related_name="message_images", null=True, on_delete=models.CASCADE)
    images = models.ImageField(null=True, upload_to='feeds/')

    def __str__ (self):
        return "%s"%self.feed_id
    
class Follower(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('follower', 'following')  # Prevent duplicate follows
        verbose_name = 'Follower'
        verbose_name_plural = 'Followers'

    def __str__(self):
        return f"{self.follower} follows {self.following}"
    
class Friendship(models.Model):
    user1 = models.ForeignKey(MyUser, related_name='friends_1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(MyUser, related_name='friends_2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user1', 'user2')
    def __str__(self):
        return f"{self.user1} & {self.user2}"