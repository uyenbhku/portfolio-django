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
from django.views.decorators.csrf import csrf_protect
# from django.urls import reverse
from .models import Article, ContactInfo
from .forms import ContactForm



# Create your views here.
def index(request, **kwargs):
   return render(request, 'pages/home.html')


@csrf_protect
def contact(request, **kwargs):
   if request.method == "POST":
      #Get the posted form
      MyContactInfo = ContactForm(request.POST)
      
      if MyContactInfo.is_valid():
         name = MyContactInfo.cleaned_data['name']
         email = MyContactInfo.cleaned_data['email']
         message = request.POST.get('message').strip()
         # print(name, email,)
         new_info = ContactInfo(name=name, 
                     email=email, 
                     message=message)
         new_info.save()

         isSuccess = True
         message = 'Thank you for sending me a message. I will review and contact you soon!'
         print(new_info.get_client_message())
      else:
         print('Failed to read')
         message = 'Something happens, please try again later.'
         isSuccess = False

      Data = {
         'isSuccess' : isSuccess,
         'message': message,
      }
      
      return HttpResponse(render(request, 'pages/contact.html', Data))

   return render(request, 'pages/contact.html')


def portfolio(request, **kwargs):
   Data = {'Articles': Article.objects.all().order_by('date')}

   return render(request, 'pages/portfolio.html', Data)
