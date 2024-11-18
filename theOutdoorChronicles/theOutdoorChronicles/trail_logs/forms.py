from django import forms

from theOutdoorChronicles.trail_logs.models import TrailLog


class TrailLogBaseForm(forms.ModelForm):
    class Meta:
        model = TrailLog
        exclude = ('user',)


class TrailLogCreateForm(TrailLogBaseForm):
    pass

# TODO fix date field to display date format


class TrailLogEditForm(TrailLogBaseForm):
    pass


class TrailLogDeleteForm(TrailLogBaseForm):
    class Meta(TrailLogBaseForm.Meta):
        exclude = ('trail', 'user')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['readonly'] = 'readonly'
