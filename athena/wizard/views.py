from wsgiref.util import FileWrapper
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command

import os
import json
import re

from lib import jdbc, boto, metadata



@staff_member_required
def base(request):
    return render(request, 'wizard/base.html')


@staff_member_required
def console(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode())
        fetched = req['fetch']
        athena = jdbc.PyAthenaLoader()

        if fetched == 'dbs':
            res = athena.databases()
            databases = map(' '.join, res)
            databases = list(databases)
            return JsonResponse({'success': True,
                                 'data': databases})

        if fetched == 'tables':
            database = req['database']
            res = athena.tables(database)
            tables = map(' '.join, res)
            tables = list(tables)
            if not tables:
                tables = 'None'
            return JsonResponse({'success': True,
                                 'db': database,
                                 'data': tables})

        if fetched == 'delete_table':
            table = req['table']
            parent_db = req['parent_db']
            athena.query('DROP TABLE {0}.{1};'.format(parent_db, table))
            return JsonResponse({'success': True})

        if fetched == 'manip_db':
            manip = req['manip']
            db = req['database']
            if manip == 'create_db':
                delete_or_create = True
            elif manip == 'delete_db':
                delete_or_create = False

            status = athena.db_manip(db, delete_or_create)
            if not status:
                raise Http404  # Error Handling
            return JsonResponse({'success': True})

    elif request.method == 'GET':
        return render(request, 'wizard/console.html')


@staff_member_required
def add_table(request):
    athena = jdbc.PyAthenaLoader()
    res = athena.databases()
    databases = map(' '.join, res)
    common_types = ['Select a type',
                    'string',
                    'tinyint',
                    'smallint',
                    'int',
                    'bigint',
                    'boolean',
                    'float',
                    'double',
                    'array',
                    'map',
                    'timestamp'
                    ]

    return render(request, 'wizard/add_table.html', {'common_types': common_types, 'databases': databases})


@staff_member_required
def create_query(request):
    if request.method == 'POST':
        cols = request.POST.getlist('col_label')
        types = request.POST.getlist('col_type')
        location = request.POST.get('location')
        delim = request.POST.get('delim')
        database = request.POST.get('database')
        table = request.POST.get('table')

        athena = jdbc.PyAthenaLoader()
        created = athena.create(database, table, cols, types, delim, location)
        if created:
            return redirect(reverse('console'))
        else:
            return HttpResponse("<h1> Watch your steps </h1>")
    else:
        raise Http404




@staff_member_required
def external(request):
    customer = 'external'
    s3_location, region = metadata.s3_verif(customer)
    aws = boto.BotoLoader(s3_location, region)
    not_front = True

    if request.method == 'GET':
        folders = aws.s3_prefixes('')
        data = aws.s3loader('')
        not_front = False
        prefix = None

    if request.method == 'POST':
        try:
            req = json.loads(request.body.decode())
            fetched = req['fetch']
            file = req['file']

            if fetched == 'delete':
                is_deleted = aws.delete_from_athena(customer, file, False) 
                if is_deleted:
                    return JsonResponse({'fetch':fetched,
                                         'success': True})
                else:
                    raise Http404


            if fetched == 'download':
                content_type, content_length, content_disposition = aws.download_from_bucket(file)
                wrapper = FileWrapper(open(file))
                response = HttpResponse(wrapper, content_type=content_type)
                response['Content-Length'] = content_length
                response['Content-Disposition'] = content_disposition
                os.remove(file)
                return response


        except Exception as Ex:
            print(Ex)
            pass


        if request.POST.get('purge'):
            call_command('purge')
            messages.success(request, 'Bucket Purged Successfully! ')
            return redirect(reverse('external'))


        if request.POST.get('prefix'):
            prefix = request.POST.get('prefix', '')
        if request.POST.get('back'):
            Parent = request.POST.get('Parent')
            if re.match(r'^.[^/]*/$', Parent):
                return redirect(reverse('external'))
            else:
                prefix = Parent.strip().split('/')
                prefix = prefix[:-2]
                prefix.append('')
                prefix = '/'.join(prefix)


        folders = aws.s3_prefixes(prefix)
        data = aws.s3loader(prefix)


    return  render(request, 'wizard/external.html', {'folders': folders,
                                                     'not_front': not_front,
                                                     'Parent': prefix,
                                                     'data': data})