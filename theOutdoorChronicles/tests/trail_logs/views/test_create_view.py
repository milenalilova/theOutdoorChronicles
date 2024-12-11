from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tests.test_variables_data import user_data, trail_data, first_log_data, second_log_data
from theOutdoorChronicles.trail_logs.models import TrailLog
from theOutdoorChronicles.trails.models import Trail

UserModel = get_user_model()


class TrailLogCreateViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(user_data)
        self.trail = Trail.objects.create(**trail_data)
        self.url = reverse('trail-log-create', kwargs={'trail_id': self.trail.pk})

    def test__trail_added_to_context(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.context['trail'], self.trail)
        self.assertEqual(response.status_code, 200)

    def test__previous_logs_count__added_to_context(self):
        self.client.force_login(self.user)

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
