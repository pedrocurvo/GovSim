from datetime import datetime

import numpy as np

from simulation.persona.common import PersonaIdentity
from simulation.utils import ModelWandbWrapper
from pathfinder import assistant, system, user

from .utils import (
    consider_identity_persona_prompt,
    conversation_to_string_with_dash,
    get_sytem_prompt,
    list_to_comma_string,
    list_to_string_with_dash,
    location_time_info,
    memory_prompt,
    reasoning_steps_prompt,
)


def prompt_converse_utterance_in_group(
    model: ModelWandbWrapper,
    init_persona: PersonaIdentity,
    target_personas: list[PersonaIdentity],
    init_retrieved_memory: list[str],
    current_location: str,
    current_time: datetime,
    current_context: str,
    current_conversation: list[tuple[str, str]],
) -> tuple[str, bool, str]:
    lm = model.start_chain(
        init_persona.name, "cognition_converse", "converse_utterance"
    )

    with user():
        lm += f"{get_sytem_prompt(init_persona)}\n"
        lm += location_time_info(current_location, current_time)
        # List key memories of the initial persona
        lm += memory_prompt(init_persona, init_retrieved_memory)
        # Provide the current context
        lm += "\n"
        # lm += f"Current context: {current_context}\n\n"
        # Describe the group chat scenario
        lm += (
            f"シナリオ: {list_to_comma_string([t.name for t in target_personas])}さんが"
            "グループチャットに参加している。"
        )
        lm += "\nこれまでの会話:\n"
        lm += f"{conversation_to_string_with_dash(current_conversation)}\n\n"
        # Define the task for the language model
        lm += (
            f"タスク: グループチャットで次に何を話す？"
            "会話が自然に流れ、繰り返しがないようにする。 "
            "あなたの返答が会話を完結させるかどうかを判断する。"
            "そうでない場合は、次のスピーカーを指名する。\n\n"
        )
        # Define the format for the output
        REPONSE = "反応: "
        ANSWER_STOP = "私が会話を終える場合の結論: "
        NEXT_SPEAKER = "次に話す人: "

        lm += "出力フォーマット：\n"
        lm += REPONSE + "[埋める]\n"
        lm += ANSWER_STOP + "[はい／いいえ]\n"
        lm += NEXT_SPEAKER + "[埋める]\n"
    with assistant():
        lm += REPONSE
        lm = model.gen(
            lm,
            name="utterance",
            default_value="",
            stop_regex=r"私による会話の結論：",  # name can be mispelled by LLM sometimes
        )
        utterance = lm["utterance"].strip()
        if len(utterance) > 0 and utterance[-1] == '"' and utterance[0] == '"':
            utterance = utterance[1:-1]
        lm += ANSWER_STOP
        lm = model.select(
            lm,
            name="utterance_ended",
            #a lot of yes no Check
            options=["はい", "いいえ"],
            default_value="はい",
        )
        utterance_ended = lm["utterance_ended"].lower() == "はい"

        if utterance_ended:
            next_speaker = None
        else:
            lm += "\n"
            lm += NEXT_SPEAKER
            options = [t.name for t in target_personas]
            lm = model.select(
                lm,
                name="next_speaker",
                options=options,
                default_value=options[0],
            )
            assert lm["next_speaker"] in options
            next_speaker = lm["next_speaker"]

    model.end_chain(init_persona.name, lm)
    return utterance, utterance_ended, next_speaker, lm.html()


def prompt_summarize_conversation_in_one_sentence(
    model: ModelWandbWrapper,
    conversation: list[tuple[str, str]],
):
    lm = model.start_chain(
        "framework",
        "cognition_converse",
        "prompt_summarize_conversation_in_one_sentence",
    )

    with user():
        lm += f"会話:\n"
        lm += f"{conversation_to_string_with_dash(conversation)}\n\n"
        lm += "上記の会話を一文で要約してください。"
    with assistant():
        lm = model.gen(lm, name="summary", default_value="", stop_regex=r"\.")
        summary = lm["summary"] + "."

    model.end_chain("framework", lm)
    return summary, lm.html()
