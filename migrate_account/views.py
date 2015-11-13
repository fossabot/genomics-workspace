from __future__ import absolute_import
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.cache import cache
from uuid import uuid4
from os import path, makedirs, chmod
from blast.models import BlastDb, Organism, JbrowseSetting
from migrate_account.models import MigrateUserRecord
#from .tasks import run_clustal_task
#from clustal.models import ClustalQueryRecord
from datetime import datetime, timedelta
from pytz import timezone
import json
import traceback
import stat as Perm
import os
import re
import urllib2
import cookielib
from .forms import AddMigrationForm, ConfirmMigrationForm

# Create your views here.

@login_required
def index(request):
    current_user = request.user
    organism_list = sorted([db.id, db.display_name, db.short_name] for db in Organism.objects.all())
    user_list = sorted([udb.id, udb.organism_id, udb.user_id, udb.username, udb.password] for udb in MigrateUserRecord.objects.all().filter(user_id=request.user.id))
    result_set = []

    for organism in organism_list:
        blastdb_list = sorted([bdb.id, bdb.organism_id] for bdb in BlastDb.objects.all().filter(organism_id=organism[0]))
        for blast in blastdb_list:
            jbrowse_list = sorted([jdb.id, jdb.url, jdb.blast_db_id] for jdb in JbrowseSetting.objects.all().filter(blast_db_id=blast[0]))
            for jbrowse in jbrowse_list:
                var = [organism[0], organism[1], organism[2], jbrowse[1], False, None, None]
                for user in user_list:
                    if organism[0] == user[1] and user[2] == request.user.id:
                        var = [organism[0], organism[1], organism[2], jbrowse[1], True, user[3], user[4] ]
                result_set.append(var)

    return render(request,'migrate_account/main.html',{
            'title': 'Organism Listing',
            'organism_id':organism[0], 
            'organism_display_name':organism[1], 
            'organism_short_name':organism[2], 
            'jbrowse_url':jbrowse[1],
            'result_set': result_set
            })

@login_required
def add(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddMigrationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            organism_id = form.cleaned_data['organism_id']
            jbrowse_url =  form.cleaned_data['jbrowse_url']
            organism_display_name = form.cleaned_data['organism_display_name']
            organism_short_name = form.cleaned_data['organism_short_name']
            username =  form.cleaned_data['username']
            password =  form.cleaned_data['password']
#This is the type of command I need to use to test if the login is good...
# curl -b cookies.txt -c cookies.txt -e "https://apollo.nal.usda.gov"  -H "Content-Type:application/json" -d "{'username': 'demo', 'password': 'demo'}" "https://apollo.nal.usda.gov/lepdec_training/Login?operation=login" -k
            try:
                mu = MigrateUserRecord.objects.get(username=username, password = password, organism_id = organism_id)
                # Warning! This account has already been claimed!
                form = AddMigrationForm(request.POST)
                return render(request, 'migrate_account/add.html', {
                        'form': form,
                        'status': 'This account has already been claimed. Please verify your login and re-enter your credentials.'
                        })
            except MigrateUserRecord.DoesNotExist:
                m = MigrateUserRecord( username = username, password = password, organism_id = organism_id, user_id = request.user.id )
                m.save()
                return index(request)
    # if a GET (or any other method) we'll create a blank form
        else:
            form = AddMigrationForm(request.POST)
#            return index(request)
        return render(request, 'migrate_account/add.html', {
                'form': form
                })
    else:
        return index(request)




@login_required
def confirm(request):
    return()
