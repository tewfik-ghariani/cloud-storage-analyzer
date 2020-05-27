from wsgiref.util import FileWrapper
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
import os
import json

from lib import athenajdbcWrapper
from lib import botoWrapper
from lib import metadataWrapper


@staff_member_required
def wizard(request):
    return render(request, "wizard/wizard.html")


@staff_member_required
def console(request):
    if request.method == "GET":
        return render(request, "wizard/console.html")
    elif request.method == "POST":
        req = json.loads(request.body.decode())
        fetched = req["fetch"]
        athena = athenajdbcWrapper.PyAthenaLoader()

        if fetched == "dbs":
            res_dbs = athena.databases()
            if not res_dbs["success"]:
                return JsonResponse(res_dbs)
            res_dbs = res_dbs["data"]
            databases = map(" ".join, res_dbs)
            databases = list(databases)
            return JsonResponse({"success": True, "data": databases})

        if fetched == "tables":
            database = req["database"]
            res_tables = athena.tables(database)
            if not res_tables["success"]:
                return JsonResponse(res_tables)
            res_tables = res_tables["data"]
            tables = map(" ".join, res_tables)
            tables = list(tables)
            if not tables:
                tables = "None"
            return JsonResponse({"success": True, "db": database, "data": tables})

        if fetched == "delete_table":
            table = req["table"]
            parent_db = req["parent_db"]
            is_deleted = athena.query("DROP TABLE {0}.{1};".format(parent_db, table))
            if not is_deleted["success"]:
                return JsonResponse(is_deleted)

            # Remove from local database automatically
            local_is_deleted = metadataWrapper.del_config(parent_db, table, auto=True)
            return JsonResponse(local_is_deleted)

        if fetched == "manip_db":
            manip = req["manip"]
            db = req["database"]
            if manip == "create_db":
                delete_or_create = True
            elif manip == "delete_db":
                delete_or_create = False

            res_manip = athena.db_manip(db, delete_or_create)
            return JsonResponse(res_manip)

        if fetched == "create_table":
            columns = req["columns"]
            delim = req["delim"]
            try:
                database = req["database"]
                if not database:
                    raise KeyError
            except KeyError:
                return JsonResponse({"success": False, "error": "Select a Database!"})

            table = req["table"]
            athena = athenajdbcWrapper.PyAthenaLoader()
            # create in athena catalog
            created = athena.create(columns, delim, database, table)
            if not created["success"]:
                return JsonResponse(created)

            # Add to local database automatically
            added = metadataWrapper.addConfig(database, table, columns, auto=True)
            return JsonResponse(added)

        if fetched == "desc_table":
            database = req["database"]
            table = req["table"]
            athena = athenajdbcWrapper.PyAthenaLoader()
            tableDesc = athena.desc(database, table)
            return JsonResponse(tableDesc)

        else:
            return JsonResponse({"success": False, "error": "Are you lost?"})


@staff_member_required
def external(request):
    if request.method == "GET":
        return render(request, "wizard/external.html")
    elif request.method == "POST":

        # Handle Purge Request
        if request.POST.get("purge"):
            botoWrapper.BotoLoader.folders = []
            call_command("purge")
            messages.success(request, "Bucket Purged Successfully! ")
            return redirect(reverse("external"))

        req = json.loads(request.body.decode())
        fetched = req["fetch"]

        customer = "external"
        s3_location, region = metadataWrapper.s3_verif(customer)
        aws = botoWrapper.BotoLoader(s3_location, region)

        # Handle Delete request
        if fetched == "delete":
            file = req["file"]
            is_deleted = aws.delete_from_athena(customer, table=None, key=file)
            if is_deleted["success"]:
                return JsonResponse({"success": True})
            else:
                return JsonResponse(is_deleted)

        # Handle getSize request
        if fetched == "size":
            object = req["object"]
            size = aws.getSize(object, external=True)
            return JsonResponse(size)

        # Handle Download request
        if fetched == "download":
            file = req["file"]
            res_download = aws.download_from_bucket(file)
            if not res_download["success"]:
                return HttpResponse(status=202)
            try:
                content = res_download["data"]
                filename = content["filename"]

                wrapper = FileWrapper(open(filename))
                response = HttpResponse(wrapper, content_type=content["content_type"])
                response["Content-Length"] = content["content_length"]
                response["Content-Disposition"] = content["content_disposition"]
                os.remove(filename)
            except Exception as X:
                print(X.args[0])
                return HttpResponse(status=201)
            return response

        # Handle getObjects request
        if fetched == "objects":
            prefix = req["prefix"]
            back = req["back"]
            front = True

            if not prefix:
                prefix = ""

            if back:
                prefix = prefix.strip().split("/")
                prefix = prefix[:-2]
                prefix.append("")
                prefix = "/".join(prefix)

            if prefix == "":
                front = False

            folders_rep = aws.s3_prefixes(prefix)
            if not folders_rep["success"]:
                return JsonResponse(folders_rep)
            folders = folders_rep["data"]

            objects_rep = aws.s3loader(prefix)
            if not objects_rep["success"]:
                return JsonResponse(objects_rep)
            objects = objects_rep["data"]

            return JsonResponse(
                {
                    "success": True,
                    "data": {
                        "customer": customer,
                        "objects": objects,
                        "folders": folders,
                        "prefix": prefix,
                        "front": front,
                    },
                }
            )

        else:
            return JsonResponse({"success": False, "error": "Are you lost?"})


@login_required
def metadata(request):
    if request.method == "GET":
        return render(request, "wizard/metadata.html")
    elif request.method == "POST":
        req = json.loads(request.body.decode())
        fetched = req["fetch"]

        if fetched == "customers":
            customers = metadataWrapper.get_clients()
            return JsonResponse({"success": True, "data": {"customers": customers}})

        if fetched == "addConfig":
            try:
                customer = req["customer"]
                if not customer:
                    raise KeyError
            except KeyError:
                return JsonResponse({"success": False, "error": "Select a customer!"})
            name = req["name"]
            rows = req["rows"]
            added = metadataWrapper.addConfig(customer, name, rows)
            return JsonResponse(added)

        if fetched == "get_local_config":
            try:
                customer = req["customer"]
                if not customer:
                    raise KeyError
            except KeyError:
                return JsonResponse({"success": False, "error": "Choose a customer"})

            configuration = metadataWrapper.get_all_config(customer)
            return JsonResponse(configuration)

        if fetched == "fetchFDV":
            try:
                customer = req["customer"]
                object = req["object"]
                if not customer or not object:
                    raise KeyError
            except KeyError:
                return JsonResponse({"success": False, "error": "Try again"})

            found_config = metadataWrapper.fetch_fieldsFDV(customer, object)
            return JsonResponse(found_config)

        if fetched == "updateFDV":
            try:
                customer = req["customer"]
                object = req["object"]
                fieldsFDV = req["fieldsFDV"]
                if not customer or not object:
                    raise KeyError
            except KeyError:
                return JsonResponse({"success": False, "error": "Try again"})

            update_fieldsFDV = metadataWrapper.updateFDV(customer, object, fieldsFDV)
            return JsonResponse(update_fieldsFDV)

        if fetched == "deleteConfig":
            try:
                customer = req["customer"]
                object = req["object"]
                if not customer or not object:
                    raise KeyError
            except KeyError:
                return JsonResponse({"success": False, "error": "Try again"})

            deleteConfiguration = metadataWrapper.del_config(customer, object)
            return JsonResponse(deleteConfiguration)

        else:
            return JsonResponse({"success": False, "error": "Are you lost?"})
