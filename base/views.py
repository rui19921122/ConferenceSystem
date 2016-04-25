from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class Menu(APIView):
    def get(self, request):
        '''
        :param request:Request
        :return:
        '''
        user = request.user
        if user.is_authenticated():
            return Response(
                [{'type': 'single', 'name': '首页', 'href': 'loginIn', 'key': 'index'},
                 {
                     'type': 'single', 'name': '班计划管理查询', 'href': 'class-plan', 'key': 'plan0',
                 },
                 {
                     'type': 'multiple', 'name': '事故案例', 'href': 'accident', 'key': 'risk0',
                     'children': [
                         {'type': 'single', 'name': '管理事故案例', 'href': 'manage-accident', 'key': 'risk1'},
                         {'type': 'single', 'name': '增加事故案例', 'href': 'add-accident', 'key': 'risk2'},
                         {'type': 'single', 'name': '事故案例学习情况查询', 'href': 'query-accident', 'key': 'risk3'}
                     ]
                 },
                 {
                     'type': 'multiple', 'name': '业务学习', 'href': 'study', 'key': 'study0',
                     'children': [
                         {'type': 'single', 'name': '管理业务学习', 'href': 'manage-study', 'key': 'study1'},
                         {'type': 'single', 'name': '新增业务学习', 'href': 'add-study', 'key': 'study2'},
                         {'type': 'single', 'name': '业务学习情况查询', 'href': 'query-study', 'key': 'study3'}
                     ]
                 },
                 {
                     'type': 'multiple', 'name': '考勤管理', 'href': 'check', 'key': 'check0',
                     'children': [
                         {'type': 'single', 'name': '考勤情况预处理', 'href': 'manage-check', 'key': 'check1'},
                         {'type': 'single', 'name': '历史考勤情况查询', 'href': 'query-check', 'key': 'check2'},
                         {'type': 'single', 'name': '职工管理', 'href': 'manage-worker', 'key': 'check3'}
                     ]
                 },
                 {
                     'type': 'single', 'name': '点名会综合查询', 'href': 'query', 'key': 'query0'
                 }]
                , status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class get_user_detail(APIView):
    def get(self, request):
        user = request.user.user
        return Response(data={'name': user.name, 'department': user.department.name},
                        status=status.HTTP_200_OK)
