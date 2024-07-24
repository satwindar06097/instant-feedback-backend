from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from testimonial.models import Post, Review
from testimonial.serializers import PostSerializer, ReviewSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    user = request.user
    data = request.data
    post = Post.objects.create(
        user=user,
        title=data['title'],
        content=data['content'],
        image=data.get('image')  # Ensure image is handled properly
    )
    serializer = PostSerializer(post, many=False, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

    if post.user != request.user and not request.user.is_staff:
        return Response({'detail': 'You do not have permission to delete this post.'}, status=status.HTTP_403_FORBIDDEN)
    
    post.delete()
    return Response({'detail': 'Post deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_posts(request):
    user = request.user
    posts = Post.objects.filter(user=user).order_by('-created_at')
    serializer = PostSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
def create_review(request, slug):
    data = request.data
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user if request.user.is_authenticated else None

    # Extract files from request.FILES
    photo = request.FILES.get('photo')
    video = request.FILES.get('video_review')
    review_image = request.FILES.get("review_image")

    # print("FILES:", request.FILES)
    # print("Photo:", photo)
    # print("Video:", video)

    review = Review.objects.create(
        post=post,
        user=user,
        customer_name=data.get('name'),
        customer_email=data.get('email'),
        customer_photo=photo,
        review_image =  review_image ,
        text_review=data.get('text_review'),
        video_review=video,
    )
    serializer = ReviewSerializer(review, many=False, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_post_reviews(request, slug):
    post = Post.objects.get(slug=slug)
    reviews = post.reviews.all()
    serializer = ReviewSerializer(reviews, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, my_id):
    try:
        review = Review.objects.get(my_id=my_id)
    except Review.DoesNotExist:
        return Response({'detail': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)

    if review.post.user != request.user and not request.user.is_staff:
        return Response({'detail': 'You do not have permission to delete this review.'}, status=status.HTTP_403_FORBIDDEN)
    
    review.delete()
    return Response({'detail': 'Review deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
