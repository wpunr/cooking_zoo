from cooking_zoo.cooking_world.abstract_classes import *
from cooking_zoo.cooking_world.constants import *
import inspect
import sys
from collections.abc import Callable
import itertools


world_id_counter = itertools.count(start=0, step=1)


def reset_world_counter():
    global world_id_counter
    world_id_counter = itertools.count(start=0, step=1)


class Floor(StaticObject, ContentObject):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location, True)

    def accepts(self, dynamic_object) -> bool:
        return False

    def releases(self) -> bool:
        return True

    def add_content(self, content):
        assert isinstance(content, Agent), f"Floors can only hold Agents as content! not {content}"
        self.content.append(content)

    def numeric_state_representation(self):
        return 1,

    def feature_vector_representation(self):
        return []

    @classmethod
    def state_length(cls):
        return 1

    @classmethod
    def feature_vector_length(cls):
        return 0

    def file_name(self) -> str:
        return "Floor"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""


class Counter(StaticObject, ContentObject):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location, False)
        self.max_content = 1

    def accepts(self, dynamic_object) -> bool:
        # return not bool(self.content)
        return len(self.content) < self.max_content

    def releases(self) -> bool:
        return True

    def add_content(self, content):
        self.content.append(content)
        for c in self.content:
            c.free = False
        self.content[-1].free = True

    def numeric_state_representation(self):
        return 1,

    def feature_vector_representation(self):
        return list(self.location) + [1]

    @classmethod
    def state_length(cls):
        return 1

    @classmethod
    def feature_vector_length(cls):
        return 3

    def file_name(self) -> str:
        return "Counter"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""


class Deliversquare(StaticObject, ContentObject):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location, False)

    def accepts(self, dynamic_object) -> bool:
        return len(self.content) < self.max_content

    def add_content(self, content):
        if self.accepts(content):
            self.content.append(content)
            for c in self.content:
                c.free = False
            self.content[-1].free = True

    def releases(self) -> bool:
        return False

    def numeric_state_representation(self):
        return 1,

    def feature_vector_representation(self):
        return list(self.location) + [1]

    @classmethod
    def feature_vector_length(cls):
        return 3

    @classmethod
    def state_length(cls):
        return 1

    def file_name(self) -> str:
        return "DeliverySquare"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""


class AbsorbingDeliversquare(StaticObject, ContentObject, ProgressingObject):
    """Backported from drother moop branch"""

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location, False)
        self.internal_id = 1
        self.timer = 1

        self.deliver = 0

    def accepts(self, dynamic_object) -> bool:
        return len(self.content) < self.max_content

    def progress(self):
        if self.content and self.timer > 0:
            self.timer -= 1
            deleted_obj_list = []
        elif self.content and self.timer == 0:
            self.timer = 1
            content_objs = []
            for cont in self.content:
                content_objs.extend(get_recursive_content_objects(cont))
            deleted_obj_list = content_objs
            self.content = []

            self.deliver += 1
        else:
            deleted_obj_list = []
        new_obj_list = []
        return new_obj_list, deleted_obj_list

    def add_content(self, content):
        if self.accepts(content):
            self.content.append(content)
            for c in self.content:
                c.free = False
            self.content[-1].free = True

    def releases(self) -> bool:
        return False

    def numeric_state_representation(self):
        return 1,

    def feature_vector_representation(self):
        return list(self.location) + [1]

    @classmethod
    def feature_vector_length(cls):
        return 3

    @classmethod
    def state_length(cls):
        return 1

    def file_name(self) -> str:
        return "DeliverySquare"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return f"{self.deliver}"



class Switch(StaticObject, ContentObject, LinkedObject):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location, True)
        self.max_content = 1
        self.switch_active = False
        self.button_pressed = False

    def accepts(self, dynamic_object) -> bool:
        return False

    def releases(self) -> bool:
        return True

    def add_content(self, content):
        assert isinstance(content, Agent), f"Floors can only hold Agents as content! not {content}"
        self.content.append(content)
        self.switch_active = not self.switch_active
        self.button_pressed = True

    def process_linked_objects(self):
        if self.button_pressed:
            for obj in self.linked_objects:
                obj.switch_state()
        self.button_pressed = False

    def numeric_state_representation(self):
        return 1,

    def feature_vector_representation(self):
        return list(self.location) + [self.switch_active, 1]

    @classmethod
    def state_length(cls):
        return 1

    @classmethod
    def feature_vector_length(cls):
        return 4

    def file_name(self) -> str:
        return "SwitchOn" if self.switch_active else "SwitchOff"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""


class Block(StaticObject, ContentObject, LinkedObject):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location, False)
        self.max_content = 1

    def releases(self) -> bool:
        return True

    def process_linked_objects(self):
        pass

    def accepts(self, dynamic_objects) -> bool:
        return False

    def add_content(self, content):
        assert isinstance(content, Agent), f"Blocks can only hold Agents as content! not {content}"
        self.content.append(content)

    def switch_state(self):
        self.walkable = not self.walkable

    def numeric_state_representation(self):
        return 1,

    def feature_vector_representation(self):
        return list(self.location) + [int(self.walkable), 1]

    @classmethod
    def state_length(cls):
        return 1

    @classmethod
    def feature_vector_length(cls):
        return 4

    def file_name(self) -> str:
        return "Floor" if self.walkable else "BlockActive"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""


class Cutboard(StaticObject, ActionObject, ContentObject):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location, False)

        self.max_content = 1

    def action(self) -> Tuple[List, List, bool]:
        valid = self.status == ActionObjectState.READY
        if valid:
            for obj in self.content:
                if isinstance(obj, ChopFood):
                    new_obj_list, deleted_obj_list, action_executed = obj.chop()

                    if action_executed:
                        for del_obj in deleted_obj_list:
                            self.content.remove(del_obj)
                        for new_obj in new_obj_list:
                            self.content.append(new_obj)

                        self.status = ActionObjectState.NOT_USABLE

                        return new_obj_list, deleted_obj_list, action_executed
                else:
                    return [], [], False
        else:
            return [], [], False

    def accepts(self, dynamic_object) -> bool:
        return isinstance(dynamic_object, ChopFood) and len(self.content) < self.max_content and \
                dynamic_object.chop_state == ChopFoodStates.FRESH

    def releases(self) -> bool:
        if len(self.content) == 1:
            self.status = ActionObjectState.NOT_USABLE
        return True

    def add_content(self, content):
        if self.accepts(content):
            self.status = ActionObjectState.READY
            self.content.append(content)
            for c in self.content:
                c.free = False
            self.content[-1].free = True
        else:
            raise Exception(f"Tried to add invalid object {content.__name__} to CutBoard")

    def numeric_state_representation(self):
        return 1,

    def feature_vector_representation(self):
        return list(self.location) + [1]

    @classmethod
    def state_length(cls):
        return 1

    @classmethod
    def feature_vector_length(cls):
        return 3

    def file_name(self) -> str:
        return "cutboard"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""


class Blender(StaticObject, ProcessingObject, ContentObject, ToggleObject, ActionObject):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location, False)
        self.max_content = 10
        
    def process(self):
        assert len(self.content) <= self.max_content, "Too many Dynamic Objects placed into the Blender"

        if self.content and self.toggle:
            for con in self.content:
                con.blend()

            if all([cont.blend_state == BlenderFoodStates.MASHED for cont in self.content]):
                self.switch_toggle()

                self.status = ActionObjectState.NOT_USABLE

                to_delete = []

                for obj in self.content:
                    to_delete.append(obj)

                self.content = []
                to_add = Smoothie(self.location, True)
                
                self.content.append(to_add)

                return self.content, to_delete 
            
        return [], [] # no added or deleted objects

    def accepts(self, dynamic_object) -> bool:
        return isinstance(dynamic_object, BlenderFood) and (not self.toggle) and len(self.content) + 1 <= self.max_content and dynamic_object.blend_state == BlenderFoodStates.FRESH

    def releases(self) -> bool:
        valid = not self.toggle
        if valid:
            # if last removed, not usable
            if len(self.content) - 1 == 0:
                self.status = ActionObjectState.NOT_USABLE
        return valid

    def add_content(self, content):
        if self.accepts(content):
            self.status = ActionObjectState.READY
            self.content.append(content)
            for c in self.content:
                c.free = False
            self.content[-1].free = True

    def action(self) -> Tuple[List, List, bool]:
        valid = self.status == ActionObjectState.READY
        if valid:
            self.switch_toggle()
        return [], [], valid

    def numeric_state_representation(self):
        return 1,

    @classmethod
    def state_length(cls):
        return 1

    def feature_vector_representation(self):
        return list(self.location) + [1]

    @classmethod
    def feature_vector_length(cls):
        return 3

    def file_name(self) -> str:
        return "blender_on" if self.toggle else "blender3"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""


class Toaster(StaticObject, ProcessingObject, ContentObject, ToggleObject, ActionObject):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location, False)
        self.max_content = 2  # TODO

    def process(self):
        assert len(self.content) <= self.max_content, "Too many Dynamic Objects placed into the Toaster"

        if self.content and self.toggle:
            for cont in self.content:
                print("toast")
                cont.toast()

            if all([cont.toast_state == ToasterFoodStates.TOASTED for cont in self.content]):
                self.switch_toggle()

                self.status = ActionObjectState.NOT_USABLE

                for cont in self.content:
                    cont.current_progress = cont.min_progress

        return [], []  # no added or deleted objects

    def accepts(self, dynamic_object) -> bool:
        return isinstance(dynamic_object, ToasterFood) and (not self.toggle) and len(
            self.content) + 1 <= self.max_content and dynamic_object.toast_state in {ToasterFoodStates.FRESH,
                                                                                     ToasterFoodStates.READY}

    def releases(self) -> bool:
        valid = not self.toggle
        if valid:
            # if last removed, not usable
            if len(self.content) - 1 == 0:
                self.status = ActionObjectState.NOT_USABLE
        return valid

    def add_content(self, content):
        if self.accepts(content):
            self.content.append(content)
            if len(self.content) <= self.max_content:
                for cont in self.content:
                    cont.toast_state = ToasterFoodStates.READY
                self.status = ActionObjectState.READY
            for c in self.content:
                c.free = False
            self.content[-1].free = True

    def action(self) -> Tuple[List, List, bool]:
        valid = self.status == ActionObjectState.READY
        if valid:
            self.switch_toggle()
        return [], [], valid

    def numeric_state_representation(self):
        return 1,

    @classmethod
    def state_length(cls):
        return 1

    def feature_vector_representation(self):
        # TODO check this
        return list(self.location) + [1]

    @classmethod
    def feature_vector_length(cls):
        return 3

    def file_name(self) -> str:
        if self.toggle:
            return "toaster_on"
        elif self.content and all([cont.toast_state == ToasterFoodStates.TOASTED for cont in self.content]):
            return "toaster_toasted_bread_2"
        elif self.content:
            return "toaster_fresh_bread_2"
        else:
            return "toaster_off"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""


class Pot(StaticObject, ProcessingObject, ContentObject, ToggleObject, ActionObject):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location, False)
        self.max_content = 1  # TODO

    def process(self):
        assert len(self.content) <= self.max_content, "Too many Dynamic Objects placed into the Pot"

        if self.content and self.toggle:
            for cont in self.content:
                print("boil")
                cont.boil()

            if all([cont.boil_state == PotFoodStates.COOKED for cont in self.content]):
                self.switch_toggle()

                self.status = ActionObjectState.NOT_USABLE

                for cont in self.content:
                    cont.current_progress = cont.min_progress

        return [], []  # no added or deleted objects

    def accepts(self, dynamic_object) -> bool:
        return isinstance(dynamic_object, PotFood) and (not self.toggle) and len(
            self.content) + 1 <= self.max_content and dynamic_object.boil_state in {PotFoodStates.FRESH,
                                                                                     PotFoodStates.READY}

    def releases(self) -> bool:
        valid = not self.toggle
        if valid:
            # if last removed, not usable
            if len(self.content) - 1 == 0:
                self.status = ActionObjectState.NOT_USABLE
        return valid

    def add_content(self, content):
        if self.accepts(content):
            self.content.append(content)
            if len(self.content) <= self.max_content:
                for cont in self.content:
                    cont.boil_state = PotFoodStates.READY
                self.status = ActionObjectState.READY
            for c in self.content:
                c.free = False
            self.content[-1].free = True

    def action(self) -> Tuple[List, List, bool]:
        valid = self.status == ActionObjectState.READY
        if valid:
            self.switch_toggle()
        return [], [], valid

    def numeric_state_representation(self):
        return 1,

    @classmethod
    def state_length(cls):
        return 1

    def feature_vector_representation(self):
        # TODO check this
        return list(self.location) + [1]

    @classmethod
    def feature_vector_length(cls):
        return 3

    def file_name(self) -> str:
        if self.toggle:
            return "Pot_on"
        else:
            return "Pot"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""

class Pan(StaticObject, ProcessingObject, ContentObject, ToggleObject, ActionObject):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location, False)
        self.max_content = 1  # TODO

    def process(self):
        assert len(self.content) <= self.max_content, "Too many Dynamic Objects placed into the Pan"

        if self.content and self.toggle:
            for cont in self.content:
                print("fry")
                cont.fry()

            if all([cont.fry_state == PanFoodStates.FRIED for cont in self.content]):
                self.switch_toggle()

                self.status = ActionObjectState.NOT_USABLE

                for cont in self.content:
                    cont.current_progress = cont.min_progress

        return [], []  # no added or deleted objects

    def accepts(self, dynamic_object) -> bool:
        return isinstance(dynamic_object, PanFood) and (not self.toggle) and len(
            self.content) + 1 <= self.max_content and dynamic_object.fry_state in {PanFoodStates.FRESH,
                                                                                     PanFoodStates.READY}

    def releases(self) -> bool:
        valid = not self.toggle
        if valid:
            # if last removed, not usable
            if len(self.content) - 1 == 0:
                self.status = ActionObjectState.NOT_USABLE
        return valid

    def add_content(self, content):
        if self.accepts(content):
            self.content.append(content)
            if len(self.content) <= self.max_content:
                for cont in self.content:
                    cont.fry_state = PanFoodStates.READY
                self.status = ActionObjectState.READY
            for c in self.content:
                c.free = False
            self.content[-1].free = True

    def action(self) -> Tuple[List, List, bool]:
        valid = self.status == ActionObjectState.READY
        if valid:
            self.switch_toggle()
        return [], [], valid

    def numeric_state_representation(self):
        return 1,

    @classmethod
    def state_length(cls):
        return 1

    def feature_vector_representation(self):
        # TODO check this
        return list(self.location) + [1]

    @classmethod
    def feature_vector_length(cls):
        return 3

    def file_name(self) -> str:
        if self.toggle:
            return "Pan_on"
        else:
            return "Pan"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""

class Plate(DynamicObject, ContentObject):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location)
        self.max_content = 64

    def move_to(self, new_location):
        for content in self.content:
            content.move_to(new_location)
        self.location = new_location

    def add_content(self, content):
        if not isinstance(content, Food):
            raise TypeError(f"Only Food can be added to a plate! Tried to add {content.name()}")
        if not content.done():
            raise Exception(f"Can't add food in unprepared state.")
        self.content.append(content)
        for c in self.content:
            c.free = False
        self.content[-1].free = True

    def accepts(self, dynamic_object):
        return isinstance(dynamic_object, Food) and dynamic_object.done() and len(self.content) < self.max_content

    def numeric_state_representation(self):
        return 1,

    def feature_vector_representation(self):
        return list(self.location) + [1]

    @classmethod
    def state_length(cls):
        return 1

    @classmethod
    def feature_vector_length(cls):
        return 3

    def file_name(self) -> str:
        return "Plate"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""

class Tomato(ChopFood, PanFood):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location)

    def done(self):
        return self.chop_state == ChopFoodStates.CHOPPED or self.fry_state == PanFoodStates.FRIED

    def numeric_state_representation(self):
        return 1, 0, 0

    def feature_vector_representation(self):
        return list(self.location) + [int(not self.done()), int(self.done())] + [int(self.fry_state == PanFoodStates.FRIED)] + [1]

    @classmethod
    def state_length(cls):
        return 3

    @classmethod
    def feature_vector_length(cls):
        return 6

    def file_name(self) -> str:
        if self.fry_state == PanFoodStates.FRIED:
            return "TomatoSauce"
        elif self.chop_state == ChopFoodStates.CHOPPED:
            return "ChoppedTomato"
        else:
            return "FreshTomato"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""
    
class Pasta(PotFood):

    def __init__(self, location): 
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location)

    def done(self):
        return self.boil_state == PotFoodStates.COOKED
    
    def numeric_state_representation(self):
        return 1, 0, 0
    
    def feature_vector_representation(self):
        return list(self.location) + [int(not self.done()), int(self.done())] + [1]
    
    @classmethod
    def state_length(cls):
        return 3
    
    @classmethod
    def feature_vector_length(cls):
        return 5

    def file_name(self) -> str:
        if self.boil_state == PotFoodStates.COOKED:
            return "PenneCooked"
        else:
            return "PenneRaw"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return f""

class Egg(PanFood):

    def __init__(self, location): 
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location)

    def done(self):
        return self.fry_state == PanFoodStates.FRIED
    
    def numeric_state_representation(self):
        return 1, 0
    
    def feature_vector_representation(self):
        return list(self.location) + [int(not self.done()), int(self.done())] + [1]
    
    @classmethod
    def state_length(cls):
        return 2
    
    @classmethod
    def feature_vector_length(cls):
        return 5

    def file_name(self) -> str:
        if self.done():
            return "FriedEgg"
        else:
            return "Egg"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return f""


class Onion(ChopFood):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location)

    def done(self):
        return self.chop_state == ChopFoodStates.CHOPPED

    def numeric_state_representation(self):
        return 1, int(self.chop_state == ChopFoodStates.CHOPPED)

    def feature_vector_representation(self):
        return list(self.location) + [int(not self.done()), int(self.done())] + [1]

    @classmethod
    def state_length(cls):
        return 2

    @classmethod
    def feature_vector_length(cls):
        return 5

    def file_name(self) -> str:
        if self.done():
            return "ChoppedOnion"
        else:
            return "FreshOnion"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""

class Lettuce(ChopFood):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location)

    def done(self):
        return self.chop_state == ChopFoodStates.CHOPPED

    def numeric_state_representation(self):
        return 1, int(self.chop_state == ChopFoodStates.CHOPPED)

    def feature_vector_representation(self):
        return list(self.location) + [int(not self.done()), int(self.done())] + [1]

    @classmethod
    def state_length(cls):
        return 2

    @classmethod
    def feature_vector_length(cls):
        return 5

    def file_name(self) -> str:
        if self.done():
            return "ChoppedLettuce"
        else:
            return "FreshLettuce"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""
    
class Smoothie(BlenderFood):

    def __init__(self, location, made_correctly=False):
        if not made_correctly:
            raise RuntimeError("Made smoothie outside of blender class. Returning in error.")
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location)

        self.blend_state = BlenderFoodStates.MASHED

    def done(self):
        return self.blend_state == BlenderFoodStates.MASHED

    def numeric_state_representation(self):
        return 1, int(self.blend_state == BlenderFoodStates.MASHED)

    def feature_vector_representation(self):
        return list(self.location) + [int(not self.done()), int(self.done())] + [1]

    @classmethod
    def state_length(cls):
        return 2

    @classmethod
    def feature_vector_length(cls):
        return 5

    def file_name(self) -> str:
        return "Smoothie"
    
    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""

class Ice(BlenderFood):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location)

    def done(self):
        return self.blend_state == BlenderFoodStates.MASHED

    def numeric_state_representation(self):
        return 1, int(self.blend_state == BlenderFoodStates.MASHED)

    def feature_vector_representation(self):
        return list(self.location) + [int(not self.done()), int(self.done())] + [1]

    @classmethod
    def state_length(cls):
        return 2

    @classmethod
    def feature_vector_length(cls):
        return 5

    def file_name(self) -> str:
        return "Ice"
    
    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""
    
class Strawberry(BlenderFood):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location)

    def done(self):
        return self.blend_state == BlenderFoodStates.MASHED

    def numeric_state_representation(self):
        return 1, int(self.blend_state == BlenderFoodStates.MASHED)

    def feature_vector_representation(self):
        return list(self.location) + [int(not self.done()), int(self.done())] + [1]

    @classmethod
    def state_length(cls):
        return 2

    @classmethod
    def feature_vector_length(cls):
        return 5

    def file_name(self) -> str:
        return "Strawberry"
    
    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""

class Carrot(BlenderFood, ChopFood):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location)

    def done(self):
        return self.chop_state == ChopFoodStates.CHOPPED or self.blend_state == BlenderFoodStates.MASHED

    def numeric_state_representation(self):
        return 1, int(self.chop_state == ChopFoodStates.CHOPPED)

    def feature_vector_representation(self):
        return list(self.location) + [int(not self.done()), int(self.chop_state == ChopFoodStates.CHOPPED),
                                      int(self.blend_state == BlenderFoodStates.MASHED)] + [1]

    @classmethod
    def state_length(cls):
        return 2

    @classmethod
    def feature_vector_length(cls):
        return 6

    def file_name(self) -> str:
        if self.done():
            if self.chop_state == ChopFoodStates.CHOPPED:
                return "ChoppedCarrot"
            elif self.blend_state == BlenderFoodStates.MASHED:
                return "CarrotMashed"
        else:
            return "FreshCarrot"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""


class Cucumber(ChopFood):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location)

    def done(self):
        return self.chop_state == ChopFoodStates.CHOPPED

    def numeric_state_representation(self):
        return 1, int(self.chop_state == ChopFoodStates.CHOPPED)

    def feature_vector_representation(self):
        return list(self.location) + [int(not self.done()), int(self.done())] + [1]

    @classmethod
    def state_length(cls):
        return 2

    @classmethod
    def feature_vector_length(cls):
        return 5

    def file_name(self) -> str:
        return "default_dynamic"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return "Cu " + str(self.chop_state.value[:3])


class Banana(BlenderFood, ChopFood):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location)

    def done(self):
        return self.blend_state == BlenderFoodStates.MASHED

    def numeric_state_representation(self):
        return 1, int(self.chop_state == ChopFoodStates.CHOPPED)

    def feature_vector_representation(self):
        return list(self.location) + [int(not self.done()), int(self.chop_state == ChopFoodStates.CHOPPED),
                                      int(self.blend_state == BlenderFoodStates.MASHED)] + [1]

    @classmethod
    def state_length(cls):
        return 2

    @classmethod
    def feature_vector_length(cls):
        return 6

    def file_name(self) -> str:
        if self.chop_state == ChopFoodStates.CHOPPED:
            return "ChoppedBanana"
        else:
            return "FreshBanana"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""


class Apple(ChopFood):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location)

    def done(self):
        return self.chop_state == ChopFoodStates.CHOPPED

    def numeric_state_representation(self):
        return 1, int(self.chop_state == ChopFoodStates.CHOPPED)

    def feature_vector_representation(self):
        return list(self.location) + [int(not self.done()), int(self.chop_state == ChopFoodStates.CHOPPED)] + [1]

    @classmethod
    def state_length(cls):
        return 2

    @classmethod
    def feature_vector_length(cls):
        return 5

    def file_name(self) -> str:
        if self.chop_state == ChopFoodStates.CHOPPED:
            return "ChoppedApple"
        else:
            return "FreshApple"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return f""


class Watermelon(ChopFood):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location)

    def done(self):
        return self.chop_state == ChopFoodStates.CHOPPED

    def numeric_state_representation(self):
        return 1, int(self.chop_state == ChopFoodStates.CHOPPED)

    def feature_vector_representation(self):
        return list(self.location) + [int(not self.done()), int(self.done())] + [1]

    @classmethod
    def state_length(cls):
        return 2

    @classmethod
    def feature_vector_length(cls):
        return 5

    def file_name(self) -> str:
        if self.chop_state == ChopFoodStates.CHOPPED:
            return "ChoppedWatermelon"
        else:
            return "FreshWatermelon"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return f""


class Bread(ChopFood, ToasterFood):

    def __init__(self, location):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location)
        self.chop_state = ChopFoodStates.FRESH

    def done(self):
        # TODO ambiguous
        return self.chop_state == ChopFoodStates.CHOPPED or self.toast_state == ToasterFoodStates.TOASTED

    def chop(self):
        if self.chop_state == ChopFoodStates.FRESH:
            self.chop_state = ChopFoodStates.CHOPPED
            new_chopped_bread = Bread(self.location)
            new_chopped_bread.chop_state = ChopFoodStates.CHOPPED
            return [new_chopped_bread], [], True
        else:
            return [], [], False

    def numeric_state_representation(self):
        return 1, 0, 0

    @classmethod
    def state_length(cls):
        return 3

    def feature_vector_representation(self):
        # TODO check this
        return list(self.location) + [int(not self.done()), int(self.done())] + [
            int(self.toast_state == ToasterFoodStates.TOASTED)] + [1]

    @classmethod
    def feature_vector_length(cls):
        return 6

    def file_name(self) -> str:
        if self.toast_state == ToasterFoodStates.TOASTED:
            return "ChoppedToastedBread"
        elif self.chop_state == ChopFoodStates.CHOPPED:
            return "ChoppedFreshBread"
        else:
            return "Bread"

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return f""


class Agent(Object):

    def __init__(self, location, color, name, num_arms):
        unique_id = next(world_id_counter)
        super().__init__(unique_id, location, False, False)
        self._holding_capacity = num_arms
        self._holding: list[None | Object] = [None] * self._holding_capacity
        self.color = color
        self.name = name
        self.orientation = 1
        self.interacts_with = []

    def grab(self, obj: DynamicObject, arm=None):
        """Insert `obj` into the first available slot in holding"""
        if arm is None:
            slc = slice(len(self.holding))
        else:
            slc = slice(arm, arm + 1)

        idx = self._find_free_holding(slc)
        if idx is not None:
            self.holding[idx] = obj
            obj.move_to(self.location)
        else:
            print("No free holding slot")
            raise Exception("Failed to grab object.")

    def put_down(self, location, obj: Object, arm=None):
        idx = self.holding.index(obj)  # raises if object not in holding

        if arm is not None:
            try:
                slc = slice(arm, arm + 1)
                self.holding[slc].index(obj)
            except ValueError:
                print("Agent is holding that object, but in a different arm")
                return

        self.holding[idx] = None

        obj.move_to(location)

    def move_to(self, new_location):
        self.location = new_location
        for held in self.holding:
            if held is not None:
                held.move_to(new_location)

    def change_orientation(self, new_orientation):
        assert 0 < new_orientation < 5
        self.orientation = new_orientation

    def numeric_state_representation(self):
        return 1, int(self.orientation == 1), int(self.orientation == 2), int(self.orientation == 3), \
               int(self.orientation == 4)

    def feature_vector_representation(self):
        return list(self.location) + [int(self.orientation == 1), int(self.orientation == 2),
                                      int(self.orientation == 3), int(self.orientation == 4)] + [1]

    @classmethod
    def state_length(cls):
        return 5

    @classmethod
    def feature_vector_length(cls):
        return 7

    def file_name(self) -> str:
        pass

    def icons(self) -> List[str]:
        return []

    def display_text(self) -> str:
        return ""

    def find_appropriate_holding(self, predicate, arm= None):
        """
        Find first object in Agent.holding that satisfies `predicate`

        :param predicate: Callable[[Object], bool] function like StaticObject.accepts()
        :param arm: Which arm/holding slot to consider
        :return: satisfying object, else None
        """
        if arm is None:
            slc = slice(len(self.holding))
        else:
            slc = slice(arm, arm + 1)
        return next((obj for obj in self.holding[slc] if predicate(obj) and obj is not None), None)

    def holding_empty(self, arm=None):
        """
        :param arm: Which arm/holding slot to consider
        :return: True if all holding slots are empty
        """
        if arm is None:
            slc = slice(len(self.holding))
        else:
            slc = slice(arm, arm + 1)
        return not any(self.holding[slc])

    def holding_has_free(self, arm=None):
        """
        :param arm: Which arm/holding slot to consider
        :return: True if any free holding slot exists
        """
        if arm is None:
            slc = slice(len(self.holding))
        else:
            slc = slice(arm, arm + 1)
        return any(held is None for held in self.holding[slc])

    @property
    def holding(self):
        return self._holding

    # Private
    def _find_free_holding(self, slc: slice):
        """
        Find first free slot in Agent.holding, limited to /slc/

        Note that return index is in terms of Agent.holding, not Agent.holding[slc]

        :param slc: slice of Agent.holding to consider
        :return: index of first free slot in Agent.holding, or None if no free slot.
        """
        slc_start = slc.start if slc.start is not None else 0
        for idx, val in enumerate(self.holding[slc]):
            if val is None:
                return idx + slc_start
        return None


####### Dispensers Differ from Drother moop in that they add the new object to their content, not agent.holding #######
def CreateDispenserClass(addedObjectCls, derived_name: str, file_name: str):
    def init_imp(self, location):
        unique_id = next(world_id_counter)
        super(cls, self).__init__(unique_id, location, False)
        self.max_content = 1

    def releases_imp(self) -> bool:
        return True

    def accepts_imp(self, dynamic_objects) -> bool:
        return False

    def action_imp(self) -> Tuple[List, List, bool]:
        if len(self.content) < self.max_content:
            new_obj = addedObjectCls(self.location)
            self.add_content(new_obj)
            new_obj_list = [new_obj]
            deleted_obj_list = []
            return new_obj_list, deleted_obj_list, True
        else:
            return [], [], False

    def add_content_imp(self, content):
        self.content.append(content)
        for c in self.content:
            c.free = False
        self.content[-1].free = True

    def numeric_state_representation_imp(self):
        return 1,

    def feature_vector_representation_imp(self):
        return list(self.location) + [int(self.walkable), 1]

    @classmethod
    def state_length_imp(cls):
        return 1

    @classmethod
    def feature_vector_length_imp(cls):
        return 4

    def file_name_imp(self) -> str:
        # TODO improve dispenser icon
        return file_name if not self.content else "Counter"

    def icons_imp(self) -> List[str]:
        return []

    def display_text_imp(self) -> str:
        return ""

    class_dict = {
        '__module__': __name__,
        '__init__': init_imp,
        'releases': releases_imp,
        'accepts': accepts_imp,
        'action': action_imp,
        'add_content': add_content_imp,
        'numeric_state_representation': numeric_state_representation_imp,
        'feature_vector_representation': feature_vector_representation_imp,
        'state_length': state_length_imp,
        'feature_vector_length': feature_vector_length_imp,
        'file_name': file_name_imp,
        'icons': icons_imp,
        'display_text': display_text_imp
    }
    cls = type(derived_name, (StaticObject, ContentObject, ActionObject), class_dict)
    return cls


PlateDispenser = CreateDispenserClass(Plate, "PlateDispenser", "DispenserPlate")
AppleDispenser = CreateDispenserClass(Apple, "AppleDispenser", "DispenserApple")
OnionDispenser = CreateDispenserClass(Onion, "OnionDispenser", "DispenserOnion")
BananaDispenser = CreateDispenserClass(Banana, "BananaDispenser", "DispenserBanana")
CarrotDispenser = CreateDispenserClass(Carrot, "CarrotDispenser", "DispenserCarrot")
TomatoDispenser = CreateDispenserClass(Tomato, "TomatoDispenser", "DispenserTomato")
LettuceDispenser = CreateDispenserClass(Lettuce, "LettuceDispenser", "DispenserLettuce")
WatermelonDispenser = CreateDispenserClass(Watermelon, "WatermelonDispenser", "DispenserWatermelon")
BreadDispenser = CreateDispenserClass(Bread, "BreadDispenser", "DispenserBread")
PastaDispenser = CreateDispenserClass(Pasta, "PastaDispenser", "DispenserPenne")
EggDispenser = CreateDispenserClass(Egg, "EggDispenser", "DispenserEgg")
IceDispenser = CreateDispenserClass(Ice, "IceDispenser", "DispenserIce")
StrawberryDispenser = CreateDispenserClass(Strawberry, "StrawberryDispenser", "DispenserStrawberry")

GAME_CLASSES = [m[1] for m in inspect.getmembers(sys.modules[__name__], inspect.isclass) if m[1].__module__ == __name__]

StringToClass = {game_cls.__name__: game_cls for game_cls in GAME_CLASSES}
ClassToString = {game_cls: game_cls.__name__ for game_cls in GAME_CLASSES}


def get_recursive_content_objects(obj):
    """Backported from drother moop branch"""
    if isinstance(obj, ContentObject):
        other_objs = []
        for cont_obj in obj.content:
            other_objs.extend(get_recursive_content_objects(cont_obj))
        return [obj] + other_objs
    else:
        return [obj]
