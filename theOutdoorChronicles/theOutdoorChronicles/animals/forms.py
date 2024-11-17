from django import forms

from theOutdoorChronicles.animals.models import Animal


class AnimalBaseForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = '__all__'


class AnimalCreateForm(AnimalBaseForm):
    pass


# TODO add multiple choice field for trails


class AnimalEditForm(AnimalBaseForm):
    pass


# TODO add multiple choice field for trails


class AnimalDeleteForm(AnimalBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['readonly'] = 'readonly'

#  TODO fix the form to show only the trails the animal is on
