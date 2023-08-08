from django.test import TestCase, override_settings


class MultiDomainTestCase(TestCase):
    @override_settings(ALLOWED_HOSTS=["uyenbhku.up.railway.app"])
    def test_other_domain(self):
        response = self.client.get("http://uyenbhku.up.railway.app/")