from simulation.persona.common import PersonaIdentity
from simulation.utils import ModelWandbWrapper
from pathfinder import assistant, system, user

from .utils import (
    conversation_to_string_with_dash,
    get_sytem_prompt,
    list_to_comma_string,
    list_to_string_with_dash,
    numbered_list_of_strings,
    numbered_memory_prompt,
    reasoning_steps_prompt,
)


def prompt_insight_and_evidence(
    model: ModelWandbWrapper, persona: PersonaIdentity, statements: list[str]
):
    lm = model.start_chain(
        persona.name, "cognition_retrieve", "prompt_insight_and_evidence"
    )

    with user():
        lm += f"{get_sytem_prompt(persona)}\n"
        lm += f"{numbered_memory_prompt(persona, statements)}\n"
        lm += (
            f"上記の記述から、どのようなハイレベルな洞察が得られますか？"
            "(例：洞察（1,5,3のため）"
        )
    with assistant():
        acc = []
        lm += f"1."
        for i in range(len(statements)):
            lm = model.gen(
                lm,
                name=f"evidence_{i}",
                stop_regex=rf"{i+2}\.|\(",
                save_stop_text=True,
            )
            if lm[f"evidence_{i}"].endswith(f"{i+2}."):
                evidence = lm[f"evidence_{i}"][: -len(f"{i+2}.")]
                acc.append(evidence.strip())
                continue
            else:
                evidence = lm[f"evidence_{i}"]
                if evidence.endswith("("):
                    evidence = lm[f"evidence_{i}"][: -len("(")]
                lm = model.gen(
                    lm,
                    name=f"evidence_{i}_justification",
                    stop_regex=rf"{i+2}\.",
                    save_stop_text=True,
                )
                if lm[f"evidence_{i}_justification"].endswith(f"{i+2}."):
                    acc.append(evidence.strip())
                    continue
                else:
                    # no more evidence
                    acc.append(evidence.strip())
                    break
        model.end_chain(persona.name, lm)

    return acc


def prompt_planning_thought_on_conversation(
    model: ModelWandbWrapper,
    persona: PersonaIdentity,
    conversation: list[tuple[str, str]],
) -> str:
    lm = model.start_chain(
        persona.name, "cognition_retrieve", "prompt_planning_thought_on_conversation"
    )

    with user():
        lm += f"{get_sytem_prompt(persona)}\n"
        lm += f"会話だ：\n"
        lm += f"{conversation_to_string_with_dash(conversation)}\n"
        lm += (
            "会話の中で、プランニングのために覚えておく必要があることがあれば、"
            "あなた自身の視点から、全文で書き出してください。"
        )
    with assistant():
        lm = model.gen(lm, name="planning_thought", stop_regex=r"\.")
        res = lm["planning_thought"]

    model.end_chain(persona.name, lm)
    return res


def prompt_memorize_from_conversation(
    model: ModelWandbWrapper,
    persona: PersonaIdentity,
    conversation: list[tuple[str, str]],
) -> str:
    lm = model.start_chain(
        persona.name, "cognition_retrieve", "prompt_memorize_from_conversation"
    )

    with user():
        lm += f"{get_sytem_prompt(persona)}\n"
        lm += f"会話だ：\n"
        lm += f"{conversation_to_string_with_dash(conversation)}\n"
        lm += (
            "会話の中で、プランニングのために覚えておく必要があることがあれば、"
            "あなた自身の視点から、全文で書き出してください。"
        )
    with assistant():
        lm = model.gen(lm, name="memorize", stop_regex=r"\.")
        res = lm["memorize"]

    model.end_chain(persona.name, lm)
    return res


def prompt_find_harvesting_limit_from_conversation(
    model: ModelWandbWrapper,
    conversation: list[tuple[str, str]],
) -> tuple[int, str]:
    lm = model.start_chain(
        "framework",
        "cognition_refelct",
        "prompt_find_harvesting_limit_from_conversation",
    )

    with user():
        lm += (
            "次の会話で、参加者は自分たちの漁業活動や活動内容、釣った魚の重さについて話し合う。"
            "具体的な漁獲制限について明確な合意があったかどうかを判断する。"
            "この会話の中で、グループが守ることに合意した漁獲制限の数値について、"
            "直接的な言及や合意があったかどうかを探してください。"
        )
        lm += f"\n\会話だ：\n"
        lm += f"{conversation_to_string_with_dash(conversation)}\n"
        lm += "会話の中で合意された一人当たりの具体的な漁獲制限をご記入ください。制限に合意されなかった場合は、N/A とお答えください。"
        lm += reasoning_steps_prompt()
        lm += ' 最終的な答えは「回答:」の後に書く。'

    option_fish_num = range(0, 101)
    with assistant():
        lm = model.gen(
            lm,
            "reasoning",
            stop_regex=f"回答:",
        )
        lm += f"回答: "
        lm = model.find(
            lm,
            regex=r"\d+",
            default_value="-1",
            name="num_resource",
        )

        resource_limit_agreed = int(lm["num_resource"]) != -1

        if resource_limit_agreed:
            res = int(lm["num_resource"])
            model.end_chain("framework", lm)
            return res, lm.html()
        else:
            model.end_chain("framework", lm)
            return None, lm.html()
