import random, redis, web

# Connect to redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# URL mapping
urls = (
    '/entry/?', 'entry_random',
    '/entry/(.+)/(.+)', 'entry_create',
    '/entry/(.+)', 'entry_get',
    '/list/(.+)', 'list',
    '.*', 'bad_request'
)

# 400 error for any un-matched URLs
class bad_request:
    def GET(self):
        raise web.badrequest()

# Random entry
class entry_random:

    #  Return random entry
    def GET(self):
        length = r.llen('keys')
        if length:
            key = r.lindex('keys', random.randint(0, length-1))
            return "{0} -> {1}".format(key, r.hget('values', key))
        else:
            raise web.notfound()

    # Handle post error for random entries
    def POST(self):
        web.ctx.status = '400 BAD REQUEST'

# Create entry
class entry_create:

    # Create entry on post
    def POST(self, key, value):
        key = key[0:126] # limit to 127 characters
        value = value[0:126] # limit to 127 characters
        if key and not r.exists(key):
            r.hset('values', key, value) # Set key value
            r.rpush('keys', key) # Add to list for random and paging

# Get entry
class entry_get:

    # Return entry by key or 404 if does not exist
    def GET(self, key):
        val = r.hget('values', key)
        if not val:
            raise web.notfound()
        return val

    # Return 400 error for post
    def POST(self, key):
        web.ctx.status = '400 BAD REQUEST'

# List entries
class list:

    # Show 4 entries per page
    def GET(self, i):
        start = int(i) * 4
        keys = r.lrange('keys', start, start+3)
        return "\n".join(["{0} -> {1}".format(k, r.hget('values', k)) for k in keys])

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
