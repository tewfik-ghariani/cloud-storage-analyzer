import os
import mimetypes
import re
import boto3
from hurry.filesize import size as hsize
import time

EXTERNAL_BUCKET = "athena-internship"


class BotoLoader:
    lock = False
    folders = []
    MAX = 5

    def __init__(self, bucket, region):
        self.s3 = boto3.resource("s3", region_name=region)
        self.bucket_name = bucket
        self.bucket = self.s3.Bucket(self.bucket_name)
        self.client = boto3.client("s3", region_name=region,)

    def s3loader(self, prefix):
        res = []
        try:
            object_summary_iterator = self.bucket.objects.filter(
                Delimiter="/", Prefix=prefix
            )
            for obj in object_summary_iterator:
                res.append(obj.key)
        except Exception as X:
            return {"success": False, "error": X.args[0]}
        return {"success": True, "data": res}

    def search(self, key):
        res = []
        try:
            all_objects = self.bucket.objects.all()

            for obj in all_objects:
                if re.match(key, obj.key):
                    res.append(obj.key)
        except Exception as X:
            print(X.args[0])
            return {"success": False, "error": "The search operation is not possible"}
        return {"success": True, "data": res}

    def copy_to_athena(self, customer, table, key):
        # Verify if the external bucket is not empty using a class attribute lock
        folder = customer + "." + table
        while BotoLoader.lock or folder in BotoLoader.folders:
            time.sleep(2)

        BotoLoader.folders.append(folder)
        # BotoLoader.lock = True

        copy_source = {"Bucket": self.bucket_name, "Key": key}

        dest_key = "tmp/{0}/{1}/{2}".format(customer, table, key)
        if re.match(r".*gz.*", dest_key):
            head, sep, tail = dest_key.partition(".gz")
            dest_key = head + sep

        try:
            self.s3.meta.client.copy(
                copy_source, EXTERNAL_BUCKET, dest_key,
            )
        except Exception as X:
            if folder in BotoLoader.folders:
                BotoLoader.folders.remove(folder)
            return {"success": False, "error": X.args[0]}

        return {"success": True}

    def download_from_bucket(self, object):
        """
        Download text files for now
        :param object(full name of s3 object):
        :return:
        """
        try:
            if re.match(r".*/*", object):
                file = object.split("/")[-1]
            else:
                file = object

            self.bucket.download_file(object, file)
            content_type = mimetypes.guess_type(file)[1]
            content_length = os.path.getsize(file)
            content_disposition = 'attachment; filename="{0}"'.format(file)
        except Exception as X:
            print(X.args[0])
            return {"success": False, "error": X.args[0]}
        return {
            "success": True,
            "data": {
                "content_type": content_type,
                "content_length": content_length,
                "content_disposition": content_disposition,
                "filename": file,
            },
        }

    def delete_from_athena(self, customer, table, key, auto=False):
        """
        Delete file from the bucket athena
        """
        if table:
            folder = customer + "." + table
            if folder in BotoLoader.folders:
                BotoLoader.folders.remove(folder)

        if auto:
            dest_key = "tmp/{0}/{1}/{2}".format(customer, table, key)
            # BotoLoader.lock = False
        else:
            dest_key = key

        if re.match(r".*gz.*", dest_key):
            head, sep, tail = dest_key.partition(".gz")
            dest_key = head + sep

        try:
            self.client.delete_object(Bucket=EXTERNAL_BUCKET, Key=dest_key)
        except Exception as X:
            return {"success": False, "error": X.args[0]}
        return {"success": True}

    def s3_prefixes(self, prefix):
        try:
            result = self.bucket.meta.client.list_objects_v2(
                Bucket=self.bucket_name, Delimiter="/", Prefix=prefix
            )
            res = []
            if result.get("CommonPrefixes"):
                for o in result.get("CommonPrefixes"):
                    res.append(o.get("Prefix"))

        except Exception as X:
            return {"success": False, "error": X.args[0]}

        return {"success": True, "data": res}

    def getSize(self, key, external=False):
        try:
            if external:
                print(BotoLoader.folders)
                target_bucket = EXTERNAL_BUCKET
            else:
                target_bucket = self.bucket_name

            object = self.client.head_object(Bucket=target_bucket, Key=key)
            size = object["ContentLength"]
            size = hsize(size)
        except Exception as X:
            return {"success": False, "error": X.args[0]}
        return {"success": True, "size": size}
