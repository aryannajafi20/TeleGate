from django.urls import path
from telegram import views

app_name = 'telegram'


urlpatterns = [
    path("webhook/<str:token>/", views.telegram_webhook, name="telegram_webhook"),
    path('users_list/<uuid:token>/<str:chat_id>/', views.UsersListView.as_view(), name='users_list'),
    path('delete/u/<uuid:token>/<str:admin_chat_id>/<str:chat_id>/', views.DeleteUserView.as_view(), name='delete_user'),
    path('admins_list/<uuid:token>/<str:chat_id>/', views.AdminsListView.as_view(), name='admins_list'),
    path('delete/a/<uuid:token>/<str:admin_chat_id>/<str:chat_id>', views.DeleteAdminView.as_view(), name='delete_admin'),
    path('ULAV/<str:token>/', views.UsersListAPIView.as_view(), name='users_list_api'),
]