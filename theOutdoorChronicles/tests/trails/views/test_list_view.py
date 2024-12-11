from django.contrib.auth import get_user_model

from django.test import TestCase
from django.urls import reverse

from tests.test_variables_data import user_data, trail_data

from theOutdoorChronicles.trails.models import Trail

UserModel = get_user_model()


class TrailListViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(user_data)
        self.trail = Trail.objects.create(**trail_data)

    def test__trail_list_view__uses_correct_template(self):
        self.client.force_login(self.user)

        url = reverse('trail-list')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'trails/trail-list-page.html')

    def test__trail_list_view__context_includes_search_form(self):
        self.client.force_login(self.user)

        url = reverse('trail-list')
        response = self.client.get(url)

        self.assertIn('trails_search_form', response.context)

    def test__trail_list_view__filters_queryset_based_on_search_query(self):
        self.client.force_login(self.user)

        url = reverse('trail-list') + '?search_query=France'
        response = self.client.get(url)

        self.assertEqual(len(response.context['object_list']), 1)

    def test__trail_list_view__clear_param_redirects_to_trail_list(self):
        self.client.force_login(self.user)

        url = reverse('trail-list') + '?search_query=France&clear=true'
        response = self.client.get(url)

        self.assertRedirects(response, reverse('trail-list'))
