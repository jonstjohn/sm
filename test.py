import unittest, httplib, redis

tests = [
    {'op': 'GET', 'url': '/entry/', 'code': 404}, # no entries yets
    {'op': 'GET', 'url': '/badurl', 'code': 400}, # bad url
    {'op': 'POST', 'url': '/entry/ffff/3456', 'code': 200},
    {'op': 'POST', 'url': '/entry/', 'code': 400},
    {'op': 'POST', 'url': '/entry/12', 'code': 400},
    {'op': 'POST', 'url': '/entry/12/qqqq', 'code': 200},
    {'op': 'GET', 'url': '/entry/ffff', 'code': 200, 'output': '3456'},
    {'op': 'GET', 'url': '/entry/fffe', 'code': 404},
    {'op': 'GET', 'url': '/entry/', 'code': 200, 'output': ['12 -> qqqq', 'ffff -> 3456']},
    {'op': 'POST', 'url': '/entry/zz/zyx', 'code': 200},
    {'op': 'POST', 'url': '/entry/az/zyx', 'code': 200},
    {'op': 'POST', 'url': '/entry/34/zyx', 'code': 200},
    {'op': 'POST', 'url': '/entry/AF/zyx', 'code': 200},
    {'op': 'POST', 'url': '/entry/zez/zyx', 'code': 200},
    {'op': 'GET', 'url': '/list/0', 'code': 200, 'output': 'ffff -> 3456\n12 -> qqqq\nzz -> zyx\naz -> zyx'},
    {'op': 'GET', 'url': '/list/1', 'code': 200, 'output': '34 -> zyx\nAF -> zyx\nzez -> zyx'},
    {'op': 'GET', 'url': '/list/2', 'code': 200, 'output': ''}
]


class SmTestCase(unittest.TestCase):

    def runTest(self):
        
        # Clean up redis
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        for k in r.keys():
            r.delete(k)

        # Iterate over tests
        for test in tests:
            conn = httplib.HTTPConnection('localhost:8080')
            conn.request(test['op'], test['url'])
            response = conn.getresponse()
            self.assertEquals(response.status, test['code']) # check status code

            if 'output' in test: # check output if needed
                data = response.read()
                self.assertIn(data, test['output']) 

if __name__ == '__main__':
    unittest.main()
