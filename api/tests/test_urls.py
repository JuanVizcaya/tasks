from django.test import TestCase

class URLTests(TestCase):
    """  Test unitarios para URLS """
    def test_homepage(self):
        """ Test URL Principal:
        a) Prueba que la url principal redireccione hacia el panel de administración.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)