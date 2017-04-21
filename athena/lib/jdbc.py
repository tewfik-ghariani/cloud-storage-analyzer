import os
import pyathenajdbc
import re

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
                return X
        finally:
            self.conn.close()
        return True

    def create(self, database, table, cols, types, delim, location):
        self.connecti()
        create_q = "CREATE EXTERNAL TABLE IF NOT EXISTS {0}.{1} (".format(database, table)
        columns = ""

        for i in range(len(cols)):
            if re.match(r'Select', types[i]):
                types[i] = "string"
            one_col = " {0} {1}, ".format(cols[i], types[i])
            columns += one_col

        columns = columns[:-2]
        create_q += columns
        create_q += """)
                    ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
                    WITH SERDEPROPERTIES (
                        'serialization.format' = '{0}',
                        'field.delim' = '{0}',
                        'collection.delimm' = 'undefined',
                        'mapkey.delim' = 'undefined'
                    ) LOCATION '{1}';
                """.format(delim, location)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(create_q)
        except Exception as X:
                return X
        finally:
            self.conn.close()
        return True

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
            return X
        finally:
            self.conn.close()
        return res

    # def detect(self, res):

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
        # print(pyathenajdbc.__doc__)
        # print(pyathenajdbc.__loader__)
        dic = pyathenajdbc.__dict__

        res = []
        for i in dir(pyathenajdbc):
            temp = i + ' = ' + str(dic[i])
            # print(temp)
            res.append(temp)

        return res