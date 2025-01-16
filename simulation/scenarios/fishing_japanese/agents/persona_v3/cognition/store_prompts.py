from simulation.persona.common import PersonaIdentity
from simulation.persona.memory.associative_memory import (
    Action,
    Chat,
    Event,
    Thought,
)
from simulation.utils import ModelWandbWrapper
from pathfinder import assistant, system, user

from .utils import get_sytem_prompt


def prompt_importance_chat(
    model: ModelWandbWrapper, persona: PersonaIdentity, chat: Chat
):
    lm = model.start_chain(persona.name, "cognition_retrieve", "prompt_importance_chat")

    with user():
        lm += f"{get_sytem_prompt(persona)}\n"
        lm += (
            "タスク 会話の重要性を評価する "
            "1から10までの尺度で、1は平凡な会話（例：日常的な朝の挨拶）、"
            "10は非常にインパクトのある議論（例：別れ話や深刻な口論）を表し、"
            f"{persona.name}の以下の会話の重要性を評価する。"
        )
        lm += f"\n評価するための会話:\n{chat.description}\n\n"

    with assistant():
        lm += "評価（1～10）： "
        lm = model.select(
            lm,
            options=[str(i) for i in range(1, 11)],
            default_value="5",  # Assuming a neutral default value for guidance
            name="significance",
        )
        significance = int(lm["significance"])

    model.end_chain(persona.name, lm)
    return significance


def prompt_importance_event(
    model: ModelWandbWrapper, persona: PersonaIdentity, event: Event
):
    lm = model.start_chain(persona.name, "cognition_perceive", "relevancy_event")

    with user():
        lm += f"{get_sytem_prompt(persona)}\n"
        lm += (
            "課題 ある出来事の重要性を評価する "
            "1から10までの尺度で、1は日常的で平凡な活動（例：歯磨き、ベッドメイキング）を表し、"
            "10は極めて感情的に重要な出来事（例：恋愛の破局、大学の合格通知を受け取る）を意味します。"
            f"{persona.name}の視点から、以下の出来事を評価してください。"
        )
        lm += f"\n評価するイベント {event.description}\n"

    with assistant():
        lm += "評価（1～10）： "
        lm = model.select(
            lm,
            options=[str(i) for i in range(1, 11)],
            name="significance",
            default_value="5",  # assuming a neutral default value for better user guidance
        )
        importance_score = int(lm["significance"])

    model.end_chain(persona.name, lm)
    return importance_score


def prompt_importance_thought(
    model: ModelWandbWrapper, persona: PersonaIdentity, thought: Thought
):
    lm = model.start_chain(
        persona.name, "cognition_retrieve", "prompt_importance_thought"
    )

    with user():
        lm += f"{get_sytem_prompt(persona)}\n"
        lm += (
            "タスク ある思考の重要性を評価する"
            "1～10の尺度で、1は日常的な思考（例：家事をしなければならない）、"
            "10は非常に重要な思考（例：キャリアへの願望、深い感情）を表し、"
            f"{persona.name}の視点から以下の思考を評価する。"
        )
        lm += f"\nThought to rate:\n{thought.description}\n\n"

    with assistant():
        lm += "評価（1～10）： "
        lm = model.select(
            lm,
            options=[str(i) for i in range(1, 11)],
            default_value="5",  # Assuming a neutral default value for guidance
            name="significance_rating",
        )
        significance_rating = int(lm["significance_rating"])

    model.end_chain(persona.name, lm)
    return significance_rating


def prompt_importance_action(
    model: ModelWandbWrapper, persona: PersonaIdentity, action: Action
):
    lm = model.start_chain(
        persona.name, "cognition_retrieve", "prompt_importance_action"
    )

    with user():
        lm += f"{get_sytem_prompt(persona)}\n"
        lm += (
            "タスク 行動の重要性を評価する"
            "1～10の尺度で、1は日常的な行動（例：家事）、"
            "10は重要性や影響力の大きい行動（例：進路決定、深い感情の表現）を表し、"
            f"{persona.name}の以下の行動の重要性を評価してください。"
        )
        lm += f"\n評価するアクション\n{action.description}\n\n"

    with assistant():
        lm += "評価（1～10）： "
        lm = model.select(
            lm,
            options=[str(i) for i in range(1, 11)],
            default_value="5",  # Setting a neutral default value for guidance
            name="significance_rating",
        )
        significance_rating = int(lm["significance_rating"])

    model.end_chain(persona.name, lm)
    return significance_rating


def prompt_text_to_triple(model: ModelWandbWrapper, text: str):
    lm = model.start_chain("framework", "cognition_retrieve", "prompt_text_to_triple")

    with user():
        lm += f"フレーズを主語、述語、目的語に分割する： {text}\n"

    with assistant():
        lm += "テーマ: "
        lm = model.gen(lm, name="subject", stop_regex=r"\n")
        lm += "\n述語： "
        lm = model.gen(lm, name="predicate", stop_regex=r"\n")
        lm += "\nオブジェクトがある： "
        lm = model.gen(lm, name="object", stop_regex=r"\n")

    model.end_chain("framework", lm)
    return lm["subject"], lm["predicate"], lm["object"]
