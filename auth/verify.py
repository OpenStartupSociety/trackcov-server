import logging

import jwt
from firebase_admin import auth, exceptions as f_exception
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from track_cov.settings import google_project_id
from django.utils.translation import ugettext as _
from rest_framework.permissions import BasePermission
from firebase_admin import firestore

from core.constants import ResponseCode
from .token import token_decode

logger = logging.getLogger(__name__)


class IdTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        """
                Returns a two-tuple of `User` and token if a valid signature has been
                supplied using JWT-based authentication.  Otherwise returns `None`.
                """
        self.jwt_token = self.get_token_from_header(request)
        if self.jwt_token is None:
            return None

        try:
            payload = token_decode(self.jwt_token)
            user = self.verify_user(payload)
            return user, self.jwt_token
        except jwt.ExpiredSignature:
            # if request.META.get('PATH_INFO', None) == '/refresh-token/':
            #     jwt_token = jwe_decode_handler(self.jwe_token)
            #     payload = jwt_decode_handler(jwt_token, {'verify_exp': False, })
            #     auth_user = self.verify_user(payload)
            #     jwt_payload = generate_jwt_payload(request, auth_user)
            #     ref_jwt_token = jwt_encode_handler(jwt_payload)
            #     ref_jwe_token = jwe_encode_handler(ref_jwt_token)
            #     return auth_user, ref_jwe_token
            logger.info({
                'token': self.jwt_token,
                'message': 'Token has expired.',
                'code': 401,
            })
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            logger.exception({
                'token': self.jwt_token,
                'message': 'DecodeError on jwt token.',
                'code': 406,
            })
            msg = _('Error decoding signature.')
            raise exceptions.NotAcceptable(msg)
        except jwt.InvalidTokenError:
            logger.exception({
                'token': self.jwt_token,
                'message': 'InvalidTokenError on jwt token.',
                'code': 406,
            })
            raise exceptions.NotAcceptable()
        except Exception as err:
            msg = ('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)

    def verify_user(self, payload):
        db = firestore.client()
        doc_ref = db.collection('profile').document(payload['user_id'])
        doc_ref = doc_ref.get()
        if doc_ref.exists:
            user_obj = doc_ref.to_dict()
            return {'user_id': user_obj['user_id'], 'phone_number': user_obj['phone_number']}
        return None

    def get_token_from_header(self, request):
        auth = get_authorization_header(request).split()
        if not auth:
            return None

        elif len(auth) > 1:
            logger.exception({
                'token': self.jwe_token,
                'message': 'Authorization header contains spaces.',
                'code': 403,
            })
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.PermissionDenied(msg)

        return auth[0].decode('utf-8')


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user)


def verify_google(id_token):
    db = firestore.client()
    decoded_token = auth.verify_id_token(id_token)
    print(decoded_token)
    data = {
        'user_id': decoded_token['user_id'],
        'phone_number': decoded_token['phone_number'],
        'name': decoded_token['name']
    }
    if decoded_token['aud'] == google_project_id:
        doc_ref = db.collection('profile').document(decoded_token['user_id'])
        user_obj = doc_ref.get()
        if user_obj.exists:
            pass
        else:
            doc_ref.set(data)
        return data
    else:
        None
