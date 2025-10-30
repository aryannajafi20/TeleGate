from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from telegram.models import Invite, TelegramUser, Token, Status
from telegram.utils.hash import unhash_value
from telegram.core.bot.bot import bot
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from telebot import types
import json


@csrf_exempt
def telegram_webhook(request, token):
    if token != settings.TELEGRAM_BOT_TOKEN:
        return HttpResponseForbidden("invalid token in URL")

    expected = settings.WEBHOOK_SECRET_TOKEN
    if expected:
        received = request.META.get("HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN")
        if received != expected:
            return HttpResponseForbidden("invalid secret token header")

    if request.method != "POST":
        return HttpResponseBadRequest("only POST allowed")

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("bad json")

    try:
        update = types.Update.de_json(data)
        bot.process_new_updates([update])
    except Exception:
        JsonResponse({"error": "bad json"}, status=200)
    return JsonResponse({"ok": True})


class UsersListView(View):
    def get(self, request, token, chat_id):
        try:
            link = Token.objects.get(token=token)
        except Token.DoesNotExist:
            return HttpResponse("Invalid link.", status=400)

        if link.has_expired:
            link.delete()
            return HttpResponse("This link has expired or already been used.", status=404)
        ci = unhash_value(chat_id)
        user = TelegramUser.objects.get(chat_id=ci)
        invites = Invite.objects.filter(creator=user, receiver__isnull=False, receiver__is_admin=False)
        return render(request, 'telegram/users_list.html', {'invites': invites, "token": token, "admin_user": chat_id})

class DeleteUserView(View):
    def get(self, request, token, admin_chat_id, chat_id):
        try:
            link = Token.objects.get(token=token)
        except Token.DoesNotExist:
            return HttpResponse("Invalid link.", status=400)

        if link.has_expired:
            link.delete()
            return HttpResponse("This link has expired or already been used.", status=404)

        user = TelegramUser.objects.filter(chat_id=chat_id)
        if user.exists():
            user.delete()
        return redirect("telegram:users_list", token, admin_chat_id)

class AdminsListView(View):
    def get(self, request, token, chat_id):
        try:
            link = Token.objects.get(token=token)
        except Token.DoesNotExist:
            return HttpResponse("Invalid link.", status=400)

        if link.has_expired:
            link.delete()
            return HttpResponse("This link has expired or already been used.", status=404)


        ci = unhash_value(chat_id)
        user = TelegramUser.objects.get(chat_id=ci)
        invites = Invite.objects.filter(creator=user, receiver__isnull=False, receiver__is_admin=True)
        return render(request, 'telegram/admins_list.html', {'invites': invites, "token": token, "admin_user": chat_id})


class DeleteAdminView(View):
    def get(self, request, token, admin_chat_id, chat_id):
        try:
            link = Token.objects.get(token=token)
        except Token.DoesNotExist:
            return HttpResponse("Invalid link.", status=400)

        if link.has_expired:
            link.delete()
            return HttpResponse("This link has expired or already been used.", status=404)

        user = TelegramUser.objects.filter(chat_id=chat_id)
        if user.exists():
            user.delete()
        return redirect("telegram:admins_list", token, admin_chat_id)

class UsersListAPIView(View):
    def get(self, request, token):
        if token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden("invalid token in URL")
        status, created = Status.objects.get_or_create(token=settings.TELEGRAM_BOT_TOKEN, defaults={"status": True})
        if created or status.status:
            qs = TelegramUser.objects.filter(has_permission=True, subscription=True, is_active=True, is_admin=False, is_superuser=False)
            admin_qs = TelegramUser.objects.filter(is_admin=True, has_permission=True)
            super_users = TelegramUser.objects.filter(is_superuser=True, has_permission=True)
            users = list(qs.values("chat_id", "username", "telegram_name"))
            admins = list(admin_qs.values('chat_id', 'username', 'telegram_name'))
            superusers = list(super_users.values('chat_id', 'username', 'telegram_name'))
            return JsonResponse({"ok": True, "users": users + admins + superusers})
        else:
            super_users = TelegramUser.objects.filter(is_superuser=True, has_permission=True)
            superusers = list(super_users.values('chat_id', 'username', 'telegram_name'))
            return JsonResponse({"ok": True, "users": superusers})
