from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Feeds)
class FeedsAdmin(admin.ModelAdmin):
    # def has_add_permission(self, request):
    #     return False
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.has_perm('feed.can_view_feeed'):
            queryset = queryset.none()
        return queryset

@admin.register(Feeds_comments)
class Feeds_commentsAdmin(admin.ModelAdmin):
    pass

@admin.register(Feeds_likes)
class Feeds_likesAdmin(admin.ModelAdmin):
    pass

@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    pass
