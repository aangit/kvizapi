def contains_object_with(object_list, key, target_id):
    for obj in object_list:
        if obj[key] == target_id:
            return True
    return False
