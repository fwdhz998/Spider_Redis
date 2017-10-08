import redis

r=redis.Redis(host='115.156.186.125',port=6379)

print r.get('foo')