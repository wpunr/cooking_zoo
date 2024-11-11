from cooking_zoo.environment.cooking_env import parallel_env
from cooking_zoo.environment.manual_policy import ManualPolicy


num_agents = 2
max_steps = 100
render = True
obs_spaces = ["tensor", "tensor"]
action_scheme = "scheme3"
meta_file = "jaamas3"
level = "jaamas3_tight_super_wide_room"
recipes = ["AppleWatermelon", "AppleWatermelon"]
end_condition_all_dishes = True
agent_visualization = ["robot", "human"]
reward_scheme = {"recipe_reward": 20, "max_time_penalty": -20, "recipe_penalty": 0, "recipe_node_reward": 5}

env = parallel_env(level=level, meta_file=meta_file, num_agents=num_agents, max_steps=max_steps, recipes=recipes,
                   agent_visualization=agent_visualization, obs_spaces=obs_spaces,
                   end_condition_all_dishes=end_condition_all_dishes, action_scheme=action_scheme, render=render,
                   reward_scheme=reward_scheme)

obs, infos = env.reset()

env.render()

action_space = env.action_space(f"{recipes[0]}_0")

manual_policy = ManualPolicy(env, agent_id=f"{recipes[0]}_0")

terminations = {f"{recipes[0]}_0": False}
truncations = {f"{recipes[0]}_0": False}
reward_sum = 0

while not any(terminations.values()) and not any(truncations.values()):
    action = {f"{recipes[0]}_0": action_space.sample(), f"{recipes[1]}_1": manual_policy(f"{recipes[0]}_0")}
    observations, rewards, terminations, truncations, infos = env.step(action)
    reward_sum += rewards[f"{recipes[0]}_0"]
    print(rewards)
    env.render()

print(reward_sum)
