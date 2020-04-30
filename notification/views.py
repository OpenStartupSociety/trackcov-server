from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from firebase_admin import firestore

from core.constants import ResponseCode, MessageStrings, NotificationMessages
from notification.helper import send_notification

db = firestore.client()


class Device(APIView):

    @staticmethod
    def get(request):
        # users_ref = db.collection(u'users')
        # docs = users_ref.stream()
        # for doc in docs:
        #     print(u'{} => {}'.format(doc.id, doc.to_dict()))

        doc_ref = db.collection('fcm_device').document(request.user['user_id'])
        doc_ref.get()
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        doc_ref = db.collection('fcm_device').document(request.user['user_id'])
        if 'registration_id' not in request.data:
            return Response({
                'data': "Failed",
                'message': MessageStrings.registration_id_req.value,
                'code': ResponseCode.bad_request.value
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.data['registration_id'].strip() == '' or not request.data['registration_id']:
                return Response({
                    'data': "Failed",
                    'message': MessageStrings.registration_id_blank.value,
                    'code': ResponseCode.bad_request.value
                }, status=status.HTTP_400_BAD_REQUEST)
        if 'device_id' not in request.data:
            return Response({
                'data': "Failed",
                'message': MessageStrings.device_id_req.value,
                'code': ResponseCode.bad_request.value
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.data['device_id'].strip() == '' or not request.data['device_id']:
                return Response({
                    'data': "Failed",
                    'message': MessageStrings.device_id_blank.value,
                    'code': ResponseCode.bad_request.value
                }, status=status.HTTP_400_BAD_REQUEST)
        doc_ref.set({
            'registration_id': request.data['registration_id'],
            'device_id': request.data['device_id'],
            'user_id': request.user['user_id']
        })
        return Response({
            'data': "Success",
            'message': MessageStrings.device_updated_successfully.value,
            'code': ResponseCode.created.value
        }, status=status.HTTP_201_CREATED)


class NotifyUsers(APIView):

    @staticmethod
    def post(request):
        user_devices = []
        print(request.data)
        for user in request.data['users']:
            doc_ref = db.collection('fcm_device').document(user)
            user_obj = doc_ref.get().to_dict()
            user_devices.append(user_obj['registration_id'])
        send_notification(user_devices, NotificationMessages.positive_detected.value)
        doc_ref = db.collection('notification_log').document()
        doc_ref.set({
            'sent_to': request.data['users'],
            'date': datetime.today().strftime('%d-%m-%Y, %H:%M:%S'),
            'user_id': request.user['user_id']
        })
        return Response({
            'data': "Success",
            'code': ResponseCode.ok.value,
            'message': MessageStrings.success.value
        }, status=status.HTTP_200_OK)


class ReportPositiveUser(APIView):

    def post(self, request, format=None):
        doc_ref = db.collection('profile')
        query = doc_ref.where(
            'phone_number', '==', request.data['phone_number']
        )
        user_obj = query.get()

        for user in user_obj:
            user_update_ref = db.collection('profile').document(user.id)
            user_update_ref.update({'is_positive': True})
            fcm_ref = db.collection('fcm_device').document(user.id)
            fcm_obj = fcm_ref.get().to_dict()
            send_notification(fcm_obj['registration_id'], NotificationMessages.silent_notification.value)
        return Response(status=status.HTTP_200_OK)
