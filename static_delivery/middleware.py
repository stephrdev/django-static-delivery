import re

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http.response import Http404
from django.views.static import serve


class StaticDeliveryMiddleware(object):
    """
    Middleware to serve static files from within Django.

    In some setups it is a good idea to serve static files from Django and have
    them cached in a reverse proxy like Nginx or something similar.

    By doing this, we can easily serve static files from our - for example - our
    Docker image without putting them in a shared volume.

    It is important to know that serving files from Django directly won't perform
    very well. Always have a cache in front of it.

    Additionally, the middleware is able to recover from invalid hashes in static
    file names when you use a staticfiles storage with name hashing in place.
    If a file with a certain hash is unavailable, the middleware will try to
    look up the correct hash for the file.
    """

    HASHED_PATH_RE = re.compile(r'(.+)(\.[0-9a-f]{12})(\.?)(\w+)?$')

    #: The middleware instance has a regex ready to match paths against STATIC_URL.
    path_re = None

    #: the staicfiles manifest is loaded once when the middleware is initialized.
    manifest = None

    def __init__(self, get_response=None):
        self.get_response = get_response

        if not (
            settings.STATIC_URL.startswith('/')
            and not settings.STATIC_URL.startswith(  # Is a relative path
                '//'
            )  # No schemaless absolute path
        ):
            raise ImproperlyConfigured(
                '`static_delivery` currently only works with same-domain static urls'
            )

        self.path_re = re.compile(r'^/{0}(.*)$'.format(settings.STATIC_URL.strip('/')))
        self.manifest = self.load_staticfiles_manifest()

    def __call__(self, request):
        """
        When the middleware is called, the request path is matched against the
        STATIC_URL settings. If the paths match, static content will be delivered.

        If the delivery fails or the path doesn't match, request processing will
        continue down to other middlewares and views.
        """
        static_path = self.path_re.match(request.path)
        if static_path:
            response = self.serve_response(request, static_path.group(1))
            if response:
                return response

        return self.get_response(request)

    def serve_response(self, request, path):
        """
        This method takes the request and a path to deliver static content for.

        The method tries to deliver content for the requested path, if this fails
        the code will try to recover the currently valid path and try to serve
        that file instead. If nothing works, None is returned.
        """
        response = self.get_staticfile_response(request, path)
        if response:
            return response

        recovered_path = self.recover_staticfile_path(path)

        return self.get_staticfile_response(request, recovered_path) if recovered_path else None

    def get_staticfile_response(self, request, path):
        """
        This method takes a path and tries to serve the content for the given path.
        Will return None if serving fails.
        """
        try:
            return serve(request, path, document_root=settings.STATIC_ROOT)
        except Http404:
            pass

        return None

    def recover_staticfile_path(self, path):
        """
        This method strips the hash from the requested path and tries to look up
        the unhashed file name in the manifest dataset.
        """
        parsed_path = self.HASHED_PATH_RE.search(path)
        if not parsed_path:
            return None

        return self.manifest.get(
            '{}{}{}'.format(
                parsed_path.group(1) or '',
                parsed_path.group(3) or '',
                parsed_path.group(4) or '',
            ).strip('/'),
            None,
        )

    def load_staticfiles_manifest(self):
        """
        Supported staticfiles storages map original static file names to hashed ones.
        This method loads the manifest file for lookups later.

        In addition, this method might raise an exception if the configured
        staticfiles storage doesn't support manifest files/data.
        """
        from django.contrib.staticfiles.storage import staticfiles_storage

        if not hasattr(staticfiles_storage, 'load_manifest'):
            raise ImproperlyConfigured(
                'The configured staticfiles storage has no support for manifest data.'
            )

        loaded_manifest = staticfiles_storage.load_manifest()

        # Django >=4.2 return a tuple with paths and hashed instead off only the paths.
        if isinstance(loaded_manifest, tuple):
            return loaded_manifest[0]

        return loaded_manifest
