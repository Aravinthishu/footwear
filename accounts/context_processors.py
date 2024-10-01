from .models import Profile

def profile(request):
    profile_image = None
    profile_instance = None

    if request.user.is_authenticated:
        try:
            profile_instance = Profile.objects.get(user=request.user)
            profile_image = profile_instance.avatar  # Accessing the avatar property
        except Profile.DoesNotExist:
            # Handle case where profile doesn't exist
            profile_image = None

    return {'profile': profile_instance, 'profile_image': profile_image}