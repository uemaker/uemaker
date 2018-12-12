from haystack import indexes

from book.models import Chapter


class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    content = indexes.CharField(model_attr='content')

    def get_model(self):
        return Chapter

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

