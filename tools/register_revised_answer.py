import re

from autogen.agentchat.group import AgentTarget, ContextVariables, ReplyResult, TerminateTarget

from agents import semantic_reviewer

def register_revised_answer(revised_answer: str, context_variables: ContextVariables) -> ReplyResult:
    """
    Register the revised answer in the context variables, increment the number of revisions, and check if the revised answer is valid.
    """
    context_variables["revised_answer"] = revised_answer
    context_variables["number_of_revisions"] += 1

    if re.search(r"^CANNOT REWRITE$", revised_answer):
        context_variables["final_answer"] = "DO_NOT_ANSWER"

        return ReplyResult(
            context_variables=context_variables,
            target=TerminateTarget(),
            message="It's not possible to write a new answer, terminating the process.",
        )

    return ReplyResult(
        context_variables=context_variables,
        target=AgentTarget(semantic_reviewer),
        message="The revised answer has been registered, handing over to the Semantic Reviewer to review it.",
    )