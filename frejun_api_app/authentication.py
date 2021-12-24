from rest_framework import authentication
from rest_framework import exceptions
from .models import Account


class AccountAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.data.get('username', None)
        auth_id = request.data.get('auth_id', None)

        if not username or not auth_id:
            return None

        try:
            user = Account.objects.get(
                username=username, auth_id=auth_id)  # get the user
        except Account.DoesNotExist:
            # raise exception if user does not exist
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)  # authentication successful
