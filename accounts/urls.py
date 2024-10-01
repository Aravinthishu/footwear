from django.urls import path
from accounts.views import *

urlpatterns = [
    path('profile/', profile_view, name="profile"),
    path('profile-update',profile_update , name="profile-update")

    
]