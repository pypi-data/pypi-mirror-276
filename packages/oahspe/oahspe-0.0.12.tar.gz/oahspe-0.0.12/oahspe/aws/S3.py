# coding: utf-8


from oahspe.tool import *

class AwsS3:
  def __init__(self, access, secret, endpoint, bucket=None):
    from boto3 import client
    self.login = client(
      's3',
      aws_access_key_id = access,
      aws_secret_access_key = secret,
      endpoint_url = endpoint
    )
    self.bucket = bucket


  def list_object(self, prefix=''):
    from pandas import DataFrame
    content = []
    for page in self.login.get_paginator('list_objects_v2').paginate(Bucket=self.bucket, Prefix=prefix):
      if 'Contents' in page:
        for obj in page['Contents']:
          key, prefix = parse_key(obj['Key'])
          content.append({
            'key': key,
            'prefix': prefix,
            'size': int(obj['Size']),
            'etag': obj['ETag'].strip('"'),
            'modified': obj['LastModified'],
          })
    content = DataFrame(content)
    return content


  def transfer_config(self, args={}):
    from boto3.s3.transfer import TransferConfig
    args = setdefault(args, {
      'multipart_threshold': 100*1024*1024+1,
      'multipart_chunksize': 100*1024*1024,
      'use_threads': True,
      'max_concurrency': 16,
    })
    self.transfer = TransferConfig(**args)
  

  def copy_object(self, src_key, dst_key, dst_bucket=None):
    if dst_bucket is None: dst_bucket = self.bucket
    self.login.copy_object(Bucket=self.bucket, CopySource={'Bucket':dst_bucket,'Key':src_key}, Key=dst_key)


  def delete_object(self, key):
    self.login.delete_object(Bucket=self.bucket, Key=key)


  def move_object(self, src_key, dst_key, dst_bucket=None):
    self.copy_object(src_key, dst_key, dst_bucket)
    self.delete_object(src_key)


  def put_object(self, key, data):
    self.login.put_object(Bucket=self.bucket, Key=key, Body=data)


  def put_local(self, local, key, type='bz2', checksum=False):
    if isinstance(local, str):
      if os.path.isfile(local): return self.put_file(local, key, checksum)
      elif os.path.isdir(local): return self.put_folder(local, key, type, checksum)
    local = tmp_write(to_byte(local))
    res = self.put_file(local, key, checksum)
    os.remove(local)
    return res


  def put_file(self, local, key, checksum=False):
    if not hasattr(self, 'transfer'): self.transfer_config()
    self.login.upload_file(local, Bucket=self.bucket, Key=key, Config=self.transfer)
    if checksum:
      return self.checksum(local, key)


  def put_folder(self, local, key, type='bz2', checksum=False):
    local = tar(local, type=type)
    res = self.put_file(local, key, checksum)
    os.remove(local)
    return res


  def checksum(self, local, key):
    from math import floor
    head = self.head_object(key)
    size, etag = head['size'], head['etag']
    chunk = floor(size / int(etag.split('-')[-1])) if '-' in etag else size
    return checksum(local, chunk) == etag


  def head_object(self, key):
    res = self.login.head_object(Bucket=self.bucket, Key=key)
    return {
      'modified': res['LastModified'],
      'size': int(res['ContentLength']),
      'etag': res['ETag'].strip('"'),
      'type': res['ContentType'],
    }

  def get_object(self, key) -> bytes:
    with self.login.get_object(Bucket=self.bucket, Key=key)['Body'] as f:
      res = f.read()
    return res
  

  def delete_prefix(self, prefix=''):
    danhsach = self.list_object(prefix)
    if len(danhsach) == 0: return
    danhsach = danhsach['key'].to_list()
    if prefix:
      danhsach = [prefix + '/' + key for key in danhsach]
    for key in danhsach:
      self.delete_object(key)


  def list_bucket(self):
    from pandas import DataFrame
    return DataFrame([{
      'name': obj['Name'],
      'creation_date': obj['CreationDate'],
    } for obj in self.login.list_buckets()['Buckets']])


  def create_bucket(self):
    self.login.create_bucket(Bucket=self.bucket)
  

  def delete_bucket(self):
    self.delete_prefix()
    self.login.delete_bucket(Bucket=self.bucket)
