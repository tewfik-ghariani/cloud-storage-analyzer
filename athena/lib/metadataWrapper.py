from django.shortcuts import get_object_or_404
from wizard.models import s3Info
from wizard.models import configObject
import re

f = lambda x: x["attr"]


def findName(names, key):
    i = 0
    regex = r".*" + re.escape(names[i]) + r".*"
    while not re.search(regex, key, re.IGNORECASE):
        i += 1
        regex = r".*" + re.escape(names[i]) + r".*"
    return names[i]


def get_config(customer, key, attr=False):
    try:
        customer = s3Info.objects.get(shortcut=customer)
        names = configObject.objects.filter(customer=customer).values()
        fname = lambda x: x["name"]
        names = [fname(name) for name in names]
        name = findName(names, key)
        config = configObject.objects.get(customer=customer, name=name)
    except Exception as X:
        print(X.args[0])
        return {
            "success": False,
            "error": "Configuration not set yet! Contact the admin!",
        }

    table = config.name
    headers = config.headers
    fieldsFDV = config.fieldsFDV
    if attr:
        headers = [f(head) for head in headers]

    return {
        "success": True,
        "data": {"headers": headers, "table": table, "fieldsFDV": fieldsFDV},
    }


def fetch_fieldsFDV(customer, object):
    try:
        object = object.strip()
        customer = s3Info.objects.get(
            label=customer["label"], shortcut=customer["shortcut"]
        )
        config = configObject.objects.get(customer=customer, name=object)
        headers = config.headers
        fieldsFDV = config.fieldsFDV
        headers = [f(head) for head in headers]
        if isinstance(fieldsFDV, dict):
            if not fieldsFDV:
                fieldsFDV = []
    except Exception as X:
        return {"success": False, "error": X.args[0]}

    return {"success": True, "data": {"headers": headers, "fieldsFDV": fieldsFDV}}


def updateFDV(customer, object, fieldsFDV):
    try:
        for field in fieldsFDV:
            if not field["value"]:
                return {"success": False, "error": "Empty value is not accepted"}

            for key in field["keys"]:
                if not key["name"]:
                    return {"success": False, "error": "Empty key is not accepted"}

                if key["name"] == field["value"]:
                    return {
                        "success": False,
                        "error": "An attribute must not be key and value in the same predicate",
                    }

                for index, key in enumerate(field["keys"]):
                    if key in field["keys"][index + 1 :]:
                        return {
                            "success": False,
                            "error": "Duplicate keys for the same predicate are not accepted",
                        }

        object = object.strip()
        customer = s3Info.objects.get(
            label=customer["label"], shortcut=customer["shortcut"]
        )
        config = configObject.objects.get(customer=customer, name=object)
        config.fieldsFDV = fieldsFDV
        config.save()
    except Exception as X:
        return {"success": False, "error": X.args[0]}

    msg = "FDV fields for '{0}' for the customer '{1}' have been updated!".format(
        object, customer
    )
    return {"success": True, "data": {"msg": msg}}


def s3_verif(customer):
    infos = get_object_or_404(s3Info, shortcut=customer)
    return infos.bucket_name, infos.bucket_region


def get_clients(all=False):
    res = []
    if all:
        objects = s3Info.objects.all()
    else:
        objects = s3Info.objects.filter(type="public").order_by("label")

    for customer in objects:
        info = {"label": customer.label, "shortcut": customer.shortcut}
        res.append(info)

    return res


def addConfig(customer, name, rows, auto=False):
    try:
        for col in rows:
            if col["type"] in [
                "tinyint",
                "smallint",
                "int",
                "bigint",
                "float",
                "double",
                "timestamp",
            ]:
                col["html_type"] = "number"
            else:
                col["html_type"] = "text"
                if not col["type"]:
                    col["type"] = "string"

        if auto:
            customer = s3Info.objects.get(shortcut=customer)
        else:
            customer = s3Info.objects.get(
                label=customer["label"], shortcut=customer["shortcut"]
            )

        if customer.type == "private":
            return {
                "success": False,
                "error": " Adding configuration to a private bucket is not possible!",
            }
        # configObject.objects.get(customer=customer, name=name)
        configObject.objects.create(
            name=name, customer=customer, headers=rows, fieldsFDV={}
        )

    except Exception as X:
        if auto:
            return {
                "success": True,
                "msg": " but could not add it to the local database!",
            }
        return {"success": False, "error": X.args[0]}

    if auto:
        msg = " and added to the local Database as well!"
    else:
        msg = " '{0}' configuration for '{1}' was added!".format(name, customer)
    return {"success": True, "msg": msg}


def get_all_config(customer):
    try:
        customer = s3Info.objects.get(
            label=customer["label"], shortcut=customer["shortcut"]
        )
        objects = configObject.objects.filter(customer=customer).values()
    except Exception as X:
        return {"success": False, "error": X.args[0]}

    if not objects:
        return {"success": False, "error": "Nothing is configured yet"}

    rowData = []
    for row in objects:
        new_line = {}
        new_line["group"] = row["name"]
        new_line["participants"] = row["headers"]
        rowData.append(new_line)

    return {"success": True, "rowData": rowData}


def del_config(parent_db, table, auto=False):
    try:
        if not auto:
            parent_db = parent_db["shortcut"]

        table = table.strip()
        customer = s3Info.objects.get(shortcut=parent_db)
        object = configObject.objects.get(customer=customer, name=table)
        object.delete()
    except Exception as X:
        print(X.args[0])
        if auto:
            return {
                "success": True,
                "msg": " but this does not exist in the local database",
            }
        else:
            return {"success": False, "error": X.args[0]}

    if auto:
        msg = " and this was deleted from the local database as well"
    else:
        msg = " Object '{0}' for the customer '{1}' has been deleted ".format(
            table, parent_db
        )

    return {"success": True, "msg": msg}
