from pyfcm import FCMNotification
from track_cov.settings import fcm_server_key


def send_notification(devices, data):
    push_service = FCMNotification(api_key=fcm_server_key)
    if type(devices) == list:
        # To multiple devices
        result = push_service.notify_multiple_devices(registration_ids=devices, data_message=data)
    else:
        # To a single device
        result = push_service.notify_single_device(registration_id=devices, data_message=data)
