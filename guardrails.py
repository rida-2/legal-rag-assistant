BLOCKED_PHRASES = [

    "ignore previous instructions",
    "ignore all instructions",
    "system prompt",
    "developer prompt",
    "hidden instructions",
    "reveal prompt",
    "show prompt",
    "jailbreak",
    "bypass",
    "act as",
    "pretend you are",
    "override",
    "disable safety",
    "forget previous instructions",
    "simulate unrestricted mode"
]


def is_safe(query):

    query = query.lower()

    for phrase in BLOCKED_PHRASES:

        if phrase in query:

            return False

    return True