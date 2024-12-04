from django import forms


class BaseSearchForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={}),
    )

    def __init__(self, *args, placeholder='', **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_query'].widget.attrs['placeholder'] = placeholder
