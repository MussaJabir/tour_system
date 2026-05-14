from rest_framework import serializers
from .models import Review, ReviewPhoto


class ReviewPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewPhoto
        fields = ['id', 'photo', 'caption', 'order']


class ReviewListSerializer(serializers.ModelSerializer):
    photos = ReviewPhotoSerializer(many=True, read_only=True)
    package_name = serializers.CharField(source='package.name', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'package', 'package_name', 'reviewer_name', 'reviewer_country',
            'rating', 'title', 'body', 'featured', 'photos', 'created_at',
        ]


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['package', 'rating', 'title', 'body', 'reviewer_name', 'reviewer_country']

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value
