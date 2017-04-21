from http import client

from django.core.management.base import BaseCommand, CommandError
import boto3



class Command(BaseCommand):
    help = 'Empty the external bucket from any leftover & delete all csv results files'

    def handle(self, *args, **options):
        s3 = boto3.resource(
                            's3',
                            region_name='us-east-1',
                            )
        bucket = s3.Bucket('athena-internship')

        objects_to_delete = bucket.objects.all()
        for obj in objects_to_delete:
            self.stdout.write(self.style.NOTICE("Deleting : " + obj.key))

        try :
            bucket.objects.delete()
        except:
            raise CommandError("Could not purge the bucket")

        self.stdout.write(self.style.SUCCESS('Successfully Purged! The bucket is clean!'))