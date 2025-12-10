from django.contrib.auth.models import AbstractUser
from django.db import models

from course.models import Course, Lessons


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Телефон')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватарка')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    date_pay = models.DateTimeField(verbose_name='Дата оплаты', auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    lessons = models.ForeignKey(Lessons, on_delete=models.CASCADE, blank=True, null=True)
    amount_pay = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    method_pay = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES,
                                  verbose_name='Способ оплаты')
    session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID сессии')
    url = models.URLField(max_length=500, blank=True, null=True, verbose_name='Ссылка на оплату')

    def __str__(self):
        return f'Платеж {self.amount_pay} от {self.user.email}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-date_pay']
