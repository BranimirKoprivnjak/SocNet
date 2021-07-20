from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm,
                                       PasswordResetForm)
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe

#forms.Form
#q = forms.CharField(label='search',
#                    widget=forms.TextInput(attrs={'placeholder': 'Search'}))
#forms.ModelForm
#class Meta:
#        model = MyModel
#        widgets = {
#            'name': forms.TextInput(attrs={'placeholder': 'Name'}),}

class CreateAccountForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('identifier', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.error_class = DivErrorList
        #removes default help_text
        for fieldname in ['identifier','email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs = {
                'class': 'wjQ2q'
            }

        self.fields['password1'].widget.attrs = {
            'maxlength': 128,
            'class': 'wjQ2q'
        }

        self.fields['password2'].widget.attrs = {
            'maxlength': 128,
            'class': 'wjQ2q'
        }

#Login view -> default form -> AuthenticationForm
class LoginForm(AuthenticationForm):
    #check AuthenticationForm on github
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.error_class = DivErrorList

        self.fields['password'].widget.attrs = {
            'maxlength': 128,
            'class': 'wjQ2q',
        }

        self.fields['username'].widget.attrs = {
            'class': 'wjQ2q',
        }

class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs = {
            'class': 'wjQ2q',
        }

class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        #mark_safe() -> Explicitly mark a string as safe for (HTML) output purposes
        #format_html() -> alternative
        return mark_safe('<div class="S8wIM">%s</div>' % ''
            .join(['<div class="bBQfN">%s</div>' % e for e in self]))

#<ul class="errorlist"><li>email<ul class="errorlist"><li>
#Enter a valid email address.</li></ul></li><li>
#password2<ul class="errorlist"><li>This password is too short.
#It must contain at least 8 characters.</l
#i><li>This password is too common.</li></ul></li></ul>
