from itertools import chain

from django.core.cache import cache
from django.db.models import Q
from django.views.generic import TemplateView, ListView, DetailView

from theOutdoorChronicles.accounts.models import Profile
from theOutdoorChronicles.animals.models import Animal
from theOutdoorChronicles.common.forms import SearchForm
from theOutdoorChronicles.trails.models import Trail


class IndexView(ListView):
    context_object_name = 'searched_result'
    template_name = 'common/home-page.html'

    def get_queryset(self):
        queryset = None
        search_term = self.request.GET.get('search_term', '')
        if search_term:
            trails = Trail.objects.filter(
                Q(name__icontains=search_term) |
                Q(location__icontains=search_term)
            )

            animals = Animal.objects.filter(
                Q(common_name__icontains=search_term) |
                Q(species__icontains=search_term)
            )
            queryset = list(chain(trails, animals))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET)

        if self.request.user.is_authenticated:
            user_location = Profile.objects.get(user=self.request.user).location
            random_trails = None
            random_animals = None

            if user_location:
                random_trails = Trail.objects.filter(location__icontains=user_location)
                random_animals = (t.animals for t in random_trails)
            #     TODO check what's inside random trails

            if not user_location or not random_trails:
                random_trails = Trail.objects.order_by('?')[:5]
                random_animals = Animal.objects.order_by('?')[:5]

            context['random_trails'] = random_trails
            context['random_animals'] = random_animals

        else:
            random_trails = cache.get('daily_trails')
            random_animals = cache.get('daily_animals')

            if not random_trails:
                random_trails = list(Trail.objects.order_by('?')[:5])
                cache.set('daily_trails', random_trails, 86400)  # cashes for 24h

            if not random_animals:
                random_animals = list(Animal.objects.order_by('?')[:5])
                cache.set('daily_animals', random_animals, 86400)

            context['random_trails'] = random_trails
            context['random_animals'] = random_animals

        return context
