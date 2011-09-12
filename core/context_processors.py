from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.decorators import login_required


@login_required
def add_flatpages(request):
    return {'flatpages':FlatPage.objects.all()}
