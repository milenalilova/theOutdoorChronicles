from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tests.test_variables_data import user_data, trail_data, photo_data
from theOutdoorChronicles.photos.models import Photo
from theOutdoorChronicles.trails.models import Trail

UserModel = get_user_model()


class PhotoCreateViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(user_data)
        self.client.force_login(self.user)
        self.trail = Trail.objects.create(**trail_data)
        self.photo = Photo.objects.create(**photo_data, user=self.user, trail=self.trail)

        self.url = reverse('photo-create')
        response = self.client.post(self.url)

    def test__photo_exists(self):
        self.assertEqual(Photo.objects.count(), 1)
