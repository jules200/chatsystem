from django import template
from main.models import *

main = template.Library()

@main.filter

def timeago(post_time):

    return post_time

@main.filter
def likecheck(feed_id, user_id):
    validlikes= Feeds_likes.objects.get(feed= feed_id, user=user_id)

    return validlikes.status