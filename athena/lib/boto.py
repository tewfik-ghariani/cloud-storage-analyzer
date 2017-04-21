import os
import mimetypes
import re
import boto3
from lib import cloud_store

class BotoLoader():
    def __init__(self, bucket, region):
        self.s3 = boto3.resource('s3',
                                 region_name=region)
        self.bucket_name = bucket
        self.bucket = self.s3.Bucket(self.bucket_name)
        self.client = boto3.client(
            's3',
            region_name=region,
        )

    def s3loader(self, prefix):
        res = []

        object_summary_iterator = self.bucket.objects.filter(
            Delimiter='/',
            Prefix=prefix
        )

        for obj in object_summary_iterator:
            res.append(obj.key)
        return res

    def search(self, key):
        res = []
        all_objects = self.bucket.objects.all()

        for obj in all_objects:
            if re.match(key, obj.key):
                res.append(obj.key)
        return res



    def to_athena(self, customer, key):

        copy_source = {
            'Bucket': self.bucket_name,
            'Key': key
        }


        dest_key = "tmp/{0}/{1}".format(customer, key)
        if re.match(r'.*gz.*', dest_key):
            head, sep, tail = dest_key.partition('.gz')
            dest_key = head + sep

        '''command_download = "download s3://{0}/{1} ".format(self.bucket_name, key)
        cloud_store.main(command_download)
        command_upload = "upload -i {0} s3://athena-internship/{1}".format(key, dest_key)
        cloud_store.main(command_upload)

        try:
            os.remove(key)
        except Exception as X:
            print(X)
        '''
        try:
            self.s3.meta.client.copy(copy_source,
                                     'athena-internship',
                                     dest_key,
                                     )
        except Exception as X:
            return X

        return True

    def download_from_bucket(self, file):
        try:

            self.bucket.download_file(file, file)

            content_type = mimetypes.guess_type(file)[0]
            content_length = os.path.getsize(file)
            content_disposition = 'attachment; filename="%s"' % file

        except Exception as X:
            print(X)
            return False
        return content_type, content_length, content_disposition

    """
    Delete file from the bucket athena for now ( /tmp later )
    """
    def delete_from_athena(self, customer, key, how = True):
        if how:
            dest_key = "tmp/{0}/{1}".format(customer, key)
        else:
            dest_key = key

        if re.match(r'.*gz.*', dest_key):
            head, sep, tail = dest_key.partition('.gz')
            dest_key = head + sep

        response = self.client.delete_object(Bucket='athena-internship', Key=dest_key)
        """all = re.compile('*')
        response = self.client.delete_object(
            Bucket='athena-internship',
            Delete={
                'Objects': [
                    {
                    'Key': key,
                     },
        ],
        })
        """
        return response

    def s3_prefixes(self, prefix):
        result = self.bucket.meta.client.list_objects_v2(Bucket=self.bucket_name,
                                                         Delimiter='/',
                                                         Prefix=prefix)
        res = []
        try:
            for o in result.get('CommonPrefixes'):
                res.append(o.get('Prefix'))
        except Exception as X:
            pass

        return res
