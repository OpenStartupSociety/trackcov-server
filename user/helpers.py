from datetime import date


def validate_daily_symptoms(request):
    fields = ['q_code', 'ans', 'date', 'user']
    validated_data = []
    if type(request.data) is list:
        for obj in request.data:
            obj_dic = {}
            keys = obj.keys()
            for key in keys:
                if key in fields:
                    obj_dic[key] = obj[key]
            validated_data.append(obj_dic)
        return validated_data
    else:
        obj_dic = {}
        keys = request.data.keys()
        for key in keys:
            if key in fields:
                obj_dic[key] = request.data[key]
        return obj_dic


def validate_health_profile(request):
    fields = ['q_code', 'ans', 'date', 'user']
    validated_data = []
    if type(request.data) is list:
        for obj in request.data:
            obj_dic = {}
            keys = obj.keys()
            for key in keys:
                if key in fields:
                    obj_dic[key] = obj[key]
            validated_data.append(obj_dic)
        return validated_data
    else:
        obj_dic = {}
        keys = request.data.keys()
        for key in keys:
            if key in fields:
                obj_dic[key] = request.data[key]
        return obj_dic


