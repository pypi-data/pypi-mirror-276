import ray
import pickle
import copy
import os
import random

from ml.raylib.environment import RLCEnvironment
from ray.rllib.env.multi_agent_env import make_multi_agent
from ray.rllib.algorithms import ppo
from ray.rllib.algorithms.algorithm import Algorithm
from ray.rllib.algorithms.ppo import PPOConfig, PPO
from ray.rllib.algorithms.ppo import PPOTorchPolicy
from ray import train
from ml.raylib.module_config import agent_to_module_mapping_fn, get_config

from command_line import load_simulation_from_args, make_rlc_argparse

from typing import (
    Any,
    Callable,
    Dict,
    KeysView,
    List,
    Mapping,
    Optional,
    Set,
    Type,
    Union,
)


def train_impl(model, fixed_nets = 0):
    for _ in range(1000000000):
        with open(f"./list_of_fixed.txt", "wb+") as f:
          if not os.path.exists(f"./net_p3_{fixed_nets}"):
            os.makedirs(f"./net_p3_{fixed_nets}")
          if not os.path.exists(f"./net_p4_{fixed_nets}"):
            os.makedirs(f"./net_p4_{fixed_nets}")
          model.workers.local_worker().module["p1"].save_state(f"./net_p3_{fixed_nets}")
          model.workers.local_worker().module["p2"].save_state(f"./net_p4_{fixed_nets}")
          fixed_nets = fixed_nets + 1
          pickle.dump(fixed_nets, f)
        for x in range(20):
          for i in range(10):
            print(x, i)
            train.report(model.train())
            if fixed_nets != 0:
              model.workers.local_worker().module["p3"].load_state(f"./net_p3_{random.choice(range(fixed_nets))}")
              model.workers.local_worker().module["p4"].load_state(f"./net_p4_{random.choice(range(fixed_nets))}")
              model.workers.sync_weights(policies=["p3", "p4"])
        model.save(f"./checkpoint")

def load(model):
    model.restore(f"./checkpoint/")
    model.workers.local_worker().module["p1"].load_state(f"./checkpoint/learner/module_state/p1/module_state_dir/")
    model.workers.local_worker().module["p2"].load_state(f"./checkpoint/learner/module_state/p2/module_state_dir/")
    model.workers.sync_weights(policies=["p1", "p2"])
    with open(f"./list_of_fixed.txt", "rb") as f:
      return pickle.load(f)
    return 0

def tuner_run(config):
    config = PPOConfig().update_from_dict(config)
    model = config.build()
    #train_impl(model, load(model))
    train_impl(model, 0)
    model.save()
    model.stop()

def get_trainer(output_path):
  def single_agent_train(config):
    config = PPOConfig().update_from_dict(config)
    model = config.build()
    for _ in range(1000000000):
        for i in range(10):
            train.report(model.train())
        model.save(output_path)
    model.save()
    model.stop()
  return single_agent_train

def main():
    parser = make_rlc_argparse("train", description="runs a action of the simulation")
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        nargs="?",
        help="path where to write the output",
        default="",
    )
    parser.add_argument("--one-agent-per-player", action="store_true", default=True)

    args = parser.parse_args()
    sim, wrapper_path, tmp_dir = load_simulation_from_args(args)

    from ray import air, tune
    ppo_config, hyperopt_search = get_config(wrapper_path, 1 if not args.one_agent_per_player else sim.module.functions.get_num_players().value)
    tune.register_env('rlc_env', lambda config: RLCEnvironment(wrapper_path=wrapper_path))

    stop = {
        "timesteps_total": 1e15,
        # "episode_reward_mean": 2,  # divide by num_agents for actual reward per agent
    }


    ray.init(num_cpus=12, num_gpus=1)
    # resumption_dir = os.path.abspath("./results")
    resources = PPO.default_resource_request(ppo_config)
    tuner = tune.Tuner(
        tune.with_resources(get_trainer(args.output), resources=resources),
        param_space=ppo_config.to_dict(),
        tune_config=ray.tune.TuneConfig(num_samples=1, search_alg=hyperopt_search),
        run_config=air.RunConfig(
            stop=stop,
            verbose=2,
            # storage_path=resumption_dir
        ),
    )

    results = tuner.fit()



if __name__ == "__main__":
    main()
