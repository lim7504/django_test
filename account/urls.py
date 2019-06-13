from django.contrib import admin
from django.urls import path
from . import views


from rest_framework_nested import routers

# router = routers.SimpleRouter()
# router.register(r'users', views.UserViewSet, base_name="users")
# # urlpatterns = router.urls
#
#
# certs_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
# certs_router.register(r'certs', views.CertViewSet, base_name='user-certs')


# urlpatterns = patterns('',
#     url(r'^', include(router.urls)),
#     url(r'^', include(domains_router.urls)),
# )



urlpatterns = [
    path('', views.LoginView.as_view(), name="login"),
    path('sociallogin/', views.SocialLoginView.as_view(), name="sociallogin"),
    path('join/', views.JoinView.as_view(), name="join"),
    path('socialjoin/', views.SocialJoinView.as_view(), name="socialjoin"),

    path('main/', views.MainView.as_view(), name="main"),
    path('mydata/', views.MyDataView.as_view(), name="mydata"),
    path('alltable/', views.AllTableView.as_view(), name="alltable"),
    # path('filedownload/', views.FileDownload.as_view(), name="filedownload"),

]

# urlpatterns += router.urls
# urlpatterns += certs_router.urls



