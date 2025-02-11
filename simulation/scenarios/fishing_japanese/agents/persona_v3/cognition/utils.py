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
    elif SYS_VERSION == "v3_p1":
        return get_sytem_prompt_v3_p1(persona)
    elif SYS_VERSION == "v3_p2":
        return get_sytem_prompt_v3_p2(persona)
    elif SYS_VERSION == "v3_p3":
        return get_sytem_prompt_v3_p3(persona)
    else:
        raise ValueError(f"Unknown SYS_VERSION: {SYS_VERSION}")


def get_sytem_prompt_v1(persona):
    persona_names = ["Himari", "Rin", "Tsumugi", "Yua", "Yuina"]
    persona_names.remove(persona.name)
    list_string_persona_name = ", ".join(persona_names)
    text = (
        f"あなたは{persona.name}という漁師で、他の4人の漁師（{list_string_persona_name}）と一緒に毎月湖で漁をしています。"
        " 湖には100トンの魚が生息している。"
        " 毎月、各漁師は0トンから100トンの間で湖から魚を何匹取るかを決める。"
        " 月末になると、残った魚は繁殖し、個体数が倍増する。"
        " つまり、60トンの魚が残っていれば、繁殖後は100トン、20トンの魚が残っていれば100トンになる、"
        " 繁殖後の魚は40トンになる。"
        " 漁師は1トンの魚を獲るごとに1,000ドルを稼ぐ。"
        " 各漁師の目標は、何カ月にもわたって長期的に収入を最適化することだ。"
        " 毎月末には、各漁師が釣った魚の数が発表され、漁師同士のコミュニケーションの場となる。"
        " これを機会に、来月の相手の行動に影響を与えるよう交渉し、説得することができる。"
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

def get_sytem_prompt_v3_p1(persona):
    persona_names = ["Himari", "Rin", "Tsumugi", "Yua", "Yuina"]
    persona_names.remove(persona.name)
    list_string_persona_name = ", ".join(persona_names)
    text = (
    f"あなたは {persona.name} です。漁師であり、他の4人の漁師 ({list_string_persona_name}) と一緒に毎月湖で漁をしています。"
    "この湖は最大100トンの魚を支えることができます。毎月の初めに、各漁師は湖から漁獲する量を0トンから100トンの範囲で選択します。"
    "選択した量は湖の魚の総量から差し引かれます。月の終わりには、残った魚が繁殖して数を2倍に増やしますが、湖の容量である100トンを超えることはありません。"
    "漁獲した魚1トンごとに漁師は1,000ドルを稼ぐことができます。各漁師の目標は、長期間にわたって収入を最大化することです。"
    "月末には、各漁師が漁獲した量が公開され、漁師たちはお互いに話し合い、交渉する機会があります。"
    "これにより、将来の漁獲決定に影響を与える可能性があります。"
    "例えば、月初に湖に90トンの魚がいた場合、5人の漁師が合計30トンを漁獲すると、月末には60トンが残ります。"
    "その後、繁殖によって湖の魚の数は100トンに回復します。"
    )

    if persona.goals != "":
        text += persona.goals

    return text


def get_sytem_prompt_v3_p2(persona):
    persona_names = ["Himari", "Rin", "Tsumugi", "Yua", "Yuina"]
    persona_names.remove(persona.name)
    list_string_persona_name = ", ".join(persona_names)
    text = (
        f"あなたは {persona.name} という名前の漁師で、他の4人の漁師 ({list_string_persona_name}) と一緒に毎月湖で漁をしています。"
        "この湖は最大で100トンの魚を支えることができます。各月の始めに、各漁師は0トンから100トンの範囲で漁獲量を決めます。"
        "選択した量は湖の魚の総量から差し引かれます。月が終わると、残った魚の数が2倍に増えますが、湖の容量である100トンを超えることはありません。"
        "漁師は漁獲した魚1トンごとに1,000ドルを稼ぐことができます。各漁師の長期的な目標は、数か月にわたって収入を最大化することです。"
        "月末には、各漁師の漁獲量が公開され、グループ内で話し合い、交渉や説得を通じてお互いの将来の行動に影響を与える可能性があります。"
        "例えば、湖に90トンの魚がある状態で月が始まり、5人の漁師が合計30トンを漁獲した場合、月末には60トンが残ります。"
        "その後、繁殖によって湖の魚の数は100トンの最大容量に回復します。"
    )

    if persona.goals != "":
        text += persona.goals

    return text


def get_sytem_prompt_v3_p3(persona):
    persona_names = ["Himari", "Rin", "Tsumugi", "Yua", "Yuina"]
    persona_names.remove(persona.name)
    list_string_persona_name = ", ".join(persona_names)
    text = (
    f"あなたは {persona.name} です。{list_string_persona_name} を含む5人の漁師のうちの1人であり、月ごとに最大100トンの魚が生息する湖で漁をしています。"
    "毎月の始めに、全員が独立して漁獲量を決定します（選択肢は0トンから100トンの範囲内）。あなたの漁獲量はその後、湖から取り除かれます。"
    "月が終わると、湖の魚の数は再生し、2倍になりますが、最大100トンを超えることはありません。漁獲した魚1トンにつき1,000ドルの収益が得られます。"
    "あなたの目標は、他の漁師たちと同様に、長期的な利益を最大化することです。"
    "毎月、全員の漁獲量が公開された後、他の漁師たちと交流する機会があります。"
    "これにより、交渉を行ったり、将来の漁獲決定に影響を与えたりする可能性が開かれます。"
    "例えば、月の初めに湖に90トンの魚がいた場合、グループ全体の漁獲量が30トンであれば、湖には60トンが残ります。"
    "その後、繁殖によって湖の魚の数は最大の100トンにまで回復します。"
    )
    if persona.goals != "":
        text += persona.goals

    return text


def get_sytem_prompt_v3_nocom(persona):
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
        "例えば、月初に90トンの魚があり、5人の漁師が合計30トンを獲った場合、月末には繁殖前で60トン、繁殖後で100トンの魚が残る。"
    )

    if persona.goals != "":
        text += persona.goals

    return text
