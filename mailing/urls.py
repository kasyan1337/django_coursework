from allauth.account import views as allauth_views
from django.urls import path

from . import views

app_name = 'mailing'

urlpatterns = [
    path('clients/', views.client_list, name='client_list'),
    path('clients/create/', views.client_create, name='client_create'),
    path('clients/<int:pk>/edit/', views.client_update, name='client_update'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),

    path('messages/', views.message_list, name='message_list'),
    path('messages/create/', views.message_create, name='message_create'),
    path('messages/<int:pk>/edit/', views.message_update, name='message_update'),
    path('messages/<int:pk>/delete/', views.message_delete, name='message_delete'),

    path('mailings/', views.mailing_list, name='mailing_list'),
    path('mailings/create/', views.mailing_create, name='mailing_create'),
    path('mailings/<int:pk>/edit/', views.mailing_update, name='mailing_update'),
    path('mailings/<int:pk>/delete/', views.mailing_delete, name='mailing_delete'),

    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/block/', views.block_user, name='block_user'),
    path('users/<int:user_id>/unblock/', views.unblock_user, name='unblock_user'),

    path('mailings/<int:pk>/disable/', views.disable_mailing, name='disable_mailing'),
    path('mailings/<int:pk>/enable/', views.enable_mailing, name='enable_mailing'),

    path('accounts/login/', allauth_views.login, name='account_login'),
    path('accounts/logout/', allauth_views.logout, name='account_logout'),
    path('accounts/signup/', allauth_views.signup, name='account_signup'),
    path('accounts/password/reset/', allauth_views.password_reset, name='account_reset_password'),
    path('accounts/password/reset/done/', allauth_views.password_reset_done, name='account_reset_password_done'),
    path('accounts/password/reset/key/<uidb64>/<key>/', allauth_views.password_reset_from_key,
         name='account_reset_password_from_key'),
    path('accounts/password/reset/key/done/', allauth_views.password_reset_from_key_done,
         name='account_reset_password_from_key_done'),
]
