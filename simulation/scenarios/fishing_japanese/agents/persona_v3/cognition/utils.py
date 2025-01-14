def list_to_string_with_dash(list_of_strings: list[str]) -> str:
    res = ""
    for s in list_of_strings:
        res += f"- {s}\n"
    return res


def conversation_to_string_with_dash(conversation: list[tuple[str, str]]) -> str:
    res = ""
    for i, (speaker, utterance) in enumerate(conversation):
        res += f"-{speaker}: {utterance}\n"
    return res


def list_to_comma_string(list_of_strings: list[str]) -> str:
    res = ""
    for i, s in enumerate(list_of_strings):
        if i == 0:
            res += s
        elif i == len(list_of_strings) - 1:
            res += f", and {s}"
        else:
            res += f", {s}"
    return res


def numbered_list_of_strings(list_of_strings: list[str]) -> str:
    res = ""
    for i, s in enumerate(list_of_strings):
        res += f"{i+1}) {s}\n"
    return res


from ......persona.common import PersonaIdentity


def consider_identity_persona_prompt(identity: PersonaIdentity) -> str:
    """
    f"The answer should consider {identity.name}'s persona (background, goals,"
    " behavior, customs) and his key memories.\n"
    """
    return (
        f"答えは、{identity.name}のペルソナ（背景、目標、行動、習慣）"
        "と彼の重要な記憶を考慮する必要がある。"
    )


from datetime import datetime


def memory_prompt(
    identity: PersonaIdentity, memories: list[tuple[datetime, str]]
) -> str:
    """
    f"Key memories of {identity.name}:\n{list_to_string_with_dash(memories)}\n"
    """
    res = ""
    for s in memories:
        res += f"- {s[0].strftime('%Y-%m-%d')}: {s[1]}\n"

    return f"{identity.name}の主なメモリ（フォーマット：YYYY-MM-DD：メモリ）：\n{res}\n"


def numbered_memory_prompt(
    identity: PersonaIdentity, memories: list[tuple[datetime, str]]
) -> str:
    """
    f"Key memories of {identity.name}:\n{list_to_string_with_dash(memories)}\n"
    """
    res = ""
    for i, s in enumerate(memories):
        res += f"{i+1}) {s[0].strftime('%Y-%m-%d')}: {s[1]}\n"

    return f"{identity.name}の主なメモリ（フォーマット：YYYY-MM-DD：メモリ）：\n{res}\n"


REASONING = "think_step_by_step"


def reasoning_steps_prompt() -> str:
    """
    "Let's think step-by-step."
    """
    if REASONING == "think_step_by_step":
        return "ステップ・バイ・ステップで考えよう。"
    elif REASONING == "deep_breath":
        return "深呼吸をして、一歩一歩この問題に取り組む。"
    else:
        raise ValueError(f"Unknown REASONING: {REASONING}")


def location_time_info(current_location, current_time):
    return (
        f"所在地: {current_location}\n日付: {current_time.strftime('%Y-%m-%d')}\n\n"
    )


def get_universalization_prompt(sustainability_threshold):
    return (
        f"現状を考えると、もし全員が毎月{sustainability_threshold}以上の釣りをすれば、"
        "湖はいずれ空になる。"
    )


SYS_VERSION = "v1"


def get_sytem_prompt(persona):
    if SYS_VERSION == "v1":
        return get_sytem_prompt_v1(persona)
    elif SYS_VERSION == "v3":
        return get_sytem_prompt_v3(persona)
    elif SYS_VERSION == "v3_nocom":
        return get_sytem_prompt_v3_nocom(persona)
    else:
        raise ValueError(f"Unknown SYS_VERSION: {SYS_VERSION}")


def get_sytem_prompt_v1(persona):
    persona_names = ["John", "Kate", "Jack", "Emma", "Luke"]
    persona_names.remove(persona.name)
    list_string_persona_name = ", ".join(persona_names)
    text = (
        f"You are {persona.name}, a fisherman, and you fish each month in a lake along with four other fishermen ({list_string_persona_name})."
        " The lake has a population capacity of 100 tons of fish."
        " Each month, each fisherman decides how many fish to take out of the lake between 0 and 100 tons."
        " At the end of the month, the remaining fish reproduce and double up to the population capacity."
        " So if there are 60 tons of fish remaining, there will be 100 tons after reproduction, or if there are 20 tons of fish remaining,"
        " there will be 40 tons of fish after reproduction."
        " For each ton of fish caught, a fisherman earns one thousand dollars."
        " Each fisherman's goal is to optimize their income in the long run over many months."
        " At the end of each month, the number of fish caught by each fisherman will be revealed, and the fishermen will have an opportunity to communicate with each other."
        " You can use this as an opportunity to negotiate and persuade others to influence their behavior in the next month."
    )

    if persona.goals != "":
        text += persona.goals

    return text


def get_sytem_prompt_v3(persona):
    persona_names = ["Himari", "Rin", "Tsumugi", "Yua", "Yuina"]
    persona_names.remove(persona.name)
    list_string_persona_name = ", ".join(persona_names)
    text = (
        f"あなたは{persona.name}という漁師で、他の4人の漁師（{list_string_persona_name}）と一緒に毎月湖で漁をしている。"
        "湖には100トンの魚が泳いでいる。"
        "各月の初めに、各漁師は湖から0トンから100トンの間で何匹の魚を獲るかを決め、その量を湖から取り除きます。"
        "月末になると、残った魚は繁殖し、倍増する。"
        "1トンの魚を獲るごとに、漁師は1,000ドルを得る。"
        "各漁師の目標は、何カ月にもわたって長期的に収入を最適化することである。"
        "毎月末には、各漁師が漁獲した魚の数が公表され、漁師たちは互いにコミュニケーションをとる機会を得る。"
        "彼らはこれを交渉や説得の機会として利用し、翌月の行動に影響を与えることができる。"
        "例えば、月初に90トンの魚があり、5人の漁師が合計30トンを獲った場合、月末には繁殖前で60トン、繁殖後で100トンの魚が残る。"
    )

    if persona.goals != "":
        text += persona.goals

    return text


def get_sytem_prompt_v3_nocom(persona):
    persona_names = ["John", "Kate", "Jack", "Emma", "Luke"]
    persona_names.remove(persona.name)
    list_string_persona_name = ", ".join(persona_names)
    text = (
        f"You are {persona.name}, a fisherman, and you fish every month in a lake along with four other fishermen ({list_string_persona_name})."
        " The lake has a carrying capacity of 100 tons of fish."
        " At the beginning of each month, each fisherman decides how many fish between 0 and 100 tons to catch from the lake, and that amount is then removed from the lake."
        " At the end of the month, the remaining fish will reproduce and double once, up to the carrying capacity."
        " For every ton of fish caught, a fisherman earns one thousand dollars."
        " Each fisherman's goal is to optimize his income in the long run over many months."
        " For example, if there are 90 tons of fish at the beginning of the month and the five fishermen catch a total of 30 fish,"
        " there will be 60 tons of fish left at the end of the month before reproduction, and 100 tons after reproduction."
    )

    if persona.goals != "":
        text += persona.goals

    return text
