from cooking_zoo.cooking_world.world_objects import *
from cooking_zoo.cooking_book.recipe import Recipe, RecipeNode
from copy import deepcopy


def id_num_generator():
    num = 0
    while True:
        yield num
        num += 1


NUM_GOALS = 0
id_generator = id_num_generator()

DEFAULT_NUM_GOALS = 0
default_id_generator = id_num_generator()

RECIPE_STORE = {}


def get_next_id():
    global NUM_GOALS
    NUM_GOALS += 1
    return next(id_generator)


def get_next_default_id():
    global DEFAULT_NUM_GOALS
    DEFAULT_NUM_GOALS += 1
    return next(default_id_generator)


def register_recipe(recipe, name):
    RECIPE_STORE[name] = lambda: deepcopy(recipe)


#  Basic food Items
# root_type, id_num, parent=None, conditions=None, contains=None
ChoppedLettuce = RecipeNode(root_type=Lettuce, id_num=get_next_default_id(), name="Lettuce",
                            conditions=[("chop_state", ChopFoodStates.CHOPPED)])
ChoppedOnion = RecipeNode(root_type=Onion, id_num=get_next_default_id(), name="Onion",
                          conditions=[("chop_state", ChopFoodStates.CHOPPED)])
ChoppedTomato = RecipeNode(root_type=Tomato, id_num=get_next_default_id(), name="Tomato",
                           conditions=[("chop_state", ChopFoodStates.CHOPPED)])
ChoppedApple = RecipeNode(root_type=Apple, id_num=get_next_default_id(), name="Apple",
                          conditions=[("chop_state", ChopFoodStates.CHOPPED)])
ChoppedCucumber = RecipeNode(root_type=Cucumber, id_num=get_next_default_id(), name="Cucumber",
                             conditions=[("chop_state", ChopFoodStates.CHOPPED)])
ChoppedWatermelon = RecipeNode(root_type=Watermelon, id_num=get_next_default_id(), name="Watermelon",
                               conditions=[("chop_state", ChopFoodStates.CHOPPED)])
ChoppedBanana = RecipeNode(root_type=Banana, id_num=get_next_default_id(), name="Banana",
                           conditions=[("chop_state", ChopFoodStates.CHOPPED)])
MashedBanana = RecipeNode(root_type=Banana, id_num=get_next_default_id(), name="Banana",
                          conditions=[("blend_state", BlenderFoodStates.MASHED)])
ChoppedCarrot = RecipeNode(root_type=Carrot, id_num=get_next_default_id(), name="Carrot",
                           conditions=[("chop_state", ChopFoodStates.CHOPPED)])
MashedCarrot = RecipeNode(root_type=Carrot, id_num=get_next_default_id(), name="Carrot",
                          conditions=[("blend_state", BlenderFoodStates.MASHED)])
ChoppedBread = RecipeNode(root_type=Bread, id_num=get_next_default_id(), name="Bread",
                          conditions=[("chop_state", ChopFoodStates.CHOPPED)])
ToastedBread = RecipeNode(root_type=Bread, id_num=get_next_default_id(), name="Bread",
                          conditions=[("chop_state", ChopFoodStates.CHOPPED),
                                      ("toast_state", ToasterFoodStates.TOASTED)])

# # Needed for ToastedBreadPlate, where the two toasted breads cannot be the same...
# ToastedBread2 = RecipeNode(root_type=Bread, id_num=get_next_default_id(), name="Bread",
#                           conditions=[("chop_state", ChopFoodStates.CHOPPED),
#                                       ("toast_state", ToasterFoodStates.TOASTED)])

# Salad Plates
TomatoSaladPlate = RecipeNode(root_type=Plate, id_num=get_next_default_id(), name="Plate", conditions=None,
                              contains=[ChoppedTomato])
TomatoLettucePlate = RecipeNode(root_type=Plate, id_num=get_next_default_id(), name="Plate", conditions=None,
                                contains=[ChoppedTomato, ChoppedLettuce])
TomatoLettuceOnionPlate = RecipeNode(root_type=Plate, id_num=get_next_default_id(), name="Plate", conditions=None,
                                     contains=[ChoppedTomato, ChoppedLettuce, ChoppedOnion])

CarrotBananaPlate = RecipeNode(root_type=Plate, id_num=get_next_default_id(), name="Plate", conditions=None,
                               contains=[MashedCarrot, ChoppedBanana])

MashedCarrotBananaPlate = RecipeNode(root_type=Plate, id_num=get_next_default_id(), name="Plate", conditions=None,
                                     contains=[MashedCarrot, MashedBanana])

CucumberOnionPlate = RecipeNode(root_type=Plate, id_num=get_next_default_id(), name="Plate", conditions=None,
                                contains=[ChoppedCucumber, ChoppedOnion])

AppleWatermelonPlate = RecipeNode(root_type=Plate, id_num=get_next_default_id(), name="Plate", conditions=None,
                                  contains=[ChoppedApple, ChoppedWatermelon])
MashedCarrotPlate = RecipeNode(root_type=Plate, id_num=get_next_default_id(), name="Plate", conditions=None,
                               contains=[MashedCarrot])

ToastedBreadPlate = RecipeNode(root_type=Plate, id_num=get_next_default_id(), name="Plate", conditions=None,
                               contains=[ToastedBread])

TomatoToastedBreadPlate = RecipeNode(root_type=Plate, id_num=get_next_default_id(), name="Plate", conditions=None,
                                     contains=[ToastedBread, ChoppedTomato])

ApplePlate = RecipeNode(root_type=Plate, id_num=get_next_default_id(), name="Plate", conditions=None,
                        contains=[ChoppedApple])

WatermelonPlate = RecipeNode(root_type=Plate, id_num=get_next_default_id(), name="Plate", conditions=None,
                             contains=[ChoppedWatermelon])

# Delivered Salads
TomatoSalad = RecipeNode(root_type=Deliversquare, id_num=get_next_default_id(), name="Deliversquare", conditions=None,
                         contains=[TomatoSaladPlate])
TomatoLettuceSalad = RecipeNode(root_type=Deliversquare, id_num=get_next_default_id(), name="Deliversquare",
                                conditions=None, contains=[TomatoLettucePlate])
TomatoLettuceOnionSalad = RecipeNode(root_type=Deliversquare, id_num=get_next_default_id(), name="Deliversquare",
                                     conditions=None, contains=[TomatoLettuceOnionPlate])

CarrotBanana = RecipeNode(root_type=Deliversquare, id_num=get_next_default_id(), name="Deliversquare", conditions=None,
                          contains=[CarrotBananaPlate])

MashedCarrotBanana = RecipeNode(root_type=Deliversquare, id_num=get_next_default_id(), name="Deliversquare",
                                conditions=None, contains=[MashedCarrotBananaPlate])

CucumberOnion = RecipeNode(root_type=Deliversquare, id_num=get_next_default_id(), name="Deliversquare", conditions=None,
                           contains=[CucumberOnionPlate])
AppleWatermelon = RecipeNode(root_type=Deliversquare, id_num=get_next_default_id(), name="Deliversquare", conditions=None,
                             contains=[AppleWatermelonPlate])
# MashedCarrot = RecipeNode(root_type=Deliversquare, id_num=get_next_default_id(), name="Deliversquare",
#                           conditions=None, contains=[CarrotPlate])

floor = RecipeNode(root_type=Floor, id_num=get_next_default_id(), name="Floor", conditions=None, contains=[])

no_recipe_node = RecipeNode(root_type=Deliversquare, id_num=get_next_default_id(), name='Deliversquare', conditions=None,
                            contains=[floor])

RECIPES = {"TomatoSalad": lambda: deepcopy(Recipe(TomatoSalad, DEFAULT_NUM_GOALS)),
           "TomatoLettuceSalad": lambda: deepcopy(Recipe(TomatoLettuceSalad, DEFAULT_NUM_GOALS)),
           "CarrotBanana": lambda: deepcopy(Recipe(CarrotBanana, DEFAULT_NUM_GOALS)),
           "MashedCarrotBanana": lambda: deepcopy(Recipe(MashedCarrotBanana, DEFAULT_NUM_GOALS)),
           "CucumberOnion": lambda: deepcopy(Recipe(CucumberOnion, DEFAULT_NUM_GOALS)),
           "AppleWatermelon": lambda: deepcopy(Recipe(AppleWatermelon, DEFAULT_NUM_GOALS)),
           "TomatoLettuceOnionSalad": lambda: deepcopy(Recipe(TomatoLettuceOnionSalad, DEFAULT_NUM_GOALS)),
           # "MashedCarrot": lambda: deepcopy(Recipe(MashedCarrot)),

           # for use with CookingEnvironment::handle_absorbed_recipe(), which doesn't send the Deliversquare
           "no_recipe": lambda: deepcopy(Recipe(no_recipe_node, DEFAULT_NUM_GOALS)),
           "TomatoSaladPlate": lambda: deepcopy(Recipe(TomatoSaladPlate, DEFAULT_NUM_GOALS)),
           "TomatoLettucePlate": lambda: deepcopy(Recipe(TomatoLettucePlate, DEFAULT_NUM_GOALS)),
           "CarrotBananaPlate": lambda: deepcopy(Recipe(CarrotBananaPlate, DEFAULT_NUM_GOALS)),
           "MashedCarrotBananaPlate": lambda: deepcopy(Recipe(MashedCarrotBananaPlate, DEFAULT_NUM_GOALS)),
           # "CucumberOnionPlate": lambda: deepcopy(Recipe(CucumberOnionPlate, DEFAULT_NUM_GOALS)),
           "AppleWatermelonPlate": lambda: deepcopy(Recipe(AppleWatermelonPlate, DEFAULT_NUM_GOALS)),
           "TomatoLettuceOnionPlate": lambda: deepcopy(Recipe(TomatoLettuceOnionPlate, DEFAULT_NUM_GOALS)),
           "MashedCarrotPlate": lambda: deepcopy(Recipe(MashedCarrotPlate, DEFAULT_NUM_GOALS)),
           "ToastedBreadPlate": lambda: deepcopy(Recipe(ToastedBreadPlate, DEFAULT_NUM_GOALS)),
           "TomatoToastedBreadPlate": lambda: deepcopy(Recipe(TomatoToastedBreadPlate, DEFAULT_NUM_GOALS)),
           "ApplePlate": lambda: deepcopy(Recipe(ApplePlate, DEFAULT_NUM_GOALS)),
           "WatermelonPlate": lambda: deepcopy(Recipe(WatermelonPlate, DEFAULT_NUM_GOALS))
           }
