sm
==
This sample code demonstrates the use of web.py for restful interface for a key/value store.  It uses redis to manage key/values in memory.  In particular, it uses two data structures in redis, a hash and a list.  The hash contains the key/values and the hash stores the keys for easy random access and paging.  Although there is a small trade-off by maintaining redundant keys, it greatly improves the GET requests performance.
