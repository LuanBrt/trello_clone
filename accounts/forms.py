from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import Layout, Field


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(
            Submit('submit', 'Submit', css_class='btn-primary'))


class UserRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.add_layout(Layout(CustomField('username'),
                                      CustomField('password1'),
                                      CustomField('password2')))


        # restrict user of submiting form if it's not valid
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary',
                              disabled=not self.is_valid(), hx_swap_oob='true'))

        # htmx for doing asynchronous validation on the fields
        for k, field in self.fields.items():
            field.widget.attrs.update({'hx-post': reverse_lazy('accounts:register'),
                                       'autocomplete': 'off',
                                       'hx-swap': 'none',
                                       'autofocus': False, })

        self.fields['username'].widget.attrs.update({'hx-select-oob': 'id_username-errors,id_password2-errors'})
        self.fields['password1'].widget.attrs.update({'hx-select-oob': 'id_password1-errors,id_password2-errors'})
        self.fields['password2'].widget.attrs.update({'hx-select-oob': 'id_password2-errors'})

class CustomField(Field):
    """ We create this field just to select where the errors will be swapped in the ui"""
    template = 'accounts/snippets/custom_field.html'


