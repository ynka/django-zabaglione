# -*- coding: utf-8 -*-
from django.forms import ModelForm
from core.models import Project, Ticket, News, RelatedTickets
from django import forms

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('members')

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ('project','author','related')

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('parent_project', None)
        super(TicketForm, self).__init__(*args, **kwargs)

        if project is not None:
            self.fields['version'].queryset = project.version_set


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        exclude=('project','author')

class RelatedTicketsForm(forms.ModelForm):
    class Meta:
        model=RelatedTickets
        exclude=('first')

