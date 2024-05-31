def is_list_of_dicts(obj):
    return isinstance(obj, list) and all(isinstance(element, dict) for element in obj)
