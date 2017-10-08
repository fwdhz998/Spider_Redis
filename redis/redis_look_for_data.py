import redis

def look_for_redis(user):
    if user=='master':
        pool = redis.ConnectionPool(host='localhost', port=6379)
        r=redis.Redis(connection_pool=pool)
    elif user=='slaver':
        r=redis.Redis(host='115.156.186.125',port=6379)
    else:
        print '''Input 'master'or'slaver'''
    print "ershoufang_urls=",r.scard("ershoufang_urls")
    print 'rents_urls=',r.scard("rents_urls")

if __name__ == '__main__':
    look_for_redis('master')