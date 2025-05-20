from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Driver, Client, Organization, VehicleType, Order, Service, CargoType, Review
from django.utils import timezone
import pytz

class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class DriverRegistrationForm(forms.ModelForm):

    qualified_vehicle_types = forms.ModelMultipleChoiceField(
        queryset=VehicleType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Допущен к видам ТС"
    )
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'birth_date', 'phone_number', 'license_number', 'experience_years', 'qualified_vehicle_types']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ClientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'phone_number', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class OrganizationRegistrationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'registration_number', 'contact_person_name', 'contact_phone', 'contact_email']

class OrderCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user_timezone_str = kwargs.pop('user_timezone_str', settings.TIME_ZONE)
        super().__init__(*args, **kwargs)

    pickup_datetime = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'ДД/ММ/ГГГГ ЧЧ:ММ'
            }
        ),
        label="Желаемая дата и время погрузки",
    )
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        label="Выберите услугу",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cargo_type = forms.ModelChoiceField(
        queryset=CargoType.objects.all(),
        label="Вид груза",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Order
        fields = [
            'service', 'cargo_description', 'cargo_type',
            'pickup_address', 'delivery_address', 'pickup_datetime'
        ]
        widgets = {
            'cargo_description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control',
                                                       'placeholder': 'Например: Личные вещи, коробки, мебель (укажите габариты, если важно)'}),
            'pickup_address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Город, улица, дом, квартира/офис'}),
            'delivery_address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Город, улица, дом, квартира/офис'}),
        }
        labels = {
            'cargo_description': "Подробное описание груза",
            'pickup_address': "Адрес погрузки",
            'delivery_address': "Адрес доставки",
        }

    def clean_pickup_datetime(self):
        dt = self.cleaned_data.get('pickup_datetime')
        if not dt:
            return None

        try:
            user_input_timezone_pytz = pytz.timezone(self.user_timezone_str)
        except pytz.UnknownTimeZoneError:

            user_input_timezone_pytz = pytz.timezone(settings.TIME_ZONE)

        django_default_timezone_obj = timezone.get_default_timezone()

        if not timezone.is_naive(dt):

            dt_tz_key = None
            default_tz_key = None

            if hasattr(dt.tzinfo, 'key'):
                dt_tz_key = dt.tzinfo.key
            elif hasattr(dt.tzinfo, 'zone'):
                dt_tz_key = dt.tzinfo.zone
            else:
                dt_tz_key = str(dt.tzinfo)

            if hasattr(django_default_timezone_obj, 'key'):
                default_tz_key = django_default_timezone_obj.key
            elif hasattr(django_default_timezone_obj, 'zone'):
                default_tz_key = django_default_timezone_obj.zone
            else:
                default_tz_key = str(django_default_timezone_obj)

            if dt_tz_key == default_tz_key:

                dt = timezone.make_naive(dt, dt.tzinfo)
            else:

                dt = dt.astimezone(user_input_timezone_pytz)

        if timezone.is_naive(dt):
            try:
                dt = user_input_timezone_pytz.localize(dt, is_dst=None)
            except pytz.exceptions.AmbiguousTimeError:

                raise forms.ValidationError(
                    "Неоднозначное время из-за смены часовых поясов. Пожалуйста, выберите время немного раньше или позже."
                )
            except pytz.exceptions.NonExistentTimeError:
                raise forms.ValidationError(
                    "Указанное время не существует (например, при переходе на летнее время вперед)."
                )

        if dt < timezone.now():
            raise forms.ValidationError("Дата и время погрузки не могут быть в прошлом.")

        return dt

class DriverOrderStatusUpdateForm(forms.ModelForm):

    DRIVER_ALLOWED_STATUSES = [

        ('in_transit', 'В пути'),
        ('delivered', 'Доставлен'),

    ]

    status = forms.ChoiceField(
        choices=DRIVER_ALLOWED_STATUSES,
        label="Новый статус заказа",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Order
        fields = ['status']

class DriverProfileUpdateForm(forms.ModelForm):
    qualified_vehicle_types = forms.ModelMultipleChoiceField(
        queryset=VehicleType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Допущен к видам ТС"
    )

    class Meta:
        model = Driver
        fields = [
            'first_name', 'last_name', 'birth_date', 'phone_number',
            'license_number', 'experience_years', 'qualified_vehicle_types'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': "Имя",
            'last_name': "Фамилия",
            'birth_date': "Дата рождения",
            'phone_number': "Номер телефона",
            'license_number': "Номер ВУ",
            'experience_years': "Стаж (лет)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        pass

class CustomerReviewForm(forms.ModelForm):
    class Meta:
        model = Review

        fields = ['author_name', 'rating', 'text']

        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя (как оно будет отображаться в отзыве)'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select form-select-lg mb-3'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Поделитесь вашими впечатлениями о нашем сервисе...'
            }),
        }
        labels = {
            'author_name': "Ваше имя для отзыва",
            'rating': "Общая оценка сервиса (от 1 до 5)",
            'text': "Текст вашего отзыва",
        }
        help_texts = {
            'author_name': 'Это имя будет видно другим пользователям. Если вы авторизованы, оно может быть предзаполнено.',
            'rating': 'Пожалуйста, выберите оценку.',
            'text': 'Напишите, что вам понравилось или что можно улучшить.',
        }

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user and self.user.is_authenticated and not self.instance.pk:
            if not self.initial.get('author_name'):
                self.fields['author_name'].initial = self.user.get_full_name() or self.user.username

    def clean_author_name(self):
        author_name = self.cleaned_data.get('author_name')

        if not self.user or not self.user.is_authenticated:
            if not author_name:
                raise forms.ValidationError("Пожалуйста, укажите ваше имя для отзыва.")

        elif self.user and self.user.is_authenticated and not author_name:
            return self.user.get_full_name() or self.user.username
        return author_name

