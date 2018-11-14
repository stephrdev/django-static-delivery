Advanced topics
===============

Nginx configuration
-------------------

To improve the performance of static file delivery, you might use the cache options
Nginx provide.

Here is an example configuration of Nginx together with uwsgi:

.. code-block:: nginx

    # Prepare a cache with 100 MB storage capacity
    uwsgi_cache_path
        /path/to/cache
        levels=1:2
        keys_zone=static_cache:2m
        max_size=100m
        inactive=1w
        use_temp_path=off;

    # You django backend / uwsgi process
    upstream app {
        server django:8000;
    }

    server {
        listen 80 default_server;
        root /var/www;

        location / {
            try_files $uri @proxy_to_app;
        }

        # Important section, tell nginx to use the cache for all requests to /static/*
        location /static/ {
            uwsgi_cache static_cache;
            uwsgi_cache_use_stale updating;
            uwsgi_cache_lock on;
            uwsgi_cache_valid any 1w;
            uwsgi_cache_key $host$request_uri;

            include uwsgi_params;
            uwsgi_pass app;
        }

        location @proxy_to_app {
            include uwsgi_params;
            uwsgi_pass app;
        }
    }


Please note, this is just an example. Please test the configration before putting this
to production.

.. note::

    You are not bound to use uWSGI. Gunicorn will work fine too - you just need to
    find the Nginx equivalents to the uwsgi_* settings (most of them will be prefixed proxy_*)
