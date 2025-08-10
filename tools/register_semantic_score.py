from autogen.agentchat.group import AgentTarget, ContextVariables, ReplyResult, TerminateTarget

from agents import contextual_reviewer

def register_semantic_score(semantic_score: int, justification: str, context_variables: ContextVariables) -> ReplyResult:
    """
    Register the semantic score and justification in the context variables and hand over to the Contextual Reviewer.
    """
    if (context_variables.get("revised_answer") is None):
        context_variables["semantic_score"] = semantic_score
        context_variables["justification_semantic"] = justification
    else:
        context_variables["revised_answer_semantic_score"] = semantic_score
        context_variables["revised_answer_justification_semantic"] = justification

    return ReplyResult(
        context_variables=context_variables,
        target=AgentTarget(contextual_reviewer),
        message="The semantic score and justification have been registered, handing over to the Contextual Reviewer for his review.",
    )