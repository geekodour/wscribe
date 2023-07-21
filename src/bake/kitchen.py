# NOTE: using relative imports
from . import ingregients
from .recipies import difficult, easy

# NOTE: could also be using absolute imports
# import bake.ingregients
# import bake.recipies.difficult
# import bake.recipies.easy


def do_something():
    print(ingregients.food_list)
    print(easy.easy_stuff())
    print(difficult.hard_stuff())
    return 22
