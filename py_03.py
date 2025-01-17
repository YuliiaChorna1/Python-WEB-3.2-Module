# приклад з використанням структур у спільній пам'яті.
# ми створили:
# - структуру Point, яка описує координати точки на площині;
# - дробове число number;
# - рядкову змінну string (підтримуються тільки byte-рядки);
# - масив array, який містить координати точок відповідно до структури Point.
# Зверніть увагу, для опису полів структури їх потрібно помістити в список кортежів _fields_, 
# де кожен кортеж — це ім'я та тип поля.

# Масив Array поводиться багато в чому як список і дозволяє зберігати в ньому різнотипні дані,
# але його розмір статичний і додавати/видаляти елементи не можна. 
# Так само як і змінювати тип існуючих.

# Також у структурі даних ми передали механізм блокування через параметр lock.
# Як Value, так і Array забезпечують блокування ресурсу, до якого можна отримати доступ, 
# щоб як читати, так і оновлювати дані.

from multiprocessing import Process, RLock, current_process
from multiprocessing.sharedctypes import Value, Array
from ctypes import Structure, c_double
import logging


logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


class Point(Structure):

    _fields_ = [('x', c_double), ('y', c_double)]


def modify(num: Value, string: Array, arr: Array):

    logger.debug(f"Started {current_process().name}")
    logger.debug(f"Change num: {num.value}")
    
    with num.get_lock():
        num.value **= 2

    logger.debug(f"to num: {num.value}")

    with string.get_lock():
        string.value = string.value.upper()

    with arr.get_lock():
        for a in arr:
            a.x **= 2
            a.y **= 2
    
    logger.debug(f"Done {current_process().name}")


if __name__ == '__main__':

    lock = RLock()
    number = Value(c_double, 1.5, lock=lock)
    string = Array('c', b"hello world", lock=lock)
    array = Array(Point, [(1, -6), (-5, 2), (2, 9)], lock=lock)

    p = Process(target=modify, args=(number, string, array))
    p2 = Process(target=modify, args=(number, string, array))

    p.start()
    p2.start()
    p.join()
    p2.join()

    print(number.value)
    print(string.value)
    print([(arr.x, arr.y) for arr in array])
