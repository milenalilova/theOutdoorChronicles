from django import forms

from theOutdoorChronicles.common.forms import BaseSearchForm
from theOutdoorChronicles.trails.models import Trail


class TrailBaseForm(forms.ModelForm):
    class Meta:
        model = Trail
        fields = '__all__'


class TrailCreateForm(TrailBaseForm):
    pass


class TrailEditForm(TrailBaseForm):
    pass


class TrailDeleteForm(TrailBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs['readonly'] = 'readonly'


class TrailSearchForm(BaseSearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, placeholder='Search trails by name or location', **kwargs)
