# # Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# from django.urls import reverse
from .models import Project, ContactInfo, MyLanguage, MySkill, MyTool, MyTitle, MyInfo
from .forms import ContactForm


# Create your views here.
@csrf_exempt
def index(request, **kwargs):
   myinfo = MyInfo.objects.all()[:1][0]

   Data = {
      'Skills': MySkill.objects.filter(is_hidden=False),
      'Tools': MyTool.objects.filter(is_hidden=False),
      'Languages': MyLanguage.objects.filter(is_hidden=False),
      'Titles': MyTitle.objects.filter(is_hidden=False),
      'Description': myinfo.home_description,
      'PersonalImage': myinfo.personal_image.url,
   }
   print(Data)
   return render(request, 'pages/home.html', Data)


@csrf_exempt
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
   
      myinfo = MyInfo.objects.all()[:1][0]
      Data = {
         'isSuccess' : isSuccess,
         'message': message,
         'PersonalImage': myinfo.personal_image.url,
      }
      
      return HttpResponse(render(request, 'pages/contact.html', Data))

   return render(request, 'pages/contact.html')


def portfolio(request, **kwargs):
   myinfo = MyInfo.objects.all()[:1][0]

   Data = {
      'Projects': Project.objects.all().filter(is_hidden=False).order_by('date'),
      'Description': myinfo.portfolio_description
   }
   return render(request, 'pages/portfolio.html', Data)


def pdf_view(request, **kwargs):
   myinfo = MyInfo.objects.all()[:1][0]
   Data = {
      'resume_url': myinfo.resume.url
   }
   return render(request, 'pages/resume.html', Data)