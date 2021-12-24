import redis
from datetime import timedelta
from django.core.cache import cache
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from .models import PhoneNumber, Account
from rest_framework.decorators import api_view
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .serializers import AccountSerializer
# Create your views here.

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)


def index(request):
    return HttpResponse("<h2>Welcome to FreJun API</h2>")


def data_validation(input_param, txt: str) -> dict:
    """Validation code for the input parameters."""
    data_dictionary = {'message': '', 'error': ''}
    if input_param is None:  # checks if input_param is None
        data_dictionary['error'] = txt + ' is missing'
    else:   # check the length of strings
        if txt == 'text':
            if len(input_param) not in range(1, 121):
                data_dictionary['error'] = txt + ' is invalid'
        else:
            if len(input_param) not in range(6, 17):
                data_dictionary['error'] = txt + ' is invalid'

    return data_dictionary


@csrf_exempt
@api_view(['POST'])
def inbound(request):
    if request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            account = data.get('username')
            frm = data.get('from', None)
            to = data.get('to', None)
            text = data.get('text', None)
            input_params_list = [(frm, 'from'), (to, 'to'), (text, 'text')]
            # Looping through the parameters
            for k, v in input_params_list:
                res_dict = data_validation(k, v)
                if res_dict['error'] != '':
                    return Response(res_dict)

            # Checking if "to" is present in PhoneNumber model for this account
            try:
                account_id = Account.objects.get(username=account)
                ph = PhoneNumber.objects.get(account=account_id, number=to)
            except PhoneNumber.DoesNotExist:
                return Response({'message': '', 'error': 'to parameter not found'})

            # Caching the from and to pair for 4 hours if text is STOP
            if text.strip() == 'STOP':
                entry = f"{frm} | {to}"
                # put into cache and expires in 4 hours
                redis_instance.set(entry, entry, timedelta(hours=4))
                print(f"STORE FROM/TO PAIR [{entry}] TO CACHE WITH EXPIRY = 4 HRS")

            return Response({'message': 'inbound sms ok', 'error': ''}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@csrf_exempt
@api_view(['POST'])
def outbound(request):
    if request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            account = data.get('username')
            frm = data.get('from', None)
            to = data.get('to', None)
            text = data.get('text', None)
            input_params_list = [(frm, 'from'), (to, 'to'), (text, 'text')]
            # Looping through the parameters
            for k, v in input_params_list:
                res_dict = data_validation(k, v)
                if res_dict['error'] != '':
                    return Response(res_dict)

            # Checking if "from" is present in PhoneNumber model for this account
            try:
                account_id = Account.objects.get(username=account)
                ph = PhoneNumber.objects.get(account=account_id, number=frm)
            except PhoneNumber.DoesNotExist:
                return Response({'message': '', 'error': 'from parameter not found'})

            # Block SMS
            entry = f"{to} | {frm}"
            if redis_instance.get(entry):
                print("FETCHING TO/FROM [{entry}] PAIR DATA FROM CACHE.")
                error_msg = f"sms from {frm} to {to} blocked by STOP request"
                return Response({'message': '', 'error': error_msg})

            # API Ratelimiting to 50 requests from <from>
            if redis_instance.hget(frm, 'quota'):  # If frm is already present
                print(f"FETCHING THE API QUOTA LIMIT FOR {frm}")
                quota = int(redis_instance.hget(frm, 'quota'))
                if quota < 1:
                    error_msg = f"limit reached for from {frm}"
                    return Response({'message': '', 'error': error_msg})
                else:   # Decrementing the quota
                    quota -= 1
                    redis_instance.hset(frm, 'quota', quota)

            else:   # If frm is not already present - Set the key to frm and quota to 50
                redis_instance.hset(frm, 'quota', 50)
                print("STORING THE FROM: {frm} AND QUOTA TO 50.")
                # expire the key after 24 hours
                redis_instance.expire(frm, timedelta(days=1))
                print("SETTING THE EXPIRY OF FROM: {frm} TO 24 HOURS.")

            return Response({'message': 'outbound sms ok', 'error': ''}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
