from simulation.persona.cognition.plan import PlanComponent
from simulation.utils import ModelWandbWrapper
from pathfinder import assistant, system, user


class TrashPlanComponent(PlanComponent):
    def __init__(self, model: ModelWandbWrapper):
        super().__init__(model)