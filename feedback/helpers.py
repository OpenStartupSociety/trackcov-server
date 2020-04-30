
def validate_feedback(request):
    fields = ['feedback']
    obj_dic = {}
    keys = request.data.keys()
    for key in keys:
        if key in fields:
            obj_dic[key] = request.data[key]
    return obj_dic
