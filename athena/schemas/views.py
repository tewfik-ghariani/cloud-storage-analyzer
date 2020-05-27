from wsgiref.util import FileWrapper
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.core.cache import cache

import os
import json
import re
import time
from lib import athenajdbcWrapper
from lib import botoWrapper
from lib import metadataWrapper


def home(request):
    return render(request, "schemas/home.html")


@login_required
def index(request):
    customers = metadataWrapper.get_clients()
    return render(request, "schemas/index.html", {"customers": customers})


@login_required
def list(request):
    if request.method == "GET":
        return render(request, "schemas/partials/list.html")
    elif request.method == "POST":
        req = json.loads(request.body.decode())
        fetched = req["fetch"]

        try:
            customer = req["customer"]
        except KeyError:
            return JsonResponse({"success": False, "error": "Please choose a customer"})

        s3_location, region = metadataWrapper.s3_verif(customer)
        aws = botoWrapper.BotoLoader(s3_location, region)

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
                        "objects": objects,
                        "folders": folders,
                        "prefix": prefix,
                        "front": front,
                    },
                }
            )

        if fetched == "download":
            object = req["object"]
            res_download = aws.download_from_bucket(object)
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
                print(X)
                return HttpResponse(status=201)
            return response

        if fetched == "search":
            regex = req["regex"]
            customer = req["customer"]
            s3_location, region = metadataWrapper.s3_verif(customer)
            aws = botoWrapper.BotoLoader(s3_location, region)
            objects = aws.search(regex)
            return JsonResponse(objects)

        if fetched == "size":
            object = req["object"]
            size = aws.getSize(object)
            return JsonResponse(size)

        else:
            return JsonResponse({"success": False, "error": "Are you lost?"})


@login_required
def config(request):
    if request.method == "GET":
        return render(request, "schemas/partials/config.html")
    elif request.method == "POST":
        req = json.loads(request.body.decode())
        fetched = req["fetch"]

        if fetched == "configuration":
            customer = req["customer"]
            object = req["object"]
            if not object or not customer:
                return JsonResponse(
                    {"success": False, "error": "Please select an object to query"}
                )

            bucket, region = metadataWrapper.s3_verif(customer)

            found_config = metadataWrapper.get_config(customer, object)

            if not found_config["success"]:
                return JsonResponse(found_config)

            headers = found_config["data"]["headers"]

            nbr_headers = []
            for champ in headers:
                if champ["html_type"] == "number":
                    nbr_headers.append(champ)

            return JsonResponse(
                {
                    "success": True,
                    "data": {
                        "headers": headers,
                        "object": object,
                        "nbr_headers": nbr_headers,
                        "customer": customer,
                        "bucket": bucket,
                    },
                }
            )
        else:
            return JsonResponse({"success": False, "error": "Are you lost?"})


@login_required
def details(request):
    if request.method == "GET":
        return render(request, "schemas/partials/details.html")

    if request.method == "POST":
        req = json.loads(request.body.decode())
        fetched = req["fetch"]

        if fetched == "details":
            customer = req["customer"]
            object = req["object"]
            headers = req["headers"]
            conditions = req["conditions"]
            custom = req["custom"]
            xtra = req["xtra"]
            if not object or not customer:
                return JsonResponse(
                    {"success": False, "error": "Hmm, something is missing.."}
                )

            # retrieve table name to query in athena
            found_config = metadataWrapper.get_config(customer, object, attr=True)
            if not found_config["success"]:
                return JsonResponse(found_config)

            all_headers = found_config["data"]["headers"]
            table = found_config["data"]["table"]

            # retrieve bucket config to connect with boto
            bucket, region = metadataWrapper.s3_verif(customer)
            # connect with boto
            aws = botoWrapper.BotoLoader(bucket, region)

            # prepare to query with athena
            athena = athenajdbcWrapper.PyAthenaLoader()

            # Construct the query (either custom or normal or xtra)
            try:
                # ------------------------------------------------ Custom Query -----------------
                if custom:
                    if re.match(r"^SELECT.*", headers):
                        head, sep, tail = headers.partition("SELECT")
                        headers = tail

                    selected_columns = headers
                    if selected_columns == "*":
                        headers = all_headers
                    else:
                        headers = [selected_columns]
                    conditions_if_exist = conditions
                    # to escape %
                    if re.search(r"\%", conditions_if_exist):
                        conditions_if_exist = conditions_if_exist.replace("%", "%%")

                # ------------------------------------------------ Normal Query --------------------
                else:
                    # ---------------------------------- Handle Xtra columns ---------------
                    if xtra:
                        xtraHeaders = req["xtraHeaders"]
                        if not xtraHeaders:
                            raise ValueError
                        selected_columns = ""
                        for xHead in xtraHeaders:
                            if not xHead["op"]:
                                return JsonResponse(
                                    {"success": False, "error": "Specify an operator"}
                                )

                            selected_columns += " {0}({1}) , ".format(
                                xHead["op"], xHead["col"]["attr"]
                            )
                        selected_columns = selected_columns[:-3]
                        headers = selected_columns.split(",")

                    # -------------- Handle ordinary columns --------------------------
                    else:
                        selected_columns = ",".join(headers)
                        if not selected_columns:
                            selected_columns = "*"
                            headers = all_headers

                    # -------------- Handle Conditions --------------------------

                    if conditions:
                        conditions_if_exist = "WHERE"
                        conditions[0]["logical"] = ""
                        for cond in conditions:
                            if not cond["operator"]:
                                raise ValueError
                            if cond["selected_column"]["html_type"] == "text":
                                # to escape %
                                if re.search(r"\%", cond["input"]):
                                    cond["input"] = cond["input"].replace("%", "%%")
                                # to properly format the strings
                                cond["input"] = "'{0}'".format(cond["input"])
                            conditions_if_exist += " {0} {1} {2} {3} ".format(
                                cond["logical"],
                                cond["selected_column"]["attr"],
                                cond["operator"],
                                cond["input"],
                            )
                    else:
                        conditions_if_exist = ""

            except Exception as X:
                print(X)
                return JsonResponse(
                    {"success": False, "error": "Verify your conditions"}
                )

                # -------- ------ Query statement
            query = "SELECT {0} from {1}.{2} {3} ;".format(
                selected_columns, customer, table, conditions_if_exist
            )

            # copy the file to the external bucket
            copy_status = aws.copy_to_athena(customer, table, object)
            if not copy_status["success"]:
                return JsonResponse(copy_status)

            # Send the query and fetch details
            res_query = athena.details(query, headers)

            # delete the file from the external bucket either way
            is_deleted = aws.delete_from_athena(customer, table, object, auto=True)
            if is_deleted["success"]:
                msg = ""
            else:
                msg = is_deleted["error"]

            if not res_query["success"]:
                return JsonResponse(res_query)

            content = res_query["data"]  # toDo send chunks of data
            # toDo find a solution for the header line

            columnDefs = content["columnDefs"]
            query_id = content["query_id"]

            return JsonResponse(
                {
                    "success": True,
                    "data": {
                        "columnDefs": columnDefs,
                        "msg": msg,
                        "query_id": query_id,
                    },
                }
            )

        if fetched == "more":
            query_id = req["query_id"]
            startRow = req["startRow"]
            endRow = req["endRow"]
            time.sleep(1)
            rowData = cache.get(query_id + str(endRow))
            lastRow = -1
            time.sleep(1)
            if cache.get(query_id + "done"):
                lastRow = len(rowData)

            return JsonResponse(
                {"success": True, "data": {"rowData": rowData, "lastRow": lastRow}}
            )

        if fetched == "export":
            query_id = req["query_id"]
            customer = "external"
            s3_location, region = metadataWrapper.s3_verif(customer)
            aws = botoWrapper.BotoLoader(s3_location, region)

            res_download = aws.download_from_bucket(query_id + ".csv")
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

        else:
            return JsonResponse({"success": False, "error": "Are you lost?"})


@login_required
def FDV(request):
    if request.method == "GET":
        return render(request, "schemas/partials/FDV.html")

    if request.method == "POST":
        req = json.loads(request.body.decode())
        fetched = req["fetch"]

        if fetched == "FDVcheck":
            customer = req["customer"]
            object = req["object"]
            if not object or not customer:
                return JsonResponse(
                    {"success": False, "error": "Hmm, something is missing.."}
                )

            # retrieve table name to query in athena
            found_config = metadataWrapper.get_config(customer, object, attr=True)
            if not found_config["success"]:
                return JsonResponse(found_config)

            config = found_config["data"]
            headers = config["headers"]
            fieldsFDV = config["fieldsFDV"]
            if not fieldsFDV:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "FDV fields are not set yet! Contact the administrator!",
                    }
                )

            table = config["table"]

            # retrieve bucket config to connect with boto
            bucket, region = metadataWrapper.s3_verif(customer)
            # connect with boto wrapper
            aws = botoWrapper.BotoLoader(bucket, region)

            # copy the file to the external bucket
            copy_status = aws.copy_to_athena(customer, table, object)
            if not copy_status["success"]:
                return JsonResponse(copy_status)

            athena = athenajdbcWrapper.PyAthenaLoader()  # prepare to query with athena

            # -------------- FDV detection
            res_query = athena.checkFDV(fieldsFDV, customer, table)

            # delete the file from the external bucket either way
            is_deleted = aws.delete_from_athena(customer, table, object, auto=True)
            if is_deleted["success"]:
                msg = ""
            else:
                msg = is_deleted["error"]

            if not res_query["success"]:
                return JsonResponse(res_query)

            content = res_query["data"]
            fdv = res_query["fdv"]

            return JsonResponse(
                {
                    "success": True,
                    "data": {
                        "content": content,
                        "headers": headers,
                        "fdv": fdv,
                        "msg": msg,
                    },
                }
            )

        else:
            return JsonResponse({"success": False, "error": "Are you lost?"})
