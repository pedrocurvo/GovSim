from omegaconf import DictConfig

from ...common import ConcurrentEnv, PerturbationEnv


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
