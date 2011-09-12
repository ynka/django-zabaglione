#*- coding: utf-8 -*-
from core.forms import *
from core.models import *
from datetime import date, timedelta
from dateutil.rrule import rrule,WEEKLY
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mass_mail
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import loader, RequestContext
from django.utils.translation import ugettext as _
from django.views.generic import list_detail
from haystack.views import basic_search
from object_permissions.helpers import has_permissions_or_403
import os
import subprocess

@login_required
def index(request):
    ''' Strona glowna '''
    return render(request, 'core/index.html')

@login_required
def projects(request):
    ''' Lista projektow danego usera '''
    projects = Project.objects.for_user(request.user)
    latest_news = News.objects.order_by('-created').filter(project__in=projects)
    return render(request,
                  'core/project_list.html',
                  {'projects' : projects, 'latest_news':latest_news})

@login_required
def project_detail(request,object_id):
    ''' Szczegoly projektu '''
    project = get_object_or_404(Project, pk=object_id)
    has_permissions_or_403(request.user, "view", project)
    tickets = Ticket.objects.filter(project=project)
    return render(request,
                  'core/project_detail.html',
                  {'project' : project,'tickets' : tickets})


@login_required
def project_repository(request, object_id):
    ''' Widok repozytorium zwiazanego z projektem - komunikuje sie przez
        subprocess z Mercurialem '''
    project = get_object_or_404(Project, pk=object_id)
    has_permissions_or_403(request.user, "view", project)
    
    # projekt nie ma podanej sciezki do repo, ale ktos requestuje url,
    # ktory ja serwuje - np wpisane z palca do paska przegladarki = hacker :P
    if not project.repository_path:
        raise Http404

    stdout, stderr = "", ""
    try:
        pipe = subprocess.Popen(
                [settings.MERCURIAL_BIN, "log"], # polecenie "hg log"
                cwd = project.repository_path,   # w folderze repo projektu
                stdout = subprocess.PIPE,        # przechwycenie stdout
                stderr=subprocess.PIPE)          # i stderr
        (stdout, stderr) = pipe.communicate()
    except OSError:
        messages.error(request, _('OS Error (bad repository path or filesystem permissions)'))

    # niepuste stderr oznacza blad od Mercuriala
    if stderr:
        messages.error(request, _('Mercurial error: %s' % stderr))

    log = stdout.split("\n")
    log = [line for line in log if line != "\n"]
    log = [log[i:i+3] for i in xrange(0, len(log)-1, 4)]

    return render(request, 'core/project_repository.html', {'project' : project, 'log' : log})

@login_required
def add_or_update_ticket(request, project_id, ticket_id=None):
    project = get_object_or_404(Project, pk=project_id)
    has_permissions_or_403(request.user, "change", project)

    adding = ticket_id is None

    if adding:
        # tworzenie ticketa
        ticket = Ticket(author=request.user, project=project)
    else:
        # edycja ticketa
        ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket, parent_project=project)
        if form.is_valid():
            ticket = form.save()
            if adding:
                ok_msg = _('Ticket creation successful')
            else:
                ok_msg = _('Ticket update successfull')

            messages.success(request, ok_msg)
            return HttpResponseRedirect(reverse('ticket_detail_url',
                                                kwargs={'project_id' : project.pk,
                                                        'object_id'  : ticket.pk}))
        
        else: # niepowodzenie dodawania/uaktualniania
            if adding:
                fail_msg = _('Ticket creation failed. Correct errors and try again')
            else:
                fail_msg = _('Ticket update failed. Correct errors and try again')

            messages.error(request, fail_msg)
    else: # GET
        form = TicketForm(instance = ticket, parent_project=project)
    
    return render(request, 'core/add_ticket.html', {'tform' : form, 'project' : project})

@login_required
def add_ticket(request,object_id):
    ''' Dodawanie ticketa - wyswietlanie formularza, obsluga POSTu '''
    project = get_object_or_404(Project, pk=object_id)
    has_permissions_or_403(request.user, "change", project)
    if request.method == "POST":
        tform = TicketForm(data = request.POST)
        if tform.is_valid():
            ticket = tform.save(commit=False)
            ticket.project = project
            ticket.author = request.user
            ticket.save()
            tform.save_m2m()
            messages.success(request,_('Ticket creation successful.'))
            return HttpResponseRedirect(reverse('ticket_detail_url',
                                                kwargs={'project_id' : project.pk,
                                                        'object_id' : ticket.pk}))
        else:
            messages.error(request,_('Ticket creation failed. Correct errors below and try again.'))
    else:
        tform = TicketForm()

    # ograniczenie zbioru mozliwych do ustawienia wersji do wersji
    # zwiazanych z aktualnym projektem
    tform.fields['version'].queryset = project.version_set
    return render(request, 'core/add_ticket.html',{'tform' : tform, 'project' : project })


@login_required
def update_ticket(request,object_id,project_id):
    ticket = get_object_or_404(Ticket, pk=object_id)
    project = ticket.project
    has_permissions_or_403(request.user, "change", project)
    if request.method == "POST":
        tform = TicketForm(request.POST, instance=ticket)
        if tform.is_valid():
            ticket = tform.save(commit=False)
            # ticket.project = project
            ticket.save()
            tform.save_m2m()
            messages.success(request,_('Ticket update successful.'))
            return HttpResponseRedirect(reverse('ticket_detail_url', kwargs={'project_id' : ticket.project.pk, 'object_id' : ticket.pk}))
        else:
            tform.fields['version'].queryset = project.version_set
            print tform.errors
            messages.error(request,_('Ticket update failed. Corrert errors below and try again.'))
    else:
        tform = TicketForm(instance=ticket)
        tform.fields['version'].queryset = project.version_set
    return render(request, 'core/add_ticket.html',{'tform' : tform, 'project' : ticket.project, 'ticket_id' : ticket.pk})


@login_required
def add_related_ticket(request,project_id,object_id):
    ''' Dodawanie ticketu zwiazanego (np. x duplikuje y, x poprzedza y
        itp) '''
    ticket = get_object_or_404(Ticket, pk=object_id)
    has_permissions_or_403(request.user, "change", ticket.project)
    if request.method == "POST":
        form = RelatedTicketsForm(data = request.POST)
        if form.is_valid():
            related = form.save(commit=False)
            related.first = ticket
            related.save()
            form.save_m2m()
            messages.success(request,_('Relation creation successful.'))
            return HttpResponseRedirect(reverse('ticket_detail_url',
                                                kwargs={'project_id' : ticket.project.pk,
                                                        'object_id' : ticket.pk}))
        else:
            messages.error(request,_('Relation creation failed.'))
    else:
        form = RelatedTicketsForm()

        # do wyboru w formularzu sa tylko tickety z tego samego projektu,
        # z wylaczeniem samego siebie
        form.fields['second'].queryset = Ticket.objects.filter(project=ticket.project).exclude(pk=ticket.pk)
    return render(request,
                  'core/add_related_ticket.html',
                  {'ticket':ticket,'form':form})

@login_required
def ticket_detail(request,object_id,project_id):
    ''' Szczegoly ticketu '''
    ticket = get_object_or_404(Ticket, pk=object_id)
    has_permissions_or_403(request.user, "view", ticket.project)
    workers = ticket.workers.all()
    first_related = RelatedTickets.objects.filter(first=ticket.pk)
    second_related = RelatedTickets.objects.filter(second=ticket.pk)
    return render(request,
                  'core/ticket_detail.html',
                  {'ticket' : ticket,
                   'workers' : workers,
                   'first_related':first_related,
                   'second_related':second_related})

@login_required
def news(request,object_id):
    project = get_object_or_404(Project, pk=object_id)
    has_permissions_or_403(request.user, "view", project)
    news = project.news_set.all().order_by('-created')
    return render(request, 'core/news_list.html',{'news' : news,
        'project':project})


@login_required
def news_detail(request,object_id,project_id):
    news = get_object_or_404(News, pk=object_id)
    has_permissions_or_403(request.user, "view", news.project)
    return render(request, 'core/news_detail.html',{'news' : news})

@login_required
def add_news(request,object_id):
    project = get_object_or_404(Project, pk=object_id)
    has_permissions_or_403(request.user, "change", project)
    if request.method == "POST":
        nform = NewsForm(data = request.POST)
        if nform.is_valid():
            news = nform.save(commit=False)
            news.project = project
            news.author = request.user
            news.save()
            messages.success(request,_('News creation successful.'))
            return render(request,
                          'core/news_detail.html',
                          {'news': news})
        else:
            messages.error(request,_('News creation failed.'))
            return render(request,
                          'core/add_news.html',
                          {'nform' : nform, 'project' : project })

    else:
        nform = NewsForm()
        return render(request, 'core/add_news.html',{'nform' : nform, 'project' : project })

@login_required
def custom_search_view(request, *args, **kwargs):
    return basic_search(request, *args, **kwargs)
