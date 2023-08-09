from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label='name',
                            help_text="Please enter your name", 
                            max_length=200)
    email = forms.CharField(label='email',
                            help_text='Please enter your email so that I can contact you',
                            max_length=100)
    message = forms.Textarea()

        