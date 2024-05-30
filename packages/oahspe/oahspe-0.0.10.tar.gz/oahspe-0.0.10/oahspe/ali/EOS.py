# coding: utf-8

class AlicloudEOS:
  def __init__(self, access, secret, bucket):
    from oss2 import Auth, Bucket
    self.login = Bucket(
      auth = Auth(access, secret),
      endpoint = 'https://eos.aliyuncs.com',
      bucket_name = bucket,
    )
    self.bucket = bucket
  
  
  def list_object(self, prefix=''):
    from pandas import DataFrame
    from oahspe.tool import parse_key
    from oss2 import ObjectIterator
    from datetime import datetime
    content = []
    for obj in ObjectIterator(self.login, prefix):
      key, prefix = parse_key(obj.key)
      content.append({
        'key': key,
        'prefix': prefix,
        'modified': datetime.fromtimestamp(int(obj.last_modified)),
        'etag': obj.etag.lower(),
        'size': int(obj.size),
      })
    content = DataFrame(content)
    return content
