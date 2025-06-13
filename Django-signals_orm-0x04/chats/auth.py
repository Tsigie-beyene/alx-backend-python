from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer to add user details to JWT token."""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['user_id'] = str(user.user_id)
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom view to use the custom token serializer."""
    serializer_class = CustomTokenObtainPairSerializer
