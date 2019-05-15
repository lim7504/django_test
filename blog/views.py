from django.shortcuts import render
from django.views.generic import View

# Create your views here.
class IndexView(View):

    def get(self,request):
        print('-----------------------')
        return render(request, 'blog/index.html', {})