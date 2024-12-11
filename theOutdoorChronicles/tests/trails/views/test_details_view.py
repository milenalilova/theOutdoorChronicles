from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count, Avg
from django.test import TestCase
from django.urls import reverse

from tests.test_variables_data import user_data, trail_data, first_log_data, second_log_data
from theOutdoorChronicles.trail_logs.models import TrailLog
from theOutdoorChronicles.trails.models import Trail

UserModel = get_user_model()


class TrailDetailsViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(user_data)
        self.trail = Trail.objects.create(**trail_data)

        self.log_one = TrailLog.objects.create(**{
            **first_log_data,
            'user': self.user,
            'trail': self.trail
        })

        self.log_two = TrailLog.objects.create(**{
            **second_log_data,
            'user': self.user,
            'trail': self.trail
        })

    def test__trail_details_context_data__includes_public_stats(self):
        self.client.force_login(self.user)

        url = reverse('trail-details', kwargs={'trail_id': self.trail.pk})
        response = self.client.get(url)

        public_stats = self.trail.trail_logs.aggregate(
            total_hikers=Count('user', distinct=True),
            total_logs=Count('id'),
            avg_duration=Avg('duration') or timedelta(0),
        )

        public_stats['avg_duration'] = str(public_stats['avg_duration']).split('.')[0]

        self.assertDictEqual(response.context_data['public_stats'], public_stats)
        self.assertEqual(response.status_code, 200)
