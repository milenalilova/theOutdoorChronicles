from django.core.cache import cache
from django.shortcuts import render
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
            random_animals = None

            if user_location:
                random_trails = Trail.objects.filter(location__icontains=user_location)
                random_animals = Animal.objects.filter(trails__in=random_trails).distinct()
                # Some trails have no animals

            if not user_location or not random_trails:
                random_trails = Trail.objects.order_by('?')[:5]
                random_animals = Animal.objects.order_by('?')[:5]

            context['random_trails'] = random_trails
            context['random_animals'] = random_animals
            context['user_location'] = user_location

        else:
            random_trails = cache.get('daily_trails')
            random_animals = cache.get('daily_animals')

            if not random_trails:
                random_trails = list(Trail.objects.order_by('?')[:5])
                cache.set('daily_trails', random_trails, 86400)  # Cashes for 24h

            if not random_animals:
                random_animals = list(Animal.objects.order_by('?')[:5])
                cache.set('daily_animals', random_animals, 86400)  # Cashes for 24h

            context['random_trails'] = random_trails
            context['random_animals'] = random_animals

        return context


class AboutView(TemplateView):
    template_name = 'common/about-page.html'


def custom_403(request, exception):
    return render(request, 'errors/403.html', status=403)


def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)
