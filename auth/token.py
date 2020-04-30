import datetime
import jwt
import logging
from django.utils import timezone
# from jwcrypto import jwe, jwk
# from jwcrypto.common import json_encode
from rest_framework import exceptions
from django.utils.translation import ugettext as _

from track_cov import settings
from .constraints import JWT_DEFAULTS, JWE_DEFAULTS

logger = logging.getLogger(__name__)


def jwt_encode_handler(payload):
    key = settings.jwt_secret
    return jwt.encode(
        payload,
        key,
        JWT_DEFAULTS['JWT_ALGORITHM']
    ).decode('utf-8')


def jwt_decode_handler(token, options=None):
    if options is None:
        options = {
         'verify_exp': JWT_DEFAULTS['JWT_VERIFY_EXPIRATION'],
        }
    secret_key = settings.jwt_secret
    return jwt.decode(
        token,
        secret_key,
        options=options,
        leeway=JWT_DEFAULTS['JWT_LEEWAY'],
        audience=JWT_DEFAULTS['JWT_AUDIENCE'],
        issuer=JWT_DEFAULTS['JWT_ISSUER'],
        algorithms=[JWT_DEFAULTS['JWT_ALGORITHM']]
    )


def generate_jwt_payload(user):
    payload = {
        'user_id': user['user_id'],
        'iss': JWT_DEFAULTS['JWT_ISSUER'],
        'iat': timezone.localtime(),
        'exp': timezone.localtime() + datetime.timedelta(days=14)
    }
    return payload


# def jwe_encode_handler(payload):
#     key = jwk.JWK(**{
#         'k': settings.jwe_secret,
#         'kty': JWE_DEFAULTS['JWE_KEY_TYPE'],
#     })
#     jwe_token = jwe.JWE(payload.encode('utf-8'), json_encode({
#         "alg": JWE_DEFAULTS['JWE_ALGORITHM'],
#         "enc": JWE_DEFAULTS['JWE_ENCODER']
#     }))
#     jwe_token.add_recipient(key)
#     token = jwe_token.serialize('json')
#     return token


# def jwe_decode_handler(token):
#
#     key = jwk.JWK(**{
#         'k': settings.jwe_secret,
#         'kty': JWE_DEFAULTS['JWE_KEY_TYPE'],
#     })
#     jwe_token = jwe.JWE()
#     jwe_token.deserialize(token)
#     jwe_token.decrypt(key)
#     return jwe_token.payload


def token_encode(user):
    payload = generate_jwt_payload(user)
    jwt_token = jwt_encode_handler(payload)
    # jwe_token = jwe_encode_handler(jwt_token)
    return jwt_token


def token_decode(token):
    # jwt_token = jwe_decode_handler(token)
    payload = jwt_decode_handler(token)
    return payload
