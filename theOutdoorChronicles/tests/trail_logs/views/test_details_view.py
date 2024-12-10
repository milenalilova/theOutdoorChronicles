from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from theOutdoorChronicles.animals.models import Animal
from theOutdoorChronicles.trail_logs.models import TrailLog
from theOutdoorChronicles.trails.models import Trail

UserModel = get_user_model()

user_data = {
    'username': 'testuser',
    'email': 'pepi@pepi.com',
    'password': 'pass1234'
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

first_log_data = {
    'title': 'Nice Walk',
    'date_completed': date(2000, 12, 25),
    'notes': 'It was a good walk'
}
second_log_data = {
    'title': 'Another Nice Walk',
    'date_completed': date(2000, 12, 28),
    'notes': 'It was another good walk'
}


class TrailLogDetailsViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(user_data)
        self.trail = Trail.objects.create(**trail_data)
        self.animal = Animal.objects.create(**animal_data)
        self.trail_log = TrailLog.objects.create(**{
            **first_log_data,
            'user': self.user,
            'trail': self.trail
        })

        self.trail_log.animals.add(self.animal)

    def test__context_data__adds_animal(self):
        self.client.force_login(self.user)

        url = reverse('trail-log-details', kwargs={'trail_log_id': self.trail.id})
        response = self.client.get(url)

        self.assertIn('animals', response.context)

# TODO a real image must be added
