import django_filters
from django_filters import OrderingFilter
from .models import Thing

FILTER_ORDERING_TITLE_CHOICES = (
    ('title', 'title'),
    ('-title', '-title')
)

class ThingFilter(django_filters.FilterSet):
    date_start = django_filters.DateFilter(field_name='date_published', lookup_expr='gte')
    date_end = django_filters.DateFilter(field_name='date_published', lookup_expr='lte')
    order_by = django_filters.ChoiceFilter(method='filter_order_by', choices=FILTER_ORDERING_TITLE_CHOICES)
    state = django_filters.ChoiceFilter(field_name='state', choices=Thing.STATE_CHOICES)
    section = django_filters.NumberFilter(field_name='section')
    tags = django_filters.NumberFilter(field_name='tags')

    class Meta:
        model = Thing
        fields = ['date_start', 'date_end', 'order_by', 'state', 'section', 'tags']

    def filter_order_by(self, queryset, name, value):
        if value:
            return queryset.order_by(value)
