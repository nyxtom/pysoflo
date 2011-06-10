![python](python.png)
Introduction to Redis, Socket.io, Gevent and Django
###################################################

    Presented by: Thomas Holloway

    Hosted by Nextown Technologies
    235 Lincoln Road, Miami Beach, FL

---

Do it live!
===========

<iframe width="750" height="550" src="http://www.youtube.com/embed/5j2YDq6FkVE" frameborder="0" allowfullscreen></iframe>

---

Why sites should be live?
========================

.notes: More like a game, users will ultimately spend more time on the website as new stuff comes in (A.D.D. awesome!)

* Quicker feedback
* More informed users
* More engaging experience
* More return on investment
* It's fun development!


---

Issues to run into
==================

* The web is stateless (typically)
* Managing sessions
* Connection timeouts
* Concurrency (**yay!**)
* Persistence
* Things can come out of order
* People do run older browsers (thx IE, thx)
* Mo' queries, mo' problems


---

Messaging patterns
=========================

**Note: We've always had client/server technologies that can communicate
in this fashion. Leveraging this on the web is fairly similar.**

* Request-reply: ``connects a set of clients to a set of services. - rpc, task distribution pattern``
* Publish/Subscribe: ``connects a set of publishers to a set of subscribers. - data distribution pattern.``
* Push-pull: ``connects nodes in a fan-out / fan-in pattern that can have multiple steps and loops - parallel task distribution, collection pattern.``
* Exclusive pair: ``connects two sockets in an exclusive pair. - low-level pattern for specific use.``


---

<iframe style="margin-top: -130px; margin-left: 40px;" src="http://www.slideshare.net/slideshow/embed_code/2563177" 
width="725" height="655" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>


---

Redis.io
========

Described as: ``an open source, advanced key-value store. Often referred
to as a data structure server since keys can contain strings, hashes,
lists, sets and sorted sets.``

Data Structures:
http://redis.io/topics/data-types

---

Redis.io String Data Structure
==============================
- **Strings**: most basic, binary safe, max 512 MB in length
  - Use strings as atomic counters: INCR, DECR, INCRBY
  - Append to strings with APPEND
  - Use strings to access vectors with GETRANGE, SETRANGE
  - Encode a lot of data in little space, or create a Redis backed Bloom
    Filter (GETBIT and SETBIT)
    - http://en.wikipedia.org/wiki/Bloom_filter

---

Redis.io Hashes
===============

.notes: (few 100, store millions of objects in small instance, 2^(32-1) field-value pairs)

* **Hashes**: maps between string field and string value
    * Perfect data type to represent objects
        * Ex: users with a number of fields like name, surname..etc


---

Commands for Redis.io Hashes
============================
* HDEL ``key field``: delete a hash field
* HEXISTS ``key field``: does it exist?
* HGET ``key field``: get a value of a hash field
* HGETALL ``key``: get all the field and values of a hash
* HINCRBY ``key field increment``: increment integer value of hash field by given number
* HKEYS ``key``: get all the fields of a hash
* HLEN ``key``: number of fields
* HMGET ``key field [field ...]``: get values of all given hash fields
* HMSET ``key field value [field value ...]``: set multiple hash-field values
* HMSETNX ``key field value``: set value of a hash field (only if !exists)
* HVALS ``key``: get all the values


---

![redis](redis.png)
========

<iframe src="http://try.redis-db.com/" width="860" height="580"
frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>

---

Publish/Subscribe with Redis
============================

    !python
    from redis import Redis
    from gevent.greenlet import Greenlet
    from django.http import HttpResponse

    def listener(socketio):
        red = Redis('localhost')
        pubsub = red.pubsub()
        pubsub.subscribe('users-online')
        for i in pubsub.listen():
            socketio.send({'message': i})

    def socketio(request):
        socketio = request.environ['socketio']
        while True:
            message = socketio.recv()
            if len(message) and message[0] == 'subscribe-me!':
                g = Greenlet.spawn(listener, socketio)

        return HttpResponse()

    def send_message(json_data):
        red = Redis('localhost')
        red.publish('users-online', json_data)

---

Greenlets & GEvent
==================

gevent is a Python networking library that uses **greenlet** to provide an
async API on top of **libevent** event loop.

- Fast event loop based on libevent (epoll on Linux, kqueue on FreeBSD)
- Lightweight execution units based on greenlet
- Cooperative socket and ssl modules
- Ability to use standard library and 3rd party modules written for
  standard blocking sockets (gevent.monkey)
- DNS queries performed through libevent-dns
- Fast WSGI server based on libevent-http

**libevent**: API that provides a mechanism to execute a callback function
when a specific event occurs on a file descriptor or after a timeout has
been reached. Supports callbacks due to signals or regular timeouts. Meant
to replace the event loop found in event-driven network servers.


---

Web sockets!!
====================================

.notes: remember how excited you were when you heard about websockets?

![koolaid](koolaid.jpg)

- Case in point... shit breaks for people who don't have it supported


---

Socket.io
=========

.notes: awesome callback support for heartbeats, progressive retries..etc

* Supports cross-domain connections (on every browser)
* In order to support real-time connectivity on every browser, socket.io
  selects the most capable transport at runtime.
    * WebSocket
    * Adobe Flash Socket
    * AJAX long polling
    * AJAX multipart streaming
    * Forever Iframe
    * JSONP Polling

---

Socket.io Browsers
==================
* Supported browsers
    * IE 5.5+
    * Safari 3+
    * Google Chrome 4+
    * Firefox 3+
    * Opera 10.61
    * **Mobile**: IPhone Safari, IPad Safari, Android WebKit, WebOs WebKit


---

Socket.io WSGI Server
=====================


    !python
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    # Be sure to pip install redis, gevent, gevent-websocket, gevent-socketio
    from gevent import monkey
    from socketio import SocketIOServer
    import django.core.handlers.wsgi
    import os, sys, settings

    # use gevent to patch the standard lib to get async support
    monkey.patch_all()

    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    app = django.core.handlers.wsgi.WSGIHandler()
    sys.path.insert(0, os.path.join(settings.PROJECT_PATH, '../'))
    sys.path.insert(0, os.path.join(settings.PROJECT_PATH, 'apps'))

    if __name__ == '__main__':
        SocketIOServer(('', 7777), app, resource='socket.io').server_forever()

---

Socket.io Javascript
====================

    !html
    <script type="text/javascript" src="{{ MEDIA_URL }}js/socket.io.min.js"></script>
    <script type="text/javascript">
        $(document).ready(function() {
            var server = new io.Socket('{{ HOST }}', {{ PORT }});
            server.on('connect', function() {
                console.log('Connected to socket.io!!');
            });
            server.connect();
        });
    </script>

---

Socket.io Events
================

* connect: fired when the connection is established and the handshake successful.
* connecting(``transport_type``): fired with a connection is attempted, passing the transport name.
* connect_failed: Fired when the connection timeout occurs after the last
* message(``message``): fired when a message arrives
* close: fired when the connection is closed. Be careful with using this events, as some transports will fire it even under temp, expected disconnections (such as XHR-Polling).
* disconnect: fired when the connection is considered disconnected
* reconnect(``transport_type``, ``reconnectionAttempts``): fired when a reconnection is attempted, passing the next delay for the next reconnection.

---

These things and more!
======================

This presentation has a some source online:

* http://github.com/miamiwebstaff/pysoflo
* http://github.com/nyxtom/
* http://github.com/nyxtom/saywhat
