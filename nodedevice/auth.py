from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from django.utils.translation import gettext_lazy as _

from db.models import NodeDevice


class NodeTokenAuth(BaseAuthentication):
    keyword = "Token"

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            msg = _('No token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)

        if len(auth) <= 2:
            msg = _('Invalid token header. Credentials missing.')
            raise exceptions.AuthenticationFailed(msg)

        elif len(auth) > 3:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
            token_id = auth[2].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token, token_id)

    @staticmethod
    def authenticate_credentials(key, key_id):
        try:
            token = NodeDevice.objects.get(token=key)
        except NodeDevice.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if int(token.id) != int(key_id):
            raise exceptions.AuthenticationFailed(_('Invalid user or stolen token!.'))

        return token, None
