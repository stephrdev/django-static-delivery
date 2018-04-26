import pytest
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404, HttpResponse

from static_delivery.middleware import StaticDeliveryMiddleware


def test_invalid_static_url_setting(settings):
    settings.STATIC_URL = 'https://my.cdn.com/static/'
    with pytest.raises(ImproperlyConfigured):
        StaticDeliveryMiddleware(None)

    settings.STATIC_URL = '//my.cdn.com/static/'
    with pytest.raises(ImproperlyConfigured):
        StaticDeliveryMiddleware(None)


def test_invalid_static_storage_setting(settings):
    settings.STATICFILES_STORAGE = (
        'django.contrib.staticfiles.storage.StaticFilesStorage')
    with pytest.raises(ImproperlyConfigured):
        StaticDeliveryMiddleware(None)


class TestMiddlewareCall:

    def setup(self):
        self.middleware = StaticDeliveryMiddleware(
            lambda r: HttpResponse(b'NOSTATIC'))

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
        with pytest.raises(Http404):
            self.middleware(rf.get('/static/notfound.txt'))

    def test_file_hashed(self, rf):
        response = self.middleware(rf.get('/static/test_hash.11aa22bb33cc.jpg'))
        assert response.status_code == 200
        assert response['Content-Type'] == 'image/jpeg'

    def test_file_recovered_hash(self, rf):
        response = self.middleware(rf.get('/static/test_hash.44dd66eee899.jpg'))
        assert response.status_code == 200
        assert response['Content-Type'] == 'image/jpeg'

    def test_file_unrecoverable(self, rf):
        with pytest.raises(Http404):
            self.middleware(rf.get('/static/notfound.44dd66eee899.jpg'))


#
# class TestServeStaticFileMiddlewareWithHashedFiles:
#
#     @pytest.fixture(autouse=True)
#     def setup(self, settings):
#         settings.ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
#         settings.STATIC_ROOT = os.path.join(settings.ROOT_DIR, 'tests', 'resources', 'static')
#         settings.STATICFILES_STORAGE = (
#             'django.contrib.staticfiles.storage.ManifestStaticFilesStorage')
#
#     @pytest.fixture
#     def patch_settings(self, settings):
#         """
#         Patch settings for tests fith django client
#         """
#         settings.STATICFILES_FINDERS = (
#             'django.contrib.staticfiles.finders.FileSystemFinder',
#             'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#             'compressor.finders.CompressorFinder',
#         )
#         settings.MIDDLEWARE_CLASSES = [
#             'barbeque.staticfiles.middleware.ServeStaticFileMiddleware',
#         ]
#         settings.INSTALLED_APPS = settings.INSTALLED_APPS + ('django.contrib.staticfiles',)
#         settings.ROOT_URLCONF = 'barbeque.tests.test_staticfiles'
#
#     def test_unhash_file_name(self):
#         middleware = ServeStaticFileMiddleware()
#         assert middleware.unhash_file_name(
#             '/static/test_hash.11aa22bb33cc.jpg') == ('/static/test_hash.jpg')
#         assert middleware.unhash_file_name('test_hash.jpg') == 'test_hash.jpg'
#         assert middleware.unhash_file_name(
#             'test_hash.11aa22bb33cc.11aa22bb33cc.jpg') == ('test_hash.11aa22bb33cc.jpg')
#         assert middleware.unhash_file_name('test_hash.11aa22bb33cc') == 'test_hash'
#         assert middleware.unhash_file_name('11aa22bb33cc') == '11aa22bb33cc'
#         assert middleware.unhash_file_name('11aa22bb33cc.jpg') == '11aa22bb33cc.jpg'
#         assert middleware.unhash_file_name('.11aa22bb33cc.jpg') == '.11aa22bb33cc.jpg'
#
#     def test_hash_file_exists(self, rf):
#         request = rf.get('/static/test_hash.11aa22bb33cc.jpg')
#         middleware = ServeStaticFileMiddleware()
#         response = middleware.process_response(request, HttpResponseNotFound(''))
#         assert response.status_code == 200
#         assert response['Content-Type'] == 'image/jpeg'
#         assert len(response.items()) == 3
#         assert response.has_header('Content-Length')
#         assert response.has_header('Last-Modified')
#
#     def test_hash_file_original_exists(self, rf):
#         request = rf.get('/static/test_hash.jpg')
#         middleware = ServeStaticFileMiddleware()
#         response = middleware.process_response(request, HttpResponseNotFound(''))
#         assert response.status_code == 200
#         assert response['Content-Type'] == 'image/jpeg'
#         assert len(response.items()) == 3
#         assert response.has_header('Content-Length')
#         assert response.has_header('Last-Modified')
#
#     def test_old_hash(self, rf):
#         request = rf.get('/static/test_hash.44dd55ee66ff.jpg')
#         middleware = ServeStaticFileMiddleware()
#         response = middleware.process_response(request, HttpResponseNotFound(''))
#         assert len(response.items()) == 3
#         assert response.has_header('Content-Length')
#         assert response.has_header('Last-Modified')
#
#     def test_hash_file_exists_with_client_hit(self, client, patch_settings):
#         response = client.get('/static/test_hash.11aa22bb33cc.jpg')
#         assert response.status_code == 200
#
#     def test_hash_file_original_exists_with_client_hit(self, client, patch_settings):
#         response = client.get('/static/test_hash.jpg')
#         assert response.status_code == 200
#
#     def test_hash_old_hash_with_client_hit(self, client, patch_settings):
#         response = client.get('/static/test_hash.44dd55ee66ff.jpg')
#         assert response.status_code == 200
#
#     @mock.patch('django.contrib.staticfiles.storage.ManifestStaticFilesStorage.load_manifest')
#     def test_no_staticfiles_manifest(self, manifest_mock, rf):
#         manifest_mock.return_value = OrderedDict()
#         request = rf.get('/static/test_hash.jpg')
#         middleware = ServeStaticFileMiddleware()
#         response = middleware.process_response(request, HttpResponseNotFound(''))
# assert response.status_code == 404
