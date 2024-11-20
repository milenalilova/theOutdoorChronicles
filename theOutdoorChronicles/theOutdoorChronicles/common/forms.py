from django import forms


class SearchForm(forms.Form):
    search_term = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search trails or animals',
            }
        )
    )


# TODO split the form in 2 part - animals and trails