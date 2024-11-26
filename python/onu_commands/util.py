
def filter_object_attributes(obj, required_attributes = []):
    new_obj = {}

    for item in obj:
        if item in required_attributes:
            new_obj[item] = obj[item]
    
    return new_obj
