from wsgiref.util import FileWrapper
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import render

import os
import json
import re
from lib import jdbc, boto, metadata


def base(request):
    return render(request, 'base.html')


@login_required
def index(request):
    customers = metadata.get_clients()
    return render(request, 'schemas/index.html', {'customers': customers})


@login_required
def second(request):
    athena = jdbc.PyAthenaLoader()
    res = dir(athena)
    res += athena.info()
    return render(request, 'schemas/second.html', {'data': res})


@login_required
def list(request):
    if request.method == 'GET':
        return render(request, 'schemas/partials/list.html')
    elif request.method == 'POST':
        req = json.loads(request.body.decode())
        fetched = req['fetch']

        customer = req['customer']
        s3_location, region = metadata.s3_verif(customer)
        aws = boto.BotoLoader(s3_location, region)

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

        elif fetched == 'download':
            object = req['object']
            content_type, content_length, content_disposition = aws.download_from_bucket(object)
            wrapper = FileWrapper(open(object))
            response = HttpResponse(wrapper, content_type=content_type)
            response['Content-Length'] = content_length
            response['Content-Disposition'] = content_disposition
            os.remove(object)
            return response


        elif fetched == 'search':
            regex = req['regex']
            customer = req['customer']
            s3_location, region = metadata.s3_verif(customer)
            aws = boto.BotoLoader(s3_location, region)
            objects = aws.search(regex)
            return JsonResponse({'success': True,
                                 'data': {'objects': objects}})

    '''paginator = Paginator(data, 20)

    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        # page not integer
        data = paginator.page(1)
    except EmptyPage:
        # Out of range
        data = paginator.page(paginator.num_pages)

    # in case of too many pages
    data.custom_range = range(max(data.number - 3, 1), min(data.number + 3, data.paginator.num_pages) + 1)
    '''


@login_required
def config(request):
    if request.method == 'GET':
        return render(request, 'schemas/partials/config.html')
    elif request.method == 'POST':
        req = json.loads(request.body.decode())
        fetched = req['fetch']

        if fetched == 'configuration':
            customer = req['customer']
            bucket, region = metadata.s3_verif(customer)
            object = req['object']
            headers, table = metadata.get_config(customer, object)
            if not table and not headers:
                return JsonResponse({'success': False})

            return JsonResponse({'success': True,
                                 'data': {'headers': headers,
                                          'object': object,
                                          'customer': customer,
                                          'bucket': bucket}})


@login_required
def details(request):
    if request.method == 'GET':
        return render(request, 'schemas/partials/details.html')

    if request.method == 'POST':
        req = json.loads(request.body.decode())
        fetched = req['fetch']

        if fetched == 'details':
            customer = req['customer']
            object = req['object']
            headers = req['headers']
            conditions = req['conditions']

            all_headers, table = metadata.get_config(customer, object)  # retrieve table name to query in athena
            bucket, region = metadata.s3_verif(customer)  # retrieve bucket config to connect with boto
            aws = boto.BotoLoader(bucket, region)  # connect with boto

            copy_status = aws.to_athena(customer, object)  # copy the file to the external bucket
            if not copy_status:
                return JsonResponse({'success': False,
                                     'error': 'Error in copy'})

            athena = jdbc.PyAthenaLoader()  # prepare to query with athena

            # -------------- Handle columns --------------------------
            selected_items = ','.join(headers)
            if not selected_items:
                selected_items = '*'
                f = lambda x: x['attribute']
                headers = [f(head) for head in all_headers]

            # -------------- Handle Conditions --------------------------
            if conditions:
                conditions_if_exist = "WHERE "
                for cond in conditions:
                    conditions_if_exist += "{0} {1} {2} and ".format(cond['selected_column']['attribute'],
                                                                     cond['operator'],
                                                                     cond['input'])
                conditions_if_exist = conditions_if_exist[:-5]  # to delete the last 'and'
            else:
                conditions_if_exist = ""

            # -------- ------ Construct the query
            custom_query = "SELECT {0} from {1} {2} ;".format(selected_items, table, conditions_if_exist)
            content = athena.query(custom_query)

            is_deleted = aws.delete_from_athena(customer, object)  # delete the file from tmp/

            return JsonResponse({'success': True,
                                 'data': {'content': content,
                                          'selected_items': headers}})

            ### --------------------- Custom Query-----------------------
            if 'custom_submit' in request.POST:
                selected_items = request.POST.get('select', '')
                conditions_if_exist = request.POST.get('conds', '')
                custom_query = "{0} from {1} {2} ".format(selected_items, table, conditions_if_exist)

                head, sep, tail = selected_items.partition('SELECT ')
                selected_items = tail
                if selected_items == '*':
                    selected_header = headers
                else:
                    selected_header = selected_items.split(',')


            ### -------------------------CONFIG-----------------------

            # retrieve config toDo : create another function in another module
            # columns
            elif 'submit' in request.POST:
                columns = request.POST.getlist('columns', '')
                extra_op = request.POST.get('extra_op', '')
                extra_col = request.POST.get('extra_col', '')

                xtra = request.POST.get('xtra', '')
                if xtra == 'xtra':
                    selected_items = "{0}({1})".format(extra_op, extra_col)
                    selected_header = [selected_items]

                elif xtra == 'ord_cols':
                    if columns:
                        selected_items = ""
                        for col in columns:
                            column_to_add = "{0}, ".format(col)
                            selected_items += column_to_add
                        selected_items = selected_items[:-2]  # to delete the last ','
                        selected_header = selected_items.split(',')
                    else:
                        selected_items = "*"
                        selected_header = headers

                        type = champ.html_type
                        if re.match(r'text', type):
                            choice = "\'{0}\'".format(choice)

                        condition_to_add = "{0} {1} {2} and ".format(champ.attribute, operator, choice)
                        conditions_if_exist += condition_to_add

                conditions_if_exist = conditions_if_exist[:-5]  # to delete the last 'and'

                custom_query = "SELECT {0} from {1} {2} ;".format(selected_items, table, conditions_if_exist)

            res = athena.query(custom_query)
            data = res

            is_deleted = aws.delete_from_athena(customer, object)  # delete the file from tmp/

        return render(request, 'schemas/partials/details.html', {'success': True,
                                                                 'data': data,
                                                                 'query': custom_query,
                                                                 'selected_header': selected_header})
