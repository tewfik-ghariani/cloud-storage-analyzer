from wsgiref.util import FileWrapper
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

import os
import json
import re
from lib import athenajdbcWrapper
from lib import botoWrapper
from lib import metadata


def base(request):
    return render(request, "base.html")


@login_required
def index(request):
    customers = metadata.get_clients()
    return render(request, "schemas/index.html", {"customers": customers})


@login_required
def second(request):
    athena = athenajdbcWrapper.PyAthenaLoader()
    res = dir(athena)
    res += athena.info()
    return render(request, "schemas/second.html", {"data": res})


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

        s3_location, region = metadata.s3_verif(customer)
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

            folders = aws.s3_prefixes(prefix)
            objects = aws.s3loader(prefix)

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

        elif fetched == "download":
            object = req["object"]
            res_download = aws.download_from_bucket(object)
            if not res_download["success"]:
                return HttpResponse(status=201)
            content = res_download["data"]
            content_type = content["content_type"]
            content_length = content["content_length"]
            content_disposition = content["content_disposition"]

            wrapper = FileWrapper(open(object))
            response = HttpResponse(wrapper, content_type=content_type)
            response["Content-Length"] = content_length
            response["Content-Disposition"] = content_disposition
            os.remove(object)
            return response

        elif fetched == "search":
            regex = req["regex"]
            customer = req["customer"]
            s3_location, region = metadata.s3_verif(customer)
            aws = botoWrapper.BotoLoader(s3_location, region)
            objects = aws.search(regex)
            return JsonResponse({"success": True, "data": {"objects": objects}})


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

            bucket, region = metadata.s3_verif(customer)

            found_config = metadata.get_config(customer, object)

            if not found_config["success"]:
                return JsonResponse(found_config)

            headers = found_config["data"]["headers"]
            return JsonResponse(
                {
                    "success": True,
                    "data": {
                        "headers": headers,
                        "object": object,
                        "customer": customer,
                        "bucket": bucket,
                    },
                }
            )


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
            if not object or not customer:
                return JsonResponse(
                    {"success": False, "error": "Hmm, something is missing.."}
                )

            # retrieve table name to query in athena
            found_config = metadata.get_config(customer, object)
            all_headers = found_config["data"]["headers"]
            table = found_config["data"]["table"]

            # retrieve bucket config to connect with boto
            bucket, region = metadata.s3_verif(customer)
            # connect with boto
            aws = botoWrapper.BotoLoader(bucket, region)

            # copy the file to the external bucket
            copy_status = aws.to_athena(customer, table, object)
            if not copy_status["success"]:
                return JsonResponse(copy_status)

            # prepare to query with athena
            athena = athenajdbcWrapper.PyAthenaLoader()

            # ------------------------------------------------ Custom Query -----------------------------
            if custom:
                if re.match(r"^SELECT.*", headers):
                    head, sep, tail = headers.partition("SELECT")
                    headers = tail

                selected_items = headers
                if selected_items == "*":
                    headers = all_headers
                else:
                    headers = [headers]
                conditions_if_exist = conditions
                # to escape %
                if re.search(r"\%", conditions_if_exist):
                    conditions_if_exist = conditions_if_exist.replace("%", "%%")

            # ------------------------------------------------ Normal Query -------------------------
            else:
                # -------------- Handle columns --------------------------
                selected_items = ",".join(headers)
                if not selected_items:
                    selected_items = "*"
                    f = lambda x: x["attr"]
                    headers = [f(head) for head in all_headers]

                # -------------- Handle Conditions --------------------------
                if conditions:
                    conditions_if_exist = "WHERE"
                    conditions[0]["logical"] = ""
                    for cond in conditions:
                        if cond["selected_column"]["html_type"] == "text":
                            # to escape %
                            if re.search(r"\%", cond["input"]):
                                cond["input"] = cond["input"].replace("%", "%%")
                            cond["input"] = "'{0}'".format(cond["input"])
                        conditions_if_exist += " {0} {1} {2} {3} ".format(
                            cond["logical"],
                            cond["selected_column"]["attr"],
                            cond["operator"],
                            cond["input"],
                        )
                else:
                    conditions_if_exist = ""

            # -------- ------ Construct the query
            query = "SELECT {0} from {1}.{2} {3} ;".format(
                selected_items, customer, table, conditions_if_exist
            )

            res_query = athena.query(query)
            if not res_query["success"]:
                return JsonResponse(res_query)
            content = res_query["data"]

            # if not conditions_if_exist:
            #    content = content[1:]  # to delete the header line (problem for extra columns)

            # delete the file from the external bucket
            is_deleted = aws.delete_from_athena(customer, table, object, auto=True)
            if is_deleted["success"]:
                msg = ""
            else:
                msg = is_deleted["error"]

            return JsonResponse(
                {
                    "success": True,
                    "data": {"content": content, "headers": headers, "msg": msg},
                }
            )

            ### -------------------------CONFIG-----------------------

            # retrieve config toDo : create another function
            # columns
            if "submit" in request.POST:
                columns = request.POST.getlist("columns", "")
                extra_op = request.POST.get("extra_op", "")
                extra_col = request.POST.get("extra_col", "")

                xtra = request.POST.get("xtra", "")
                if xtra == "xtra":
                    selected_items = "{0}({1})".format(extra_op, extra_col)
                    selected_header = [selected_items]

                elif xtra == "ord_cols":
                    if columns:
                        selected_items = ""
                        for col in columns:
                            column_to_add = "{0}, ".format(col)
                            selected_items += column_to_add
                        selected_items = selected_items[:-2]  # to delete the last ','
                        selected_header = selected_items.split(",")
                    else:
                        selected_items = "*"
                        selected_header = headers

                        condition_to_add = "{0} {1} {2} and ".format(
                            champ.attr, operator, choice
                        )
                        conditions_if_exist += condition_to_add

                conditions_if_exist = conditions_if_exist[
                    :-5
                ]  # to delete the last 'and'

                custom_query = "SELECT {0} from {1} {2} ;".format(
                    selected_items, table, conditions_if_exist
                )

        return render(
            request,
            "schemas/partials/details.html",
            {
                "success": True,
                "data": data,
                "query": custom_query,
                "selected_header": selected_header,
            },
        )


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
            found_config = metadata.get_config(customer, object)
            fieldsFDV = found_config["data"]["fieldsFDV"]
            table = found_config["data"]["table"]

            # retrieve bucket config to connect with boto
            bucket, region = metadata.s3_verif(customer)
            # connect with boto wrapper
            aws = botoWrapper.BotoLoader(bucket, region)

            # copy the file to the external bucket
            copy_status = aws.to_athena(customer, table, object)
            if not copy_status["success"]:
                return JsonResponse(copy_status)

            athena = athenajdbcWrapper.PyAthenaLoader()  # prepare to query with athena

            # -------- ------ FDV detection
            res_query = athena.checkFDV(fieldsFDV, customer, table)
            if not res_query["success"]:
                return JsonResponse(res_query)

            content = res_query["data"]

            # delete the file from the external bucket
            is_deleted = aws.delete_from_athena(customer, table, object, auto=True)
            if is_deleted["success"]:
                msg = ""
            else:
                msg = is_deleted["error"]

            return JsonResponse(
                {"success": True, "data": {"content": content, "msg": msg}}
            )
