import boto3
from boto3 import Session

class S3:
    def __init__(self, session: Session, bucket_name: str, serv_name: str, endpoint: str):
        self.session = session
        self.bucket_name = bucket_name
        self.serv_name = serv_name
        self.endpoint = endpoint

    def create_bucket(self):
        s3 = self.session.client(service_name=self.serv_name, endpoint_url=self.endpoint)
        return s3.create_bucket(Bucket=self.bucket_name)


test_s3 = S3(session=boto3.session.Session(), bucket_name='loik', serv_name='s3', endpoint='https://storage.yandexcloud.net')

print(test_s3.create_bucket())