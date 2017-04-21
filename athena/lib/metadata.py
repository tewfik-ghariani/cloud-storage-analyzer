from django.shortcuts import get_object_or_404
from schemas.models import testSchema
from schemas.models_dir import thd
from wizard.models import s3Info
import re


def get_config(customer, key):
    headers = None
    table = None
    if re.match(r'^thd', customer):
        if re.match(r'.*sales.*', key):
            headers = thd.thdSales.objects.all()
            table = 'thd.sales'
        if re.match(r'.*receipts.*', key):
            headers = thd.thdReceipts.objects.all()
            table = 'thd.receipts'
        if re.match(r'.*AUTH$', key):
            headers = thd.thdAUTH.objects.all()
            table = 'thd.AUTH'
        if re.match(r'.*CATM$', key):
            headers = thd.thdCATM.objects.all()
            table = 'thd.CATM'
        if re.match(r'.*CATR$', key):
            headers = thd.thdCATR.objects.all()
            table = 'thd.CATR'
        if re.match(r'.*CLST$', key):
            headers = thd.thdCLST.objects.all()
            table = 'thd.CLST'
        if re.match(r'.*LOCH$', key):
            headers = thd.thdLOCH.objects.all()
            table = 'thd.LOCH'
        if re.match(r'.*PGAD$', key):
            headers = thd.thdPGAD.objects.all()
            table = 'thd.PGAD'
        if re.match(r'.*PGHD$', key):
            headers = thd.thdPGHD.objects.all()
            table = 'thd.PGHD'
        if re.match(r'.*PGSR$', key):
            headers = thd.thdPGSR.objects.all()
            table = 'thd.PGSR'
        if re.match(r'.*PRDH$', key):
            headers = thd.thdPRDH.objects.all()
            table = 'thd.PRDH'
        if re.match(r'.*PSPC$', key):
            headers = thd.thdPSPC.objects.all()
            table = 'thd.PSPC'
        if re.match(r'.*PSSD$', key):
            headers = thd.thdPSSD.objects.all()
            table = 'thd.PSSD'
        if re.match(r'.*SKUA$', key):
            headers = thd.thdSKUA.objects.all()
            table = 'thd.SKUA'
        if re.match(r'.*SKUM$', key):
            headers = thd.thdSKUM.objects.all()
            table = 'thd.SKUM'
        if re.match(r'.*STRM$', key):
            headers = thd.thdSTRM.objects.all()
            table = 'thd.STRM'
        if re.match(r'.*STRT$', key):
            headers = thd.thdSTRT.objects.all()
            table = 'thd.STRT'
        if re.match(r'.*UDSG$', key):
            headers = thd.thdUDSG.objects.all()
            table = 'thd.UDSG'
        if re.match(r'.*UDSV$', key):
            headers = thd.thdUDSV.objects.all()
            table = 'thd.UDSV'

    if re.match(r'^athena$', customer):
        if re.match(r'.*sales.*', key):
            headers = testSchema.objects.all().values()
            table = 'shadow.sales'

    if headers:
        #convert queryset object to a list
        obj = []
        for val in headers:
            obj.append(val)
        headers = obj


    return headers, table


def s3_verif(customer):
    infos = get_object_or_404(s3Info, shortcut=customer)
    return infos.bucket_name, infos.bucket_region


def get_clients():
    res = []
    for customer in s3Info.objects.filter(type='public').order_by('label'):
        info = {'label': customer.label,
                'shortcut': customer.shortcut}
        res.append(info)

    return res
