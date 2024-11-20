from django import forms

from theOutdoorChronicles.animals.models import Animal
from theOutdoorChronicles.trails.models import Trail


class AnimalBaseForm(forms.ModelForm):
    trails = forms.ModelMultipleChoiceField(
        queryset=Trail.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = Animal
        exclude = ('trail_logs',)


class AnimalCreateForm(AnimalBaseForm):
    pass


class AnimalEditForm(AnimalBaseForm):
    pass


class AnimalDeleteForm(AnimalBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'trails' in self.fields:
            del self.fields['trails']

        for _, field in self.fields.items():
            field.widget.attrs['readonly'] = 'readonly'


class AnimalSearchForm(forms.Form):
    animal_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search animal by common_name or species',
            }
        )
    )

# TODO rename the field or hide from temlpate
