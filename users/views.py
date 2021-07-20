import json
import urllib

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.contrib.auth import views as auth_views
from django.contrib import messages
from users.forms import CreateAccountForm, UserPasswordResetForm
from users.models import User
from django.http import JsonResponse
# Create your views here.
#https://www.agiliq.com/blog/2019/01/django-createview/

class SignUpView(CreateView):
    form_class = CreateAccountForm
    template_name = 'users/signup.html'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.

        #Begin reCAPTCHA validation
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        #End reCAPTCHA validation

        if result['success']:
            self.object = form.save()
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, 'Invalid reCAPTCHA. Please try again.')

        return render(self.request, 'users/signup.html', {'form':self.form_class})

    #form_invalid --> httpresonse on invalid form

class ValidateIdentififer(View):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('users:signup')

    def get(self, request, *args, **kwargs):
        identifier = self.request.GET.get('identifier', None)
        data = {
            'is_taken': User.objects.filter(identifier__iexact=identifier).exists()
        }
        if data['is_taken']:
            data['error_message'] = 'A user with this username already exists.'
        return JsonResponse(data)

class MyPasswordResetView(auth_views.PasswordResetView):
    success_url = reverse_lazy('password_reset_done')
    template_name = 'password_reset/password_reset_form.html'
    form_class = UserPasswordResetForm

class MyPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'password_reset/password_reset_done.html'

class MyPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'password_reset/password_reset_confirm.html'

class MyPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'password_reset/password_reset_complete.html'
