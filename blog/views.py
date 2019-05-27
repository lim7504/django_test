from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from django.http import JsonResponse
import jwt

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

