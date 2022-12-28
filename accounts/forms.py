from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import PasswordInput

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))


class UserRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
        self.helper.form_id = 'registration-form'

        # we need this to preserve the password values in the form when a validation request is made
        self.fields['password1'].widget = PasswordInput(render_value = True)
        self.fields['password2'].widget = PasswordInput(render_value = True)
        
        # htmx for doing asynchronous validation on the fields
        for k, field in self.fields.items():
            field.widget.attrs.update({'hx-post': reverse_lazy('accounts:register'),
                                    'autocomplete': 'off',
                                    'hx-target': f'#div_id_{k}',
                                    'hx-swap': 'outerHTML',
                                    'hx-sync': 'closest form:abort',
                                    'autofocus': False,
                                    'hx-select': f'#div_id_{k}'})

        self.fields['password1'].widget.attrs.update({'hx-select-oob': '#div_id_password2'})

