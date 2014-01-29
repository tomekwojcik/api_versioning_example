# API Versioning examples

This repository contains example Flask apps that are meant to visualize the
difference between path- and header-based API versioning.

## Path-based versioning

App available in `through_header` package uses path-based API versioning. It
consists of two blueprints - `api_v1` and `api_v2`. Each one of them is
mounted under its own URL prefix. Effectively, both API versions are separate.

Being separate, both blueprints can use different databases and other
resources (e.g. remote services) to serve API clients. It's also possible to
easily extract one of them into completely new app.

Routing uses standard mechanisms (`Blueprint.route` decorator) which means
that this scheme of API separation requires no changes to the underlying
framework.

Disabling one version of the API is as simple as commenting out two lines of
code (e.g. `through_path/app.py` lines 12 and 13).

## Header-based versioning

App available in `through_header` package uses simple header-based API
versioning. It consists of two blueprints - `api`. It's moounted under
`/api` URL prefix. API version discovery is done by the blueprint's
`before_request` callback. Both API versions share the same code base and
view functions must alter their behavior (e.g. response format) according to
API version being requested.

Extracting a single API version into a separate app requires going through the
entire code base to move the relevant pieces of code into the new app.

Since both API versions share the same URL prefix, each view function must
define behavior for both API versions. If a given endpoint doesn't exist in a
given API version, then view function must properly react to this condition
(e.g. respond with `HTTP 400` status).

Routing uses standard mechanisms (`Blueprint.route` decorator) which means
that this scheme of API separation requires no changes to the underlying
framework.

Disabling one version of the API at least requires changes in the
`before_request` filter.

## A note on proxying in nginx

Suppose you have an app that exports some sort of API, e.g. for mobile clients
and you wish to introduce a new version of the API. Obviously, you're going to
need keep the old version around. You decide to go with different clusters for
both the API versions.

**NOTE**: I only have limited experience with nginx. Somebody smarter than me
can surely do it better :).

Let's look at nginx config for path-based versioning:

    server {
        server_name example.com;
        listen      127.0.0.1:80;

        location /api/v1 {
            proxy_pass  http://api1.example.com:8080;
        }

        location /api/v2 {
            proxy_pass  http://api2.example.com:8080;
        }

        location / {
            proxy_pass  http://web.example.com:8080;
        }
    }

Here, routing between servers is done via standard `location` directive. Easy
to maintain, easy to verify.

Now, how about some config for header-based versioning:

    server {
        server_name api_through_header.web;
        listen      127.0.0.1:80;

        location /api {
            if ($http_x_apiversion = 1) {
                proxy_pass  http://api1.example.com:8080;
                break;
            }

            if ($http_x_apiversion = 2) {
                proxy_pass  http://api2.example.com:8080;
                break;
            }

            return 400;
        }

        location / {
            proxy_pass  http://web.example.com:8080;
        }
    }

IMO routing here is tricky. Personnaly, I like to keep my nginx/haproxy/Varnish
configs as simple as possible to avoid hunting weird bugs in production when
something goes wrong.

## Finishing thoughts

As I stated on Twitter, I don't believe in header-based API versioning. It
forces me to hack and write ugly code. Not to mention headers similar to
`Accept: application/vnd.me.v1+json`. Path-based versioning, on the other hand,
uses standard HTTP and framework mechanisms to achieve versioning.

