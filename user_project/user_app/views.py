from django.shortcuts import render
from .models import UserProfile


# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['POST', 'PATCH'])
@permission_classes([IsAuthenticated])
def create_or_update_profile(request):
    data = request.data
    user = request.user

    try:
        profile, created = UserProfile.objects.get_or_create(user=user)

        # Update the profile fields
        profile.name = data.get('name', profile.name)
        profile.email = data.get('email', profile.email)
        profile.bio = data.get('bio', profile.bio)
        profile.profile_picture = request.FILES.get('profile_picture', profile.profile_picture)
        profile.save()

        if created:
            message = "Profile created successfully."
        else:
            message = "Profile updated successfully."

        return Response({'message': message})
    except Exception as e:
        return Response({'message': str(e)}, status=400)
