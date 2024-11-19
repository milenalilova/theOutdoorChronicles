from django import forms

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

    class Meta:
        model = TrailLog
        exclude = ('user',)


class TrailLogCreateForm(TrailLogBaseForm):
    pass

# TODO exclude the trail field. Takes the pk from url


class TrailLogEditForm(TrailLogBaseForm):
    pass


class TrailLogDeleteForm(TrailLogBaseForm):
    class Meta(TrailLogBaseForm.Meta):
        exclude = ('trail', 'user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['readonly'] = 'readonly'
