import random

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login

from .models import User, Profile
from .serializers import ProfileSerializer, UserSerializer, AuthSerializer


class UserViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get', 'post'])
    def authenticate(self, request):
        if request.method == 'POST':
            phone_number = request.POST.get('phone_number')
            email = request.POST.get('email')
            code = request.POST.get('code')

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User(phone_number=phone_number, email=email) 
                user.set_password('1231')
                user.save()

            if not code:
                code = random.randint(1000, 9999)
                user.auth_code = code
                user.save()
                send_mail( 'Ваш код подтверждения', f'Ваш код подтверждения: {code}', 'no-reply@example.com', [email], fail_silently=False, )
                return render(request, 'users/auth_step2.html', {'phone_number': phone_number, 'email': email})

            elif code == user.auth_code:
                user = User.objects.get(phone_number=phone_number)
                login(request=request, user=user)
                return render(request, 'users/auth_success.html', {'message': 'Аутентификация успешна'})
            else:
                return render(request, 'users/auth_step2.html', {'phone_number': phone_number, 'email': email, 'error': 'Неверный код'})

        return render(request, 'users/auth_step1.html')


class ProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    @action(detail=False, methods=['get', 'post'], permission_classes=[IsAuthenticated])
    def activate_invite_code(self, request):
        profile = self.get_object()
        
        if request.method == 'POST':
            invite_code = request.POST.get('invite_code')  # Измените на request.POST.get для получения данных из формы

            if profile.activated_invite_code:
                return render(request, 'users/profile.html', {
                    'error': 'Инвайт-код уже активирован',
                    'user': request.user
                })

            if not Profile.objects.filter(invite_code=invite_code).exists():
                return render(request, 'users/profile.html', {
                    'error': 'Инвайт-код не существует',
                    'user': request.user
                })

            profile.activated_invite_code = invite_code
            profile.save()
            return render(request, 'users/profile.html', {
                'message': 'Инвайт-код успешно активирован',
                'user': request.user
            })

        # Для GET-запроса возвращаем HTML-шаблон с данными пользователя
        return render(request, 'users/profile.html', {'user': request.user})
