from rest_framework import serializers
from .models import Feeds, Images

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id', 'image']

class FeedSerializer(serializers.ModelSerializer):
    # images = ImageSerializer(many=True, read_only=True) 

    class Meta:
        model = Feeds
        fields = ['id', 'user', 'text', 'added_at']
        read_only_fields = ['user', 'added_at']