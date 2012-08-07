import random, redis, web

r = redis.StrictRedis(host='localhost', port=6379, db=0)

urls = (
    '/entry/?', 'entry_random',
    '/entry/(.+)/(.+)', 'entry_create',
    '/entry/(.+)', 'entry_get',
    '/list/(.+)', 'list'
)

class entry_random:

    def GET(self):
        length = r.llen('keys')
        if length:
            key = r.lindex('keys', random.randint(0, length-1))
            return "{0} -> {1}".format(key, r.hget('values', key))
        else:
            return ''

    def POST(self):
        web.ctx.status = '400 BAD REQUEST'

class entry_create:

    def POST(self, key, value):
        if key and not r.exists(key):
            r.hset('values', key, value) # Set key value
            r.rpush('keys', key) #

class entry_get:

    def GET(self, key):
        if not r.hexists('values', key):
            raise web.notfound()
        return r.hget('values', key)

    def POST(self, key):
        web.ctx.status = '400 BAD REQUEST'

class list:

    def GET(self, i):
        start = int(i) * 4
        keys = r.lrange('keys', start, start+3)
        return "\n".join(["{0} -> {1}".format(k, r.hget('values', k)) for k in keys])

if __name__ == "__main__":
    for k in r.keys():
        r.delete(k)
    app = web.application(urls, globals())
    app.run()
