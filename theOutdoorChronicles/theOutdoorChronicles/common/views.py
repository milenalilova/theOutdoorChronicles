from django.core.cache import cache
from django.views.generic import TemplateView

from theOutdoorChronicles.accounts.models import Profile
from theOutdoorChronicles.animals.models import Animal
from theOutdoorChronicles.trails.models import Trail


class IndexView(TemplateView):
    template_name = 'common/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            user_location = Profile.objects.get(user=self.request.user).location
            random_trails = None

            if user_location:
                random_trails = Trail.objects.filter(location__icontains=user_location)

            if not user_location or not random_trails:
                random_trails = Trail.objects.order_by('?')[:5]

            context['random_trails'] = random_trails
            context['random_animals'] = None  # Placeholder for future animal logic
            #     TODO add animals on those trails

        else:
            random_trails = cache.get('daily_trails')
            random_animals = cache.get('daily_animals')

            if not random_trails:
                random_trails = list(Trail.objects.order_by('?')[:5])
                cache.set('daily_trails', random_trails, 86400)

            if not random_animals:
                random_animals = list(Animal.objects.order_by('?')[:5])
                cache.set('daily_animals', random_animals, 86400)

            context['random_trails'] = random_trails
            context['random_animals'] = random_animals

        return context
