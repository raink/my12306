from app import station_dict


def name2three_code(name):
    if name in station_dict:
        return station_dict[name]
    else:
        raise SyntaxError('不存在的车站')


def city2name_list(city_name):
    # todo EINDEX 用city 来得到一个城市3字码的列表
    return name2three_code(city_name)
    pass



