from django.urls import path
from testimonial.views import post_views as views
urlpatterns = [
    path('posts/all/', views.get_user_posts, name='user-posts'),
    path('posts/create/', views.create_post, name='create-post'),
    path('posts/reviews/<slug:slug>/', views.get_post_reviews, name='post-reviews'),
    path('posts/create/reviews/<slug:slug>/', views.create_review, name='create-review'),
    path('posts/delete/<slug:slug>/', views.delete_post, name='delete-post'),
    path('posts/review/delete/<int:my_id>/', views.delete_review, name='delete-review'),
]
