import math
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from omegaconf import DictConfig, OmegaConf
from pettingzoo.utils import agent_selector

from ...common import ConcurrentEnv, PerturbationEnv, HarvestingObs
from pettingzoo.utils import agent_selector
from simulation.persona.common import (
    PersonaAction,
    PersonaActionChat,
    PersonaActionHarvesting,
    PersonaEvent,
    PersonaIdentity,
)


def units_trash(num):
    return f"Before everyone takes out trash, there are {num} units of trash in the house."


def units_caught(agent_name, wanted, took):
    return (
        f"{agent_name} wanted to take out {wanted} units of trash, and took out {took} units."
    )


def univ(sustainability_threshold):
    return f"Given the current situation, if everyone takes out less than {sustainability_threshold} units, the house will be overfull with trash by next month."


def units_caught_home(agent_name, took):
    return f"This month, {agent_name} took out {took} units of trash."


class TrashConcurrentEnv(ConcurrentEnv):
    def __init__(
        self, cfg: DictConfig, experiment_storage: str, map_id_to_name: dict[str, str]
    ) -> None:
        super().__init__(cfg, experiment_storage, map_id_to_name)
        self.POOL_LOCATION = "lake"

    def _prompt_pool_amount_of_resource(self):
        if self.cfg.harvesting_order == "concurrent":
            num = self.internal_global_state["resource_in_pool"]
        else:
            raise ValueError(f"Unknown trash order: {self.cgf.harvesting_order}")
        return units_trash(num)

    def _prompt_pool_amount_of_resource_after_harvesting(self, agent):
        wanted = self.internal_global_state["wanted_resource"][agent]
        caught = self.internal_global_state["last_collected_resource"][agent]
        agent_name = self.agent_id_to_name[agent]
        return units_caught(agent_name, wanted, caught)

    def _prompt_universalization(self, sustainability_threshold):
        return univ(sustainability_threshold)
    
    def step(self, action: PersonaAction) -> tuple[str, HarvestingObs, dict, dict]:
        if self.terminations[self.agent_selection]:
            return

        assert action.agent_id == self.agent_selection

        if self.phase == self.POOL_LOCATION:
            assert action.location == self.POOL_LOCATION
            assert type(action) == PersonaActionHarvesting
            self._step_lake_bet(action)
        elif self.phase == "pool_after_harvesting":
            assert action.location == self.POOL_LOCATION
            self._step_pool_after_harvesting(action)
        elif self.phase == "restaurant":
            assert action.location == "restaurant"
            self._step_restaurant(action)
        elif self.phase == "home":
            assert action.location == "home"
            self._step_home(action)
            if self._agent_selector.is_last():
                self.save_log()
                self.num_round += 1
                self.phase = self._phase_selector.next()

                # We want to see also the discussion in case no fish remain
                self.terminations = {
                    agent: (
                        (self.num_round > 0 and
                        self.internal_global_state["resource_in_pool"]
                        > 95) # TRASH ONLY, otherwise < 5  # less than 5 fish remain, so we collapse
                        or self.num_round >= self.cfg.max_num_rounds
                    )
                    for agent in self.agents
                }

                self.internal_global_state["resource_in_pool"] = min(
                    self.cfg.initial_resource_in_pool,
                    self.internal_global_state["resource_in_pool"] + 50, #TRAHS ONLY, otherwise * 2
                )  # Increase the fish in the lake, but cap at 100
                self.internal_global_state["resource_before_harvesting"] = (
                    self.internal_global_state["resource_in_pool"]
                )
                self.internal_global_state["sustainability_threshold"] = int(
                    50 # TRASH ONLY, otherwise (self.internal_global_state["resource_in_pool"] // 2)
                    // self.internal_global_state["num_agents"]
                )
                if self.cfg.harvesting_order == "random-sequential":
                    agents = list(np.random.permutation(self.agents))
                    self._agent_selector = agent_selector(agents)
            self.agent_selection = self._agent_selector.next()

        return (
            self.agent_selection,
            self._observe(self.agent_selection),
            self.rewards,
            self.terminations,
        )


class TrashPerturbationEnv(PerturbationEnv):
    def __init__(
        self, cfg: DictConfig, experiment_storage: str, map_id_to_name: dict[str, str]
    ) -> None:
        super().__init__(cfg, experiment_storage, map_id_to_name)
        self.POOL_LOCATION = "lake"

    def _prompt_pool_amount_of_resource(self):
        if self.cfg.harvesting_order == "concurrent":
            num = self.internal_global_state["resource_in_pool"]
        else:
            raise ValueError(f"Unknown trash order: {self.cgf.harvesting_order}")
        return units_trash(num)

    def _prompt_pool_amount_of_resource_after_harvesting(self, agent):
        wanted = self.internal_global_state["wanted_resource"][agent]
        took = self.internal_global_state["last_collected_resource"][agent]
        agent_name = self.agent_id_to_name[agent]
        return units_caught(agent_name, wanted, took)

    def _prompt_universalization(self, sustainability_threshold):
        return univ(sustainability_threshold)

    def _prompt_home_observe_agent_resource(self, agent):
        took = self.internal_global_state["last_collected_resource"][agent]
        agent_name = self.agent_id_to_name[agent]
        return units_caught_home(agent_name, took)
