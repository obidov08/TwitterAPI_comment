from rest_framework import serializers
from TwitterAPI.models import Post, Media


class PostCreatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fieldds = ('content', )


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fieldds = ('post_id', 'media', )



