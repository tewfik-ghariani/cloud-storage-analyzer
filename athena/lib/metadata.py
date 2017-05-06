from django.shortcuts import get_object_or_404
from wizard.models import s3Info
from wizard.models import configObject
import re


def findName(names, key):
    i = 0
    regex = r".*" + re.escape(names[i]) + r".*"
    while not re.search(regex, key, re.IGNORECASE):
        i += 1
        regex = r".*" + re.escape(names[i]) + r".*"
    return names[i]


def get_config(customer, key):
    try:
        customer = s3Info.objects.get(shortcut=customer)
        names = configObject.objects.filter(customer=customer).values()
        f = lambda x: x['name']
        names = [f(name) for name in names]
        name = findName(names, key)
        config = configObject.objects.get(customer=customer, name=name)
    except Exception as X:
        print(X.args[0])
        return {'success': False, 'error': 'Configuration not set yet! Contact the admin!'}

    table = config.name
    headers = config.headers
    fieldsFDV = config.fieldsFDV
    return {'success': True, 'data': {'headers': headers,
                                      'table': table,
                                      'fieldsFDV': fieldsFDV}}


def s3_verif(customer):
    infos = get_object_or_404(s3Info, shortcut=customer)
    return infos.bucket_name, infos.bucket_region


def get_clients(all=False):
    res = []
    if all:
        objects = s3Info.objects.all()
    else:
        objects = s3Info.objects.filter(type='public').order_by('label')

    for customer in objects:
        info = {'label': customer.label,
                'shortcut': customer.shortcut}
        res.append(info)

    return res


def addConfig(customer, name, rows, auto=False):
    try:
        for col in rows:
            if col['type'] in ['tinyint',
                               'smallint',
                               'int',
                               'bigint',
                               'float',
                               'double',
                               'timestamp']:
                col['html_type'] = 'number'
            else:
                col['html_type'] = 'text'

        if auto:
            customer = s3Info.objects.get(shortcut=customer)
        else:
            customer = s3Info.objects.get(label=customer['label'], shortcut=customer['shortcut'])

        configObject.objects.create(name=name, customer=customer, headers=rows)
    except Exception as X:
        return {'success': False, 'error': X.args[0]}

    return {'success': True}


def getAllConfig(customer):
    try:
        customer = s3Info.objects.get(label=customer['label'], shortcut=customer['shortcut'])
        objects = configObject.objects.filter(customer=customer).values()
    except Exception as X:
        return {'success': False, 'error': X.args[0]}

    if not objects:
        return {'success': False, 'error': 'Nothing is configured yet'}

    obj = []
    for val in objects:
        obj.append(val)
    objects = obj
    return {'success': True, 'data': objects}
