from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer, UserRegisterSerializer


class PaymentListAPIView(generics.ListAPIView):
    """Контроллер вывода платежей"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lessons', 'method_pay')
    ordering_fields = ('date_pay',)
    permission_classes = [IsAuthenticated]


class UserCreateAPIView(generics.CreateAPIView):
    """Контроллер создания профиля"""
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер просмотра деталей пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(UpdateAPIView):
    """Контроллер редактирования профиля пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserListAPIView(ListAPIView):
    """Контроллер вывода списка пользователей"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(DestroyAPIView):
    """Контроллер удаления пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
