import json
import requests
from django.test import SimpleTestCase
from django.urls import resolve, reverse
from frejun_api_app.views import inbound


class TestViews(SimpleTestCase):
    """
    def setUp(self):
        self.client = Client()
        self.inbound_url = reverse('inbound')
        self.account1 = Account.objects.create(auth_id="6DLH8A25XZ", username="plivo5")
        self.account2 = Account.objects.create(auth_id="54P2EOKQ47", username="plivo2")
        self.ph1 = PhoneNumber.objects.create(number="61871112931", account=self.account1)
        self.ph2 = PhoneNumber.objects.create(number="61871112939", account=self.account1)
        self.ph3 = PhoneNumber.objects.create(number="441224459660", account=self.account2)
        self.ph4 = PhoneNumber.objects.create(number="441873440028", account=self.account2)
    """

    def test_outbound_fail_if_not_authenticated_POST(self):
        data = {
            "username": "pliv5",
            "auth_id": "6DLH8A25XZ",
            "from": "9528631470",
            "to": "61871112939",
            "text": "STOP\r\n"

        }
        inbound_url = 'http://localhost:8000/api/outbound/sms'
        response = requests.post(inbound_url, json=data)
        self.assertEquals(response.status_code, 403)

    def test_outbound_pass_if_authenticated_POST(self):
        data = {
            "username": "plivo5",
            "auth_id": "6DLH8A25XZ",
            "from": "9528631470",
            "to": "61871112939",
            "text": "STOP\r\n"

        }
        inbound_url = 'http://localhost:8000/api/outbound/sms'
        response = requests.post(inbound_url, json=data)
        self.assertEquals(response.status_code, 200)

    def test_outbound_fail_if_method_is_GET(self):
        data = {
            "username": "plivo5",
            "auth_id": "6DLH8A25XZ",
            "from": "9528631470",
            "to": "61871112939",
            "text": "STOP\r\n"

        }
        inbound_url = 'http://localhost:8000/api/outbound/sms'
        response = requests.get(inbound_url, json=data)
        self.assertEquals(response.status_code, 405)

    def test_outbound_fail_if_method_is_PUT(self):
        data = {
            "username": "plivo5",
            "auth_id": "6DLH8A25XZ",
            "from": "9528631470",
            "to": "61871112939",
            "text": "STOP\r\n"

        }
        inbound_url = 'http://localhost:8000/api/outbound/sms'
        response = requests.put(inbound_url, json=data)
        self.assertEquals(response.status_code, 405)

    def test_outbound_fail_if_method_is_DELETE(self):
        data = {
            "username": "plivo5",
            "auth_id": "6DLH8A25XZ",
            "from": "9528631470",
            "to": "61871112939",
            "text": "STOP\r\n"

        }
        inbound_url = 'http://localhost:8000/api/outbound/sms'
        response = requests.delete(inbound_url, json=data)
        self.assertEquals(response.status_code, 405)

    def test_outbound_from_missing_POST(self):
        data = {
            "username": "plivo5",
            "auth_id": "6DLH8A25XZ",
            "to": "61871112939",
            "text": "STOP\r\n"

        }
        inbound_url = 'http://localhost:8000/api/outbound/sms'
        response = requests.post(inbound_url, json=data)
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
                             "message": "", "error": "from is missing"})

    def test_outbound_to_missing_POST(self):
        data = {
            "username": "plivo5",
            "auth_id": "6DLH8A25XZ",
            "from": "61871112939",
            "text": "STOP\r\n"

        }
        inbound_url = 'http://localhost:8000/api/outbound/sms'
        response = requests.post(inbound_url, json=data)
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
                             "message": "", "error": "to is missing"})

    def test_outbound_text_missing_POST(self):
        data = {
            "username": "plivo5",
            "auth_id": "6DLH8A25XZ",
            "from": "9528631470",
            "to": "61871112939",
        }
        inbound_url = 'http://localhost:8000/api/outbound/sms'
        response = requests.post(inbound_url, json=data)
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
                             "message": "", "error": "text is missing"})

    def test_outbound_from_invalid_length_small_POST(self):
        data = {
            "username": "plivo5",
            "auth_id": "6DLH8A25XZ",
            "from": "42",
            "to": "61871112939",
            "text": "STOP\r\n"

        }
        inbound_url = 'http://localhost:8000/api/outbound/sms'
        response = requests.post(inbound_url, json=data)
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
                             "message": "", "error": "from is invalid"})

    def test_outbound_from_invalid_length_large_POST(self):
        data = {
            "username": "plivo5",
            "auth_id": "6DLH8A25XZ",
            "from": "4244546464684654464484646465464",
            "to": "61871112939",
            "text": "STOP\r\n"

        }
        inbound_url = 'http://localhost:8000/api/outbound/sms'
        response = requests.post(inbound_url, json=data)
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
                             "message": "", "error": "from is invalid"})

    def test_outbound_to_invalid_length_small_POST(self):
        data = {
            "username": "plivo5",
            "auth_id": "6DLH8A25XZ",
            "from": "4244546456",
            "to": "6",
            "text": "STOP\r\n"

        }
        inbound_url = 'http://localhost:8000/api/outbound/sms'
        response = requests.post(inbound_url, json=data)
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
                             "message": "", "error": "to is invalid"})

    def test_outbound_to_invalid_length_large_POST(self):
        data = {
            "username": "plivo5",
            "auth_id": "6DLH8A25XZ",
            "from": "4244546456",
            "to": "6455546813184943315489",
            "text": "STOP\r\n"

        }
        inbound_url = 'http://localhost:8000/api/outbound/sms'
        response = requests.post(inbound_url, json=data)
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
                             "message": "", "error": "to is invalid"})

    def test_outbound_text_invalid_length_small_POST(self):
        data = {
            "username": "plivo5",
            "auth_id": "6DLH8A25XZ",
            "from": "4244546456",
            "to": "645554689",
            "text": ""

        }
        inbound_url = 'http://localhost:8000/api/outbound/sms'
        response = requests.post(inbound_url, json=data)
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
                             "message": "", "error": "text is invalid"})

    def test_outbound_text_invalid_length_large_POST(self):
        test_text_data = 'x'*121
        data = {
            "username": "plivo5",
            "auth_id": "6DLH8A25XZ",
            "from": "4244546456",
            "to": "645554689",
            "text": test_text_data

        }
        inbound_url = 'http://localhost:8000/api/outbound/sms'
        response = requests.post(inbound_url, json=data)
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
                             "message": "", "error": "text is invalid"})

    def test_outbound_from_parameter_not_found_POST(self):
        data = {
            "username": "plivo5",
            "auth_id": "6DLH8A25XZ",
            "from": "645554689",
            "to": "5625654686",
            "text": "Hello World!"

        }
        inbound_url = 'http://localhost:8000/api/outbound/sms'
        response = requests.post(inbound_url, json=data)
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
                             "message": "", "error": "from parameter not found"})
