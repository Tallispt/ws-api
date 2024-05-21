def convert_case(str_camelcase):
    # This function takes in a string in camelCase and converts it to snake_case
    str_snake_case = ""
    for ele in list(str_camelcase):
        if ele.islower():
            str_snake_case = str_snake_case + ele
        else:
            str_snake_case = str_snake_case + "_" + ele.lower()
    return str_snake_case


def convert_json(json_dict):
    # This function takes in a dictionary and converts the keys of the dictionary to snake_case
    temp = {}
    for item in json_dict:
        new_item = convert_case(item)
        temp[new_item] = json_dict[item]
        new_list = []
        if type(json_dict[item]) is list:
            for ele in json_dict[item]:
                if type(ele) is dict:
                    new_list.append(convert_json(ele))
            if len(new_list) != 0:
                temp[new_item] = new_list
        if type(json_dict[item]) is dict:
            # if the value is a dictionary, recursively convert it to snake_case
            temp[new_item] = convert_json(json_dict[item])
    return temp
