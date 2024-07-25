from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post, Review

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['_id', 'username', 'email', 'name', 'isAdmin']

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name
        if not name:
            name = obj.email
        return name

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['_id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

class ReviewSerializer(serializers.ModelSerializer):
    video_review = serializers.SerializerMethodField()
    customer_photo = serializers.SerializerMethodField()
    review_image = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['customer_name', 'customer_email', 'customer_photo',"review_image",'text_review', 'video_review', 'created_at',"my_id"]

    def get_video_review(self, obj):
        request = self.context.get('request')
        if obj.video_review:
            return request.build_absolute_uri(obj.video_review.url)
        return None

    def get_customer_photo(self, obj):
        request = self.context.get('request')
        if obj.customer_photo:
            return request.build_absolute_uri(obj.customer_photo.url)
        return None
    
    def get_review_image(self, obj):
        request = self.context.get('request')
        if obj.review_image:
            return request.build_absolute_uri(obj.review_image.url)
        return None

class PostSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['user', 'title', 'content', 'image', 'slug', 'created_at', 'reviews']

    def get_reviews(self, obj):
        reviews = obj.reviews.order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True, context=self.context)
        return serializer.data

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            image_url = request.build_absolute_uri(obj.image.url)
            print(f"Generated Image URL: {image_url}")  # Log the generated URL
            return image_url
        return None
