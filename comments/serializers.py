from things.models import Thing
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    user_name = serializers.StringRelatedField(many=False, source = 'user')


    class Meta:
        model = Comment
        fields = ('id', 'content', 'user_name', 'user')