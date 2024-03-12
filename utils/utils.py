

def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


# transform list of object to list of type
def object_list_to_type_list(object_list):
    type_list = []
    for object in object_list:
        type_list.append(type(object))
    return type_list


# concatenate string values of a dictionnary
def concatenate_dict_values(dict: dict) -> str:
    string = ""
    for key in dict:
        string += dict[key]
    return string
