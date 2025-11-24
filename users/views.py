from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import UpdateAPIView, ListAPIView, DestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer, UserRegisterSerializer
from users.services import create_stripe_price, create_stripe_session, create_stripe_product


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product_id = create_stripe_product(payment.course)
        price = create_stripe_price(payment.amount_pay, product_id)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.url = payment_link
        payment.save()


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
