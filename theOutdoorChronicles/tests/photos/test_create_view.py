from datetime import date

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from theOutdoorChronicles.photos.models import Photo
from theOutdoorChronicles.trails.models import Trail

UserModel = get_user_model()

user_data = {
    'username': 'testuser',
    'email': 'pepi@pepi.com',
    'password': 'pass1234'
}

photo_data = {
    'image': 'images/photo_uploads/image.jpg',
    'description': 'A beautiful trail photo.',
    'date_uploaded': date(2000, 12, 25)
}

trail_data = {
    'name': 'TestTrail',
    'location': 'France',
    'length': 15,
    'elevation_gain': 125,
    'difficulty': 'Easy',
    'route_type': 'Loop',
    'description': 'Difficult'
}
animal_data = {
    'image': 'images/photo_uploads/image.jpg',
    'common_name': 'sparrow',
    'species': 'some_name',
    'conservation_status': 'CB',
    'description': 'Some description',
    'wikipedia_page': 'https://en.wikipedia.org/wiki/House_sparrow',
}


class PhotoCreateViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(user_data)
        self.client.force_login(self.user)
        self.trail = Trail.objects.create(**trail_data)
        self.photo = Photo.objects.create(**photo_data, user=self.user, trail=self.trail)
        with open('mediafiles/images/photo_uploads/animals_hero_snakes.jpg', 'rb') as f:
            self.real_image = SimpleUploadedFile('animals_hero_snakes', f.read(), content_type='image/jpeg')

        self.url = reverse('photo-create')
        response = self.client.post(self.url)

    def test__photo_exists(self):
        self.assertEqual(Photo.objects.count(), 1)

    def test__photo_create__redirects_to_trail_details(self):
       pass

    def test__photo_update__redirects_to_animal_details(self):
        pass

    def test__photo_update__redirects_to_trail_log_details(self):
        pass
