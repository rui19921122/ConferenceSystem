import re

from django.shortcuts import render
from call_over.views import get_current_class
from rest_framework import generics
from rest_framework.request import Request
from call_over.models import AttentionTable, CallOverNumber
from rest_framework.response import Response

from utils.response import ErrorResponse
from worker.models import Worker, AttentionDetail
from .models import StationUserAndPassword
from bs4 import BeautifulSoup
import requests
import html
from .serization import ScrapySer
from call_over.serialzation import AttentionSer


# Create your views here.

class GetId(generics.GenericAPIView):
    '''
    返回选择的日期路局系统已录入的班前预想表id列表,
    需要field date,url,shift
    '''

    def get(self, request: Request):
        pass

    def post(self, request: Request):
        try:
            url = request.data.get('url')
        except:
            return ErrorResponse('url pattern not found')
        department = request.user.user.department
        try:
            attend_table = AttentionTable.objects.get(pk=request.data.get('attend_table'))
        except:
            return ErrorResponse('wrong attend table number')
        if attend_table.department == request.user.user.department:
            pass
        else:
            return ErrorResponse('wrong department')
        try:
            station_message = StationUserAndPassword.objects.get(
                user=request.user
            )
        except Exception as error:
            return ErrorResponse('未找到存储的路局网站数据，忘记设置密码？')
        username, password = station_message.username, station_message.password
        login_url = r'http://10.128.20.124/'
        session = requests.session()
        try:
            login_page = session.get(login_url)
        except Exception as error:
            return ErrorResponse("服务器访问路局网页失败")
        if login_page.status_code != 200:
            return ErrorResponse('get login page failure')
        soup = BeautifulSoup(login_page.text, "html.parser")
        try:
            viewstate = soup.find(id='__VIEWSTATE')
            eventvalidation = soup.find(id='__EVENTVALIDATION')
        except:
            return ErrorResponse('登录页解析错误')
        data = {
            "__EVENTVALIDATION": eventvalidation['value'],
            "__VIEWSTATE": viewstate['value'],
            "tbLoginName": username,
            'tbPWD': password,
            'btnLogin.x': 101,
            'btnLogin.y': 19
        }
        login = session.post(login_url + 'Login.aspx?ReturnUrl=%2f',
                             data=data, allow_redirects=False)
        if login.status_code != 302:
            return ErrorResponse('登陆失败，可能是用户名密码错误')
        _raw_text = session.get(url)
        if _raw_text.status_code != 200:
            return ErrorResponse('获取指定地址信息失败，错误的url?')
        response = BeautifulSoup(session.get(url).text, "html.parser")
        results = response.find_all('tr', class_='tbs')
        data = []
        if len(results) > 0:
            for number, result in enumerate(results):
                title, content = result.find_all('td')
                title = html.unescape(title.get_text())
                content = html.unescape(content.get_text())
                data.append({'title': title,
                             'content': content,
                             'number': number + 1})
            attend_ser = AttentionSer(attend_table)
            attend_ser.scrapy = ScrapySer(data=data, many=True)
            if attend_ser.is_valid():
                attend_ser.save()
                return Response(data={'data': attend_ser.scrapy.data}, status=200)
            else:
                return ErrorResponse('序列化失败')
        else:
            return ErrorResponse('解析失败')


class SetPasswordView(generics.GenericAPIView):
    '''
    用于查询、更改或删除当前用户存储的路局库账号密码
    post的格式为{username:string,password:string}
    get请求不会返回具体的用户名密码，只会返回200
    '''

    def post(self, request: Request):
        try:
            username, password = str(request.data['username']) \
                , str(request.data['password'])
        except:
            return ErrorResponse('not enough fields')
        if len(username) >= 0 and len(password) >= 0:
            pass
        else:
            return ErrorResponse('用户名或密码字符段为空')
        try:
            StationUserAndPassword.objects.filter(user=request.user).delete()
        except:
            pass
        StationUserAndPassword.objects.create(
            user=request.user,
            username=username,
            password=password
        )
        return Response({'status': 'success'}, status=200)

    def delete(self, request: Request):
        try:
            StationUserAndPassword.objects.filter(user=request.user).delete()
            return Response({'status': 'success'}, status=201)
        except:
            return ErrorResponse('失败')

    def get(self, request: Request):
        if StationUserAndPassword.objects.filter(user=request.user).exists():
            return Response({'status': 'success'}, status=200)
        else:
            return ErrorResponse('未找到相应的用户名密码')
