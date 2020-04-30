import enum


class ResponseCode(enum.Enum):
    bad_request = 400
    created = 201
    ok = 200
    user_not_found = 704
    user_exists = 705
    method_not_allowed = 405
    not_acceptable = 406
    unauthorized = 401
    forbidden = 403
    package_expired = 1002
    payment_required = 402


class MessageStrings(enum.Enum):
    success = "Success"
    registration_id_req = 'registration_id field required'
    registration_id_blank = 'registration_id field should not be blank'
    device_id_req = 'device_id field required'
    device_id_blank = 'device_id field should not be blank'
    device_updated_successfully = 'Device updated successfully'
    date_of_birth_req = 'date_of_birth field required'
    name_req = 'name field required'
    some_thing_went_wrong = "Something went wrong"
    profile_added = "Profile added successfully"
    profile_updated = "Profile updated successfully"
    must_contain_one_field = "Please provide at least one field"
    symptoms_added = "Daily Symptoms added successfully"
    symptoms_updated = "Daily Symptoms updated successfully"
    health_profile_added = "Health profile added successfully"
    health_profile_updated = "Health profile updated successfully"


class DailySymptomsQuestionCodes(enum.Enum):
    dq01 = {'code': 'DQ01', 'q': 'Have you had a COVID-19 test?'}
    dq02 = {'code': 'DQ02', 'q': 'Has anyone in your family undergone COVID-19 test?'}
    dq03 = {'code': 'DQ03', 'q': 'How do you feel right now? (Feeling normal OR Not feeling normal)'}
    dq04 = {'code': 'DQ04', 'q': 'Do you have any of the following symptoms today?'}
    dq05 = {'code': 'DQ05', 'q': 'Did you travel outside home/current residence yesterday?'}
    dq06 = {'code': 'DQ06', 'q': 'Is your local area safe i.e. no COVID-19 positive patients identified?'}


class HealthProfileQuestionCodes(enum.Enum):
    hq01 = {'code': 'HQ01', 'q': 'Do you have any health problems that require you to limit movement and activity?'}
    hq02 = {'code': 'HQ02', 'q': 'Do you suffer from any of the following heath conditions (multiple selection options)'}
    hq03 = {'code': 'HQ03', 'q': 'Do you take any immunosupressants taken after transplant (e.g. steroids, methotrexate, other)'}
    hq04 = {'code': 'HQ04', 'q': 'Do you regularly take Nonsteroidal anti-inflammatory drugs (NSAIDs) taken for inflammation associated conditions such as arthritis, tendonitis, and bursitis etc.'}
    hq05 = {'code': 'HQ05', 'q': 'Do you regularly take blood pressure medications (e.g. enapril, ramipril, other) (Yes/ No)'}
    hq06 = {'code': 'HQ06', 'q': 'Do you have any health conditions that restrict you from staying at home? (Yes/No)'}
    hq07 = {'code': 'HQ07', 'q': 'Do you use a stick, wheelchair or other assistive devices? (Yes/No)'}
    hq08 = {'code': 'HQ08', 'q': 'How many people in your family or apartment?'}
    hq09 = {'code': 'HQ09', 'q': 'Do you think you already had COVID-19, but were not tested? (Yes/No)'}
    hq10 = {'code': 'HQ10', 'q': 'Have you or anyone in your family travelled abroad in last 14 days? (Yes/No)'}
    hq11 = {'code': 'HQ11', 'q': 'Is yes which country (China, Italy, Spain, UK, USA, Middle East, East Asia, Other)'}
    hq12 = {'code': 'HQ12', 'q': 'Have you or someone in your family been in close contact with a confirmed COVID-19 patient within last 14 days? (Yes/No)'}
    hq13 = {'code': 'HQ13', 'q': 'Have you or someone in your family been in close contact with someone having cough, cold, fever and shortness of breathe within last 14 days?'}


class NotificationMessages(enum.Enum):
    positive_detected = {
        'title': 'TrackCov',
        'description': 'Positive COVID-19 patient found near by you',
        'code': '999'
    }
    silent_notification = {
        'code': '1001'
    }
