from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper


class UserRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'registration-form'
        
        # htmx for doing asynchronous validation on the fields
        for k, field in self.fields.items():
            field.widget.attrs.update({'hx-post': reverse_lazy('accounts:register'),
                                    'hx-target': f'#div_id_{k}',
                                    'hx-swap': 'outerHTML',
                                    'hx-sync': 'closest form:abort',
                                    'autofocus': False,
                                    'hx-select': f'#div_id_{k}',
                                    'hx-preserve': ''})

