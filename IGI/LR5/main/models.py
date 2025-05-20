from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import re

def validate_belarusian_phone_number(value):
    pattern = re.compile(r'^\+375\s\((17|25|29|33|44)\)\s\d{3}-\d{2}-\d{2}$')
    if not pattern.match(value):
        raise ValidationError(
            'Номер телефона должен быть в формате +375 (XX) XXX-XX-XX, где XX - код оператора (17, 25, 29, 33, 44).'
        )

def validate_age_18_plus(value):
    today = timezone.now().date()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError('Возраст должен быть 18 лет или старше.')

class VehicleType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название вида ТС")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Вид ТС"
        verbose_name_plural = "Виды ТС"

    def __str__(self):
        return self.name

class BodyType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название типа кузова")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Тип кузова"
        verbose_name_plural = "Типы кузовов"

    def __str__(self):
        return self.name

class CargoType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название вида груза")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Вид груза"
        verbose_name_plural = "Виды грузов"

    def __str__(self):
        return self.name

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Аккаунт пользователя")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    birth_date = models.DateField(verbose_name="Дата рождения", validators=[validate_age_18_plus])
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона", validators=[validate_belarusian_phone_number])
    license_number = models.CharField(max_length=50, unique=True, verbose_name="Номер ВУ")
    experience_years = models.PositiveIntegerField(default=0, verbose_name="Стаж (лет)")

    qualified_vehicle_types = models.ManyToManyField(VehicleType, blank=True, verbose_name="Допущен к видам ТС")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username})"

    @property
    def age(self):
        today = timezone.now().date()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

class Vehicle(models.Model):
    """Транспортные средства"""
    make = models.CharField(max_length=100, verbose_name="Марка")
    model = models.CharField(max_length=100, verbose_name="Модель")
    license_plate = models.CharField(max_length=20, unique=True, verbose_name="Гос. номер")
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.PROTECT, verbose_name="Вид ТС")
    body_type = models.ForeignKey(BodyType, on_delete=models.PROTECT, verbose_name="Тип кузова")

    current_driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Текущий водитель")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Транспортное средство"
        verbose_name_plural = "Транспортные средства"

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Аккаунт пользователя", null=True, blank=True)
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона", validators=[validate_belarusian_phone_number])
    birth_date = models.DateField(verbose_name="Дата рождения", validators=[validate_age_18_plus], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Клиент (Физ. лицо)"
        verbose_name_plural = "Клиенты (Физ. лица)"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Аккаунт пользователя", null=True,
                                blank=True)
    name = models.CharField(max_length=255, verbose_name="Название организации")
    registration_number = models.CharField(max_length=50, unique=True, verbose_name="УНП/Регистрационный номер")
    contact_person_name = models.CharField(max_length=150, verbose_name="Контактное лицо")
    contact_phone = models.CharField(max_length=20, verbose_name="Телефон контактного лица", validators=[validate_belarusian_phone_number])
    contact_email = models.EmailField(verbose_name="Email контактного лица")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Организация (Клиент)"
        verbose_name_plural = "Организации (Клиенты)"

    def __str__(self):
        if self.user:
            return f"{self.name} ({self.user.username})"
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание услуги")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Базовая стоимость")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Клиент (Физ. лицо)")
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Клиент (Организация)")

    service = models.ForeignKey(Service, on_delete=models.PROTECT, verbose_name="Услуга")
    cargo_description = models.TextField(verbose_name="Описание груза")
    cargo_type = models.ForeignKey(CargoType, on_delete=models.PROTECT, verbose_name="Вид груза")

    pickup_address = models.TextField(verbose_name="Адрес погрузки")
    delivery_address = models.TextField(verbose_name="Адрес доставки")
    pickup_datetime = models.DateTimeField(verbose_name="Плановое время погрузки (UTC)")

    assigned_vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Назначенное ТС")
    assigned_driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Назначенный водитель")

    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('confirmed', 'Подтвержден'),
        ('in_transit', 'В пути'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус заказа")
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Общая стоимость")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа (UTC)")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления (UTC)")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        customer = self.client if self.client else self.organization
        return f"Заказ #{self.id} от {customer}"

    def clean(self):
        super().clean()

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    author_name = models.CharField(max_length=100, verbose_name="Имя автора (если не пользователь)")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Автор (пользователь)")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Оценка")
    text = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата отзыва")
    created_at_db = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания в БД")
    updated_at_db = models.DateTimeField(auto_now=True, verbose_name="Дата обновления в БД")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        author = self.user.username if self.user else self.author_name
        return f"Отзыв от {author} на {self.rating} звезд"

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Промокод")
    description = models.TextField(verbose_name="Описание")
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Процент'),
        ('fixed_amount', 'Фиксированная сумма'),
    ]
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, verbose_name="Тип скидки")
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Значение скидки")
    start_date = models.DateTimeField(verbose_name="Дата начала действия")
    end_date = models.DateTimeField(verbose_name="Дата окончания действия")
    is_active = models.BooleanField(default=True, verbose_name="Активен (вручную)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"

    def __str__(self):
        return self.code

    def is_currently_active(self):
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date

    def clean(self):
        if self.discount_type == 'percentage' and not (0 < self.discount_value <= 100):
            raise ValidationError({'discount_value': "Процент скидки должен быть между 0 и 100."})
        if self.end_date < self.start_date:
            raise ValidationError({'end_date': "Дата окончания не может быть раньше даты начала."})
        super().clean()

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок новости")
    short_description = models.TextField(verbose_name="Краткое описание (для главной и списка)")
    full_description = models.TextField(verbose_name="Полное описание новости")
    image = models.ImageField(upload_to='news_images/', null=True, blank=True, verbose_name="Изображение (необязательно)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']

    def __str__(self):
        return self.title