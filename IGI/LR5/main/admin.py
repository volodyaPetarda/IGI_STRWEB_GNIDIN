from django.contrib import admin
from django.utils.html import format_html
from .models import (
    VehicleType, BodyType, CargoType, Driver, Vehicle, Client, Organization,
    Service, Order, Review, PromoCode, News, Partner, CompanyInfo, CompanyHistoryItem, GlossaryItem,
    Contact
)

admin.site.site_header = "Администрирование Грузоперевозок"
admin.site.site_title = "Панель администратора"
admin.site.index_title = "Добро пожаловать в панель управления"

class VehicleInline(admin.TabularInline):
    model = Vehicle
    extra = 0
    fields = ('make', 'model', 'license_plate', 'vehicle_type', 'body_type')
    readonly_fields = ('make', 'model', 'license_plate', 'vehicle_type', 'body_type')
    can_delete = False
    verbose_name_plural = "Закрепленные транспортные средства"

    def has_add_permission(self, request, obj=None):
        return False

class OrderInlineForClient(admin.TabularInline):
    model = Order
    fk_name = "client"
    extra = 0
    fields = ('id', 'service', 'status', 'total_cost', 'created_at')
    readonly_fields = ('id', 'service', 'status', 'total_cost', 'created_at')
    can_delete = False
    verbose_name_plural = "Заказы клиента"

    def has_add_permission(self, request, obj=None):
        return False

class OrderInlineForOrganization(admin.TabularInline):
    model = Order
    fk_name = "organization"
    extra = 0
    fields = ('id', 'service', 'status', 'total_cost', 'created_at')
    readonly_fields = ('id', 'service', 'status', 'total_cost', 'created_at')
    can_delete = False
    verbose_name_plural = "Заказы организации"

    def has_add_permission(self, request, obj=None):
        return False

class CompanyHistoryItemInline(admin.TabularInline):
    model = CompanyHistoryItem
    extra = 1
    fields = ('year', 'text')
    verbose_name = "Пункт истории"
    verbose_name_plural = "История по годам"

@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_per_page = 25

@admin.register(BodyType)
class BodyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_per_page = 25

@admin.register(CargoType)
class CargoTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_per_page = 25

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'full_name_display', 'phone_number', 'license_number', 'experience_years', 'age_display', 'created_at')
    search_fields = ('user__username', 'first_name', 'last_name', 'phone_number', 'license_number')
    list_filter = ('experience_years', 'qualified_vehicle_types', 'created_at')
    readonly_fields = ('age_display', 'created_at', 'updated_at')
    filter_horizontal = ('qualified_vehicle_types',)
    inlines = [VehicleInline]
    list_per_page = 25
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', ('first_name', 'last_name'), 'birth_date', 'age_display', 'phone_number')
        }),
        ('Профессиональные данные', {
            'fields': ('license_number', 'experience_years', 'qualified_vehicle_types')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_link(self, obj):
        return format_html('<a href="{}">{}</a>',
                           f'/admin/auth/user/{obj.user.id}/change/',
                           obj.user.username)
    user_link.short_description = "Аккаунт"
    user_link.admin_order_field = 'user__username'

    def full_name_display(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name_display.short_description = "Полное имя"
    full_name_display.admin_order_field = 'last_name'

    def age_display(self, obj):
        if obj.birth_date:
            return obj.age
        return "Не указана"
    age_display.short_description = "Возраст"

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'make_model_display', 'vehicle_type', 'body_type', 'current_driver_link', 'created_at')
    search_fields = ('make', 'model', 'license_plate', 'current_driver__first_name', 'current_driver__last_name')
    list_filter = ('vehicle_type', 'body_type', 'make')
    autocomplete_fields = ['vehicle_type', 'body_type', 'current_driver']
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25
    fieldsets = (
        (None, {
            'fields': (('make', 'model'), 'license_plate')
        }),
        ('Характеристики', {
            'fields': ('vehicle_type', 'body_type')
        }),
        ('Ответственный', {
            'fields': ('current_driver',)
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def make_model_display(self, obj):
        return f"{obj.make} {obj.model}"
    make_model_display.short_description = "Марка и модель"

    def current_driver_link(self, obj):
        if obj.current_driver:
            return format_html('<a href="{}">{}</a>',
                               f'/admin/logistics/driver/{obj.current_driver.id}/change/',
                               obj.current_driver)
        return "Не назначен"
    current_driver_link.short_description = "Текущий водитель"
    current_driver_link.admin_order_field = 'current_driver'

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name_display', 'email', 'phone_number', 'user_link', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'user__username')
    list_filter = ('created_at',)
    inlines = [OrderInlineForClient]
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25
    fieldsets = (
        ('Личная информация', {
            'fields': (('first_name', 'last_name'), 'email', 'phone_number', 'birth_date')
        }),
        ('Аккаунт', {
            'fields': ('user',)
        }),
         ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_link(self, obj):
        if obj.user:
            return format_html('<a href="{}">{}</a>',
                               f'/admin/auth/user/{obj.user.id}/change/',
                               obj.user.username)
        return "Нет аккаунта"
    user_link.short_description = "Аккаунт"

    def full_name_display(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name_display.short_description = "Полное имя"
    full_name_display.admin_order_field = 'last_name'

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'registration_number', 'contact_person_name', 'contact_phone', 'contact_email', 'created_at')
    search_fields = ('name', 'registration_number', 'contact_person_name', 'contact_email')
    list_filter = ('created_at',)
    inlines = [OrderInlineForOrganization]
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('base_price',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_display', 'service', 'status', 'total_cost_display', 'pickup_datetime_local', 'created_at_local')
    search_fields = (
        'id', 'client__first_name', 'client__last_name', 'client__email',
        'organization__name', 'service__name', 'pickup_address', 'delivery_address',
        'assigned_driver__first_name', 'assigned_driver__last_name',
        'assigned_vehicle__license_plate'
    )
    list_filter = ('status', 'service', 'cargo_type', 'pickup_datetime', 'created_at', 'assigned_driver', 'assigned_vehicle')
    readonly_fields = ('created_at', 'updated_at', 'total_cost_display', 'pickup_datetime_local', 'created_at_local')
    autocomplete_fields = ['client', 'organization', 'service', 'cargo_type', 'assigned_vehicle', 'assigned_driver']
    list_per_page = 20
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Информация о заказчике', {
            'fields': ('client', 'organization')
        }),
        ('Детали заказа', {
            'fields': ('service', 'cargo_type', 'cargo_description',
                       ('pickup_address', 'delivery_address'),
                       'pickup_datetime', 'status', 'total_cost')
        }),
        ('Исполнители', {
            'fields': ('assigned_vehicle', 'assigned_driver')
        }),
        ('Даты (UTC)', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def customer_display(self, obj):
        if obj.client:
            return format_html('<a href="{}">{}</a>',
                               f'/admin/logistics/client/{obj.client.id}/change/',
                               obj.client)
        elif obj.organization:
            return format_html('<a href="{}">{}</a>',
                               f'/admin/logistics/organization/{obj.organization.id}/change/',
                               obj.organization)
        return "Не указан"
    customer_display.short_description = "Заказчик"
    customer_display.admin_order_field = 'client'

    def total_cost_display(self, obj):
        return f"{obj.total_cost} руб."
    total_cost_display.short_description = "Стоимость"
    total_cost_display.admin_order_field = 'total_cost'

    def pickup_datetime_local(self, obj):
        if obj.pickup_datetime:
            return obj.pickup_datetime.astimezone().strftime('%d/%m/%Y %H:%M')
        return "-"
    pickup_datetime_local.short_description = "Время погрузки (локальное)"
    pickup_datetime_local.admin_order_field = 'pickup_datetime'

    def created_at_local(self, obj):
        if obj.created_at:
            return obj.created_at.astimezone().strftime('%d/%m/%Y %H:%M')
        return "-"
    created_at_local.short_description = "Создан (локальное)"
    created_at_local.admin_order_field = 'created_at'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_display', 'rating', 'created_at_local', 'is_approved_display')
    search_fields = ('author_name', 'user__username', 'text')
    list_filter = ('rating', 'created_at')
    readonly_fields = ('created_at_db', 'updated_at_db', 'created_at_local')
    list_per_page = 25

    fields = ('author_name', 'user', 'rating', 'text', 'created_at', ('created_at_db', 'updated_at_db'))

    def is_approved_display(self, obj):
        return "N/A (поле is_approved отсутствует)"
    is_approved_display.short_description = "Одобрен"

    def author_display(self, obj):
        if obj.user:
            return format_html('<a href="{}">{} (пользователь)</a>',
                               f'/admin/auth/user/{obj.user.id}/change/',
                               obj.user.username)
        return obj.author_name
    author_display.short_description = "Автор"

    def created_at_local(self, obj):
        return obj.created_at.astimezone().strftime('%d/%m/%Y %H:%M')
    created_at_local.short_description = "Дата отзыва (локальное)"
    created_at_local.admin_order_field = 'created_at'

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'discount_type', 'discount_value_display', 'start_date_local', 'end_date_local', 'is_active_manual', 'is_currently_active_display')
    search_fields = ('code', 'description')
    list_filter = ('discount_type', 'is_active', 'start_date', 'end_date')
    readonly_fields = ('created_at', 'updated_at', 'is_currently_active_display', 'start_date_local', 'end_date_local')
    list_per_page = 25
    fieldsets = (
        (None, {'fields': ('code', 'description')}),
        ('Условия скидки', {'fields': ('discount_type', 'discount_value')}),
        ('Период действия', {'fields': ('start_date', 'end_date', 'is_active')}),
        ('Даты (UTC)', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def discount_value_display(self, obj):
        if obj.discount_type == 'percentage':
            return f"{obj.discount_value}%"
        return f"{obj.discount_value} руб."
    discount_value_display.short_description = "Размер скидки"

    def is_active_manual(self, obj):
        return "Да" if obj.is_active else "Нет"
    is_active_manual.short_description = "Активен (вручную)"
    is_active_manual.admin_order_field = 'is_active'

    def is_currently_active_display(self, obj):
        return "Да" if obj.is_currently_active() else "Нет"
    is_currently_active_display.short_description = "Действует сейчас"

    def start_date_local(self, obj):
        return obj.start_date.astimezone().strftime('%d/%m/%Y %H:%M')
    start_date_local.short_description = "Начало (локальное)"
    start_date_local.admin_order_field = 'start_date'

    def end_date_local(self, obj):
        return obj.end_date.astimezone().strftime('%d/%m/%Y %H:%M')
    end_date_local.short_description = "Окончание (локальное)"
    end_date_local.admin_order_field = 'end_date'

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'created_at', 'is_published', 'updated_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'short_description', 'full_description')
    list_editable = ('is_published',)

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_url', 'logo_preview', 'created_at')
    readonly_fields = ('logo_preview',)
    search_fields = ('name', 'website_url')
    list_per_page = 25

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:40px;">', obj.logo.url)
        return "—"
    logo_preview.short_description = "Логотип"

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'updated_at')
    inlines = [CompanyHistoryItemInline]
    readonly_fields = ('updated_at',)
    fieldsets = (
        (None, {'fields': ('company_name', 'description', 'logo', 'video_url')}),
        ('Официальная информация', {'fields': ('requisites', 'certificate_text')}),
        ('Системные поля', {'fields': ('updated_at',), 'classes': ('collapse',)}),
    )

@admin.register(GlossaryItem)
class GlossaryItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'added_at')
    search_fields = ('question', 'answer')
    list_filter = ('added_at',)
    date_hierarchy = 'added_at'
    ordering = ('-added_at',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'email', 'phone_number', 'is_active', 'preview', 'sort_order', 'updated_at')
    list_editable = ('is_active', 'sort_order')
    search_fields = ('full_name', 'position', 'email', 'phone_number')
    list_filter = ('is_active',)
    readonly_fields = ('preview', 'created_at', 'updated_at')
    fields = (('full_name', 'position'), ('email', 'phone_number'), 'photo', 'preview', 'responsibilities', ('is_active', 'sort_order'), ('created_at', 'updated_at'))

    def preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:60px;">', obj.photo.url)
        return "—"
    preview.short_description = "Фото"