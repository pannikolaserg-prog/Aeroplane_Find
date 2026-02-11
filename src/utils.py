from src.planes import Plane

def get_object_list(planes_information: dict):
    """
    Функция для упорядочивания данных о самолетах.
    """
    object_list = []
    for plane in planes_information["states"]:
        object_ = Plane(plane[2], plane[1], plane[9], plane[13])
        object_list.append(object_)

    return object_list