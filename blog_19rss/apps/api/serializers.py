# -*- coding: utf-8 -*-
# @AuThor  : frank_lee
from rest_framework import serializers
from storm.models import Article, Tag, Category
from user.models import Ouser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ouser
        fields = ('id', 'username', 'first_name', 'link', 'avatar')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    keywords = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = Article
        exclude = ('body',)

