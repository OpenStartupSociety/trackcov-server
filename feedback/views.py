import logging
from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from firebase_admin import firestore

from core.constants import MessageStrings, ResponseCode
from .helpers import validate_feedback

db = firestore.client()


class Feedback(APIView):
    def get(self, request, format=None):
        pass

    @staticmethod
    def post(request):
        doc_ref = db.collection('feedback').document()
        validated_data = validate_feedback(request)
        validated_data['user_id'] = request.user['user_id']
        print(datetime.today().strftime('%d-%m-%Y, %H:%M:%S'))
        validated_data['created_at'] = datetime.today().strftime('%d-%m-%Y, %H:%M:%S')
        doc_ref.set(validated_data)
        return Response({
            'message': MessageStrings.success.value, 'code': ResponseCode.created.value,
            'data': MessageStrings.success.value
        }, status=status.HTTP_201_CREATED)