from rest_framework import views, serializers, response, decorators
from rest_framework.permissions import AllowAny
from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    credits = serializers.CharField(source='profile.credits', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'is_superuser', 'credits')
        write_only = ('password')
        read_only = ('is_superuser', 'credits')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()

        Profile.objects.create(user=user)

        return user


class UserView(views.APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return response.Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return response.Response(serializer.data)
