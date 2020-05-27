import os
import pyathenajdbc
from django.core.cache import cache
import threading

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_path = BASE_DIR + "/lib/static/queries.log"


class cachingThread(threading.Thread):
    def __init__(self, threadID, name, cursor, headers):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.cursor = cursor
        self.headers = headers

    def run(self):
        print("----------------")
        print("Starting " + self.name)
        counter = 100
        cache.set(self.threadID + "done", False)
        while not self.cursor.is_closed:
            to_be_cached = self.format(self.cursor.fetchmany(100))
            if not to_be_cached["success"]:
                break
            cache.set(self.threadID + str(counter), to_be_cached["rows"])
            print(str(counter) + " for " + self.threadID + " cached! ")
            counter += 100

    def format(self, all_rows):
        if not all_rows:
            self.cursor.close()
            cache.set(self.threadID + "done", True)
            print("Terminating " + self.name)
            print("----------------")
            return {"success": False}
        rows = []
        for row in all_rows:
            new_line = {}
            i = 0
            for head in self.headers:
                new_line[head] = row[i]
                i += 1
            rows.append(new_line)
        return {"success": True, "rows": rows}


class PyAthenaLoader:
    def connecti(self):
        self.conn = pyathenajdbc.connect(
            s3_staging_dir="s3://athena-internship",
            region_name="us-east-1",
            log_path=log_path,
        )

    def databases(self):
        dbs = self.query("show databases;")
        return dbs

    def tables(self, database):
        tables = self.query("show tables in {0};".format(database))
        return tables

    def db_manip(self, database, bool):
        self.connecti()
        if bool:
            query = "CREATE DATABASE IF NOT EXISTS {0};"
        else:
            query = "DROP DATABASE {0};"

        query = query.format(database)
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
        except Exception as X:
            return {"success": False, "error": X.args[0]}
        finally:
            self.conn.close()
        return {"success": True, "msg": ""}

    def create(self, columns, delim, database, table):
        self.connecti()
        try:
            create_q = "CREATE EXTERNAL TABLE IF NOT EXISTS {0}.{1} (".format(
                database, table
            )

            for col in columns:
                if not col["type"]:
                    col["type"] = "string"
                create_q += " {0} {1}, ".format(col["attr"], col["type"])
            create_q = create_q[:-2]

            create_q += """)
                        ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
                        WITH SERDEPROPERTIES (
                            'serialization.format' = '{0}',
                            'field.delim' = '{0}',
                            'collection.delimm' = 'undefined',
                            'mapkey.delim' = 'undefined'
                        ) LOCATION '""".format(
                delim
            )

            slocation = "s3://athena-internship"
            create_q += "{0}/tmp/{1}/{2}/';".format(slocation, database, table)

            with self.conn.cursor() as cursor:
                cursor.execute(create_q)
        except Exception as X:
            return {"success": False, "error": X.args[0]}
        finally:
            self.conn.close()
        return {"success": True}

    def query(self, req):
        try:
            self.connecti()
            with self.conn.cursor() as cursor:
                cursor.execute(req)
                res = cursor.fetchall()
        except Exception as X:
            return {"success": False, "error": X.args[0]}
        finally:
            self.conn.close()
        return {"success": True, "data": res}

    def details(self, req, headers):
        self.connecti()
        try:
            cursor = self.conn.cursor()
            cursor.execute(req)
            query_id = cursor.query_id

            columnDefs = []
            for head in headers:
                columnDefs.append({"headerName": head, "field": head, "editable": True})

            test = cachingThread(query_id, query_id, cursor, headers)
            test.start()

        except Exception as X:
            return {"success": False, "error": X.args[0]}

        return {
            "success": True,
            "data": {"columnDefs": columnDefs, "query_id": query_id},
        }

    def checkFDV(self, fieldsFDV, customer, table):
        """
        Using locally stored FDV (keys/value), verify if the object contains Functional Dependency Violation,
        It is a query that scans the file twice such as this :
        SELECT a.* from customer.table as a, customer.table as b where a.keys = b.keys and a.value != b.value;
        or perform multiple queries with join statement for each predicate
        :param fieldsFDV: [{value: '', keys = [{'name': ''}]}]
        :param customer:
        :param table: Name of the file
        :return: Success or not && rows describing the FDVs
        """
        try:
            """ base = 'SELECT a.* from {0}.{1} as a, {0}.{1} as b where '.format(customer, table)
                for set in fieldsFDV:
                    primary_keys = set['keys']
                    unique = set['value']
                    case = ''
                    for key in primary_keys:
                        case += " a.{0} = b.{0} and ".format(key['name'])

                    case += " a.{0} != b.{0} ".format(unique)
                    base += case + " or "
                base = base[:-4]

                detectFDV = self.query(base)
                return detectFDV
            """
            fname = lambda x: x["name"]
            base = "SELECT a.* from {0}.{1}  a \n LEFT JOIN {0}.{1}  b \n ON ".format(
                customer, table
            )
            res = []
            fdv = {"found": False, "msg": ""}
            for set in fieldsFDV:
                primary_keys = set["keys"]
                primary_keys_names = [fname(name) for name in primary_keys]
                unique = set["value"]
                case = base
                for key in primary_keys_names:
                    case += " b.{0} = a.{0} \n and ".format(key)
                case = case[:-4]
                case += "WHERE b.{0} != a.{0}".format(unique)
                detectFDV = self.query(case)
                if detectFDV["data"]:
                    fdv["found"] = True
                    fdv[
                        "msg"
                    ] += " Found FDV for : \n Keys = {0}, Value = '{1}' <br>".format(
                        primary_keys_names, unique
                    )

                res.append({"unique": unique, "table": detectFDV["data"]})

            if not fdv["found"]:
                fdv["msg"] = "No FDV found!"

        except Exception as X:
            return {"success": False, "error": X.args[0]}

        return {"success": True, "data": res, "fdv": fdv}

    def desc(self, database, table):
        """
        table description

        :param database.table:
        :return:
        """
        self.connecti()
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("desc {0}.{1};".format(database, table))
                data = cursor.fetchall()
                formatDesc = lambda x: x[0]
                data = [formatDesc(row) for row in data]
        except Exception as X:
            return {"success": False, "error": str(X.args[0])}
        finally:
            self.conn.close()
        return {"success": True, "data": data}
