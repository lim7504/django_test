from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponse, Http404
import os
import jwt
from account.models import User
from django.core.files.storage import default_storage
from functools import wraps
from django.utils.decorators import method_decorator
from django.views.generic import DetailView

def login_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        access_token = request.COOKIES.get('access_token')
        if access_token is None:
            print("Token is None!!")
            context = {
                'status': 400,
                'message': "Token is None!!"
            }
            return JsonResponse(context)

        try:
            payload = jwt.decode(access_token, 'secret', algorithm='HS256')
        except jwt.InvalidTokenError:
            payload = None

        if payload is None:
            context = {
                'status': 401,
                'message': "Wrong Token!!"
            }
            return JsonResponse(context)

        kwargs['email'] = payload['email']

        return f(request, *args, **kwargs)
    return decorated_function

class LoginView(View):

    def get(self,request):
        print('-----------------------')
        return render(request, 'login.html', {})

    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(user_email=email, user_password=password).first()

        if user is None:
            context = {
                'status': 400,
                'message': "fail!!"
            }
            return JsonResponse(context)

        token = jwt.encode({'email': email}, 'secret', algorithm='HS256')
        context = {
            'status': 200,
            'message': "success!!",
            'access_token' : token.decode('UTF-8')
        }
        return JsonResponse(context)

class JoinView(View):

    def get(self,request):
        return render(request, 'join.html', {})

    def post(self, request):
        user_email = request.POST.get('user_email')
        user_nick_name = request.POST.get('user_nick_name')
        user_password = request.POST.get('user_password')

        user = User.objects.filter(user_email=user_email).first()

        if user is not None:
            context = {
                'status': 400,
                'message': "fail!!"
            }
            return JsonResponse(context)

        user = User(user_email=user_email
                , user_password=user_password
                , user_nick_name=user_nick_name)
        user.save()

        # upload_file = request.FILES.get('upload_file')
        # filename = upload_file._name
        # with default_storage.open('upload_files/' + filename, 'wb+') as destination:
        #     for chunk in upload_file.chunks():
        #         destination.write(chunk)

        token = jwt.encode({'email': user_email}, 'secret', algorithm='HS256')
        context = {
            'status': 200,
            'message': "success!!",
            'access_token': token.decode('UTF-8')
        }
        return JsonResponse(context)


class MainView(View):

    @method_decorator(login_required)
    def get(self,request, email):
        return render(request, 'main.html', {})

class MyDataView(View):

    @method_decorator(login_required)
    def get(self,request, email):

        user = User.objects.filter(user_email=email).first()
        return render(request, 'mydata.html', {'user': user})


class AllTableView(View):

    @method_decorator(login_required)
    def get(self,request, email):
        return render(request, 'alltable.html', {})









class FileDownload(View):

    def get(self, request):
        file_path = os.path.join(settings.MEDIA_ROOT, "abc.jpg")
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404


