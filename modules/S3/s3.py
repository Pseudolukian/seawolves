import asyncio
import aioboto3
from contextlib import asynccontextmanager
from typing import AsyncContextManager, Any
import configparser
import aiofiles
from pprint import pprint

@asynccontextmanager
async def s3_session() -> AsyncContextManager:
    session = aioboto3.session.Session(
        aws_access_key_id = "YCAJE7srO1x0ucWLMF6-fnL7x",
        aws_secret_access_key = "YCNMTzK545MZfwxru7GGsjpTaiDigYDw9dJ96SKr",
        region_name="ru-central1"
    )
    async with session.client('s3', endpoint_url='https://storage.yandexcloud.net') as client:
        yield client


class S3:
    def __init__(self, session: Any, s3_conf_path: str = './S3_structure.cfg'):
        self.session = session
        self.s3_conf_path = s3_conf_path

    async def conf_loader(self):
        config = configparser.ConfigParser()
        async with aiofiles.open(self.s3_conf_path, mode='r') as file:
            contents = await file.read()
            config.read_string(contents)
            return config

    async def create_bucket(self, bucket_name: str):
        async with self.session() as s3:
            bucket = await s3.create_bucket(Bucket=bucket_name)
            return {'StatusCode': bucket['ResponseMetadata']['HTTPStatusCode']}

    async def delete_bucket(self, bucket_name: str):
        async with self.session() as s3:
            bucket = await s3.delete_bucket(Bucket=bucket_name)
            return {'StatusCode': bucket['ResponseMetadata']['HTTPStatusCode']}

    async def create_folder(self, bucket_name: str, folder_path: str):
        async with self.session() as s3:
            folder = await s3.put_object(Bucket=bucket_name, Key=folder_path)
            return {'StatusCode': folder['ResponseMetadata']['HTTPStatusCode']}

    async def delete_folder(self, bucket_name: str, folder_path: str):
        async with self.session() as s3:
            folder = await s3.delete_object(Bucket=bucket_name, Key=folder_path)
            return {'StatusCode': folder['ResponseMetadata']['HTTPStatusCode']}

    async def create_structure(self, id:str, bucket_name: str = 'seausers', structure_name: str = 'sea_user'):
        conf = await self.conf_loader()
        paths = []
        if structure_name in conf:

            for key, path_template in conf[structure_name].items():
                folder_path = path_template.format(user_id=id)
                paths.append(folder_path)

        for path in paths:
            await self.create_folder(bucket_name=bucket_name, folder_path=path)

        return {'StatusCode': 200, 'Created:': paths}


"""
s3_ses = s3_session
test_s3 = S3(session=s3_ses)

if __name__ == "__main__":
    #pprint(asyncio.run(s3_conf_load))
    #print(asyncio.run(test_s3.create_bucket(bucket_name='pppp')))
    #print(asyncio.run(test_s3.delete_bucket(bucket_name='pppp')))
    #print(asyncio.run(test_s3.create_folder(bucket_name='seausers', folder_path='test/')))
    #print(asyncio.run(test_s3.delete_folder(bucket_name='pppp', folder_path='test/')))
    print(asyncio.run(test_s3.create_structure(id='qweeersasddsada')))
"""