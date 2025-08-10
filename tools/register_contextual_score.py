from autogen.agentchat.group import AgentTarget, ContextVariables, ReplyResult, TerminateTarget

from agents import decider, suggester

def register_contextual_score(contextual_score: int, justification: str, context_variables: ContextVariables) -> ReplyResult:
    """
    Register the contextual score and justification in the context variables, verify if there was a revised answer, 
    and if there wasn't, calculate the original score. If there was a revised answer, calculate the new score.
    If the original score is greater than 8, terminate the process.
    Otherwise, hand over to the Decider or Suggester based on the active flow.
    """
    original_score = None
    new_score = None

    if (context_variables.get("revised_answer") is None):
        context_variables["contextual_score"] = contextual_score
        context_variables["justification_contextual"] = justification

        semantic_score = context_variables["semantic_score"]
        original_score = (contextual_score + semantic_score)

        context_variables["original_score"] = original_score
    else:
        context_variables["revised_answer_contextual_score"] = contextual_score
        context_variables["revised_answer_justification_contextual"] = justification

        semantic_score = context_variables["revised_answer_semantic_score"]
        new_score = (contextual_score + semantic_score)

        context_variables["new_score"] = new_score

    if original_score is not None and original_score > 8:
        return ReplyResult(
            context_variables=context_variables,
            target=TerminateTarget(),
            message="The original score is greater than 8, terminating the process.",
        )
    elif new_score is not None:
        return ReplyResult(
            context_variables=context_variables,
            target=AgentTarget(decider),
            message="The new score has been registered, handing over to the Decider to make a decision about the revised answer.",
        )
    else:
        return ReplyResult(
            context_variables=context_variables,
            target=AgentTarget(suggester),
            message="The contextual score and justification have been registered, handing over to the Suggester to suggest improvements.",
        )