import pytest
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse

from static_delivery.middleware import StaticDeliveryMiddleware


def test_invalid_static_url_setting(settings):
    settings.STATIC_URL = 'https://my.cdn.com/static/'
    with pytest.raises(ImproperlyConfigured):
        StaticDeliveryMiddleware(None)

    settings.STATIC_URL = '//my.cdn.com/static/'
    with pytest.raises(ImproperlyConfigured):
        StaticDeliveryMiddleware(None)


def test_invalid_static_storage_setting(settings):
    settings.STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    with pytest.raises(ImproperlyConfigured):
        StaticDeliveryMiddleware(None)


class TestMiddlewareCall:
    def setup(self):
        self.middleware = StaticDeliveryMiddleware(lambda r: HttpResponse(b'NOSTATIC'))

    def test_no_static(self, rf):
        response = self.middleware(rf.get('/foo/'))
        assert response.status_code == 200
        assert response.content == b'NOSTATIC'

    def test_file_served(self, rf):
        response = self.middleware(rf.get('/static/test.txt'))
        assert response.status_code == 200
        assert response.file_to_stream.name.endswith('test.txt')
        assert response['Content-Type'] == 'text/plain'

    def test_file_notfound(self, rf):
        response = self.middleware(rf.get('/static/notfound.txt'))
        assert response.status_code == 200
        assert response.content == b'NOSTATIC'

    def test_file_hashed(self, rf):
        response = self.middleware(rf.get('/static/test_hash.11aa22bb33cc.jpg'))
        assert response.status_code == 200
        assert response['Content-Type'] == 'image/jpeg'

    def test_file_recovered_hash(self, rf):
        response = self.middleware(rf.get('/static/test_hash.44dd66eee899.jpg'))
        assert response.status_code == 200
        assert response['Content-Type'] == 'image/jpeg'

    def test_file_unrecoverable(self, rf):
        response = self.middleware(rf.get('/static/notfound.44dd66eee899.jpg'))
        assert response.status_code == 200
        assert response.content == b'NOSTATIC'
