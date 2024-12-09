from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from theOutdoorChronicles.trail_logs.models import TrailLog
from theOutdoorChronicles.trails.models import Trail

UserModel = get_user_model()

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
    'notes': 'It was a good walk'
}
second_log_data = {
    'title': 'Another Nice Walk',
    'date_completed': date(2000, 12, 28),
    'notes': 'It was another good walk'
}


class TrailLogCreateViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username='testuser', email='pepi@pepi.com', password='pass1234')
        self.trail = Trail.objects.create(**trail_data)
        self.url = reverse('trail-log-create', kwargs={'trail_id': self.trail.pk})

    def test__trail_added_to_context(self):
        self.client.login(email='pepi@pepi.com', password='pass1234')

        response = self.client.get(self.url)

        self.assertEqual(response.context['trail'], self.trail)
        self.assertEqual(response.status_code, 200)

    def test__previous_logs_count__added_to_context(self):
        self.client.login(email='pepi@pepi.com', password='pass1234')

        log_one = TrailLog.objects.create(**{
            **first_log_data,
            'user': self.user,
            'trail': self.trail
        })
        log_two = TrailLog.objects.create(**{
            **second_log_data,
            'user': self.user,
            'trail': self.trail
        })

        response = self.client.get(self.url)

        self.assertEqual(response.context['previous_logs_count'], 2)
        self.assertEqual(response.status_code, 200)

    