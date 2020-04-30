import logging
from datetime import date

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from firebase_admin import firestore
from google.cloud import exceptions as gexceptions

from auth.token import token_encode
from auth.verify import verify_google
from core.constants import ResponseCode, MessageStrings
from core.utils import validate_date
from user.helpers import validate_daily_symptoms, validate_health_profile

db = firestore.client()

logger = logging.getLogger(__name__)


class UserProfile(APIView):

    @staticmethod
    def get(request):
        try:
            doc_ref = db.collection('profile').document(request.user['user_id'])
            doc_ref = doc_ref.get()
            return Response({
                'data': doc_ref.to_dict(),
                'message': 'Success',
                'code': ResponseCode.ok.value
            }, status=status.HTTP_200_OK)
        except gexceptions.NotFound:
            return Response({
                'data': {},
                'message': 'Success',
                'code': ResponseCode.ok.value
            }, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        try:
            doc_ref = db.collection('profile').document(request.user['user_id'])
            user_obj = {}
            if 'date_of_birth' in request.data:
                try:
                    validate_date(request.data['date_of_birth'])
                    user_obj['date_of_birth'] = request.data['date_of_birth']
                except ValueError as err:
                    return Response({
                        'data': "Failed",
                        'message': err.args,
                        'code': ResponseCode.bad_request.value
                    }, status=status.HTTP_400_BAD_REQUEST)
            if 'name' in request.data:
                if request.data['name'].strip() == "":
                    return Response({
                        'data': "Failed",
                        'message': MessageStrings.name_blank.value,
                        'code': ResponseCode.bad_request.value
                    }, status=status.HTTP_400_BAD_REQUEST)
                user_obj['name'] = request.data['name']
            if 'gender' in request.data:
                if request.data['gender'] and request.data['gender'] in [1, 2, 3]:
                    user_obj['gender'] = request.data['gender']
            if 'height' in request.data:
                user_obj['height'] = request.data['height']
            if 'weight' in request.data:
                user_obj['weight'] = request.data['weight']
            if user_obj:
                user_obj['phone_number'] = request.data['phone_number']
                doc_ref.update(user_obj)
                return Response({
                    'data': "Success",
                    'message': MessageStrings.profile_added.value,
                    'code': ResponseCode.created.value
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'data': "Failed",
                    'message': MessageStrings.must_contain_one_field.value,
                    'code': ResponseCode.bad_request.value
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:

            logger.info({
                'error': err
            })
            return Response({
                'data': "Failed",
                'message': MessageStrings.some_thing_went_wrong.value,
                'code': ResponseCode.bad_request.value
            }, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request):
        try:
            doc_ref = db.collection('profile').document(request.user['user_id'])
            user_obj = {}
            if 'date_of_birth' in request.data:
                try:
                    validate_date(request.data['date_of_birth'])
                    user_obj['date_of_birth'] = request.data['date_of_birth']
                except ValueError as err:

                    print(err)
                    return Response({
                        'data': "Failed",
                        'message': err.args,
                        'code': ResponseCode.bad_request.value
                    })
            if 'name' in request.data:
                if request.data['name'].strip() == "":
                    return Response({
                        'data': "Failed",
                        'message': MessageStrings.name_req.value,
                        'code': ResponseCode.bad_request.value
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user_obj['name'] = request.data['name']
            if 'gender' in request.data:
                if request.data['gender'] and int(request.data['gender']) in [1, 2, 3]:
                    user_obj['gender'] = request.data['gender']
            if 'height' in request.data:
                user_obj['height'] = request.data['height']
            if 'weight' in request.data:
                user_obj['weight'] = request.data['weight']
            if user_obj:
                doc_ref.update(user_obj)
                return Response({
                    'data': "Success",
                    'message': MessageStrings.profile_updated.value,
                    'code': ResponseCode.created.value
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'data': "Failed",
                    'message': MessageStrings.must_contain_one_field.value,
                    'code': ResponseCode.bad_request.value
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(err)
            logger.info({
                'error': err
            })
            return Response({
                'data': "Failed",
                'message': MessageStrings.some_thing_went_wrong.value,
                'code': ResponseCode.bad_request.value
            }, status=status.HTTP_400_BAD_REQUEST)


class DailySymptomsTracker(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        doc_ref = db.collection('daily_symptoms')
        result_obj = []
        query = doc_ref.where(
            'user_id', '==', request.user['user_id']
        )
        d_obj = query.get()
        for doc in d_obj:
            result_obj.append(doc.to_dict())
        return Response(
            {
                'data': result_obj,
                'message': MessageStrings.success.value,
                'code': ResponseCode.ok.value
            }, status=status.HTTP_200_OK
        )

    @staticmethod
    def post(request):
        validate_data = validate_daily_symptoms(request)
        doc_ref = db.collection('daily_symptoms')
        query = doc_ref.where(
            'user_id', '==', request.user['user_id']
        ).where('date', '==', date.today().strftime('%d-%m-%Y'))
        d_obj = query.get()
        for doc in d_obj:
            if doc.exists:
                doc_ref.document(doc.id).update({'symptoms': validate_data})
                return Response({
                    'code': ResponseCode.ok.value,
                    'message': MessageStrings.symptoms_updated.value,
                    'data': {'result': 1}
                })

        doc_ref.document().set(
            {
                'symptoms': validate_data,
                'date': date.today().strftime('%d-%m-%Y'),
                'user_id': request.user['user_id']
            }, merge=True
        )
        return Response({
            'data': {'result': 1},
            'message': MessageStrings.symptoms_added.value,
            'code': ResponseCode.created.value
        }, status=status.HTTP_201_CREATED)


class HealthProfile(APIView):

    def get(self, request):
        doc_ref = db.collection('health_profile').document(request.user['user_id'])
        d_obj = doc_ref.get()

        return Response(
            {
                'data': d_obj.to_dict(),
                'message': MessageStrings.success.value,
                'code': ResponseCode.ok.value
            }, status=status.HTTP_200_OK
        )

    @staticmethod
    def post(request):
        validate_data = validate_health_profile(request)
        doc_ref = db.collection('health_profile').document(request.user['user_id'])

        doc_ref.set(
            {
                'health_profile': validate_data,
                'date': date.today().strftime('%d-%m-%Y'),
                'user_id': request.user['user_id']
            }, merge=True
        )
        return Response({
            'data': 'Success',
            'message': MessageStrings.health_profile_added.value,
            'code': ResponseCode.created.value
        }, status=status.HTTP_201_CREATED)

    @staticmethod
    def put(request):
        validate_data = validate_health_profile(request)
        doc_ref = db.collection('health_profile').document(request.user['user_id'])

        doc_ref.update(
            {
                'health': validate_data,
                'update_date': date.today().strftime('%d-%m-%Y'),
            }
        )
        return Response({
            'data': 'Success',
            'message': MessageStrings.health_profile_updated.value,
            'code': ResponseCode.ok.value
        }, status=status.HTTP_200_OK)


class Login(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        user = verify_google(request.data['token'])
        token = token_encode(user)
        health_profile_ref = db.collection('health_profile').document(user['user_id'])
        health_profile_obj = health_profile_ref.get()
        if health_profile_obj.exists:
            is_health_profile = True
        else:
            is_health_profile = False
        return Response({
            'data': {'token': token, 'is_health_profile': is_health_profile},
            'message': MessageStrings.success.value,
            'code': ResponseCode.ok.value
        }, status=status.HTTP_200_OK)
