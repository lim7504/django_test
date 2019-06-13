from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import View
from functools import wraps
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
import jwt
import boto3
import mysite.config as config

from django.contrib.auth.models import User
from social_django.models import UserSocialAuth
from account.models import ExtendUser
# from account.models import Certificate

# from account.serializers import UserSerializer, CertificateSerializer
# from rest_framework import viewsets
# from rest_framework.response import Response


#region Login & Join

def login_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        access_token = request.COOKIES.get('access_token')
        context = {}
        if access_token is None:
            context['status'] = 400
            context['message'] = "Token is None!!"
            return JsonResponse(context)

        try:
            payload = jwt.decode(access_token, 'secret', algorithm='HS256')
        except jwt.InvalidTokenError:
            payload = None

        if payload is None:
            context['status'] = 401
            context['message'] = "Wrong Token!!"
            return JsonResponse(context)

        kwargs['email'] = payload['email']

        return f(request, *args, **kwargs)
    return decorated_function

class LoginView(View):

    def get(self,request):
        return render(request, 'login.html', {})

    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        context = {}

        user = User.objects.filter(email=email, password=password).first()

        if user is None:
            context['status'] = 400
            context['message'] = "fail!!"
            return JsonResponse(context)

        token = jwt.encode({'email': email}, 'secret', algorithm='HS256')

        context['status'] = 200
        context['message'] = "success!!"
        context['access_token'] = token.decode('UTF-8')
        return JsonResponse(context)

class SocialLoginView(View):

    def get(self,request):
        try:
            ExtendUser.objects.get(user_id=request.user.id)
        except:
            return redirect('/socialjoin', {})

        return render(request, 'main.html', {})

class JoinView(View):

    def get(self,request):
        return render(request, 'join.html', {})

    def post(self, request):
        user_email = request.POST.get('user_email')
        user_nick_name = request.POST.get('user_nick_name')
        user_password = request.POST.get('user_password')

        upload_file = request.FILES.get('upload_file')


        # cert_name_array = request.POST.getlist('cert_name_array[]')
        # cert_date_array = request.POST.getlist('cert_date_array[]')
        # cert_no_array = request.POST.getlist('cert_no_array[]')

        context = {}

        user = User.objects.filter(email=user_email).first()

        if user is not None:
            context['status'] = 400
            context['message'] = "같은 이메일 존재!!"
            return JsonResponse(context)


        try:
            user = User(email=user_email
                        , password=user_password
                        , username=user_nick_name)
            user.save()

            if upload_file is not None:
                directory_path = 'upload_files/' + str(user.pk) + '/user_profile/'
                filename = upload_file.name

                s3 = boto3.client("s3"
                                  , aws_access_key_id=config.S3_ACCESS_KEY
                                  , aws_secret_access_key=config.S3_SECRET_KEY
                                  )
                s3.put_object(Bucket=config.S3_BUCKET, Key=(directory_path))
                s3.upload_fileobj(upload_file, config.S3_BUCKET, directory_path + filename)

                extend_user = ExtendUser(user=user
                                , user_profile=config.S3_BUCKET_URL + directory_path + filename)
                extend_user.save()


        except Exception as err:
            print(str(err))
            context['status'] = 500
            context['message'] = "저장 에러!!"
            return JsonResponse(context)

        token = jwt.encode({'email': user_email}, 'secret', algorithm='HS256')

        context['status'] = 200
        context['message'] = "success!!"
        context['access_token'] = token.decode('UTF-8')
        return JsonResponse(context)

class SocialJoinView(View):

    def get(self,request):
        return render(request, 'socialjoin.html', {})

    def post(self, request):
        user_nick_name = request.POST.get('user_nick_name')
        upload_file = request.FILES.get('upload_file')
        profile_path = ""
        # cert_name_array = request.POST.getlist('cert_name_array[]')
        # cert_date_array = request.POST.getlist('cert_date_array[]')
        # cert_no_array = request.POST.getlist('cert_no_array[]')

        context = {}

        try:
            user = request.user
            user.username = user_nick_name
            user.save()

            if upload_file is not None:
                directory_path = 'upload_files/' + str(user.pk) + '/user_profile/'
                filename = upload_file.name

                s3 = boto3.client("s3"
                                  , aws_access_key_id=config.S3_ACCESS_KEY
                                  , aws_secret_access_key=config.S3_SECRET_KEY
                                  )
                s3.put_object(Bucket=config.S3_BUCKET, Key=(directory_path))
                s3.upload_fileobj(upload_file, config.S3_BUCKET, directory_path + filename)

                profile_path = config.S3_BUCKET_URL + directory_path + filename

            extend_user = ExtendUser(user=user
                            , user_profile=profile_path)
            extend_user.save()


        except Exception as err:
            print(str(err))
            context['status'] = 500
            context['message'] = "저장 에러!!"
            return JsonResponse(context)

        token = jwt.encode({'email': user.email}, 'secret', algorithm='HS256')

        context['status'] = 200
        context['message'] = "success!!"
        context['access_token'] = token.decode('UTF-8')
        return JsonResponse(context)

#endregion

#region Page

class MainView(View):

    @method_decorator(login_required)
    def get(self,request, email):
        return render(request, 'main.html', {})

class MyDataView(View):

    @method_decorator(login_required)
    def get(self, request, email):
        user = User.objects.filter(email=email).first()
        # certlist = Certificate.objects.all()
        return render(request, 'mydata.html', {'user': user })
        # return render(request, 'mydata.html', {'user': user, 'certlist': certlist})

    @method_decorator(login_required)
    def post(self, request, email):
        user_nick_name = request.POST.get('user_nick_name')
        upload_file = request.FILES.get('upload_file')

        user = User.objects.filter(email=email).first()
        context = {}
        try:
            user.username = user_nick_name
            if upload_file is not None:
                directory_path = 'upload_files/' + str(user.pk) + '/user_profile/'
                filename = upload_file.name
                extend_user = ExtendUser.objects.get(user=user)
                extend_user.user_profile = config.S3_BUCKET_URL + directory_path + filename

                s3 = boto3.client("s3"
                                  , aws_access_key_id=config.S3_ACCESS_KEY
                                  , aws_secret_access_key=config.S3_SECRET_KEY
                                  )
                s3.put_object(Bucket=config.S3_BUCKET, Key=( directory_path ))
                s3.upload_fileobj(upload_file, config.S3_BUCKET, directory_path + filename)
                extend_user.save()

            user.save()


        except Exception as err:
            print(str(err))
            context['status'] = 500
            context['message'] = "저장 에러!!"
            return JsonResponse(context)

        context['status'] = 200
        context['message'] = "success!!"
        return JsonResponse(context)

class AllTableView(View):

    @method_decorator(login_required)
    def get(self,request, email):

        userlist = User.objects.all()
        return render(request, 'alltable.html', {'userlist': userlist})





#endregion Page











#
# class FileDownload(View):
#
#     def get(self, request):
#         file_path = os.path.join(settings.MEDIA_ROOT, "abc.jpg")
#         if os.path.exists(file_path):
#             with open(file_path, 'rb') as fh:
#                 response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#                 response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#                 return response
#         raise Http404
#









#
#
#
# class UserViewSet(viewsets.ViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """
#     def list(self, request):
#         queryset = User.objects.all()
#         serializer = UserSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = User.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)


# class CertViewSet(viewsets.ViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """
#     def list(self, request):
#         queryset = Certificate.objects.all()
#         serializer = CertificateSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = Certificate.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = CertificateSerializer(user)
#         return Response(serializer.data)


# class CertViewSet(viewsets.ViewSet):
#     def get_queryset(self):
#         return Certificate.objects.filter(user=self.kwargs['user_pk'])
#
#     def list(self, request, user_pk=None):
#         certs = self.get_queryset()
#         serializer = CertificateSerializer(certs)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None, user_pk=None):
#         certs = self.get_queryset().get(pk=pk, user=user_pk)
#         serializer = CertificateSerializer(certs)
#         return Response(serializer.data)







