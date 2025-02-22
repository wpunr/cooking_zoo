import pytest
import time

import cooking_zoo.cooking_book.recipe
from cooking_zoo.cooking_world.constants import ChopFoodStates, ToasterFoodStates
from cooking_zoo.cooking_world.world_objects import Lettuce, Tomato, Plate, Deliversquare, Bread
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


class TestCookingZoo:
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
                print(val)
            env.render()
        print(f'total: {cumulative}')
        print(f'time: {time.time() - start} steps: {env.unwrapped.t}')
        assert env.unwrapped.t < 40

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

    def test_two_arms(self):
        """Similar to test_cooking_zoo, but with 2 arms"""
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
                print(val)
            env.render()
        print(f'total: {cumulative}')
        print(f'time: {time.time() - start} steps: {env.unwrapped.t}')
        assert env.unwrapped.t < 40
