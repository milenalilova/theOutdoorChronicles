from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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

first_log_data = {
    'title': 'Nice Walk',
    'date_completed': date(2000, 12, 25),
    'notes': 'It was a good walk',
}
second_log_data = {
    'title': 'Another Nice Walk',
    'date_completed': date(2000, 12, 28),
    'notes': 'It was another good walk'
}


class TrailLogDeleteViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username='testuser', email='pepi@pepi.com', password='testpass')
        self.client.login(email='pepi@pepi.com', password='testpass')

        self.trail = Trail.objects.create(
            name='TestTrail',
            location='France',
            length=15,
            elevation_gain=125,
            difficulty='Easy',
            route_type='Loop',
            description='Difficult'
        )

        self.trail_log = TrailLog.objects.create(
            title='Test Trail Log',
            date_completed='2024-01-01',
            duration='01:30:00',
            weather_conditions='Sunny',
            trail_conditions='Good',
            difficulty_rating='Moderate',
            notes='Great hike!',
            user=self.user,
            trail=self.trail
        )

        self.url = reverse('trail-log-delete', kwargs={'trail_log_id': self.trail_log.id})

    def test_trail_log_delete(self):
        self.assertEqual(TrailLog.objects.count(), 1)

        response = self.client.post(self.url, {})

        self.assertEqual(TrailLog.objects.count(), 0)
        self.assertRedirects(response, reverse('trail-logs-my-logs'))

#   TODO the test fails. The form is invalid
