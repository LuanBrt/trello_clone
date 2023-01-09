
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, Div
from django.urls import reverse_lazy

from cards.models import Item, Tag

class TagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'tag-form'

        self.helper.add_layout(Layout('name', 'color', HTML("""<input class="btn btn-primary"
                                                                hx-post={% url 'cards:tag-list' %}
                                                                hx-trigger="click"
                                                                _="on htmx:afterRequest send click to closest .dropdown-toggle"
                                                                type="reset"
                                                                value="Submit">
                                                                </input>""")))

    class Meta:
        model = Tag
        fields = ['name', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }

class ItemDescriptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemDescriptionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = f'item{self.instance.uuid}detailsform'
        self.helper.attrs = {'hx-put': reverse_lazy('cards:item', kwargs={'uuid': self.instance.uuid }),
                             'hx-trigger': 'detailsformsubmit from:body',
                             'hx-swap': 'none'}
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Fieldset('',
                'title',
                HTML("""<h5>Description</h5>"""),
                'description',
                HTML("""<h5>Item Details</h5>"""),
                Div(HTML('<label class="col-form-label">Due date</label>'), 'due_date', css_class='form-row'),
            ),)

        

    class Meta:
        model = Item
        fields = ['title', 'description', 'due_date']

    title =  forms.CharField(widget=forms.TextInput(attrs={'style': 'border-style: none; font-size: 2.0rem; color: black; outline:none !important;'}), 
    label='')

    description = forms.CharField(widget=forms.Textarea(attrs={'style': 'border-style: none; resize: none; background-color: white !important; width:90%; color: black; max-height:50vh;', 
                                                               'cols': '100',
                                                               'rows': '3',

                                                                # for the resizing of the text area
                                                               'oninput': 'this.style.height = ""; this.style.height = this.scrollHeight + 3 + "px"',
                                                                '_': 'on load js(me) me.style.height = ""; me.style.height = me.scrollHeight + 3 + "px"',
                                                               'placeholder': 'Enter your description',}), label='', required=False)

    due_date = forms.DateField(widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'placeholder':'Select a date', 'type':'date'}), label='', required=False)