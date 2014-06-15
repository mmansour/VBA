import datetime
from haystack import indexes
from models import Agent


class AgentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    agent = indexes.CharField(model_attr='full_name')

    def get_model(self):
        return Agent

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(publish_date__lte=datetime.datetime.now())
