from rest_framework import serializers
from .models import Project, Review, Tag
from profiles.models import Profile


class TagSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ReviewSerilaizer(serializers.ModelSerializer):
    owner = ProfileSerializer(many = False)
    project = 'ProjectSerializer(many = False)'
    class Meta:
        model = Review
        fields = '__all__'

class ProjectSerilaizer(serializers.ModelSerializer):
    owner = ProfileSerializer(many = False, read_only = True)
    tags = TagSerilaizer(many = True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerilaizer(reviews, many = True)
        return serializer.data

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')

        instance.tags.all().delete()

        for tag in tags:
            t, created = Tag.objects.get_or_create(name=tag['name'])
            instance.tags.add(t)

        return super().update(instance, validated_data)
