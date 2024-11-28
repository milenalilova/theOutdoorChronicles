from django import forms

from theOutdoorChronicles.photos.models import Photo


class PhotoBaseForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ('user',)


class PhotoCreateForm(PhotoBaseForm):
    pass


class PhotoEditForm(PhotoBaseForm):
    pass


class PhotoDeleteForm(PhotoBaseForm):
    class Meta(PhotoBaseForm.Meta):
        fields = ('description',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['readonly'] = 'readonly'

# TODO fix the form to show the photo itself, photos trails and animals as a list and display delete message
