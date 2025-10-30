from django.contrib import admin
from telegram.models import Status, TelegramUser, Invite, Plan, Token
from django.utils import timezone
from datetime import timedelta
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'chat_id',
        'username',
        'name',
        'email',
        'is_active',
        'invited',
        'is_superuser',
        'has_permission',
        'subscription',
        'subscription_date',
        'created',
    )
    list_filter = (
        'is_active',
        'is_admin',
        'is_superuser',
        'has_permission',
        'subscription',
    )
    search_fields = ('chat_id', 'username', 'name', 'email')
    readonly_fields = ('created', 'updated', 'subscription_date')

    ordering = ('-created',)
    list_per_page = 30

    fieldsets = (
        ('Telegram Info', {
            'fields': ('chat_id', 'username', 'telegram_name')
        }),
        ('Personal Info', {
            'fields': ('name', 'email')
        }),
        ('Status & Permissions', {
            'fields': ('is_active', 'invited', 'is_admin', 'is_superuser', 'has_permission')
        }),
        ('Subscription', {
            'fields': ('subscription', 'subscription_date')
        }),
        ('Timestamps', {
            'fields': ('created', 'updated')
        }),
    )
class InviteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "creator",
        "receiver",
        "role",
        "name",
        "token_short",
        "used",
        "is_expired_display",
        "created",
    )
    list_filter = ("role", "created")
    search_fields = (
        "token",
        "name",
        "creator__username",
        "creator__telegram_id",
        "receiver__username",
        "receiver__telegram_id",
    )
    readonly_fields = ("token", "created", "updated", "is_expired_display")
    autocomplete_fields = ("creator", "receiver")
    date_hierarchy = "created"
    ordering = ("-created",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("creator", "receiver")

    def token_short(self, obj):
        token_str = str(obj.token)
        return token_str if len(token_str) <= 16 else f"{token_str[:8]}…{token_str[-4:]}"
    token_short.short_description = "Token"
    token_short.admin_order_field = "token"

    def used(self, obj):
        return bool(obj.receiver)
    used.boolean = True
    used.short_description = "Used"

    def is_expired_display(self, obj):
        try:
            return obj.is_expired
        except Exception:
            return (obj.created + timedelta(minutes=10)) < timezone.now()
    is_expired_display.boolean = True
    is_expired_display.short_description = "Expired"

class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "creator",
        "receiver",
        "days",
        "is_active",
        "is_used",
        "expired_display",
        "created",
        "activated",
    )
    list_filter = ("is_active", "is_used", "days", "created")
    search_fields = (
        "token",
        "creator__username",
        "creator__telegram_id",
        "receiver__username",
        "receiver__telegram_id",
    )
    readonly_fields = ("token", "created", "updated")
    autocomplete_fields = ("creator", "receiver")
    ordering = ("-created",)
    date_hierarchy = "created"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("creator", "receiver")

    def expired_display(self, obj):
        """Shows if plan has expired based on duration."""
        return obj.has_expired()
    expired_display.boolean = True
    expired_display.short_description = "Expired"
class TokenAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "creator",
        "token_short",
        "has_expired_display",
        "created",
    )
    list_filter = ("created",)
    search_fields = (
        "token",
        "creator__username",
        "creator__telegram_id",
    )
    readonly_fields = ("token", "created")
    autocomplete_fields = ("creator",)
    ordering = ("-created",)
    date_hierarchy = "created"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("creator")

    def token_short(self, obj):
        token_str = str(obj.token)
        return token_str if len(token_str) <= 16 else f"{token_str[:8]}…{token_str[-4:]}"
    token_short.short_description = "Token"
    token_short.admin_order_field = "token"

    def has_expired_display(self, obj):
        return obj.has_expired
    has_expired_display.boolean = True
    has_expired_display.short_description = "Expired"


admin.site.register(Status)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(Invite, InviteAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Token, TokenAdmin)
