from wsgiref.util import FileWrapper
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
import os
import json

from lib import athenajdbcWrapper
from lib import botoWrapper
from lib import metadata


@staff_member_required
def base(request):
    return render(request, 'wizard/base.html')


@staff_member_required
def console(request):
    if request.method == 'GET':
        return render(request, 'wizard/console.html')
    elif request.method == 'POST':
        req = json.loads(request.body.decode())
        fetched = req['fetch']
        athena = athenajdbcWrapper.PyAthenaLoader()

        if fetched == 'dbs':
            res_dbs = athena.databases()
            if not res_dbs['success']:
                return JsonResponse(res_dbs)
            res_dbs = res_dbs['data']
            databases = map(' '.join, res_dbs)
            databases = list(databases)
            return JsonResponse({'success': True,
                                 'data': databases})

        if fetched == 'tables':
            database = req['database']
            res_tables = athena.tables(database)
            if not res_tables['success']:
                return JsonResponse(res_tables)
            res_tables = res_tables['data']
            tables = map(' '.join, res_tables)
            tables = list(tables)
            if not tables:
                tables = 'None'
            return JsonResponse({'success': True,
                                 'db': database,
                                 'data': tables})

        if fetched == 'delete_table':
            table = req['table']
            parent_db = req['parent_db']
            is_deleted = athena.query('DROP TABLE {0}.{1};'.format(parent_db, table))
            if is_deleted['success']:
                return JsonResponse({'success': True})
            else:
                return JsonResponse(is_deleted)

        if fetched == 'manip_db':
            manip = req['manip']
            db = req['database']
            if manip == 'create_db':
                delete_or_create = True
            elif manip == 'delete_db':
                delete_or_create = False

            res_manip = athena.db_manip(db, delete_or_create)
            if not res_manip['success']:
                return JsonResponse(res_manip)

            return JsonResponse({'success': True})

        if fetched == 'create_table':
            columns = req['columns']
            delim = req['delim']
            database = req['database']
            table = req['table']
            athena = athenajdbcWrapper.PyAthenaLoader()
            # create in athena catalog
            created = athena.create(columns, delim, database, table)
            if not created['success']:
                return JsonResponse(created)

            # Add to local database automatically
            added = metadata.addConfig(database, table, columns, auto=True)
            if not added['success']:
                return JsonResponse(added)

            return JsonResponse({'success': True})


@staff_member_required
def external(request):
    if request.method == 'GET':
        return render(request, 'wizard/external.html')
    elif request.method == 'POST':

        # Handle Purge Request
        if request.POST.get('purge'):
            call_command('purge')
            messages.success(request, 'Bucket Purged Successfully! ')
            return redirect(reverse('external'))

        req = json.loads(request.body.decode())
        fetched = req['fetch']

        customer = 'external'
        s3_location, region = metadata.s3_verif(customer)
        aws = botoWrapper.BotoLoader(s3_location, region)

        # Handle Delete request
        if fetched == 'delete':
            file = req['file']
            is_deleted = aws.delete_from_athena(customer, table=None, key=file)
            if is_deleted['success']:
                return JsonResponse({'success': True})
            else:
                return JsonResponse(is_deleted)

        # Handle Download request
        if fetched == 'download':
            file = req['file']
            res_download = aws.download_from_bucket(file)
            if not res_download['success']:
                return HttpResponse(status=201)
            content = res_download['data']
            content_type = content['content_type']
            content_length = content['content_length']
            content_disposition = content['content_disposition']

            wrapper = FileWrapper(open(file))
            response = HttpResponse(wrapper, content_type=content_type)
            response['Content-Length'] = content_length
            response['Content-Disposition'] = content_disposition
            os.remove(file)
            return response

        # Handle getObjects request
        if fetched == 'objects':
            prefix = req['prefix']
            back = req['back']
            front = True

            if not prefix:
                prefix = ''

            if back:
                prefix = prefix.strip().split('/')
                prefix = prefix[:-2]
                prefix.append('')
                prefix = '/'.join(prefix)

            if prefix == '':
                front = False

            folders = aws.s3_prefixes(prefix)
            objects = aws.s3loader(prefix)

            return JsonResponse({'success': True,
                                 'data': {'customer': customer,
                                          'objects': objects,
                                          'folders': folders,
                                          'prefix': prefix,
                                          'front': front}
                                 })


@staff_member_required
def database(request):
    if request.method == 'GET':
        return render(request, 'wizard/database.html')
    elif request.method == 'POST':
        req = json.loads(request.body.decode())
        fetched = req['fetch']

        if fetched == 'customers':
            customers = metadata.get_clients(True)
            return JsonResponse({'success': True,
                                 'data': {'customers': customers}})

        if fetched == 'addConfig':
            customer = req['customer']
            name = req['name']
            rows = req['rows']
            added = metadata.addConfig(customer, name, rows)
            if not added['success']:
                return JsonResponse(added)
            return JsonResponse({'success': True})

        if fetched == 'getConfig':
            try:
                customer = req['customer']
            except:
                return JsonResponse({'success': False, 'error': "Choose a customer"})

            configuration = metadata.getAllConfig(customer)
            if not configuration['success']:
                return JsonResponse(configuration)

            content = configuration['data']
            rowData = []
            for row in content:
                new_line = {}
                new_line['group'] = row['name']
                new_line['participants'] = row['headers']
                rowData.append(new_line)

            return JsonResponse({'success': True, 'rowdata': rowData})
