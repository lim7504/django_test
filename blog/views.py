from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from django.http import JsonResponse
import jwt
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import HttpResponse, Http404

# Create your views here.
class IndexView(View):

    def get(self,request):
        print('-----------------------')
        return render(request, 'blog/index.html', {})


    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email != "aaa" or password != "bbb":
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



class MainView(View):

    def get(self,request):
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

        if payload is not None:
            print(payload['email'])

        context = {
            'status': 200,
            'message': "Success!!"
        }
        # return JsonResponse(context)
        return render(request, 'blog/main.html', {})


    def post(self,request):
        upload_file = request.FILES.get('upload_file')
        filename = upload_file._name
        with default_storage.open('upload_files/' + filename, 'wb+') as destination:
            for chunk in upload_file.chunks():
                destination.write(chunk)

        context = {
            'status': 200,
            'message': "success!!",
        }
        return JsonResponse(context)

class Second(View):

    def get(self,request):
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

        if payload is not None:
            print(payload['email'])

        context = {
            'status': 200,
            'message': "Success!!"
        }
        return render(request, 'blog/second.html', {})

class FileDownload(View):

    def get(self, request):
        file_path = os.path.join(settings.MEDIA_ROOT, "abc.jpg")
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404