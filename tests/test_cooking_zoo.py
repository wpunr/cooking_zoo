import pytest
import time

import cooking_zoo.cooking_book.recipe
from cooking_zoo.cooking_world.abstract_classes import DynamicObject, StaticObject, ContentObject
from cooking_zoo.cooking_world.constants import ChopFoodStates, ToasterFoodStates
from cooking_zoo.cooking_world.cooking_world import CookingWorld
from cooking_zoo.cooking_world.world_objects import Lettuce, Tomato, Plate, Deliversquare, Bread, Counter, Agent
from cooking_zoo.cooking_book.recipe import Recipe
from cooking_zoo.cooking_book.recipe_drawer import TomatoLettucePlate, ChoppedLettuce, ChoppedTomato, \
    TomatoLettuceSalad, ChoppedOnion, DEFAULT_NUM_GOALS, ChoppedBread, ToastedBread, ToastedBreadPlate
from cooking_zoo.environment.cooking_env import parallel_env
from cooking_zoo.cooking_agents.cooking_agent import CookingAgent
from cooking_zoo.environment.manual_policy import ManualPolicy


def example_environment(agents_arms=None):
    num_agents = 1
    max_steps = 50
    render = False
    obs_spaces = ["symbolic"]
    action_scheme = "scheme3"
    meta_file = "example"
    level = "coop_test"
    recipes = ["TomatoLettuceSalad"]
    end_condition_all_dishes = True
    agent_visualization = ["human"]
    reward_scheme = {"recipe_reward": 20, "max_time_penalty": -5, "recipe_penalty": -40, "recipe_node_reward": 0}
    env = parallel_env(level=level, meta_file=meta_file, num_agents=num_agents, max_steps=max_steps,
                       recipes=recipes,
                       agent_visualization=agent_visualization, obs_spaces=obs_spaces,
                       end_condition_all_dishes=end_condition_all_dishes, action_scheme=action_scheme,
                       render=render,
                       reward_scheme=reward_scheme, agents_arms=agents_arms)
    return env, recipes

class TestCookingZoo_heuristic_agent:
    def test_cooking_zoo(self):
        """
        Straight copy of demo_heuristic_agent.py

        See that the environment inits without issue and  heuristic agent runs in a reasonable time.
        """
        env, recipes = example_environment()

        cooking_agent = CookingAgent(recipes[0], "agent-1")

        observations, info = env.reset()

        env.render()

        terminations = {"player_0": False}
        cumulative = 0
        start = time.time()
        while not all(terminations.values()):
            action = {"player_0": cooking_agent.step(observations['player_0'])}
            observations, rewards, terminations, truncations, infos = env.step(action)
            for val in rewards.values():
                cumulative += val
            env.render()
        print(f'total: {cumulative}')
        print(f'time: {time.time() - start} steps: {env.unwrapped.t}')
        assert env.unwrapped.t < 40

    def test_two_arms(self):
        """Similar to test_cooking_zoo, but with 2 arms. Just make sure that it runs,
        even though heuristic_agent isn't aware of this feature yet."""
        env, recipes = example_environment(agents_arms=[2])

        cooking_agent = CookingAgent(recipes[0], "agent-1")

        observations, info = env.reset()

        env.render()

        terminations = {"player_0": False}
        cumulative = 0
        start = time.time()
        while not all(terminations.values()):
            action = {"player_0": cooking_agent.step(observations['player_0'])}
            observations, rewards, terminations, truncations, infos = env.step(action)
            for val in rewards.values():
                cumulative += val
            env.render()
        print(f'total: {cumulative}')
        print(f'time: {time.time() - start} steps: {env.unwrapped.t}')
        assert env.unwrapped.t < 40

class TestCookingZoo:
    def test_manual_policy(self):
        env, _ = example_environment()
        assert ManualPolicy(env, agent_id="player_0")

    def test_get_recursive_content_objects(self):
        from cooking_zoo.cooking_world.world_objects import get_recursive_content_objects
        lettuce = Lettuce((0, 0))
        tomato = Tomato((0, 0))
        plate = Plate((0, 0))
        deliver = Deliversquare((0, 0))

        lettuce.chop()
        tomato.chop()
        plate.add_content(lettuce)
        plate.add_content(tomato)
        deliver.add_content(plate)

        assert set(get_recursive_content_objects(lettuce)) == set([lettuce])
        assert set(get_recursive_content_objects(tomato)) == set([tomato])
        assert set(get_recursive_content_objects(plate)) == set([plate, lettuce, tomato])
        assert set(get_recursive_content_objects(deliver)) == set([deliver, plate, lettuce, tomato])

        foo = "not an obj"
        assert set(get_recursive_content_objects(foo)) == set([foo])

    @pytest.mark.skip(reason="Eyeball it in gameplay")
    def test_AbsorbingDeliversquare(self):
        pass

    def test_recipe_checker(self):
        lettuce = Lettuce((0, 0))
        tomato = Tomato((0, 0))
        plate = Plate((0, 0))
        deliver = Deliversquare((0, 0))
        objects = [lettuce, tomato, plate, deliver]

        lettuce.chop()
        tomato.chop()
        plate.add_content(lettuce)
        plate.add_content(tomato)
        deliver.add_content(plate)

        def check_recipe(node):
            recipe = Recipe(node, DEFAULT_NUM_GOALS)
            recipe.update_recipe_state(objects)
            return recipe.completed()

        assert isinstance(check_recipe(ChoppedLettuce), bool)
        assert check_recipe(ChoppedLettuce) == True
        assert check_recipe(ChoppedTomato) == True
        assert check_recipe(TomatoLettucePlate) == True
        assert check_recipe(TomatoLettuceSalad) == True
        assert check_recipe(ChoppedOnion) == False

        objects = [lettuce, tomato, plate]
        assert check_recipe(TomatoLettucePlate) == True
        assert check_recipe(TomatoLettuceSalad) == False

    def test_bread_types(self):
        bread = Bread((0, 0))
        bread2 = Bread((0, 0))
        plate = Plate((0, 0))
        objects = [bread]

        def check_recipe(node):
            recipe = Recipe(node, DEFAULT_NUM_GOALS)
            recipe.update_recipe_state(objects)
            return recipe.completed()

        assert check_recipe(ChoppedBread) == False
        assert check_recipe(ToastedBread) == False
        assert check_recipe(ToastedBreadPlate) == False

        bread.chop()
        assert check_recipe(ChoppedBread) == True
        assert check_recipe(ToastedBread) == False

        bread.toast_state = ToasterFoodStates.TOASTED
        assert check_recipe(ChoppedBread) == True
        assert check_recipe(ToastedBread) == True

        # needs to have both slices
        plate.add_content(bread)
        objects = [plate, bread]
        assert check_recipe(ToastedBreadPlate) == False

        bread2.chop()
        bread2.toast_state = ToasterFoodStates.TOASTED
        objects = [bread2]
        assert check_recipe(ToastedBread) == True

        plate.add_content(bread2)
        objects = [plate, bread, bread2]
        assert check_recipe(ToastedBreadPlate) == True

        # needs to be toasted and chopped
        bread = Bread((0, 0))
        bread.toast_state = ToasterFoodStates.TOASTED
        objects = [bread]
        assert check_recipe(ChoppedBread) == False
        assert check_recipe(ToastedBread) == False

    def test_two_arms_attempt_merge_case_1(self):
        """Case 1"""
        world = CookingWorld(meta_file="example")
        agent = Agent((1, 0), '', 'foo', 2)
        counter = Counter((0, 0))  # static object
        plate = Plate((0, 0))  # dynamic and content object
        lettuce = Lettuce((99, 99))  # dynamic object, agent will hold this
        tomato = Tomato((99, 99))  # dynamic object, agent will also hold this
        lettuce.chop()
        # tomato.chop() don't chop the tomato yet, lettuce will be the only acceptable object to merge

        world.add_object(counter)
        world.add_object(plate)
        world.add_object(lettuce)
        world.add_object(tomato)
        dynamic_objects = world.get_objects_at((0, 0), DynamicObject)
        static_object = world.get_objects_at((0, 0), StaticObject)[0]
        assert plate in dynamic_objects
        assert counter is static_object

        world.attempt_merge(agent, dynamic_objects, (0, 0), static_object)
        assert lettuce not in counter.content  # agent isn't holding plate yet

        assert agent.holding_empty()
        agent.grab(lettuce)
        assert agent.holding_has_free()
        agent.grab(tomato)
        assert lettuce in agent.holding and tomato in agent.holding
        world.attempt_merge(agent, dynamic_objects, (0, 0), static_object)
        assert lettuce in plate.content and tomato not in plate.content

        """Chop tomato too. Now lettuce and tomato are acceptable for plate. This is ambiguous, but we choose the 
        first acceptable, which will be the lettuce. So asserts should be exactly the same."""
        world = CookingWorld(meta_file="example")
        agent = Agent((1, 0), '', 'foo', 2)
        counter = Counter((0, 0))  # static object
        plate = Plate((0, 0))  # dynamic and content object
        lettuce = Lettuce((99, 99))  # dynamic object, agent will hold this
        tomato = Tomato((99, 99))  # dynamic object, agent will also hold this
        lettuce.chop()
        tomato.chop()

        world.add_object(counter)
        world.add_object(plate)
        world.add_object(lettuce)
        world.add_object(tomato)
        dynamic_objects = world.get_objects_at((0, 0), DynamicObject)
        static_object = world.get_objects_at((0, 0), StaticObject)[0]
        assert plate in dynamic_objects
        assert counter is static_object

        world.attempt_merge(agent, dynamic_objects, (0, 0), static_object)
        assert lettuce not in counter.content  # agent isn't holding plate yet

        assert agent.holding_empty()
        agent.grab(lettuce)
        assert agent.holding_has_free()
        agent.grab(tomato)
        assert lettuce in agent.holding and tomato in agent.holding
        world.attempt_merge(agent, dynamic_objects, (0, 0), static_object)
        assert lettuce in plate.content and tomato not in plate.content

    def test_two_arms_attempt_merge_case_2(self):
        world = CookingWorld(meta_file="example")
        agent = Agent((1, 0), '', 'foo', 2)
        counter = Counter((0, 0))  # static object
        tomato = Tomato((99, 99))  # something else for the agent to hold and is in the first slot
        plate = Plate((99, 99))  # dynamic and content object, agent will hold this in the second slot
        lettuce = Lettuce((0, 0))  # dynamic object
        lettuce.chop()

        world.add_object(counter)
        world.add_object(plate)
        world.add_object(lettuce)
        counter.add_content(lettuce)
        dynamic_objects = world.get_objects_at((0, 0), DynamicObject)
        static_object = world.get_objects_at((0, 0), StaticObject)[0]

        world.attempt_merge(agent, dynamic_objects, (0, 0), static_object)
        assert lettuce not in plate.content  # not picked up yet
        agent.grab(tomato)  # make the agent hold something in addition to the plate
        agent.grab(plate)
        assert tomato in agent.holding and plate in agent.holding
        world.attempt_merge(agent, dynamic_objects, (0, 0), static_object)
        assert lettuce in plate.content

    def test_two_arms_attempt_merge_case_3(self):
        world = CookingWorld(meta_file="example")
        agent = Agent((1, 0), '', 'foo', 2)
        counter = Counter((0, 0))  # static object
        tomato = Tomato((99, 99))  # something else for the agent to hold
        lettuce = Lettuce((99, 99))  # dynamic object, what the agent will hold

        world.add_object(counter)
        world.add_object(lettuce)
        dynamic_objects = world.get_objects_at((0, 0), DynamicObject)
        static_object = world.get_objects_at((0, 0), StaticObject)[0]

        world.attempt_merge(agent, dynamic_objects, (0, 0), static_object)
        assert lettuce not in counter.content
        agent.grab(lettuce)
        agent.grab(tomato)  # make the agent hold something in addition to the plate
        world.attempt_merge(agent, dynamic_objects, (0, 0), static_object)
        assert lettuce in counter.content

    def test_agent_holding(self):
        tomato1 = Tomato((0,0))
        tomato2 = Tomato((0, 0))
        tomato3 = Tomato((0, 0))
        numarms = 2
        agent = Agent((1, 0), '', 'foo', numarms)

        agent.grab(tomato1)
        agent.grab(tomato2)
        agent.grab(tomato3)
        assert tomato1 in agent.holding and tomato2 in agent.holding and tomato3 not in agent.holding

        agent.put_down((99,99), tomato1)
        agent.put_down((99,99), tomato2)

        with pytest.raises(ValueError):
            agent.put_down((99,99), tomato3)


    @pytest.mark.skip(reason="TODO")
    def test_two_arms_resolve_primary_interaction(self):
        pass  # run through the test cases and compare the logic with old commit

    @pytest.mark.skip(reason="TODO")
    def test_two_arms_resolve_interaction_special(self):
        pass  # just check the agent.holding_has_free()

    def test_two_arms_explicit_arm(self):
        tomato1 = Tomato((0, 0))
        tomato2 = Tomato((0, 0))
        numarms = 2
        agent = Agent((1, 0), '', 'foo', numarms)

        agent.grab(tomato1, 0)
        assert agent.holding[0] is tomato1

        agent.grab(tomato2, 0)
        assert agent.holding[0] is tomato1
        assert tomato2 not in agent.holding

        agent.grab(tomato2, 1)
        assert agent.holding[1] is tomato2

        agent.put_down((99, 99), tomato1, 1)
        assert agent.holding[0] is tomato1  # used wrong arm

        agent.put_down((99, 99), tomato1, 0)
        assert agent.holding[0] is None and tomato1.location == (99, 99)

    @pytest.mark.skip(reason="TODO")
    def test_two_arms_resolve_primary_interaction_explicit_arm(self):
        pass  # run through the test cases and compare the logic with old commit

    @pytest.mark.skip(reason="TODO")
    def test_two_arms_resolve_interaction_special_explicit_arm(self):
        pass  # just check the agent.holding_has_free()
