from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import Http404
import sys
import json
import logging
from django.core.mail import send_mail
from blast.models import SearchQuery
from dashboard.models import SearchForm


import misc.fileline as src
from misc.logger import i5kLogger

dash = i5kLogger()

def dashboard(request):
    search_list = []
    if request.method == 'GET':
        id_num = 0
        if request.path == '/dashboard':
            return render(request, 'dashboard/index.html')
        if request.path == '/blast_hist':
            search_list = []
            for obj in SearchQuery.objects.all():
                search_dict = {}
                id_num += 1
                orgs = json.loads(obj.db_name)
                search_dict['search_head']     = '%s - TAG -  %s  -  %s  -  %s' % (str(id_num), obj.enqueue_date, obj.program, orgs)
                search_dict['id_str']          = 'collapsible' + str(id_num)
                search_dict['soft_masking']    = obj.soft_masking
                search_dict['enqueue_date']    = obj.enqueue_date
                search_dict['low_complexity']  = obj.low_complexity
                search_dict['penalty']         = obj.penalty
                search_dict['evalue']          = obj.evalue
                search_dict['gapopen']         = obj.gapopen
                search_dict['strand']          = obj.strand
                search_dict['gapextend']       = obj.gapextend
                search_dict['word_size']       = obj.word_size
                search_dict['max_target_seqs'] = obj.max_target_seqs
                search_dict['sequence']        = obj.sequence
                search_list.append(search_dict)
            return render(request, 'dashboard/blast_hist.html', { 'search_list': search_list})
    elif request.method == 'POST':
        return render(request, 'dashboard/index.html', { 'year': datetime.now().year, 'title': 'Dashboard', })


