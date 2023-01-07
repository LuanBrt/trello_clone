from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import PasswordInput
from crispy_forms.layout import Layout, HTML, Div, Field


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

        self.helper.add_layout(Layout(custom_render_field(self.fields['username'].label, self.fields['username'].help_text, 'username'),
                                      custom_render_field(self.fields['password1'].label, self.fields['password1'].help_text, 'password1'), 
                                      custom_render_field(self.fields['password2'].label, self.fields['password2'].help_text, 'password2')))

        self.helper.form_show_errors = False
        self.helper.form_show_labels = False

        # restrict user of submiting form if it's not valid
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary',
                              disabled=not self.is_valid(), hx_swap_oob='true'))

        # htmx for doing asynchronous validation on the fields
        for k, field in self.fields.items():
            field.help_text = ''
            field.widget.attrs.update({'hx-post': reverse_lazy('accounts:register'),
                                       'autocomplete': 'off',
                                       'hx-select-oob': f'#{k}-errors',
                                       'hx-swap': 'none',
                                       'autofocus': False, })

        self.fields['username'].widget.attrs.update({'hx-select-oob': 'username-errors,password2-errors'})
        self.fields['password1'].widget.attrs.update({'hx-select-oob': 'password1-errors,password2-errors'})


def custom_render_field(label, help_text, field):
    """ Custom rendering of form field, we do that so we can access the error div for swapping """
    error_html = """<div id="field-errors">
                        {% for error in form.field.errors %}
                            <span class="invalid-feedback mt-0 pb-1" ><strong>{{ error|escape }}</strong> </span>
                        {% endfor %}
                    </div>""".replace('field', field)
    div = Div(HTML(f"""<label for="{ field }">{ label }</label>"""), Field(field), HTML(error_html), 
              HTML(f"""<small class="form-text text-muted mt-0 pb-1" >{help_text}</small>"""), css_class='mb-3')

    return div

