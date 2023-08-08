# from django.shortcuts import render
# from django.http import HttpResponse
# # Create your views here.
# def index(request):
#    response = HttpResponse()
#    response.writelines('<h1>Xin chào</h1>')
#    response.write('Đây là app home')
#    return response

# # Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .models import Article

# Create your views here.
def index(request):
   return render(request, 'pages/home.html')


def contact(request):
   return render(request, 'pages/contact.html')


def portfolio(request):
   Data = {'Articles': Article.objects.all().order_by('date')}

   return render(request, 'pages/portfolio.html', Data)