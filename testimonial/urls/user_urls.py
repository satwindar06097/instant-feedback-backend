from django.urls import path
from testimonial.views import user_views as views

from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('all/' ,views.allUser, name ='register'),
    path('register/' ,views.registerUser, name ='register'),
    path('profile/', views.getUserProfile, name='users-profile'),
    path('profile/update/', views.updateUserProfile, name='user-profile-update'),
   
   
]
