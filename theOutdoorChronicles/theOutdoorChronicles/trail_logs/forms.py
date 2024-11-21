from django import forms

from theOutdoorChronicles.animals.models import Animal
from theOutdoorChronicles.trail_logs.models import TrailLog


class TrailLogBaseForm(forms.ModelForm):
    date_completed = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )
    duration = forms.DurationField(
        widget=forms.TextInput(attrs={
            'placeholder': 'HH:MM'
        }),
        help_text='Enter duration as hours:minutes'
    )

    animals_spotted = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Animal.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-list'})
    )

    class Meta:
        model = TrailLog
        exclude = ('user', 'animals', 'photos')


class TrailLogCreateForm(TrailLogBaseForm):
    pass


class TrailLogEditForm(TrailLogBaseForm):
    pass


class TrailLogDeleteForm(TrailLogBaseForm):
    class Meta(TrailLogBaseForm.Meta):
        exclude = ('user', 'trail', 'photos')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['readonly'] = 'readonly'
