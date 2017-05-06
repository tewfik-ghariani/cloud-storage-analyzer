import os
import pyathenajdbc

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_path = BASE_DIR + "/lib/static/queries.log"


class PyAthenaLoader():
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
            return {'success': False, 'error': X.args[0]}
        finally:
            self.conn.close()
        return {'success': True}

    def create(self, columns, delim, database, table):
        self.connecti()
        try:
            create_q = "CREATE EXTERNAL TABLE IF NOT EXISTS {0}.{1} (".format(database, table)

            for col in columns:
                # toDo verify type
                create_q += " {0} {1}, ".format(col['attr'], col['type'])
            create_q = create_q[:-2]

            create_q += """)
                        ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
                        WITH SERDEPROPERTIES (
                            'serialization.format' = '{0}',
                            'field.delim' = '{0}',
                            'collection.delimm' = 'undefined',
                            'mapkey.delim' = 'undefined'
                        ) LOCATION '""".format(delim)

            slocation = "s3://athena-internship"
            create_q += "{0}/tmp/{1}/{2}/';".format(slocation, database, table)

            with self.conn.cursor() as cursor:
                cursor.execute(create_q)
        except Exception as X:
            return {'success': False, 'error': X.args[0]}
        finally:
            self.conn.close()
        return {'success': True}

    """
    def detect(self,table):
        self.connecti()

        try:
            with self.conn.cursor() as cursor:
                cursor.execute('COUNT *')
    """

    def query(self, req):
        self.connecti()

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(req)
                res = cursor.fetchall()
        except Exception as X:
            return {'success': False, 'error': X.args[0]}
        finally:
            self.conn.close()
        return {'success': True, 'data': res}

    def checkFDV(self, fieldsFDV, customer, table):
        fetchQuery = "SELECT * from {0}.{1} ; ".format(customer, table)
        fileContent = self.query(fetchQuery)
        if not fileContent['success']:
            return fileContent

        try:
            content = fileContent['data']
            content = content[1:]
            print(content)

            # for set in fieldsFDV:

            set = fieldsFDV[0]
            primary_keys = set['headers']
            headers = ','.join(primary_keys)
            unique = set['unique']



        except Exception as X:
            return {'success': False, 'error': X.args[0]}
        return {'success': True, 'data': 'All Good'}

    def desc(self, table):
        """
        table description

        :param table:
        :return:
        """
        self.connecti()

        try:
            with self.conn.cursor() as cursor:
                cursor.execute('desc {0};'.format(table))
                res = cursor.description
        finally:
            self.conn.close()
        return res

    def info(self):
        """ Basic info about athena jdbc
        """
        print('_________')
        print(pyathenajdbc.ATHENA_DRIVER_CLASS_NAME)
        print(pyathenajdbc.ATHENA_CONNECTION_STRING)
        print(pyathenajdbc.ATHENA_DRIVER_DOWNLOAD_URL)
        print(pyathenajdbc.ATHENA_JAR)
        print(pyathenajdbc.BINARY)
        print(pyathenajdbc.__athena_driver_version__)
        print('________________')
        print(pyathenajdbc.ATHENA_CONNECTION_STRING)

        dic = pyathenajdbc.__dict__

        res = []
        for i in dir(pyathenajdbc):
            temp = i + ' = ' + str(dic[i])

            res.append(temp)

        return res
