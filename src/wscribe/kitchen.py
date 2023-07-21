from . import ingregients
from .recipies import difficult, easy


def do_something():
    print(ingregients.food_list)
    print(easy.easy_stuff())
    print(difficult.hard_stuff())
    return 22
