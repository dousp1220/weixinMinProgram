# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.module_loading import import_string
from django.views.decorators.csrf import csrf_exempt
from weixin import WXAPPAPI
from weixin.lib.wxcrypt import WXBizDataCrypt

from account.django_jwt_session_auth import jwt_login, jwt_settings

WEIXIN_APPID = "wxb71fe6e43de3cbf2"
WEIXIN_APPSECRET = "092a1f3423f5f97af3aa330ccf00b262"


@csrf_exempt
def onAppLogin(request):
    if request.method == "POST":
        code = request.POST.get("code")
        encrypted_data = request.POST.get("encryptedData")
        iv = request.POST.get("iv")

        api = WXAPPAPI(appid=WEIXIN_APPID, app_secret=WEIXIN_APPSECRET)
        session_info = api.exchange_code_for_session_key(code=code)

    # 获取session_info 后

    session_key = session_info.get('session_key')
    crypt = WXBizDataCrypt(WEIXIN_APPID, session_key)

    # encrypted_data 包括敏感数据在内的完整用户信息的加密数据
    # iv 加密算法的初始向量
    # 这两个参数需要js获取

    user_info = crypt.decrypt(encrypted_data, iv)
    openId = user_info.get("openId")

    try:
        user1 = User.objects.get(username=openId)
    except:
        user = User()
        user.username = openId
        user.password = openId
        user.save()
        user1 = user

    # import_string(jwt_settings['USER_TO_PAYLOAD'])
    token = jwt_login(user1, request, expire=60 * 60 * 24 * 7)
    user_info['token'] = token

    json_string = json.dumps(user_info)

    return HttpResponse(json_string)
