from autogen.agentchat.group import AgentTarget, ContextVariables, ReplyResult

from agents import rewriter

def register_suggestions(suggestions: str, context_variables: ContextVariables) -> ReplyResult:
    """
    Register the suggestions in the context variables.
    """
    context_variables["suggestions"] = suggestions

    return ReplyResult(
        context_variables=context_variables,
        target=AgentTarget(rewriter),
        message="The suggestions have been registered, handing over to the Rewriter to write a new answer.",
    )