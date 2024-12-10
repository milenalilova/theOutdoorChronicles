from datetime import date

from django.contrib.auth import get_user_model
from django.db.models import Count
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


class TestAnimalDetailsView(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(user_data)
        self.animal = Animal.objects.create(**animal_data)
        self.trail = Trail.objects.create(**trail_data)
        self.trail_log = TrailLog.objects.create(**{
            **first_log_data,
            'user': self.user,
            'trail': self.trail
        })

        self.animal.trails.add(self.trail)
        self.animal.trail_logs.add(self.trail_log)

    def test__animal_exists(self):
        self.assertTrue(Animal.objects.exists())

    def test__animal_details__returns_correct_status_code(self):
        self.client.force_login(self.user)

        url = reverse('animal-details', kwargs={'animal_id': self.animal.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test__animal_details_context_data__adds_public_stats(self):
        self.client.force_login(self.user)

        url = reverse('animal-details', kwargs={'animal_id': self.animal.pk})
        response = self.client.get(url)

        public_stats = self.animal.trail_logs.aggregate(
            total_observers=Count('user', distinct=True),
            total_logs=Count('id')
        )

        self.assertDictEqual(response.context['public_stats'], public_stats)

    def test__animal_details__uses_correct_template(self):
        self.client.force_login(self.user)

        url = reverse('animal-details', kwargs={'animal_id': self.animal.pk})
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'animals/animal-details-page.html')
