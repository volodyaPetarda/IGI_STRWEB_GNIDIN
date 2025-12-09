from decimal import Decimal, InvalidOperation

import requests
from django.contrib.auth import logout
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import (
    CustomUserCreationForm,
    DriverRegistrationForm,
    ClientRegistrationForm,
    OrganizationRegistrationForm,
    OrderCreationForm, DriverOrderStatusUpdateForm,
    DriverProfileUpdateForm, CustomerReviewForm
)
from .models import Client, Driver, Organization, Order, PromoCode, Review, Service, \
    CargoType, News, Partner, CompanyInfo, GlossaryItem, Contact
from .utils import generate_user_types_pie_chart, generate_ages_histogram

def register_driver(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        driver_form = DriverRegistrationForm(request.POST)
        if user_form.is_valid() and driver_form.is_valid():
            try:
                with transaction.atomic():
                    user = user_form.save()
                    driver = driver_form.save(commit=False)
                    driver.user = user
                    driver.save()

                messages.success(request, 'Регистрация водителя прошла успешно! Теперь вы можете войти.')
                return redirect('registration_success')
            except Exception as e:
                messages.error(request, f'Произошла ошибка при регистрации: {e}')
        else:
            error_messages = []
            if not user_form.is_valid():
                for field, errors in user_form.errors.items():
                    error_messages.append(
                        f"Данные аккаунта: Поле '{user_form.fields[field].label or field}' - {' '.join(errors)}")
            if not driver_form.is_valid():
                for field, errors in driver_form.errors.items():
                    error_messages.append(
                        f"Данные водителя: Поле '{driver_form.fields[field].label or field}' - {' '.join(errors)}")
            messages.error(request, "Пожалуйста, исправьте ошибки в форме: " + "; ".join(error_messages))
    else:
        user_form = CustomUserCreationForm()
        driver_form = DriverRegistrationForm()
    context = {'user_form': user_form, 'driver_form': driver_form, 'title': 'Регистрация водителя'}
    return render(request, 'logistics/register_driver.html', context)

def register_client(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        client_form = ClientRegistrationForm(request.POST)
        if user_form.is_valid() and client_form.is_valid():
            # Use email from user_form, validate against Client uniqueness
            email = user_form.cleaned_data.get('email')
            if email and Client.objects.filter(email__iexact=email).exists():
                user_form.add_error('email', 'Этот email уже зарегистрирован как клиент. Пожалуйста, используйте другой.')
                messages.error(request, "Пожалуйста, исправьте ошибки в форме: Email уже зарегистрирован.")
                context = {'user_form': user_form, 'client_form': client_form, 'title': 'Регистрация клиента'}
                return render(request, 'logistics/register_client.html', context)

            try:
                with transaction.atomic():
                    user = user_form.save()
                    client = client_form.save(commit=False)
                    client.user = user
                    # Ensure client.email is filled from user_form
                    client.email = email
                    client.save()
                messages.success(request, 'Регистрация клиента прошла успешно! Теперь вы можете войти.')
                return redirect('registration_success')
            except IntegrityError as e:
                # Fallback in case of race condition on Client.email
                if 'main_client.email' in str(e):
                    user_form.add_error('email', 'Этот email уже зарегистрирован как клиент. Пожалуйста, используйте другой.')
                    messages.error(request, "Пожалуйста, исправьте ошибки в форме: Email уже зарегистрирован.")
                    context = {'user_form': user_form, 'client_form': client_form, 'title': 'Регистрация клиента'}
                    return render(request, 'logistics/register_client.html', context)
                messages.error(request, f'Произошла ошибка при регистрации: {e}')
            except Exception as e:
                messages.error(request, f'Произошла ошибка при регистрации: {e}')
        else:
            error_messages = []
            if not user_form.is_valid():
                for field, errors in user_form.errors.items():
                    error_messages.append(
                        f"Данные аккаунта: Поле '{user_form.fields[field].label or field}' - {' '.join(errors)}")
            if not client_form.is_valid():
                for field, errors in client_form.errors.items():
                    error_messages.append(
                        f"Данные клиента: Поле '{client_form.fields[field].label or field}' - {' '.join(errors)}")
            messages.error(request, "Пожалуйста, исправьте ошибки в форме: " + "; ".join(error_messages))
    else:
        user_form = CustomUserCreationForm()
        client_form = ClientRegistrationForm()
    context = {'user_form': user_form, 'client_form': client_form, 'title': 'Регистрация клиента'}
    return render(request, 'logistics/register_client.html', context)

def register_organization(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        organization_form = OrganizationRegistrationForm(request.POST)
        if user_form.is_valid() and organization_form.is_valid():
            try:
                with transaction.atomic():
                    user = user_form.save()
                    organization = organization_form.save(commit=False)
                    organization.user = user
                    organization.save()
                messages.success(request,
                                 'Регистрация организации и аккаунта пользователя прошла успешно! Теперь вы можете войти.')
                return redirect('registration_success')
            except Exception as e:
                messages.error(request,
                               f'Произошла ошибка при регистрации: {e}. Попробуйте другие данные или обратитесь в поддержку.')
        else:
            error_messages = []
            if not user_form.is_valid():
                for field, errors in user_form.errors.items():
                    error_messages.append(
                        f"Данные аккаунта: Поле '{user_form.fields[field].label or field}' - {' '.join(errors)}")
            if not organization_form.is_valid():
                for field, errors in organization_form.errors.items():
                    error_messages.append(
                        f"Данные организации: Поле '{organization_form.fields[field].label or field}' - {' '.join(errors)}")
            messages.error(request, "Пожалуйста, исправьте ошибки в форме: " + "; ".join(error_messages))
    else:
        user_form = CustomUserCreationForm()
        organization_form = OrganizationRegistrationForm()
    context = {'user_form': user_form, 'organization_form': organization_form, 'title': 'Регистрация организации'}
    return render(request, 'logistics/register_organization.html', context)

def registration_success(request):
    return render(request, 'logistics/registration_success.html', {'title': 'Регистрация завершена'})

def home_page(request):
    latest_news = News.objects.filter(is_published=True).order_by('-created_at').first()
    partners = Partner.objects.all().order_by('name')
    faq_items = GlossaryItem.objects.all().order_by('-added_at')
    context = {
        'title': 'Главная страница',
        'latest_news': latest_news,
        'partners': partners,
        'faq_items': faq_items,
    }
    return render(request, 'logistics/home.html', context)

@login_required
def account_hub_view(request):
    user = request.user

    try:
        if user.client:
            return redirect('customer_account')
    except Client.DoesNotExist:
        pass

    try:
        if user.organization:
            return redirect('customer_account')
    except Organization.DoesNotExist:
        pass

    try:
        if user.driver:
            return redirect('driver_account')
    except Driver.DoesNotExist:
        pass

    if user.is_superuser or user.is_staff:
        messages.info(request, "Вы вошли как администратор. Для управления перейдите в админ-панель.")
        return redirect('admin:index')

    messages.error(request,
                   "Не удалось определить тип вашего аккаунта или ваш профиль не завершен. Обратитесь в поддержку.")
    return redirect('home_page')

@login_required
def customer_account_view(request):
    user = request.user
    profile = None
    profile_type = None
    orders = Order.objects.none()

    try:
        profile = Client.objects.get(user=user)
        profile_type = "Клиент (Физ. лицо)"
        orders = Order.objects.filter(client=profile).order_by('-created_at')
    except Client.DoesNotExist:
        try:
            profile = Organization.objects.get(user=user)
            profile_type = "Организация"
            orders = Order.objects.filter(organization=profile).order_by('-created_at')
        except Organization.DoesNotExist:
            messages.error(request, "Профиль клиента или организации не найден.")
            return redirect('home_page')

    context = {
        'title': f'Кабинет - {profile_type}',
        'profile': profile,
        'profile_type': profile_type,
        'orders': orders
    }
    return render(request, 'logistics/customer_account.html', context)

@login_required
def driver_account_view(request):
    user = request.user
    try:
        driver_profile = Driver.objects.get(user=user)
    except Driver.DoesNotExist:
        messages.error(request, "Профиль водителя не найден или доступ запрещен.")
        return redirect('home_page')

    assigned_orders = Order.objects.filter(assigned_driver=driver_profile).order_by('-pickup_datetime', '-created_at')

    context = {
        'title': 'Кабинет водителя',
        'profile': driver_profile,
        'orders': assigned_orders,
    }
    return render(request, 'logistics/driver_account.html', context)

def promocodes_view(request):
    promocodes_query = PromoCode.objects.filter(

        end_date__gte=timezone.now(),
        is_active=True
    )

    min_percentage_str = request.GET.get('min_percentage', None)
    sort_option = request.GET.get('sort_option', 'default')

    current_filters = {
        'min_percentage': min_percentage_str,
        'sort_option': sort_option,
    }

    if min_percentage_str:
        try:
            min_percentage_decimal = Decimal(min_percentage_str)
            if 0 <= min_percentage_decimal <= 100:
                promocodes_query = promocodes_query.filter(
                    discount_type='percentage',
                    discount_value__gte=min_percentage_decimal
                )
            else:
                current_filters['min_percentage'] = None
        except (InvalidOperation, ValueError):
            current_filters['min_percentage'] = None

    if sort_option == 'perc_asc':
        promocodes_query = promocodes_query.filter(discount_type='percentage').order_by('discount_value', 'end_date')
    elif sort_option == 'perc_desc':
        promocodes_query = promocodes_query.filter(discount_type='percentage').order_by('-discount_value', 'end_date')
    else:

        promocodes_query = promocodes_query.order_by('end_date', '-start_date', 'code')

    promocodes_list = list(promocodes_query)

    context = {
        'title': 'Промокоды и Акции',
        'promocodes_list': promocodes_list,
        'current_filters': current_filters,
    }
    return render(request, 'logistics/promocodes.html', context)

def reviews_view(request):
    all_reviews = Review.objects.all().order_by('-created_at')
    context = {'title': 'Отзывы Клиентов', 'reviews_list': all_reviews}
    return render(request, 'logistics/reviews.html', context)

def privacy_policy_view(request):
    context = {'title': 'Политика Конфиденциальности'}
    return render(request, 'logistics/privacy_policy.html', context)

def about_us_view(request):
    company = CompanyInfo.objects.first()
    context = {
        'title': 'О Нас',
        'company': company,
        'history_items': list(company.history_items.all()) if company else [],
    }
    return render(request, 'logistics/about_us.html', context)

@login_required
def create_order_view(request):
    user = request.user
    profile = None
    profile_type_for_order = None

    effective_user_timezone = 'Europe/Minsk'

    try:
        client_profile = Client.objects.get(user=user)
        profile = client_profile
        profile_type_for_order = 'client'
    except Client.DoesNotExist:
        try:
            organization_profile = Organization.objects.get(user=user)
            profile = organization_profile
            profile_type_for_order = 'organization'
        except Organization.DoesNotExist:
            messages.error(request,
                           "Для создания заказа ваш аккаунт должен быть связан с профилем клиента или организации.")
            return redirect('account_hub')

    if not profile:
        messages.error(request, "Не удалось идентитифицировать ваш профиль для создания заказа.")
        return redirect('account_hub')

    if request.method == 'POST':
        form = OrderCreationForm(request.POST, user_timezone_str=effective_user_timezone)
        if form.is_valid():
            order = form.save(commit=False)
            if profile_type_for_order == 'client':
                order.client = profile
                order.organization = None
            elif profile_type_for_order == 'organization':
                order.organization = profile
                order.client = None
            else:
                messages.error(request, "Произошла ошибка при обработке вашего профиля. Заказ не может быть создан.")

                context = {'form': form, 'title': 'Создание нового заказа', 'profile': profile}
                return render(request, 'logistics/create_order.html', context)

            selected_service = form.cleaned_data.get('service')
            order.total_cost = selected_service.base_price if selected_service else 0
            order.status = 'pending'
            try:
                order.save()
                # Add created order to session cart (quantity-aware, migrate if needed)
                cart_data = request.session.get('cart_order_ids', {})
                if isinstance(cart_data, list):
                    migrated = {}
                    for oid in cart_data:
                        try:
                            k = str(int(oid))
                        except Exception:
                            continue
                        migrated[k] = migrated.get(k, 0) + 1
                    cart_data = migrated
                k = str(order.id)
                cart_data[k] = int(cart_data.get(k, 0)) + 1
                request.session['cart_order_ids'] = cart_data
                request.session.modified = True

                messages.success(request, f"Заказ #{order.id} успешно создан и добавлен в корзину.")
                return redirect('cart')
            except ValidationError as ve:
                error_message_str = "; ".join(ve.messages) if isinstance(ve.messages, list) else str(ve.messages)
                messages.error(request, f"Ошибка при сохранении заказа: {error_message_str}")

            except Exception as e:
                messages.error(request, f"Произошла непредвиденная ошибка при сохранении заказа: {type(e).__name__} - {e}")

        else:
            messages.error(request, f"Пожалуйста, исправьте ошибки в форме: {form.errors.as_ul()}")

    else:
        form = OrderCreationForm(user_timezone_str=effective_user_timezone)

    context = {
        'title': 'Создание нового заказа',
        'form': form,
        'profile': profile
    }
    return render(request, 'logistics/create_order.html', context)

@login_required
def order_list_view(request):
    user = request.user
    order_list_qs = Order.objects.none()
    user_type_for_display = "Не определен"

    try:
        client_profile = Client.objects.get(user=user)
        order_list_qs = Order.objects.filter(client=client_profile).order_by('-created_at')
        user_type_for_display = "Клиент (Физ. лицо)"
    except Client.DoesNotExist:
        try:
            organization_profile = Organization.objects.get(user=user)
            order_list_qs = Order.objects.filter(organization=organization_profile).order_by('-created_at')
            user_type_for_display = "Организация"
        except Organization.DoesNotExist:
            try:
                driver_profile = Driver.objects.get(user=user)
                order_list_qs = Order.objects.filter(assigned_driver=driver_profile).order_by('-pickup_datetime', '-created_at')
                user_type_for_display = "Водитель"
            except Driver.DoesNotExist:
                if not (user.is_superuser or user.is_staff):
                    messages.warning(request, "Не удалось определить ваш профиль для отображения списка заказов.")

    paginator = Paginator(order_list_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Список заказов',
        'page_obj': page_obj,
        'user_type': user_type_for_display,
        'is_paginated': paginator.num_pages > 1
    }
    return render(request, 'logistics/order_list.html', context)

# Restore available_orders_list_view (used in urls.py)
@login_required
def available_orders_list_view(request):
    user = request.user
    try:
        driver_profile = Driver.objects.get(user=user)
    except Driver.DoesNotExist:
        messages.error(request, "Только водители могут просматривать доступные заказы.")
        return redirect('account_hub')

    available_orders = Order.objects.filter(
        status='pending',
        assigned_driver__isnull=True
    ).order_by('pickup_datetime', 'created_at')

    context = {
        'title': 'Доступные заказы для выполнения',
        'available_orders': available_orders,
        'driver_profile': driver_profile
    }
    return render(request, 'logistics/available_orders_list.html', context)

# Cart: show, inc, dec, remove, clear
@login_required
def cart_view(request):
    user = request.user
    cart_data = request.session.get('cart_order_ids', {})

    # migrate legacy list -> dict {order_id: qty}
    if isinstance(cart_data, list):
        migrated = {}
        for oid in cart_data:
            try:
                k = str(int(oid))
            except Exception:
                continue
            migrated[k] = migrated.get(k, 0) + 1
        cart_data = migrated
        request.session['cart_order_ids'] = cart_data
        request.session.modified = True

    # detect owner
    owner_client = None
    owner_org = None
    try:
        owner_client = Client.objects.get(user=user)
    except Client.DoesNotExist:
        try:
            owner_org = Organization.objects.get(user=user)
        except Organization.DoesNotExist:
            owner_client = None
            owner_org = None

    if not (owner_client or owner_org):
        messages.error(request, "Корзина доступна только клиентам и организациям.")
        return redirect('account_hub')

    # handle actions
    if request.method == 'POST':
        action = request.POST.get('action')
        order_id_raw = request.POST.get('order_id', '')
        try:
            order_id_int = int(order_id_raw)
            order_key = str(order_id_int)
        except (TypeError, ValueError):
            order_key = None

        if action == 'inc' and order_key:
            cart_data[order_key] = int(cart_data.get(order_key, 0)) + 1
            request.session['cart_order_ids'] = cart_data
            request.session.modified = True
            return redirect('cart')
        elif action == 'dec' and order_key:
            current = int(cart_data.get(order_key, 0))
            if current <= 1:
                cart_data.pop(order_key, None)
            else:
                cart_data[order_key] = current - 1
            request.session['cart_order_ids'] = cart_data
            request.session.modified = True
            return redirect('cart')
        elif action == 'remove' and order_key:
            cart_data.pop(order_key, None)
            request.session['cart_order_ids'] = cart_data
            request.session.modified = True
            return redirect('cart')
        elif action == 'clear':
            request.session['cart_order_ids'] = {}
            request.session.modified = True
            return redirect('cart')

    # build items list limited to current owner
    id_list = [int(k) for k in cart_data.keys()] if cart_data else []
    qs = Order.objects.filter(id__in=id_list)
    if owner_client:
        qs = qs.filter(client=owner_client)
    else:
        qs = qs.filter(organization=owner_org)

    orders_by_id = {o.id: o for o in qs}
    cart_items = []
    subtotal = Decimal('0.00')
    for k, qty in cart_data.items():
        try:
            oid = int(k)
        except Exception:
            continue
        order = orders_by_id.get(oid)
        if not order:
            continue
        q = int(qty) if qty else 0
        if q <= 0:
            continue
        line_total = (order.total_cost or Decimal('0.00')) * q
        subtotal += line_total
        cart_items.append({
            'order': order,
            'qty': q,
            'line_total': line_total,
        })

    context = {
        'title': 'Моя корзина',
        'cart_items': cart_items,
        'cart_subtotal': subtotal,
    }
    return render(request, 'logistics/cart.html', context)

# Payment: apply promocode and confirm
@login_required
def payment_view(request):
    user = request.user
    cart_data = request.session.get('cart_order_ids', {})
    if isinstance(cart_data, list):
        migrated = {}
        for oid in cart_data:
            try:
                k = str(int(oid))
            except Exception:
                continue
            migrated[k] = migrated.get(k, 0) + 1
        cart_data = migrated
        request.session['cart_order_ids'] = cart_data
        request.session.modified = True

    # detect owner
    owner_client = None
    owner_org = None
    try:
        owner_client = Client.objects.get(user=user)
    except Client.DoesNotExist:
        try:
            owner_org = Organization.objects.get(user=user)
        except Organization.DoesNotExist:
            owner_client = None
            owner_org = None

    if not (owner_client or owner_org):
        messages.error(request, "Оплата доступна только клиентам и организациям.")
        return redirect('account_hub')

    id_list = [int(k) for k in cart_data.keys()] if cart_data else []
    qs = Order.objects.filter(id__in=id_list)
    if owner_client:
        qs = qs.filter(client=owner_client)
    else:
        qs = qs.filter(organization=owner_org)

    orders_by_id = {o.id: o for o in qs}
    orders_in_cart = []
    subtotal = Decimal('0.00')
    for k, qty in cart_data.items():
        try:
            oid = int(k)
        except Exception:
            continue
        order = orders_by_id.get(oid)
        if not order:
            continue
        q = int(qty) if qty else 0
        if q <= 0:
            continue
        line_total = (order.total_cost or Decimal('0.00')) * q
        subtotal += line_total
        orders_in_cart.append(order)

    promo_code_input = request.POST.get('promo_code') if request.method == 'POST' else request.GET.get('promo_code')
    applied_promo = None
    discount_amount = Decimal('0.00')

    if promo_code_input:
        try:
            promo = PromoCode.objects.get(code__iexact=promo_code_input, is_active=True)
            if promo.is_currently_active():
                applied_promo = promo
                if promo.discount_type == 'percentage':
                    discount_amount = (subtotal * (promo.discount_value or Decimal('0'))) / Decimal('100')
                else:
                    discount_amount = min((promo.discount_value or Decimal('0')), subtotal)
                discount_amount = discount_amount.quantize(Decimal('0.01'))
                messages.success(request, f"Промокод {promo.code} применен.")
            else:
                messages.warning(request, "Этот промокод сейчас неактивен.")
        except PromoCode.DoesNotExist:
            messages.error(request, "Промокод не найден.")

    total_due = (subtotal - discount_amount).quantize(Decimal('0.01')) if subtotal else Decimal('0.00')

    if request.method == 'POST' and request.POST.get('action') == 'pay':
        if not orders_in_cart:
            messages.warning(request, "Корзина пуста. Добавьте заказы перед оплатой.")
            return redirect('cart')
        # mark unique orders as confirmed (оплата симулируется)
        for o in orders_in_cart:
            if o.status == 'pending':
                o.status = 'confirmed'
                o.save()
        request.session['cart_order_ids'] = {}
        request.session.modified = True
        messages.success(request, f"Оплата прошла успешно. Оплачено: {total_due} руб.")
        return redirect('order_list')

    context = {
        'title': 'Оплата заказов',
        'cart_orders': orders_in_cart,
        'cart_subtotal': subtotal,
        'applied_promo': applied_promo,
        'promo_code_input': promo_code_input or '',
        'discount_amount': discount_amount,
        'total_due': total_due,
    }
    return render(request, 'logistics/payment.html', context)

@login_required
def driver_take_order_view(request, order_id):
    user = request.user
    try:
        driver_profile = Driver.objects.get(user=user)
    except Driver.DoesNotExist:
        messages.error(request, "Только водители могут брать заказы.")
        return redirect('account_hub')

    if request.method == 'POST':

        order_to_take = get_object_or_404(Order, id=order_id)

        if order_to_take.status == 'pending' and order_to_take.assigned_driver is None:

            order_to_take.assigned_driver = driver_profile

            order_to_take.status = 'confirmed'
            order_to_take.save()

            messages.success(request, f"Заказ #{order_to_take.id} успешно назначен вам.")
            return redirect('driver_account')
        else:
            messages.warning(request,
                             f"Заказ #{order_to_take.id} уже был взят другим водителем или его статус изменился.")
            return redirect('available_orders_list')
    else:

        return redirect('available_orders_list')

@login_required
def driver_update_order_status_view(request, order_id):
    user = request.user
    try:

        driver_profile = Driver.objects.get(user=user)
    except Driver.DoesNotExist:
        messages.error(request, "Доступ запрещен. Только водители могут изменять статус заказа.")
        return redirect('account_hub')

    order = get_object_or_404(Order, id=order_id, assigned_driver=driver_profile)

    if order.status in ['delivered', 'cancelled']:
        messages.warning(request,
                         f"Заказ #{order.id} уже находится в статусе '{order.get_status_display()}' и не может быть изменен водителем.")
        return redirect('driver_account')

    if request.method == 'POST':
        form = DriverOrderStatusUpdateForm(request.POST, instance=order)
        if form.is_valid():
            new_status = form.cleaned_data['status']

            if order.status == 'confirmed' and new_status not in ['in_transit',
                                                                  'delivered']:
                messages.error(request,
                               f"Недопустимый переход статуса из '{order.get_status_display()}' в '{dict(form.fields['status'].choices).get(new_status)}'.")
            elif order.status == 'in_transit' and new_status not in ['delivered']:
                messages.error(request,
                               f"Недопустимый переход статуса из '{order.get_status_display()}' в '{dict(form.fields['status'].choices).get(new_status)}'.")
            else:
                order.status = new_status
                order.save()
                messages.success(request,
                                 f"Статус заказа #{order.id} успешно обновлен на '{order.get_status_display()}'.")
                return redirect('driver_account')
        else:

            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:

        form = DriverOrderStatusUpdateForm(instance=order)

    context = {
        'title': f'Обновление статуса заказа #{order.id}',
        'form': form,
        'order': order
    }
    return render(request, 'logistics/driver_update_order_status.html', context)

@login_required
def driver_profile_update_view(request):
    try:
        driver_profile = Driver.objects.get(user=request.user)
    except Driver.DoesNotExist:
        messages.error(request, "Профиль водителя не найден.")
        return redirect('account_hub')

    if request.method == 'POST':
        form = DriverProfileUpdateForm(request.POST, instance=driver_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш профиль успешно обновлен.")
            return redirect('driver_account')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = DriverProfileUpdateForm(instance=driver_profile)

    context = {
        'title': 'Обновление профиля водителя',
        'form': form,
        'profile': driver_profile
    }
    return render(request, 'logistics/driver_profile_update.html', context)

@login_required
def driver_profile_delete_view(request):
    try:
        driver_profile = Driver.objects.get(user=request.user)
        user_to_delete = request.user
    except Driver.DoesNotExist:
        messages.error(request, "Профиль водителя не найден.")
        return redirect('account_hub')

    if request.method == 'POST':

        try:
            with transaction.atomic():

                username_deleted = user_to_delete.username

                user_to_delete.delete()

            logout(request)
            messages.success(request,
                             f"Аккаунт водителя '{username_deleted}' и все связанные данные были успешно удалены.")
            return redirect('home_page')
        except Exception as e:
            messages.error(request, f"Произошла ошибка при удалении аккаунта: {e}")
            return redirect('driver_account')

    context = {
        'title': 'Подтверждение удаления аккаунта водителя',
        'profile': driver_profile
    }
    return render(request, 'logistics/driver_profile_delete_confirm.html', context)

@login_required
def add_site_review_view(request):
    current_user = request.user

    if Review.objects.filter(user=current_user).exists():
        messages.warning(request, "Вы уже оставляли отзыв о нашем сервисе. Спасибо!")

        return redirect('customer_account')

    if request.method == 'POST':
        form = CustomerReviewForm(request.POST, user=current_user)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = current_user

            if not review.author_name:
                review.author_name = current_user.get_full_name() or current_user.username

            review.save()
            messages.success(request, "Спасибо! Ваш отзыв о сервисе успешно добавлен.")
            return redirect('customer_account')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме и попробуйте снова.")
    else:
        form = CustomerReviewForm(user=current_user)

    context = {
        'title': 'Оставить отзыв о сервисе',
        'form': form,
    }

    return render(request, 'logistics/add_site_review.html', context)

@login_required
def customer_order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    current_user = request.user

    is_order_client = False
    if order.client and order.client.user == current_user:
        is_order_client = True
    elif order.organization and order.organization.user == current_user:
        is_order_client = True

    if not is_order_client:
        messages.error(request, "Вы не имеете доступа к деталям этого заказа.")
        return redirect('customer_account')

    context = {
        'title': f'Детали Заказа #{order.id}',
        'order': order,
    }
    return render(request, 'logistics/customer_order_detail.html', context)

def news_list_view(request):
    news_list_qs = News.objects.filter(is_published=True).order_by('-created_at')

    paginator = Paginator(news_list_qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Новости компании',
        'page_obj': page_obj,
        'is_paginated': paginator.num_pages > 1
    }
    return render(request, 'logistics/news_list.html', context)

def news_detail_view(request, news_id):
    news_item = get_object_or_404(News, id=news_id, is_published=True)
    context = {
        'title': news_item.title,
        'news_item': news_item,
    }
    return render(request, 'logistics/news_detail.html', context)

def services_catalog_view(request):
    services = Service.objects.all().order_by('name')
    context = {
        'title': 'Каталог услуг',
        'services': services,
    }
    return render(request, 'logistics/services_catalog.html', context)

def random_fact_pet_view(request):
    pet_image_url = None
    fact_text = None
    error_message_pet = None
    error_message_fact = None
    pet_type_for_display = "собака"

    try:

        attempts = 0
        max_attempts = 5
        image_found = False
        while attempts < max_attempts and not image_found:
            response_pet = requests.get('https://random.dog/woof.json', timeout=5)
            response_pet.raise_for_status()
            data_pet = response_pet.json()
            url = data_pet.get('url')
            if url and not (url.endswith('.mp4') or url.endswith('.webm')):
                pet_image_url = url
                image_found = True
            attempts += 1

        if not image_found:
            error_message_pet = "Не удалось загрузить изображение собаки после нескольких попыток. Попробуйте еще раз."

    except requests.exceptions.RequestException as e:
        error_message_pet = f"Ошибка при запросе изображения питомца: {e}"
    except ValueError:
        error_message_pet = "Ошибка при обработке ответа от API изображений питомцев."

    try:
        response_fact = requests.get('https://uselessfacts.jsph.pl/random.json?language=en', timeout=5)
        response_fact.raise_for_status()
        data_fact = response_fact.json()
        fact_text = data_fact.get('text')
    except requests.exceptions.RequestException as e:
        error_message_fact = f"Ошибка при запросе факта: {e}"
    except ValueError:
        error_message_fact = "Ошибка при обработке ответа от API фактов."

    context = {
        'title': "Уголок Развлечений",
        'pet_image_url': pet_image_url,
        'fact_text': fact_text,
        'error_message_pet': error_message_pet,
        'error_message_fact': error_message_fact,
        'pet_type_for_display': pet_type_for_display,
    }
    return render(request, 'logistics/random_fact_pet.html', context)

@login_required
def site_statistics_view(request):

    user_types_chart_b64 = generate_user_types_pie_chart()
    ages_histogram_chart_b64 = generate_ages_histogram()

    context = {
        'title': "Статистика Сайта",
        'user_types_chart': user_types_chart_b64,
        'ages_histogram_chart': ages_histogram_chart_b64,
    }

    return render(request, 'logistics/site_statistics.html', context)

def contacts(request):
    staff = Contact.objects.filter(is_active=True).order_by('sort_order', 'full_name')
    return render(request, 'logistics/contacts.html', {
        'title': 'Контакты',
        'staff': staff,
    })

def glossary_view(request):
    """Словарь терминов и FAQ: список вопросов с датой и раскрывающимся ответом."""
    items = GlossaryItem.objects.all().order_by('-added_at')
    context = {
        'title': 'Словарь и FAQ',
        'items': items,
    }
    return render(request, 'logistics/glossary.html', context)