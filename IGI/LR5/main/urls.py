from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('', views.home_page, name='home_page'),

    path('register/driver/', views.register_driver, name='register_driver'),
    path('register/client/', views.register_client, name='register_client'),
    path('register/organization/', views.register_organization, name='register_organization'),
    path('registration-success/', views.registration_success, name='registration_success'),

    path('login/', auth_views.LoginView.as_view(template_name='logistics/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('account/', views.account_hub_view, name='account_hub'),
    path('account/customer/', views.customer_account_view, name='customer_account'),
    path('account/driver/', views.driver_account_view, name='driver_account'),

    path('orders/create/', views.create_order_view, name='create_order'),
    path('orders/', views.order_list_view, name='order_list'),
    path('order/detail/<int:order_id>/', views.customer_order_detail_view, name='customer_order_detail'),

    path('promocodes/', views.promocodes_view, name='promocodes'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('about-us/', views.about_us_view, name='about_us'),
    path('reviews/', views.reviews_view, name='reviews'),

    path('driver/order/<int:order_id>/update_status/', views.driver_update_order_status_view,
         name='driver_update_order_status'),
    path('driver/available-orders/', views.available_orders_list_view, name='available_orders_list'),
    path('driver/take-order/<int:order_id>/', views.driver_take_order_view, name='driver_take_order'),
    path('driver/profile/update/', views.driver_profile_update_view, name='driver_profile_update'),
    path('driver/profile/delete/', views.driver_profile_delete_view, name='driver_profile_delete'),

    path('review/add/', views.add_site_review_view, name='add_site_review'),
    path('order/detail/<int:order_id>/', views.customer_order_detail_view, name='customer_order_detail'),

    path('news/', views.news_list_view, name='news_list'),
    path('news/<int:news_id>/', views.news_detail_view, name='news_detail'),

    path('random-fact-pet/', views.random_fact_pet_view, name='random_fact_pet'),
    path('statistics/', views.site_statistics_view, name='site_statistics'),

]