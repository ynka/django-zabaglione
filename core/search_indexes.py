from haystack import indexes
from haystack import site
from core.models import Ticket, Project, News

class TicketIndex(indexes.SearchIndex):
    text = indexes.CharField(use_template=True,document=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')

class ProjectIndex(indexes.SearchIndex):
    text = indexes.CharField(use_template=True,document=True)
    name = indexes.CharField(model_attr='name')
    description = indexes.CharField(model_attr="description")

class NewsIndex(indexes.SearchIndex):
    text = indexes.CharField(use_template=True,document=True)
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')


site.register(Project,ProjectIndex)
site.register(Ticket, TicketIndex)
site.register(News,NewsIndex)

