import random
import factory
from vote.models import Vote

VOTE_VALUES = [x for x in Vote.ValueChoices.values]

def get_vote_value():
    return random.choice(VOTE_VALUES)


class VoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vote

    value = factory.LazyFunction(get_vote_value)