import json
import redis
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import resolve, reverse
from frejun_api_app.models import Account, PhoneNumber


class TestViews(APITestCase):

    def setUp(self):
        # self.client = APIClient()
        self.inbound_url = reverse('inbound')
        self.account1 = Account.objects.create(
            auth_id="6DLH8A25XZ", username="plivo5")
        self.account2 = Account.objects.create(
            auth_id="54P2EOKQ47", username="plivo2")
        self.ph1 = PhoneNumber.objects.create(
            number="61871112931", account=self.account1)
        self.ph2 = PhoneNumber.objects.create(
            number="61871112939", account=self.account1)
        self.ph3 = PhoneNumber.objects.create(
            number="441224459660", account=self.account2)
        self.ph4 = PhoneNumber.objects.create(
            number="441873440028", account=self.account2)
        self.redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                                port=settings.REDIS_PORT, db=0)
        self.data = {
            "username": self.account1.username,
            "auth_id": self.account1.auth_id,
            "from": "9585644555",
            "to": self.ph1.number,
            "text": "Hello World."
        }

    def test_inbound_fail_if_authenticated_GET(self):
        response = self.client.get(
            reverse('inbound'), self.data, format='json')
        response_json = json.loads(response.content)
        self.assertEquals(response.status_code,
                          status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_inbound_fail_if_authenticated_PUT(self):
        response = self.client.put(
            reverse('inbound'), self.data, format='json')
        response_json = json.loads(response.content)
        self.assertEquals(response.status_code,
                          status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_inbound_fail_if_authenticated_DELETE(self):
        response = self.client.delete(
            reverse('inbound'), self.data, format='json')
        response_json = json.loads(response.content)
        self.assertEquals(response.status_code,
                          status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_inbound_pass_if_authenticated_POST(self):
        response = self.client.post(
            reverse('inbound'), self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_inbound_forbid_if_not_authenticated_POST(self):
        self.data['username'] = 'pilvo'
        response = self.client.post(
            reverse('inbound'), self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_inbound_from_missing_POST(self):
        del self.data['from']
        response = self.client.post(
            reverse('inbound'), self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'message': '', 'error': 'from is missing'})

    def test_inbound_to_missing_POST(self):
        del self.data['to']
        response = self.client.post(
            reverse('inbound'), self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'message': '', 'error': 'to is missing'})

    def test_inbound_text_missing_POST(self):
        del self.data['text']
        response = self.client.post(
            reverse('inbound'), self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'message': '', 'error': 'text is missing'})

    def test_inbound_from_invalid_length_small_POST(self):
        self.data['from'] = '45'
        response = self.client.post(
            reverse('inbound'), self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'message': '', 'error': 'from is invalid'})

    def test_inbound_from_invalid_length_large_POST(self):
        temp_num = '5'*17
        self.data['from'] = temp_num
        response = self.client.post(
            reverse('inbound'), self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'message': '', 'error': 'from is invalid'})

    def test_inbound_to_invalid_length_small_POST(self):
        self.data['to'] = '25'
        response = self.client.post(
            reverse('inbound'), self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'message': '', 'error': 'to is invalid'})

    def test_inbound_to_invalid_length_large_POST(self):
        temp_num = '9'*17
        self.data['to'] = temp_num
        response = self.client.post(
            reverse('inbound'), self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'message': '', 'error': 'to is invalid'})

    def test_inbound_text_invalid_length_small_POST(self):
        self.data['text'] = ''
        response = self.client.post(
            reverse('inbound'), self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'message': '', 'error': 'text is invalid'})

    def test_inbound_text_invalid_length_large_POST(self):
        test_text_data = 'x'*121
        self.data['text'] = test_text_data
        response = self.client.post(
            reverse('inbound'), self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'message': '', 'error': 'text is invalid'})

    def test_inbound_to_parameter_not_found_POST(self):
        self.data['to'] = '8596214589'
        response = self.client.post(
            reverse('inbound'), self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'message': '', 'error': 'to parameter not found'})

    def test_inbound_all_parameters_valid_POST_and_text_is_not_STOP_POST(self):
        self.data['from'] = '58462452684'
        self.entry = f"{self.data['from']} | {self.data['to']}"
        response = self.client.post(
            reverse('inbound'), self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'message': 'inbound sms ok', 'error': ''})
        self.assertFalse(self.redis_instance.get(self.entry))

    def test_inbound_all_parameters_valid_and_text_is_STOP_Uppercase_POST(self):
        self.data['text'] = "STOP"
        response = self.client.post(
            reverse('inbound'), self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'message': 'inbound sms ok', 'error': ''})
        self.entry = f"{self.data['from']} | {self.data['to']}"
        self.assertTrue(self.redis_instance.get(self.entry))

    def test_inbound_all_parameters_valid_and_text_is_STOP_lowercase_POST(self):
        self.data['text'] = "stop"
        response = self.client.post(
            reverse('inbound'), self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'message': 'inbound sms ok', 'error': ''})
        self.entry = f"{self.data['from']} | {self.data['to']}"
        self.assertTrue(self.redis_instance.get(self.entry))

    def test_inbound_all_parameters_valid_and_text_is_STOP_with_ending_spaces_and_returns_POST(self):
        self.data['text'] = "STOP\r\n"
        response = self.client.post(
            reverse('inbound'), self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'message': 'inbound sms ok', 'error': ''})
        self.entry = f"{self.data['from']} | {self.data['to']}"
        self.assertTrue(self.redis_instance.get(self.entry))
