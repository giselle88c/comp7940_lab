"""Basic connection example.
redis
"""

import redis

r = redis.Redis(
    host='redis-19958.c256.us-east-1-2.ec2.redns.redis-cloud.com',
    port=19958,
    decode_responses=True,
    username="default",
    password="bxPZDk4Kq7oAa92lP3ht8efkvgYQr5xD",
)

success = r.set('foo', 'bar')
# True

result = r.get('foo')
print(result)
# >>> bar

