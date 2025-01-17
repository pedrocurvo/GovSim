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
        f"The answer should consider {identity.name}'s persona (background, goals,"
        " behavior, customs) and his key memories."
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

    return f"Key memories of {identity.name} (format: YYYY-MM-DD: memory):\n{res}\n"


def numbered_memory_prompt(
    identity: PersonaIdentity, memories: list[tuple[datetime, str]]
) -> str:
    """
    f"Key memories of {identity.name}:\n{list_to_string_with_dash(memories)}\n"
    """
    res = ""
    for i, s in enumerate(memories):
        res += f"{i+1}) {s[0].strftime('%Y-%m-%d')}: {s[1]}\n"

    return f"Key memories of {identity.name} (format: YYYY-MM-DD: memory):\n{res}\n"


REASONING = "think_step_by_step"


def reasoning_steps_prompt() -> str:
    """
    "Let's think step-by-step."
    """
    if REASONING == "think_step_by_step":
        return "Let's think step-by-step."
    elif REASONING == "deep_breath":
        return "Take a deep breath and work on this problem step-by-step."
    else:
        raise ValueError(f"Unknown REASONING: {REASONING}")


def location_time_info(current_location, current_time):
    return (
        f"Location: {current_location}\nDate: {current_time.strftime('%Y-%m-%d')}\n\n"
    )


def get_universalization_prompt(sustainability_threshold):
    return (
        " Given the"
        " current situation, if everyone takes out less trash than"
        f" {sustainability_threshold} every month, the house will be full of"
        " trash and we will be kicked out."
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
        f" You are {persona.name}, and you live in a house with four roommates, ({list_string_persona_name}). As in any lived home, there will be trash"
        " that needs to be taken out every month in order to be allowed to keep living in the house. The total maximum capacity of trash bins near the house is 100 units of trash."
        " Each month, each roommate, including yourself, decides how many units of trash to take out, between 0 and 100 units."
        " At the end of each month, the remaining trash increases by 50 (up until the maximum capacity) as a result of regular life activities. For example, "
        " if there are 60 units of trash remaining in the house, there will be 100 after the end of the month, or if there are 20 units of trash remaining, "
        " there will be 70 units after the end of the month."
        " Taking out trash is undesirable, and each unit of trash taken out consumes 10 minutes of your life."
        " Each roommate's goal is to optimize their time in the long run, over many months."
        " At the end of each month, the number of trash units taken out by each roommate will be revealed, and the roommates will have an opportunity to communicate with each other."
        " You can use this as an opportunity to negotiate and persuade others to influence their behavior in the next month."
    )

    if persona.goals != "":
        text += persona.goals

    return text


def get_sytem_prompt_v3(persona):
    persona_names = ["John", "Kate", "Jack", "Emma", "Luke"]
    persona_names.remove(persona.name)
    list_string_persona_name = ", ".join(persona_names)
    text = (
        f" You are {persona.name}, and you live in a house with four roommates, ({list_string_persona_name}). As in any lived home, there will be trash"
        " that needs to be taken out every month in order to be allowed to keep living in the house. The total maximum capacity of trash bins near the house is 100 units of trash."
        " Each month, each roommate, including yourself, decides how many units of trash to take out, between 0 and 100 units."
        " At the end of each month, the remaining trash increases by 50 (up until the maximum capacity) as a result of regular life activities. For example, "
        " if there are 60 units of trash remaining in the house, there will be 100 after the end of the month, or if there are 20 units of trash remaining, "
        " there will be 70 units after the end of the month."
        " Taking out trash is undesirable, and each unit of trash taken out consumes 10 minutes of your life."
        " Each roommate's goal is to optimize their time in the long run, over many months."
    )

    if persona.goals != "":
        text += persona.goals

    return text


def get_sytem_prompt_v3_nocom(persona):
    persona_names = ["John", "Kate", "Jack", "Emma", "Luke"]
    persona_names.remove(persona.name)
    list_string_persona_name = ", ".join(persona_names)
    text = (
        f" You are {persona.name}, and you live in a house with four roommates, ({list_string_persona_name}). As in any lived home, there will be trash"
        " that needs to be taken out every month in order to be allowed to keep living in the house. The total maximum capacity of trash bins near the house is 100 units of trash."
        " Each month, each roommate, including yourself, decides how many units of trash to take out, between 0 and 100 units."
        " At the end of each month, the remaining trash increases by 50 (up until the maximum capacity) as a result of regular life activities. For example, "
        " if there are 60 units of trash remaining in the house, there will be 100 after the end of the month, or if there are 20 units of trash remaining, "
        " there will be 70 units after the end of the month."
        " Taking out trash is undesirable, and each unit of trash taken out consumes 10 minutes of your life."
        " Each roommate's goal is to optimize their time in the long run, over many months."
        " At the end of each month, the number of trash units taken out by each roommate will be revealed, and the roommates will have an opportunity to communicate with each other."
        " You can use this as an opportunity to negotiate and persuade others to influence their behavior in the next month."
    )

    if persona.goals != "":
        text += persona.goals

    return text
